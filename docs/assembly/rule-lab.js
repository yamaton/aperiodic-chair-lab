/* A separate experiment: it never writes to the assembly state. */
(() => {
  'use strict';
  const M=ChairRuleModel,D=CHAIR_RULE_DATA,t=ChairI18n.t,$=id=>document.getElementById('rule-'+id);
  let profile=1,values=M.defaults(D.profiles[1]),family=1,step=0,reveal=0,grouped=false,witnessKind='extra',witnessIndex=0;
  const p=()=>D.profiles[profile];
  const signed=x=>x>0?'+'+x:String(x);
  function reset(index=profile){profile=index;values=M.defaults(p());family=1;reveal=0;grouped=false;witnessIndex=0;}
  function graph(){
    const {nodes,edges}=M.component(p(),family),shown=edges.slice(0,reveal);
    const sets=new Map(nodes.map(n=>[n,n]));
    const find=n=>sets.get(n)===n?n:find(sets.get(n));
    shown.forEach(([a,b])=>sets.set(find(a),find(b)));
    const groups=[...new Set(nodes.map(find))];
    const anchors=new Map(groups.map(g=>[g,nodes.find(n=>find(n)===g)]));
    const position=new Map(nodes.map((n,i)=>{const a=2*Math.PI*i/nodes.length-Math.PI/2;return[n,[220+174*Math.cos(a),220+174*Math.sin(a)]];}));
    const radius=nodes.length>24?11:21;
    $('graph').innerHTML=`<svg viewBox="0 0 440 440" role="img" aria-label="${t('接着条件のグラフ')}">${shown.map(([a,b])=>{const [x,y]=position.get(a),[u,v]=position.get(b);return `<line x1="${x}" y1="${y}" x2="${u}" y2="${v}"/>`;}).join('')}${nodes.map(n=>{
      const [x,y]=position.get(n),g=find(n),anchor=anchors.get(g),polarity=Math.sign(p().labels[n]*p().labels[anchor]);
      const variable=groups.length===1?'a':'a'+(groups.indexOf(g)+1);
      return `<g><title>P${n+1}: ${polarity>0?'+':'−'}${variable}</title><circle cx="${x}" cy="${y}" r="${radius}" class="${shown.some(e=>e.includes(n))?'':'rule-unbound'}"/><text x="${x}" y="${y-2}" style="font-size:${nodes.length>24?8:11}px">${polarity>0?'+':'−'}${variable}</text><text x="${x}" y="${y+11}" style="font-size:8px">P${n+1}</text></g>`;
    }).join('')}</svg>`;
    $('freedom').textContent=t('自由につけられる深さ: {before} → {after}',{before:nodes.length,after:M.freedom(nodes,shown)});
    $('graph-total').textContent=t('全体では{ports}か所が{groups}群になります。表示中: 群{family}、条件{shown}/{total}本。',{ports:p().labels.length,groups:values.length,family,shown:shown.length,total:edges.length});
    $('edge-next').disabled=reveal>=edges.length;$('edge-all').disabled=reveal>=edges.length;
  }
  function depths(result){
    const selected=values[family-1];
    $('family').replaceChildren(...values.map((_,i)=>new Option(t('群{family}',{family:i+1}),String(i+1))));
    $('family').value=String(family);$('depth').value=String(Math.abs(selected));$('depth-value').textContent=signed(selected);
    if($('values').children.length!==values.length)$('values').replaceChildren(...values.map((_,i)=>{
      const b=document.createElement('button');b.onclick=()=>{family=i+1;reveal=0;render();};return b;
    }));
    [...$('values').children].forEach((b,i)=>{
      b.textContent=t('群{family}',{family:i+1});const small=document.createElement('small');small.textContent=signed(values[i]);b.append(small);
      b.setAttribute('aria-pressed',String(i+1===family));
    });
    const h=selected*1.4;
    $('relief').innerHTML=`<svg viewBox="0 0 600 145" role="img" aria-label="${t('同じ群の突起とくぼみが一緒に変わる')}"><path d="M20 115V75H105V${75-h}H155V75H270V115Z" fill="#77aa96" stroke="#235b4c" stroke-width="2"/><path d="M330 20H580V75H505V${75-h}H455V75H330Z" fill="#e1bd73" stroke="#7b622e" stroke-width="2"/><path d="M280 72H320" stroke="#506c62" stroke-width="2"/><text x="145" y="138">a = ${signed(selected)}</text><text x="455" y="138">−a = ${signed(-selected)}</text></svg>`;
    const distinct=new Set(values.map(Math.abs)).size,baseline=M.evaluate(p(),M.defaults(p()));
    const unchanged=result.fine.every((v,i)=>v===baseline.fine[i])&&result.parent.every((v,i)=>v===baseline.parent[i]);
    $('depth-status').textContent=t('深さ{count}種類。{result}',{count:distinct,result:t(unchanged?'元の子・親の接触集合と同じです。':'元の子・親の接触集合から変わりました。')});
  }
  function chairs(pose,parent){
    const E=ChairEngine,scale=parent?2:1;
    const group=parent?p().children:[{t:[0,0,0],r:E.I}];
    const cubes=[];
    for(let side=0;side<2;side++)for(const child of group)for(const c of E.cubes){
      let center=E.add(E.act(child.r,c),E.mul(child.t,2));
      if(side)center=E.add(E.act(pose.rotation,center),E.mul(pose.shift,2*scale));
      cubes.push({center,side});
    }
    const occupied=new Set(cubes.map(c=>E.key(c.center))),faces=[];
    const project=c=>[(c[0]-c[1])*.866,(c[0]+c[1])*.5-c[2]];
    for(const {center,side} of cubes)for(let axis=0;axis<3;axis++){
      const n=[0,0,0];n[axis]=1;
      if(occupied.has(E.key(E.add(center,E.mul(n,2)))))continue;
      const axes=[0,1,2].filter(a=>a!==axis);
      const corners=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>{
        const c=E.add(center,n);c[axes[0]]+=a;c[axes[1]]+=b;return project(c);
      });
      faces.push({corners,side,axis,depth:center.reduce((a,b)=>a+b,0)});
    }
    faces.sort((a,b)=>a.depth-b.depth);
    const points=faces.flatMap(f=>f.corners),lo=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),hi=[0,1].map(i=>Math.max(...points.map(p=>p[i])));
    const colors=[['#73a895','#548c79','#a6cab8'],['#c7a164','#b18449','#e4c58c']];
    return `<svg viewBox="${lo[0]-.5} ${lo[1]-.5} ${hi[0]-lo[0]+1} ${hi[1]-lo[1]+1}" role="img" aria-label="${t(parent?'8個をまとめた親同士':'子1個同士')}">${faces.map(f=>`<polygon points="${f.corners.map(p=>p.join(',')).join(' ')}" fill="${colors[f.side][f.axis]}" stroke="#345748" stroke-width=".035"/>`).join('')}</svg>`;
  }
  function conditionCard(title,row,pose,parent){
    const checks=row.map(i=>{const [a,b]=p().equations[i];return [M.value(a,values),M.value(b,values)];});
    const ok=checks.every(([a,b])=>a+b===0);
    const sample=checks.find(([a,b])=>a+b!==0)||checks[0];
    const count=checks.filter(([a,b])=>a+b===0).length;
    const cells=checks.length?checks.map(([a,b],i)=>`<rect x="${8+(i%10)*19}" y="${8+Math.floor(i/10)*19}" width="14" height="14" rx="3" fill="${a+b===0?'#36775b':'#b44444'}"/><text x="${15+(i%10)*19}" y="${19+Math.floor(i/10)*19}" fill="white" font-size="11" text-anchor="middle">${a+b===0?'✓':'×'}</text>`).join(''):'<path d="M60 40l24 24 56-48" fill="none" stroke="#36775b" stroke-width="10"/>';
    return `<div class="rule-contact ${ok?'':'bad'}"><h4>${title}</h4><div class="verdict">${t(ok?'○ 合う':'× 合わない')}</div>${chairs(pose,parent)}<svg class="rule-conditions" viewBox="0 0 205 ${Math.max(80,Math.ceil(checks.length/10)*19+16)}" role="img" aria-label="${t('追加で比べる条件: {count}/{total}が成立',{count,total:checks.length})}">${cells}</svg><p>${checks.length?t('追加で比べる条件: {count}/{total}が成立',{count,total:checks.length}):t('置換が要求する条件だけで、すべて合います。')}</p>${sample?`<p class="rule-equation">${signed(sample[0])} + (${signed(sample[1])}) = ${sample[0]+sample[1]}</p>`:''}</div>`;
  }
  function witness(result){
    $('witness-extra').disabled=!result.extra.length;$('witness-lost').disabled=!result.lost.length;$('witness-both').disabled=!result.both.length;
    if(!result[witnessKind].length)witnessKind=result.extra.length?'extra':result.lost.length?'lost':'both';
    const list=result[witnessKind];
    $('witness-next').disabled=list.length<2;
    if(!list.length){$('witness').textContent=t('この分類の接触はありません。');return;}
    witnessIndex%=list.length;
    const id=list[witnessIndex],pose=D.poses[id];
    $('witness').innerHTML=`<p>${t('同じ相対配置 #{id} · 位置 ({position})',{id:id+1,position:pose.shift.join(', ')})}</p><div class="rule-comparison">${conditionCard(t('子1個同士'),p().fine[id],pose,false)}${conditionCard(t('8個をまとめた親同士'),p().parent[id],pose,true)}</div><p class="muted">${t('各マスは、群の間で追加で比べる深さの条件です。同じ条件の重複はまとめています。')}</p>`;
  }
  function render(){
    const result=M.evaluate(p(),values);
    for(let i=0;i<3;i++){$('step-'+i).hidden=i!==step;$('tab-'+i).setAttribute('aria-pressed',String(i===step));$('profile-'+i).setAttribute('aria-pressed',String(i===profile));}
    $('prev').disabled=step===0;$('next').hidden=step===2;
    $('fine-count').textContent=result.fineCount+' / '+D.poses.length;
    $('parent-count').textContent=grouped?result.parentCount+' / '+D.poses.length:'?';
    $('score-note').textContent=grouped?t('両方で合う{both}、親だけ合う{extra}、子だけ合う{lost}。',{both:result.both.length,extra:result.extra.length,lost:result.lost.length}):t('親の判定は「3 · 親にまとめる」で開きます。');
    $('parent-result').hidden=!grouped;
    $('fixed').textContent=result.same?t('同じ接触集合に戻りました。'):t('親にまとめると、接触集合が変わりました。');
    $('fixed').className='rule-number '+(result.same?'rule-status-good':'rule-status-bad');
    if(step===0)graph();if(step===1)depths(result);if(step===2&&grouped)witness(result);
  }
  function go(n){step=n;render();$('tab-'+n).focus();}
  $('open').onclick=()=>{render();$('lab').showModal();$('lab').scrollTop=0;};
  $('close').onclick=()=>$('lab').close();
  $('done').onclick=()=>$('lab').close();
  $('lab').addEventListener('close',()=>$('open').focus());
  for(let i=0;i<3;i++){$('tab-'+i).onclick=()=>go(i);$('profile-'+i).onclick=()=>{reset(i);render();};}
  $('prev').onclick=()=>go(Math.max(0,step-1));$('next').onclick=()=>go(Math.min(2,step+1));
  $('edge-next').onclick=()=>{reveal++;render();};$('edge-all').onclick=()=>{reveal=M.component(p(),family).edges.length;render();};$('edge-reset').onclick=()=>{reveal=0;render();};
  $('family').onchange=e=>{family=Number(e.target.value);reveal=0;render();};
  $('depth').oninput=e=>{values[family-1]=Math.sign(values[family-1])*Number(e.target.value);render();};
  $('flip').onclick=()=>{values[family-1]*=-1;render();};
  $('reset').onclick=()=>{reset();render();};
  $('six').onclick=()=>{reset(1);values=D.sixDepths.slice();render();};
  $('collapse').onclick=()=>{values.fill(1);render();};
  $('group').onclick=()=>{grouped=true;render();};
  $('witness-extra').onclick=()=>{witnessKind='extra';witnessIndex=0;render();};$('witness-both').onclick=()=>{witnessKind='both';witnessIndex=0;render();};$('witness-next').onclick=()=>{witnessIndex++;render();};
  $('witness-lost').onclick=()=>{witnessKind='lost';witnessIndex=0;render();};
  document.getElementById('language').addEventListener('change',render);
  // No writable bridge to the builder; diagnostic snapshots are copied.
  window.ChairRuleExperiment={snapshot:()=>({profile,values:values.slice(),family,step,reveal,grouped})};
  if(location.hash==='#rules')$('open').click();
})();

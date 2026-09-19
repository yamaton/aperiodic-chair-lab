/* Read-only experiment: its choices never enter assembly history. */
const ChairParentLab={create(model,t,onSelect){
  const $=id=>document.getElementById(id);
  let face=3,partner='A',turn=0;
  const arrow=u=>u[0]===1?'→':u[0]===-1?'←':u[1]===1?'↑':'↓';
  const symbol=f=>f.motif+arrow(f.u);
  const verdict=ok=>t(ok?'○ 合う':'× 合わない');
  function diagram(el,panels,results){
    el.setAttribute('role','img');
    el.setAttribute('aria-label',t('左上・右上・左下・右下: {panels}',{panels:panels.map((p,i)=>symbol(p)+(results?' '+t(results[i]?'合う':'合わない'):'')).join(', ')}));
    el.innerHTML=`<svg viewBox="0 0 144 144" aria-hidden="true">${panels.map((p,i)=>{
      const x=p.x>0?74:2,y=p.y>0?2:74,checked=!!results,ok=results?.[i];
      return `<g class="${checked?(ok?'parent-good':'parent-bad'):'parent-neutral'}"><rect x="${x}" y="${y}" width="68" height="68" rx="5"/><text x="${x+34}" y="${y+39}" text-anchor="middle" class="parent-glyph">${symbol(p)}</text>${checked?`<text x="${x+6}" y="${y+14}" class="parent-mark">m${'₁₂₃₄'[i]}</text><text x="${x+34}" y="${y+59}" text-anchor="middle" class="parent-verdict">${verdict(ok)}</text>`:''}</g>`;
    }).join('')}</svg>`;
  }
  function render(){
    const options=model.faces.map(f=>[String(f.id),t('親の面{face} · {motif}',{face:f.id+1,motif:f.motif})]);
    const signature=JSON.stringify(options);
    if($('parent-face').dataset.options!==signature){
      $('parent-face').replaceChildren(...options.map(([v,label])=>new Option(label,v)));
      $('parent-face').dataset.options=signature;
    }
    $('parent-face').value=String(face);$('parent-partner').value=partner;
    const result=model.compare(face,partner,turn),checks=result.pairs.map(p=>p.ok);
    diagram($('parent-word-diagram'),result.pairs.map(p=>p.a));
    $('parent-word-symbol').textContent=symbol(result.a);
    diagram($('parent-left'),result.pairs.map(p=>p.a),checks);
    diagram($('parent-right'),result.pairs.map(p=>p.b),checks);
    for(const [id,f] of [['parent-left-symbol',result.a],['parent-right-symbol',result.b]]){
      $(id).textContent=symbol(f);$(id).className=result.parent.ok?'parent-good':'parent-bad';
    }
    const out=$('parent-equivalence');
    out.dataset.fine=String(checks.every(Boolean));out.dataset.coarse=String(result.parent.ok);
    out.className=result.parent.ok?'parent-good':'parent-bad';
    out.replaceChildren();
    for(const text of [
      t('小さい面: {count}/4組が合う',{count:checks.filter(Boolean).length}),
      checks.map(Number).join(' × ')+' = '+Number(checks.every(Boolean))+'　⇔　'+t('親の判定: {value}',{value:Number(result.parent.ok)}),
      t('親: {left} と {right} · {result}',{left:symbol(result.a),right:symbol(result.b),result:verdict(result.parent.ok)})
    ]){const p=document.createElement('p');p.textContent=text;out.append(p);}
    $('parent-dictionary').replaceChildren(...['A','B','C'].map(motif=>{
      const id=model.faces.find(f=>f.motif===motif).id,word=model.compare(id,'A',0);
      const card=document.createElement('div'),drawing=document.createElement('div'),label=document.createElement('strong');
      diagram(drawing,word.pairs.map(p=>p.a));label.textContent='⇔ '+motif+'→';card.append(drawing,label);return card;
    }));
  }
  function select(id,focusView=false){if(id<0)return;face=id;render();onSelect(id,focusView);}
  $('parent-face').onchange=e=>select(Number(e.target.value),true);
  $('parent-partner').onchange=e=>{partner=e.target.value;render();};
  $('parent-turn-left').onclick=()=>{turn=(turn+1)%4;render();};
  $('parent-turn-right').onclick=()=>{turn=(turn+3)%4;render();};
  return {render,select,get face(){return face;}};
}};

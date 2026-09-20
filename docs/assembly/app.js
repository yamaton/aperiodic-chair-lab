/* Offline interaction prototype; rendering never decides contact validity. */
(() => {
  'use strict';
  const E=ChairEngine, F=ChairFeedback, rules=E.create(CHAIR_DATA), $=id=>document.getElementById(id);
  const {t}=ChairI18n, translateTemplate=ChairI18n.bind(document.documentElement);
  ChairI18n.setLanguage(window.CHAIR_DEMO?parent.document.documentElement.lang:ChairI18n.initialLanguage());
  $('language').value=document.documentElement.lang;translateTemplate();
  const {add,sub,mul,dot,cross,act,product,eq,key,poseKey,clone,I}=E;
  const initial=()=>({tiles:[{t:[0,0,0],r:I.slice()}],pending:true,op:null,ref:'',level:0,
    grouped:false,unit:null,anchor:{t:[0,0,0],r:I.slice()}});
  let history=new E.History(initial()), mode='guided', allFaces=false, explainRef=null;
  let hintStep=0, hintMessage='', highlight=null, parentView='children', inspection=null;
  const parentModel=ChairParentRules.create(E,rules);
  const parentLab=ChairParentLab.create(parentModel,t,(id,focusView)=>{
    if(focusView){
      const p=rules.parent(state().tiles),f=parentModel.faces[id];
      if(p){const n=act(p.r,f.n);pitch=Math.asin(n[2]*.85);yaw=Math.atan2(n[0],n[1]);
        viewCenter=add(p.t,act(p.r,f.c));zoom=1.1;}
    }
    draw();
  });
  let yaw=.8,pitch=.6, zoom=1, viewCenter=[0,0,0], oldView=null, hitFaces=[];
  let pieceYaw=.8,piecePitch=.6;
  let restartMode=null;
  const state=()=>history.state;
  const camera=()=>({yaw,pitch,zoom,viewCenter:viewCenter.slice()});
  function restoreCamera(c){({yaw,pitch,zoom,viewCenter}=clone(c));}
  const samePose=(a,b)=>a&&b&&poseKey(a)===poseKey(b);
  function commit(label, fn) {
    if (inspection) return;
    const next = clone(state());
    fn(next);
    history.commit(label, next);
    explainRef = null;
    highlight = null;
  }
  function adjust(fn) {
    if (inspection) return;
    const next = clone(state());
    fn(next);
    history.adjust(next);
    explainRef = null;
    highlight = null;
  }
  function resetHint() {
    hintStep = 0;
    hintMessage = '';
  }
  function selectable(){return rules.exposed(state().tiles);}
  function currentResult(){const s=state();return rules.check(s.tiles,s.pending?s.op:null);}
  function resultMessage(result){
    if(result.overlap.length)return t('ブロックの内部が重なっています');
    if(!result.contacts.length)return t('面を選んでください');
    const bad=result.contacts.filter(c=>!c.ok).length;
    return bad?t('{total}面中 {bad}面が不適合',{total:result.contacts.length,bad}):t('接触{count}面すべて適合',{count:result.contacts.length});
  }
  function chosenContact(result){return result.contacts.find(c=>c.a.ref===(explainRef||state().ref))||result.contacts[0];}
  function guideMatches(tiles=state().tiles){return rules.onGoal(tiles,state().anchor);}
  function setOptions(select,options,value){
    const signature=JSON.stringify(options);
    if(select.dataset.options!==signature){select.replaceChildren(...options.map(([v,label])=>new Option(label,v)));select.dataset.options=signature;}
    select.value=value;
  }
  function selectTarget(ref){
    const s=state();if(inspection||s.grouped||s.tiles.length>=8)return;
    if(!selectable().some(f=>f.ref===ref))return;
    resetHint();
    // Selecting the bonded face does not choose or position the moving face.
    const fn=d=>{d.pending=true;d.ref=ref;d.op=null;};
    if(!s.pending)commit('部品の追加',fn);else adjust(fn);
    render();
  }
  function selectMovingFace(faceId){
    const s=state();if(inspection||!s.pending||!s.ref)return;
    const options=rules.candidates(s.tiles,s.ref,true).filter(c=>c.face===faceId);
    // Keep the closest orientation, without selecting a correct handshake for the player.
    const orientation=s.op?.r||I;
    options.sort((a,b)=>dot(b.p.r,orientation)-dot(a.p.r,orientation));
    const chosen=options[0];if(!chosen)return;
    const target=selectable().find(f=>f.ref===s.ref);
    if(!rules.handshake(target,rules.placedFaces(chosen.p)[faceId]).patterns)allFaces=true;
    if(samePose(chosen.p,s.op)){explainRef=null;render();return;}
    adjust(d=>{d.op=chosen.p;});
    render();
  }
  function movingFaceId(boundary=selectable()){
    const s=state(),target=boundary.find(f=>f.ref===s.ref);
    if(!s.op||!target)return null;
    return rules.placedFaces(s.op).find(f=>eq(f.c,target.c)&&eq(f.n,mul(target.n,-1)))?.id??null;
  }
  function arrowName(u,a){const v=[dot(u,a.u),dot(u,cross(a.n,a.u))];return v[0]===1?'→':v[0]===-1?'←':v[1]===1?'↑':'↓';}
  function faceSVG(face,base,label,expected){
    const uv=[dot(face.u,base.u),dot(face.u,cross(base.n,base.u))];
    const line=(u,dashed)=>`<path d="M 52 76 L ${52+u[0]*29} ${76-u[1]*29}" stroke="${dashed?'#a87747':'#176b64'}" stroke-width="${dashed?2:3}" ${dashed?'stroke-dasharray="3 3"':''}/><path d="M ${52+u[0]*29-u[0]*8-u[1]*4} ${76-u[1]*29+u[1]*8-u[0]*4} L ${52+u[0]*29} ${76-u[1]*29} L ${52+u[0]*29-u[0]*8+u[1]*4} ${76-u[1]*29+u[1]*8+u[0]*4}" fill="none" stroke="${dashed?'#a87747':'#176b64'}" stroke-width="2"/>`;
    const wanted=expected?[dot(expected,base.u),dot(expected,cross(base.n,base.u))]:null;
    return `<div class="face-card">${label}<svg viewBox="0 0 104 115" role="img" aria-label="${t('{label} {motif}、矢印{arrow}',{label,motif:face.motif,arrow:arrowName(face.u,base)})}"><rect x="3" y="4" width="98" height="106" rx="7" fill="#edf3ea" stroke="#c4d7c9"/><text x="52" y="38" text-anchor="middle" font-size="25" fill="#213c45">${face.motif}</text>${wanted?line(wanted,true):''}<g class="face-arrow">${line(uv,false)}</g></svg></div>`;
  }
  // One exact snapshot per UI/frame update. Camera and hover share these results.
  function displayState() {
    const s = state();
    const boundary = selectable();
    return {s, boundary, result: currentResult(), movingFaceId: movingFaceId(boundary)};
  }
  function renderContactFeedback(frame){
    const {s,result}=frame,inspecting=!!inspection;
    const remaining=8-s.tiles.length-Number(s.pending);
    // Preserve control positions while the comparison temporarily shows progress.
    $('compare-content').style.minHeight=motion?Math.max(150,$('compare-content').getBoundingClientRect().height)+'px':'';
    const contact=motion?null:chosenContact(result);
    if(contact){
      const appearance=F.describe(contact);
      const effect=!inspecting&&appearance.className?' '+appearance.className:'';
      $('compare-content').innerHTML=`<div class="face-pair${effect}">${faceSVG(contact.a,contact.a,t('接着済み'))}${faceSVG(contact.b,contact.a,t('取り付け中'),$('why').open&&contact.patterns?contact.expected:null)}</div><p class="muted">${t('この面: {result}',{result:t(appearance.detail)})}</p>`;
    }else $('compare-content').innerHTML=`<p class="muted">${motion?t('位置と向きを調整中…'):t('面を選ぶと、二つの矢印がここに並びます。')}</p>`;
    const other=contact&&contact.a.ref!==s.ref;
    $('rotate-left').hidden=!!other;$('rotate-right').hidden=!!other;$('return-face').hidden=!other;
    for(const id of ['rotate-left','rotate-right'])$(id).disabled=!s.op||!s.pending||inspecting;
    $('status').textContent=motion?t('位置と向きを調整中…'):s.pending?(s.ref&&!s.op?t('取り付ける部品の面をクリック'):resultMessage(result)):s.tiles.length===8?t('この作業面の材料はすべて使用中です。'):t('接着済み{count}個。残り材料{remaining}個。',{count:s.tiles.length,remaining});
    if(!motion&&mode==='guided'&&s.op&&result.ok&&!guideMatches([...s.tiles,s.op]))$('status').textContent+=t(' 案内中の完成例とは異なる配置です。');
    $('status').className='status '+(!motion&&s.pending?(s.op?F.status(result):''):'');
    $('why-text').textContent=motion?t('位置と向きを調整中…'):result.overlap.length?t('内部が重なる単位立方体が{count}個あります。別の候補を試してください。',{count:result.overlap.length}):t('選んだ一面だけでなく、触れているすべての面を確認します。');
    $('contacts').replaceChildren(...(motion?[]:result.contacts).map((c,i)=>{
      const button=document.createElement('button');button.textContent=t('接触{number} · {a}/{b} · {result}',{number:i+1,a:c.a.motif,b:c.b.motif,result:t(F.describe(c).label)});
      button.setAttribute('aria-pressed',String(c.a.ref===(explainRef||s.ref)));
      button.onclick=()=>{explainRef=c.a.ref;render();};return button;
    }));
    $('problem-view').hidden=!!motion||!result.contacts.some(c=>!c.ok);
    $('attach').hidden=!s.pending;
  }
  function render(){
    syncMotion();
    const home=$('project-home');if(home)home.href='../?lang='+document.documentElement.lang;
    const frame=displayState(),{s}=frame, parent=rules.parent(s.tiles), inspecting=!!inspection;
    const remaining=8-s.tiles.length-Number(s.pending);
    const inGuide=mode==='guided'&&guideMatches();
    $('level').textContent=t('階層 {level} · 基準長 {scale}倍',{level:s.level,scale:2**s.level});
    $('progress').textContent=inspecting?t('内部を観察中'):s.grouped?t('親ができました'):inGuide?t('親の組立 {count}/8',{count:s.tiles.length}):t('接着済み{count} · 調整中{pending} · 残り{remaining}',{count:s.tiles.length,pending:Number(s.pending),remaining});
    $('guided').setAttribute('aria-pressed',String(mode==='guided'));$('free').setAttribute('aria-pressed',String(mode==='free'));
    $('undo').disabled=inspecting||!history.canUndo;$('redo').disabled=inspecting||!history.canRedo;
    $('undo').title=history.canUndo?t('{action}を戻す',{action:t(history.entries[history.index].label)}):t('戻す操作はありません');
    $('redo').title=history.canRedo?t('{action}をやり直す',{action:t(history.entries[history.index+1].label)}):t('やり直す操作はありません');
    for(const id of ['guided','free','restart'])$(id).disabled=inspecting;
    $('editing').hidden=inspecting||s.grouped||!!parent;
    $('parent-actions').hidden=inspecting||!parent;
    $('group').hidden=s.grouped;$('parent-summary').hidden=!s.grouped;
    $('inspection-note').hidden=!inspecting;
    $('inspect').hidden=inspecting||(!s.unit&&!s.grouped);
    $('inspect-up').hidden=!inspecting||inspection.path.length<=1;
    $('inspect-return').hidden=!inspecting;
    const canDeeper=inspecting&&!!inspectScene().unit.childUnit;
    $('inspect-choice').hidden=inspecting?!canDeeper:!s.unit||s.grouped;
    $('inspect-deeper').hidden=!canDeeper;
    const choice=$('inspect-tile').value;
    setOptions($('inspect-tile'),(inspecting?rules.group:s.tiles).map((p,i)=>[String(i),t('部品{number}',{number:i+1})]),choice||'0');
    $('inspection-path').textContent=inspecting?t('作業中の組立')+' → '+inspection.path.map(p=>t('部品{number}の内部',{number:p.tile+1})).join(' → '):'';
    document.querySelector('.workspace').classList.toggle('studying-parent',s.grouped&&!inspecting);
    parentLab.render();
    $('scene-caption').textContent=inspecting?t('各部品自身の座標で内部を表示しています。子の選択は3Dまたは一覧から。接着と履歴の操作は「組立に戻る」で再開できます。'):s.grouped?t('面をクリックすると、対応する4枚と親の記号を比べられます。金色の枠が選んだ面です。'):t('面をクリックで選択 · ドラッグで視点を回転 · 接着済みの群は固定されています');
    $('instruction-title').textContent=inspecting?t('作業を保ったまま、内部を見る'):s.grouped?t('同じルールで、次の階層へ'):parent?t('大きなブロックができました'):!s.pending?t('次の部品を用意する'):s.ref?t('向きを合わせて接着する'):t('取り付けたい面を選ぶ');
    $('instruction').textContent=inspecting?t('戻るだけで先ほどの操作を再開できます。'):s.grouped?t('まず4枚の接触条件を調べ、親の記号と比べてみましょう。'):parent?t('8個の位置と向きが、親の配置に一致しました。'):mode==='guided'&&!inGuide?t('案内の完成例とは異なる配置です。Undoで戻るか、自由に組み続けられます。'):s.pending?t('AはA、BはC。矢印の向きも比べてみましょう。'):s.tiles.length===8?t('材料をすべて使用中です。この8個は一つの親の配置ではありません。Undoで組み替えられます。'):t('接着した部品は組立の一部になります。');
    const {boundary}=frame;
    $('view-face').disabled=inspecting||!boundary.some(f=>f.ref===(highlight||s.ref));
    setOptions($('target-face'),[['',t('面を選んでください')],...boundary.map(f=>[f.ref,t('部品{piece} · 面{face} {motif} · ({position})',{piece:f.tile+1,face:f.id+1,motif:f.motif,position:mul(f.c,.5).join(', ')})])],s.ref);
    $('target-face').disabled=inspecting||s.grouped||s.tiles.length>=8;
    $('candidate-controls').hidden=!s.ref||!s.pending;
    $('all-faces').checked=allFaces;
    let list=s.ref?rules.candidates(s.tiles,s.ref,allFaces):[];
    if(s.op&&!list.some(c=>samePose(c.p,s.op)))list=rules.candidates(s.tiles,s.ref,true);
    const a=boundary.find(f=>f.ref===s.ref);
    setOptions($('candidate'),list.map(c=>[poseKey(c.p),t('{motif} · 面{face} · 矢印{arrow}{overlap}',{motif:c.motif,face:c.face+1,arrow:arrowName(rules.placedFaces(c.p)[c.face].u,a),overlap:c.result.overlap.length?t(' · 重なり'):''})]),s.op?poseKey(s.op):'');
    $('candidate-note').textContent=allFaces?t('全模様を表示中。模様が違う候補も調べられます。'):t('組み合わせ可能な模様を優先。候補を選ぶと3D上の位置も変わります。');
    renderContactFeedback(frame);
    $('add').hidden=s.pending;$('add').disabled=s.tiles.length>=8||inspecting;
    $('cancel').hidden=!s.pending;$('cancel').disabled=inspecting;
    $('hint').hidden=mode!=='guided';$('hint').disabled=inspecting||!inGuide||s.tiles.length>=8;
    $('hint').textContent=[t('ヒントを見る'),t('矢印のヒントを見る'),t('具体的な候補を表示'),t('候補を表示しました')][Math.min(hintStep,3)];
    $('hint-text').textContent=(hintMessage?hintMessage():'')||(!inGuide&&mode==='guided'?t('完成例へ戻るには「元に戻す」を使います。接着そのものが間違いとは限りません。'):'');
    for(const [id,value] of [['show-boundary','children'],['show-shell','shell'],['show-parent','rules']])$(id).setAttribute('aria-pressed',String(parentView===value));
    drawPiecePicker(frame.movingFaceId);updateScene(frame);
  }

  // A simple orthographic canvas renderer with face hit testing; no network/GPU dependencies.
  const canvas=$('scene'),ctx=canvas.getContext('2d');
  // Read the shared CSS palette once; camera/animation frames do not read styles.
  const contactCSS=getComputedStyle(document.documentElement);
  const contactColor=name=>contactCSS.getPropertyValue('--contact-'+name).trim();
  const contactPalette={
    goodBorder:contactColor('good-border'), goodFill:contactColor('good-fill'),
    badBorder:contactColor('bad-border'), badFill:contactColor('bad-fill'),
    emphasis:contactColor('emphasis'), glow:contactColor('glow'),
  };
  const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
  let motion=null,motionState=null,motionPausedAt=null;
  function motionSample(){return motion?ChairMotion.sample(motion,(motionPausedAt??performance.now())-motion.started):null;}
  function clearMotion(){motion=null;motionState=null;motionPausedAt=null;}
  function finishMotion() {
    motion = null;
    motionPausedAt = null;
    const frame = displayState();
    renderContactFeedback(frame);
    updateScene(frame);
  }
  function pauseMotion(){if(motion&&motionPausedAt===null)motionPausedAt=performance.now();draw();}
  function resumeMotion(){if(motion&&motionPausedAt!==null)motion.started+=performance.now()-motionPausedAt;motionPausedAt=null;draw();}
  function syncMotion(){
    const s=state(),pose=placementPose(),previous=motionState;
    const next={pose,op:s.op,ref:s.ref,assembly:JSON.stringify([s.tiles,s.level])};
    if(!pose||inspection||s.grouped||!previous?.pose||previous.assembly!==next.assembly){
      motion=null;motionPausedAt=null;
    }else if(!samePose(previous.pose,pose)){
      const from=motionSample()?.pose||previous.pose;
      const oldFace=previous.op&&!motion?selectable().find(f=>f.ref===previous.ref):null;
      motion=reducedMotion.matches||document.hidden?null:{...ChairMotion.transition(from,pose,oldFace?.n),started:performance.now()};
      if(!motion?.duration)motion=null;
      motionPausedAt=null;
    }
    motionState=next;
  }
  let scenePointer=null,sceneHover=null,pickerPointer=null,pickerHover=null,pickerFocus=null,effectFrame=0,lastEffectDraw=0;
  function interactionPhase(){
    const s=state();
    return inspection||s.grouped||s.tiles.length>=8||!s.pending?'':s.ref?'moving':'target';
  }
  function activeFace(f){return f&&!!f[interactionPhase()];}
  function faceAt(x,y){return hitFaces.slice().reverse().find(f=>pointInside(x,y,f.points));}
  function panelActive(){return !!sceneHover||interactionPhase()==='moving'&&(pickerHover!==null||pickerFocus!==null);}
  function syncEffects(sample=motionSample()){
    const phase=interactionPhase(),pulse=!!phase&&!motion&&!panelActive()&&!drag?.moved&&!pieceDrag?.moved;
    picker.classList.toggle('attention',phase==='moving'&&pulse);
    picker.classList.toggle('dragging',!!pieceDrag?.moved);
    canvas.dataset.phase=phase;
    canvas.dataset.effect=phase?(panelActive()?'panel':pulse?'block':''):'';
    // Keep the last phase until draw settles both the scene and contact feedback.
    canvas.dataset.motion=motion?(sample.phase||motion.segments.at(-1).phase):'';
    canvas.style.cursor=drag?.moved?'grabbing':sceneHover?'pointer':'grab';
    if((pulse||motion&&motionPausedAt===null)&&!reducedMotion.matches&&!document.hidden){
      if(!effectFrame)effectFrame=requestAnimationFrame(animateEffects);
    }else if(effectFrame){cancelAnimationFrame(effectFrame);effectFrame=0;}
    return pulse;
  }
  function animateEffects(now){
    effectFrame=0;
    if(motion||now-lastEffectDraw>=32){lastEffectDraw=now;draw();}else syncEffects();
  }
  reducedMotion.addEventListener('change',()=>{if(reducedMotion.matches)finishMotion();else draw();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)finishMotion();else draw();});
  const colors=['#83ae9e','#a4b7d0','#c5ad82','#a7a1c4','#b1c596','#ccaaa1','#8cbcc0','#c4bb8e'];
  function view(v){const x=Math.cos(yaw)*v[0]-Math.sin(yaw)*v[1],d=Math.sin(yaw)*v[0]+Math.cos(yaw)*v[1];return [x,Math.sin(pitch)*d-Math.cos(pitch)*v[2],Math.cos(pitch)*d+Math.sin(pitch)*v[2]];}
  function project(v){const w=canvas.clientWidth,h=canvas.clientHeight,q=view(sub(v,viewCenter)),scale=Math.min(w,h)/8*zoom;return [w/2+q[0]*scale,h*.49+q[1]*scale,q[2]];}
  function inspectScene(){return inspection.path[inspection.path.length-1];}
  function placementPose(){
    const s=state();if(!s.pending)return null;
    // Keep the unselected piece outside the whole bonded assembly, with a unit gap.
    return s.op||{t:[Math.max(...s.tiles.flatMap(rules.placedCubes).map(c=>c[0]))*.5+2.5,s.anchor.t[1]-1,s.anchor.t[2]],r:I};
  }
  function movingPose(){return motionSample()?.pose||placementPose();}
  function sceneFaces(frame,pose){
    const {s,boundary}=frame;
    if(inspection){const item=inspectScene();return rules.exposed(item.unit.children.map(p=>({t:mul(p.t,2),r:p.r})))
      .map(f=>({...f,c:mul(f.c,.5),scale:.5,ref:`i:${f.tile}`,inspectTile:f.tile,displayOnly:true}));}
    if(s.grouped&&parentView==='rules'){
      const p=rules.parent(s.tiles);
      return rules.placedFaces({t:[0,0,0],r:p.r}).map(f=>({...f,c:add(mul(f.c,2),mul(p.t,2)),scale:2,ref:'parent',parentFace:f.id,displayOnly:true,tile:0}));
    }
    const target=boundary.map(f=>({...f,target:true,unmarked:s.grouped&&parentView==='shell'}));
    if(s.grouped){const p=rules.parent(s.tiles);for(const f of target)f.parentFace=parentModel.faceFor(f,p);}
    if(s.pending){
      target.push(...rules.placedFaces(pose).map(f=>({...f,moving:true,tile:-1})));
    }
    return target;
  }
  function polygon(points,fill,stroke,width=1){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fillStyle=fill;ctx.fill();ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}
  function drawFaceArrow(f,emphasized=false){
    const p=project(f.center),end=project(add(f.center,mul(f.u,(f.scale||1)*.27)));
    const dx=end[0]-p[0],dy=end[1]-p[1],len=Math.hypot(dx,dy)||1;
    ctx.save();ctx.strokeStyle=emphasized?contactPalette.emphasis:'#173f3d';ctx.lineWidth=emphasized?3:1.7;
    if(emphasized){ctx.shadowColor=contactPalette.glow;ctx.shadowBlur=5;}
    ctx.beginPath();ctx.moveTo(p[0]-dx*.15,p[1]-dy*.15);ctx.lineTo(end[0],end[1]);ctx.stroke();
    ctx.beginPath();ctx.moveTo(end[0]-dx/len*5+dy/len*3,end[1]-dy/len*5-dx/len*3);ctx.lineTo(end[0],end[1]);ctx.lineTo(end[0]-dx/len*5-dy/len*3,end[1]-dy/len*5+dx/len*3);ctx.stroke();ctx.restore();
    return {p,dx,dy};
  }
  function draw() {
    updateScene(displayState());
  }
  // Settle motion and DOM feedback before painting; never rebuild the face picker here.
  function updateScene(frame) {
    const sample = motionSample();
    if (motion && !sample.phase) {
      motion = null;
      motionPausedAt = null;
      renderContactFeedback(frame);
    }
    $('attach').disabled = !!motion || !!inspection || !frame.result.ok;
    drawScene(frame, sample?.pose || placementPose(), sample);
  }
  function drawScene(frame, pose, sample) {
    const w=canvas.clientWidth,h=canvas.clientHeight,dpr=Math.min(devicePixelRatio||1,2);
    if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);}
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);hitFaces=[];
    const ground=project([0,0,-2.5]);ctx.fillStyle='#526b6211';ctx.beginPath();ctx.ellipse(ground[0],ground[1],w*.28,h*.075,0,0,Math.PI*2);ctx.fill();
    const {s,result,movingFaceId:selectedMovingId}=frame,showFeedback=!motion&&!inspection;
    const contacts=showFeedback?result.contacts:[];
    const targetContacts=new Map(contacts.map(c=>[c.a.ref,c])),movingContacts=new Map(contacts.map(c=>[c.b.id,c]));
    const faces=sceneFaces(frame,pose).filter(f=>view(f.n)[2]>.001).map(f=>{
      const center=mul(f.c,.5),u=mul(f.u,(f.scale||1)*.5),v=mul(cross(f.n,f.u),(f.scale||1)*.5);
      const corners=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>add(center,add(mul(u,a),mul(v,b))));
      return {...f,center,points:corners.map(project),depth:project(center)[2]};
    }).sort((a,b)=>a.depth-b.depth||Number(a.moving)-Number(b.moving));
    hitFaces=faces.filter(f=>f.target||f.displayOnly||f.moving);
    const rect=canvas.getBoundingClientRect();
    const underPointer=scenePointer&&!drag?.moved?faceAt(scenePointer.x-rect.left,scenePointer.y-rect.top):null;
    sceneHover=activeFace(underPointer)?underPointer:null;
    const pulse=syncEffects(sample),glow=reducedMotion.matches?.16:.09+.15*(.5+.5*Math.sin(performance.now()*Math.PI/1400));
    const contactFaces=[];
    for(const f of faces){
      const selected=f.target&&(f.ref===s.ref||f.ref===highlight||f.ref===explainRef)||f.moving&&f.id===selectedMovingId;
      const contact=f.target?targetContacts.get(f.ref):f.moving?movingContacts.get(f.id):null;
      const issue=contact&&!contact.ok;
      ctx.globalAlpha=f.moving?.67:1;
      polygon(f.points,f.moving?(showFeedback&&result.overlap.length?'#e1a39a':'#efc17e'):colors[Math.max(0,f.tile)%colors.length],selected?'#075c61':issue?'#bd4236':'#486b6270',selected?3:issue?2:1);
      ctx.globalAlpha=1;
      if(activeFace(f)){
        const hovered=f===sceneHover||f.moving&&(f.id===pickerHover||f.id===pickerFocus);
        if(hovered||pulse){
          ctx.save();ctx.shadowColor=hovered?'#38bdb4':'#b5f5df';ctx.shadowBlur=hovered?13:7;
          polygon(f.points,`rgba(255,255,240,${hovered?.42:glow})`,hovered?'#087f80':`rgba(223,255,241,${glow*2})`,hovered?3:1.5);
          ctx.restore();
        }
      }
      if(contact)contactFaces.push({f,selected,contact,appearance:F.describe(contact)});
      if(!f.unmarked){
        const {p,dx,dy}=drawFaceArrow(f);
        ctx.font='600 11px system-ui';ctx.textAlign='center';ctx.fillStyle='#163d38';ctx.fillText(f.motif,p[0]-dx*.65,p[1]-dy*.65+3);
      }
      if(s.grouped&&!inspection&&f.parentFace===parentLab.face)
        polygon(f.points,'rgba(240,189,75,.14)','#9a6417',3);
    }
    // Show every contact through the pieces and hover; keep warnings above matches.
    contactFaces.sort((a,b)=>a.appearance.priority-b.appearance.priority);
    for(const {f,selected,contact,appearance} of contactFaces){
      ctx.save();
      if(appearance.dashed)ctx.setLineDash([5,3]);
      polygon(f.points,contact.ok?contactPalette.goodFill:contactPalette.badFill,
        contact.ok?contactPalette.goodBorder:contactPalette.badBorder,selected?3.5:2.5);
      ctx.restore();
      if(appearance.dashed)drawFaceArrow(f,true);
    }
    if(showFeedback&&result.overlap.length&&s.op){ctx.fillStyle='#a13730';ctx.font='600 13px system-ui';ctx.fillText(t('重なりあり · この位置には接着できません'),w/2,h-45);}
  }
  function pointInside(x,y,points){let inside=false;for(let i=0,j=points.length-1;i<points.length;j=i++){
    const a=points[i],b=points[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])inside=!inside;
  }return inside;}
  function drawPiecePicker(selected=movingFaceId()){
    pickerHover=null;pickerFocus=null;
    if($('candidate-controls').hidden){$('piece-picker').replaceChildren();$('piece-selection').textContent='';return;}
    const view=v=>{const x=Math.cos(pieceYaw)*v[0]-Math.sin(pieceYaw)*v[1],d=Math.sin(pieceYaw)*v[0]+Math.cos(pieceYaw)*v[1];return [x,Math.sin(piecePitch)*d-Math.cos(piecePitch)*v[2],Math.cos(piecePitch)*d+Math.sin(piecePitch)*v[2]];};
    const project=v=>{const p=view(sub(v,[-.35,-.35,-.35]));return [150+p[0]*58,108+p[1]*58,p[2]];};
    const visible=rules.placedFaces({t:[0,0,0],r:I}).filter(f=>view(f.n)[2]>.001).map(f=>{
      const center=mul(f.c,.5),v=cross(f.n,f.u);
      const points=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>project(add(center,add(mul(f.u,a*.5),mul(v,b*.5)))));
      return {...f,center,points,depth:project(center)[2]};
    }).sort((a,b)=>a.depth-b.depth);
    $('piece-picker').innerHTML=visible.map(f=>{
      const c=project(f.center),end=project(add(f.center,mul(f.u,.29))),dx=end[0]-c[0],dy=end[1]-c[1],length=Math.hypot(dx,dy)||1;
      return `<g role="button" tabindex="0" data-face="${f.id}" aria-label="${t('{motif}模様の面を使う（面{face}）',{motif:f.motif,face:f.id+1})}" aria-pressed="${selected===f.id}"><polygon points="${f.points.map(p=>p.slice(0,2).join(',')).join(' ')}" fill="#f2d9ac" stroke="#89745c" stroke-width="1"/><text x="${c[0]-dx*.7}" y="${c[1]-dy*.7+4}" text-anchor="middle" font-size="13" font-weight="600" fill="#31483e">${f.motif}</text><path d="M ${c[0]} ${c[1]} L ${end[0]} ${end[1]} M ${end[0]-dx/length*6+dy/length*3} ${end[1]-dy/length*6-dx/length*3} L ${end[0]} ${end[1]} L ${end[0]-dx/length*6-dy/length*3} ${end[1]-dy/length*6+dx/length*3}" stroke="#31483e" stroke-width="2" fill="none"/></g>`;
    }).join('');
    if(pickerPointer&&!pieceDrag?.moved){
      const face=document.elementFromPoint(pickerPointer.x,pickerPointer.y)?.closest('#piece-picker [data-face]');
      pickerHover=face?Number(face.dataset.face):null;
    }
    $('piece-selection').textContent=selected===null?t('使いたい面を選んでください。'):t('選択中: {motif}模様の面。枠の濃い面を対象物に合わせます。',{motif:rules.faces[selected].motif});
  }
  const picker=$('piece-picker');let pieceDrag=null,suppressPieceClick=false;
  function updatePickerHover(e){
    pickerPointer=e.pointerType==='touch'?null:{x:e.clientX,y:e.clientY};
    pickerHover=e.pointerType==='touch'||pieceDrag?.moved?null:Number(e.target.closest('[data-face]')?.dataset.face??NaN);
    if(Number.isNaN(pickerHover))pickerHover=null;
    draw();
  }
  picker.addEventListener('pointerover',updatePickerHover);
  picker.addEventListener('pointerout',()=>{pickerPointer=null;pickerHover=null;draw();});
  picker.addEventListener('focusin',e=>{pickerFocus=Number(e.target.closest('[data-face]')?.dataset.face??NaN);if(Number.isNaN(pickerFocus))pickerFocus=null;draw();});
  picker.addEventListener('focusout',()=>{pickerFocus=null;draw();});
  picker.addEventListener('pointerdown',e=>{pieceDrag={x:e.clientX,y:e.clientY,lastX:e.clientX,lastY:e.clientY,moved:false};suppressPieceClick=false;});
  picker.addEventListener('pointermove',e=>{
    if(!pieceDrag){updatePickerHover(e);return;}
    if(Math.hypot(e.clientX-pieceDrag.x,e.clientY-pieceDrag.y)>5)pieceDrag.moved=true;
    if(pieceDrag.moved){picker.setPointerCapture(e.pointerId);pieceYaw+=(e.clientX-pieceDrag.lastX)*.012;piecePitch=Math.max(-1.5,Math.min(1.5,piecePitch+(e.clientY-pieceDrag.lastY)*.01));drawPiecePicker();draw();}
    pieceDrag.lastX=e.clientX;pieceDrag.lastY=e.clientY;
  });
  picker.addEventListener('pointerup',e=>{suppressPieceClick=!!pieceDrag?.moved;pieceDrag=null;updatePickerHover(e);});
  picker.addEventListener('pointercancel',()=>{pieceDrag=null;suppressPieceClick=true;pickerPointer=null;pickerHover=null;draw();});
  picker.addEventListener('pointerleave',()=>{if(pieceDrag&&!pieceDrag.moved)pieceDrag=null;pickerPointer=null;pickerHover=null;draw();});
  picker.addEventListener('click',e=>{if(suppressPieceClick){suppressPieceClick=false;return;}const face=e.target.closest('[data-face]');if(face)selectMovingFace(Number(face.dataset.face));});
  picker.addEventListener('keydown',e=>{const face=e.target.closest('[data-face]');if(!face||!['Enter',' '].includes(e.key))return;
    e.preventDefault();const id=Number(face.dataset.face);selectMovingFace(id);picker.querySelector(`[data-face="${id}"]`)?.focus();});
  for(const [id,axis,delta] of [['piece-left','yaw',-.4],['piece-right','yaw',.4],['piece-up','pitch',.3],['piece-down','pitch',-.3]])$(id).onclick=()=>{
    if(axis==='yaw')pieceYaw+=delta;else piecePitch=Math.max(-1.5,Math.min(1.5,piecePitch+delta));drawPiecePicker();draw();
  };
  $('piece-reset').onclick=()=>{pieceYaw=.8;piecePitch=.6;drawPiecePicker();draw();};
  let drag=null;
  canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,lastX:e.clientX,lastY:e.clientY,moved:false};if(e.isTrusted)canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointermove',e=>{scenePointer=e.pointerType==='touch'?null:{x:e.clientX,y:e.clientY};if(!drag){draw();return;}const dx=e.clientX-drag.lastX,dy=e.clientY-drag.lastY;
    if(Math.hypot(e.clientX-drag.x,e.clientY-drag.y)>5)drag.moved=true;
    if(drag.moved){yaw+=dx*.009;pitch=Math.max(-1.1,Math.min(1.3,pitch+dy*.007));draw();}drag.lastX=e.clientX;drag.lastY=e.clientY;
  });
  canvas.addEventListener('pointerup',e=>{if(!drag)return;const moved=drag.moved;drag=null;if(moved){draw();return;}
    const rect=canvas.getBoundingClientRect(),x=e.clientX-rect.left,y=e.clientY-rect.top;
    const f=faceAt(x,y);if(!f)return;
    if(inspection)deeper(f.inspectTile);
    else if(state().grouped)parentLab.select(f.parentFace);else if(f.moving)selectMovingFace(f.id);else selectTarget(f.ref);
  });
  canvas.addEventListener('pointercancel',()=>{drag=null;scenePointer=null;draw();});
  canvas.addEventListener('pointerleave',()=>{scenePointer=null;draw();});
  window.addEventListener('blur',()=>{scenePointer=null;pickerPointer=null;pickerHover=null;draw();});
  window.addEventListener('scroll',()=>{scenePointer=null;pickerPointer=null;pickerHover=null;draw();},{passive:true});
  canvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.45,Math.min(3,zoom*Math.exp(-e.deltaY*.001)));draw();},{passive:false});
  new ResizeObserver(draw).observe(canvas);
  function fitView(){yaw=.8;pitch=.6;zoom=1;viewCenter=[0,0,0];if(!inspection){
    const points=state().tiles.flatMap(rules.placedCubes).map(c=>mul(c,.5));
    const lo=[0,1,2].map(i=>Math.min(...points.map(p=>p[i]))),hi=[0,1,2].map(i=>Math.max(...points.map(p=>p[i])));
    viewCenter=mul(add(lo,hi),.5);zoom=Math.min(1,5/(Math.max(...sub(hi,lo))+2));
  }}
  function resetView(){fitView();draw();}
  for(const [id,axis,delta] of [['view-left','yaw',-.25],['view-right','yaw',.25],['view-up','pitch',.18],['view-down','pitch',-.18]])$(id).onclick=()=>{if(axis==='yaw')yaw+=delta;else pitch=Math.max(-1.1,Math.min(1.3,pitch+delta));draw();};
  $('view-reset').onclick=resetView;
  $('view-zoom-in').onclick=()=>{zoom=Math.min(3,zoom*1.2);draw();};
  $('view-zoom-out').onclick=()=>{zoom=Math.max(.45,zoom/1.2);draw();};
  $('view-back').onclick=()=>{if(oldView)restoreCamera(oldView);oldView=null;$('view-back').hidden=true;draw();};
  function viewFace(face){if(!face||inspection)return;if(!oldView)oldView=camera();const n=face.n;
    pitch=Math.asin(n[2]*.85);yaw=Math.atan2(n[0],n[1]);viewCenter=mul(face.c,.5);zoom=1.1;$('view-back').hidden=false;render();}
  $('view-face').onclick=()=>viewFace(selectable().find(f=>f.ref===(highlight||state().ref)));
  $('target-face').onchange=e=>selectTarget(e.target.value);
  $('candidate').onchange=e=>{const entry=rules.candidates(state().tiles,state().ref,true).find(c=>poseKey(c.p)===e.target.value);if(entry){adjust(s=>{s.op=entry.p;});render();}};
  $('all-faces').onchange=e=>{allFaces=e.target.checked;render();};
  for(const [id,sign] of [['rotate-left',1],['rotate-right',-1]])$(id).onclick=()=>{if(state().op&&!inspection){adjust(s=>{s.op=rules.rotateAt(s.tiles,s.op,s.ref,sign);});render();}};
  $('return-face').onclick=()=>{explainRef=null;render();};
  $('why').addEventListener('toggle',()=>render());
  $('problem-view').onclick=()=>{const bad=currentResult().contacts.find(c=>!c.ok);if(!bad)return;explainRef=bad.a.ref;viewFace(bad.a);};
  $('attach').onclick=()=>{if(motion||!currentResult().ok||inspection)return;commit('接着',s=>{s.tiles.push(s.op);s.pending=false;s.op=null;s.ref='';});resetHint();render();(rules.parent(state().tiles)?$('group'):$('add')).focus();};
  $('add').onclick=()=>{if(state().tiles.length>=8||state().pending||state().grouped||inspection)return;commit('部品の追加',s=>{s.pending=true;s.op=null;s.ref='';});render();$('target-face').focus();};
  $('cancel').onclick=()=>{if(inspection)return;commit('追加の取消',s=>{s.pending=false;s.op=null;s.ref='';});render();};
  $('undo').onclick=()=>{if(inspection)return;clearMotion();history.undo();resetHint();explainRef=null;highlight=null;render();};
  $('redo').onclick=()=>{if(inspection)return;clearMotion();history.redo();resetHint();explainRef=null;highlight=null;render();};
  $('free').onclick=()=>{if(inspection)return;mode='free';hintMessage='';render();};
  function confirmRestart(nextMode){if(inspection)return;restartMode=nextMode;$('confirm').showModal();}
  $('guided').onclick=()=>{if(mode!=='guided')confirmRestart('guided');};
  $('restart').onclick=()=>confirmRestart(mode);
  $('confirm').addEventListener('close',()=>{if($('confirm').returnValue!=='start')return;
    clearMotion();
    mode=restartMode;history=new E.History(initial());resetHint();explainRef=null;highlight=null;parentView='rules';allFaces=false;oldView=null;$('view-back').hidden=true;fitView();render();});
  $('hint').onclick=()=>{
    const s=state(),hint=rules.nextHint(s.tiles,s.anchor);if(!hint||inspection)return;
    hintStep=Math.min(hintStep+1,3);highlight=hint.ref;
    if(hintStep===1){const face=selectable().find(f=>f.ref===hint.ref);hintMessage=()=>t('部品{piece}の面{face}（{motif}）に取り付けられます。裏に隠れているときは「選択・ヒントの面を見る」を押してください。',{piece:face.tile+1,face:face.id+1,motif:face.motif});}
    else if(hintStep===2){const c=rules.check(s.tiles,hint.p).contacts.find(c=>c.a.ref===hint.ref);hintMessage=()=>t('対象は部品{piece}の面{face}（{a}）。相手は{b}。比較窓で矢印が{arrow}になる向きです。',{piece:c.a.tile+1,face:c.a.id+1,a:c.a.motif,b:c.b.motif,arrow:arrowName(c.expected,c.a)});}
    else {hintMessage=()=>t('具体的な候補を表示しました。二つの矢印を確かめて「接着する」を押してください。');
      const fn=d=>{d.pending=true;d.op=hint.p;d.ref=hint.ref;};if(s.pending)adjust(fn);else commit('部品の追加',fn);}
    render();
  };
  $('group').onclick=()=>{if(!inspection&&rules.parent(state().tiles)){commit('親への集約',s=>{s.grouped=true;});parentView='children';render();}};
  for(const [id,value] of [['show-boundary','children'],['show-shell','shell'],['show-parent','rules']])$(id).onclick=()=>{parentView=value;render();};
  function makeUnit(s){return {children:rules.group.map(p=>({t:mul(p.t,.5),r:p.r})),childUnit:s.unit};}
  $('promote').onclick=()=>{const p=rules.parent(state().tiles);if(!p||!state().grouped||inspection)return;
    commit('次の階層',s=>{s.unit=makeUnit(s);s.level++;s.tiles=[{t:[0,0,0],r:p.r}];s.anchor=clone(s.tiles[0]);s.grouped=false;s.pending=false;s.op=null;s.ref='';});resetHint();parentView='rules';fitView();render();};
  function openInspection(){if(inspection)return;const s=state(),unit=s.grouped?makeUnit(s):s.unit;if(!unit)return;
    inspection={path:[{unit,tile:s.grouped?0:Number($('inspect-tile').value)||0}],rootChoice:$('inspect-tile').value,camera:camera(),explainRef,oldView};viewCenter=[0,0,0];zoom=1.5;oldView=null;$('view-back').hidden=true;render();}
  function deeper(tile){if(!inspection||!inspectScene().unit.childUnit)return;inspection.path.push({unit:inspectScene().unit.childUnit,tile});viewCenter=[0,0,0];zoom=1.5;render();}
  $('inspect-deeper').onclick=()=>deeper(Number($('inspect-tile').value)||0);
  $('inspect').onclick=openInspection;
  $('inspect-up').onclick=()=>{if(inspection&&inspection.path.length>1){inspection.path.pop();render();}};
  $('inspect-return').onclick=()=>{if(!inspection)return;restoreCamera(inspection.camera);explainRef=inspection.explainRef;oldView=inspection.oldView;$('inspect-tile').value=inspection.rootChoice;inspection=null;$('view-back').hidden=!oldView;render();};
  let guideStep=0;
  function renderGuide(){
    document.querySelectorAll('[data-guide-step]').forEach((el,i)=>{el.hidden=i!==guideStep;});
    $('guide-progress').textContent=t('{step} / {total}',{step:guideStep+1,total:4});
    $('guide-prev').disabled=guideStep===0;
    $('guide-next').textContent=guideStep===3?t('組立を試す'):t('次へ');
  }
  $('guide-open').onclick=()=>{renderGuide();$('play-guide').showModal();$('play-guide').scrollTop=0;};
  $('guide-close').onclick=()=>$('play-guide').close();
  $('guide-prev').onclick=()=>{guideStep=Math.max(0,guideStep-1);renderGuide();$('play-guide').scrollTop=0;};
  $('guide-next').onclick=()=>{if(guideStep===3){$('play-guide').close();return;}guideStep++;renderGuide();$('play-guide').scrollTop=0;};
  document.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]'))return;if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'){
    e.preventDefault();if(!inspection)(e.shiftKey?$('redo'):$('undo')).click();}
    if(e.key==='Escape'&&inspection)$('inspect-return').click();
  });
  $('language').onchange=e=>{ChairI18n.setLanguage(e.target.value,true);translateTemplate();renderGuide();render();};
  // Read-only diagnostic snapshot for reproducible prototype checks.
  window.ChairPrototype={snapshot:()=>clone({state:state(),mode,inspection:!!inspection,canUndo:history.canUndo,canRedo:history.canRedo}),camera,movingPose:()=>clone(movingPose()),rules};
  // Only the isolated demonstration document exposes scripted controls.
  if(window.CHAIR_DEMO){
    document.documentElement.classList.add('demo-document');
    const targetRef='0:11',pieceFace=20;
    window.ChairDemoScene={
      finishMotion,pauseMotion,resumeMotion,
      reset(){
        clearMotion();
        const s=initial();s.pending=false;history=new E.History(s);mode='guided';inspection=null;
        allFaces=false;resetHint();explainRef=null;highlight=null;oldView=null;
        const target=selectable().find(f=>f.ref===targetRef);
        yaw=Math.atan2(target.n[0],target.n[1])+.55;pitch=Math.asin(target.n[2]*.85)+.38;
        viewCenter=mul(target.c,.5);zoom=1.7;
        const face=rules.faces[pieceFace];pieceYaw=Math.atan2(face.normal[0],face.normal[1])+.18;
        piecePitch=Math.asin(face.normal[2]*.85)+.1;render();window.scrollTo(0,0);
      },
      focus(kind){
        const el=kind==='target'?canvas:kind==='piece'?picker.querySelector(`[data-face="${pieceFace}"]`):kind==='compare'?$('compare-content'):$(kind);
        if(!el)throw new Error(`Demo control missing: ${kind}`);
        // Firefox may scroll an SVG's outer viewport instead of the selected face.
        // Center the face's measured bounds explicitly within this document.
        const before=el.getBoundingClientRect();
        window.scrollBy({top:before.top+before.height/2-innerHeight/2,behavior:'instant'});
        const rect=el.getBoundingClientRect();
        if(kind==='target'){
          const face=hitFaces.find(f=>f.ref===targetRef);
          if(!face)throw new Error('Demo target face is hidden');
          const p=project(face.center);return {x:rect.left+p[0],y:rect.top+p[1],width:36,height:36};
        }
        return {x:rect.left+rect.width/2,y:rect.top+rect.height/2,width:kind==='compare'?rect.width:Math.min(rect.width,260),height:rect.height};
      },
      click(kind,point){
        const el=document.elementFromPoint(point.x,point.y);
        if(kind==='target'){
          if(el!==canvas)throw new Error('Demo target is obscured');
          for(const type of ['pointerdown','pointerup'])canvas.dispatchEvent(new PointerEvent(type,{clientX:point.x,clientY:point.y,bubbles:true,pointerId:1}));
          if(state().ref!==targetRef)throw new Error('Demo selected a different target face');
        }else if(kind==='piece'){
          if(el?.closest('[data-face]')?.dataset.face!==String(pieceFace))throw new Error('Demo piece face is obscured');
          el.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:point.x,clientY:point.y}));
        }else{
          const button=$(kind);if(button.disabled)throw new Error(`Demo action is disabled: ${kind}`);button.click();
        }
        if(kind==='rotate-right'&&!currentResult().ok)throw new Error('Demo rotation failed to match');
        if(kind==='attach'){if(state().tiles.length!==2)throw new Error('Demo attachment failed');fitView();zoom=1.5;draw();canvas.scrollIntoView({block:'center',behavior:'instant'});}
      }
    };
  }
  render();
})();

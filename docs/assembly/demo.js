/* Plays real UI actions in a separate copy of the offline application. */
(() => {
  'use strict';
  const $=id=>document.getElementById(id),{t}=ChairI18n;
  const dialog=$('play-demo'),frame=$('demo-frame'),cursor=$('demo-cursor'),mark=$('demo-mark');
  const steps=[
    {kind:'target',text:'接着済みの組立で、この面をクリックします。',after:'取り付ける部品が現れました。まだ仮置きです。'},
    {kind:'piece',text:'小窓で、取り付ける部品の面をクリックします。',after:'使う面が変わりました。次に矢印を合わせます。'},
    {kind:'compare',text:'模様は合っていますが、矢印はまだ違います。比較窓で見比べましょう。'},
    {kind:'rotate-right',text:'「この図で右へ90°」をクリックします。',after:'矢印が合い、すべての接触面が適合しました。'},
    {kind:'attach',text:'「接着する」をクリックして、仮置きを確定します。',after:'接着できました。この2個は一体になりました。'}
  ];
  let ready=false,playing=false,index=0,elapsed=0,acted=false,ended=false,failed=false;
  let point=null,from={x:24,y:24},position={x:24,y:24},raf=0,last=0;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const scene=()=>frame.contentWindow.ChairDemoScene;
  function controls(){
    $('demo-toggle').textContent=playing?t('一時停止'):ended?t('もう一度'):t('再生');
    $('demo-toggle').disabled=!ready||failed;$('demo-next').disabled=!ready||ended||failed;
    $('demo-restart').disabled=!ready;
    dialog.dataset.playing=String(playing);dialog.dataset.step=String(index);dialog.dataset.ended=String(ended);
  }
  function caption(){
    const step=steps[index];
    $('demo-caption').textContent=`${t('{step} / {total}',{step:index+1,total:steps.length})} · ${t(acted&&step.after?step.after:step.text)}`;
  }
  function pause(){playing=false;cancelAnimationFrame(raf);raf=0;controls();}
  function fail(error){
    console.error(error);failed=true;pause();cursor.toggleAttribute('hidden',true);mark.hidden=true;
    $('demo-caption').textContent=t('デモを再生できませんでした。「もう一度」で再読み込みできます。');
  }
  function locate(){
    point=scene().focus(steps[index].kind);
    mark.style.cssText=`left:${point.x-point.width/2}px;top:${point.y-point.height/2}px;width:${point.width}px;height:${point.height}px`;
    mark.hidden=false;
  }
  function beginStep(){
    elapsed=0;acted=false;from={...position};mark.classList.remove('clicked');
    locate();caption();controls();
  }
  function drawCursor(fraction){
    const p=reduced.matches?1:Math.min(1,fraction),ease=p*p*(3-2*p);
    position={x:from.x+(point.x-from.x)*ease,y:from.y+(point.y-from.y)*ease};
    cursor.style.transform=`translate(${position.x}px,${position.y}px)`;cursor.toggleAttribute('hidden',false);
  }
  function perform(){
    // Recompute after scrolling or resizing so the illustrated click hits the real control.
    locate();drawCursor(1);
    if(steps[index].kind!=='compare'){
      scene().click(steps[index].kind,point);mark.classList.remove('clicked');void mark.offsetWidth;mark.classList.add('clicked');
    }
    acted=true;caption();
    if(steps[index].kind==='attach'){ended=true;pause();cursor.toggleAttribute('hidden',true);mark.hidden=true;}
  }
  function advance(){
    if(index===steps.length-1){ended=true;pause();cursor.toggleAttribute('hidden',true);mark.hidden=true;return;}
    index++;beginStep();
  }
  function tick(now){
    if(!playing||!dialog.open)return;
    try{
      elapsed+=Math.min(now-last,100);last=now;
      if(!(acted&&steps[index].kind==='attach'))drawCursor(elapsed/1000);
      if(elapsed>=1450&&!acted)perform();
      if(elapsed>=3600)advance();
      if(playing)raf=requestAnimationFrame(tick);
    }catch(error){fail(error);}
  }
  function play(){if(!ready||failed)return;playing=true;last=performance.now();controls();raf=requestAnimationFrame(tick);}
  function restart(){
    pause();failed=false;ended=false;index=0;position={x:24,y:24};
    try{scene().reset();beginStep();play();}catch(error){fail(error);}
  }
  function load(){
    ready=false;failed=false;ended=false;cursor.toggleAttribute('hidden',true);mark.hidden=true;controls();
    $('demo-caption').textContent=t('デモを準備しています…');
    frame.onload=()=>{
      if(!dialog.open)return;
      ready=true;restart();
    };
    frame.srcdoc=CHAIR_DEMO_DOCUMENT;
  }
  $('demo-open').onclick=()=>{dialog.showModal();load();};
  $('demo-close').onclick=()=>dialog.close();
  dialog.addEventListener('close',()=>{
    pause();ready=false;frame.onload=null;frame.removeAttribute('srcdoc');
    $('demo-open').focus();
  });
  $('demo-toggle').onclick=()=>{if(playing)pause();else if(ended)restart();else play();};
  $('demo-next').onclick=()=>{
    pause();try{if(acted)advance();if(!ended){perform();elapsed=1600;}}catch(error){fail(error);}
  };
  $('demo-restart').onclick=()=>failed?load():restart();
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing)pause();});
  new ResizeObserver(()=>{
    if(!ready||!dialog.open||ended||failed)return;
    // After attachment the old button no longer exists; leave the final result visible.
    if(acted&&steps[index].kind==='attach')return;
    try{locate();drawCursor(1);from={...position};}catch(error){fail(error);}
  }).observe($('demo-stage'));
  if(new URL(location.href).searchParams.get('demo')==='1'){
    $('guide-open').click();$('demo-open').click();
  }
})();

const assert=require('node:assert/strict');
const {withBrowser,monitorPage,htmlURL,htmlHash,writeReport}=require('./browser-check.cjs');
withBrowser(async browser=>{
  const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'ja-JP',offline:true});
  const page=await context.newPage();

  const {errors,requests}=monitorPage(page);
  await page.goto(htmlURL);
  const scene=page.locator('#scene'),picker=page.locator('#piece-picker');
  const snap=()=>page.evaluate(()=>ChairPrototype.snapshot());
  const movingPose=()=>page.evaluate(()=>ChairPrototype.movingPose());
  const pixels=()=>scene.evaluate(el=>el.toDataURL());
  const effect=()=>scene.getAttribute('data-effect');
  const leave=async()=>{await page.mouse.move(2,2);await page.locator('h1').click();};
  const panelPoint=async()=>{
   await scene.scrollIntoViewIfNeeded();
   // Find a visible active panel; hit testing must respect the frontmost solid.
   const point=await scene.evaluate(el=>{
    const r=el.getBoundingClientRect();
    for(let y=20;y<r.height-20;y+=12)for(let x=20;x<r.width-20;x+=12){
     el.dispatchEvent(new PointerEvent('pointermove',{clientX:r.left+x,clientY:r.top+y,pointerType:'mouse'}));
     if(el.dataset.effect==='panel')return {x:r.left+x,y:r.top+y};
    }
   });
   assert(point,'An active panel must be reachable');
   await page.mouse.move(point.x,point.y);return point;
  };
  const unchangedOverTime=async()=>{const a=await pixels();await page.waitForTimeout(750);assert.equal(await pixels(),a);};
  assert.equal(await scene.getAttribute('data-phase'),'target');
  await leave();const initial=await snap(),samples=[];
  for(let i=0;i<4;i++){samples.push(await pixels());await page.waitForTimeout(250);}
  assert(new Set(samples).size>1,'Whole-block attention must visibly animate');
  const target=await panelPoint();assert.equal(await effect(),'panel');
  await unchangedOverTime();assert.deepEqual(await snap(),initial);
  await page.screenshot({path:'/tmp/chair-effects-target-hover.png'});
  const detached=await movingPose();
  await page.mouse.click(target.x,target.y);
  assert.equal(await scene.getAttribute('data-phase'),'moving');
  assert.match(await page.locator('#instruction-title').innerText(),/向きを合わせて接着する/);
  assert.equal((await snap()).state.tiles.length,1);
  assert.equal((await snap()).state.op,null,'Target selection must not create an attachment placement');
  assert.deepEqual(await movingPose(),detached,'The rendered piece must stay in exactly the same detached pose');
  assert.equal(await picker.locator('[aria-pressed="true"]').count(),0,'No moving face is preselected');
  assert(await page.locator('#attach').isDisabled());assert(await page.locator('#rotate-right').isDisabled());
  assert.equal(await page.locator('.face-pair').count(),0,'No contact is shown before both faces are selected');
  await leave();assert.equal(await effect(),'block');
  assert(await picker.evaluate(el=>el.classList.contains('attention')));
  const pending=await snap(),movingPoint=await panelPoint();await unchangedOverTime();
  assert.equal(await picker.evaluate(el=>el.classList.contains('attention')),false,'Main-view hover stops both whole-piece effects');
  assert.deepEqual(await snap(),pending);
  await page.screenshot({path:'/tmp/chair-effects-moving-hover.png'});
  await page.mouse.click(movingPoint.x,movingPoint.y);
  assert((await snap()).state.op,'The separate piece also supports second-face selection in the main view');
  assert.equal((await snap()).state.tiles.length,1);
  await page.locator('#target-list').evaluate(el=>el.open=true);
  await page.locator('#target-face').selectOption(pending.state.ref);
  assert.equal((await snap()).state.op,null,'Reselecting the target requires a new moving-face selection');
  await page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);
  assert.deepEqual(await movingPose(),detached);
  await page.locator('#target-list').evaluate(el=>el.open=false);
  const face=picker.locator('[data-face]').last();await face.hover();
  assert.equal(await effect(),'panel');assert.equal(await picker.evaluate(el=>el.classList.contains('attention')),false);
  assert.equal(await face.locator('polygon').evaluate(el=>getComputedStyle(el).fill),'rgb(255, 242, 206)');
  await face.click();assert.equal((await snap()).state.tiles.length,1,'Piece-face selection must not attach');
  assert((await snap()).state.op,'Selecting the second face creates the first attachment preview');
  assert.notDeepEqual(await movingPose(),detached);
  assert(await page.evaluate(()=>{const s=ChairPrototype.snapshot().state;return ChairPrototype.rules.check(s.tiles,s.op).contacts.some(c=>c.a.ref===s.ref);}),
   'Only after both selections do the chosen faces touch');
  await page.mouse.move(2,2);await picker.locator('[data-face]').last().focus();assert.equal(await effect(),'panel');
  await leave();await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(100);
  await unchangedOverTime();assert.equal(await picker.evaluate(el=>getComputedStyle(el).animationName),'none');
  await page.screenshot({path:'/tmp/chair-effects-reduced-motion.png',fullPage:true});
  for(let i=0;i<3;i++)await page.locator('#hint').click();
  await page.locator('#attach').click();assert.equal((await snap()).state.tiles.length,2);
  assert.equal(await scene.getAttribute('data-phase'),'');assert.equal(await effect(),'');
  await page.locator('#add').click();assert.equal(await scene.getAttribute('data-phase'),'target');
  assert(await page.evaluate(()=>{const s=ChairPrototype.snapshot().state,r=ChairPrototype.rules,result=r.check(s.tiles,ChairPrototype.movingPose());return !result.contacts.length&&!result.overlap.length;}),
   'The separate piece must stay clear of a larger bonded assembly too');
  await page.locator('#cancel').click();assert.equal(await effect(),'');
  await page.locator('#undo').click();assert.equal(await scene.getAttribute('data-phase'),'target');
  await page.setViewportSize({width:390,height:900});
  const touchPoint=await panelPoint();
  await scene.dispatchEvent('pointerleave');
  const beforeTouch=await snap();
  await scene.dispatchEvent('pointermove',{clientX:touchPoint.x,clientY:touchPoint.y,pointerType:'touch'});
  assert.equal(await effect(),'block','Touch must not leave a sticky hover');assert.deepEqual(await snap(),beforeTouch);
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const report={checked_at:new Date().toISOString(),status:'pass',offline:true,
   html_sha256:htmlHash(),
   checks:['target and moving-block attention','visible pulse and static panel hover','shared main/picker attention','picker hover and keyboard focus','target selection preserves detached rendered pose','no moving-face preselection or contact before second face selection','second face selection moves piece into contact without bonding','hover preserves placement and history','explicit attachment and next-piece phase','cancel and Undo restore effects','reduced motion stops animation','mobile touch has no sticky hover'],page_errors:errors};
  writeReport('docs/assembly_effects_verification.json',report);
}).catch(e=>{console.error(e);process.exitCode=1;});

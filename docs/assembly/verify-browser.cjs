const assert=require('node:assert/strict');
const {withBrowser,monitorPage,htmlURL,htmlHash,writeReport}=require('./browser-check.cjs');
withBrowser(async browser=>{
  const context=await browser.newContext({viewport:{width:1280,height:900},offline:true,locale:'ja-JP'});
  const page=await context.newPage();
  const {errors,requests}=monitorPage(page);
  await page.goto(htmlURL);
  const snap=()=>page.evaluate(()=>ChairPrototype.snapshot());
  const english=async()=>{
    const before=await snap();
    await page.locator('#language').selectOption('en');
    assert.equal(await page.locator('html').getAttribute('lang'),'en');
    assert.deepEqual(await snap(),before,'Switching language must preserve assembly and history');
    const untranslated=await page.evaluate(()=>{
      const found=[],jp=/[\u3040-\u30ff\u4e00-\u9fff]/,walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
      while(walker.nextNode()){
        const n=walker.currentNode;if(n.parentElement.closest('script,style,noscript,#language'))continue;
        if(jp.test(n.textContent))found.push(n.textContent);
      }
      for(const el of document.querySelectorAll('[aria-label],[title]'))for(const name of ['aria-label','title']){
        const text=el.getAttribute(name);if(jp.test(text||''))found.push(text);
      }
      return found;
    });
    assert.deepEqual(untranslated,[],'All interface text and accessibility labels should be translated');
  };
  const japanese=()=>page.locator('#language').selectOption('ja');
  const playGuide=async(language)=>{
    await page.locator('#language').selectOption(language);
    const before=await snap();
    await page.locator('#guide-open').click();
    while(await page.locator('#guide-prev').isEnabled())await page.locator('#guide-prev').click();
    for(let step=0;step<4;step++){
      assert.equal(await page.locator('#guide-progress').innerText(),`${step+1} / 4`);
      assert.equal(await page.locator('.guide-step:visible').count(),1);
      assert.match(await page.locator('.guide-step:visible h3').innerText(),new RegExp(`^${step+1}\\.`));
      await page.keyboard.press('Control+z');assert.deepEqual(await snap(),before,'Help must not edit the assembly');
      const overflow=await page.locator('#play-guide').evaluate(el=>el.scrollWidth>el.clientWidth);
      assert.equal(overflow,false,'The guide should fit horizontally');
      if(step===2)await page.screenshot({path:`/tmp/chair-play-guide-${language}-${await page.evaluate(()=>innerWidth)}.png`});
      await page.locator('#guide-next').click();
    }
    assert.equal(await page.locator('#play-guide').evaluate(el=>el.open),false);
    assert.deepEqual(await snap(),before,'Closing help must preserve pending work and history');
    assert.equal(await page.evaluate(()=>document.activeElement.id),'guide-open');
  };
  const hint=async()=>{for(let i=0;i<3;i++)await page.locator('#hint').click();};
  const goodCandidate=async()=>page.evaluate(()=>{
    const {state:s}=ChairPrototype.snapshot();
    const c=ChairPrototype.rules.candidates(s.tiles,s.ref,true).find(c=>c.result.ok);return c?ChairEngine.poseKey(c.p):null;
  });
  await english();await japanese();
  await playGuide('ja');await playGuide('en');await japanese();
  assert.equal(await page.locator('.mast a[href*="APERIODIC_CHAIR_TUTORIAL"]').count(),0);
  assert.equal(await page.locator('.background-reading a').getAttribute('href'),'APERIODIC_CHAIR_TUTORIAL.html');
  await page.screenshot({path:'/tmp/chair-assembly-initial.png',fullPage:true});
  assert.equal((await snap()).state.tiles.length,1);
  const canvas=await page.locator('#scene').boundingBox();
  await page.locator('#scene').click({position:{x:canvas.width*.49,y:canvas.height*.5}});
  assert((await snap()).state.ref,'Clicking a target face should select the target');
  assert.equal((await snap()).state.op,null,'Do not place the piece before its face is selected');
  for(let step=0;step<3;step++){await page.locator('#hint').click();await english();await japanese();}
  await page.waitForFunction(()=>!document.getElementById('attach').disabled);
  await english();assert.match(await page.locator('#hint-text').innerText(),/placement is shown/);await japanese();
  // Reselecting either the same or a different target discards the old placement hint.
  const hintedRef=(await snap()).state.ref;
  const otherRef=await page.locator('#target-face option').evaluateAll((options,ref)=>options.find(o=>o.value&&o.value!==ref).value,hintedRef);
  for(const ref of [hintedRef,otherRef]){
    const tiles=(await snap()).state.tiles;
    await page.locator('#target-list').evaluate(el=>el.open=true);
    await page.locator('#target-face').selectOption(ref);
    assert.equal((await snap()).state.op,null);
    assert.deepEqual((await snap()).state.tiles,tiles);
    assert(await page.locator('#attach').isDisabled());
    assert.equal(await page.locator('#hint-text').innerText(),'');
    assert.equal(await page.locator('#hint').innerText(),'ヒントを見る');
    await page.locator('#target-list').evaluate(el=>el.open=false);
    await page.locator('#hint').click();
    assert.equal((await snap()).state.op,null,'The first hint after reselection must not move the piece');
    assert.equal(await page.locator('#hint').innerText(),'矢印のヒントを見る');
    await page.locator('#hint').click();await page.locator('#hint').click();
    await page.waitForFunction(()=>!document.getElementById('attach').disabled);
  }
  // Click the moving piece's face directly, without the candidate dropdown.
  const beforeFacePick=(await snap()).state;
  const faceButton=page.locator('#piece-picker [data-face][aria-pressed="false"]').last();
  const pickedFace=Number(await faceButton.getAttribute('data-face'));
  await faceButton.click();
  const afterFacePick=(await snap()).state;
  assert.equal(afterFacePick.ref,beforeFacePick.ref);assert.deepEqual(afterFacePick.tiles,beforeFacePick.tiles);
  assert.equal(await page.locator(`#piece-picker [data-face="${pickedFace}"]`).getAttribute('aria-pressed'),'true');
  const aligned=await page.evaluate(()=>{const s=ChairPrototype.snapshot().state,r=ChairPrototype.rules;
    const a=r.exposed(s.tiles).find(f=>f.ref===s.ref),b=r.placedFaces(s.op).find(f=>ChairEngine.eq(a.c,f.c)&&ChairEngine.eq(a.n,ChairEngine.mul(f.n,-1)));return b.id;});
  assert.equal(aligned,pickedFace);
  await page.locator('#piece-right').click();await page.locator('#piece-up').click();assert.deepEqual((await snap()).state,afterFacePick);
  const pieceBox=await page.locator('#piece-picker').boundingBox();
  await page.mouse.move(pieceBox.x+pieceBox.width*.5,pieceBox.y+pieceBox.height*.5);await page.mouse.down();
  await page.mouse.move(pieceBox.x+pieceBox.width*.75,pieceBox.y+pieceBox.height*.65,{steps:6});await page.mouse.up();
  assert.deepEqual((await snap()).state,afterFacePick,'Dragging the isolated view must not change the assembly');
  await page.locator('#piece-reset').click();
  const keyFace=page.locator('#piece-picker [data-face][aria-pressed="false"]').last();
  const keyId=await keyFace.getAttribute('data-face');await keyFace.focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator(`#piece-picker [data-face="${keyId}"]`).getAttribute('aria-pressed'),'true');
  // Restore the suggested placement without changing the target.
  await page.locator('#hint').click();await page.waitForFunction(()=>!document.getElementById('attach').disabled);
  const before=(await snap()).state;
  await page.locator('#rotate-left').click();assert(await page.locator('#attach').isDisabled());
  await english();await page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);assert.match(await page.locator('#status').innerText(),/Mismatched|overlap/);
  assert.deepEqual((await snap()).state.tiles,before.tiles);
  await page.locator('#rotate-right').click();await page.waitForFunction(()=>!document.getElementById('attach').disabled);
  await page.locator('#attach').click();assert.equal((await snap()).state.tiles.length,2);
  await page.locator('#undo').click();assert.equal((await snap()).state.tiles.length,1);assert(await page.locator('#redo').isEnabled());
  await playGuide('en');await japanese();assert(await page.locator('#redo').isEnabled());
  await english();assert(await page.locator('#redo').isEnabled());await japanese();
  await page.locator('#piece-right').click();assert(await page.locator('#redo').isEnabled());
  await page.locator('#free').click();assert(await page.locator('#redo').isEnabled());
  await page.locator('#redo').click();assert.equal((await snap()).mode,'free');assert.equal((await snap()).state.tiles.length,2);
  await page.locator('#guided').click();await page.getByRole('button',{name:'今の作業を続ける'}).click();assert.equal((await snap()).mode,'free');
  await page.locator('#guided').click();await page.getByRole('button',{name:'新しく始める',exact:true}).click();
  for(let i=1;i<8;i++){await hint();await page.waitForFunction(()=>!document.getElementById('attach').disabled);await page.locator('#attach').click();assert.equal((await snap()).state.tiles.length,i+1);}
  await page.screenshot({path:'/tmp/chair-assembly-eight.png',fullPage:true});
  assert(await page.locator('#group').isVisible());await page.locator('#group').click();
  const grouped=await snap();await page.locator('#inspect').click();assert((await snap()).inspection);
  const inspecting=await snap();await page.locator('#guide-open').click();await page.keyboard.press('Escape');
  assert.deepEqual(await snap(),inspecting,'Escape should close help without leaving inspection');
  await english();assert.match(await page.locator('#inspection-path').innerText(),/Inside piece/);await japanese();
  assert(await page.locator('#undo').isDisabled());assert(await page.locator('#free').isDisabled());
  await page.keyboard.press('Control+z');assert.deepEqual((await snap()).state,grouped.state);
  await page.locator('#inspect-return').click();assert.deepEqual((await snap()).state,grouped.state);
  await page.locator('#promote').click();assert.equal((await snap()).state.level,1);assert.equal((await snap()).state.tiles.length,1);
  await page.locator('#undo').click();assert.equal((await snap()).state.level,0);assert((await snap()).state.grouped);
  await page.locator('#redo').click();assert.equal((await snap()).state.level,1);
  await hint();const pending=await snap();await page.locator('#inspect').click();await page.locator('#inspect-return').click();assert.deepEqual((await snap()).state,pending.state);
  await page.locator('#attach').click();
  for(let i=2;i<8;i++){await hint();await page.locator('#attach').click();}
  await page.locator('#group').click();await page.locator('#promote').click();assert.equal((await snap()).state.level,2);
  await page.locator('#inspect').click();assert(await page.locator('#inspect-deeper').isVisible());
  await page.locator('#inspect-tile').selectOption('3');await page.locator('#inspect-deeper').click();
  assert.match(await page.locator('#inspection-path').innerText(),/部品4の内部/);
  await page.locator('#inspect-up').click();await page.locator('#inspect-return').click();
  // Undo branch must not revive the old bond.
  await hint();await page.locator('#attach').click();await page.locator('#undo').click();
  const poseP=(await snap()).state.op;await page.locator('#rotate-left').click();const poseQ=(await snap()).state.op;
  assert.notDeepEqual(poseP,poseQ);assert(await page.locator('#redo').isDisabled());
  await page.locator('#undo').click();assert.deepEqual((await snap()).state.op,poseP);
  await page.locator('#redo').click();assert.deepEqual((await snap()).state.op,poseQ);assert.equal((await snap()).state.tiles.length,1);
  // Inspecting another contact must not change the attachment axis.
  const candidate=await goodCandidate();assert(candidate);await page.locator('#candidate-list').evaluate(el=>el.open=true);await page.locator('#candidate').selectOption(candidate);
  await page.locator('#why').evaluate(el=>el.open=true);
  await page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);
  const count=await page.locator('#contacts button').count();assert(count>1);
  const ref=(await snap()).state.ref;
  const other=await page.evaluate(ref=>ChairPrototype.rules.check(ChairPrototype.snapshot().state.tiles,ChairPrototype.snapshot().state.op).contacts.findIndex(c=>c.a.ref!==ref),ref);
  await page.locator('#contacts button').nth(other).click();assert(await page.locator('#return-face').isVisible());
  const stable=(await snap()).state;await page.locator('#return-face').click();assert.deepEqual((await snap()).state,stable);
  await page.locator('#why').evaluate(el=>el.open=false);
  const layouts=[];
  for(const width of [1280,390]){
   await page.setViewportSize({width,height:900});
   if(width===390){await playGuide('ja');await playGuide('en');await japanese();}
   const scroll=await page.evaluate(()=>document.documentElement.scrollWidth);assert(scroll<=width,`Overflow ${width}: ${scroll}`);
   if(width===390){await page.locator('#attach').scrollIntoViewIfNeeded();
     const rect=await page.locator('#scene').boundingBox();assert(rect.y>=0&&rect.y+rect.height<900,'Mobile controls should leave the model visible');
     await page.locator('#rotate-left').click();await page.locator('#rotate-right').click();
     const mobileFace=page.locator('#piece-picker [data-face][aria-pressed="false"]').last();
     const mobileId=await mobileFace.getAttribute('data-face');const fixedTarget=(await snap()).state.tiles;
     await mobileFace.click();assert.equal(await page.locator(`#piece-picker [data-face="${mobileId}"]`).getAttribute('aria-pressed'),'true');
     assert.deepEqual((await snap()).state.tiles,fixedTarget);
     await page.screenshot({path:'/tmp/chair-assembly-mobile-controls.png'});}
   layouts.push({width,scroll});await page.screenshot({path:`/tmp/chair-assembly-${width}.png`,fullPage:true});
   await english();
   const englishScroll=await page.evaluate(()=>document.documentElement.scrollWidth);
   assert(englishScroll<=width,`English overflow ${width}: ${englishScroll}`);
   await page.locator('#piece-picker').scrollIntoViewIfNeeded();
   await page.screenshot({path:`/tmp/chair-assembly-en-${width}.png`,fullPage:true});
   await japanese();
  }
  await english();await page.reload();assert.equal(await page.locator('#language').inputValue(),'en','Remember the chosen language');
  const automatic=await browser.newContext({locale:'en-US',offline:true});
  const englishPage=await automatic.newPage();await englishPage.goto(htmlURL);
  assert.equal(await englishPage.locator('#language').inputValue(),'en','Use a supported browser language on first visit');
  // Storage may be unavailable when opening standalone files under restrictive browser settings.
  await englishPage.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked');}});});
  await englishPage.reload();await englishPage.locator('#language').selectOption('ja');
  assert.equal(await englishPage.locator('html').getAttribute('lang'),'ja');await automatic.close();
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const report={checked_at:new Date().toISOString(),scope:'Prototype presentation and scripted interactions; not player testing or a mathematical proof',
   hint_checks:['same/different target reselection clears stale attachment advice','hint sequence restarts without moving the unselected piece'],
   guide_checks:['four-step Japanese/English operation guide','desktop/mobile fit','pending piece and Redo preserved','keyboard and focus return','Escape preserves inspection','mathematics link separated'],
   languages:['ja','en'],language_checks:['in-progress state and Undo/Redo preserved','hints, contact results and accessibility labels translated','desktop/mobile layout','saved preference','browser language detection','blocked storage fallback'],
   status:'pass',html_sha256:htmlHash(),
   offline:true,levels_completed:2,layouts,checks:['canvas face picking','moving-piece face click and keyboard selection','moving-piece view drag preserves pose and history','mobile moving-piece face click','attachment and rigid target','invalid rotation','Undo/Redo','mode change preserves Redo','restart cancellation','eight-child recognition','parent inspection','keyboard-accessible nested inspection','inspection blocks edits','promotion Undo/Redo','pending piece survives inspection','history branch','other-contact rotation guard','mobile controls with visible model'],page_errors:errors};
  writeReport('docs/assembly_verification.json',report);
}).catch(e=>{console.error(e);process.exitCode=1;});

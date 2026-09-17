const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {firefox}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/kanpo-review-browser/node_modules/playwright');
(async()=>{
 const browser=await firefox.launch({headless:true,executablePath:process.env.FIREFOX_PATH||'/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
 try{
  const context=await browser.newContext({viewport:{width:1280,height:1000},locale:'ja-JP',offline:true});
  const page=await context.newPage(),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  await page.goto(pathToFileURL(process.cwd()+'/docs/assembly.html').href);
  for(let i=0;i<3;i++)await page.locator('#hint').click();
  await page.locator('#attach').click();await page.locator('#undo').click();
  const player=()=>page.evaluate(()=>({snapshot:ChairPrototype.snapshot(),canvas:document.querySelector('#scene').toDataURL()}));
  const preserved=await player();assert(preserved.snapshot.canRedo);
  const demo=()=>page.locator('#demo-frame').evaluate(el=>el.contentWindow.ChairPrototype.snapshot());
  const open=async()=>{
    await page.locator('#demo-open').click();
    await page.waitForFunction(()=>document.querySelector('#play-demo').dataset.playing==='true');
  };
  const pause=()=>page.locator('#demo-toggle').click();
  const next=()=>page.locator('#demo-next').click();
  const close=async()=>{await page.locator('#demo-close').click();assert.deepEqual(await player(),preserved);};
  await page.locator('#guide-open').click();await open();await pause();
  const stopped=await demo();await page.waitForTimeout(1700);assert.deepEqual(await demo(),stopped,'Pause must stop pending clicks');
  await next();assert((await demo()).state.op);assert.equal((await demo()).state.ref,'0:11');
  await next();
  const beforeTurn=await page.locator('#demo-frame').evaluate(el=>{
    const w=el.contentWindow,s=w.ChairPrototype.snapshot().state;return w.ChairPrototype.rules.check(s.tiles,s.op);
  });
  assert.equal(beforeTurn.overlap.length,0);assert.equal(beforeTurn.ok,false);
  assert(beforeTurn.contacts.some(c=>c.patterns&&!c.arrow));
  await next();await next();
  assert(await page.locator('#demo-frame').evaluate(el=>{const w=el.contentWindow,s=w.ChairPrototype.snapshot().state;return w.ChairPrototype.rules.check(s.tiles,s.op).ok;}));
  await next();assert.equal((await demo()).state.tiles.length,2);
  assert(await page.locator('#demo-cursor').isHidden(),'Hide the click cursor once attachment is complete');
  assert.equal(await page.locator('#play-demo').getAttribute('data-ended'),'true');
  await page.screenshot({path:'/tmp/chair-demo-ja-finished.png'});await close();
  // Actual timed cursor movement and clicks, with an interrupted run and replay.
  await open();await page.waitForFunction(()=>document.querySelector('#play-demo').dataset.step==='1');
  await page.keyboard.press('Escape');assert.deepEqual(await player(),preserved);
  assert.equal(await page.evaluate(()=>document.activeElement.id),'demo-open');
  await open();await page.waitForFunction(()=>document.querySelector('#play-demo').dataset.ended==='true',{},{timeout:30000});
  assert.equal((await demo()).state.tiles.length,2);await close();
  await page.locator('#guide-close').click();
  // Compact English layout and reduced motion use the same real controls.
  await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'reduce'});
  await page.locator('#language').selectOption('en');
  const englishPlayer=await player();
  await page.locator('#guide-open').click();await open();await pause();
  for(let step=0;step<5;step++){
    await next();
    assert.equal(await page.locator('#demo-frame').evaluate(el=>el.contentDocument.documentElement.lang),'en');
    assert(!/[\u3040-\u30ff\u4e00-\u9fff]/.test(await page.locator('#demo-caption').innerText()));
    assert(await page.locator('#play-demo').evaluate(el=>el.scrollWidth<=el.clientWidth));
    if(step<4){
      const visible=await page.locator('#demo-cursor').evaluate(el=>{const r=el.getBoundingClientRect(),s=document.querySelector('#demo-stage').getBoundingClientRect();return r.x>=s.x&&r.x<s.right&&r.y>=s.y&&r.y<s.bottom;});
      assert(visible,'Cursor tip must stay in the demo viewport');
    }
    await page.screenshot({path:`/tmp/chair-demo-en-mobile-${step}.png`});
  }
  assert.equal((await demo()).state.tiles.length,2);
  await page.locator('#demo-restart').click();await pause();assert.equal((await demo()).state.tiles.length,1);
  await page.locator('#demo-close').click();assert.deepEqual(await player(),englishPlayer);
  await page.locator('#guide-close').click();assert(await page.locator('#redo').isEnabled());
  // Review regressions: SVG faces must remain clickable in short/wide viewports.
  for(const [width,height] of [[667,375],[750,600],[320,568]]){
    await page.setViewportSize({width,height});await page.locator('#language').selectOption('en');
    const before=await player();await page.locator('#guide-open').click();await open();await pause();
    for(let step=0;step<5;step++){
      await next();
      const reachable=await page.evaluate(()=>['demo-close','demo-toggle','demo-next','demo-restart'].every(id=>{
        const r=document.getElementById(id).getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&r.left>=0&&r.right<=innerWidth;
      }));
      assert(reachable,`Demo controls must remain on screen at ${width}×${height}`);
      if(step===2){
        const includesBoth=await page.evaluate(()=>{
          const frame=document.getElementById('demo-frame'),offset=frame.getBoundingClientRect(),mark=document.getElementById('demo-mark').getBoundingClientRect();
          return [...frame.contentDocument.querySelectorAll('.face-card')].every(el=>{
            const r=el.getBoundingClientRect(),x=offset.left+r.left+r.width/2;return x>=mark.left&&x<=mark.right;
          });
        });
        assert(includesBoth,'The comparison highlight must include both face cards');
      }
      if(step===1)await page.screenshot({path:`/tmp/chair-demo-review-${width}.png`});
    }
    assert.equal((await demo()).state.tiles.length,2);
    await page.locator('#demo-close').click();assert.deepEqual(await player(),before);
    await page.locator('#guide-close').click();
  }
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const report={status:'pass',checked_at:new Date().toISOString(),scope:'Scripted offline UI demonstration checks; not player trials',
    html_sha256:crypto.createHash('sha256').update(fs.readFileSync('docs/assembly.html')).digest('hex'),
    checks:['real target and piece clicks','mismatched arrows become valid after rotation','timed playback attaches two pieces','pause and manual stepping','close during playback and replay','player pending piece, camera and Redo preserved','Japanese and English','390px layout and visible cursor','667×375, 750×600 and 320×568 face picking and reachable controls','reduced motion','offline, no external requests'],page_errors:errors};
  fs.writeFileSync('docs/assembly_demo_verification.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});

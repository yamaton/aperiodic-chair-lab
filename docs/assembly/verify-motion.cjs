const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const E=require('./engine.js'),M=require('./motion.js');
const near=(a,b,message)=>assert(a.every((v,i)=>Math.abs(v-b[i])<1e-8),message);
const center=p=>E.mul(E.cubes.map(c=>E.add(p.t,E.act(p.r,E.mul(c,.5)))).reduce(E.add,[0,0,0]),1/E.cubes.length);
let pairs=0;
for(const a of E.rotations)for(const b of E.rotations){
  const from={t:[2,3,-1],r:a},to={t:[-3,2,0],r:b},m=M.transition(from,to,[0,0,1]);
  near(M.sample(m,0).pose.t,from.t);near(M.sample(m,0).pose.r,from.r);
  assert.deepEqual(M.sample(m,m.duration).pose,E.clone(to));
  for(let time=0;time<m.duration;time+=17){
    const {pose,phase}=M.sample(m,time),r=pose.r;
    near(E.product(r,E.transpose(r)),E.I,'Intermediate rotations remain rigid');
    const x=E.act(r,[1,0,0]),y=E.act(r,[0,1,0]),z=E.act(r,[0,0,1]);
    near(E.cross(x,y),z,'No reflection or scale distortion');
    if(phase==='rotate')near(center(pose),E.add(center(from),[0,0,1.5]),'Rotation keeps the centroid stationary');
  }
  pairs++;
}
const {firefox}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/kanpo-review-browser/node_modules/playwright');
(async()=>{
 const browser=await firefox.launch({headless:true,executablePath:process.env.FIREFOX_PATH||'/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
 try{
  const context=await browser.newContext({viewport:{width:1280,height:1000},offline:true,locale:'ja-JP'});
  const page=await context.newPage(),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  await page.goto(pathToFileURL(process.cwd()+'/docs/assembly.html').href);
  const snap=()=>page.evaluate(()=>ChairPrototype.snapshot());
  const pose=()=>page.evaluate(()=>ChairPrototype.movingPose());
  const settled=()=>page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);
  const collect=()=>page.evaluate(()=>new Promise(resolve=>{
    const samples=[];
    function frame(){const scene=document.getElementById('scene');samples.push({phase:scene.dataset.motion,pose:ChairPrototype.movingPose(),pixels:scene.toDataURL(),disabled:document.getElementById('attach').disabled});
      if(scene.dataset.motion)requestAnimationFrame(frame);else resolve(samples);}
    frame();
  }));
  const staged=await pose();
  await page.locator('#target-list').evaluate(el=>el.open=true);
  await page.locator('#target-face').selectOption('0:11');
  assert.deepEqual(await pose(),staged);assert.equal((await snap()).state.op,null);
  await page.locator('#target-list').evaluate(el=>el.open=false);
  const id=await page.locator('#piece-picker [data-face]').evaluateAll(elements=>{
    const s=ChairPrototype.snapshot().state;
    return elements.map(el=>Number(el.dataset.face)).find(id=>{
      const options=ChairPrototype.rules.candidates(s.tiles,s.ref,true).filter(c=>c.face===id);
      options.sort((a,b)=>ChairEngine.dot(b.p.r,ChairEngine.I)-ChairEngine.dot(a.p.r,ChairEngine.I));
      return !ChairEngine.eq(options[0].p.r,ChairEngine.I);
    });
  });
  assert.notEqual(id,undefined);
  await page.locator(`#piece-picker [data-face="${id}"]`).click();
  const chosen=await snap(),first=await collect();
  assert.deepEqual([...new Set(first.map(s=>s.phase))],['rotate','approach','']);
  assert(new Set(first.map(s=>s.pixels)).size>5,'Visible motion continues while the selected panel has hover/focus');
  assert(first.filter(s=>s.phase).every(s=>s.disabled),'Cannot commit before arrival');
  assert.deepEqual(await snap(),chosen,'Animation frames create no history or bond');
  assert.deepEqual(await pose(),chosen.state.op);
  await page.locator('#rotate-right').click();const turned=await snap(),second=await collect();
  assert.deepEqual([...new Set(second.map(s=>s.phase))],['separate','rotate','approach','']);
  assert.deepEqual(await snap(),turned);assert.equal(turned.state.tiles.length,1);
  near(second.find(s=>s.phase==='separate').pose.r,chosen.state.op.r,'Separation does not rotate');
  await page.screenshot({path:'/tmp/chair-motion-arrived.png'});
  // A new request begins at the currently visible pose, even in the middle of a turn.
  await page.locator('#rotate-left').click();
  await page.waitForFunction(()=>document.getElementById('scene').dataset.motion==='rotate');
  const retarget=await page.evaluate(()=>{
    const original=performance.now,now=performance.now();performance.now=()=>now;
    try{const before=ChairPrototype.movingPose();document.getElementById('rotate-right').click();
      return {before,after:ChairPrototype.movingPose()};
    }finally{performance.now=original;}
  });
  near(retarget.before.t,retarget.after.t);near(retarget.before.r,retarget.after.r);await settled();
  assert.deepEqual(await pose(),turned.state.op);
  // Choosing a new target clears the moving-face choice and animates back to staging.
  await page.locator('#target-list').evaluate(el=>el.open=true);
  await page.locator('#target-face').selectOption('0:0');
  assert.equal((await snap()).state.op,null);
  assert.equal(await page.locator('#piece-picker [aria-pressed="true"]').count(),0);
  const detach=await collect();assert.equal(detach[0].phase,'separate');
  assert.deepEqual(await pose(),staged);
  await page.locator('#target-list').evaluate(el=>el.open=false);
  for(let i=0;i<3;i++)await page.locator('#hint').click();await settled();
  assert(await page.locator('#attach').isEnabled());
  const valid=await snap();await page.locator('#attach').click();await page.locator('#undo').click();
  assert.deepEqual((await snap()).state,valid.state);
  await page.locator('#rotate-left').click();await page.locator('#undo').click();
  assert.equal(await page.locator('#scene').getAttribute('data-motion'),'');
  assert.deepEqual((await snap()).state,valid.state);
  await page.locator('#redo').click();const redone=await snap();await page.waitForTimeout(950);assert.deepEqual(await snap(),redone);
  // Reducing motion during a transition settles it without changing the selection.
  await page.locator('#rotate-right').click();const reducing=await snap();
  await page.emulateMedia({reducedMotion:'reduce'});await settled();
  assert.deepEqual(await pose(),reducing.state.op);assert.deepEqual(await snap(),reducing);
  await page.locator('#rotate-left').click();assert.equal(await page.locator('#scene').getAttribute('data-motion'),'');
  await page.emulateMedia({reducedMotion:'no-preference'});
  await page.locator('#rotate-right').click();await page.locator('#cancel').click();
  assert.equal(await pose(),null);await page.waitForTimeout(950);assert.equal(await pose(),null);
  await page.locator('#add').click();for(let i=0;i<3;i++)await page.locator('#hint').click();
  await page.locator('#restart').click();await page.getByRole('button',{name:'新しく始める',exact:true}).click();
  assert.deepEqual(await pose(),staged);assert.equal((await snap()).state.op,null);
  await page.setViewportSize({width:390,height:900});
  for(let i=0;i<3;i++)await page.locator('#hint').click();await settled();
  assert(await page.locator('#attach').isEnabled());await page.locator('#attach').click();assert.equal((await snap()).state.tiles.length,2);
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const report={status:'pass',checked_at:new Date().toISOString(),rotation_pairs:pairs,offline:true,
    html_sha256:crypto.createHash('sha256').update(fs.readFileSync('docs/assembly.html')).digest('hex'),
    checks:['rigid interpolation including 180-degree turns','stationary centroid during rotation','exact endpoints','first selection rotates then approaches','preview rotation separates, rotates, approaches','visible frames under panel hover','commit disabled until arrival','no frame history or automatic bond','continuous retargeting mid-turn','target reselection returns to staging without preselection','Undo/Redo and cancellation stop stale motion','restart during motion','live reduced-motion change','mobile attachment'],page_errors:errors};
  fs.writeFileSync('docs/assembly_motion_verification.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

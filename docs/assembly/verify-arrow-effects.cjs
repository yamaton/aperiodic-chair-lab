const assert=require('node:assert/strict');
const fs=require('node:fs'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {firefox}=require(process.env.PLAYWRIGHT_MODULE||'/tmp/kanpo-review-browser/node_modules/playwright');
(async()=>{
 const browser=await firefox.launch({headless:true,executablePath:process.env.FIREFOX_PATH||'/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:1000},locale:'ja-JP',offline:true,reducedMotion:'reduce'}),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  // Observe actual canvas drawing, not just diagnostic state or CSS classes.
  await page.addInitScript(()=>{
    const p=CanvasRenderingContext2D.prototype,clear=p.clearRect,stroke=p.stroke;
    p.clearRect=function(...args){if(this.canvas.id==='scene')window.arrowStrokes=[];return clear.apply(this,args);};
    p.stroke=function(...args){if(this.canvas.id==='scene')window.arrowStrokes.push({color:this.strokeStyle,width:this.lineWidth,dash:this.getLineDash()});return stroke.apply(this,args);};
  });
  await page.goto(pathToFileURL(process.cwd()+'/docs/assembly.html').href);
  const cases=await page.evaluate(()=>{
    const r=ChairPrototype.rules,s=ChairPrototype.snapshot().state,out={};
    for(const face of r.exposed(s.tiles))for(const c of r.candidates(s.tiles,face.ref,true)){
      const result=c.result,contact=result.contacts.find(a=>a.a.ref===face.ref),arrow=contact.patterns&&!contact.arrow;
      const entry={ref:face.ref,key:ChairEngine.poseKey(c.p)};
      if(!result.overlap.length){
        if(!contact.patterns)out['pair-'+contact.a.motif+contact.b.motif]??=entry;
        if(arrow&&result.contacts.every(a=>a.patterns))out[face.motif==='A'?'aa':'bc']??=entry;
        if(!contact.patterns)out.symbol??=entry;
        if(result.ok)out.valid??=entry;
        if(arrow&&result.contacts.some(a=>!a.patterns))out.mixed??=entry;
      }else if(arrow)out.overlap??=entry;
    }
    return out;
  });
  for(const name of ['aa','bc','symbol','valid','mixed','overlap'])assert(cases[name],`Missing ${name} witness`);
  const snap=()=>page.evaluate(()=>ChairPrototype.snapshot());
  const select=async entry=>{
    await page.locator('#target-list').evaluate(el=>el.open=true);
    await page.locator('#target-face').selectOption(entry.ref);
    await page.locator('#candidate-list').evaluate(el=>el.open=true);
    await page.locator('#all-faces').check();
    await page.locator('#candidate').selectOption(entry.key);
    await page.locator('#target-list').evaluate(el=>el.open=false);
    await page.locator('#candidate-list').evaluate(el=>el.open=false);
    await page.locator('#view-face').click();
  };
  const hasEffect=()=>page.locator('.face-pair.arrow-mismatch').count();
  const strokes=()=>page.evaluate(()=>window.arrowStrokes);
  for(const name of ['aa','bc']){
    await select(cases[name]);assert.equal(await hasEffect(),1);
    assert.match(await page.locator('#compare-content').innerText(),/矢印の向きが違います/);
    assert.equal(await page.locator('#status').getAttribute('class'),'status arrow-mismatch');
    assert(await page.locator('#attach').isDisabled());
    const before=await snap();
    const border=(await strokes()).find(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3');assert(border);assert.deepEqual(border.dash,[5,3]);
    assert((await strokes()).some(s=>s.color==='#a12e27'&&s.width===3),'3D arrows are emphasized');
    assert.equal(await page.locator('.face-arrow path').first().evaluate(el=>getComputedStyle(el).stroke),'rgb(161, 46, 39)');
    assert.deepEqual(await page.locator('.face-card rect').first().evaluate(el=>{
      const s=getComputedStyle(el);return {stroke:s.stroke,fill:s.fill,dash:s.strokeDasharray};
    }),{stroke:'rgb(180, 59, 50)',fill:'rgb(255, 240, 237)',dash:'5px, 3px'});
    await page.locator('#piece-picker [aria-pressed="true"]').evaluateAll(elements=>elements[0]?.focus());
    assert((await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'),'Keyboard focus does not hide the warning');
    await page.locator('#scene').hover();
    assert((await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'),'Scene hover does not hide the warning');
    assert.equal((await strokes()).at(-1).color,'#a12e27','Contact emphasis is drawn over the foreground piece and hover');
    const pixels=await page.locator('#scene').evaluate(el=>el.toDataURL());await page.waitForTimeout(250);
    assert.equal(await page.locator('#scene').evaluate(el=>el.toDataURL()),pixels,'Reduced motion preserves a static warning');
    assert.deepEqual(await snap(),before,'Effect does not mutate state or history');
    await page.screenshot({path:`/tmp/chair-arrow-effect-${name}.png`,fullPage:true});
  }
  await select(cases.symbol);assert.equal(await hasEffect(),0);assert.equal(await page.locator('#status').getAttribute('class'),'status bad');
  for(const pair of ['AB','AC','BA','BB','CA','CC']){
    assert(cases['pair-'+pair]);await select(cases['pair-'+pair]);
    assert.equal(await page.locator('.face-pair.symbol-mismatch').count(),1,`${pair} comparison must show motif failure`);
    assert.equal(await page.locator('.face-card rect').first().evaluate(el=>getComputedStyle(el).stroke),'rgb(180, 59, 50)');
    const red=(await strokes()).find(s=>s.color==='#b43b32'&&!s.dash.length);assert(red,`${pair} main-view panel must show motif failure`);assert.deepEqual(red.dash,[]);
    assert(await page.locator('#attach').isDisabled());
  }
  // User report: choose an assembly B face, then click a visible A face in the picker.
  await page.locator('#target-list').evaluate(el=>el.open=true);
  await page.locator('#target-face').selectOption(cases['pair-BA'].ref);
  await page.locator('#target-list').evaluate(el=>el.open=false);
  const faceA=await page.locator('#piece-picker [data-face]').evaluateAll(elements=>elements.find(el=>ChairPrototype.rules.faces[Number(el.dataset.face)].motif==='A').dataset.face);
  await page.locator(`#piece-picker [data-face="${faceA}"]`).click();await page.locator('#view-face').click();
  assert.equal(await page.locator('.face-pair.symbol-mismatch').count(),1);
  assert.match(await page.locator('#compare-content').innerText(),/模様が違います/);
  const baState=await snap();
  await page.locator(`#piece-picker [data-face="${faceA}"]`).focus();
  await page.locator('#scene').hover();
  assert((await strokes()).some(s=>s.color==='#b43b32'),'B/A remains red under selection, keyboard focus and hover');
  assert.deepEqual(await snap(),baState);assert(await page.locator('#attach').isDisabled());
  await page.screenshot({path:'/tmp/chair-ba-effect-fixed.png',fullPage:true});
  await select(cases.overlap);assert.equal(await hasEffect(),1);assert((await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'));assert.equal(await page.locator('#status').getAttribute('class'),'status bad');
  assert.match(await page.locator('#status').innerText(),/重なっています/);assert(await page.locator('#attach').isDisabled());
  await select(cases.mixed);assert.equal(await hasEffect(),1);assert.equal(await page.locator('#status').getAttribute('class'),'status bad','Other symbol mismatches retain overall failure');
  await page.locator('#why').evaluate(el=>el.open=true);
  const index=await page.evaluate(()=>{const s=ChairPrototype.snapshot().state;return ChairPrototype.rules.check(s.tiles,s.op).contacts.findIndex(c=>!c.patterns);});
  await page.locator('#contacts button').nth(index).click();assert.equal(await hasEffect(),0,'Comparison is specific to the displayed contact');
  await page.locator('#return-face').click();assert.equal(await hasEffect(),1);
  await page.locator('#why').evaluate(el=>el.open=false);
  await select(cases.valid);assert.equal(await hasEffect(),0);assert.equal(await page.locator('#status').getAttribute('class'),'status good');
  assert(!(await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'));await page.locator('#attach').click();await page.locator('#undo').click();
  await page.emulateMedia({reducedMotion:'no-preference'});
  await select(cases.bc);await page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);
  assert.equal(await hasEffect(),1);assert((await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'));
  await page.locator('#undo').click();assert.equal(await hasEffect(),0);
  await page.locator('#redo').click();assert.equal(await hasEffect(),1);
  for(const language of ['en','ja','zh']){
    const before=await snap();await page.locator('#language').selectOption(language);assert.equal(await hasEffect(),1);assert.deepEqual(await snap(),before);
  }
  await page.setViewportSize({width:390,height:900});assert.equal(await hasEffect(),1);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.locator('#cancel').click();assert.equal(await hasEffect(),0);assert.deepEqual(errors,[]);assert(!(await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'));
  // Reproduce rotation of the initial guided placement: the intermediate turns
  // overlap, but the selected C/B face still needs its own arrow warning.
  await page.locator('#language').selectOption('ja');
  await page.locator('#restart').click();await page.getByRole('button',{name:'新しく始める',exact:true}).click();
  for(let i=0;i<3;i++)await page.locator('#hint').click();
  await page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);
  await page.locator('#view-face').click();
  const cycleStart=await snap();
  const observeMotion=()=>page.evaluate(()=>new Promise(resolve=>{
    const frames=[];
    function frame(){
      const motion=document.getElementById('scene').dataset.motion;
      frames.push({motion,arrowWarning:window.arrowStrokes.some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'),
        cards:document.querySelectorAll('.face-pair').length,status:document.getElementById('status').className,
        text:document.getElementById('compare-content').textContent,attach:!document.getElementById('attach').disabled});
      if(motion)requestAnimationFrame(frame);else resolve(frames);
    }frame();
  }));
  for(let turn=1;turn<=4;turn++){
    await page.locator('#rotate-left').click();
    const frames=await observeMotion(),moving=frames.filter(f=>f.motion);
    assert(moving.length>0,'Observe an active rotation, not only its destination');
    assert(moving.every(f=>!f.arrowWarning&&!f.cards&&f.status==='status '&&!f.attach&&f.text.includes('位置と向きを調整中')),
      'Neither old nor future matching feedback appears during separation, rotation or approach');
    const after=frames.at(-1),s=await snap();
    if(turn<4){
      assert(after.arrowWarning);assert.equal(await hasEffect(),1);
      assert.equal(after.status,'status bad');assert(!after.attach);
      assert.match(await page.locator('#status').innerText(),/重なっています/);
    }else{assert(!after.arrowWarning);assert.equal(await hasEffect(),0);assert.equal(after.status,'status good');assert(after.attach);}
    assert.deepEqual(s.state.tiles,cycleStart.state.tiles);
  }
  assert.deepEqual((await snap()).state.op,cycleStart.state.op);
  // Live reduced-motion changes settle both scene and DOM feedback immediately.
  await page.locator('#rotate-left').click();await page.emulateMedia({reducedMotion:'reduce'});
  await page.waitForFunction(()=>!document.getElementById('scene').dataset.motion);
  assert.equal(await hasEffect(),1);assert((await strokes()).some(s=>s.color==='#b43b32'&&s.dash.join(',')==='5,3'));
  await page.locator('#rotate-right').click();assert.equal(await hasEffect(),0);assert(await page.locator('#attach').isEnabled());
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const report={status:'pass',checked_at:new Date().toISOString(),offline:true,
    html_sha256:crypto.createHash('sha256').update(fs.readFileSync('docs/assembly.html')).digest('hex'),
    checks:['A/A and B/C arrow-only mismatch','all six invalid motif pairings show red panels and comparison','B-target/A-picker click, focus and hover regression','actual canvas dashed borders and emphasized arrows','comparison card styles','selection, hover and keyboard focus preserve warning','reduced motion static rendering','no state/history changes from rendering','overlap warning and per-face arrow mismatch coexist','comparison follows each contact','mixed interface retains overall failure','matching, Undo/Redo and cancellation clear/restore effect','three languages and mobile width','four-turn cycle through overlapping placements','no matching feedback during motion','scene, comparison and status update together on arrival','live reduced-motion completion updates feedback'],page_errors:errors};
  fs.writeFileSync('docs/assembly_arrow_effects_verification.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

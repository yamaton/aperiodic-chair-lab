// Aligned panel recurrence plus the read-only parent experiment in the offline UI.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const E=require('./engine.js');
const {withBrowser,monitorPage,htmlURL,htmlHash,writeReport}=require('./browser-check.cjs');
const certificate=JSON.parse(fs.readFileSync('strong/audit/motif_grouping_certificate.json'));
const rules=E.create({faces:certificate.face_table,group:certificate.derived_group});
const model=require('./parent-rules.js').create(E,rules);
const base={t:[0,0,0],r:E.I},faces=rules.placedFaces(base),boundary=rules.exposed(rules.group);
assert.equal(boundary.length,96);
assert.equal(new Set(model.patches.flat().map(f=>E.key(f.c))).size,96);
const words=new Map();let comparisons=0,compatible=0;
for(const a of faces){
  const word=model.compare(a.id,'A',0).pairs.map(p=>p.a);
  if(words.has(a.motif))assert.deepEqual(word,words.get(a.motif));else words.set(a.motif,word);
  for(const b of faces)for(const r of E.rotations){
    if(!E.eq(a.n,E.mul(E.act(r,b.n),-1)))continue;
    // Reconstruct the physical panels from translated, rotated child placements.
    const t=E.mul(E.sub(E.mul(a.c,2),E.act(r,E.mul(b.c,2))),.5);
    const other=rules.exposed(rules.group.map(p=>({t:E.add(t,E.act(r,p.t)),r:E.product(r,p.r)})));
    const patch=boundary.filter(f=>E.eq(f.n,a.n)&&E.dot(E.sub(f.c,E.mul(a.c,2)),a.n)===0&&E.sub(f.c,E.mul(a.c,2)).every(x=>Math.abs(x)<=1));
    const matched=patch.every(f=>{const g=other.find(g=>E.eq(g.c,f.c)&&E.eq(g.n,E.mul(f.n,-1)));return g&&rules.handshake(f,g).ok;});
    const u=E.act(r,b.u),v=E.cross(a.n,a.u);
    const turn=[a.u,v,E.mul(a.u,-1),E.mul(v,-1)].findIndex(x=>E.eq(x,u));
    const result=model.compare(a.id,b.motif,turn);
    assert.equal(result.pairs.every(p=>p.ok),matched);
    assert.equal(result.parent.ok,matched);
    comparisons++;compatible+=Number(matched);
  }
}
assert.equal(words.size,3);assert.equal(comparisons,2304);assert.equal(compatible,192);
// Scene selection maps back correctly under every parent rotation and translation.
for(const r of E.rotations){
  const parent={t:[7,-3,2],r};
  model.patches.forEach((patch,id)=>patch.forEach(f=>assert.equal(model.faceFor({c:E.add(E.act(r,f.c),E.mul(parent.t,2)),n:E.act(r,f.n)},parent),id)));
}
withBrowser(async browser=>{
  const context=await browser.newContext({viewport:{width:1280,height:1000},offline:true,reducedMotion:'reduce'});
  const page=await context.newPage(),{errors}=monitorPage(page,{requestsAsErrors:true});
  await page.goto(htmlURL+'?lang=ja');
  const snap=()=>page.evaluate(()=>ChairPrototype.snapshot());
  const assemble=async(start=1)=>{for(let i=start;i<8;i++){
    for(let j=0;j<3;j++)await page.locator('#hint').click();
    await page.locator('#attach').click();
  }await page.locator('#group').click();};
  await assemble();const grouped=await snap();
  assert.equal(await page.locator('#show-boundary').getAttribute('aria-pressed'),'true');
  for(const [id,motif,goodTurn] of [[3,'A',1],[2,'C',2],[0,'B',2]]){
    await page.locator('#parent-face').selectOption(String(id));
    await page.locator('#parent-partner').selectOption(motif);
    for(let turn=0;turn<4;turn++){
      const result=page.locator('#parent-equivalence');
      assert.equal(await result.getAttribute('data-fine'),String(turn===goodTurn));
      assert.equal(await result.getAttribute('data-coarse'),String(turn===goodTurn));
      assert.equal(await page.locator('#parent-left .parent-good').count(),await page.locator('#parent-right .parent-good').count());
      await page.locator('#parent-turn-left').click();
    }
  }
  await page.locator('#parent-face').selectOption('3');await page.locator('#parent-partner').selectOption('A');
  await page.locator('#parent-turn-left').focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#parent-equivalence').getAttribute('data-fine'),'true');
  const drawing=()=>page.locator('#parent-left').evaluate(el=>{
    const copy=el.cloneNode(true);copy.querySelectorAll('.parent-verdict').forEach(label=>label.remove());return copy.innerHTML;
  });
  const geometry=await drawing();
  const labels={ja:['○ 合う','× 合わない'],en:['✓ Match','✕ No match'],zh:['✓ 对得上','✕ 对不上']};
  const layouts=[];
  for(const width of [1280,320,667])for(const lang of ['ja','en','zh']){
    await page.setViewportSize({width,height:width===667?375:1000});
    await page.locator('#language').selectOption(lang);
    assert.equal(await drawing(),geometry,'Language changes must preserve panel geometry and arrows');
    assert.deepEqual(await page.locator('#parent-left .parent-verdict').allTextContents(),Array(4).fill(labels[lang][0]));
    assert((await page.locator('#parent-left').getAttribute('aria-label')).includes(labels[lang][0].slice(2)));
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${lang}/${width} overflow`);
    if(lang!=='ja')assert(!/[\u3040-\u30ff]/.test(await page.locator('#parent-summary').innerText()));
    await page.locator('#parent-lab details').evaluate(el=>el.open=true);
    if(lang!=='ja')assert(!/[\u3040-\u30ff]/.test(await page.locator('#parent-lab').innerText()));
    await page.locator('#parent-turn-right').click();
    assert.deepEqual(await page.locator('#parent-left .parent-verdict').allTextContents(),Array(4).fill(labels[lang][1]));
    assert(await page.locator('.parent-verdict').evaluateAll(els=>els.every(el=>el.getBBox().width<=62)),'Translated labels must fit inside each panel');
    assert((await page.locator('#parent-left').getAttribute('aria-label')).includes(labels[lang][1].slice(2)));
    await page.locator('#parent-turn-left').click();
    layouts.push({width,lang});
    await page.screenshot({path:`/tmp/chair-parent-lab-${lang}-${width}.png`,fullPage:true});
  }
  assert.deepEqual(await snap(),grouped,'Experiment and language changes must preserve history');
  await page.setViewportSize({width:1280,height:1000});
  await page.locator('#show-parent').click();
  // Pick the centered parent face through the actual canvas pointer handler.
  await page.locator('#parent-face').selectOption('2');
  const canvas=page.locator('#scene');await canvas.scrollIntoViewIfNeeded();
  const box=await canvas.boundingBox();
  await page.mouse.click(box.x+box.width/2,box.y+box.height*.49);
  assert.equal(await page.locator('#parent-face').inputValue(),'2');
  assert(!(await snap()).inspection,'Clicking a parent face must open its word, not child inspection');
  await page.locator('#show-shell').click();await page.locator('#show-boundary').click();
  await page.locator('#inspect').click();assert((await snap()).inspection);
  await page.locator('#inspect-return').click();assert.deepEqual(await snap(),grouped);
  await page.locator('#undo').click();assert(!(await snap()).state.grouped);
  await page.locator('#redo').click();assert.deepEqual(await snap(),grouped);
  await page.locator('#promote').click();assert.equal((await snap()).state.level,1);
  await assemble();assert.equal((await snap()).state.level,1);
  await page.locator('#parent-face').selectOption('0');
  assert.equal(await page.locator('#parent-word-symbol').innerText(),'C→');
  assert.deepEqual(errors,[]);
  writeReport('docs/assembly_parent_verification.json',{status:'pass',html_sha256:htmlHash(),
    scope:'Aligned four-panel interfaces and offline UI; not an infinite-tiling proof',
    comparisons,compatible,patterns:words.size,selection_rotation_checks:24*96,layouts,
    history_preserved:true,levels:2,page_errors:errors});
  await context.close();
}).catch(e=>{console.error(e);process.exitCode=1;});

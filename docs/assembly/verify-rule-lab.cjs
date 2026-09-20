// Independent raw-port replay plus interaction checks for the rule experiment.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const E=require('./engine.js'),M=require('./rule-model.js'),D=require('./rule-data.json');
const frozen=JSON.parse(fs.readFileSync('strong/audit/frozen_v1/candidate.json'));
const recorded=JSON.parse(fs.readFileSync('strong/artifacts/chair_recut_substitution.json'));
const {withBrowser,monitorPage,htmlURL,htmlHash,writeReport}=require('./browser-check.cjs');
const fraction=s=>{const [n,d='1']=String(s).split('/');return Number(n)/Number(d);};
const ports=frozen.ports.map((p,i)=>({c:p.center.map(x=>16*fraction(x)),n:p.outward_normal,u:p.u_axis,v:p.v_axis,i}));
function move(port,pose){return {...port,c:E.add(E.act(pose.r,port.c),E.mul(pose.t,16)),n:E.act(pose.r,port.n),u:E.act(pose.r,port.u),v:E.act(pose.r,port.v)};}
function boundary(p,parent){
 if(!parent)return ports;
 const map=new Map();
 for(const child of p.children)for(const port of ports){const q=move(port,child),k=E.key(q.c);map.set(k,map.has(k)?null:q);}
 return [...map.values()].filter(Boolean);
}
function rawDecisions(p,values,parent){
 const b=boundary(p,parent),lookup=new Map(b.map(q=>[E.key(q.c),q]));
 assert.equal(b.length,parent?768:192);
 const rotated=new Map();
 return D.poses.map(pose=>{
  const rk=E.key(pose.rotation);if(!rotated.has(rk))rotated.set(rk,b.map(q=>move(q,{r:pose.rotation,t:[0,0,0]})));
  let hits=0;
  for(const q of rotated.get(rk)){
   const c=E.add(q.c,E.mul(pose.shift,parent?32:16)),a=lookup.get(E.key(c));
   if(!a||!E.eq(a.n,E.mul(q.n,-1)))continue;
   hits++;
   const depth=k=>Math.sign(k)*values[Math.abs(k)-1];
   if(depth(p.labels[a.i])+depth(p.labels[q.i])!==0||!E.eq(a.u,q.u)||!E.eq(a.v,q.v))return false;
  }
  assert(hits>0);return true;
 });
}
let rawComparisons=0;
const cases=D.profiles.map((p,i)=>({i,values:M.defaults(p)}));
cases.push({i:1,values:D.sixDepths},{i:1,values:Array(12).fill(1)},{i:1,values:[1,2,3,4,5,6,7,8,9,10,11,24]});
for(const {i,values} of cases){
 const p=D.profiles[i],r=M.evaluate(p,values);
 assert.deepEqual(r.fine,rawDecisions(p,values,false));
 assert.deepEqual(r.parent,rawDecisions(p,values,true));rawComparisons+=2*D.poses.length;
}
D.profiles.forEach((p,i)=>{
 const r=M.evaluate(p,M.defaults(p));
 assert.equal(r.fineCount,recorded.profiles[i].allowed_contacts);
 assert.equal(r.parentCount,recorded.profiles[i].induced_parent_contacts);
 assert.deepEqual(r.parent.flatMap((v,id)=>v?[id]:[]),recorded.profiles[i].induced_contact_type_ids);
 for(let f=1;f<=M.defaults(p).length;f++){
  const {nodes,edges}=M.component(p,f);
  assert.equal(M.freedom(nodes,[]),nodes.length);
  assert.equal(M.freedom(nodes,edges),1);
  for(let n=0;n<nodes.length;n++)assert.equal(M.freedom(nodes,edges.slice(0,n)),nodes.length-n);
 }
});
withBrowser(async browser=>{
 const context=await browser.newContext({offline:true,reducedMotion:'reduce',locale:'ja'}),page=await context.newPage();
 const {errors}=monitorPage(page,{requestsAsErrors:true});
 await page.goto(htmlURL+'?lang=ja');
 for(let i=0;i<3;i++)await page.locator('#hint').click();
 const before=await page.evaluate(()=>ChairPrototype.snapshot());
 await page.locator('#rule-open').click();
 assert((await page.locator('#rule-freedom').innerText()).includes('16 → 16'));
 await page.locator('#rule-edge-next').click();
 assert((await page.locator('#rule-freedom').innerText()).includes('16 → 15'));
 await page.locator('#rule-edge-all').click();
 assert((await page.locator('#rule-freedom').innerText()).includes('16 → 1'));
 await page.locator('#rule-next').click();
 await page.locator('#rule-family').selectOption('12');
 await page.locator('#rule-depth').fill('24');await page.locator('#rule-depth').dispatchEvent('input');
 assert.equal(await page.locator('#rule-fine-count').innerText(),'44 / 1194');
 assert((await page.locator('#rule-depth-status').innerText()).includes('同じ'));
 await page.locator('#rule-flip').click();
 assert.equal(await page.locator('#rule-depth-value').innerText(),'-24');
 await page.locator('#rule-relief').screenshot({path:'/tmp/chair-rule-negative-relief.png'});
 await page.locator('#rule-flip').click();
 await page.locator('#rule-collapse').click();assert.equal(await page.locator('#rule-fine-count').innerText(),'228 / 1194');
 await page.locator('#rule-next').click();await page.locator('#rule-group').click();
 assert.equal(await page.locator('#rule-parent-count').innerText(),'44 / 1194');
 await page.locator('#rule-witness-lost').click();
 assert.deepEqual(await page.locator('#rule-witness .verdict').allTextContents(),['○ 合う','× 合わない']);
 await page.locator('#rule-tab-1').click();await page.locator('#rule-six').click();
 assert((await page.locator('#rule-depth-status').innerText()).includes('深さ6種類'));
 assert.equal(await page.locator('#rule-fine-count').innerText(),'44 / 1194');
 await page.locator('#rule-next').click();await page.locator('#rule-group').click();
 assert.equal(await page.locator('#rule-parent-count').innerText(),'44 / 1194');
 for(const [i,fine,parent] of [[0,186,1194],[1,44,44],[2,62,398]]){
  await page.locator('#rule-profile-'+i).click();assert(await page.locator('#rule-parent-result').isHidden());
  await page.locator('#rule-group').click();
  assert.equal(await page.locator('#rule-fine-count').innerText(),fine+' / 1194');
  assert.equal(await page.locator('#rule-parent-count').innerText(),parent+' / 1194');
  if(i!==1){await page.locator('#rule-witness-extra').click();assert.deepEqual(await page.locator('#rule-witness .verdict').allTextContents(),['× 合わない','○ 合う']);}
  if(i===2)await page.locator('#rule-witness').screenshot({path:'/tmp/chair-rule-witness.png'});
 }
 await page.keyboard.press('Control+z');
 assert.deepEqual(await page.evaluate(()=>ChairPrototype.snapshot()),before);
 await page.keyboard.press('Escape');assert(await page.locator('#rule-lab').isHidden());assert(await page.locator('#rule-open').evaluate(el=>el===document.activeElement));
 const layouts=[];
 for(const width of [1280,320,667])for(const lang of ['ja','en','zh']){
  await page.setViewportSize({width,height:width===667?375:900});
  await page.locator('#language').selectOption(lang);
  await page.locator('#rule-open').click();
  for(let step=0;step<3;step++){
   await page.locator('#rule-tab-'+step).click();
   assert(await page.locator('#rule-lab').evaluate(el=>el.scrollWidth<=el.clientWidth),`${lang}/${width}/${step} overflow`);
   if(lang!=='ja')assert(!/[\u3040-\u30ff]/.test(await page.locator('#rule-lab').innerText()),`${lang}: untranslated text`);
   if(lang==='ja'&&width!==667)await page.screenshot({path:`/tmp/chair-rule-${width}-${step}.png`});
  }
  await page.locator('#rule-close').click();
  assert.deepEqual(await page.evaluate(()=>ChairPrototype.snapshot()),before);
  layouts.push({width,lang});
 }
 assert.deepEqual(errors,[]);
 await page.goto(htmlURL+'?lang=ja#rules');
 assert(await page.locator('#rule-lab').isVisible());
 writeReport('docs/assembly_rule_verification.json',{status:'pass',html_sha256:htmlHash(),raw_port_comparisons:rawComparisons,
  scope:'Six assignments replayed from raw port coordinates at all 1,194 aligned fine and parent poses; graph freedom and offline browser controls. No misregistration or infinite-tiling claim.',layouts,assembly_history_preserved:true,page_errors:errors});
 await context.close();
}).catch(e=>{console.error(e);process.exitCode=1;});

// Offline UI checks for every registered language, including RTL geometry and demos.
const assert=require('node:assert/strict');
const {withBrowser,monitorPage,htmlURL,htmlHash,writeReport}=require('./browser-check.cjs');
const {readCatalogs}=require('../build-locales.cjs');
withBrowser(async browser=>{
 const catalogs=readCatalogs(),checks=[];
  const context=await browser.newContext({locale:'en-US',offline:true,reducedMotion:'reduce'});
  const page=await context.newPage();
  const {errors}=monitorPage(page,{requestsAsErrors:true});
  for(const width of [1280,320,667]){
   const height=width===667?375:900;
   await page.setViewportSize({width,height});
   await page.goto(htmlURL+'?lang=en');
   for(let i=0;i<3;i++)await page.locator('#hint').click();
   const before=await page.evaluate(()=>ChairPrototype.snapshot());
   const arrows=await page.locator('.face-card svg').evaluateAll(els=>els.map(el=>el.innerHTML));
   for(const locale of catalogs){
    await page.locator('#language').selectOption(locale.code);
    assert.equal(await page.locator('html').getAttribute('dir'),locale.dir);
    assert.equal(await page.locator('html').getAttribute('lang'),locale.code);
    assert.deepEqual(await page.evaluate(()=>ChairPrototype.snapshot()),before,'Changing language must preserve assembly and history');
    assert.deepEqual(await page.locator('.face-card svg').evaluateAll(els=>els.map(el=>el.innerHTML)),arrows,'Arrows must not change with language');
    const faces=await page.locator('.face-card').evaluateAll(els=>els.map(el=>el.getBoundingClientRect().left));
    assert(faces[0]<faces[1],'The fixed face must remain physically on the left');
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${locale.code}: page overflow at ${width}`);
    const text=await page.locator('body').innerText();
    if(locale.code!=='ja')assert(!/[\u3040-\u30ff]/.test(text),`${locale.code}: untranslated Japanese`);
    await page.locator('#guide-open').click();
    while(await page.locator('#guide-prev').isEnabled())await page.locator('#guide-prev').click();
    for(let step=0;step<4;step++){
     assert(await page.locator('#play-guide').evaluate(el=>el.scrollWidth<=el.clientWidth),`${locale.code}: guide overflow`);
     if(step<3)await page.locator('#guide-next').click();
    }
    await page.locator('#demo-open').click();
    await page.waitForFunction(()=>document.querySelector('#play-demo').dataset.playing==='true');
    await page.locator('#demo-toggle').click();
    for(let step=0;step<5;step++){
     await page.locator('#demo-next').click();
     assert.equal(await page.locator('#demo-frame').evaluate(el=>el.contentDocument.documentElement.lang),locale.code);
     assert(await page.evaluate(()=>['demo-close','demo-next','demo-restart'].every(id=>{const r=document.getElementById(id).getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight;})),`${locale.code}: demo controls outside viewport`);
     if(step===2){
      const both=await page.evaluate(()=>{
       const frame=document.getElementById('demo-frame'),offset=frame.getBoundingClientRect(),mark=document.getElementById('demo-mark').getBoundingClientRect();
       return [...frame.contentDocument.querySelectorAll('.face-card')].every(el=>{const r=el.getBoundingClientRect(),x=offset.left+r.left+r.width/2;return x>=mark.left&&x<=mark.right;});
      });assert(both,`${locale.code}: both faces must be highlighted`);
     }
    }
    assert.equal(await page.locator('#demo-frame').evaluate(el=>el.contentWindow.ChairPrototype.snapshot().state.tiles.length),2);
    await page.screenshot({path:`/tmp/chair-locales-demo-${locale.code}-${width}.png`});
    await page.locator('#demo-close').click();await page.locator('#guide-close').click();
    assert.deepEqual(await page.evaluate(()=>ChairPrototype.snapshot()),before);
    await page.screenshot({path:`/tmp/chair-locales-${locale.code}-${width}.png`,fullPage:true});
    checks.push({language:locale.code,width,height,direction:locale.dir});
   }
   await page.locator('#attach').click();assert.equal(await page.evaluate(()=>ChairPrototype.snapshot().state.tiles.length),2);
  }
  assert.deepEqual(errors,[]);
  const report={status:'pass',checked_at:new Date().toISOString(),scope:'Automated translation coverage, offline UI and RTL interaction checks; not native-speaker review',html_sha256:htmlHash(),checks,state_and_arrows_preserved:true,demos_attach:true,page_errors:errors};
  writeReport('docs/assembly_locales_verification.json',report);
}).catch(e=>{console.error(e);process.exitCode=1;});

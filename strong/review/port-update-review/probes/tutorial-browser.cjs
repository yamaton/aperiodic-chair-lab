const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {firefox}=require('/tmp/kanpo-review-browser/node_modules/playwright');
(async()=>{
 const browser=await firefox.launch({headless:true,executablePath:'/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
 try {
  const output={browser:browser.version(),layouts:[],network:[],errors:[]};
  for(const width of [1200,390]) {
   const page=await browser.newPage({viewport:{width,height:900},offline:true});
   page.on('request',r=>{if(/^https?:/.test(r.url()))output.network.push(r.url());});
   page.on('pageerror',e=>output.errors.push(e.message));
   await page.goto(pathToFileURL(path.resolve('docs/APERIODIC_CHAIR_TUTORIAL.html')).href);
   const info=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,math:document.querySelectorAll('math').length,images:[...document.querySelectorAll('.figure-preview img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,embedded:i.src.startsWith('data:'),alt:i.alt})),anchors:[...document.querySelectorAll('a[href]')].map(a=>a.href)}));
   assert.equal(info.width,info.scroll);assert.equal(info.images.length,11);assert(info.images.every(i=>i.loaded&&i.embedded&&i.alt));
   const links=[...new Set(info.anchors.filter(h=>h.startsWith('file:')))];
   for(const href of links){const u=new URL(href);assert(fs.existsSync(fileURLToPath(u)));if(u.hash&&fileURLToPath(u)===path.resolve('docs/APERIODIC_CHAIR_TUTORIAL.html'))assert(await page.evaluate(id=>!!document.getElementById(id),decodeURIComponent(u.hash.slice(1))));}
   await page.getByRole('heading',{name:'10.1 Move and enlarge the ports while preserving the rules',exact:true}).scrollIntoViewIfNeeded();
   await page.screenshot({path:`/tmp/aperiodic-independent-dimensions-${width}.png`});
   await page.locator('table').filter({hasText:'Relocated candidate'}).screenshot({path:`/tmp/aperiodic-independent-table-${width}.png`});
   let controls=0;
   for(const trigger of await page.locator('.figure-preview').all()){
    await trigger.focus();await page.keyboard.press('Enter');assert(await page.locator('.figure-viewer').isVisible());
    assert(await page.locator('.figure-viewer img').evaluate(i=>i.complete&&i.naturalWidth>0));
    if(controls===6||controls===10)await page.screenshot({path:`/tmp/aperiodic-independent-enlarged-${controls+1}-${width}.png`});
    await page.keyboard.press('Escape');assert(await trigger.evaluate(i=>i===document.activeElement));controls++;
   }
   output.layouts.push({width,math:info.math,images:info.images.length,localLinks:links.length,controls});await page.close();
  }
  const plain=await browser.newPage({javaScriptEnabled:false,offline:true,viewport:{width:390,height:844}});
  await plain.goto(pathToFileURL(path.resolve('docs/APERIODIC_CHAIR_TUTORIAL.html')).href);
  output.noScript=await plain.evaluate(()=>({images:document.querySelectorAll('img').length,math:document.querySelectorAll('math').length,overflow:document.documentElement.scrollWidth>innerWidth,loaded:[...document.querySelectorAll('img')].every(i=>i.complete&&i.naturalWidth>0)}));
  assert(output.noScript.loaded&&!output.noScript.overflow);assert.deepEqual(output.errors,[]);assert.deepEqual(output.network,[]);
  fs.writeFileSync('/tmp/aperiodic-independent-tutorial-result.json',JSON.stringify(output,null,2));console.log(JSON.stringify(output,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});

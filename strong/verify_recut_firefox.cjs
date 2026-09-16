// Optional real-browser check. Override the two environment paths as needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {firefox} = require(process.env.PLAYWRIGHT_MODULE || '/tmp/kanpo-review-browser/node_modules/playwright');
(async () => {
  const browser = await firefox.launch({headless: true,
    executablePath: process.env.FIREFOX_PATH || '/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
  try {
    const page = await browser.newPage({viewport: {width: 1400, height: 1100}});
    const errors = [], requests = [], checks = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => {if (/^https?:/.test(request.url())) requests.push(request.url());});
    await page.goto(pathToFileURL(path.resolve('strong/artifacts/recut-chair.html')).href);
    await page.waitForFunction(() => document.querySelector('#view').dataset.rendered === 'one');
    for (const size of ['enlarged', 'actual']) {
      await page.selectOption('#features', size);
      for (const mode of ['one', 'eight', 'many', 'valid', 'periodic']) {
        await page.locator(`.toolbar [data-mode="${mode}"]`).click();
        await page.waitForFunction(value => document.querySelector('#view').dataset.rendered === value, mode);
        const check = await page.evaluate(() => ({count: document.querySelector('#count').textContent,
          faces: Number(document.querySelector('#view').dataset.faces),
          gapDisabled: document.querySelector('#gap').disabled}));
        assert(check.faces > 0);
        assert(check.count.startsWith(String({one: 1, eight: 8, many: 64, valid: 2, periodic: 2}[mode])+' '));
        assert.equal(check.gapDisabled, ['one', 'many'].includes(mode));
        checks.push({size, mode, ...check});
      }
    }
    await page.selectOption('#features', 'enlarged');
    await page.locator('.toolbar [data-mode="eight"]').click();
    const before = await page.locator('#view').screenshot();
    await page.locator('#gap').evaluate(el => {el.value = '65';el.dispatchEvent(new Event('input'));});
    const after = await page.locator('#view').screenshot();
    assert(!before.equals(after));
    const box = await page.locator('#view').boundingBox();
    await page.mouse.move(box.x+box.width/2, box.y+box.height/2);
    await page.mouse.down();await page.mouse.move(box.x+box.width/2+90,box.y+box.height/2+30,{steps:5});await page.mouse.up();
    await page.waitForTimeout(100);
    const rotated = await page.locator('#view').screenshot();assert(!after.equals(rotated));
    await page.mouse.wheel(0,-250);await page.waitForTimeout(100);
    const zoomed = await page.locator('#view').screenshot();assert(!rotated.equals(zoomed));
    await page.locator('#reset').click();
    await page.locator('.toolbar [data-mode="one"]').click();
    await page.screenshot({path:'/tmp/recut-chair-one-firefox.png',fullPage:true});
    await page.locator('.toolbar [data-mode="eight"]').click();
    await page.screenshot({path:'/tmp/recut-chair-eight-firefox.png',fullPage:true});
    await page.locator('.toolbar [data-mode="periodic"]').click();
    await page.screenshot({path:'/tmp/recut-chair-periodic-firefox.png',fullPage:true});
    await page.setViewportSize({width:390,height:844});
    await page.locator('.toolbar [data-mode="one"]').click();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({path:'/tmp/recut-chair-mobile-firefox.png',fullPage:true});
    assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
    fs.writeFileSync('strong/artifacts/recut_chair_firefox.json',JSON.stringify({status:'passed',
      browser:'Firefox',version:browser.version(),local_file_open:true,external_requests:requests,
      checks,separation_control:true,orbit_control:true,zoom_control:true,mobile_no_horizontal_overflow:true,
      page_errors:errors},null,2)+'\n');
    console.log('Firefox file:// passed: five modes, both feature scales, separation, orbit, zoom, mobile layout, zero external requests and zero page errors.');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});

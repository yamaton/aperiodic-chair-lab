// Optional delivery check. No browser automation is needed for mathematical verification.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {firefox} = require(process.env.PLAYWRIGHT_MODULE || '/tmp/kanpo-review-browser/node_modules/playwright');

(async () => {
  const files = process.argv.slice(2);
  assert(files.length, 'Supply one or more local HTML brief paths.');
  const browser = await firefox.launch({headless: true,
    executablePath: process.env.FIREFOX_PATH || '/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
  const checks = [];
  try {
    for (const [index, filename] of files.entries()) {
      const page = await browser.newPage({viewport: {width: 1250, height: 950}});
      const errors = [], requests = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('request', request => {if (/^https?:/.test(request.url())) requests.push(request.url());});
      await page.goto(pathToFileURL(path.resolve(filename)).href);
      assert.match(await page.title(), /one-chair 3D/);
      assert.match(await page.locator('body').innerText(), /not an established theorem/);
      assert.match(await page.locator('body').innerText(), /AI assistance/);
      const math = await page.locator('math').count();
      assert(math >= 10, 'Expected native MathML formulas.');
      const blocks = await page.locator('math[display="block"]').evaluateAll(nodes =>
        nodes.map(node => ({width: node.getBoundingClientRect().width, height: node.getBoundingClientRect().height})));
      assert(blocks.length && blocks.every(box => box.width > 0 && box.height > 15));
      await page.screenshot({path: `/tmp/chair-review-brief-${index}-desktop.png`, fullPage: true});
      await page.setViewportSize({width: 390, height: 844});
      const overflow = await page.evaluate(() => ({width: innerWidth, scroll: document.documentElement.scrollWidth,
        outside: [...document.body.querySelectorAll('*')].filter(el => el.getBoundingClientRect().right > innerWidth)
          .slice(0, 8).map(el => ({tag: el.tagName, className: String(el.className), right: el.getBoundingClientRect().right}))}));
      assert(overflow.scroll <= overflow.width, 'Mobile page overflow: '+JSON.stringify(overflow));
      await page.screenshot({path: `/tmp/chair-review-brief-${index}-mobile.png`, fullPage: true});
      assert.deepEqual(errors, []); assert.deepEqual(requests, []);
      checks.push({file: filename, math_elements: math, display_math_visible: true,
        mobile_no_horizontal_overflow: true, external_requests: requests, page_errors: errors});
      await page.close();
    }
    fs.writeFileSync('strong/artifacts/review_brief_firefox.json', JSON.stringify({status: 'passed',
      browser: 'Firefox', version: browser.version(), local_file_open: true, checks}, null, 2)+'\n');
    console.log('Offline Firefox briefs passed: MathML, desktop/mobile layout, no requests or page errors.');
  } finally {await browser.close();}
})().catch(error => {console.error(error); process.exitCode = 1;});

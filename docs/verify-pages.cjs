// Optional presentation/deployment check, not mathematical verification.
// node docs/verify-pages.cjs [https://host/project/] [report.json]
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const os = require('node:os');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');
const {firefox} = require(process.env.PLAYWRIGHT_MODULE || '/tmp/kanpo-review-browser/node_modules/playwright');

(async () => {
  let server, browser;
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'chair-pages-check-'));
  try {
    let base = process.argv[2];
    if (!base) {
      const root = path.resolve('_site');
      server = http.createServer((request, response) => {
        let name = new URL(request.url, 'http://localhost').pathname;
        if (!name.startsWith('/aperiodic-chair-lab/')) {response.writeHead(404).end(); return;}
        name = decodeURIComponent(name.slice('/aperiodic-chair-lab/'.length));
        const file = path.resolve(root, name + (name.endsWith('/') || !name ? 'index.html' : ''));
        if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
          response.writeHead(404).end(); return;
        }
        response.setHeader('Content-Type', file.endsWith('.json') ? 'application/json' : 'text/html; charset=utf-8');
        response.end(fs.readFileSync(file));
      });
      await new Promise((resolve, reject) => {
        server.once('error', reject);
        server.listen(0, '127.0.0.1', resolve);
      });
      base = `http://127.0.0.1:${server.address().port}/aperiodic-chair-lab/`;
    }
    assert(base.endsWith('/'), 'Supply the project URL with a trailing slash');
    browser = await firefox.launch({headless: true,
      executablePath: process.env.FIREFOX_PATH || '/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
    const context = await browser.newContext({viewport: {width: 1200, height: 900},locale:'en-US'});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const manifestResponse = await context.request.get(base + 'build.json');
    assert.equal(manifestResponse.status(), 200);
    const manifest = await manifestResponse.json();
    for (const [file, hash] of Object.entries(manifest.files)) {
      const response = await context.request.get(base + file);
      assert.equal(response.status(), 200, file);
      assert.equal(crypto.createHash('sha256').update(await response.body()).digest('hex'), hash, file);
    }
    const layouts = [];
    const languages=require('./build-locales.cjs').readCatalogs().map(locale=>locale.code);
    for (const width of [1200, 390]) {
      await page.setViewportSize({width, height: 900});
      assert.equal((await page.goto(base)).status(), 200);
      for(const language of languages){
        await page.locator('#language').selectOption(language);
        assert.equal(await page.locator('html').getAttribute('lang'),language);
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
        const cta=await page.locator('#start-assembly').boundingBox();assert(cta.y+cta.height<900,'Primary activity link should be visible without scrolling');
        assert(new URL(await page.locator('#start-assembly').getAttribute('href')).searchParams.get('lang')===language);
        await page.screenshot({path:`/tmp/chair-pages-home-${language}-${width}.png`,fullPage:true});
        await page.locator('#start-assembly').click();
        assert.equal(await page.locator('html').getAttribute('lang'),language);
        await page.locator('#project-home').click();
        assert.equal(await page.locator('#language').inputValue(),language);
      }
      await page.locator('#language').selectOption('ja');
      await page.locator('#start-assembly').click();await page.waitForURL(base+'assembly/?lang=ja');
      assert.equal(await page.locator('html').getAttribute('lang'),'ja');
      for(let step=0;step<3;step++)await page.locator('#hint').click();
      await page.locator('#attach').click();assert.equal(await page.evaluate(()=>ChairPrototype.snapshot().state.tiles.length),2);
      await page.locator('#project-home').click();await page.waitForURL(base+'?lang=ja');
      assert.equal(await page.locator('#language').inputValue(),'ja');
      await page.locator('#watch-demo').click();await page.waitForURL(base+'assembly/?lang=ja&demo=1');
      await page.waitForFunction(()=>document.querySelector('#play-demo').dataset.playing==='true');
      await page.locator('#demo-toggle').click();
      for(let step=0;step<5;step++)await page.locator('#demo-next').click();
      assert.equal(await page.locator('#play-demo').getAttribute('data-ended'),'true');
      await page.locator('#demo-close').click();await page.locator('#guide-close').click();
      await page.locator('#project-home').click();await page.locator('#language').selectOption('en');
      await page.locator('#math-tutorial').click();
      await page.waitForURL(base + 'tutorial/');
      assert.equal(await page.locator('math').count(), manifest.tutorial_counts.math);
      assert.equal(await page.locator('.figure-preview').count(), manifest.tutorial_counts.images);
      assert(await page.locator('.figure-preview img').evaluateAll(images => images.every(img =>
        img.complete && img.naturalWidth > 0 && img.src.startsWith('data:') && img.alt)));
      const scroll = await page.evaluate(() => document.documentElement.scrollWidth);
      assert(scroll <= width, `Tutorial overflows at ${width}px`);
      const trigger = page.locator('.figure-preview').nth(4);
      await trigger.focus();
      await page.keyboard.press('Enter');
      assert(await page.locator('.figure-viewer').isVisible());
      await page.locator('.figure-viewer img').evaluate(img => img.decode());
      assert(await page.locator('.figure-viewer img').evaluate(img => img.width >= 1000));
      await page.keyboard.press('Escape');
      assert(await trigger.evaluate(button => button === document.activeElement));
      await page.getByRole('link', {name: 'Project home', exact: true}).click();
      await page.waitForURL(base);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({path: `/tmp/chair-pages-home-${width}.png`, fullPage: true});
      layouts.push({width, tutorial_scroll_width: scroll, figure_keyboard_control: true});
    }
    await page.locator('#shape-viewer').click();
    await page.waitForURL(base + 'viewer/');
    await page.locator('button[data-mode="eight"]').click();
    assert.match(await page.locator('#title').innerText(), /Eight copies/);
    await page.locator('#features').selectOption('actual');
    assert(await page.locator('#view').evaluate(canvas => canvas.width > 0 && canvas.height > 0));
    await page.getByRole('link', {name: 'Tutorial', exact: true}).click();
    await page.waitForURL(base + 'tutorial/');
    const downloadEvent = page.waitForEvent('download');
    await page.getByRole('link', {name: 'Download HTML', exact: true}).click();
    const download = await downloadEvent;
    assert.equal(download.suggestedFilename(), 'aperiodic-chair-tutorial.html');
    const filename = path.join(scratch, download.suggestedFilename());
    await download.saveAs(filename);
    await context.setOffline(true);
    await page.goto(pathToFileURL(filename).href);
    assert.equal(await page.locator('math').count(), manifest.tutorial_counts.math);
    assert.equal(await page.locator('.figure-preview').count(), manifest.tutorial_counts.images);
    assert(await page.locator('.figure-preview img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0)));
    assert(await page.locator('a[href]').evaluateAll(links => links.every(link => /^(#|https?:|mailto:)/.test(link.getAttribute('href')))));
    await context.setOffline(false);
    const blocked=await browser.newContext({locale:'en-US',viewport:{width:390,height:900}});
    await blocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked');}}));
    const blockedPage=await blocked.newPage();await blockedPage.goto(base);
    await blockedPage.locator('#language').selectOption('ja');await blockedPage.locator('#start-assembly').click();
    assert.equal(await blockedPage.locator('#language').inputValue(),'ja','Navigation carries language even without storage');
    await blockedPage.locator('#language').selectOption('en');await blockedPage.reload();
    assert.equal(await blockedPage.locator('#language').inputValue(),'en','A manual change updates the navigation language');
    await blocked.close();
    assert.deepEqual(errors, []);
    const report = {checked_at: new Date().toISOString(), scope: 'Presentation, navigation, artifact hashes and offline download; not mathematical verification',
      base_url: base, manifest, layouts, home_languages:languages,primary_activity_navigation:true,demo_entry:true,language_handoff_without_storage:true,viewer_controls: true, offline_download: true, page_errors: errors};
    if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report, null, 2));
  } finally {
    if (browser) await browser.close();
    if (server?.listening) await new Promise(resolve => server.close(resolve));
    fs.rmSync(scratch, {recursive: true});
  }
})().catch(error => {console.error(error); process.exitCode = 1;});

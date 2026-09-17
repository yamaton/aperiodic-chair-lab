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
    const context = await browser.newContext({viewport: {width: 1200, height: 900}});
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
    for (const width of [1200, 390]) {
      await page.setViewportSize({width, height: 900});
      assert.equal((await page.goto(base)).status(), 200);
      await page.getByRole('link', {name: 'Read the illustrated tutorial →'}).click();
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
    await page.getByRole('link', {name: 'Interactive chair viewer', exact: true}).click();
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
    assert.deepEqual(errors, []);
    const report = {checked_at: new Date().toISOString(), scope: 'Presentation, navigation, artifact hashes and offline download; not mathematical verification',
      base_url: base, manifest, layouts, viewer_controls: true, offline_download: true, page_errors: errors};
    if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report, null, 2));
  } finally {
    if (browser) await browser.close();
    if (server?.listening) await new Promise(resolve => server.close(resolve));
    fs.rmSync(scratch, {recursive: true});
  }
})().catch(error => {console.error(error); process.exitCode = 1;});

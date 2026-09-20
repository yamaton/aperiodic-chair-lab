// Optional presentation check; this does not verify mathematical theorems.
// Run from the root; use PLAYWRIGHT_MODULE and FIREFOX_PATH for other installs.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL, fileURLToPath} = require('node:url');
const {firefox} = require(process.env.PLAYWRIGHT_MODULE || '/tmp/kanpo-review-browser/node_modules/playwright');

(async () => {
  const browser = await firefox.launch({headless: true,
    executablePath: process.env.FIREFOX_PATH || '/tmp/kanpo-review-browser/browsers/firefox-1543/firefox/firefox'});
  try {
    const page = await browser.newPage({viewport: {width: 1200, height: 900}});
    const requests = [], errors = [];
    page.on('request', request => {if (/^https?:/.test(request.url())) requests.push(request.url());});
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(path.resolve('docs/APERIODIC_CHAIR_TUTORIAL.html')).href);
    assert.match(await page.title(), /How one shape can enforce order/);
    const images = await page.locator('.figure-preview img').evaluateAll(nodes => nodes.map(n => ({
      embedded: n.src.startsWith('data:'), loaded: n.complete && n.naturalWidth > 0,
      alt: n.alt,
    })));
    assert.equal(images.length, 11);
    assert.match(images[10].alt, /Recorded and relocated triangular port footprints/);
    assert(images.every(n => n.embedded && n.loaded && n.alt));
    const mathCount = await page.locator('math').count();
    assert(mathCount > 250, 'Expected native MathML throughout the expanded tutorial.');
    assert.equal(await page.locator('span.math:not(:has(math))').count(), 0,
      'A formula fell back to raw TeX.');
    const links = await page.locator('a[href]').evaluateAll(nodes => nodes.map(n => n.href));
    const local = [...new Set(links.filter(href => href.startsWith('file:')))];
    const missingAnchors = [];
    for (const href of local) {
      const url = new URL(href);
      const filename = fileURLToPath(url);
      assert(fs.existsSync(filename), `Missing linked file: ${filename}`);
      if (!url.hash) continue;
      const anchor = decodeURIComponent(url.hash.slice(1));
      if (filename === path.resolve('docs/APERIODIC_CHAIR_TUTORIAL.html')) {
        if (!await page.evaluate(id => Boolean(document.getElementById(id)), anchor)) missingAnchors.push(href);
      } else if (filename.endsWith('.md')) {
        const headings = fs.readFileSync(filename, 'utf8').split('\n')
          .filter(line => /^#{1,6} /.test(line))
          .map(line => line.replace(/^#+ /, '').toLowerCase()
            .replace(/[^\p{L}\p{N}_\-\s]/gu, '').replace(/\s/g, '-'));
        if (!headings.includes(anchor)) missingAnchors.push(href);
      } else throw new Error(`No anchor checker for ${href}`);
    }
    assert.deepEqual(missingAnchors, []);
    const layouts = [];
    const enlarged = [];
    for (const width of [1200, 390]) {
      await page.setViewportSize({width, height: width === 1200 ? 900 : 844});
      const layout = await page.evaluate(() => ({
        viewport: innerWidth, scroll: document.documentElement.scrollWidth,
        display_formulas: [...document.querySelectorAll('math[display="block"]')].map(n => {
          const r = n.getBoundingClientRect(); return {width: r.width, height: r.height};
        }),
      }));
      assert(layout.scroll <= layout.viewport, `Horizontal page overflow at ${width}: ${layout.scroll}`);
      assert(layout.display_formulas.every(r => r.width > 0 && r.height > 15));
      layouts.push(layout);
      await page.screenshot({path: `/tmp/chair-tutorial-${width}.png`});
      await page.getByRole('heading', {name: '10.1 Move and enlarge the ports while preserving the rules', exact: true}).scrollIntoViewIfNeeded();
      await page.screenshot({path: `/tmp/chair-tutorial-dimensions-${width}.png`});
      const dimensions = page.locator('table').filter({hasText: 'Relocated candidate'});
      assert.equal(await dimensions.count(), 1);
      await dimensions.screenshot({path: `/tmp/chair-tutorial-dimension-table-${width}.png`});
      for (const [index, picture] of (await page.locator('.figure-preview img').all()).entries()) {
        await picture.screenshot({path: `/tmp/chair-tutorial-figure-${index + 1}-${width}.png`});
      }
      const previews = await page.locator('.figure-preview').all();
      for (const [index, trigger] of previews.entries()) {
        await trigger.focus();
        await page.keyboard.press('Enter');
        assert(await page.locator('.figure-viewer').isVisible(), 'Keyboard activation did not open the figure.');
        const full = await page.locator('.figure-viewer img').evaluate(async img => {
          await img.decode();
          return {src: img.src, alt: img.alt, width: img.getBoundingClientRect().width};
        });
        assert.equal(full.src, await trigger.locator('img').getAttribute('src'));
        assert.equal(full.alt, images[index].alt);
        assert(full.width >= 1000, 'Full-size view still shrinks labels on small screens.');
        const initialPan = await page.locator('.figure-scroll').evaluate(region => ({
          actual: region.scrollLeft, expected: (region.scrollWidth - region.clientWidth) / 2,
        }));
        assert(Math.abs(initialPan.actual - initialPan.expected) <= 1,
          'Enlargement should open horizontally centered.');
        const horizontalPan = await page.locator('.figure-scroll').evaluate(region => {
          region.scrollLeft = 100;
          return region.scrollLeft;
        });
        if (width === 390) assert(horizontalPan > 0, 'Full-size diagram cannot be panned.');
        if (width === 390 && (index === 4 || index === 6 || index === 10)) {
          await page.locator('.figure-scroll').evaluate((region, left) => {region.scrollLeft = left;}, initialPan.actual);
          await page.screenshot({path: index === 4 ? '/tmp/chair-tutorial-enlarged-mobile.png'
            : index === 6 ? '/tmp/chair-tutorial-cap-enlarged-mobile.png'
              : '/tmp/chair-tutorial-dimensions-enlarged-mobile.png'});
        }
        if (index % 2 === 0) await page.keyboard.press('Escape');
        else await page.getByRole('button', {name: 'Close', exact: true}).click();
        assert(!await page.locator('.figure-viewer').isVisible());
        assert(await trigger.evaluate(button => document.activeElement === button), 'Focus was not restored.');
        enlarged.push({figure: index + 1, viewport_width: width, image_width: full.width,
          keyboard_open: true, close_and_focus_restore: true, horizontal_pan: horizontalPan > 0,
          initially_centered: true});
      }
    }
    const noScript = await browser.newPage({javaScriptEnabled: false});
    await noScript.goto(pathToFileURL(path.resolve('docs/APERIODIC_CHAIR_TUTORIAL.html')).href);
    assert.equal(await noScript.locator('img').count(), 11);
    assert(await noScript.locator('img').evaluateAll(nodes => nodes.every(n => n.complete && n.naturalWidth > 0)));
    assert.equal(await noScript.locator('math').count(), mathCount);
    await noScript.close();
    assert.deepEqual(requests, []); assert.deepEqual(errors, []);
    const files = ['docs/APERIODIC_CHAIR_TUTORIAL.md', 'docs/APERIODIC_CHAIR_TUTORIAL.html',
      'docs/tutorial.css', 'docs/tutorial-controls.html', 'docs/draw_tutorial_figures.py', 'docs/verify_tutorial.cjs',
      'strong/artifacts/port-dimensions.svg', 'strong/audit/investigate_port_dimensions.py',
      'strong/audit/port_dimensions.json',
      ...fs.readdirSync('docs/figures').filter(f => f.startsWith('tutorial-')).map(f => `docs/figures/${f}`)];
    const sha256 = Object.fromEntries(files.map(f => [f,
      crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')]));
    const report = {status: 'passed', date: new Date().toISOString().slice(0, 10),
      scope: 'Presentation and local links only; not mathematical verification',
      browser: 'Firefox', browser_version: browser.version(),
      desktop_viewport: [1200, 900], mobile_viewport: [390, 844], local_file_open: true,
      embedded_images: images.length, mathml_elements: mathCount,
      visible_display_formulas: layouts[0].display_formulas.length,
      local_links_checked: local.length, missing_anchors: missingAnchors,
      mobile_horizontal_overflow: false, external_requests: requests, page_errors: errors, sha256};
    report.figure_enlargement = enlarged;
    report.without_javascript = 'All eleven figures and all formulas remain available; enlargement controls require JavaScript';
    fs.writeFileSync('docs/tutorial_verification.json', JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report, null, 2));
  } finally {await browser.close();}
})().catch(error => {console.error(error); process.exitCode = 1;});

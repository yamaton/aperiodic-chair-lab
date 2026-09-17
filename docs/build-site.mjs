// Build only the reader-facing Pages artifact; leave the repository edition
// and preserved research data untouched. Requires Pandoc 3.11 and Node.js.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const buildAssembly=require('./build-assembly.cjs');
const buildPreview=require('./site-preview.cjs');
const {embedLocales}=require('./build-locales.cjs');

const root = process.cwd();
const output = path.join(root, '_site');
const repository = 'https://github.com/yamaton/aperiodic-chair-lab';
const revision = process.env.GITHUB_SHA || execFileSync('git', ['rev-parse', 'HEAD'], {encoding: 'utf8'}).trim();
assert.match(revision, /^[a-f0-9]{40}$/);
const site = new URL(process.env.SITE_URL || 'https://tritonlab.io/aperiodic-chair-lab/');
assert.equal(site.protocol, 'https:');
assert(!site.search && !site.hash);
if (!site.pathname.endsWith('/')) site.pathname += '/';
const pandoc = process.env.PANDOC || 'pandoc';
assert.match(execFileSync(pandoc, ['--version'], {encoding: 'utf8'}), /^pandoc 3\.11\s/);
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'chair-pages-'));
const escape = text => text.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;');
const sha256 = data => crypto.createHash('sha256').update(data).digest('hex');
const files = ['index.html', 'assembly/index.html', 'tutorial/index.html', 'viewer/index.html', 'downloads/tutorial.html'];
for (const dir of ['assembly', 'tutorial', 'viewer', 'downloads']) fs.mkdirSync(path.join(output, dir), {recursive: true});
const common = ['--from=markdown-implicit_figures', '--to=html5', '--standalone',
  '--embed-resources', '--math-method=mathml', '--resource-path=docs', '--css=tutorial.css', '--fail-if-warnings'];
try {
  let home=fs.readFileSync('docs/site-index.html','utf8');
  for(const [marker,file] of [['STYLE','site.css'],['SCRIPT','site.js']])
    home=home.replace(`/* ${marker} */`,()=>fs.readFileSync('docs/'+file,'utf8'));
  home=embedLocales(home,'home');
  home=home.replace('<!-- PREVIEW -->',()=>buildPreview());
  fs.writeFileSync(path.join(output,'index.html'),home);
  fs.writeFileSync(path.join(output,'assembly/index.html'),buildAssembly({tutorialHref:'../tutorial/',homeHref:'../'}));
  for (const edition of ['online', 'download']) {
    const home = edition === 'online' ? '../' : site.href;
    const extra = edition === 'online'
      ? '<a href="../downloads/tutorial.html" download="aperiodic-chair-tutorial.html">Download HTML</a>'
      : `<a href="${escape(site.href)}tutorial/">Read online</a>`;
    const nav = path.join(scratch, edition + '-nav.html');
    fs.writeFileSync(nav, `<nav aria-label="Tutorial navigation"><a href="${escape(home)}">Project home</a> · ${extra} · <a href="${repository}/blob/${revision}/docs/APERIODIC_CHAIR_TUTORIAL.md">Source</a></nav>\n`);
    execFileSync(pandoc, ['docs/APERIODIC_CHAIR_TUTORIAL.md', ...common, '--toc', '--toc-depth=2',
      '--lua-filter=docs/pages-links.lua', '--metadata=repository_revision:' + revision,
      '--metadata=site_url:' + site.href, '--metadata=edition:' + edition,
      '--include-before-body=' + nav, '--include-after-body=docs/tutorial-controls.html',
      '--output=' + path.join(output, edition === 'online' ? 'tutorial/index.html' : 'downloads/tutorial.html')], {stdio: 'inherit'});
  }
  const viewer = fs.readFileSync('strong/artifacts/recut-chair.html', 'utf8')
    .replace(/href="([^"]+)"/g, (attribute, href) => {
      if (/^(#|[a-z][\w+.-]*:|\/\/)/i.test(href)) return attribute;
      const target = new URL(href, 'https://repository.invalid/strong/artifacts/recut-chair.html');
      assert(fs.existsSync(path.join(root, target.pathname)), `Missing viewer link: ${href}`);
      return `href="${repository}/blob/${revision}${target.pathname}${target.hash}"`;
    })
    .replace('<body>', '<body>\n<nav aria-label="Project navigation" style="padding:12px 20px"><a href="../">Project home</a> · <a href="../tutorial/">Tutorial</a></nav>');
  fs.writeFileSync(path.join(output, 'viewer/index.html'), viewer);
  fs.writeFileSync(path.join(output, '.nojekyll'), '');

  let localLinks = 0;
  let tutorialCounts;
  for (const filename of files) {
    const content = fs.readFileSync(path.join(output, filename), 'utf8');
    const base = new URL(filename, site);
    for (const [, raw] of content.matchAll(/href="([^"]+)"/g)) {
      const href = raw.replaceAll('&amp;', '&');
      const url = new URL(href, base);
      if (url.origin !== site.origin) continue;
      assert(url.pathname.startsWith(site.pathname), `Link leaves the project path: ${href}`);
      let relative = decodeURIComponent(url.pathname.slice(site.pathname.length));
      if (relative.endsWith('/')) relative += 'index.html';
      const target = path.join(output, relative);
      assert(fs.existsSync(target), `Missing published link: ${filename} → ${relative}`);
      if (url.hash) {
        const id = decodeURIComponent(url.hash.slice(1));
        assert(fs.readFileSync(target, 'utf8').includes(`id="${id}"`), `Missing published anchor: ${href}`);
      }
      localLinks++;
    }
    if (filename.includes('tutorial')) {
      const counts = {math: (content.match(/<math\b/g) || []).length,
        images: (content.match(/<img\s[^>]*src="data:/g) || []).length};
      assert(counts.math > 0 && counts.images > 0, 'Missing embedded tutorial content');
      assert.equal(counts.images, (content.match(/<img\s[^>]*src=/g) || []).length);
      if (tutorialCounts) assert.deepEqual(counts, tutorialCounts, 'Tutorial editions differ');
      tutorialCounts = counts;
      assert(!content.includes('href="../strong/') && !content.includes('href="../formal/'));
    }
  }
  const manifest = {site_url: site.href, source_revision: revision,
    tutorial_source_sha256: sha256(fs.readFileSync('docs/APERIODIC_CHAIR_TUTORIAL.md')),
    local_links_checked: localLinks,
    tutorial_counts: tutorialCounts,
    files: Object.fromEntries(files.map(file => [file, sha256(fs.readFileSync(path.join(output, file)))]))};
  fs.writeFileSync(path.join(output, 'build.json'), JSON.stringify(manifest, null, 2) + '\n');
  console.log(JSON.stringify(manifest, null, 2));
} finally {
  fs.rmSync(scratch, {recursive: true});
}

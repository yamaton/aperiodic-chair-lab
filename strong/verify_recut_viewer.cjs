// Exercise the actual embedded viewer, including surface holes and all modes.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('strong/artifacts/recut-chair.html', 'utf8');
assert(!html.includes('__DATA__'));
assert(!/<script[^>]+src=/.test(html));
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes = new Map();
const finite = (...values) => values.forEach(v => assert(Number.isFinite(v)));
let fills = 0;
const context = {setTransform: finite, clearRect: finite, beginPath() {}, closePath() {},
  moveTo: finite, lineTo: finite, arc: finite, fill() {fills++;}, stroke() {},
  fillText(text, x, y) {finite(x, y);}, setLineDash() {}};
function node(selector) {
  if (!nodes.has(selector)) nodes.set(selector, {
    value: ({'#features': 'enlarged', '#gap': '0'})[selector], dataset: {},
    addEventListener() {}, getContext: () => context,
    getBoundingClientRect: () => ({width: 950, height: 560}),
  });
  return nodes.get(selector);
}
const sandbox = vm.createContext({document: {querySelector: node, querySelectorAll: () => [], body: {}},
  window: {devicePixelRatio: 1}, requestAnimationFrame() {return 1;},
  ResizeObserver: class {observe() {}}});
vm.runInContext(script, sandbox);
assert(fills > 0);
const read = code => vm.runInContext(code, sandbox);
const manifest = JSON.parse(fs.readFileSync('strong/audit/frozen_v1/manifest.json'));
assert.equal(read('DATA.candidate_sha256'), manifest.candidate_sha256);
assert.equal(read('DATA.faces.length'), 24);
assert.equal(read('DATA.faces.reduce((n,f)=>n+f.ports.length,0)'), 192);
for (const size of ['actual', 'enlarged']) {
  node('#features').value = size;
  for (const mode of ['one', 'eight', 'many', 'valid', 'periodic']) {
    read(`selectMode('${mode}')`);
    assert.equal(node('#view').dataset.rendered, mode);
    assert(Number(node('#view').dataset.faces) > 0);
    assert.equal(node('#gap').disabled, ['one', 'many'].includes(mode));
    assert.equal(read(`DATA.placements['${mode}'].length`), {one: 1, eight: 8, many: 64, valid: 2, periodic: 2}[mode]);
    assert(read('scene.every(f=>f.points.every(p=>p.every(Number.isFinite)))'));
  }
  // Flat strips must leave exactly the eight holes, at both display scales.
  const areas = read(`DATA.faces.map(f=>{
    const width=DATA.width*${size === 'enlarged' ? 3 : 1};
    const flat=localMesh(f,width,DATA.depth).filter(q=>q.kind===0);
    const area=flat.reduce((sum,q)=>sum+Math.hypot(...cross(q.points[1].map((x,i)=>x-q.points[0][i]),q.points[3].map((x,i)=>x-q.points[0][i]))),0);
    return [area,1-8*(2*width)**2];})`);
  for (const [actual, expected] of areas) assert(Math.abs(actual-expected) < 1e-10);
}
read("selectMode('eight')");
node('#gap').value = '0'; read('rebuild()'); const assembled = read('scene.length');
node('#gap').value = '75'; read('rebuild()');
assert(read('scene.length') > assembled, 'separation exposes the internal faces');
assert.equal(node('#gap-value').textContent, '75%');
console.log('Recut viewer passed: frozen data, all five modes at both scales, finite rendering, exact flat-hole areas, and exposed assembly interfaces.');

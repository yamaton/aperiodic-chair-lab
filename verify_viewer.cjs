// Exercise the offline explorer's actual script without external packages.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const geometry = JSON.parse(fs.readFileSync('artifacts/geometry.json', 'utf8'));
for (const path of ['viewer.html', 'artifacts/explorer.html']) {
const html = fs.readFileSync(path, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes = new Map();
const finite = (...values) => values.forEach(value => assert(Number.isFinite(value)));
const ctx = { scale: finite, clearRect: finite, beginPath() {}, closePath() {},
              moveTo: finite, lineTo: finite, fill() {}, stroke() {} };
function node(selector) {
  if (!nodes.has(selector)) nodes.set(selector, {
    value: ({'#mode': 'stack', '#layers': '5', '#radius': '1', '#explode': '0'})[selector],
    addEventListener() {}, getContext: () => ctx,
    getBoundingClientRect: () => ({width: 1000, height: 590}),
  });
  return nodes.get(selector);
}
const sandbox = vm.createContext({document: {querySelector: node},
  window: {devicePixelRatio: 1}, ResizeObserver: class {observe() {}}});
vm.runInContext(script, sandbox);
// Keep the embedded offline geometry in agreement with the Python exports.
const data = JSON.parse(vm.runInContext('JSON.stringify(DATA)', sandbox));
for (const key of ['height', 'faces', 'colors']) assert.deepEqual(data[key], geometry[key]);
assert.equal(node('#badge').textContent, '45 identical blocks / 5 layers');
for (const mode of ['stack', 'block', 'control', 'fault']) {
  for (const [layers, radius, explode] of [[1, 0, 0], [5, 1, 40], [12, 3, 100]]) {
    for (const [key, value] of Object.entries({mode, layers, radius, explode})) {
      node('#' + key).value = String(value);
    }
    vm.runInContext('rebuild()', sandbox);
    assert(node('#readout').innerHTML.length > 20);
    const count = vm.runInContext('scene.length', sandbox);
    assert.equal(count, mode === 'block' ? 8 : layers * (2 * radius + 1) ** 2 * 8);
  }
}
console.log(`${path}: 12 control combinations rendered with finite coordinates.`);
}

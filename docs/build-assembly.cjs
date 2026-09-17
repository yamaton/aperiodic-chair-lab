// Reproducibly package the prototype as one offline HTML file.
const fs=require('node:fs');
const crypto=require('node:crypto');
const certificate=fs.readFileSync('strong/audit/motif_grouping_certificate.json');
const c=JSON.parse(certificate);
const data={faces:c.face_table,group:c.derived_group,
  candidate_sha256:c.candidate_sha256,
  certificate_sha256:crypto.createHash('sha256').update(certificate).digest('hex')};
const input='docs/assembly/';
let html=fs.readFileSync(input+'page.html','utf8');
html=html.replace('<!-- GUIDE -->',()=>fs.readFileSync(input+'guide.html','utf8'));
for(const [marker,file] of [['STYLE','style.css'],['ENGINE','engine.js'],['I18N','i18n.js'],['APP','app.js']])
  html=html.replace(`/* ${marker} */`,()=>fs.readFileSync(input+file,'utf8'));
html=html.replace('/* DATA */',()=>`const CHAIR_DATA=${JSON.stringify(data)};`);
// An isolated copy uses the same renderer, rules and handlers; no recursive demo.
const demo=html.replace('<head>','<head><script>window.CHAIR_DEMO=true;</script>');
const demoSource=JSON.stringify(demo).replace(/</g,'\\u003c');
html=html.replace('</body>',()=>`<script>const CHAIR_DEMO_DOCUMENT=${demoSource};</script><script>${fs.readFileSync(input+'demo.js','utf8')}</script></body>`);
fs.writeFileSync('docs/assembly.html',html);
console.log('Built docs/assembly.html from the preserved motif certificate.');

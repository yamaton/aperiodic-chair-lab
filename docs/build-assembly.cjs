// Reproducibly package the prototype as one offline HTML file.
const fs=require('node:fs');
const crypto=require('node:crypto');
function buildAssembly({tutorialHref='APERIODIC_CHAIR_TUTORIAL.html',homeHref=null}={}){
const certificate=fs.readFileSync('strong/audit/motif_grouping_certificate.json');
const c=JSON.parse(certificate);
const data={faces:c.face_table,group:c.derived_group,
  candidate_sha256:c.candidate_sha256,
  certificate_sha256:crypto.createHash('sha256').update(certificate).digest('hex')};
const input='docs/assembly/';
let html=fs.readFileSync(input+'page.html','utf8');
html=html.replace('<!-- PARENT LAB -->',()=>fs.readFileSync(input+'parent-lab.html','utf8'));
html=html.replace('<!-- GUIDE -->',()=>fs.readFileSync(input+'guide.html','utf8'));
html=html.replace('<!-- RULE LAB -->',()=>fs.readFileSync(input+'rule-lab.html','utf8'));
html=html.replaceAll('APERIODIC_CHAIR_TUTORIAL.html',tutorialHref);
if(homeHref)html=html.replace('<p class="eyebrow">APERIODIC CHAIR LAB · INTERACTIVE PROTOTYPE</p>',`<a id="project-home" class="eyebrow" href="${homeHref}" aria-label="プロジェクトのトップへ">APERIODIC CHAIR LAB</a>`);
html=require('./build-locales.cjs').embedLocales(html,'assembly');
for(const [marker,file] of [['STYLE','style.css'],['RULE_STYLE','rule-lab.css'],['RULE_MODEL','rule-model.js'],['RULE_LAB','rule-lab.js'],['ENGINE','engine.js'],['PARENT_RULES','parent-rules.js'],['PARENT_LAB','parent-lab.js'],['MOTION','motion.js'],['I18N','i18n.js'],['FEEDBACK','feedback.js'],['APP','app.js']])
  html=html.replace(`/* ${marker} */`,()=>fs.readFileSync(input+file,'utf8'));
html=html.replace('/* DATA */',()=>`const CHAIR_DATA=${JSON.stringify(data)};`);
html=html.replace('/* RULE_DATA */',()=>`const CHAIR_RULE_DATA=${fs.readFileSync(input+'rule-data.json','utf8').trim()};`);
// An isolated copy uses the same renderer, rules and handlers; no recursive demo.
const demo=html.replace('<head>','<head><script>window.CHAIR_DEMO=true;</script>');
const demoSource=JSON.stringify(demo).replace(/</g,'\\u003c');
html=html.replace('</body>',()=>`<script>const CHAIR_DEMO_DOCUMENT=${demoSource};</script><script>${fs.readFileSync(input+'demo.js','utf8')}</script></body>`);
return html;
}
module.exports=buildAssembly;
if(require.main===module){
  fs.writeFileSync('docs/assembly.html',buildAssembly());
  console.log('Built docs/assembly.html from the preserved motif certificate.');
}

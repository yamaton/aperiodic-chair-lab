// Shared build-time catalog validation and offline embedding for both entry points.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
function readCatalogs(directory=path.join(__dirname,'locales')){
  const catalogs=fs.readdirSync(directory).filter(file=>file.endsWith('.json')).map(file=>JSON.parse(fs.readFileSync(path.join(directory,file),'utf8')));
  const base=catalogs.find(locale=>locale.code==='en');assert(base,'English fallback is required');
  const codes=new Set();
  const placeholders=text=>[...text.matchAll(/\{(\w+)\}/g)].map(match=>match[1]).sort();
  for(const locale of catalogs){
    assert(/^[a-z]{2}(?:-[A-Za-z0-9]+)*$/.test(locale.code),'Invalid language code');
    assert(!codes.has(locale.code),'Duplicate language code');codes.add(locale.code);
    assert(locale.name&&['ltr','rtl'].includes(locale.dir),'Missing language metadata');
    for(const scope of ['home','assembly']){
      assert.deepEqual(Object.keys(locale[scope]).sort(),Object.keys(base[scope]).sort(),`${locale.code}/${scope}: translation keys differ`);
      for(const [key,value] of Object.entries(locale[scope])){
        assert(typeof value==='string'&&value.trim(),`${locale.code}: empty translation ${key}`);
        assert.deepEqual(placeholders(value),placeholders(base[scope][key]),`${locale.code}: placeholders differ for ${key}`);
      }
    }
  }
  return catalogs;
}
function embedLocales(html,scope){
  const locales=readCatalogs().map(({code,name,dir,...messages})=>({code,name,dir,messages:messages[scope]}));
  const escape=text=>text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
  html=html.replace(/(<select id="language">)[\s\S]*?(<\/select>)/,(_,open,close)=>open+locales.map(locale=>`<option value="${locale.code}" lang="${locale.code}" dir="${locale.dir}">${escape(locale.name)}</option>`).join('')+close);
  return html.replace('/* LANGUAGE */',()=>`const CHAIR_LOCALES=${JSON.stringify(locales).replaceAll('<','\\u003c')};\n${fs.readFileSync(path.join(__dirname,'site-language.js'),'utf8')}`);
}
module.exports={readCatalogs,embedLocales};

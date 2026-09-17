/* Shared offline localization runtime. Catalogs and selector options come from locales/*.json. */
const ChairLanguage=(()=>{
  const catalogs=new Map(CHAIR_LOCALES.map(locale=>[locale.code,locale]));
  const supported=value=>catalogs.has(value),key='chair-assembly-language';
  let language='en';
  function match(value){
    if(!value)return null;
    const exact=[...catalogs.keys()].find(code=>code.toLowerCase()===value.toLowerCase());
    if(exact)return exact;
    return supported(value.split('-')[0])?value.split('-')[0]:null;
  }
  function read(){
    const requested=match(new URL(location.href).searchParams.get('lang'));
    if(requested)return requested;
    try{const saved=match(localStorage.getItem(key));if(saved)return saved;}catch{}
    for(const preferred of navigator.languages||[navigator.language]){const found=match(preferred);if(found)return found;}
    return 'en';
  }
  function save(value){
    if(!supported(value))return;
    try{localStorage.setItem(key,value);}catch{}
    try{const url=new URL(location.href);if(url.searchParams.has('lang')){url.searchParams.set('lang',value);history.replaceState(null,'',url);}}catch{}
  }
  function apply(value,persist=false){
    language=supported(value)?value:'en';
    document.documentElement.lang=language;document.documentElement.dir=catalogs.get(language).dir;
    if(persist)save(language);
  }
  function t(source,values={}){
    const message=catalogs.get(language).messages[source]??catalogs.get('en').messages[source]??source;
    return message.replace(/\{(\w+)\}/g,(_,name)=>{
      const value=String(values[name]??`{${name}}`);
      // Keep mathematical symbols and coordinates readable inside right-to-left prose.
      return catalogs.get(language).dir==='rtl'&&/^[\d\sA-Zxyz+−\-.,()/×↑↓←→↶↷]+$/.test(value)?`\u2066${value}\u2069`:value;
    });
  }
  const has=source=>Object.hasOwn(catalogs.get('en').messages,source);
  return {read,save,supported,apply,t,has};
})();

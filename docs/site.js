(()=>{
  const select=document.getElementById('language');
  function render(language){
    ChairLanguage.apply(language);select.value=document.documentElement.lang;
    document.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=ChairLanguage.t(el.dataset.i18n);});
    document.querySelectorAll('[data-activity]').forEach(link=>{
      const url=new URL(link.href);url.searchParams.set('lang',language);link.href=url.href;
    });
    document.querySelector('footer nav').setAttribute('aria-label',ChairLanguage.t('Project resources'));
    document.querySelector('meta[name=description]').content=ChairLanguage.t('Page description');
  }
  select.onchange=()=>{ChairLanguage.save(select.value);render(select.value);};
  render(ChairLanguage.read());
})();

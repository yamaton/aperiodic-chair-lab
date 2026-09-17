const ChairI18n=(()=>{
  const t=ChairLanguage.t;
  // Capture only the template's original text nodes and accessibility labels.
  // Dynamic UI text is translated explicitly by app.js on every render.
  function bind(root){
    const texts=[],attributes=[],walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
    while(walker.nextNode()){
      const node=walker.currentNode;
      if(node.parentElement.closest('script,style,noscript'))continue;
      if(ChairLanguage.has(node.textContent.trim()))texts.push([node,node.textContent]);
    }
    for(const el of root.querySelectorAll('[aria-label],[title]'))for(const name of ['aria-label','title']){
      const value=el.getAttribute(name);if(value&&ChairLanguage.has(value))attributes.push([el,name,value]);
    }
    return ()=>{
      for(const [node,source] of texts)node.textContent=source.replace(source.trim(),()=>t(source.trim()));
      for(const [el,name,source] of attributes)el.setAttribute(name,t(source));
    };
  }
  return {t,bind,initialLanguage:ChairLanguage.read,setLanguage:ChairLanguage.apply};
})();

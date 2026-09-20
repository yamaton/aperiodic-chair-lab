/* Signed equations exported from the preserved substitution contact closures. */
(function(root){
  'use strict';
  const defaults=p=>Array.from({length:Math.max(...p.labels.map(Math.abs))},(_,i)=>i+1);
  const value=(key,values)=>Math.sign(key)*values[Math.abs(key)-1];
  function evaluate(p,values){
    const tests=p.equations.map(([a,b])=>value(a,values)+value(b,values)===0);
    const fine=p.fine.map(row=>row.every(i=>tests[i]));
    const parent=p.parent.map(row=>row.every(i=>tests[i]));
    const both=[],extra=[],lost=[];
    fine.forEach((ok,i)=>{if(ok&&parent[i])both.push(i);else if(parent[i])extra.push(i);else if(ok)lost.push(i);});
    return {fine,parent,both,extra,lost,fineCount:fine.filter(Boolean).length,parentCount:parent.filter(Boolean).length,
      same:!extra.length&&!lost.length};
  }
  function component(p,family){
    const nodes=p.labels.flatMap((k,i)=>Math.abs(k)===family?[i]:[]);
    const nodeSet=new Set(nodes),remaining=p.edges.filter(([a,b])=>nodeSet.has(a)&&nodeSet.has(b));
    // Spanning edges first: the reveal visibly joins one new port at a time.
    const reached=new Set([nodes[0]]),edges=[];
    while(reached.size<nodes.length){
      const index=remaining.findIndex(([a,b])=>reached.has(a)!==reached.has(b));
      if(index<0)throw new Error('Exported family is disconnected');
      const [edge]=remaining.splice(index,1);edges.push(edge);edge.forEach(x=>reached.add(x));
    }
    return {nodes,edges:edges.concat(remaining)};
  }
  function freedom(nodes,edges){
    const parent=new Map(nodes.map(x=>[x,x]));
    const find=x=>parent.get(x)===x?x:find(parent.get(x));
    for(const [a,b] of edges)parent.set(find(a),find(b));
    return new Set(nodes.map(find)).size;
  }
  const api={defaults,value,evaluate,component,freedom};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.ChairRuleModel=api;
})(typeof globalThis!=='undefined'?globalThis:this);

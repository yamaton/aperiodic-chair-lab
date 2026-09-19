/* Derive each four-panel word from the actual exposed eight-child boundary. */
(function(root){
  'use strict';
  function create(E,rules){
    const {I,add,sub,mul,dot,cross,act,eq,transpose}=E;
    const faces=rules.placedFaces({t:[0,0,0],r:I});
    const boundary=rules.exposed(rules.group);
    const patches=faces.map(f=>boundary.filter(b=>eq(b.n,f.n)&&
      dot(sub(b.c,mul(f.c,2)),f.n)===0&&sub(b.c,mul(f.c,2)).every(x=>Math.abs(x)<=1)));
    if(patches.some(p=>p.length!==4))throw new Error('Parent panels must partition into fours');
    function faceFor(panel,parent){
      const r=transpose(parent.r),c=act(r,sub(panel.c,mul(parent.t,2))),n=act(r,panel.n);
      return patches.findIndex(p=>p.some(f=>eq(f.c,c)&&eq(f.n,n)));
    }
    function compare(id,motif,turn){
      const a=faces[id],b=faces.find(f=>f.motif===motif),v=cross(a.n,a.u);
      const u=[a.u,v,mul(a.u,-1),mul(v,-1)][((turn%4)+4)%4];
      const r=E.rotations.find(r=>eq(act(r,b.n),mul(a.n,-1))&&eq(act(r,b.u),u));
      const shift=sub(mul(a.c,2),act(r,mul(b.c,2)));
      const moved=patches[b.id].map(f=>({...f,c:add(act(r,f.c),shift),n:act(r,f.n),u:act(r,f.u)}));
      const project=f=>{
        const d=sub(f.c,mul(a.c,2));
        return {motif:f.motif,x:dot(d,a.u),y:dot(d,v),u:[dot(f.u,a.u),dot(f.u,v)]};
      };
      const pairs=patches[id].map(f=>{
        const g=moved.find(g=>eq(g.c,f.c));
        return {a:project(f),b:project(g),...rules.handshake(f,g)};
      }).sort((p,q)=>q.a.y-p.a.y||p.a.x-q.a.x);
      const parent=rules.handshake(a,{...b,n:mul(a.n,-1),u});
      return {pairs,parent,a:{motif:a.motif,u:[1,0]},b:{motif,u:[dot(u,a.u),dot(u,v)]}};
    }
    return {faces,patches,faceFor,compare};
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={create};
  else root.ChairParentRules={create};
})(typeof globalThis!=='undefined'?globalThis:this);

const assert=require('node:assert/strict');
const root=process.cwd(),D=require(root+'/docs/assembly/rule-data.json'),M=require(root+'/docs/assembly/rule-model.js'),F=require(root+'/strong/audit/frozen_v1/candidate.json');
const rot=(r,v)=>[0,1,2].map(i=>r[3*i]*v[0]+r[3*i+1]*v[1]+r[3*i+2]*v[2]);
const add=(a,b)=>a.map((x,i)=>x+b[i]),mul=(a,k)=>a.map(x=>x*k),key=a=>a.join(','),same=(a,b)=>key(a)===key(b);
const centers=F.coarse_cubes.map(c=>c.map(x=>2*x+1));const rotations=[...new Map(D.poses.map(p=>[key(p.rotation),p.rotation])).values()];assert.equal(rotations.length,24);
const actual=new Set();for(const r of rotations)for(let x=-3;x<=3;x++)for(let y=-3;y<=3;y++)for(let z=-3;z<=3;z++){
 const t=[x,y,z],other=centers.map(c=>add(rot(r,c),mul(t,2)));
 if(other.some(c=>centers.some(d=>same(c,d))))continue;
 if(other.some(c=>centers.some(d=>c.reduce((s,v,i)=>s+Math.abs(v-d[i]),0)===2)))actual.add(key(r)+'/'+key(t));
}
assert.equal(actual.size,1194);assert.deepEqual(new Set(D.poses.map(p=>key(p.rotation)+'/'+key(p.shift))),actual);
const fraction=s=>{const [n,d=1]=String(s).split('/').map(Number);return n*16/d;};
const ports=F.ports.map((p,i)=>({c:p.center.map(fraction),n:p.outward_normal,u:p.u_axis,v:p.v_axis,i}));
const transform=(q,r,t)=>({...q,c:add(rot(r,q.c),t),n:rot(r,q.n),u:rot(r,q.u),v:rot(r,q.v)});
const posePairs=[];
for(const p of D.profiles){const atScale=[];for(const scale of [1,2]){
 let boundary=ports;if(scale===2){const centers=new Map();for(const child of p.children)for(const q of ports){const moved=transform(q,child.r,mul(child.t,16)),k=key(moved.c);if(!centers.has(k))centers.set(k,[]);centers.get(k).push(moved);}
 for(const list of centers.values()){assert(list.length===1||list.length===2);if(list.length===2){assert(same(list[0].n,mul(list[1].n,-1)));assert.equal(p.labels[list[0].i],-p.labels[list[1].i]);}}
 boundary=[...centers.values()].filter(x=>x.length===1).flat();assert.equal(boundary.length,768);}
 const index=new Map(boundary.map(q=>[key(q.c),q]));atScale.push(D.poses.map(pose=>{const pairs=[];for(const q of boundary){const moved=transform(q,pose.rotation,mul(pose.shift,16*scale)),other=index.get(key(moved.c));if(!other||!same(other.n,mul(moved.n,-1)))continue;assert(same(other.u,moved.u)&&same(other.v,moved.v));pairs.push([other.i,q.i]);}assert(pairs.length>0);return pairs;}));}
 posePairs.push(atScale);
 // Check graph nullity by signed propagation, independent of union-find.
 const adj=Array.from({length:192},()=>[]);for(const [a,b] of p.edges){adj[a].push(b);adj[b].push(a);}
 const signs=new Map();let components=0;for(let i=0;i<192;i++){if(signs.has(i))continue;components++;const stack=[i];signs.set(i,1);while(stack.length){const a=stack.pop();for(const b of adj[a]){if(signs.has(b))assert.equal(signs.get(b),-signs.get(a));else{signs.set(b,-signs.get(a));stack.push(b);}}}}
 assert.equal(components,M.defaults(p).length);
}
let seed=81273,checks=0;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
for(let k=0;k<128;k++)for(let i=0;i<3;i++){const p=D.profiles[i],values=M.defaults(p).map(()=>((rand()%5)+1)*((rand()>>>8)&1?1:-1)),result=M.evaluate(p,values);for(let s=0;s<2;s++){const expected=posePairs[i][s].map(pairs=>pairs.every(([a,b])=>Math.sign(p.labels[a])*values[Math.abs(p.labels[a])-1]+Math.sign(p.labels[b])*values[Math.abs(p.labels[b])-1]===0));assert.deepEqual(result[s?'parent':'fine'],expected);checks+=1194;}}
console.log(JSON.stringify({geometric_contact_types:actual.size,random_assignments:384,decisions:checks,graph_signed_propagation:'pass',status:'pass'}));

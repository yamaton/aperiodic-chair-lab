// Independent integer-coordinate replay. No project geometry imports.
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const raw=fs.readFileSync('strong/audit/frozen_v1/candidate.json');
const data=JSON.parse(raw),report=JSON.parse(fs.readFileSync('strong/audit/information_transfer.json'));
assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),report.candidate_sha256);
const add=(a,b)=>a.map((x,i)=>x+b[i]),mul=(a,k)=>a.map(x=>x*k||0),key=a=>a.join(',');
const act=(r,p)=>[0,1,2].map(i=>p.reduce((s,x,j)=>s+r[3*i+j]*x,0));
const det=r=>r[0]*(r[4]*r[8]-r[5]*r[7])-r[1]*(r[3]*r[8]-r[5]*r[6])+r[2]*(r[3]*r[7]-r[4]*r[6]);
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const rotations=[];
for(const axes of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]])for(const a of [-1,1])for(const b of [-1,1])for(const c of [-1,1]){
 const r=[a,b,c].flatMap((s,i)=>[0,1,2].map(j=>j===axes[i]?s:0));if(det(r)===1)rotations.push(r);
}
const frac=s=>{const[n,d=1]=String(s).split('/').map(Number);return n/d;};
const ports=data.ports.map((p,i)=>({i,c:p.center.map(x=>16*frac(x)),n:p.outward_normal,u:p.u_axis,v:p.v_axis}));
const cubes=data.coarse_cubes.map(q=>q.map(x=>2*x+1));
const chi=ports.map(p=>dot(cross(p.u,p.v),p.n));
const assignments=[data.ports.map(p=>p.signed_key),report.two_depth_witness.signed_port_keys,chi];
assert(assignments.every(a=>a.reduce((s,x)=>s+x,0)===0));
assert(assignments[1].every((k,i)=>Math.sign(k)===chi[i]));
const move=(p,r,t)=>({...p,c:add(act(r,p.c),mul(t,16)),n:act(r,p.n),u:act(r,p.u),v:act(r,p.v)});
function assemble(ps,cs,scale){
 const boundary=new Map(),cells=[];
 for(const child of data.children){
  const r=child.matrix.flat(),t=mul(child.center,scale);
  for(const p of ps){const q=move(p,r,t),id=key(q.c);if(boundary.has(id)){
   const old=boundary.get(id);assert(old);assert.deepEqual(old.n,mul(q.n,-1));
   assignments.forEach(keys=>assert.equal(keys[old.i],-keys[q.i]));boundary.set(id,null);
  }else boundary.set(id,q);}
  cells.push(...cs.map(c=>add(act(r,c),mul(t,2))));
 }
 return [[...boundary.values()].filter(Boolean),cells];
}
const [macroPorts,macroCubes]=assemble(ports,cubes,1);
assert.equal(macroPorts.length,768);assert.equal(new Set(macroCubes.map(key)).size,56);
function canonical(pairs){const z=Array.from({length:12},(_,i)=>i),find=i=>z[i]===i?i:find(z[i]);
 for(const [i,j]of pairs)z[find(j)]=find(i);const names=new Map();return z.map((_,i)=>{const r=find(i);if(!names.has(r))names.set(r,names.size);return names.get(r);});}
function census(ps,cs,radius,table){
 const lookup=new Map(ps.map(p=>[key(p.c)+'/'+key(p.n),p])),occupied=new Set(cs.map(key));
 const expected=new Map(table.map(([t,ri,pi])=>[key(t)+'/'+key(report.rotations[ri]),report.predicates[pi].partition]));
 let count=0,matched=[0,0,0],odd=[0,0,0];const good=[];
 for(const r of rotations){const movedPorts=ps.map(p=>move(p,r,[0,0,0])),movedCubes=cs.map(c=>act(r,c));
 const shifts=[];
 if(radius===null){for(const [t,ri]of table)if(key(report.rotations[ri])===key(r))shifts.push(t);}
 else for(let x=-radius;x<=radius;x++)for(let y=-radius;y<=radius;y++)for(let z=-radius;z<=radius;z++)shifts.push([x,y,z]);
 for(const t of shifts){
  if(movedCubes.some(c=>occupied.has(key(add(c,mul(t,2))))))continue;
  const pairs=[];let flags=[true,true,true];
  for(const b of movedPorts){const a=lookup.get(key(add(b.c,mul(t,16)))+'/'+key(mul(b.n,-1)));if(!a)continue;
   assert.deepEqual(a.u,b.u);assert.deepEqual(a.v,b.v);assert.equal(chi[a.i],-chi[b.i]);
   pairs.push([Math.abs(data.ports[a.i].signed_key)-1,Math.abs(data.ports[b.i].signed_key)-1]);
   assignments.forEach((keys,i)=>{flags[i]&&=keys[a.i]+keys[b.i]===0;});
  }
  if(!pairs.length)continue;
  count++;assert.equal(pairs.length%8,0);
  assert.deepEqual(canonical(pairs),expected.get(key(t)+'/'+key(r)));
  assert.equal(flags[0],flags[1],'Two-depth witness changed a contact');
  flags.forEach((ok,i)=>{if(ok){matched[i]++;if(t.some(x=>x%2))odd[i]++;}});
  if(flags[1])good.push([t,r]);
 }}
 assert.equal(count,expected.size);return {count,matched,odd,good};
}
const fine=census(ports,cubes,2,report.fine_contact_predicates);
const macro=census(macroPorts,macroCubes,4,report.macro_contact_predicates);
assert.deepEqual(fine.matched,[44,44,1194]);assert.deepEqual(macro.matched,[44,44,6801]);assert.equal(macro.odd[1],0);
const scaledFine=new Set(fine.good.map(([t,r])=>key(mul(t,2))+'/'+key(r)));
assert(macro.good.every(([t,r])=>scaledFine.has(key(t)+'/'+key(r))));
const [levelTwoPorts,levelTwoCubes]=assemble(macroPorts,macroCubes,2);
assert.equal(levelTwoPorts.length,3072);assert.equal(new Set(levelTwoCubes.map(key)).size,448);
const secondTable=report.macro_contact_predicates.filter(([t])=>t.every(x=>x%2===0)).map(([t,ri,pi])=>[mul(t,2),ri,pi]);
const second=census(levelTwoPorts,levelTwoCubes,null,secondTable);
assert.deepEqual(second.matched,[44,44,1194]);
// An opposite-key cap determines its full orthogonal map; verify that every
// one is proper and its translation integral for this new depth assignment.
let capPairs=0;
for(const a of ports)for(const b of ports)if(assignments[1][a.i]===-assignments[1][b.i]){
 const r=[0,1,2].flatMap(i=>[0,1,2].map(j=>a.u[i]*b.u[j]+a.v[i]*b.v[j]-a.n[i]*b.n[j]));
 assert.equal(det(r),1);assert(add(a.c,mul(act(r,b.c),-1)).every(x=>x%16===0));capPairs++;
}
const result={status:'passed',candidate_sha256:report.candidate_sha256,
 implementation:'Standalone JavaScript raw integer ports, cube centers, and signed-permutation rotations; no project geometry imports.',
 symbolic_contact_predicates_crosschecked:fine.count+macro.count+second.count,
 second_level_aligned_predicates_crosschecked:second.count,
 second_level_children:64,second_level_symbolic_predicates_identical:true,
 fine_contacts:fine.count,macro_contacts:macro.count,two_depth_fine:44,two_depth_macro:44,two_depth_odd_macro:0,
 reference_contact_sets_identical:true,one_gauge_value_contacts:[1194,6801],
 opposite_key_cap_pairs:capPairs,all_cap_maps_proper_and_integral:true,
 scope:'Finite proper-grid symbolic contact census and one two-depth cap-frame witness; not an arbitrary-placement or infinite-tiling proof.'};
fs.writeFileSync('strong/audit/information_transfer_crosscheck.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));

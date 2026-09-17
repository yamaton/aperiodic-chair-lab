// Finite model checks against preserved research evidence; no infinite-tiling claim.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const E=require('./engine.js');
const cert=JSON.parse(fs.readFileSync('strong/audit/motif_grouping_certificate.json'));
const rules=E.create({faces:cert.face_table,group:cert.derived_group});
const base={t:[0,0,0],r:E.I};
assert.equal(E.rotations.length,24);
const candidates=new Map();
for(const face of rules.exposed([base]))for(const c of rules.candidates([base],face.ref,true))
  if(!c.result.overlap.length)candidates.set(E.poseKey(c.p),c);
assert.equal(candidates.size,1194);
const valid=[...candidates.values()].filter(c=>c.result.ok);
const certified=new Set(cert.contact_table.map(c=>E.poseKey({t:c.center,r:c.rotation})));
assert.equal(valid.length,44);
assert.deepEqual(new Set(valid.map(c=>E.poseKey(c.p))),certified);
for(const {p} of valid)for(const r of E.rotations){
  const move=q=>({t:E.add([3,-2,5],E.act(r,q.t)),r:E.product(r,q.r)});
  assert(rules.check([move(base)],move(p)).ok);
}
const n=[0,0,1],u=[1,0,0],around=[[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]];
let handshakes=0;
for(const a of ['A','B','C'])for(const b of ['A','B','C'])for(const v of around){
  const f={n,u,motif:a},g={n:E.mul(n,-1),u:v,motif:b};
  const expected=a==='A'&&b==='A'&&E.eq(v,[0,1,0]) || ((a==='B'&&b==='C')||(a==='C'&&b==='B'))&&E.eq(v,[-1,0,0]);
  assert.equal(rules.handshake(f,g).ok,!!expected);
  assert.equal(rules.handshake(f,g).ok,rules.handshake(g,f).ok);handshakes++;
}
const target=[base];
while(target.length<8){const h=rules.nextHint(target,base);assert(h);assert(rules.check(target,h.p).ok);target.push(h.p);}
assert(rules.parent(target));
assert.equal(new Set(target.flatMap(rules.placedCubes).map(E.key)).size,56);
for(const r of E.rotations){
  const moved=target.map(p=>({t:E.add([7,1,-4],E.act(r,p.t)),r:E.product(r,p.r)}));
  assert(rules.parent(moved));
}
const corrupt=E.clone(target);corrupt[1].r=E.rotations.find(r=>!E.eq(r,corrupt[1].r));assert.equal(rules.parent(corrupt),null);
for(const {p} of valid){
  const second=rules.group.map(c=>({t:E.add(E.mul(p.t,2),E.act(p.r,c.t)),r:E.product(p.r,c.r)}));
  let shared=0;
  for(const c of second){const result=rules.check(target,c);assert.equal(result.overlap.length,0);assert(result.contacts.every(f=>f.ok));shared+=result.contacts.length;}
  assert(shared>0);
}
// Enumerate the complete macro boundary, including odd translations, independently
// of the UI's effective-parent shortcut. Reject incompatible macro interfaces too.
const boundary=rules.exposed(target), boundaryMap=new Map(boundary.map(f=>[E.key(f.c),f]));
const volume=new Set(target.flatMap(rules.placedCubes).map(E.key));
let macroGeometric=0;
const macroValid=new Set();
for(const r of E.rotations){
  const moved=target.map(p=>({t:E.act(r,p.t),r:E.product(r,p.r)}));
  const movedFaces=rules.exposed(moved),movedCubes=moved.flatMap(rules.placedCubes);
  const offsets=new Map();
  for(const a of boundary)for(const b of movedFaces)if(E.eq(a.n,E.mul(b.n,-1))){
    const t=E.mul(E.sub(a.c,b.c),.5);if(t.every(Number.isInteger))offsets.set(E.key(t),t);
  }
  for(const t of offsets.values()){
    const t2=E.mul(t,2);
    if(movedCubes.some(c=>volume.has(E.key(E.add(c,t2)))))continue;
    macroGeometric++;
    const contacts=movedFaces.flatMap(b=>{const a=boundaryMap.get(E.key(E.add(b.c,t2)));return a?[rules.handshake(a,b).ok]:[];});
    if(contacts.length&&contacts.every(Boolean))macroValid.add(E.poseKey({t,r}));
  }
}
assert.equal(macroGeometric,6801);
assert.deepEqual(macroValid,new Set(valid.map(c=>E.poseKey({t:E.mul(c.p.t,2),r:c.p.r}))));
const h=rules.nextHint([base],base),original=E.clone(h.p);
let rotated=original;
for(let i=0;i<4;i++)rotated=rules.rotateAt([base],rotated,h.ref,1);
assert.deepEqual(rotated,original);
const wrong=rules.rotateAt([base],original,h.ref,1);assert(!rules.check([base],wrong).ok);
const multiple=valid.find(c=>c.result.contacts.some(f=>f.a.motif==='A')&&c.result.contacts.length>1);assert(multiple);
const partial=[...candidates.values()].find(c=>c.result.contacts.some(f=>f.ok)&&c.result.contacts.some(f=>!f.ok));
assert(partial&&!partial.result.ok,'A fitting selected panel must not override other failing panels');
const overlap=rules.check([base],base);assert.equal(overlap.overlap.length,7);assert(!overlap.ok);
const history=new E.History({tiles:[base],op:original});
history.commit('接着',{tiles:[base,original],op:null});
history.undo();assert(history.canRedo);history.redo();assert.equal(history.state.tiles.length,2);
history.undo();history.adjust({tiles:[base],op:wrong});assert(!history.canRedo);
history.undo();assert.deepEqual(history.state.op,original);history.redo();assert.deepEqual(history.state.op,wrong);
assert.equal(history.state.tiles.length,1);
const report={status:'pass',geometric_contacts:candidates.size,compatible_contacts:valid.length,
  canonical_handshakes:handshakes,rotation_checks:valid.length*24,group_cubes:56,macrocontact_positive_checks:44,
  macro_geometric_contacts:macroGeometric,macro_compatible_contacts:macroValid.size,
  grouping_rotations:24,whole_interface_rejection:true,history_branching:true};
fs.writeFileSync('docs/assembly_model_verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));

// Raw-coordinate replay of triangular_v1. No project geometry imports.
const fs = require('node:fs'), assert = require('node:assert/strict'), crypto = require('node:crypto');
const read = p => JSON.parse(fs.readFileSync(p));
const folder = 'strong/audit/triangular_v1/';
const raw = fs.readFileSync(folder + 'candidate.json'), data = JSON.parse(raw);
const manifest = read(folder + 'manifest.json'), reference = read('strong/audit/frozen_v1/candidate.json');
const digest = crypto.createHash('sha256').update(raw).digest('hex');
assert.equal(digest, manifest.candidate_sha256);
const baselineDigest = crypto.createHash('sha256').update(fs.readFileSync('strong/audit/frozen_v1/candidate.json')).digest('hex');
assert.equal(baselineDigest, manifest.reference_candidate_sha256);
assert.deepEqual(data.port_profile.normalized_vertices, [[-1,-1],[1,-1],[-1,0]]);
assert.deepEqual(data.port_profile.barycentric_coordinates, ['(u+1)/2','v+1','-(u+2*v+1)/2']);
assert.equal(data.port_profile.polynomial, '27*lambda0*lambda1*lambda2');
assert.equal(data.half_width, '1/64'); assert.equal(data.height_unit, '1/4096');
const add = (a,b) => a.map((x,i) => x+b[i]), mul = (a,k) => a.map(x => x*k || 0), key = a => a.join(',');
const dot = (a,b) => a.reduce((s,x,i) => s+x*b[i],0);
const act = (r,p) => [0,1,2].map(i => dot(r.slice(3*i,3*i+3),p));
const det = r => r[0]*(r[4]*r[8]-r[5]*r[7])-r[1]*(r[3]*r[8]-r[5]*r[6])+r[2]*(r[3]*r[7]-r[4]*r[6]);
const frac = s => { const [n,d=1] = String(s).split('/').map(Number); return n/d; };
const axisPermutations = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]], rotations = [];
for (const order of axisPermutations) for (const a of [-1,1]) for (const b of [-1,1]) for (const c of [-1,1]) {
  const r = [a,b,c].flatMap((s,i) => [0,1,2].map(j => j===order[i] ? s : 0));
  if (det(r)===1) rotations.push(r);
}
const amplitudes = [1,2,1,1,1,1,1,1,2,1,1,1];
const ports = data.ports.map((p,i) => {
  const old = reference.ports[i];
  for (const field of ['center','outward_normal','u_axis','v_axis']) assert.deepEqual(p[field],old[field]);
  assert.equal(p.reference_signed_key,old.signed_key);
  const chi = det([...p.u_axis,...p.v_axis,...p.outward_normal]);
  assert.equal(p.signed_key,chi*amplitudes[Math.abs(old.signed_key)-1]);
  return {i,c:p.center.map(x => 64*frac(x)),n:p.outward_normal,u:p.u_axis,v:p.v_axis,k:p.signed_key,old:old.signed_key};
});
assert(ports.every(p => p.c.every(Number.isInteger)));
assert.equal(ports.reduce((s,p) => s+p.k,0),0);
const triangle = p => data.port_profile.normalized_vertices.map(([u,v]) => add(p.c,add(mul(p.u,u),mul(p.v,v))));
// Every congruence of complete triangles must induce one of six vertex
// permutations. Only the identity preserves the three distinct edge lengths.
const tri = data.port_profile.normalized_vertices;
const d2 = (a,b) => a.reduce((s,x,i) => s+(x-b[i])**2,0);
const stabilizer = axisPermutations.filter(p => [0,1,2].every(i => [0,1,2].every(j => d2(tri[i],tri[j])===d2(tri[p[i]],tri[p[j]]))));
assert.deepEqual(stabilizer,[[0,1,2]]);
let pairs = 0; const poses = new Set();
for (const a of ports) for (const b of ports) if (a.k===-b.k) {
  const r = [0,1,2].flatMap(i => [0,1,2].map(j => a.u[i]*b.u[j]+a.v[i]*b.v[j]-a.n[i]*b.n[j]));
  const shift = add(a.c,mul(act(r,b.c),-1));
  assert.equal(det(r),1); assert(shift.every(x => x%64===0));
  assert.deepEqual(triangle(b).map(p => add(act(r,p),shift)),triangle(a));
  const fa = add(a.c,mul(add(mul(a.u,3),a.v),-4));
  const fb = add(b.c,mul(add(mul(b.u,3),b.v),-4));
  assert.deepEqual(add(act(r,add(fb,mul(b.n,-32))),shift),add(fa,mul(a.n,32)));
  poses.add(key(r)+'/'+key(shift)); pairs++;
}
assert.equal(pairs,13312); assert.equal(poses.size,1410);
const move = (p,r,t) => ({...p,c:add(act(r,p.c),mul(t,64)),n:act(r,p.n),u:act(r,p.u),v:act(r,p.v)});
const cubes = data.coarse_cubes.map(c => c.map(x => 2*x+1));
assert.deepEqual(data.coarse_cubes,reference.coarse_cubes); assert.deepEqual(data.children,reference.children);
const macroPorts = new Map(), macroCubes = [];
for (const child of data.children) {
  const r = child.matrix.flat(), t = child.center;
  for (const p of ports) {
    const q = move(p,r,t), id = key(q.c);
    if (macroPorts.has(id)) {
      const other = macroPorts.get(id); assert(other);
      assert.equal(other.k,-q.k); assert.deepEqual(other.n,mul(q.n,-1));
      assert.deepEqual(triangle(other),triangle(q)); macroPorts.set(id,null);
    } else macroPorts.set(id,q);
  }
  macroCubes.push(...cubes.map(c => add(act(r,c),mul(t,2))));
}
const boundary = [...macroPorts.values()].filter(Boolean);
assert.equal(boundary.length,768); assert.equal(new Set(macroCubes.map(key)).size,56);
function census(ps,cs,radius) {
  const lookup = new Map(ps.map(p => [key(p.c)+'/'+key(p.n),p])), occupied = new Set(cs.map(key));
  const fits = new Set(); let geometric = 0;
  for (const r of rotations) {
    const qs = ps.map(p => move(p,r,[0,0,0])), movedCells = cs.map(c => act(r,c));
    for (let x=-radius;x<=radius;x++) for (let y=-radius;y<=radius;y++) for (let z=-radius;z<=radius;z++) {
      const t=[x,y,z], t64=mul(t,64);
      if (movedCells.some(c => occupied.has(key(add(c,mul(t,2)))))) continue;
      let touches=0, ok=true, oldOk=true;
      for (const b of qs) {
        const a=lookup.get(key(add(b.c,t64))+'/'+key(mul(b.n,-1)));
        if (!a) continue;
        touches++;
        assert.deepEqual(triangle(a),triangle(b).map(p => add(p,t64)));
        ok &&= a.k===-b.k; oldOk &&= a.old===-b.old;
      }
      if (!touches) continue;
      assert.equal(touches%8,0); geometric++;
      assert.equal(ok,oldOk,'Changed whole-interface predicate');
      if (ok) fits.add(key(t)+'/'+key(r));
    }
  }
  return {geometric,fits};
}
const fine=census(ports,cubes,2), macro=census(boundary,macroCubes,4);
assert.equal(fine.geometric,1194); assert.equal(macro.geometric,6801);
assert.equal(fine.fits.size,44); assert.equal(macro.fits.size,44);
const doubled=new Set([...fine.fits].map(q => {const [t,r]=q.split('/');return key(mul(t.split(',').map(Number),2))+'/'+r;}));
assert.deepEqual(macro.fits,doubled);
// Tutorial transfer checks: the A/B/C panel table and faithful orientation
// encoding are stronger assertions than comparing whole-chair counts alone.
const panels = new Map();
for (const p of ports) {
  const f = add(p.c,mul(add(mul(p.u,3),p.v),-4)), id = key(f)+'/'+key(p.n);
  if (!panels.has(id)) panels.set(id,{f,n:p.n,ps:[]});
  panels.get(id).ps.push(p);
}
let panelComparisons=0, panelFits=0;
for (const r of rotations) for (const a of panels.values()) for (const b of panels.values()) {
  if (key(act(r,b.n))!==key(mul(a.n,-1))) continue;
  const shift=add(a.f,mul(act(r,b.f),-1)); assert(shift.every(x => x%64===0));
  const target=new Map(a.ps.map(p => [key(p.c),p])); let ok=true,oldOk=true;
  for (const p of b.ps) {
    const q=move(p,r,mul(shift,1/64)), match=target.get(key(q.c)); assert(match);
    assert.deepEqual(triangle(match),triangle(q));
    ok &&= match.k===-q.k; oldOk &&= match.old===-q.old;
  }
  assert.equal(ok,oldOk); panelComparisons++; if (ok) panelFits++;
}
assert.equal(panelComparisons,2304);
const allFrames=rotations.flatMap(r => [r,mul(r,-1)]), cellSet=new Set(cubes.map(key));
const portLookup=new Map(ports.map(p => [key(p.c)+'/'+key(p.n),p]));
const selfSymmetries=allFrames.filter(r => cubes.every(c => cellSet.has(key(act(r,c)))) && ports.every(p => {
  const q=move(p,r,[0,0,0]), match=portLookup.get(key(q.c)+'/'+key(q.n));
  return match && match.k===q.k && key(match.u)===key(q.u) && key(match.v)===key(q.v);
}));
assert.deepEqual(selfSymmetries,[[1,0,0,0,1,0,0,0,1]]);
const result={status:'passed',triangular_candidate_sha256:digest,reference_candidate_sha256:baselineDigest,
  implementation:'Standalone integer-coordinate JavaScript, no project geometry imports.',
  triangle_stabilizer:stabilizer,opposite_key_triangle_pairs:pairs,distinct_frame_locked_poses:poses.size,
  fine_geometric_contacts:fine.geometric,full_macro_geometric_contacts:macro.geometric,
  fine_fitting_contacts:fine.fits.size,full_macro_fitting_contacts:macro.fits.size,
  exact_reference_contact_sets_preserved:true,odd_macro_fitting_contacts:0,
  aligned_panel_comparisons:panelComparisons,aligned_panel_fits:panelFits,exact_reference_panel_rules_preserved:true,
  signed_frames_checked_for_self_symmetry:allFrames.length,self_symmetries:selfSymmetries,
  scope:'Independent finite frame/triangle/contact replay; universal open-patch rigidity remains a written polynomial argument.'};
fs.writeFileSync('strong/audit/triangular_ports_crosscheck.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));

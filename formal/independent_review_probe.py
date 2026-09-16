"""Fresh review probe: no imports from repository implementation modules."""
import json, re
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

ROOT = Path.cwd()
d = json.loads((ROOT/'strong/audit/frozen_v1/candidate.json').read_text())
add = lambda a,b: tuple(x+y for x,y in zip(a,b))
sub = lambda a,b: tuple(x-y for x,y in zip(a,b))
mul = lambda k,a: tuple(k*x for x in a)
normals = [tuple(s if i==j else 0 for i in range(3)) for j in range(3) for s in (-1,1)]
corners = list(product((0,1), repeat=3))
def apply(r,p): return tuple(sum(x*y for x,y in zip(row,p)) for row in r)
def cells_move(cells,r,t):
    out=[]
    for q in cells:
        verts=[add(apply(r,add(q,v)),t) for v in corners]
        out.append(tuple(min(v[i] for v in verts) for i in range(3)))
    return out
def boundary(cells):
    return {(add(add(mul(2,q),(1,1,1)),n),n) for q in cells for n in normals if add(q,n) not in cells}
cells=set(map(tuple,d['coarse_cubes']))
faces={f:{} for f in boundary(cells)}
for p in d['ports']:
    pos=tuple(map(Fraction,p['center'])); n=tuple(p['outward_normal'])
    matches=[]
    for f,fn in faces:
        delta=sub(pos,tuple(Fraction(x,2) for x in f))
        if fn==n and all(delta[i]==0 if n[i] else abs(delta[i])<Fraction(1,2) for i in range(3)):
            matches.append((f,fn))
    assert len(matches)==1
    p16=mul(16,pos); assert all(v.denominator==1 for v in p16)
    p16=tuple(map(int,p16)); f=matches[0]
    assert p16 not in faces[f]
    faces[f][p16]=(p['signed_key'],tuple(p['u_axis']),tuple(p['v_axis']))
assert len(faces)==24 and all(len(ps)==8 for ps in faces.values())
def transform(s,r,t):
    cs,fs=s
    return set(cells_move(cs,r,t)), {(add(apply(r,f),mul(2,t)),apply(r,n)):
        {add(apply(r,p),mul(16,t)):(k,apply(r,u),apply(r,v)) for p,(k,u,v) in ps.items()}
        for (f,n),ps in fs.items()}
def match(a,b,t):
    return a=={add(p,mul(16,t)):(-k,u,v) for p,(k,u,v) in b.items()}
fine=(cells,faces); mc=set(); mf={}; cancelled=0
for child in d['children']:
    cs,fs=transform(fine,child['matrix'],tuple(child['center']))
    assert mc.isdisjoint(cs); mc |= cs
    for (f,n),ps in fs.items():
        opp=(f,mul(-1,n))
        if opp in mf:
            assert match(mf.pop(opp),ps,(0,0,0)); cancelled+=1
        else:
            assert (f,n) not in mf; mf[f,n]=ps
assert len(mc)==56 and len(mf)==96 and set(mf)==boundary(mc)
assert mc=={add(mul(2,q),b) for q in cells for b in corners}
macro=(mc,mf)
# Independently decode the simple literal cache and compare complete records.
text=(ROOT/'formal/Chair/Cache.lean').read_text()
for name,solid in [('Fine',fine),('Macro',macro)]:
    block=text.split(f'def cached{name} : Solid := ⟨[',1)[1].split('\n\n',1)[0]
    cs,fs=block.split('], [',1)
    ns=list(map(int,re.findall(r'-?\d+',cs)))
    cachecells={tuple(ns[i:i+3]) for i in range(0,len(ns),3)}
    cachefaces={}
    for line in fs.strip().splitlines():
        ns=list(map(int,re.findall(r'-?\d+',line)))
        assert len(ns)==86
        cachefaces[tuple(ns[:3]),tuple(ns[3:6])]={tuple(ns[i:i+3]):(ns[i+3],tuple(ns[i+4:i+7]),tuple(ns[i+7:i+10])) for i in range(6,86,10)}
    assert (cachecells,cachefaces)==solid
def det(r):
    return sum((1 if (p in [(0,1,2),(1,2,0),(2,0,1)]) else -1)*r[0][p[0]]*r[1][p[1]]*r[2][p[2]] for p in permutations(range(3)))
rots=[]
for perm in permutations(range(3)):
    for signs in product((-1,1),repeat=3):
        r=tuple(tuple(signs[i] if j==perm[i] else 0 for j in range(3)) for i in range(3))
        if det(r)==1: rots.append(r)
assert len(set(rots))==24
summary=json.loads((ROOT/'formal/certificate_summary.json').read_text())
rows={tuple(map(tuple,row['matrix'])):row for row in summary['orientations']}
assert set(rows)==set(rots)
totals=[0,0]; geometric=[0,0]; touching=[0,0]
for r in rots:
    results=[]
    for scale,s in enumerate((fine,macro)):
        cs,fs=s; ds,gs=transform(s,r,(0,0,0))
        # Candidate shifts from adjacent occupied cubes; no face-center enumeration.
        shifts={sub(add(q,n),b) for q in cs for n in normals for b in ds}
        accepted=set()
        for t in shifts:
            overlap=not cs.isdisjoint({add(b,t) for b in ds})
            interfaces=[(fs[opp],ps) for (f,n),ps in gs.items() if (opp:=(add(f,mul(2,t)),mul(-1,n))) in fs]
            if not interfaces: continue
            touching[scale]+=1
            if overlap: continue
            geometric[scale]+=1
            if all(match(a,b,t) for a,b in interfaces): accepted.add(t)
        assert accepted==set(map(tuple,rows[r]['fine_accepted' if scale==0 else 'macro_accepted']))
        totals[scale]+=len(accepted); results.append(accepted)
    assert results[1]=={mul(2,t) for t in results[0]}
print(json.dumps(dict(status='passed',orientations=len(rots),fine_faces=len(faces),macro_faces=len(mf),cancelled_child_interfaces=cancelled,touching_offsets=touching,disjoint_geometric_contacts=geometric,accepted=totals,cache_geometry='exact match by all complete records',method='face containment; transformed cube corners; child boundary cancellation; adjacency-derived shifts'),indent=2))

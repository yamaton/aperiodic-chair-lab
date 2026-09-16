import json
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations, product, combinations
import verify_from_coordinates as audit
D=json.loads((Path(__file__).resolve().parent/'frozen_v1/candidate.json').read_text())
I=(1,0,0,0,1,0,0,0,1)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def mul(r,p): return tuple(sum(r[3*i+j]*p[j] for j in range(3)) for i in range(3))
def mm(r,s): return tuple(sum(r[3*i+k]*s[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
def tr(r): return tuple(r[3*j+i] for i in range(3) for j in range(3))
def sc(s,p): return tuple(s*x for x in p)
R=[]
for perm in permutations(range(3)):
    parity=(-1)**sum(perm[i]>perm[j] for i,j in combinations(range(3),2))
    for signs in product((-1,1),repeat=3):
        if parity*signs[0]*signs[1]*signs[2]==1:
            R.append(tuple(signs[i] if j==perm[i] else 0 for i in range(3) for j in range(3)))
N=[tuple(sign if i==j else 0 for i in range(3)) for j in range(3) for sign in (-1,1)]
base=frozenset(map(tuple,D['coarse_cubes']))
ports={}
for p in D['ports']:
    c=tuple(int(16*F(x)) for x in p['center']); n=tuple(p['outward_normal']); u=tuple(p['u_axis']); v=tuple(p['v_axis'])
    f=sub(c,add(sc(3,u),v))
    owner=tuple((f[i]-8*n[i]-8)//16 for i in range(3))
    assert owner in base and add(owner,n) not in base
    ports.setdefault((owner,n),set()).add((c,p['signed_key'],u,v))
def turn(c,r): return tuple((x-1)//2 for x in mul(r,tuple(2*a+1 for a in c)))
def transform(cells,features,r,t):
    return (frozenset(add(turn(c,r),t) for c in cells),
            {(add(turn(c,r),t),mul(r,n)):frozenset((add(mul(r,p),sc(16,t)),k,mul(r,u),mul(r,v)) for p,k,u,v in fs) for (c,n),fs in features.items()})
def opposite(fs): return frozenset((p,-k,u,v) for p,k,u,v in fs)
def cat(cells,features):
    result={}; shapes={}
    for r in R:
        oc,of=transform(cells,features,r,(0,0,0)); shapes[r]=(oc,of)
        # Any face neighbor must align a cube to one of these adjacent cells;
        # no bounding-box range appears anywhere in this enumeration.
        offsets={sub(add(a,n),b) for a,n in features for b in oc}
        for t in offsets:
            bc=frozenset(add(b,t) for b in oc)
            if cells & bc: continue
            shared={(a,n) for a,n in features if add(a,n) in bc}
            if not shared: continue
            legal=True
            for a,n in shared:
                remote=(sub(add(a,n),t),neg(n))
                rhs=frozenset((add(p,sc(16,t)),-k,u,v) for p,k,u,v in of[remote])
                if features[a,n]!=rhs: legal=False; break
            result[t,r]=(frozenset(shared),legal)
    return result,shapes
ports={key:frozenset(value) for key,value in ports.items()}
C,shapes=cat(base,ports)
original,oriented=audit.contact_catalogue(audit.from_data(D),audit.rotation_group())
assert set(C)==set(original)
assert all(legal==original[p][1] for p,(_,legal) in C.items())
legal=sorted(p for p,(_,ok) in C.items() if ok)
print('Independent adjacency catalogue equals audit:',len(C),'geometric;',len(legal),'legal',flush=True)

def placed(p):
    t,r=p; return transform(base,ports,r,t)
placed_cache={p:placed(p) for p in legal}
def direct_bad(a,b):
    ac,af=placed_cache.get(a) or placed(a); bc,bf=placed_cache.get(b) or placed(b)
    if ac&bc: return True
    for c,n in af:
        d=add(c,n)
        if d in bc and af[c,n]!=opposite(bf[d,neg(n)]): return True
    return False
conflicts={p:{q for q in legal if p!=q and direct_bad(p,q)} for p in legal}
faces=frozenset(ports)
stars=[]
def dfs(remaining,eligible,chosen):
    if not remaining: stars.append(frozenset(chosen)); return
    face=min(remaining)
    for p in sorted(eligible):
        cover=C[p][0]
        if face in cover and cover<=remaining:
            dfs(remaining-cover,eligible-{p}-conflicts[p],chosen+[p])
dfs(faces,set(legal),[])
audit_candidates,audit_stars,_=audit.all_stars(original,oriented)
expected={frozenset(audit_candidates[i] for i in s) for s in audit_stars}
assert len(stars)==len(set(stars)) and set(stars)==expected
print('Independent first-face exact cover equals audit:',len(stars),'stars',flush=True)
children=[(tuple(c['center']),tuple(x for row in c['matrix'] for x in row)) for c in D['children']]
# Independently build macro boundary by collecting every child's patches and
# retaining precisely faces with no owning coarse cube on the other side.
macro=set(); all_ports={}
for t,r in children:
    cs,fs=transform(base,ports,r,t)
    assert not macro&cs; macro.update(cs)
    assert not all_ports.keys()&fs.keys(); all_ports.update(fs)
macro_ports={f:fs for f,fs in all_ports.items() if add(*f) not in macro}
for (c,n),fs in all_ports.items():
    d=add(c,n)
    if d in macro: assert fs==opposite(all_ports[d,neg(n)])
macro=frozenset(macro)
M,_=cat(macro,macro_ports)
original_macro=audit.assemble(children,audit.from_data(D),oriented)
auditM,_=audit.contact_catalogue(original_macro,audit.rotation_group())
expectedM={p for p,(_,ok) in auditM.items() if ok}
assert {p for p,(_,ok) in M.items() if ok}==expectedM
assert len(M)==6801
print('Independent macro catalogue:',len(M),'geometric;',len(expectedM),'legal; exact allowed placements equal audit',flush=True)
# Recheck every claimed forcing implication and group incompatibility using
# independent actual occupied cells and face ports.
anchor=((0,0,0),I)
def relative(a,b):
    ta,ra=a; tb,rb=b
    return mul(tr(ra),sub(tb,ta)),mm(tr(ra),rb)
groups=[frozenset(relative(role,c) for c in children) for role in children]
neighborhoods=[s|{anchor} for s in stars]
central=[groups[0]<=s for s in neighborhoods]
for s in neighborhoods:
    if groups[0]<=s: continue
    found=False
    for neighbor in s-{anchor}:
        required={relative(neighbor,p) for p in s-{neighbor} if relative(neighbor,p) in C}
        opts=[o for o in neighborhoods if required<=o]
        if opts and relative(neighbor,anchor) in groups[0] and all(groups[0]<=o for o in opts):
            found=True; break
    assert found
for g,h in combinations(groups,2):
    assert any(direct_bad(a,b) for a,b in combinations(g|h,2))
print('Independent neighborhood forcing and all 28 group incompatibilities passed',flush=True)
# Three-level expansion, followed by direct occupancy and port checks.
patch=[anchor]
for level in range(1,4):
    patch=[(add(sc(2,t),mul(r,c)),mm(r,s)) for t,r in patch for c,s in children]
    occupied={}; fs={}
    for i,(t,r) in enumerate(patch):
        cs,pfs=transform(base,ports,r,t)
        assert not occupied.keys()&cs
        occupied.update(dict.fromkeys(cs,i)); fs.update(pfs)
    expectedcells={add(sc(2**level,q),bits) for q in base for bits in product(range(2**level),repeat=3)}
    assert occupied.keys()==expectedcells
    matches=0
    for (c,n),features in fs.items():
        d=add(c,n)
        if d in occupied:
            assert features==opposite(fs[d,neg(n)])
            matches+=1
    print('Direct substitution level',level,':',len(patch),'tiles,',len(occupied),'cubes,',matches//2,'matching internal unit faces',flush=True)
assert set(M)==set(auditM)
assert all(ok==auditM[p][1] for p,(_,ok) in M.items())
assert {((t[0]//2,t[1]//2,t[2]//2),r) for t,r in expectedM if all(x%2==0 for x in t)}==set(legal)
assert all(all(x%2==0 for x in t) for t,r in expectedM)
print('All macro placements and fit flags match audit; all offsets even and deflated legal set equals fine legal set',flush=True)

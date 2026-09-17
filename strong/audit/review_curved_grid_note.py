from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from collections import defaultdict
import hashlib, json
import sympy as S
raw=Path('strong/audit/frozen_v1/candidate.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54'
d=json.loads(raw)
cells=set(map(tuple,d['coarse_cubes']))
assert cells==set(product((-1,0),repeat=3))-{(0,0,0)}
w,delta=F(d['half_width']),F(d['height_unit'])
assert (w,delta)==(F(1,64),F(1,4096))
assert {k:F(d['cap_polynomial'][k]) for k in ('a','b')}=={'a':F(1,5),'b':F(1,7)}
h=F(141,35840); rho=F(1,64)
assert h==12*delta*F(47,35) and h<rho and 3*rho*rho<F(1,16) and 12*(1+h)**2<16
axes=[tuple(s*int(i==j) for i in range(3)) for j in range(3) for s in (-1,1)]
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
scale=lambda c,a:tuple(c*x for x in a)
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
mat=lambda r,a:tuple(dot(row,a) for row in r)
det=lambda r:r[0][0]*(r[1][1]*r[2][2]-r[1][2]*r[2][1])-r[0][1]*(r[1][0]*r[2][2]-r[1][2]*r[2][0])+r[0][2]*(r[1][0]*r[2][1]-r[1][1]*r[2][0])
exposed={(add(q,tuple(F(1+n[i],2) for i in range(3))),n):q for q in cells for n in axes if add(q,n) not in cells}
assert len(exposed)==24
faces=defaultdict(list); chirality=defaultdict(set); ports=[]; margins=[]
for p in d['ports']:
    c=tuple(map(F,p['center'])); u,v,n=(tuple(p[name]) for name in ('u_axis','v_axis','outward_normal')); k=p['signed_key']
    assert all(a in axes for a in (u,v,n)) and dot(u,v)==dot(u,n)==dot(v,n)==0 and 1<=abs(k)<=12
    f=tuple(c[i]-F(3*u[i]+v[i],16) for i in range(3)); q=exposed[(f,n)]
    margins.extend(F(1,2)-abs(c[i]-f[i])-w for i in range(3) if not n[i])
    faces[f,n].append(c); chirality[k].add(det((u,v,n)))
    ports.append((c,u,v,n,k,f,q))
assert len(ports)==192 and set(faces)==set(exposed) and all(len(set(v))==8 for v in faces.values()) and min(margins)==F(19,64)
assert all(len(cs)==1 and cs=={-next(iter(chirality[-k]))} for k,cs in chirality.items())
assert all(any(abs(a[0][i]-b[0][i])>(h if a[3][i] else w)+(h if b[3][i] else w) for i in range(3)) for a,b in combinations(ports,2))
poses=set(); count=0
for a,b in product(ports,repeat=2):
    if a[4]!=-b[4]: continue
    r=tuple(tuple(a[1][i]*b[1][j]+a[2][i]*b[2][j]-a[3][i]*b[3][j] for j in range(3)) for i in range(3))
    t=add(a[0],scale(-1,mat(r,b[0])))
    assert det(r)==1 and all(x.denominator==1 for x in t)
    image_corners=[add(t,mat(r,add(b[6],e))) for e in product((0,1),repeat=3)]
    assert tuple(min(v[i] for v in image_corners) for i in range(3))==add(a[6],a[3])
    poses.add((r,t)); count+=1
assert count==1536 and len(poses)==86
u,v,x,y,t,a,b=S.symbols('u v x y t a b')
phi=(1-u*u)*(1-v*v)*(1+u/5+v/7)
line=S.Poly(phi.subs({u:x+a*t,v:y+b*t}),t)
assert S.factor(line.nth(5)-a*a*b*b*(a/5+b/7))==0
assert S.factor(line.nth(3).subs(a,0))==b**3*(x-1)*(x+1)/7
assert S.factor(line.nth(3).subs(b,0))==a**3*(y-1)*(y+1)/5
assert S.factor(line.nth(4).subs(b,-7*a/5)-S.Rational(49,25)*a**4*(1+x/5+y/7))==0
stabilizers=[]
for swap,s,r in product((False,True),(-1,1),(-1,1)):
    uu,vv=(s*v,r*u) if swap else (s*u,r*v)
    if S.expand(uu/5+vv/7-u/5-v/7)==0: stabilizers.append((swap,s,r))
assert stabilizers==[(False,1,1)]
print('PASS: frozen hash, carrier cells, all 192 faces/frames/keys, separation, 1536 proper integral adjacent-owner matches, 86 poses, four line-coefficient identities, trivial D4 fifth-line stabilizer, retention and diameter bounds.')

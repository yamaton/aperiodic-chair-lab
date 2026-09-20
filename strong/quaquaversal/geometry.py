"""Exact Conway–Radin prism geometry in the rational metric diag(3, 1, 1).

Run from the repository root with uv; no binary floating point is used here.
The physical x coordinate is sqrt(3) times the first stored coordinate.
"""

from fractions import Fraction as F
from itertools import combinations, product


def vec(*xs):
    return tuple(F(x) for x in xs)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(k, a):
    return tuple(k * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def transpose(a):
    return tuple(zip(*a))


def mv(a, v):
    return tuple(dot(row, v) for row in a)


def mm(a, b):
    return tuple(tuple(dot(row, col) for col in transpose(b)) for row in a)


def det(a):
    return dot(a[0], cross(a[1], a[2]))


I = (vec(1, 0, 0), vec(0, 1, 0), vec(0, 0, 1))
G = (vec(3, 0, 0), vec(0, 1, 0), vec(0, 0, 1))
GINV = (vec(F(1, 3), 0, 0), vec(0, 1, 0), vec(0, 0, 1))
ZERO = vec(0, 0, 0)
VERTICES = tuple(vec(*p) for p in ((0,0,0), (1,0,0), (0,1,0),
                                 (0,0,1), (1,0,1), (0,1,1)))
FACES = ((0,2,1), (3,4,5), (0,1,4,3), (0,3,5,2), (1,2,5,4))
FACE_NAMES = ("bottom", "top", "long_rectangle", "square", "hypotenuse_rectangle")
EDGES = tuple(sorted({tuple(sorted((f[i], f[(i+1) % len(f)])))
                      for f in FACES for i in range(len(f))}))


def inverse_rotation(r):
    return mm(mm(GINV, transpose(r)), G)


def transform(pose, point):
    r, t, scale = pose
    return add(mul(scale, mv(r, point)), t)


def inverse_point(pose, point):
    r, t, scale = pose
    return mul(1 / scale, mv(inverse_rotation(r), sub(point, t)))


def compose(a, b):
    r, t, s = a
    q, u, h = b
    return mm(r, q), add(t, mul(s, mv(r, u))), s*h


def vertices(pose):
    return tuple(transform(pose, v) for v in VERTICES)


def child_maps():
    """Section II, Figure 1 labels; proper poses fix the prism's handedness.

    The two slabs are z in [0,1/2] and [1/2,1]. In slab A rotate
    children 2,3 by +pi/2 about physical x. In B rotate 3,4 by
    +2pi/3 about z. The unmarked carrier has no proper self-symmetry.
    """
    base = [
        (I, vec(F(1,2), 0, 0), F(1,2)),
        ((vec(-1,0,0), vec(0,1,0), vec(0,0,-1)), vec(F(1,2),0,F(1,2)), F(1,2)),
        ((vec(1,0,0), vec(0,-1,0), vec(0,0,-1)), vec(0,F(1,2),F(1,2)), F(1,2)),
        (I, vec(0,F(1,2),0), F(1,2)),
    ]
    ra = (vec(1,0,0), vec(0,0,-1), vec(0,1,0))
    ca = vec(0,F(1,4),F(1,4))
    aturn = ra, sub(ca, mv(ra, ca)), F(1)
    rb = (vec(F(-1,2),F(-1,2),0), vec(F(3,2),F(-1,2),0), vec(0,0,1))
    cb = vec(F(1,6),F(1,2),0)
    bturn = rb, sub(cb, mv(rb, cb)), F(1)
    lift = I, vec(0,0,F(1,2)), F(1)
    result = []
    for i, p in enumerate(base):
        result.append((f"{i+1}A", compose(aturn, p) if i in (1,2) else p))
    for i, p in enumerate(base):
        result.append((f"{i+1}B", compose(lift, compose(bturn,p) if i in (2,3) else p)))
    return result


def inside(p, strict=False):
    u,y,z = p
    slacks = (u,y,1-u-y,z,1-z)
    return all(a > 0 if strict else a >= 0 for a in slacks)


def face_polygons(pose):
    vs = vertices(pose)
    faces = [tuple(vs[i] for i in f) for f in FACES]
    return [tuple(reversed(f)) for f in faces] if det(pose[0]) < 0 else faces


def plane(poly):
    n = cross(sub(poly[1],poly[0]), sub(poly[2],poly[0]))
    return n, dot(n,poly[0])


def project(poly, drop):
    return [tuple(x for j,x in enumerate(p) if j != drop) for p in poly]


def area2(poly):
    return sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1]))


def clip2(subject, clipper):
    """Convex rational polygon intersection (closed halfplanes)."""
    if area2(clipper) < 0:
        clipper = list(reversed(clipper))
    out = list(subject)
    for a,b in zip(clipper,clipper[1:]+clipper[:1]):
        def side(p):
            return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        current, out = out, []
        if not current:
            break
        for p,q in zip(current,current[1:]+current[:1]):
            sp,sq = side(p),side(q)
            if sp >= 0:
                out.append(p)
            if (sp < 0 < sq) or (sq < 0 < sp):
                out.append(add(p,mul(sp/(sp-sq),sub(q,p))))
        out = list(dict.fromkeys(out))
    return out


def intersection(a, b):
    n,d = plane(a)
    m,e = plane(b)
    if dot(n,m) >= 0 or any(dot(n,p) != d for p in b):
        return ()
    drop = next(j for j in range(3) if n[j])
    poly = clip2(project(a,drop),project(b,drop))
    if len(poly) < 3 or area2(poly) == 0:
        return ()
    result = []
    for p in poly:
        v = list(p)
        v.insert(drop,F(0))
        v[drop] = (d-dot(n,v))/n[drop]
        result.append(tuple(v))
    return tuple(result)


def contacts(poses):
    faces = [face_polygons(p) for p in poses]
    out = []
    for i,j in combinations(range(len(poses)),2):
        for fi,fj in product(range(5),repeat=2):
            poly = intersection(faces[i][fi],faces[j][fj])
            if poly:
                out.append(dict(i=i,j=j,fi=fi,fj=fj,polygon=poly))
    return out


def contacts_fast(poses):
    """The same exact intersections, indexed by unoriented supporting plane."""
    groups = {}
    for i,pose in enumerate(poses):
        for fi,poly in enumerate(face_polygons(pose)):
            n,d = plane(poly)
            pivot = next(x for x in n if x)
            key = tuple(x/pivot for x in n)+(d/pivot,)
            side = int(pivot > 0)
            bounds = tuple((min(p[k] for p in poly),max(p[k] for p in poly)) for k in range(3))
            groups.setdefault(key,[[],[]])[side].append((i,fi,poly,bounds))
    out = []
    for minus,plus in groups.values():
        for a,b in product(minus,plus):
            if a[0] == b[0]:
                continue
            if any(ahi < blo or bhi < alo for (alo,ahi),(blo,bhi) in zip(a[3],b[3])):
                continue
            if a[0] > b[0]:
                a,b = b,a
            poly = intersection(a[2],b[2])
            if poly:
                out.append(dict(i=a[0],j=b[0],fi=a[1],fj=b[1],polygon=poly))
    return sorted(out,key=lambda c:(c['i'],c['j'],c['fi'],c['fj']))


def separating_axis(a,b):
    """Exact SAT certificate: returned covector separates interiors."""
    va,vb = vertices(a),vertices(b)
    axes = [plane(p)[0] for p in face_polygons(a)+face_polygons(b)]
    ea = [sub(va[j],va[i]) for i,j in EDGES]
    eb = [sub(vb[j],vb[i]) for i,j in EDGES]
    axes.extend(cross(u,v) for u in ea for v in eb)
    for n in axes:
        if n == ZERO:
            continue
        ia,ib = [dot(n,p) for p in va],[dot(n,p) for p in vb]
        if max(ia) <= min(ib):
            return n, max(ia), min(ib)
        if max(ib) <= min(ia):
            return mul(-1,n), -min(ia), -max(ib)
    return None


def encode(x):
    if isinstance(x,F):
        return str(x)
    if isinstance(x,dict):
        return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [encode(v) for v in x]
    return x


def patch(level):
    result = [((),(I,ZERO,F(1)))]
    for _ in range(level):
        result = [(address+(name,),compose(pose,child))
                  for address,pose in result for name,child in child_maps()]
    return result

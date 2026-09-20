"""Q009: closed root neighborhoods, including edge/vertex-only neighbors.

Exact separating-axis tests decide closed intersection. Spatial bins use
rational bounding boxes, so their broad phase introduces no rounding rule.
Observed finite-patch neighborhoods are only a lower bound on the language.
"""

import argparse
import hashlib
import json
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path

from geometry import (F,I,ZERO,EDGES,VERTICES,child_maps,compose,vertices,
                      face_polygons,plane,cross,sub,dot,inside,encode)
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def bounds(p):
    vs = vertices(p)
    return tuple((min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3))


def disjoint(a,b):
    return any(hi < lo2 or hi2 < lo for (lo,hi),(lo2,hi2) in zip(a,b))


def bins(box,scale):
    return product(*(range(int(lo//scale),int(hi//scale)+1) for lo,hi in box))


class TouchChecker:
    def __init__(self):
        self.cache = {}
        self.calls = 0

    def touches(self,p,q):
        self.calls += 1
        r,t,s = relative(p,q)
        assert s == 1
        if r not in self.cache:
            rp = r,ZERO,F(1)
            a,b = VERTICES,vertices(rp)
            axes = [plane(poly)[0] for poly in face_polygons((I,ZERO,F(1)))+face_polygons(rp)]
            axes += [cross(sub(a[j],a[i]),sub(b[l],b[k])) for i,j in EDGES for k,l in EDGES]
            unique = {}
            for n in axes:
                if n == ZERO:
                    continue
                pivot = next(x for x in n if x)
                n = tuple(x/pivot for x in n)
                unique[n] = (min(dot(n,v) for v in a),max(dot(n,v) for v in a),
                             min(dot(n,v) for v in b),max(dot(n,v) for v in b))
            self.cache[r] = list(unique.items())
        for n,(alo,ahi,blo,bhi) in self.cache[r]:
            d = dot(n,t)
            if ahi < blo+d or bhi+d < alo:
                return False
        return True


def patch_stars(poses,checker):
    bs = [bounds(p) for p in poses]
    grid = defaultdict(list)
    scale = poses[0][2]
    for i,b in enumerate(bs):
        for cell in bins(b,scale):
            grid[cell].append(i)
    result = []
    for i,p in enumerate(poses):
        # Strictly interior carrier support ensures its closed neighborhood is complete.
        if not all(inside(v,strict=True) for v in vertices(p)):
            continue
        candidates = {j for cell in bins(bs[i],scale) for j in grid[cell] if j != i}
        star = tuple(sorted(relative(p,poses[j]) for j in candidates
                            if not disjoint(bs[i],bs[j]) and checker.touches(p,poses[j])))
        result.append(star)
    return Counter(result)


def periodic_stars(poses,periods,checker):
    bs = [bounds(p) for p in poses]
    overall = tuple((min(b[k][0] for b in bs),max(b[k][1] for b in bs)) for k in range(3))
    radius = [int((hi-lo)//d)+1 for (lo,hi),d in zip(overall,periods)]
    grid = defaultdict(list)
    shifted = []
    scale = poses[0][2]
    for offset in product(*(range(-n,n+1) for n in radius)):
        shift = tuple(a*b for a,b in zip(offset,periods))
        for i,p in enumerate(poses):
            b = tuple((lo+d,hi+d) for (lo,hi),d in zip(bs[i],shift))
            if disjoint(b,overall):
                continue
            q = p[0],tuple(a+d for a,d in zip(p[1],shift)),p[2]
            k = len(shifted)
            shifted.append((q,b))
            for cell in bins(b,scale):
                grid[cell].append(k)
    result = []
    for i,p in enumerate(poses):
        candidates = {j for cell in bins(bs[i],scale) for j in grid[cell]}
        star = tuple(sorted(relative(p,shifted[j][0]) for j in candidates
                            if shifted[j][0] != p and not disjoint(bs[i],shifted[j][1])
                            and checker.touches(p,shifted[j][0])))
        result.append(star)
    return Counter(result),radius


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample-level',type=int,default=3)
    parser.add_argument('--periodic-level',type=int,default=1)
    args = parser.parse_args()
    children = [p for _,p in child_maps()]
    patch = [(I,ZERO,F(1))]
    for _ in range(args.sample_level):
        patch = [compose(p,q) for p in patch for q in children]
    checker = TouchChecker()
    print(f'closed sample stars: {len(patch)} tiles',flush=True)
    observed = patch_stars(patch,checker)
    print(f'observed {len(observed)} closed stars',flush=True)
    source = ROOT/'artifacts'/'atlas_periodic_reflections.json'
    raw = json.loads(source.read_text())
    periods = tuple(F(x) for x in raw['periods'])
    def normalize(p):
        return p[0],tuple(x%d for x,d in zip(p[1],periods)),p[2]
    periodic = {normalize(raw_pose(p)) for p in raw['poses']}
    for _ in range(args.periodic_level):
        periodic = {normalize(compose(p,q)) for p in periodic for q in children}
    control,radius = periodic_stars(sorted(periodic),periods,checker)
    missing = set(control)-set(observed)
    relative_poses = sorted({p for star in set(observed)|set(control) for p in star})
    pose_id = {p:i for i,p in enumerate(relative_poses)}
    output = dict(scope='Closed root stars from finite samples; missing patterns are unknown, not forbidden',
                  encoding='star lists index the shared exact relative_poses table',relative_poses=relative_poses,
                  arguments=vars(args),observed=[dict(star=[pose_id[p] for p in s],count=n) for s,n in sorted(observed.items())],
                  periodic=[dict(star=[pose_id[p] for p in s],count=n,observed=s in observed) for s,n in sorted(control.items())],
                  periodic_offset_radius=radius,closed_intersection_tests=checker.calls,
                  periodic_control_uses_only_observed_stars=not missing,
                  distinct_observed=len(observed),distinct_periodic=len(control),not_observed=len(missing),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',source,Path(__file__))})
    path = ROOT/'artifacts'/f'closed_stars_{args.sample_level}_{args.periodic_level}.json'
    path.write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('distinct_observed','distinct_periodic','not_observed',
                                          'periodic_control_uses_only_observed_stars')}),flush=True)


if __name__ == '__main__':
    main()

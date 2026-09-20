"""Replay Q009 using edge clipping, independently of separating-axis tests.

A bounded convex intersection has a vertex. Such a vertex is either a
vertex of an input polyhedron or an input edge meeting the other's face.
Clipping every input edge against the other polyhedron therefore detects
nonempty intersection and recovers enough points to determine its dimension.
"""

import hashlib
import json
from collections import Counter
from itertools import combinations,product
from pathlib import Path

from geometry import (F,I,ZERO,VERTICES,EDGES,child_maps,compose,encode,
                      inverse_point,transform,vertices,sub,add,mul,cross,dot)
from contact_atlas import relative
from closed_stars import bounds,disjoint,periodic_stars,TouchChecker
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent
IDENTITY = I,ZERO,F(1)


def clip(a,b):
    def slack(p):
        return p[0],p[1],1-p[0]-p[1],p[2],1-p[2]
    lo,hi = F(0),F(1)
    for s,t in zip(slack(a),slack(b)):
        d = t-s
        if d == 0:
            if s < 0:
                return None
        elif d > 0:
            lo = max(lo,-s/d)
        else:
            hi = min(hi,-s/d)
        if lo > hi:
            return None
    return lo,hi


def edge_points(q,first_only=False):
    result = set()
    # Root edges in q coordinates; endpoints mapped back to root coordinates.
    local = [inverse_point(q,v) for v in VERTICES]
    for i,j in EDGES:
        interval = clip(local[i],local[j])
        if interval is not None:
            for t in interval:
                result.add(add(VERTICES[i],mul(t,sub(VERTICES[j],VERTICES[i]))))
            if first_only:
                return result
    # q edges clipped directly against the root.
    world = vertices(q)
    for i,j in EDGES:
        interval = clip(world[i],world[j])
        if interval is not None:
            for t in interval:
                result.add(add(world[i],mul(t,sub(world[j],world[i]))))
            if first_only:
                return result
    return result


def dimension(points):
    if not points:
        return -1
    p,*rest = sorted(points)
    differences = [sub(q,p) for q in rest if q != p]
    if not differences:
        return 0
    a = differences[0]
    normals = [cross(a,b) for b in differences]
    normals = [n for n in normals if n != ZERO]
    if not normals:
        return 1
    return 2 if all(dot(normals[0],b) == 0 for b in differences) else 3


def main():
    path = ROOT/'artifacts'/'closed_contact_atlas.json'
    raw = json.loads(path.read_text())
    assert raw['status'] == 'closed' and not raw['pending_pose_indices']
    poses = [raw_pose(p['pose']) for p in raw['poses']]
    index = {p:i for i,p in enumerate(poses)}
    assert len(index) == len(poses)
    children = [p for _,p in child_maps()]
    dims = Counter()
    samples = {}
    for i,(p,entry) in enumerate(zip(poses,raw['poses'])):
        origin = entry['origin']
        if origin['kind'] == 'sibling':
            a,b = children[origin['i']],children[origin['j']]
        else:
            assert origin['parent'] < i
            a = children[origin['i']]
            b = compose(poses[origin['parent']],children[origin['j']])
            if origin['reverse']:
                a,b = b,a
        assert relative(a,b) == p
        points = edge_points(p)
        d = dimension(points)
        assert d in (0,1,2),(i,d)
        dims[d] += 1
        samples[i] = sorted(points)
    face_atlas = json.loads((ROOT/'artifacts'/'contact_atlas.json').read_text())
    face_poses = {raw_pose(p['pose']) for p in face_atlas['poses']}
    assert {p for i,p in enumerate(poses) if dimension(samples[i]) == 2} == face_poses
    # Exact closure audit with a different predicate than the producer's SAT.
    cb = [bounds(p) for p in children]
    checked = 0
    for pi,p in enumerate(poses):
        right = [compose(p,q) for q in children]
        rb = [bounds(q) for q in right]
        for i,a in enumerate(children):
            for j,b in enumerate(right):
                if disjoint(cb[i],rb[j]):
                    continue
                rel = relative(a,b)
                checked += 1
                if edge_points(rel,first_only=True):
                    assert rel in index and relative(b,a) in index,(pi,i,j)
        if (pi+1)%250 == 0:
            print(f'closed atlas independently audited: {pi+1}/{len(poses)}',flush=True)
    # Test the original 24-tile control, without assuming its closed pairs match.
    control_path = ROOT/'artifacts'/'atlas_periodic_reflections.json'
    control_raw = json.loads(control_path.read_text())
    controls = [raw_pose(p) for p in control_raw['poses']]
    periods = tuple(F(x) for x in control_raw['periods'])
    stars,radius = periodic_stars(controls,periods,TouchChecker())
    control_pairs = {p for star in stars for p in star}
    rejected = sorted(control_pairs-set(index))
    report = dict(scope='Independent edge-clipping audit of finite closed-contact closure and witnesses',
                  atlas_size=len(poses),dimensions=dict(dims),closure_cross_pairs_tested=checked,
                  intersection_vertices=[dict(atlas_index=i,points=v) for i,v in samples.items()],
                  original_24_tile_control=dict(distinct_stars=len(stars),distinct_pairs=len(control_pairs),
                                               outside_atlas=rejected,checked_offset_radius=radius),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'closed_stars.py',
                                     ROOT/'reflected_controls.py',path,ROOT/'artifacts'/'contact_atlas.json',control_path,Path(__file__))})
    (ROOT/'artifacts'/'closed_contact_audit.json').write_text(json.dumps(encode(report),indent=2)+'\n')
    print(json.dumps(dict(dimensions=dict(dims),checked=checked,original_periodic_pairs_outside=len(rejected))),flush=True)


if __name__ == '__main__':
    main()

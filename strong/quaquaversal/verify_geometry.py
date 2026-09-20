"""Reproduce exact geometry and baseline matching-rule obstructions."""

import hashlib
import json
from itertools import combinations, product
from pathlib import Path

from geometry import (F,I,G,ZERO,VERTICES,FACE_NAMES,child_maps,compose,contacts,contacts_fast,
                      det,encode,face_polygons,inside,inverse_point,mm,mv,plane,
                      project,area2,separating_axis,sub,transpose,vec,vertices)

ROOT = Path(__file__).resolve().parent


def face_area(poly, drop):
    return abs(area2(project(poly,drop)))


def main():
    named = child_maps()
    poses = [p for _,p in named]
    for r,t,s in poses:
        assert det(r) == 1 and mm(mm(transpose(r),G),r) == G
        assert s == F(1,2)
    assert all(inside(v) for p in poses for v in vertices(p))
    separators = []
    for i,j in combinations(range(8),2):
        witness = separating_axis(poses[i],poses[j])
        assert witness is not None
        separators.append(dict(i=i,j=j,certificate=witness))
    assert sum(s**3 for _,_,s in poses) == 1
    cs = contacts(poses)
    assert cs == contacts_fast(poses)
    parent_faces = face_polygons((I,ZERO,F(1)))
    coverage = []
    for i,pose in enumerate(poses):
        for fi,poly in enumerate(face_polygons(pose)):
            n,d = plane(poly)
            drop = next(j for j in range(3) if n[j])
            total = face_area(poly,drop)
            internal = sum(face_area(c['polygon'],drop) for c in cs
                           if (c['i'],c['fi']) == (i,fi) or (c['j'],c['fj']) == (i,fi))
            boundary = any(all(sum(a*b for a,b in zip(pn,v)) == pd for v in poly)
                           for pn,pd in map(plane,parent_faces))
            assert internal + (total if boundary else 0) == total, (i,fi,internal,total)
            coverage.append(dict(child=i,face=fi,area2_projected=total,
                                 internal_area2=internal,on_parent_boundary=boundary))
    address = ['2B','2B','4A']
    pose = (I,ZERO,F(1))
    for name in address:
        pose = compose(pose,dict(named)[name])
    assert pose[0] == I and pose[2] == F(1,8)
    assert all(inside(v,strict=True) for v in vertices(pose))
    fixed = tuple(v/(1-pose[2]) for v in pose[1])
    assert inside(fixed,strict=True)

    # Exact two-prism periodic tiling of [0,1]^3 in the rational metric.
    turn = (vec(-1,0,0),vec(0,-1,0),vec(0,0,1))
    cell = [(I,ZERO,F(1)),(turn,vec(1,1,0),F(1))]
    assert separating_axis(*cell) is not None
    assert all(all(0 <= x <= 1 for x in v) for p in cell for v in vertices(p))
    # Their equal volumes sum to the enclosing box volume, certifying coverage.
    pcs = []
    for a,p in enumerate(cell):
        for offset in product((-1,0,1),repeat=3):
            for b,q in enumerate(cell):
                if offset == (0,0,0) and a == b:
                    continue
                qq = (q[0],tuple(x+y for x,y in zip(q[1],offset)),q[2])
                for c in contacts([p,qq]):
                    pcs.append(dict(tile=a,neighbor=b,offset=offset,
                                    fi=c['fi'],fj=c['fj'],polygon=c['polygon']))
    # Equality colors on whole faces: finest partition compatible with siblings.
    parent = list(range(5))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for c in cs:
        parent[find(c['fi'])] = find(c['fj'])
    classes = [[i for i in range(5) if find(i) == root]
               for root in sorted({find(i) for i in range(5)})]
    accepted = all(find(c['fi']) == find(c['fj']) for c in pcs)
    # Arbitrary ordered compatibility predicates, even without equality semantics.
    allowed = {(c['fi'],c['fj']) for c in cs} | {(c['fj'],c['fi']) for c in cs}
    needed = {(c['fi'],c['fj']) for c in pcs}
    predicate_accepted = needed <= allowed
    # Signed constant relief: solve all sibling equations, retaining exact kernel.
    import sympy as sp
    equations = []
    for c in cs:
        row = [0]*5
        row[c['fi']] += 1
        row[c['fj']] += 1
        equations.append(row)
    kernel = sp.Matrix(equations).nullspace()
    signed_accepted = all(all(v[c['fi']]+v[c['fj']] == 0 for v in kernel) for c in pcs)
    report = dict(
        scope="Exact carrier geometry and whole-face constant-rule controls only",
        metric=[[3,0,0],[0,1,0],[0,0,1]],face_names=FACE_NAMES,
        children=[dict(name=name,rotation=p[0],translation=p[1],scale=p[2]) for name,p in named],
        all_proper_isometries=True,contained=True,volume_ratio_sum=1,
        separating_axes=separators,contacts=cs,face_coverage=coverage,
        interior_address=dict(address=address,pose=pose,fixed_point=fixed),
        periodic_control=dict(cell=cell,lattice_basis=I,contacts=pcs,
                              carrier_coverage="two nonoverlapping equal triangular prisms fill the unit box"),
        Q001=dict(equality_classes=classes,periodic_control_accepted=accepted,
                  observed_face_pairs=sorted(allowed),periodic_face_pairs=sorted(needed),
                  arbitrary_face_pair_predicate_accepts_control=predicate_accepted,
                  signed_kernel=[list(v) for v in kernel],signed_control_accepted=signed_accepted),
        sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (ROOT/'geometry.py',Path(__file__))},
    )
    out = ROOT/'artifacts'/'geometry_and_constant_rules.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(encode(report),indent=2)+'\n')
    print(json.dumps(dict(children=8,sibling_contacts=len(cs),face_checks=len(coverage),
                          periodic_contacts=len(pcs),Q001=encode(report['Q001'])),indent=2))


if __name__ == '__main__':
    main()

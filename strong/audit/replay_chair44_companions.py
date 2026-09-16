#!/usr/bin/env python3
"""Independent finite Chair44 companion-collision replay, standard library only.

Reads release geometry and certificates as data; imports no release code.
Mesh vertices are converted to integers in units of 1/10000, complete feature
poses and carrier cubes to units of 1/8, physical core widths to units of 1/400.
The continuous whole-feature-companion theorem is outside this finite check.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product
import gzip
import hashlib
import json
from pathlib import Path
import time


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def plus(a, b):
    return tuple(x+y for x,y in zip(a,b))


def minus(a, b):
    return tuple(x-y for x,y in zip(a,b))


def scale(k, a):
    return tuple(k*x for x in a)


def transform(m, v):
    return tuple(sum(a*b for a,b in zip(row,v)) for row in m)


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def rows(frame):
    perm, signs = frame
    demand(sorted(perm)==[0,1,2] and all(s in (-1,1) for s in signs), 'invalid frame')
    return tuple(tuple(signs[i] if j==perm[i] else 0 for j in range(3)) for i in range(3))


def pose(record):
    frame, shift = record
    return rows(frame), tuple(shift)


def inverse_pose(p):
    m,t=p
    mt=tuple(zip(*m))
    return mt,scale(-1,transform(mt,t))


def column_pose(frame, shift):
    demand(sorted(map(abs,frame))==[1,2,3], 'invalid column frame')
    m=tuple(tuple((1 if frame[j]>0 else -1) if abs(frame[j])==i+1 else 0 for j in range(3)) for i in range(3))
    return m,tuple(shift)


def determinant(m):
    return sum(m[0][i]*cross(m[1],m[2])[i] for i in range(3))


def main():
    start=time.monotonic()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-root',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    packet=args.release_root/'verify/packets/r44_unrestricted_alignment'
    paths={
        'solid':args.release_root/'solid/r44_solid.json',
        'atlas':packet/'input/candidate_certificate.json',
        'rejections':packet/'input/companion_collision_certificate.json',
        'boxes':packet/'results/collision_core_witnesses.jsonl.gz',
        'canonical_atlas':args.release_root/'certificates/candidate_certificate.json',
        'canonical_rejections':args.release_root/'certificates/companion_collision_certificate.json',
        'packet_solid':packet/'input/r44_solid.json',
    }
    for canonical,copy in [('canonical_atlas','atlas'),('canonical_rejections','rejections'),('solid','packet_solid')]:
        demand(paths[canonical].read_bytes()==paths[copy].read_bytes(), 'packet/canonical source mismatch: '+copy)
    solid=json.loads(paths['solid'].read_text())
    cubes=tuple(tuple(c) for c in solid['base_unit_cubes'])
    demand(cubes==tuple(c for c in product((0,1),repeat=3) if c!=(1,1,1)), 'unexpected ordered carrier cubes')
    demand(Fraction(solid['base_halfwidth'])==Fraction(1,100) and Fraction(solid['height_unit'])==Fraction(1,10000), 'unexpected feature dimensions')
    # Mesh-first feature extraction: all components of sloping triangle fans.
    vertices=[]
    for point in solid['vertices']:
        q=tuple(Fraction(x)*10000 for x in point)
        demand(all(x.denominator==1 for x in q), 'mesh not on ten-thousandths lattice')
        vertices.append(tuple(map(int,q)))
    tris=[tuple(t) for t in solid['triangles']]
    demand(len(set(vertices))==len(vertices), 'duplicate mesh vertex')
    edges=defaultdict(list)
    normals=[]
    for i,tri in enumerate(tris):
        demand(len(tri)==3 and len(set(tri))==3 and all(0<=v<len(vertices) for v in tri),'invalid mesh triangle')
        a,b,c=(vertices[v] for v in tri)
        n=cross(minus(b,a),minus(c,a))
        demand(any(n),'degenerate mesh triangle')
        normals.append(n)
        for a,b in zip(tri,tri[1:]+tri[:1]):
            edges[tuple(sorted((a,b)))].append(i)
    demand(all(len(t)==2 for t in edges.values()), 'nonmanifold mesh edge')
    sloping={i for i,n in enumerate(normals) if sum(x!=0 for x in n)>1}
    adjacent=defaultdict(set)
    for i,j in edges.values():
        if i in sloping and j in sloping:
            adjacent[i].add(j)
            adjacent[j].add(i)
    groups=[]
    unseen=set(sloping)
    while unseen:
        todo=[unseen.pop()]
        for i in todo:
            for j in adjacent[i]:
                if j in unseen:
                    unseen.remove(j)
                    todo.append(j)
        groups.append(todo)
    demand(len(groups)==192 and all(len(g)==4 for g in groups), 'unexpected feature fans')
    panels=[]
    for cube in cubes:
        for axis in range(3):
            for sign in (-1,1):
                normal=tuple(sign if j==axis else 0 for j in range(3))
                if plus(cube,normal) not in cubes:
                    center=tuple(10000*cube[j]+5000+5000*normal[j] for j in range(3))
                    panels.append((center,normal,axis))
    demand(len(panels)==24, 'wrong panel inventory')
    extracted={}
    for g in groups:
        counts=Counter(v for i in g for v in tris[i])
        demand(sorted(counts.values())==[2,2,2,2,4], 'fan incidence mismatch')
        apex=vertices[next(v for v,n in counts.items() if n==4)]
        base=frozenset(vertices[v] for v,n in counts.items() if n==2)
        sums=tuple(sum(v[j] for v in base) for j in range(3))
        demand(all(x%4==0 for x in sums), 'invalid fan center')
        center=tuple(x//4 for x in sums)
        axes=[j for j in range(3) if len({v[j] for v in base})==1]
        demand(len(axes)==1,'noncoordinate base')
        axis=axes[0]
        tangent=[j for j in range(3) if j!=axis]
        demand(all(apex[j]==center[j] for j in tangent), 'apex not centered')
        demand({tuple(v[j]-center[j] for j in tangent) for v in base}==set(product((-100,100),repeat=2)), 'incorrect square base')
        owners=[normal for pc,normal,ax in panels if ax==axis and center[axis]==pc[axis] and all(abs(center[j]-pc[j])+100<5000 for j in tangent)]
        demand(len(owners)==1, 'ambiguous carrier panel')
        normal=owners[0]
        coefficient=(apex[axis]-center[axis])*normal[axis]
        demand(1<=abs(coefficient)<=12, 'unexpected height')
        demand(all(normals[i][axis]*normal[axis]>0 for i in g), 'feature facets not oriented outward')
        demand(all(c%1250==0 for c in center),'center not eighth-integral')
        center8=tuple(c//1250 for c in center)
        extracted[(base,apex)]=(center8,normal,coefficient)
    demand(len(extracted)==192,'duplicate extracted feature')
    # Assign certificate role names only after recovering actual feature geometry.
    features={}
    for patch in solid['patches']:
        def read10000(point):
            q=tuple(Fraction(x)*10000 for x in point)
            demand(all(v.denominator==1 for v in q),'nonintegral annotation')
            return tuple(map(int,q))
        key=(frozenset(read10000(p) for p in patch['base']),read10000(patch['apex']))
        demand(key in extracted,'annotation absent from mesh')
        role=patch['role']
        demand(role not in features,'duplicate role')
        features[role]=extracted[key]
        demand(features[role][2]==patch['coefficient']==solid['profile'][role], 'coefficient annotation mismatch')
    demand(set(features)==set(range(192)) and len(set(features.values()))==192,'feature annotation not bijective')
    frames=[rows((p,s)) for p in permutations(range(3)) for s in product((-1,1),repeat=3)]
    demand(len(set(frames))==48,'frame enumeration mismatch')
    roles_by_type=defaultdict(list)
    for role,(center,normal,key) in features.items():
        roles_by_type[(normal,key)].append((role,center))
    matches=defaultdict(set)
    for m in frames:
        for source,(center,normal,key) in features.items():
            transformed_center=transform(m,center)
            opposite_normal=scale(-1,transform(m,normal))
            for target,target_center in roles_by_type[(opposite_normal,-key)]:
                matches[(m,minus(target_center,transformed_center))].add(target)
    demand(len(matches)==6862,'candidate pose count changed')
    # Use all eight cube corners to avoid negative-frame lower-corner shortcuts.
    rotated={}
    for m in frames:
        rotated[m]=tuple(tuple(min(transform(m,plus(c,d))[j] for d in product((0,1),repeat=3))*8 for j in range(3)) for c in cubes)
    @lru_cache(None)
    def lower_corners(p):
        m,t=p
        return tuple(plus(c,t) for c in rotated[m])
    def intersect(a,b):
        lo=tuple(max(x,y) for x,y in zip(a,b))
        hi=tuple(min(x,y)+8 for x,y in zip(a,b))
        return (lo,hi) if all(x<y for x,y in zip(lo,hi)) else None
    identity=(rows(((0,1,2),(1,1,1))),(0,0,0))
    direct={}
    for p in matches:
        hit=next((q for a in lower_corners(identity) for b in lower_corners(p) if (q:=intersect(a,b)) is not None),None)
        if hit is not None:
            direct[p]=hit
    survivors=set(matches)-set(direct)
    demand(len(direct)==1545 and len(survivors)==5317,'direct collision census changed')
    direct_min=min(min(50*(hi[j]-lo[j])-8 for j in range(3)) for lo,hi in direct.values())
    demand(direct_min>=42,'direct collisions fail retained-core margin')
    partners={role:set() for role in features}
    for p in survivors:
        for role in matches[p]:
            partners[role].add(p)
    demand(all(partners.values()),'empty full partner list')
    rejected=json.loads(paths['rejections'].read_text())['witnesses']
    indexed={}
    for record in rejected:
        p=pose(record['rejected_pose'])
        demand(p in survivors and p not in indexed,'invalid/duplicate rejected pose')
        owner=record['marker_owner']
        role=record['native_role']
        demand(owner in (0,1) and role in partners,'invalid rejection owner/role')
        other=p if owner==0 else inverse_pose(p)
        demand(other not in partners[role], 'other tile itself accompanies witness feature')
        demand(len(partners[role])==record['possible_partners'],'incorrect partner count')
        indexed[p]=(owner,role,other)
    demand(len(indexed)==5273,'rejection census changed')
    seen=set()
    boxes=0
    minimum=None
    owners=Counter()
    with gzip.open(paths['boxes'],'rt') as stream:
        for line in stream:
            record=json.loads(line)
            original=pose(record['original_pair'])
            demand(original in indexed and original not in seen,'invalid/duplicate collision record')
            seen.add(original)
            owner,role,other=indexed[original]
            demand((record['marker_owner'],record['native_role'])==(owner,role),'certificate/box role mismatch')
            demand(column_pose(*record['normalized_other'])==other,'incorrect normalized other pose')
            options=set()
            for frame,shift,ia,ib,claimed_lo,claimed_hi in record['overlaps']:
                p=column_pose(frame,shift)
                demand(p in partners[role] and p not in options,'invalid/duplicate listed partner')
                options.add(p)
                demand(0<=ia<7 and 0<=ib<7,'invalid cube witness')
                actual=intersect(lower_corners(other)[ia],lower_corners(p)[ib])
                demand(actual is not None,'claimed carrier collision absent')
                lo,hi=actual
                demand((tuple(claimed_lo),tuple(claimed_hi))==actual,'claimed carrier intersection incorrect')
                # Erode each carrier cube by rho=1/100. With eighth-grid
                # endpoints, the exact intersection widths in 1/400 units are:
                widths=tuple(50*(hi[j]-lo[j])-8 for j in range(3))
                demand(min(widths)>=42,'physical core collision absent')
                minimum=min(widths) if minimum is None else min(minimum,min(widths))
                boxes+=1
            demand(options==partners[role],'export omitted an unpruned partner')
            owners[owner]+=1
    demand(seen==set(indexed),'missing rejected-pose collision record')
    demand(boxes==299975,'collision witness count changed')
    final=survivors-set(indexed)
    atlas=json.loads(paths['atlas'].read_text())['legal_contacts']
    claimed={(rows(frame),scale(8,tuple(shift))) for frame,shift in atlas}
    demand(len(claimed)==len(atlas)==44 and final==claimed,'survivors do not equal registered atlas')
    demand(all(determinant(m)==1 and all(x%8==0 for x in t) for m,t in final),'final pose is improper or fractional')
    report={
        'status':'PASS',
        'scope':'Independent mesh-feature extraction, full 48-frame complete-feature mate census, direct carrier collision exclusion, and exact universal-partner collision certificate replay. Assumes the separately proved continuous whole-feature companion theorem and retained-core inclusion; does not prove those continuous statements or the full aperiodicity theorem.',
        'released_code_executed_or_imported':False,
        'packet_sources_byte_equal_canonical':True,
        'arithmetic':'integer, except exact Fraction parsing of source coordinates',
        'source_hashes':{str(p.relative_to(args.release_root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'mesh_vertices':len(vertices),'mesh_triangles':len(tris),'mesh_feature_fans':len(groups),
        'candidate_poses':len(matches),'direct_collisions':len(direct),'isolated_survivors':len(survivors),
        'isolated_integer_poses':sum(all(v%8==0 for v in t) for m,t in survivors),
        'isolated_fractional_poses':sum(any(v%8 for v in t) for m,t in survivors),
        'full_partner_sizes':{str(k):len(v) for k,v in sorted(partners.items())},
        'rejected_poses':len(indexed),'rejection_feature_owners':dict(sorted(owners.items())),
        'collision_boxes':boxes,'all_unpruned_partners_accounted_for':True,
        'minimum_direct_core_width_over_400':direct_min,'minimum_companion_core_width_over_400':minimum,
        'certified_open_ball_radius':'21/400','registered_atlas_exactly_recovered':True,
        'remaining_poses':len(final),'remaining_all_integral_and_proper':True,
        'seconds':time.monotonic()-start,
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='full_partner_sizes'},indent=2))


if __name__=='__main__':
    main()

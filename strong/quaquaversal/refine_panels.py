"""Q003: seek a finite boundary line arrangement compatible with substitution.

Full supporting chords overrefine the minimal required segments. Stabilizing
therefore gives a useful sufficient arrangement; growth alone is inconclusive.
"""

import argparse
import hashlib
import json
from pathlib import Path

from geometry import (F,I,ZERO,child_maps,contacts,encode,face_polygons,
                      inverse_point,plane,dot,area2,transform,intersection)
from polynomial_rules import COORDS,embed,contact_map
from periodic_obstruction import affine,act

ROOT = Path(__file__).resolve().parent


def line(p,q):
    a,b = p[1]-q[1],q[0]-p[0]
    c = -a*p[0]-b*p[1]
    pivot = next(x for x in (a,b) if x)
    return a/pivot,b/pivot,c/pivot


def value(l,p):
    return l[0]*p[0]+l[1]*p[1]+l[2]


def chord(l,poly):
    points = []
    for p,q in zip(poly,poly[1:]+poly[:1]):
        a,b = value(l,p),value(l,q)
        if a == 0:
            points.append(p)
        if a*b < 0:
            t = a/(a-b)
            points.append(tuple(x+t*(y-x) for x,y in zip(p,q)))
    points = list(dict.fromkeys(points))
    return (points[0],points[1]) if len(points) >= 2 else None


def split(poly,l,sign):
    out = []
    for p,q in zip(poly,poly[1:]+poly[:1]):
        a,b = sign*value(l,p),sign*value(l,q)
        if a >= 0:
            out.append(p)
        if a*b < 0:
            t = a/(a-b)
            out.append(tuple(x+t*(y-x) for x,y in zip(p,q)))
    return list(dict.fromkeys(out))


def charts():
    polys = face_polygons((I,ZERO,F(1)))
    return [[tuple(p[k] for k in COORDS[f]) for p in poly] for f,poly in enumerate(polys)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=10)
    parser.add_argument('--limit',type=int,default=1000)
    parser.add_argument('--seed-audit',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'panel_refinement.json')
    args = parser.parse_args()
    named = child_maps()
    poses = [p for _,p in named]
    transfers = []
    for c in contacts(poses):
        for reverse in (False,True):
            q = dict(c)
            if reverse:
                q.update(i=c['j'],j=c['i'],fi=c['fj'],fj=c['fi'])
            domain = [tuple(inverse_point(poses[q['i']],v)[k] for k in COORDS[q['fi']]) for v in c['polygon']]
            transfers.append(dict(kind='sibling',i=q['i'],j=q['j'],source=q['fi'],target=q['fj'],
                                  domain=domain,map=affine(contact_map(poses,q))))
    parent = (I,ZERO,F(1))
    for fi,pface in enumerate(face_polygons(parent)):
        n,d = plane(pface)
        for i,pose in enumerate(poses):
            for fj,cface in enumerate(face_polygons(pose)):
                if all(dot(n,v) == d for v in cface):
                    domain = [tuple(v[k] for k in COORDS[fi]) for v in cface]
                    q = dict(i=0,j=1,fi=fi,fj=fj)
                    transfers.append(dict(kind='hereditary',i=-1,j=i,source=fi,target=fj,
                                          domain=domain,map=affine(contact_map([parent,pose],q))))
    original = charts()
    known = [{line(p,q) for p,q in zip(poly,poly[1:]+poly[:1])} for poly in original]
    if args.seed_audit:
        seed = json.loads(args.seed_audit.read_text())
        for failure in seed['failures']:
            if 'target' not in failure:
                continue
            v = tuple(F(x) for x in failure['target'])
            for f,poly3 in enumerate(face_polygons(parent)):
                n,d = plane(poly3)
                if dot(n,v) == d:
                    a,b = (v[k] for k in COORDS[f])
                    known[f].update(((F(1),F(0),-a),(F(0),F(1),-b)))
    frontier = [set(v) for v in known]
    rounds = []
    witnesses = []
    for step in range(args.rounds):
        fresh = [set() for _ in range(5)]
        for t in transfers:
            for l in sorted(frontier[t['source']]):
                segment = chord(l,t['domain'])
                if segment is None:
                    continue
                target = line(*(act(t['map'],p) for p in segment))
                f = t['target']
                if target not in known[f] and target not in fresh[f]:
                    fresh[f].add(target)
                    witnesses.append(dict(round=step+1,transfer=transfers.index(t),source_line=l,target_line=target))
        for old,new in zip(known,fresh):
            old.update(new)
        frontier = fresh
        row = dict(round=step+1,added=sum(map(len,fresh)),line_counts=list(map(len,known)))
        rounds.append(row)
        print(json.dumps(row),flush=True)
        if row['added'] == 0 or sum(map(len,known)) >= args.limit:
            break
    stable = not any(frontier)
    panels = None
    if stable:
        panels = []
        for poly,lines in zip(original,known):
            parts = [poly]
            for l in sorted(lines):
                newer = []
                for part in parts:
                    for sign in (-1,1):
                        piece = split(part,l,sign)
                        if len(piece) >= 3 and area2(piece):
                            if piece not in newer:
                                newer.append(piece)
                parts = newer
            assert sum(abs(area2(p)) for p in parts) == abs(area2(poly))
            panels.append(parts)
        print('panel counts',list(map(len,panels)),flush=True)
    output = dict(scope='Boundary line closure; panel incidence still needs a separate audit',
                  status='line_closure_stabilized' if stable else 'unknown_after_finite_prefix',
                  rounds=rounds,lines=[sorted(v) for v in known],panels=panels,
                  transfers=transfers,new_line_witnesses=witnesses,
                  arguments={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',
                                     ROOT/'periodic_obstruction.py',Path(__file__))})
    if args.seed_audit:
        output['sources'][args.seed_audit.name] = hashlib.sha256(args.seed_audit.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(encode(output),indent=2)+'\n')


if __name__ == '__main__':
    main()

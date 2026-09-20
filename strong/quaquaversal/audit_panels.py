"""Exact positive-area and vertex audits for Q003's proposed panel partition.

This is a finite hypothesis audit, not a generated decorated tile set.
"""

import hashlib
import json
import argparse
from pathlib import Path

from geometry import F,VERTICES,child_maps,encode,inside,inverse_point,transform,area2,clip2,sub,cross,ZERO
from polynomial_rules import embed
from periodic_obstruction import act

ROOT = Path(__file__).resolve().parent


def segment_clip(a,b):
    """Parameter interval of a segment in the canonical closed prism."""
    av = (a[0],a[1],1-a[0]-a[1],a[2],1-a[2])
    bv = (b[0],b[1],1-b[0]-b[1],b[2],1-b[2])
    lo,hi = F(0),F(1)
    for x,y in zip(av,bv):
        if x < 0 and y < 0:
            return None
        if x < 0 <= y:
            lo = max(lo,-x/(y-x))
        if y < 0 <= x:
            hi = min(hi,x/(x-y))
    return (lo,hi) if lo <= hi else None


def segment_parameter(a,b,p):
    delta = sub(b,a)
    if cross(delta,sub(p,a)) != ZERO:
        return None
    j = next(i for i,x in enumerate(delta) if x)
    return (p[j]-a[j])/delta[j]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'panel_refinement.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'panel_audit.json')
    args = parser.parse_args()
    path = args.input
    raw = json.loads(path.read_text())
    panels = [[[tuple(F(x) for x in p) for p in poly] for poly in face] for face in raw['panels']]
    counts = dict(sibling_positive_pairs=0,hereditary_positive_pairs=0,vertex_incidences=0,
                  sibling_edge_incidences=0,hereditary_edges=0)
    failures = []
    for ti,t in enumerate(raw['transfers']):
        mapping = [tuple(F(x) for x in row) for row in t['map']]
        domain = [tuple(F(x) for x in p) for p in t['domain']]
        for si,source in enumerate(panels[t['source']]):
            image = [act(mapping,p) for p in source]
            for tj,target in enumerate(panels[t['target']]):
                overlap = clip2(image,target)
                area = abs(area2(overlap))
                if not area:
                    continue
                if t['kind'] == 'sibling':
                    counts['sibling_positive_pairs'] += 1
                    if area != abs(area2(image)) or area != abs(area2(target)):
                        failures.append(dict(kind='sibling_panel_mismatch',transfer=ti,source=si,target=tj))
                else:
                    counts['hereditary_positive_pairs'] += 1
                    if area != abs(area2(target)):
                        failures.append(dict(kind='hereditary_panel_cut',transfer=ti,source=si,target=tj))
    all_vertices = {tuple(embed(f,*p)) for f,face in enumerate(panels) for poly in face for p in poly}
    poses = [p for _,p in child_maps()]
    for i,p in enumerate(poses):
        for v in all_vertices:
            w = transform(p,v)
            for j,q in enumerate(poses):
                if i == j:
                    continue
                u = inverse_point(q,w)
                if inside(u):
                    counts['vertex_incidences'] += 1
                    if u not in all_vertices:
                        failures.append(dict(kind='sibling_vertex_missing',i=i,j=j,source=v,target=u))
    for v in all_vertices:
        for j,q in enumerate(poses):
            u = inverse_point(q,v)
            if inside(u) and u not in all_vertices:
                failures.append(dict(kind='hereditary_vertex_missing',child=j,source=v,target=u))
    edges = {tuple(sorted((tuple(embed(f,*p)),tuple(embed(f,*q)))))
             for f,face in enumerate(panels) for poly in face
             for p,q in zip(poly,poly[1:]+poly[:1]) if p != q}
    for i,p in enumerate(poses):
        for a,b in edges:
            aw,bw = transform(p,a),transform(p,b)
            for j,q in enumerate(poses):
                if i == j:
                    continue
                aq,bq = inverse_point(q,aw),inverse_point(q,bw)
                interval = segment_clip(aq,bq)
                if interval is None or interval[0] == interval[1]:
                    continue
                counts['sibling_edge_incidences'] += 1
                if interval != (0,1) or tuple(sorted((aq,bq))) not in edges:
                    failures.append(dict(kind='sibling_edge_mismatch',i=i,j=j,source=[a,b],
                                         target=aq,target_end=bq,interval=interval))
    for a,b in edges:
        intervals = []
        for p in poses:
            for c,d in edges:
                cw,dw = transform(p,c),transform(p,d)
                s,t = segment_parameter(a,b,cw),segment_parameter(a,b,dw)
                if s is None or t is None:
                    continue
                lo,hi = sorted((s,t))
                if hi > 0 and lo < 1:
                    if lo < 0 or hi > 1:
                        failures.append(dict(kind='hereditary_edge_crosses_vertex',source=[a,b],child_edge=[cw,dw]))
                    intervals.append((max(F(0),lo),min(F(1),hi)))
        reach = F(0)
        for lo,hi in sorted(intervals):
            if lo > reach:
                break
            reach = max(reach,hi)
        if reach != 1:
            failures.append(dict(kind='hereditary_edge_gap',source=[a,b],covered_until=reach))
        counts['hereditary_edges'] += 1
    out = dict(scope='Exact positive-area panel, line-segment, and vertex inheritance/incidence checks',
               counts=counts,panel_counts=list(map(len,panels)),canonical_vertex_count=len(all_vertices),
               failures=failures,
               sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'periodic_obstruction.py',path,Path(__file__))})
    args.output.write_text(json.dumps(encode(out),indent=2)+'\n')
    print(json.dumps(dict(counts=counts,vertices=len(all_vertices),failures=len(failures)),indent=2))
    if failures:
        print(json.dumps(encode(failures[:5]),indent=2))


if __name__ == '__main__':
    main()

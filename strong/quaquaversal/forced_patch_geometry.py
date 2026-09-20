"""Q015: geometric pair obstructions in the forced expanded patches.

Use exact integer boxes and atlas membership as a broad phase. For a
non-atlas pair, exact clipping supplies a common point if they intersect.
Such a pair cannot occur in a tiling satisfying the closed-star rule.
Surviving patches remain unresolved; this is not a tiling-extension test.
"""

import argparse
import hashlib
import json
from collections import Counter,defaultdict
from itertools import product
from math import lcm
from pathlib import Path

from geometry import inverse_rotation,encode
from contact_atlas import relative
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'forced_outer_layer_3.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'forced_patch_geometry.json')
    args = parser.parse_args()
    atlas_path = ROOT/'artifacts'/'closed_contact_atlas.json'
    atlas_raw,source = [json.loads(p.read_text()) for p in (atlas_path,args.input)]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in source['poses']]
    used = sorted({tile for row in source['results'] if 'domains' in row for tile,di in row['domains']})
    scale = poses[0][2]
    assert all(poses[i][2] == scale for i in used)
    rotations = list(dict.fromkeys(poses[i][0] for i in used))
    rotation_ids = {r:i for i,r in enumerate(rotations)}
    inverses = [inverse_rotation(r) for r in rotations]
    translations = {i:tuple(v/scale for v in poses[i][1]) for i in used}
    d = lcm(*(v.denominator for r in rotations+inverses+[p[0] for p in atlas] for row in r for v in row),
            *(v.denominator for t in list(translations.values())+[p[1] for p in atlas] for v in t))
    def integer(v):
        assert (v*d).denominator == 1
        return int(v*d)
    rs = [tuple(tuple(integer(v) for v in row) for row in r) for r in rotations]
    invs = [tuple(tuple(integer(v) for v in row) for row in r) for r in inverses]
    ts = {i:tuple(integer(v) for v in t) for i,t in translations.items()}
    rids = {i:rotation_ids[poses[i][0]] for i in used}
    ar = list(dict.fromkeys(p[0] for p in atlas))
    arids = {r:i for i,r in enumerate(ar)}
    rlookup = {tuple(integer(v)*d for row in r for v in row):i for i,r in enumerate(ar)}
    lookup = {(arids[p[0]],tuple(integer(v)*d for v in p[1])) for p in atlas}
    products = {}
    def in_atlas(i,j):
        a,b = rids[i],rids[j]
        key = a,b
        if key not in products:
            matrix = tuple(sum(invs[a][u][k]*rs[b][k][v] for k in range(3)) for u in range(3) for v in range(3))
            products[key] = rlookup.get(matrix)
        rid = products[key]
        if rid is None:
            return False
        delta = tuple(y-x for x,y in zip(ts[i],ts[j]))
        t = tuple(sum(a*b for a,b in zip(row,delta)) for row in invs[rids[i]])
        return (rid,t) in lookup
    boxes = {}
    bins = {}
    for i in used:
        r,t = rs[rids[i]],ts[i]
        vs = [tuple(t[k]+(r[k][a] if a is not None else 0)+z*r[k][2] for k in range(3))
              for a in (None,0,1) for z in (0,1)]
        boxes[i] = tuple((min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3))
        bins[i] = list(product(*(range(lo//d,hi//d+1) for lo,hi in boxes[i])))
    safe = set()
    forbidden = {}
    witnesses = []
    n = len(poses)
    results = []
    counts = Counter()
    clipping_tests = 0
    total = sum('domains' in r for r in source['results'])
    for si,record in enumerate(source['results']):
        if 'domains' not in record:
            continue
        grid = defaultdict(list)
        failure = None
        for j,di in record['domains']:
            candidates = sorted({i for cell in bins[j] for i in grid[cell]})
            for i in candidates:
                key = min(i,j)*n+max(i,j)
                if key in safe:
                    continue
                if key in forbidden:
                    failure = forbidden[key]
                    break
                if any(hi < lo2 or hi2 < lo for (lo,hi),(lo2,hi2) in zip(boxes[i],boxes[j])):
                    safe.add(key)
                    continue
                if in_atlas(i,j):
                    safe.add(key)
                    continue
                rel = relative(poses[i],poses[j])
                clipping_tests += 1
                points = edge_points(rel,first_only=True)
                if points:
                    failure = len(witnesses)
                    forbidden[key] = failure
                    witnesses.append(dict(tiles=(i,j),relative_pose=rel,common_points=sorted(points)))
                    break
                safe.add(key)
            if failure is not None:
                break
            for cell in bins[j]:
                grid[cell].append(j)
        result = dict(source_index=si,boundary_index=record['boundary_index'],cover_index=record['cover_index'])
        if failure is None:
            counts['survivor'] += 1
            result['status'] = 'unknown_after_pair_geometry'
        else:
            counts['rejected'] += 1
            result['forbidden_pair_witness'] = failure
        results.append(result)
        if len(results)%50 == 0:
            print(f'forced patch geometry: {len(results)}/{total}; {dict(counts)}; clipped {clipping_tests}',flush=True)
    output = dict(scope='Necessary exact geometric pair test of forced finite patches; survivors remain unresolved',
                  arguments={k:str(v) for k,v in vars(args).items()},integer_scale=d,
                  results=results,witnesses=witnesses,status_counts=dict(counts),
                  edge_clipping_tests=clipping_tests,distinct_safe_pairs=len(safe),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',
                            ROOT/'audit_closed_atlas.py',atlas_path,args.input,Path(__file__))})
    args.output.write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),statuses=dict(counts),witnesses=len(witnesses))),flush=True)


if __name__ == '__main__':
    main()

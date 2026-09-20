"""Q019: necessary non-overlap clauses from seven strict interior samples.

Use each candidate prism's centroid and the midpoints from it to all six
vertices. If another candidate contains one of these points in its interior,
the two supports cannot coexist. This detects only some overlaps; undetected
pairs remain unknown. All arithmetic is integer and strict, with witnesses.
"""

import hashlib
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERTICES = ((0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,0,1),(0,1,1))
SAMPLES = ((4,4,6),)+tuple((2+6*x,2+6*y,3+6*z) for x,y,z in VERTICES)


def main():
    path = ROOT/'artifacts'/'neighbor_incidence_sat.json'
    source = json.loads(path.read_text())
    keys = source['normalized_pose_keys']
    d = source['pose_key_denominator']
    rs = [tuple(tuple(key[3*i+j] for j in range(3)) for i in range(3)) for key in keys]
    ts = [tuple(key[9:]) for key in keys]
    # B/(3d) is the physical-metric inverse of R/d, G=diag(3,1,1).
    metric = (3,1,1)
    invs = [tuple(tuple((3//metric[i])*r[j][i]*metric[j] for j in range(3)) for i in range(3)) for r in rs]
    boxes = []
    grid = defaultdict(list)
    for i,(r,t) in enumerate(zip(rs,ts)):
        vs = [tuple(t[k]+sum(r[k][j]*v[j] for j in range(3)) for k in range(3)) for v in VERTICES]
        box = tuple((min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3))
        boxes.append(box)
        for cell in product(*(range(lo//d,hi//d+1) for lo,hi in box)):
            grid[cell].append(i)
    forbidden = {}
    candidate_tests = 0
    denominator = 36*d*d
    for i,(r,t) in enumerate(zip(rs,ts)):
        for sample,vector in enumerate(SAMPLES):
            point = tuple(12*t[k]+sum(r[k][j]*vector[j] for j in range(3)) for k in range(3))
            cell = tuple(v//(12*d) for v in point)
            for j in grid[cell]:
                if i == j:
                    continue
                key = min(i,j),max(i,j)
                if key in forbidden:
                    continue
                if any(not 12*lo < v < 12*hi for v,(lo,hi) in zip(point,boxes[j])):
                    continue
                candidate_tests += 1
                delta = tuple(v-12*u for v,u in zip(point,ts[j]))
                local = tuple(sum(a*b for a,b in zip(row,delta)) for row in invs[j])
                if local[0] > 0 and local[1] > 0 and local[0]+local[1] < denominator and 0 < local[2] < denominator:
                    forbidden[key] = (i,sample,j)
        if (i+1)%2000 == 0:
            print(f'interior sample exclusions: {i+1}/{len(keys)}; pairs {len(forbidden)}',flush=True)
    output = dict(scope='Strict interior common-point witnesses; only a sufficient overlap test, not all forbidden pairs',
                  normalized_pose_denominator=d,sample_denominator=12,sample_numerators=SAMPLES,
                  exclusions=[dict(positions=pair,sample_from=i,sample_index=s,containing_tile=j)
                              for pair,(i,s,j) in sorted(forbidden.items())],
                  tested_point_candidate_pairs=candidate_tests,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (path,Path(__file__))})
    (ROOT/'artifacts'/'incidence_sample_exclusions.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(potential_positions=len(keys),sampled_overlap_pairs=len(forbidden),tests=candidate_tests)),flush=True)


if __name__ == '__main__':
    main()

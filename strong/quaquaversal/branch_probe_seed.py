"""Q017 pilot: exhaustive binary star choices in six retained parent cases.

Choose the closest tile to the parent centroid with exactly two star choices.
Each choice becomes a separate necessary-condition problem. These are pilot
branches, not asserted tile placements or accepted infinite tilings.
"""

import hashlib
import json
from pathlib import Path

from geometry import F,transform
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT/'artifacts'/'expanded_arc_seed.json'
    source = json.loads(path.read_text())
    poses = [raw_pose(p) for p in source['poses']]
    pool = list(source['domain_pool'])
    pool_index = {tuple(ss):i for i,ss in enumerate(pool)}
    center = F(1,3),F(1,3),F(1,2)
    distance_cache = {}
    def distance(i):
        if i not in distance_cache:
            p = transform(poses[i],center)
            distance_cache[i] = 3*(p[0]-center[0])**2+(p[1]-center[1])**2+(p[2]-center[2])**2
        return distance_cache[i]
    results = []
    groups = []
    for si,row in enumerate(source['results']):
        if 'domains' not in row:
            continue
        choices = [(distance(tile),tile,di) for tile,di in row['domains'] if len(pool[di]) == 2]
        if not choices:
            continue
        dist,tile,di = min(choices)
        group = dict(original_source_index=si,tile=tile,original_domain=di,
                     squared_distance=str(dist),branch_records=[])
        for star in pool[di]:
            if (star,) not in pool_index:
                pool_index[star,] = len(pool)
                pool.append([star])
            domains = [[i,pool_index[star,] if i == tile else d] for i,d in row['domains']]
            group['branch_records'].append(len(results))
            results.append(dict(source_index=si,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                                branch_tile=tile,branch_star=star,domains=domains))
        groups.append(group)
        if len(groups) == 6:
            break
    assert len(groups) == 6
    output = dict(scope='Six exhaustive binary case splits for a finite propagation pilot; retained branches are unknown',
                  poses=source['poses'],domain_pool=pool,results=results,branch_groups=groups,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',path,Path(__file__))})
    (ROOT/'artifacts'/'branch_probe_seed.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(parent_cases=len(groups),branches=len(results),choices=[(g['tile'],g['squared_distance']) for g in groups])),flush=True)


if __name__ == '__main__':
    main()

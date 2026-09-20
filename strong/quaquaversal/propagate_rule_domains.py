"""Q032: exact forced-neighbor expansion with explicit rule/pose namespace.

Consumes a shared pose/domain artifact and retains every finite survivor as
unknown. Empty-domain witnesses retain their source constraints. Repeat via
explicit input/output paths; no finite survival means infinite extension.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import compose,encode
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_expansion_seed.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_forced_1.json')
    parser.add_argument('--atlas',type=Path,default=ROOT/'artifacts'/'coarse_expansion_atlas.json')
    parser.add_argument('--rules',type=Path,default=ROOT/'artifacts'/'coarse_expansion_rules.json')
    args = parser.parse_args()
    paths = [args.atlas,args.rules,args.input]
    atlas_raw,compat,source = [json.loads(p.read_text()) for p in paths]
    assert source['coordinate_level'] == atlas_raw['coordinate_level'] == compat['coordinate_level']
    active = set(compat['active_stars'])
    assert all(ss and set(ss) <= active for ss in source['domain_pool'])
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in source['poses']]
    pose_index = {p:i for i,p in enumerate(poses)}
    assert len(pose_index) == len(poses)
    cases = [dict(row) for row in compat['cases']]
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    input_bits = [sum(1<<s for s in ss) for ss in source['domain_pool']]
    forced = []
    for ss in source['domain_pool']:
        qs = set(cases[ss[0]])
        for s in ss[1:]:
            qs.intersection_update(cases[s])
        row = []
        for q in sorted(qs):
            value = 0
            for s in ss:
                value |= bits[cases[s][q]]
            row.append((q,value))
        forced.append(row)
    placement_cache = {}
    def placed(tile,q):
        key = tile,q
        if key not in placement_cache:
            p = compose(poses[tile],atlas[q])
            if p not in pose_index:
                pose_index[p] = len(poses)
                poses.append(p)
            placement_cache[key] = pose_index[p]
        return placement_cache[key]
    pool,pool_ids = [],{}
    def identifier(value):
        if value not in pool_ids:
            pool_ids[value] = len(pool)
            ss = []
            remaining = value
            while remaining:
                low = remaining & -remaining
                ss.append(low.bit_length()-1)
                remaining -= low
            pool.append(ss)
        return pool_ids[value]
    results = []
    stats = Counter()
    total = sum('domains' in r for r in source['results'])
    for source_index,record in enumerate(source['results']):
        if 'domains' not in record:
            continue
        domains = {tile:input_bits[di] for tile,di in record['domains']}
        reasons = {tile:[dict(kind='initial_domain',domain=di)] for tile,di in record['domains']}
        failure = None
        for tile,di in record['domains']:
            for q,value in forced[di]:
                neighbor = placed(tile,q)
                domains[neighbor] = domains.get(neighbor,value) & value
                reasons.setdefault(neighbor,[]).append(dict(kind='forced_neighbor',tile=tile,domain=di,pair=q))
                if not domains[neighbor]:
                    failure = dict(tile=neighbor,requirements=reasons[neighbor])
                    break
            if failure:
                break
        result = dict(source_index=source_index,boundary_index=record['boundary_index'],cover_index=record['cover_index'])
        if failure:
            stats['rejected'] += 1
            result['rejection'] = failure
        else:
            stats['survivor'] += 1
            result['domains'] = [(i,identifier(v)) for i,v in sorted(domains.items())]
        results.append(result)
        if len(results)%250 == 0:
            print(f'forced propagation: {len(results)}/{total}; {dict(stats)}; positions {len(poses)}',flush=True)
    output = dict(scope='One synchronous necessary forced-neighbor propagation; finite survivors remain unknown',
                  coordinate_level=source['coordinate_level'],
                  arguments={k:str(v) for k,v in vars(args).items()},
                  poses=poses,domain_pool=pool,results=results,status_counts=dict(stats),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),statuses=dict(stats),positions=len(poses),domains=len(pool))),flush=True)


if __name__ == '__main__':
    main()

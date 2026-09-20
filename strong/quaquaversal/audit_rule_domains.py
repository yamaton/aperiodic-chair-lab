"""Audit a whole forced layer with explicit rule/pose namespace inputs.

Snapshot of audit_forced_domains.py with absent zero-count categories handled
explicitly. Preserve the old source because earlier artifacts bind its hash.
Replay every survivor's complete domain intersections, not just rejection
witnesses. The input-domain correctness is inherited from its own certificate.
"""

import argparse
import hashlib
import json
from functools import cache
from pathlib import Path

from geometry import compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_forced_1.json')
    parser.add_argument('--source',type=Path,default=ROOT/'artifacts'/'coarse_expansion_seed.json')
    parser.add_argument('--source-poses',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_forced_1_audit.json')
    parser.add_argument('--atlas',type=Path,default=ROOT/'artifacts'/'coarse_expansion_atlas.json')
    parser.add_argument('--rules',type=Path,default=ROOT/'artifacts'/'coarse_expansion_rules.json')
    args = parser.parse_args()
    paths = [args.atlas,args.rules,args.source,args.input]
    atlas_raw,compat,source,raw = [json.loads(p.read_text()) for p in paths]
    assert source['coordinate_level'] == raw['coordinate_level'] == atlas_raw['coordinate_level'] == compat['coordinate_level']
    assert all(ss and set(ss) <= set(compat['active_stars']) for ss in source['domain_pool'])
    if 'poses' in source:
        source_poses = source['poses']
    else:
        assert args.source_poses is not None
        paths.append(args.source_poses)
        source_poses = json.loads(args.source_poses.read_text())['poses']
    assert raw['poses'][:len(source_poses)] == source_poses
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in raw['poses']]
    index = {p:i for i,p in enumerate(poses)}
    assert len(index) == len(poses)
    cases = [dict(row) for row in compat['cases']]
    pool = [frozenset(ss) for ss in source['domain_pool']]
    output_pool = [frozenset(ss) for ss in raw['domain_pool']]
    forced = []
    for ss in pool:
        qs = set.intersection(*(set(cases[s]) for s in ss))
        forced.append({q:frozenset(t for s in ss for t in compat['domains'][cases[s][q]]['stars']) for q in sorted(qs)})
    @cache
    def placed(tile,q):
        assert tile < len(source_poses)
        return index[compose(poses[tile],atlas[q])]
    seen = set()
    survived = rejected = intersections = 0
    for ri,result in enumerate(raw['results']):
        si = result['source_index']
        assert si not in seen
        seen.add(si)
        initial_record = source['results'][si]
        assert 'domains' in initial_record
        assert (result['boundary_index'],result['cover_index']) == (initial_record['boundary_index'],initial_record['cover_index'])
        initial = dict(initial_record['domains'])
        if 'rejection' in result:
            failure = result['rejection']
            target = failure['tile']
            constraints = []
            for reason in failure['requirements']:
                di = reason['domain']
                if reason['kind'] == 'initial_domain':
                    assert initial[target] == di
                    constraints.append(pool[di])
                else:
                    tile,q = reason['tile'],reason['pair']
                    assert initial[tile] == di and placed(tile,q) == target
                    constraints.append(forced[di][q])
            assert constraints and not frozenset.intersection(*constraints)
            intersections += len(constraints)
            rejected += 1
        else:
            expected = {tile:pool[di] for tile,di in initial.items()}
            for tile,di in initial.items():
                for q,options in forced[di].items():
                    target = placed(tile,q)
                    expected[target] = expected.get(target,options) & options
                    assert expected[target]
                    intersections += 1
            retained = {tile:output_pool[di] for tile,di in result['domains']}
            assert len(retained) == len(result['domains']) and retained == expected
            survived += 1
        if (ri+1)%500 == 0:
            print(f'full forced-domain audit: {ri+1}/{len(raw["results"])}',flush=True)
    assert seen == {i for i,r in enumerate(source['results']) if 'domains' in r}
    assert set(raw['status_counts']) <= {'survivor','rejected'}
    assert raw['status_counts'].get('survivor',0) == survived
    assert raw['status_counts'].get('rejected',0) == rejected
    output = dict(scope='Explicit-set replay of all retained domains and every rejected witness in one forced layer',
                  survivors=survived,rejections=rejected,domain_intersections=intersections,
                  exact_relative_placements=placed.cache_info().currsize,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

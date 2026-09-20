"""Replay every recorded expanded-domain reduction using exact placements.

Checks soundness of rejected and retained domains. It does not assert that
surviving patches extend, nor need the producer's integer placement index.
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
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_expanded_arcs_1.json')
    parser.add_argument('--source',type=Path,default=ROOT/'artifacts'/'coarse_forced_1.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_expanded_arcs_1_audit.json')
    parser.add_argument('--atlas',type=Path,default=ROOT/'artifacts'/'coarse_expansion_atlas.json')
    parser.add_argument('--rules',type=Path,default=ROOT/'artifacts'/'coarse_expansion_rules.json')
    args = parser.parse_args()
    paths = [args.atlas,args.rules,args.source,args.input]
    atlas_raw,compat,source,raw = [json.loads(p.read_text()) for p in paths]
    assert source['coordinate_level'] == raw['coordinate_level'] == atlas_raw['coordinate_level'] == compat['coordinate_level']
    assert all(ss and set(ss) <= set(compat['active_stars']) for ss in source['domain_pool'])
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in source['poses']]
    cases = [dict(row) for row in compat['cases']]
    allowed = [frozenset(d['stars']) for d in compat['domains']]
    source_pool = [frozenset(ss) for ss in source['domain_pool']]
    retained = [frozenset(ss) for ss in raw['domain_pool']]
    @cache
    def edge(i,j,q):
        assert compose(poses[i],atlas[q]) == poses[j]
        return True
    seen = set()
    rejected = survived = reductions = 0
    for ri,result in enumerate(raw['results']):
        si = result['source_index']
        assert si not in seen
        seen.add(si)
        origin = source['results'][si]
        assert 'domains' in origin
        assert (result['boundary_index'],result['cover_index']) == (origin['boundary_index'],origin['cover_index'])
        domains = {i:source_pool[di] for i,di in origin['domains']}
        for i,j,q in result['reduction_trace']:
            assert domains[i] and domains[j] and edge(i,j,q)
            new = frozenset(s for s in domains[i] if q in cases[s] and allowed[cases[s][q]] & domains[j])
            assert new < domains[i]
            domains[i] = new
            reductions += 1
        assert result['updates'] == len(result['reduction_trace'])
        if 'rejection' in result:
            i,j = result['rejection']['tiles']
            assert result['reduction_trace'][-1] == [i,j,result['rejection']['pair']]
            assert not domains[i]
            rejected += 1
        else:
            assert all(domains.values())
            assert domains == {i:retained[di] for i,di in result['domains']}
            survived += 1
        if (ri+1)%50 == 0:
            print(f'expanded-arc trace audit: {ri+1}/{len(raw["results"])}',flush=True)
    assert seen == {i for i,r in enumerate(source['results']) if 'domains' in r}
    assert raw['status_counts'].get('rejected',0) == rejected and raw['status_counts'].get('survivor',0) == survived
    output = dict(scope='Explicit-set replay of every reduction trace and rational geometry for each used edge',
                  rejected=rejected,survivors=survived,reductions=reductions,distinct_geometric_edges=edge.cache_info().currsize,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

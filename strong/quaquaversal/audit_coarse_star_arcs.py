"""Explicit-set and rational-geometry replay of conditional coarse patches."""

import argparse
import hashlib
import json
from functools import cache
from pathlib import Path

from geometry import I,ZERO,F,compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_star_arc_filter.json')
    parser.add_argument('--source',type=Path,default=ROOT/'artifacts'/'coarse_refined_frontier.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_star_arc_audit.json')
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/n for n in ('coarse_parent_language.json','coarse_support_domain_audit.json')]
    paths.extend((args.source,args.input))
    coarse,support_audit,frontier,raw = [json.loads(p.read_text()) for p in paths]
    assert support_audit['sources'][paths[0].name] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    assert raw['sources'][args.source.name] == hashlib.sha256(args.source.read_bytes()).hexdigest()
    poses = [raw_pose(p) for p in coarse['poses']]
    identity = I,ZERO,F(1)
    cases = [dict(row) for row in coarse['cases']]
    supports = [set(ss) for ss in coarse['domain_pool']]
    output_pool = [set(ss) for ss in raw['domain_pool']]
    by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    n = coarse['original_stars']
    active = set(range(n))|{by_key[r['boundary_index'],r['cover_index']]
                          for r in frontier['results'] if 'domains' in r}
    assert active == set(raw['initial_active_stars'])

    @cache
    def geometry(x,y,q):
        assert compose(identity if x == -1 else poses[x],poses[q]) == (identity if y == -1 else poses[y])

    reductions = checked = 0
    round_counts = []
    for ri,entry in enumerate(raw['rounds']):
        seen,removed = set(),set()
        for result in entry['results']:
            s = result['star']
            assert s in active and s >= n and s not in seen
            seen.add(s)
            ds = {-1:{s}}
            ds.update({q:supports[di]&active for q,di in cases[s].items()})
            initially_empty = {p for p,ss in ds.items() if not ss}
            for x,y,q in result['reduction_trace']:
                assert x in ds and y in ds
                geometry(x,y,q)
                allowed = {t for t in ds[x] if q in cases[t] and supports[cases[t][q]] & ds[y]}
                assert allowed != ds[x]
                ds[x] = allowed
                reductions += 1
            if 'rejection' in result:
                reason = result['rejection']
                assert not ds[reason['position']]
                if reason['kind'] == 'initial_empty':
                    assert reason['position'] in initially_empty and not result['reduction_trace']
                else:
                    assert reason['kind'] == 'arc_empty' and not initially_empty
                removed.add(s)
            else:
                assert all(ds.values())
                retained = {p:output_pool[di] for p,di in result['domains']}
                assert len(retained) == len(result['domains']) and ds == retained
            checked += 1
        assert seen == active-set(range(n)) and removed == set(entry['removed'])
        if not removed:
            assert ri == len(raw['rounds'])-1
        round_counts.append(len(removed))
        active -= removed
    assert raw['rounds'] and not raw['rounds'][-1]['removed']
    assert active == set(raw['final_active_stars'])
    output = dict(scope='Replay of every conditional coarse-patch rejection and retained domain with exact geometry',
                  initial_extras=len(raw['initial_active_stars'])-n,remaining_extras=len(active)-n,
                  conditional_patches=checked,reductions=reductions,distinct_geometric_edges=geometry.cache_info().currsize,
                  rejection_rounds=round_counts,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

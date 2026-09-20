"""Independently verify the parent-scale adapters and all seed domains."""

import hashlib
import json
from pathlib import Path

from geometry import I,ZERO,F,compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('coarse_parent_language.json','coarse_star_arc_filter_2.json','coarse_star_arc_audit_2.json',
             'coarse_arc_frontier_2.json','coarse_arc_frontier_2_audit.json','coarse_support_domain_audit.json',
             'coarse_expansion_atlas.json','coarse_expansion_rules.json','coarse_expansion_seed.json')
    paths = [ROOT/'artifacts'/n for n in names]
    coarse,filtered,filter_audit,fine,fine_audit,support_audit,atlas,rules,seed = [json.loads(p.read_text()) for p in paths]
    for audit,path in ((filter_audit,paths[1]),(fine_audit,paths[3]),(support_audit,paths[0])):
        assert audit['sources'][path.name] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert atlas['coordinate_level'] == rules['coordinate_level'] == seed['coordinate_level'] == 'parent'
    active = set(filtered['final_active_stars'])
    assert rules['active_stars'] == sorted(active)
    assert [p['pose'] for p in atlas['poses']] == coarse['poses']
    assert seed['poses'][:-1] == coarse['poses']
    assert raw_pose(seed['poses'][-1]) == (I,ZERO,F(1))
    root = len(coarse['poses'])
    assert seed['root_pose_id'] == root
    assert len(rules['cases']) == len(coarse['cases'])
    for s,row in enumerate(rules['cases']):
        assert row == (coarse['cases'][s] if s in active else [])
    assert len(rules['domains']) == len(coarse['domain_pool'])
    for old,new in zip(coarse['domain_pool'],rules['domains'],strict=True):
        assert new['stars'] == sorted(set(old)&active)
    used = {q for s in active for q,di in rules['cases'][s]}
    inverse = {r['pair']:dict(r['entries'])[-1] for r in rules['intersection_maps']}
    poses = [raw_pose(p['pose']) for p in atlas['poses']]
    for q in used:
        assert inverse[q] in used and compose(poses[q],poses[inverse[q]]) == (I,ZERO,F(1))
    by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    frontier = {by_key[r['boundary_index'],r['cover_index']]:(r['boundary_index'],r['cover_index'])
                for r in fine['results'] if 'domains' in r}
    last = {r['star']:r for r in filtered['rounds'][-1]['results']}
    assert not filtered['rounds'][-1]['removed'] and set(last) == set(frontier)
    seen = set()
    checked = 0
    for row in seed['results']:
        s = row['root_star']
        assert s not in seen and s in last
        seen.add(s)
        assert (row['boundary_index'],row['cover_index']) == frontier[s]
        expected = {root if p == -1 else p:filtered['domain_pool'][di] for p,di in last[s]['domains']}
        actual = {p:seed['domain_pool'][di] for p,di in row['domains']}
        assert len(actual) == len(row['domains']) and actual == expected and actual[root] == [s]
        assert all(ss and set(ss) <= active for ss in actual.values())
        checked += len(actual)
    assert seen == set(frontier)
    output = dict(scope='Exact parent-scale pose/rule adapter and complete conditional-domain census',
                  root_cases=len(seen),active_stars=len(active),seed_domain_records=checked,used_inverse_pairs=len(used),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'coarse_expansion_input_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

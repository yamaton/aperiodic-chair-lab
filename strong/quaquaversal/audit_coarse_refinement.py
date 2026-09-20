"""Check coverage, domains and every additional coarse-language rejection."""

import hashlib
import json
from pathlib import Path

from geometry import I,ZERO,F
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_star_compatibility.json','choice_cut_forced_1.json','choice_cut_expanded_arcs_1.json',
             'coarse_parent_language.json','coarse_parent_language_audit.json','coarse_refined_frontier.json')
    paths = [ROOT/'artifacts'/n for n in names]
    compat,source,fine,coarse,coarse_audit,raw = [json.loads(p.read_text()) for p in paths]
    assert coarse_audit['sources'][paths[3].name] == hashlib.sha256(paths[3].read_bytes()).hexdigest()
    assert raw['poses'] == source['poses'] and raw['domain_pool'] == fine['domain_pool']
    assert {r['source_index'] for r in fine['results']} == {i for i,r in enumerate(source['results']) if 'domains' in r}
    maps = {r['pair']:dict(r['entries']) for r in compat['intersection_maps']}
    for q,entries in coarse['added_map_entries']:
        maps.setdefault(q,{}).update(entries)
    poses = [raw_pose(p) for p in coarse['poses']]
    identity = I,ZERO,F(1)
    index = {p:i for i,p in enumerate(poses)}
    inverse = {q:index.get(relative(p,identity)) for q,p in enumerate(poses)}
    stars = [set(s) for s in coarse['stars']]
    star_by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    n = coarse['original_stars']
    active = set(range(n))|{star_by_key[r['boundary_index'],r['cover_index']]
                          for r in fine['results'] if 'domains' in r}
    assert active == set(raw['initial_active_stars'])
    comparisons = 0
    for removed in raw['coarse_removal_rounds']:
        doomed = set()
        for s,q,di in removed:
            assert s in active and s >= n and s not in doomed and q in stars[s]
            inv = inverse[q]
            if inv is not None:
                expected = {maps[q][r] for r in stars[s]|{-1} if r in maps[q]}
                for t in active:
                    if inv in stars[t]:
                        comparisons += 1
                        assert expected != {r for r in stars[t]|{-1} if r in maps[inv]}
            doomed.add(s)
        active -= doomed
    assert active == set(raw['final_active_stars'])
    seen = set()
    counts = dict(survivor=0,fine_rejection=0,coarse_rejection=0)
    for row in raw['results']:
        i = row['source_index']
        assert i not in seen
        seen.add(i)
        old = fine['results'][i]
        key = old['boundary_index'],old['cover_index']
        assert key == (row['boundary_index'],row['cover_index'])
        assert row['forced_source_index'] == old['source_index']
        star = star_by_key[key]
        if 'domains' not in old:
            assert row['rejection'] == dict(kind='fine_arc_trace',result_index=i)
            counts['fine_rejection'] += 1
        elif star not in active:
            assert row['rejection'] == dict(kind='coarse_star_support',star=star)
            counts['coarse_rejection'] += 1
        else:
            assert row['domains'] == old['domains']
            counts['survivor'] += 1
    assert seen == set(range(len(fine['results']))) and counts == raw['status_counts']
    output = dict(scope='Full-frontier coverage and retained-domain audit with exhaustive support checks for coarse rejections',
                  **counts,explicit_target_comparisons=comparisons,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'coarse_refinement_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

"""Audit coarse-star exclusions without trusting the producer's buckets.

Check each added rational fingerprint relation and inverse reciprocity.
For every elimination, explicitly compare against EVERY still-live target
star containing the inverse neighbor. This verifies no target was omitted
from a stored support domain. The remaining vocabulary is not a tiling.
"""

import hashlib
import json
from pathlib import Path

from geometry import I,ZERO,F
from contact_atlas import relative
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points,dimension

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'parent_boundary_cover_arcs.json','choice_cut_forced_1.json','coarse_parent_language.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,boundary,frontier,raw = [json.loads(p.read_text()) for p in paths]
    identity = I,ZERO,F(1)
    poses = [raw_pose(p) for p in raw['poses']]
    assert poses[:len(atlas_raw['poses'])] == [raw_pose(p['pose']) for p in atlas_raw['poses']]
    index = {p:i for i,p in enumerate(poses)}
    index[identity] = -1
    for p in poses[len(atlas_raw['poses']):]:
        assert dimension(edge_points(p)) in (0,1,2)
    maps = {r['pair']:dict(r['entries']) for r in compat['intersection_maps']}
    added = 0
    for q,entries in raw['added_map_entries']:
        row = maps.setdefault(q,{})
        for r,s in entries:
            assert r not in row
            assert relative(poses[q],identity if r == -1 else poses[r]) == (identity if s == -1 else poses[s])
            row[r] = s
            added += 1
    inverses = {q:index.get(relative(p,identity)) for q,p in enumerate(poses)}
    reciprocal = 0
    for q,row in maps.items():
        if inverses[q] is None:
            continue
        for r,s in row.items():
            assert maps[inverses[q]].get(s) == r
            reciprocal += 1
    stars = [set(s) for s in raw['stars']]
    n = len(language['stars'])
    assert raw['original_stars'] == n
    assert stars[:n] == [set(s['neighbors']) for s in language['stars']]
    records = {c['source_index']:c for c in raw['cover_stars']}
    assert set(records) == {i for i,r in enumerate(frontier['results']) if 'domains' in r}
    accounted = set(range(n))
    for i,c in records.items():
        row = frontier['results'][i]
        assert (c['boundary_index'],c['cover_index']) == (row['boundary_index'],row['cover_index'])
        cover = boundary['results'][row['boundary_index']]['covers'][row['cover_index']]
        actual = {index[raw_pose(boundary['parents'][p])] for p in cover['parents']}
        assert stars[c['star']] == actual
        accounted.add(c['star'])
    assert accounted == set(range(len(stars)))
    active = set(accounted)
    compared = 0
    for removed in raw['removal_rounds']:
        doomed = set()
        for s,q,di in removed:
            assert s in active and s >= n and s not in doomed and q in stars[s]
            inverse = inverses[q]
            if inverse is not None:
                visible = {maps[q][r] for r in stars[s]|{-1} if r in maps[q]}
                for t in active:
                    if inverse not in stars[t]:
                        continue
                    compared += 1
                    candidate = {r for r in stars[t]|{-1} if r in maps[inverse]}
                    assert visible != candidate,(s,q,t)
            doomed.add(s)
        active -= doomed
    assert active == set(raw['surviving_stars'])
    sibling_sets = [set(s) for s in language['sibling_neighbors']]
    assert raw['child_roles'] == [[i for i,ss in enumerate(sibling_sets) if ss <= star] for star in stars]
    output = dict(scope='Exact fingerprint relations and exhaustive live-target comparisons for every coarse-star exclusion',
                  original_stars=n,extra_stars=len(stars)-n,extra_rejections=len(stars)-len(active),
                  extra_survivors=len(active)-n,added_geometric_entries=added,reciprocal_entries=reciprocal,
                  explicit_target_comparisons=compared,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',ROOT/'audit_closed_atlas.py',
                            *paths,Path(__file__))})
    (ROOT/'artifacts'/'coarse_parent_language_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

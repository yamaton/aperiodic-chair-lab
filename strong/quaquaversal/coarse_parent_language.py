"""Q027: necessary star compatibility directly on candidate parent tilings.

A child tiling's recognized parent stars lie in the original language plus
the surviving nonlanguage covers. Prune this enlarged finite vocabulary
when a star has no possible neighbor star. This is a necessary language
filter; survival does not prove global realizability or closure under parents.
"""

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from geometry import I,ZERO,F,compose,encode
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'parent_boundary_cover_arcs.json','choice_cut_forced_1.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,boundary,frontier = [json.loads(p.read_text()) for p in paths]
    poses = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    index = {p:i for i,p in enumerate(poses)}
    parent_ids = []
    for raw in boundary['parents']:
        p = raw_pose(raw)
        if p not in index:
            index[p] = len(poses)
            poses.append(p)
        parent_ids.append(index[p])
    identity = I,ZERO,F(1)
    index[identity] = -1
    stars = [tuple(s['neighbors']) for s in language['stars']]
    star_index = {s:i for i,s in enumerate(stars)}
    covers = []
    for si,row in enumerate(frontier['results']):
        if 'domains' not in row:
            continue
        cover = boundary['results'][row['boundary_index']]['covers'][row['cover_index']]
        star = tuple(sorted(parent_ids[p] for p in cover['parents']))
        if star not in star_index:
            star_index[star] = len(stars)
            stars.append(star)
        covers.append(dict(source_index=si,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                           star=star_index[star]))
    old_count = len(atlas_raw['poses'])
    maps = {r['pair']:dict(r['entries']) for r in compat['intersection_maps']}
    old_maps = {q:dict(m) for q,m in maps.items()}
    for q in range(len(poses)):
        if q >= old_count:
            maps[q] = {r:index[p] for r,pose in enumerate(poses) if (p:=relative(poses[q],pose)) in index}
            if (p:=relative(poses[q],identity)) in index:
                maps[q][-1] = index[p]
        else:
            for r in range(old_count,len(poses)):
                p = relative(poses[q],poses[r])
                if p in index:
                    maps[q][r] = index[p]
            for target in range(old_count,len(poses)):
                p = compose(poses[q],poses[target])
                if p in index:
                    maps[q][index[p]] = target
    inverses = {q:index.get(relative(p,identity)) for q,p in enumerate(poses)}
    buckets = defaultdict(list)
    for si,star in enumerate(stars):
        for q in star:
            fingerprint = tuple(sorted(r for r in (*star,-1) if r in maps[q]))
            buckets[q,fingerprint].append(si)
    pool,ids,cases = [],{},[]
    for si,star in enumerate(stars):
        row = []
        for q in star:
            if inverses[q] is None:
                allowed = ()
            else:
                fingerprint = tuple(sorted(maps[q][r] for r in (*star,-1) if r in maps[q]))
                allowed = tuple(buckets[inverses[q],fingerprint])
            if allowed not in ids:
                ids[allowed] = len(pool)
                pool.append(allowed)
            row.append((q,ids[allowed]))
        cases.append(row)
    active = set(range(len(stars)))
    rounds = []
    while True:
        removed = []
        for s in sorted(active):
            for q,di in cases[s]:
                if not active.intersection(pool[di]):
                    removed.append((s,q,di))
                    break
        if not removed:
            break
        assert all(s >= len(language['stars']) for s,q,di in removed)
        rounds.append(removed)
        active.difference_update(s for s,q,di in removed)
    sibling_sets = [set(s) for s in language['sibling_neighbors']]
    roles = [[i for i,sibs in enumerate(sibling_sets) if sibs <= set(s)] for s in stars]
    output = dict(scope='Necessary neighbor-star pruning in a finite overapproximation of recognized parent stars',
                  poses=poses,stars=stars,original_stars=len(language['stars']),cover_stars=covers,
                  added_map_entries=[[q,[[r,s] for r,s in sorted(m.items()) if r not in old_maps.get(q,{})]] for q,m in maps.items()
                                     if any(r not in old_maps.get(q,{}) for r in m)],
                  domain_pool=pool,cases=cases,removal_rounds=rounds,surviving_stars=sorted(active),
                  child_roles=roles,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'coarse_parent_language.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(parent_cases=len(covers),extra_stars=len(stars)-len(language['stars']),
                          extra_survivors=len(active)-len(language['stars']),rounds=[len(r) for r in rounds],
                          role_counts=dict(Counter(len(r) for r in roles)))),flush=True)


if __name__ == '__main__':
    main()

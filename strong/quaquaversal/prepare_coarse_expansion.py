"""Q032: explicit parent-scale atlas, rules and conditional-patch seed.

World poses here have scale 1. Their IDs are NOT fine-world IDs and must
never be used with the fine choice-cut catalog. Star IDs remain indices in
the 7,075-star vocabulary; supports are restricted to the audited live set.
"""

import hashlib
import json
from pathlib import Path

from geometry import I,ZERO,F,encode
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_star_compatibility.json','coarse_parent_language.json','coarse_support_domain_audit.json',
             'coarse_star_arc_filter_2.json','coarse_star_arc_audit_2.json',
             'coarse_arc_frontier_2.json','coarse_arc_frontier_2_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    base,coarse,support_audit,filtered,filter_audit,fine,fine_audit = [json.loads(p.read_text()) for p in paths]
    for audit,path in ((support_audit,paths[1]),(filter_audit,paths[3]),(fine_audit,paths[5])):
        assert audit['sources'][path.name] == hashlib.sha256(path.read_bytes()).hexdigest()
    active = set(filtered['final_active_stars'])
    by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    keys = {by_key[r['boundary_index'],r['cover_index']]:(r['boundary_index'],r['cover_index'])
            for r in fine['results'] if 'domains' in r}
    assert set(keys) == active-set(range(coarse['original_stars']))
    supports = [sorted(set(ss)&active) for ss in coarse['domain_pool']]
    cases = [row if s in active else [] for s,row in enumerate(coarse['cases'])]
    assert all(supports[di] for s in active for q,di in cases[s])
    maps = {r['pair']:dict(r['entries']) for r in base['intersection_maps']}
    for q,entries in coarse['added_map_entries']:
        maps.setdefault(q,{}).update(entries)
    used_pairs = {q for s in active for q,di in cases[s]}
    assert all(-1 in maps[q] and maps[q][-1] in used_pairs for q in used_pairs)
    poses = [raw_pose(p) for p in coarse['poses']]
    assert all(p[2] == 1 for p in poses)
    identity = I,ZERO,F(1)
    assert identity not in poses
    root = len(poses)
    world = poses+[identity]
    last = filtered['rounds'][-1]
    assert not last['removed']
    pool,ids,results = [],{},[]
    for row in last['results']:
        s = row['star']
        assert 'domains' in row and s in keys
        domains = []
        for p,di in row['domains']:
            ss = tuple(filtered['domain_pool'][di])
            assert ss and set(ss) <= active
            if ss not in ids:
                ids[ss] = len(pool)
                pool.append(ss)
            domains.append((root if p == -1 else p,ids[ss]))
        initial = dict(domains)
        assert pool[initial[root]] == (s,)
        bi,ci = keys[s]
        results.append(dict(source_index=len(results),root_star=s,boundary_index=bi,cover_index=ci,
                            domains=sorted(domains)))
    assert {r['root_star'] for r in results} == set(keys)
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
               (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))}
    atlas = dict(scope='Parent-scale closed-contact vocabulary adapter',coordinate_level='parent',
                 poses=[dict(pose=p) for p in poses],sources=sources)
    rules = dict(scope='Audited coarse compatibility restricted to the current complete live vocabulary',
                 coordinate_level='parent',active_stars=sorted(active),cases=cases,
                 domains=[dict(stars=ss) for ss in supports],
                 intersection_maps=[dict(pair=q,entries=sorted(m.items())) for q,m in sorted(maps.items()) if -1 in m],
                 sources=sources)
    seed = dict(scope='Full extra-parent-star frontier as conditional parent-scale patches',coordinate_level='parent',
                root_pose_id=root,poses=world,domain_pool=pool,results=results,
                status_counts=dict(survivor=len(results)),sources=sources)
    for filename,data in (('coarse_expansion_atlas.json',atlas),('coarse_expansion_rules.json',rules),
                          ('coarse_expansion_seed.json',seed)):
        (ROOT/'artifacts'/filename).write_text(json.dumps(encode(data),separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),active_stars=len(active),world_positions=len(world),
                          domains=len(pool),used_pairs=len(used_pairs))),flush=True)


if __name__ == '__main__':
    main()

"""Replay the Q012 external-domain filter with set intersections.

Check geometric placement of each requirement, exhaustive tuple accounting,
every rejected conflict, and every retained domain trace. This does not
prove that surviving domains can be realized simultaneously.
"""

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from geometry import child_maps,compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_audit.json','closed_star_compatibility.json',
              'parent_join_filter.json','parent_external_domains.json')]
    atlas_raw,audit,compat,joined,raw = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    children = [p for _,p in child_maps()]
    poses = [raw_pose(p) for p in raw['poses']]
    assert poses[:8] == children and len(set(poses)) == len(poses)
    for si,(case,requirements) in enumerate(zip(compat['cases'],raw['requirements'],strict=True)):
        role, = audit['child_roles'][si]
        assert len(case) == len(requirements)
        for (q,di),(tile,dj) in zip(case,requirements,strict=True):
            assert di == dj and poses[tile] == compose(children[role],atlas[q])
    domains = [set(d['stars']) for d in compat['domains']]
    rejected = {e['tuple_index']:e for e in raw['rejections']}
    survived = {e['tuple_index']:e for e in raw['survivors']}
    assert len(rejected) == len(raw['rejections']) and len(survived) == len(raw['survivors'])
    assert not set(rejected) & set(survived)
    assert set(rejected)|set(survived) == set(range(len(joined['survivors'])))
    checked = 0
    for ti,t in enumerate(joined['survivors']):
        constraints = defaultdict(list)
        for s in t:
            for tile,di in raw['requirements'][s]:
                constraints[tile].append(di)
        if ti in rejected:
            c = rejected[ti]['conflict']
            tile = c['tile']
            assert c['domains'] == constraints[tile][:len(c['domains'])]
            value = set.intersection(*(domains[di] for di in c['domains']))
            if tile < 8:
                value &= {t[tile]}
            assert not value
            checked += 1
        else:
            stored = {d['tile']:d['domains'] for d in survived[ti]['external_domains']}
            assert stored == {k:v for k,v in constraints.items() if k >= 8}
            for tile,ids in constraints.items():
                value = set.intersection(*(domains[di] for di in ids))
                if tile < 8:
                    value &= {t[tile]}
                assert value
                checked += 1
    output = dict(scope='Geometry and set-intersection replay of external closed-star domains',
                  tuples=len(joined['survivors']),rejected=len(rejected),survivors=len(survived),
                  domain_intersections_checked=checked,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_external_domains_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

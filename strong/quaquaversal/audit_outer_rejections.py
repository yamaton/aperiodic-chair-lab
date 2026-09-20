"""Replay every Q014 empty-domain witness with explicit sets and geometry.

This audit covers rejections, not simultaneous realizability of survivors.
No source-domain choice is replaced by an arbitrary selected star.
"""

import hashlib
import json
from functools import cache
from pathlib import Path

from geometry import compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_compatibility.json',
              'parent_cover_star_constraints.json','forced_outer_layer.json')]
    atlas_raw,compat,source,raw = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in raw['poses']]
    assert len(poses) == len(set(poses))
    cases = [dict(row) for row in compat['cases']]
    @cache
    def allowed(di,q):
        choices = source['domain_pool'][di]
        assert all(q in cases[s] for s in choices)
        return frozenset(s for parent in choices for s in compat['domains'][cases[parent][q]]['stars'])
    checked = 0
    requirements = 0
    for result in raw['results']:
        if 'rejection' not in result:
            continue
        origin = source['results'][result['source_index']]
        assert 'domains' in origin
        assert (result['boundary_index'],result['cover_index']) == (origin['boundary_index'],origin['cover_index'])
        initial = dict(origin['domains'])
        failure = result['rejection']
        target = failure['tile']
        constraints = []
        for reason in failure['requirements']:
            di = reason['domain']
            if reason['kind'] == 'initial_domain':
                assert initial[target] == di
                constraints.append(set(source['domain_pool'][di]))
            else:
                tile,q = reason['tile'],reason['pair']
                assert initial[tile] == di
                assert compose(poses[tile],atlas[q]) == poses[target]
                constraints.append(set(allowed(di,q)))
            requirements += 1
        assert constraints and not set.intersection(*constraints)
        checked += 1
    assert checked == raw['status_counts']['rejected']
    output = dict(scope='Independent explicit-set and exact-placement replay of Q014 rejection witnesses only',
                  rejected_covers_checked=checked,requirements_checked=requirements,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'outer_rejection_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

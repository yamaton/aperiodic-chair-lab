"""Verify that the pilot branches exhaust their original two-choice domains.

Combine the two necessary pilot tests and compare with the unbranched
forced layer. A branch contradiction excludes a parent only when every
branch for that parent is contradicted.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('expanded_arc_seed.json','branch_probe_seed.json','branch_probe_layer_1.json',
              'branch_probe_arcs.json','forced_after_arcs_1.json')]
    original,seed,layer,arcs,baseline = [json.loads(p.read_text()) for p in paths]
    assert seed['poses'] == original['poses']
    layer_result = {r['source_index']:r for r in layer['results']}
    arc_result = {r['source_index']:r for r in arcs['results']}
    baseline_result = {r['source_index']:r for r in baseline['results']}
    assert set(layer_result) == set(arc_result) == set(range(len(seed['results'])))
    groups = []
    used = set()
    for group in seed['branch_groups']:
        si,tile = group['original_source_index'],group['tile']
        origin = original['results'][si]
        initial = {i:set(original['domain_pool'][d]) for i,d in origin['domains']}
        assert len(initial[tile]) == 2
        choices = set()
        live = []
        for bi in group['branch_records']:
            assert bi not in used
            used.add(bi)
            branch = seed['results'][bi]
            assert branch['source_index'] == si and branch['branch_tile'] == tile
            assert (branch['boundary_index'],branch['cover_index']) == (origin['boundary_index'],origin['cover_index'])
            selected = branch['branch_star']
            choices.add(selected)
            domains = {i:set(seed['domain_pool'][d]) for i,d in branch['domains']}
            expected = dict(initial)
            expected[tile] = {selected}
            assert domains == expected
            if 'domains' in layer_result[bi] and 'domains' in arc_result[bi]:
                live.append(bi)
        assert choices == initial[tile]
        excluded = not live
        already_excluded = 'domains' not in baseline_result[si]
        groups.append(dict(original_source_index=si,surviving_branches=live,
                           parent_excluded=excluded,already_excluded_without_branching=already_excluded))
    assert used == set(range(len(seed['results'])))
    output = dict(scope='Exhaustive binary split and finite outcome audit; surviving branches do not prove extension',
                  groups=groups,parent_cases=len(groups),branches=len(used),
                  additional_parent_exclusions=sum(g['parent_excluded'] and not g['already_excluded_without_branching'] for g in groups),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'branch_probe_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output|{'sources':'omitted'}),flush=True)


if __name__ == '__main__':
    main()

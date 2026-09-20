"""Q022: lift audited optional-neighbor arc failures to original choice cuts.

Backward-slice each failed reduction trace. Reconstruct the initial domains
from selected center stars using Fraction geometry, then greedily remove
antecedents while retaining a replayable empty-domain proof. Every vertex
used in the proof must still be forced present by a remaining antecedent.
No SAT UNSAT flag is used and these are not parent-case exclusions.
"""

import hashlib
import json
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

from geometry import compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json', 'closed_star_language.json', 'closed_star_compatibility.json',
             'expanded_arcs_2_seed.json', 'neighbor_star_cut_sat.json', 'neighbor_star_cut_seed.json',
             'neighbor_star_cut_layer_1.json', 'neighbor_star_cut_arcs.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw, language, compat, original, sat, seed, layer, arcs = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in layer['poses']]
    assert layer['poses'][:len(seed['poses'])] == seed['poses'] == original['poses']
    cases = [dict(row) for row in compat['cases']]
    domains = [set(row['stars']) for row in compat['domains']]
    universe = set(range(len(language['stars'])))
    cuts = []
    for result in arcs['results']:
        if 'rejection' not in result:
            continue
        model_index = result['source_index']
        model = sat['results'][model_index]
        selected = dict(model['selected_stars'])
        assert {tile: seed['domain_pool'][di][0] for tile,di in seed['results'][model_index]['domains']} == selected
        target = result['rejection']['tiles'][0]
        needed = {target}
        trace = []
        for x,y,q in reversed(result['reduction_trace']):
            if x in needed:
                needed.add(y)
                trace.append((x,y,q))
        trace.reverse()
        assert trace and trace[-1][0] == target
        for x,y,q in trace:
            assert compose(poses[x],atlas[q]) == poses[y]
        lookup = {poses[t]:t for t in needed}
        requirements = defaultdict(list)
        # Only the small backward slice is indexed. No assumption is made
        # about the existence of other optional positions.
        for tile,star in selected.items():
            if tile in needed:
                requirements[tile].append(dict(tile=tile,star=star,kind='selected_center'))
            for q in language['stars'][star]['neighbors']:
                pose = compose(poses[tile],atlas[q])
                if pose in lookup:
                    requirements[lookup[pose]].append(dict(tile=tile,star=star,kind='neighbor',pair=q))
        assert set(requirements) == needed
        initial_domains = dict(layer['results'][model_index]['domains'])

        def options(reason):
            if reason['kind'] == 'selected_center':
                return {reason['star']}
            return domains[cases[reason['star']][reason['pair']]]

        def replay(antecedents):
            ds = {}
            for tile,reasons in requirements.items():
                rs = [r for r in reasons if (r['tile'],r['star']) in antecedents]
                if not rs:
                    return False  # This proof would no longer force the tile.
                ds[tile] = set.intersection(*(options(r) for r in rs))
            for x,y,q in trace:
                ds[x] = {s for s in ds[x] if q in cases[s] and domains[cases[s][q]] & ds[y]}
            return not ds[target]

        for tile,reasons in requirements.items():
            assert set.intersection(*(options(r) for r in reasons)) == set(layer['domain_pool'][initial_domains[tile]])
        antecedents = {(r['tile'],r['star']) for rs in requirements.values() for r in rs}
        assert replay(antecedents)
        before = len(antecedents)
        for choice in sorted(antecedents):
            if replay(antecedents-{choice}):
                antecedents.remove(choice)
        assert replay(antecedents)
        original_domains = dict(original['results'][model['source_index']]['domains'])
        for tile,star in antecedents:
            assert star in original['domain_pool'][original_domains[tile]]
        fixed = all(original['domain_pool'][original_domains[tile]] == [star] for tile,star in antecedents)
        cut = dict(model_index=model_index,source_index=model['source_index'],
                   boundary_index=model['boundary_index'],cover_index=model['cover_index'],
                   antecedents=sorted(antecedents),unminimized_choices=before,
                   target=target,reduction_trace=trace,
                   requirements=[[tile,[r for r in rs if (r['tile'],r['star']) in antecedents]]
                                 for tile,rs in sorted(requirements.items())],
                   excludes_parent_without_new_choices=fixed)
        cuts.append(cut)
        print(json.dumps(dict(model=model_index,trace_steps=len(trace),proof_tiles=len(needed),
                              initial_choices=before,cut_choices=len(antecedents))),flush=True)
    output = dict(scope='Exact geometric and explicit-set proofs of forbidden center-choice conjunctions from arc failures',
                  cuts=cuts,assignment_rejections=len(cuts),
                  direct_parent_exclusions=sum(c['excludes_parent_without_new_choices'] for c in cuts),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'neighbor_arc_cuts.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cuts=len(cuts),lengths=dict(Counter(len(c['antecedents']) for c in cuts)),
                          direct_parent_exclusions=output['direct_parent_exclusions'])),flush=True)


if __name__ == '__main__':
    main()

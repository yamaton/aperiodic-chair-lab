"""Q020: audit empty neighbor-star domains and extract valid SAT cuts.

Each cut forbids a conjunction of selected center stars. The geometric
placement and compatibility-set intersection are checked independently.
An assignment rejection is not a parent exclusion unless all antecedents
were already fixed in the original parent-domain problem.
"""

import hashlib
import json
from pathlib import Path

from geometry import compose,encode
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'expanded_arcs_2_seed.json','neighbor_incidence_geometry_sat.json',
             'incidence_model_star_seed.json','incidence_model_star_extension.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,original,sat,seed,raw = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in raw['poses']]
    assert raw['poses'][:len(seed['poses'])] == seed['poses'] == original['poses']
    case_maps = [dict(row) for row in compat['cases']]
    cuts = []
    for result in raw['results']:
        if 'rejection' not in result:
            continue
        seed_row = seed['results'][result['source_index']]
        initial = dict(seed_row['domains'])
        model = sat['results'][seed_row['model_index']]
        selected = dict(model['selected_stars'])
        original_row = original['results'][model['source_index']]
        original_domains = dict(original_row['domains'])
        target = result['rejection']['tile']
        constraints = []
        for reason in result['rejection']['requirements']:
            tile = target if reason['kind'] == 'initial_domain' else reason['tile']
            di = reason['domain']
            assert initial[tile] == di and len(seed['domain_pool'][di]) == 1
            star, = seed['domain_pool'][di]
            assert selected[tile] == star
            assert star in original['domain_pool'][original_domains[tile]]
            if reason['kind'] == 'initial_domain':
                options = {star}
            else:
                q = reason['pair']
                assert q in language['stars'][star]['neighbors']
                assert compose(poses[tile],atlas[q]) == poses[target]
                options = set(compat['domains'][case_maps[star][q]]['stars'])
            constraints.append(dict(tile=tile,star=star,reason=reason,options=options))
        assert constraints and not set.intersection(*(c['options'] for c in constraints))
        # Greedy deletion makes the witnessed conjunction smaller without
        # asserting global minimum size or changing the necessity argument.
        cursor = 0
        while cursor < len(constraints) and len(constraints) > 1:
            smaller = constraints[:cursor]+constraints[cursor+1:]
            if not set.intersection(*(c['options'] for c in smaller)):
                constraints = smaller
            else:
                cursor += 1
        antecedents = sorted({(c['tile'],c['star']) for c in constraints})
        fixed = all(original['domain_pool'][original_domains[tile]] == [star] for tile,star in antecedents)
        cuts.append(dict(model_index=seed_row['model_index'],source_index=model['source_index'],
                         boundary_index=model['boundary_index'],cover_index=model['cover_index'],target_pose=poses[target],
                         antecedents=antecedents,excludes_parent_without_new_choices=fixed,
                         witnesses=[{k:(sorted(v) if k == 'options' else v) for k,v in c.items()} for c in constraints]))
    assert len(cuts) == raw['status_counts'].get('rejected',0)
    output = dict(scope='Verified necessary forbidden conjunctions of center-star choices; not full SAT unsatisfiability proofs',
                  cuts=cuts,assignment_rejections=len(cuts),
                  direct_parent_exclusions=sum(c['excludes_parent_without_new_choices'] for c in cuts),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'incidence_star_cuts.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(assignment_rejections=len(cuts),direct_parent_exclusions=output['direct_parent_exclusions'],
                          clause_lengths=[len(c['antecedents']) for c in cuts])),flush=True)


if __name__ == '__main__':
    main()

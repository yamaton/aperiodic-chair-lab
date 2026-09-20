"""Independently audit Q021 cuts with Fraction poses and explicit star sets.

Also freeze the final assignments for deeper extension tests. Satisfying
assignments and choice cuts do not exclude the original parent cases.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import F, compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json', 'closed_star_language.json',
             'closed_star_compatibility.json', 'expanded_arcs_2_seed.json',
             'incidence_star_cuts.json', 'neighbor_star_cut_sat.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw, language, compat, source, initial, raw = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in source['poses']]
    cases = [dict(row) for row in compat['cases']]
    denominator, scale = raw['pose_key_denominator'], F(raw['tile_scale'])

    def position(i):
        key = raw['normalized_pose_keys'][i]
        return (tuple(tuple(F(key[3*j+k], denominator) for k in range(3)) for j in range(3)),
                tuple(scale*F(v, denominator) for v in key[9:]), scale)

    lengths = Counter()
    placements = direct_exclusions = 0
    for cut in raw['cuts']:
        origin = cut['origin']
        lengths[len(cut['antecedents'])] += 1
        if origin['kind'] == 'audited_initial':
            assert cut['antecedents'] == initial['cuts'][origin['index']]['antecedents']
            continue
        assert origin['kind'] == 'empty_neighbor_domain'
        model = raw['results'][origin['case']]
        allowed = dict(source['results'][model['source_index']]['domains'])
        target = position(origin['position'])
        options, choices = [], set()
        for reason in origin['requirements']:
            tile, star = reason['tile'], reason['star']
            assert star in source['domain_pool'][allowed[tile]]
            choices.add((tile, star))
            if reason['kind'] == 'selected_center':
                assert poses[tile] == target
                options.append({star})
            else:
                assert reason['kind'] == 'neighbor'
                q = reason['pair']
                assert q in language['stars'][star]['neighbors']
                assert compose(poses[tile], atlas[q]) == target
                placements += 1
                di = cases[star][q]
                assert di == reason['domain']
                options.append(set(compat['domains'][di]['stars']))
        assert sorted(choices) == [tuple(a) for a in cut['antecedents']]
        assert options and not set.intersection(*options)
        direct_exclusions += all(source['domain_pool'][allowed[t]] == [s] for t, s in choices)

    pool, ids, results = [], {}, []
    for mi, model in enumerate(raw['results']):
        assert model['status'] == 'sat_passes_neighbor_star_test'
        origin = source['results'][model['source_index']]
        allowed = dict(origin['domains'])
        selected = dict(model['selected_stars'])
        assert len(selected) == len(model['selected_stars']) and set(selected) == set(allowed)
        domains = []
        for tile, star in selected.items():
            assert star in source['domain_pool'][allowed[tile]]
            if star not in ids:
                ids[star] = len(pool)
                pool.append([star])
            domains.append((tile, ids[star]))
        for ki in model['installed_cut_indices']:
            assert not all(selected.get(t) == s for t, s in raw['cuts'][ki]['antecedents'])
        results.append(dict(source_index=mi, model_index=mi,
                            boundary_index=origin['boundary_index'], cover_index=origin['cover_index'], domains=domains))
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
               (ROOT/'geometry.py', ROOT/'reflected_controls.py', *paths, Path(__file__))}
    audit = dict(scope='Exact necessary-cut audit and membership check of final finite assignments; not a tiling certificate',
                 inherited_cuts=len(initial['cuts']), new_cuts=len(raw['cuts'])-len(initial['cuts']),
                 cut_lengths=dict(lengths), exact_placements=placements,
                 direct_parent_exclusions=direct_exclusions, frozen_assignments=len(results), sources=sources)
    (ROOT/'artifacts'/'neighbor_star_cut_audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    seed = dict(scope='Final Q021 chosen stars as hypotheses for deeper complete-star extension',
                poses=source['poses'], domain_pool=pool, results=results, sources=sources)
    (ROOT/'artifacts'/'neighbor_star_cut_seed.json').write_text(json.dumps(seed, separators=(',', ':'))+'\n')
    print(json.dumps({k:v for k,v in audit.items() if k != 'sources'}), flush=True)


if __name__ == '__main__':
    main()

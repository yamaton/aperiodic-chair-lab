"""Independent exact replay of Q023 learned cuts, without SAT or bitsets.

Freeze only final assignments reported to pass the finite arc test for
separate full-domain auditing. A finite-limit result stays unknown.
"""

import hashlib
import json
from collections import Counter
from functools import cache
from pathlib import Path

from geometry import F, compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'expanded_arcs_2_seed.json','neighbor_star_cut_sat.json','neighbor_arc_cuts.json',
             'neighbor_arc_cut_sat.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,source,old_stars,old_arcs,raw = [json.loads(p.read_text()) for p in paths]
    inherited = {paths[4].name:old_stars,paths[5].name:old_arcs}
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    cases = [dict(row) for row in compat['cases']]
    options = [set(row['stars']) for row in compat['domains']]
    scale,denom = F(raw['tile_scale']),raw['pose_key_denominator']

    @cache
    def center(tile):
        return raw_pose(source['poses'][tile])

    @cache
    def position(pos):
        key = raw['normalized_pose_keys'][pos]
        return (tuple(tuple(F(key[3*i+j],denom) for j in range(3)) for i in range(3)),
                tuple(scale*F(v,denom) for v in key[9:]),scale)

    placements = steps = direct = 0
    kinds,lengths = Counter(),Counter()
    for cut in raw['cuts']:
        origin = cut['origin']
        kind = origin['kind']
        kinds[kind] += 1
        lengths[len(cut['antecedents'])] += 1
        if kind == 'audited_initial':
            assert cut['antecedents'] == inherited[origin['file']]['cuts'][origin['index']]['antecedents']
            continue
        model = raw['results'][origin['case']]
        allowed = dict(source['results'][model['source_index']]['domains'])
        hypotheses = {tuple(a) for a in cut['antecedents']}
        assert hypotheses and len(hypotheses) == len(cut['antecedents'])
        for tile,star in hypotheses:
            assert star in source['domain_pool'][allowed[tile]]
        direct += all(source['domain_pool'][allowed[t]] == [s] for t,s in hypotheses)
        requirements = ([(origin['position'],origin['requirements'])] if kind == 'empty_neighbor_domain'
                        else origin['requirements'])
        assert kind in ('empty_neighbor_domain','neighbor_arc_failure')
        ds,referenced = {},set()
        for target,reasons in requirements:
            assert target not in ds and reasons
            sets = []
            for r in reasons:
                tile,star = r['tile'],r['star']
                assert (tile,star) in hypotheses
                referenced.add((tile,star))
                if r['kind'] == 'selected_center':
                    assert center(tile) == position(target)
                    sets.append({star})
                else:
                    assert r['kind'] == 'neighbor'
                    q = r['pair']
                    assert q in language['stars'][star]['neighbors']
                    assert compose(center(tile),atlas[q]) == position(target)
                    placements += 1
                    assert r['domain'] == cases[star][q]
                    sets.append(options[cases[star][q]])
            ds[target] = set.intersection(*sets)
        assert hypotheses == referenced
        if kind == 'neighbor_arc_failure':
            for x,y,q in origin['reduction_trace']:
                assert x in ds and y in ds
                assert compose(position(x),atlas[q]) == position(y)
                placements += 1
                ds[x] = {s for s in ds[x] if q in cases[s] and options[cases[s][q]] & ds[y]}
                steps += 1
        target = origin['position'] if kind == 'empty_neighbor_domain' else origin['target']
        assert not ds[target]
    pool,ids,results = [],{},[]
    for mi,model in enumerate(raw['results']):
        if model['status'] != 'sat_passes_neighbor_arc_test':
            continue
        selected = dict(model['selected_stars'])
        original = source['results'][model['source_index']]
        allowed = dict(original['domains'])
        assert len(selected) == len(model['selected_stars']) and set(selected) == set(allowed)
        domains = []
        for tile,star in selected.items():
            assert star in source['domain_pool'][allowed[tile]]
            if star not in ids:
                ids[star] = len(pool)
                pool.append([star])
            domains.append((tile,ids[star]))
        for ki in model['installed_cut_indices']:
            assert not all(selected.get(t) == s for t,s in raw['cuts'][ki]['antecedents'])
        results.append(dict(source_index=mi,model_index=mi,boundary_index=original['boundary_index'],
                            cover_index=original['cover_index'],domains=domains))
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
               (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))}
    output = dict(scope='Exact replay of necessary Q023 choice cuts, not UNSAT or infinite-extension certification',
                  cut_kinds=dict(kinds),cut_lengths=dict(lengths),exact_placements=placements,arc_steps=steps,
                  direct_parent_exclusions=direct,frozen_assignments=len(results),sources=sources)
    (ROOT/'artifacts'/'neighbor_arc_sat_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    seed = dict(scope='Selected Q023 finite models as hypotheses for independent deeper extension',
                poses=source['poses'],domain_pool=pool,results=results,sources=sources)
    (ROOT/'artifacts'/'neighbor_arc_sat_seed.json').write_text(json.dumps(seed,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

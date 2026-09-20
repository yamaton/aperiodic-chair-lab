"""Standalone exact checker for choice/neighbor/meet/arc contradiction DAGs.

The checker uses only the certificate, prism geometry and audited star
compatibility data. It does not execute the extraction or pruning searches.
Presence is essential: an unconstrained optional position is not a domain.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'expanded_arcs_2_seed.json','neighbor_star_cut_layer_2.json','layered_choice_certificate.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,original,layer,proof = [json.loads(p.read_text()) for p in paths]
    assert layer['poses'][:len(original['poses'])] == original['poses']
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    cases = [dict(row) for row in compat['cases']]
    allowed = [set(row['stars']) for row in compat['domains']]
    poses = {n['pose']:raw_pose(layer['poses'][n['pose']]) for n in proof['nodes']}
    hypotheses = {tuple(a) for a in proof['antecedents']}
    assert len(hypotheses) == len(proof['antecedents']) and hypotheses
    selected_nodes = {(n['tile'],n['star']) for n in proof['nodes'] if n['op'] == 'choice'}
    assert hypotheses <= selected_nodes
    source = next(r for r in original['results'] if
                  (r['boundary_index'],r['cover_index']) == (proof['boundary_index'],proof['cover_index']))
    initial = {t:set(original['domain_pool'][di]) for t,di in source['domains']}
    assert all(t in initial and s in initial[t] for t,s in hypotheses)
    states = []
    checks = 0
    counts = Counter()
    for i,n in enumerate(proof['nodes']):
        op = n['op']
        counts[op] += 1
        def previous(j):
            assert 0 <= j < i
            return states[j]
        if op == 'choice':
            assert n['pose'] == n['tile'] < len(original['poses'])
            assert 0 <= n['star'] < len(language['stars'])
            domain = {n['star']} if (n['tile'],n['star']) in hypotheses else None
        elif op == 'neighbor':
            q = n['pair']
            src = previous(n['source'])
            assert compose(poses[proof['nodes'][n['source']]['pose']],atlas[q]) == poses[n['pose']]
            checks += 1
            if src is None or any(q not in cases[s] for s in src):
                domain = None
            else:
                domain = {t for s in src for t in allowed[cases[s][q]]}
        elif op == 'meet':
            assert n['inputs']
            domains = []
            for j in n['inputs']:
                value = previous(j)
                assert poses[proof['nodes'][j]['pose']] == poses[n['pose']]
                if value is not None:
                    domains.append(value)
            domain = set.intersection(*domains) if domains else None
        else:
            assert op == 'arc'
            left,right = previous(n['left']),previous(n['right'])
            assert poses[proof['nodes'][n['left']]['pose']] == poses[n['pose']]
            q = n['pair']
            assert compose(poses[n['pose']],atlas[q]) == poses[proof['nodes'][n['right']]['pose']]
            checks += 1
            domain = (left if left is None or right is None else
                      {s for s in left if q in cases[s] and allowed[cases[s][q]] & right})
        states.append(domain)
    assert 0 <= proof['root'] < len(states)
    assert states[proof['root']] is not None and not states[proof['root']]
    output = dict(scope='Exact necessary contradiction from retained choice hypotheses with presence-aware domain operations',
                  verified_cuts=1,cut_length=len(hypotheses),nodes=len(states),node_counts=dict(counts),
                  exact_placements=checks,direct_parent_exclusions=int(all(initial[t] == {s} for t,s in hypotheses)),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'layered_choice_certificate_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

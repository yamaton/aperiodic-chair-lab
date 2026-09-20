"""Replay Q013 role restrictions and synchronous star-domain propagation.

This fills the audit gap between the Q012 exterior fixed points and the
forced-layer inputs. It does not infer extension from a nonempty fixed point.
"""

import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def members(value):
    while value:
        low = value & -value
        yield low.bit_length()-1
        value -= low


def main():
    names = ('closed_star_audit.json','closed_star_compatibility.json','parent_neighbor_graph.json',
             'parent_star_arc_consistency.json','parent_boundary_cover_arcs.json','parent_cover_star_constraints.json')
    paths = [ROOT/'artifacts'/n for n in names]
    audit,compat,graph,arcs,boundary,raw = [json.loads(p.read_text()) for p in paths]
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    cases = [dict(row) for row in compat['cases']]
    role_masks = [sum(1<<s for s,rs in enumerate(audit['child_roles']) if rs == [i]) for i in range(8)]
    arc_pool = [sum(1<<s for s in ss) for ss in arcs['domain_pool']]
    retained_pool = [sum(1<<s for s in ss) for ss in raw['domain_pool']]
    bases = {r['external_index']:{i:arc_pool[d] for i,d in r['domains']} for r in arcs['results'] if 'domains' in r}
    adjacency = {}
    for i,j,q,r in graph['allowed_edges']:
        adjacency.setdefault(i,[]).append((j,q))
        adjacency.setdefault(j,[]).append((i,r))
    @lru_cache(maxsize=200000)
    def supported(value,neighbor,q):
        return sum(1<<s for s in members(value) if q in cases[s] and bits[cases[s][q]] & neighbor)
    seen = set()
    rounds = rejected = survived = 0
    for ri,result in enumerate(raw['results']):
        key = result['boundary_index'],result['cover_index']
        assert key not in seen
        seen.add(key)
        row = boundary['results'][key[0]]
        cover = row['covers'][key[1]]
        assert cover['legal_star'] is None
        domains = dict(bases[row['external_index']])
        assigned = set()
        for pi in cover['parents']:
            for tile,role in boundary['requirements'][pi]:
                assert tile not in assigned
                assigned.add(tile)
                domains[tile] &= role_masks[role]
        assert assigned == set(domains)-set(range(8))
        edges = {i:[(j,q) for j,q in adjacency.get(i,[]) if j in domains] for i in domains}
        while all(domains.values()):
            new = {}
            rounds += 1
            for i,value in domains.items():
                remaining = value
                for j,q in edges[i]:
                    remaining &= supported(value,domains[j],q)
                    if not remaining:
                        break
                new[i] = remaining
            if new == domains:
                assert 'domains' in result
                assert domains == {i:retained_pool[d] for i,d in result['domains']}
                survived += 1
                break
            domains = new
        else:
            assert 'rejection' in result
            rejected += 1
        if (ri+1)%1000 == 0:
            print(f'role-conditioned domain audit: {ri+1}/{len(raw["results"])}',flush=True)
    assert seen == {(i,j) for i,r in enumerate(boundary['results']) for j,c in enumerate(r['covers']) if c['legal_star'] is None}
    assert raw['status_counts'] == dict(survivor=survived,rejected=rejected)
    output = dict(scope='Independent synchronous replay of every Q013 role-conditioned cover domain',
                  covers=len(seen),survivors=survived,rejections=rejected,synchronous_rounds=rounds,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_cover_domain_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

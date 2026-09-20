"""Q013: require one parent cover's role choices to coexist in star domains.

The boundary-cover test only checked each role separately. Here fix all
roles of each nonlanguage cover simultaneously and repeat arc consistency.
Survival remains unknown: neighbors outside the finite patch are unassigned.
"""

import hashlib
import json
from collections import Counter,deque
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def members(value):
    while value:
        low = value & -value
        yield low.bit_length()-1
        value -= low


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_star_audit.json','closed_star_compatibility.json','parent_neighbor_graph.json',
              'parent_star_arc_consistency.json','parent_boundary_cover_arcs.json')]
    audit,compat,graph,arcs,boundary = [json.loads(p.read_text()) for p in paths]
    assert all(r['status'] != 'unknown_at_cover_limit' for r in boundary['results'])
    role_bits = [sum(1<<s for s,rs in enumerate(audit['child_roles']) if rs == [i]) for i in range(8)]
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    case_maps = [dict(row) for row in compat['cases']]
    adjacency = {}
    for i,j,q,r in graph['allowed_edges']:
        adjacency.setdefault(i,[]).append((j,q,r))
        adjacency.setdefault(j,[]).append((i,r,q))
    arc_pool = [sum(1<<s for s in ss) for ss in arcs['domain_pool']]
    arc_rows = {r['external_index']:r for r in arcs['results'] if 'domains' in r}
    @lru_cache(maxsize=200000)
    def supported(source,target,q):
        return sum(1<<s for s in members(source) if q in case_maps[s] and bits[case_maps[s][q]] & target)
    pool,pool_ids = [],{}
    def identifier(value):
        if value not in pool_ids:
            pool_ids[value] = len(pool)
            pool.append(list(members(value)))
        return pool_ids[value]
    results = []
    stats = Counter()
    for bi,row in enumerate(boundary['results']):
        base = {i:arc_pool[di] for i,di in arc_rows[row['external_index']]['domains']}
        for ci,cover in enumerate(row['covers']):
            if cover['legal_star'] is not None:
                continue
            domains = dict(base)
            assigned = {}
            for pi in cover['parents']:
                for tile,role in boundary['requirements'][pi]:
                    assert tile not in assigned
                    assigned[tile] = role
                    domains[tile] &= role_bits[role]
            assert set(assigned) == set(base)-set(range(8))
            queue = deque()
            queued = set()
            for j in domains:
                if domains[j] != base[j]:
                    for i,q,r in adjacency.get(j,[]):
                        if i in domains:
                            edge = i,j,r
                            if edge not in queued:
                                queue.append(edge)
                                queued.add(edge)
            failure = next((dict(kind='incompatible_role',tile=i) for i,v in domains.items() if not v),None)
            updates = 0
            while queue and failure is None:
                i,j,q = queue.popleft()
                queued.remove((i,j,q))
                new = supported(domains[i],domains[j],q)
                if new == domains[i]:
                    continue
                domains[i] = new
                updates += 1
                if not new:
                    failure = dict(kind='empty_star_domain',tiles=(i,j),pair=q)
                    break
                for k,r,reverse in adjacency.get(i,[]):
                    edge = k,i,reverse
                    if k in domains and edge not in queued:
                        queue.append(edge)
                        queued.add(edge)
            record = dict(boundary_index=bi,cover_index=ci,updates=updates)
            if failure:
                stats['rejected'] += 1
                record['rejection'] = failure
            else:
                stats['survivor'] += 1
                record['domains'] = [(i,identifier(v)) for i,v in sorted(domains.items())]
            results.append(record)
            if len(results)%1000 == 0:
                print(f'role-conditioned covers: {len(results)}; {dict(stats)}',flush=True)
    output = dict(scope='Necessary star-domain consistency under each nonlanguage parent cover; finite survivors remain unresolved',
                  domain_pool=pool,results=results,status_counts=dict(stats),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_cover_star_constraints.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(covers=len(results),statuses=dict(stats),domains=len(pool))),flush=True)


if __name__ == '__main__':
    main()

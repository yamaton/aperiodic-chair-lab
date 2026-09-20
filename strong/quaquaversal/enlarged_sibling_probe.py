"""Q031: bounded eight-sibling CSP for each remaining extra parent star.

Positive witnesses are finite tuples, not tilings. Exhausted searches keep
their full branch/arc trace for independent audit before any exclusion is
used. Node limits remain unknown. No parent frontier is modified here.
"""

import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NODE_LIMIT = 10000


def members(value):
    while value:
        low = value & -value
        yield low.bit_length()-1
        value -= low


def main():
    names = ('coarse_parent_language.json','coarse_support_domain_audit.json','coarse_star_arc_filter.json',
             'enlarged_sibling_roles.json')
    paths = [ROOT/'artifacts'/n for n in names]
    coarse,audit,filtered,recognizer = [json.loads(p.read_text()) for p in paths]
    assert audit['sources'][paths[0].name] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    assert recognizer['all_sibling_roles_agree']
    active = set(filtered['final_active_stars'])
    roles = dict(recognizer['roles'])
    assert set(roles) == active
    domains = [sum(1<<s for s in active if roles[s] == i) for i in range(8)]
    cases = [dict(row) for row in coarse['cases']]
    supports = [sum(1<<s for s in ss) for ss in coarse['domain_pool']]
    edges = [(i,j,q) for i,row in enumerate(recognizer['sibling_edges']) for j,q in row]

    @lru_cache(maxsize=200000)
    def restrict(value,other,q):
        return sum(1<<s for s in members(value) if q in cases[s] and supports[cases[s][q]] & other)

    results = []
    for root in sorted(active-set(range(coarse['original_stars']))):
        nodes = []
        def search(values):
            if len(nodes) >= NODE_LIMIT:
                return None,'unknown_at_node_limit',None
            ni = len(nodes)
            node = dict(trace=[])
            nodes.append(node)
            values = list(values)
            while True:
                changed = False
                for i,j,q in edges:
                    value = restrict(values[i],values[j],q)
                    if value != values[i]:
                        node['trace'].append((i,j,q))
                        values[i] = value
                        changed = True
                        if not value:
                            node['empty_role'] = i
                            return ni,'unsat_pending_audit',None
                if not changed:
                    break
            if all(v.bit_count() == 1 for v in values):
                witness = [next(members(v)) for v in values]
                node['witness'] = witness
                return ni,'sat',witness
            role = min((i for i in range(8) if values[i].bit_count()>1),key=lambda i:values[i].bit_count())
            node['branch_role'] = role
            node['branches'] = []
            for star in members(values[role]):
                child = list(values)
                child[role] = 1<<star
                ci,status,witness = search(child)
                node['branches'].append((star,ci))
                if status != 'unsat_pending_audit':
                    return ni,status,witness
            return ni,'unsat_pending_audit',None
        start = list(domains)
        start[roles[root]] = 1<<root
        entry,status,witness = search(start)
        results.append(dict(star=root,role=roles[root],status=status,witness=witness,search_nodes=len(nodes),
                            proof_nodes=nodes if status != 'sat' else None))
    counts = dict(Counter(r['status'] for r in results))
    output = dict(scope='Bounded necessary eight-sibling extension tests; SAT tuples are not global tilings',
                  node_limit=NODE_LIMIT,results=results,status_counts=counts,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'enlarged_sibling_probe.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),statuses=counts,total_nodes=sum(r['search_nodes'] for r in results))),flush=True)


if __name__ == '__main__':
    main()

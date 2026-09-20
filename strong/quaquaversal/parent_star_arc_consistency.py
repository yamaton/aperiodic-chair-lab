"""Q012: propagate allowed complete-star domains around a proposed parent.

Pairwise arc consistency is necessary, not sufficient for an infinite tiling.
No rejected tuple is called impossible outside this finite local-rule model.
Surviving domains and every rejection location are preserved for replay.
"""

import hashlib
import json
from collections import Counter,deque
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def members(bits):
    while bits:
        low = bits & -bits
        yield low.bit_length()-1
        bits -= low


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_star_compatibility.json','closed_star_audit.json','parent_external_domains.json',
              'parent_join_filter.json','parent_neighbor_graph.json')]
    compat,audit,external,joined,graph = [json.loads(p.read_text()) for p in paths]
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    cases = [dict(row) for row in compat['cases']]
    adjacency = [[] for _ in external['poses']]
    reverse_pairs = {}
    for i,j,q,r in graph['allowed_edges']:
        adjacency[i].append((j,q))
        adjacency[j].append((i,r))
        reverse_pairs[q] = r
        reverse_pairs[r] = q
    forbidden = [0 for _ in external['poses']]
    for i,j in graph['forbidden_pairs']:
        forbidden[i] |= 1<<j
        forbidden[j] |= 1<<i
    @lru_cache(maxsize=200000)
    def supported(source,target,q):
        result = 0
        for s in members(source):
            di = cases[s].get(q)
            if di is not None and bits[di] & target:
                result |= 1<<s
        return result
    pool = []
    pool_index = {}
    def domain_id(value):
        if value not in pool_index:
            pool_index[value] = len(pool)
            pool.append(list(members(value)))
        return pool_index[value]
    genuine = {tuple(t) for t in audit['transitions']}
    results = []
    stats = Counter()
    surviving_tuples = set()
    for si,row in enumerate(external['survivors']):
        t = joined['survivors'][row['tuple_index']]
        domains = {i:1<<s for i,s in enumerate(t)}
        for d in row['external_domains']:
            value = bits[d['domains'][0]]
            for di in d['domains'][1:]:
                value &= bits[di]
            domains[d['tile']] = value
        mask = sum(1<<i for i in domains)
        failure = None
        for i in domains:
            bad = forbidden[i] & mask
            if bad:
                failure = dict(kind='forbidden_pair',tiles=(i,next(members(bad))))
                break
        updates = 0
        queue = deque()
        queued = set()
        if failure is None:
            for i in sorted(domains):
                for j,q in adjacency[i]:
                    if j in domains:
                        queue.append((i,j,q))
                        queued.add((i,j,q))
        while queue and failure is None:
            i,j,q = queue.popleft()
            queued.remove((i,j,q))
            new = supported(domains[i],domains[j],q)
            if new == domains[i]:
                continue
            updates += 1
            domains[i] = new
            if not new:
                failure = dict(kind='empty_star_domain',tiles=(i,j),pair=q)
                break
            for k,r in adjacency[i]:
                edge = k,i,reverse_pairs[r]
                if k in domains and edge not in queued:
                    queue.append(edge)
                    queued.add(edge)
        if failure:
            assert tuple(t) not in genuine,(si,failure)
            stats[failure['kind']] += 1
            results.append(dict(external_index=si,tuple_index=row['tuple_index'],updates=updates,rejection=failure))
        else:
            stats['survivor'] += 1
            surviving_tuples.add(tuple(t))
            results.append(dict(external_index=si,tuple_index=row['tuple_index'],updates=updates,
                                domains=[(i,domain_id(v)) for i,v in sorted(domains.items())]))
        if (si+1)%1000 == 0:
            print(f'arc consistency: {si+1}/{len(external["survivors"])}; {dict(stats)}',flush=True)
    assert genuine <= surviving_tuples
    output = dict(scope='Arc consistency of complete-star domains on a finite parent-neighborhood patch; survivors are unresolved',
                  domain_pool=pool,results=results,status_counts=dict(stats),
                  extra_survivors=len(surviving_tuples-genuine),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_star_arc_consistency.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(statuses=dict(stats),extra_survivors=output['extra_survivors'],domains=len(pool))),flush=True)


if __name__ == '__main__':
    main()

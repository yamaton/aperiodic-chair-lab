"""Q029: conditional arc consistency around each possible parent star.

Input must be a complete necessary parent frontier, not selected SAT models.
Every root star forces all its neighbor tiles. Their star domains constrain
one another. A failed patch removes the root star from the global vocabulary;
repeat with the smaller vocabulary until this finite filter stabilizes.
"""

import argparse
import hashlib
import json
from collections import deque
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def members(value):
    while value:
        low = value & -value
        yield low.bit_length()-1
        value -= low


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_refined_frontier.json')
    parser.add_argument('--input-audit',type=Path,default=ROOT/'artifacts'/'coarse_refinement_audit.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_star_arc_filter.json')
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/n for n in ('closed_star_compatibility.json','coarse_parent_language.json',
                                         'coarse_support_domain_audit.json')]+[args.input,args.input_audit]
    base,coarse,support_audit,frontier,frontier_audit = [json.loads(p.read_text()) for p in paths]
    assert support_audit['sources'][paths[1].name] == hashlib.sha256(paths[1].read_bytes()).hexdigest()
    assert frontier_audit['sources'][args.input.name] == hashlib.sha256(args.input.read_bytes()).hexdigest()
    maps = {r['pair']:dict(r['entries']) for r in base['intersection_maps']}
    for q,entries in coarse['added_map_entries']:
        maps.setdefault(q,{}).update(entries)
    cases = [dict(row) for row in coarse['cases']]
    support = [sum(1<<s for s in ss) for ss in coarse['domain_pool']]
    by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    roots = {by_key[r['boundary_index'],r['cover_index']] for r in frontier['results'] if 'domains' in r}
    n = coarse['original_stars']
    active = set(range(n))|roots
    initial = sorted(active)
    graphs = {}
    for s in sorted(roots):
        positions = set(coarse['stars'][s])|{-1}
        edges = []
        for x in sorted(positions):
            row = {q:q for q in coarse['stars'][s]} if x == -1 else maps[x]
            edges.extend((x,y,q) for y,q in sorted(row.items()) if y in positions and x != y and q >= 0)
        incoming = {p:[] for p in positions}
        for x,y,q in edges:
            incoming[y].append((x,y,q))
        graphs[s] = edges,incoming

    @lru_cache(maxsize=200000)
    def supported(value,other,q):
        return sum(1<<s for s in members(value) if q in cases[s] and support[cases[s][q]] & other)

    pool,ids = [],{}
    def domain_id(value):
        if value not in ids:
            ids[value] = len(pool)
            pool.append(list(members(value)))
        return ids[value]

    rounds = []
    while True:
        live = sum(1<<s for s in active)
        results,removed = [],[]
        for s in sorted(active-set(range(n))):
            ds = {-1:1<<s}
            ds.update({q:support[di]&live for q,di in cases[s].items()})
            empty = next((p for p,v in ds.items() if not v),None)
            trace = []
            if empty is None:
                edges,incoming = graphs[s]
                queue,queued = deque(edges),set(edges)
                while queue:
                    x,y,q = queue.popleft()
                    queued.remove((x,y,q))
                    value = supported(ds[x],ds[y],q)
                    if value == ds[x]:
                        continue
                    ds[x] = value
                    trace.append((x,y,q))
                    if not value:
                        empty = x
                        break
                    for edge in incoming[x]:
                        if edge not in queued:
                            queue.append(edge)
                            queued.add(edge)
            result = dict(star=s,reduction_trace=trace)
            if empty is not None:
                removed.append(s)
                result['rejection'] = dict(position=empty,kind='arc_empty' if trace else 'initial_empty')
            else:
                result['domains'] = [[p,domain_id(v)] for p,v in sorted(ds.items())]
            results.append(result)
        rounds.append(dict(results=results,removed=removed))
        print(json.dumps(dict(round=len(rounds),input_extras=len(results),removed=len(removed))),flush=True)
        if not removed:
            break
        active.difference_update(removed)
    output = dict(scope='Necessary conditional neighbor-patch arc exclusions from a complete parent-star frontier',
                  arguments={k:str(v) for k,v in vars(args).items()},initial_active_stars=initial,
                  final_active_stars=sorted(active),domain_pool=pool,rounds=rounds,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(initial_extras=len(initial)-n,remaining_extras=len(active)-n,
                          conditional_domains=len(pool))),flush=True)


if __name__ == '__main__':
    main()

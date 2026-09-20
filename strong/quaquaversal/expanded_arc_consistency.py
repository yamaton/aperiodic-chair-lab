"""Q016: star-domain arc consistency inside a larger forced patch.

Discover atlas contacts by exact composition of possible star neighbors.
Only already present tiles impose these constraints. Missing geometric
contacts weaken this test; surviving finite patches remain unknown.
"""

import argparse
import hashlib
import json
from collections import Counter,deque
from functools import lru_cache
from math import lcm
from pathlib import Path

from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def members(value):
    while value:
        low = value & -value
        yield low.bit_length()-1
        value -= low


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'forced_outer_layer_4.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'expanded_arc_consistency.json')
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/'closed_contact_atlas.json',ROOT/'artifacts'/'closed_star_compatibility.json',args.input]
    atlas_raw,compat,source = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in source['poses']]
    scale = poses[0][2]
    assert all(p[2] == scale for p in poses)
    rotations = list(dict.fromkeys(p[0] for p in poses))
    rindex = {r:i for i,r in enumerate(rotations)}
    translations = [tuple(v/scale for v in p[1]) for p in poses]
    d = lcm(*(v.denominator for r in rotations+[p[0] for p in atlas] for row in r for v in row),
            *(v.denominator for t in translations+[p[1] for p in atlas] for v in t))
    def integer(v):
        assert (v*d).denominator == 1
        return int(v*d)
    rs = [tuple(tuple(integer(v) for v in row) for row in r) for r in rotations]
    ts = [tuple(integer(v) for v in t) for t in translations]
    rids = [rindex[p[0]] for p in poses]
    ar = [tuple(tuple(integer(v) for v in row) for row in p[0]) for p in atlas]
    ats = [tuple(integer(v) for v in p[1]) for p in atlas]
    rlookup = {tuple(v*d for row in r for v in row):i for i,r in enumerate(rs)}
    lookup = {(rids[i],tuple(v*d for v in t)):i for i,t in enumerate(ts)}
    assert len(lookup) == len(poses)
    @lru_cache(maxsize=200000)
    def product_rotation(ri,q):
        a,b = rs[ri],ar[q]
        return rlookup.get(tuple(sum(a[i][k]*b[k][j] for k in range(3)) for i in range(3) for j in range(3)))
    @lru_cache(maxsize=1000000)
    def placed(tile,q):
        ri = rids[tile]
        result = product_rotation(ri,q)
        if result is None:
            return None
        t = tuple(ts[tile][i]*d+sum(rs[ri][i][j]*ats[q][j] for j in range(3)) for i in range(3))
        return lookup.get((result,t))
    cases = [dict(row) for row in compat['cases']]
    reverse = {m['pair']:dict(m['entries'])[-1] for m in compat['intersection_maps']}
    bits = [sum(1<<s for s in dom['stars']) for dom in compat['domains']]
    input_pool = [sum(1<<s for s in ss) for ss in source['domain_pool']]
    possible = [sorted({q for s in ss for q in cases[s]}) for ss in source['domain_pool']]
    @lru_cache(maxsize=200000)
    def supported(value,neighbor,q):
        return sum(1<<s for s in members(value) if q in cases[s] and bits[cases[s][q]] & neighbor)
    pool,pool_index = [],{}
    def identifier(value):
        if value not in pool_index:
            pool_index[value] = len(pool)
            pool.append(list(members(value)))
        return pool_index[value]
    results = []
    stats = Counter()
    edge_total = 0
    total = sum('domains' in r for r in source['results'])
    for si,record in enumerate(source['results']):
        if 'domains' not in record:
            continue
        domains = {tile:input_pool[di] for tile,di in record['domains']}
        adjacency = {tile:{} for tile in domains}
        for tile,di in record['domains']:
            for q in possible[di]:
                neighbor = placed(tile,q)
                if neighbor in domains:
                    assert neighbor != tile
                    if neighbor in adjacency[tile]:
                        assert adjacency[tile][neighbor] == q
                    adjacency[tile][neighbor] = q
                    adjacency[neighbor][tile] = reverse[q]
        edges = [(i,j,q) for i,row in adjacency.items() for j,q in row.items()]
        edge_total += len(edges)
        queue = deque(edges)
        queued = set(edges)
        failure = None
        updates = 0
        trace = []
        while queue:
            i,j,q = queue.popleft()
            queued.remove((i,j,q))
            new = supported(domains[i],domains[j],q)
            if new == domains[i]:
                continue
            # The sequential trace is sufficient to replay every reduction,
            # including a rejected case; no search decision is hidden.
            trace.append((i,j,q))
            domains[i] = new
            updates += 1
            if not new:
                failure = dict(tiles=(i,j),pair=q)
                break
            for k,r in adjacency[i].items():
                edge = k,i,reverse[r]
                if edge not in queued:
                    queue.append(edge)
                    queued.add(edge)
        result = dict(source_index=si,boundary_index=record['boundary_index'],cover_index=record['cover_index'],
                      directed_edges=len(edges),updates=updates,reduction_trace=trace)
        if failure:
            stats['rejected'] += 1
            result['rejection'] = failure
        else:
            stats['survivor'] += 1
            result['domains'] = [(i,identifier(v)) for i,v in sorted(domains.items())]
        results.append(result)
        if len(results)%25 == 0:
            print(f'expanded arcs: {len(results)}/{total}; {dict(stats)}',flush=True)
    output = dict(scope='Necessary atlas-contact arc consistency in expanded forced patches; finite survivors are unresolved',
                  arguments={k:str(v) for k,v in vars(args).items()},integer_scale=d,
                  domain_pool=pool,results=results,status_counts=dict(stats),directed_edge_occurrences=edge_total,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),statuses=dict(stats),domains=len(pool),edges=edge_total)),flush=True)


if __name__ == '__main__':
    main()

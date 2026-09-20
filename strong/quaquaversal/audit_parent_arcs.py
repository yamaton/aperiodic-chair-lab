"""Q012 audit: rational edge poses and synchronous domain propagation.

Unlike the producer's queued arc updates, this replays whole synchronous
rounds. It checks greatest-fixpoint domains on survivors and emptiness on
rejections. The forbidden-pair shortcut was unused in this checkpoint.
"""

import hashlib
import json
from functools import cache,lru_cache
from pathlib import Path

from geometry import F,inverse_rotation,mm,mv,sub,mul
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def members(value):
    while value:
        low = value & -value
        yield low.bit_length()-1
        value -= low


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_compatibility.json','parent_external_domains.json',
              'parent_join_filter.json','parent_neighbor_graph.json','parent_star_arc_consistency.json')]
    atlas_raw,compat,external,joined,graph,raw = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in external['poses']]
    @cache
    def inverse(r):
        return inverse_rotation(r)
    @cache
    def rotation(a,b):
        return mm(inverse(a),b)
    adjacency = [[] for p in poses]
    for i,j,q,r in graph['allowed_edges']:
        for a,b,k in ((i,j,q),(j,i,r)):
            p,t = poses[a],poses[b]
            expected = rotation(p[0],t[0]),mul(1/p[2],mv(inverse(p[0]),sub(t[1],p[1]))),t[2]/p[2]
            assert expected == atlas[k]
            adjacency[a].append((b,k))
    print(f'rational directed edge checks: {2*len(graph["allowed_edges"])}',flush=True)
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    cases = [dict(row) for row in compat['cases']]
    @lru_cache(maxsize=200000)
    def supported(value,neighbor,q):
        return sum(1<<s for s in members(value) if q in cases[s] and bits[cases[s][q]] & neighbor)
    final_pool = [sum(1<<s for s in ss) for ss in raw['domain_pool']]
    assert len(raw['results']) == len(external['survivors'])
    rounds = 0
    for si,(result,source) in enumerate(zip(raw['results'],external['survivors'],strict=True)):
        assert result['external_index'] == si and result['tuple_index'] == source['tuple_index']
        t = joined['survivors'][source['tuple_index']]
        domains = {i:1<<s for i,s in enumerate(t)}
        for d in source['external_domains']:
            value = bits[d['domains'][0]]
            for di in d['domains'][1:]:
                value &= bits[di]
            domains[d['tile']] = value
        edges = {i:[(j,q) for j,q in adjacency[i] if j in domains] for i in domains}
        while True:
            new = {}
            rounds += 1
            for i,value in domains.items():
                remaining = value
                for j,q in edges[i]:
                    remaining &= supported(value,domains[j],q)
                    if not remaining:
                        break
                new[i] = remaining
            if not all(new.values()):
                assert result['rejection']['kind'] == 'empty_star_domain'
                break
            if new == domains:
                assert 'domains' in result
                assert new == {i:final_pool[di] for i,di in result['domains']}
                break
            domains = new
        if (si+1)%1000 == 0:
            print(f'synchronous star-domain audit: {si+1}/{len(raw["results"])}',flush=True)
    output = dict(scope='Fraction edge-pose checks and independent synchronous arc-consistency replay',
                  directed_pose_checks=2*len(graph['allowed_edges']),neighborhoods=len(raw['results']),
                  synchronous_rounds=rounds,status_counts=raw['status_counts'],
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_arc_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

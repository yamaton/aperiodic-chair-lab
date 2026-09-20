"""Recompute every coarse support domain using integer visibility signatures.

The geometric map additions and reciprocity already have an independent
exact audit. This checks both inclusion directions for every support set,
so later arc proofs may safely use those sets rather than scan all targets.
"""

import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_star_compatibility.json','coarse_parent_language.json','coarse_parent_language_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    base,raw,audit = [json.loads(p.read_text()) for p in paths]
    assert audit['sources'][paths[1].name] == hashlib.sha256(paths[1].read_bytes()).hexdigest()
    maps = {r['pair']:dict(r['entries']) for r in base['intersection_maps']}
    for q,entries in raw['added_map_entries']:
        maps.setdefault(q,{}).update(entries)
    inverse = {q:row.get(-1) for q,row in maps.items()}
    # Identity has code 0; pose i has code i+1. Signatures use set bits,
    # independently of the producer's ordered coordinate tuples.
    groups = defaultdict(set)
    for t,star in enumerate(raw['stars']):
        for inv in star:
            q = inverse[inv]
            if q is not None:
                sig = sum(1<<(r+1) for r in [*star,-1] if r in maps[inv])
                groups[q,sig].add(t)
    checked = 0
    for s,(star,row) in enumerate(zip(raw['stars'],raw['cases'],strict=True)):
        assert len(row) == len(star) and {q for q,di in row} == set(star)
        for q,di in row:
            sig = sum(1<<(maps[q][r]+1) for r in [*star,-1] if r in maps[q])
            expected = groups[q,sig] if inverse[q] is not None else set()
            actual = raw['domain_pool'][di]
            assert len(actual) == len(set(actual)) and set(actual) == expected
            checked += 1
    output = dict(scope='Independent complete recomputation of every coarse neighbor-star support domain',
                  stars=len(raw['stars']),support_domains=len(raw['domain_pool']),incidences=checked,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'coarse_support_domain_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

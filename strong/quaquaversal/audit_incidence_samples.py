"""Verify every sampled overlap clause with independent Fraction arithmetic."""

import hashlib
import json
from functools import cache
from pathlib import Path

from geometry import F,inside,transform,inverse_rotation,mv,sub

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in ('neighbor_incidence_sat.json','incidence_sample_exclusions.json')]
    source,raw = [json.loads(p.read_text()) for p in paths]
    d = raw['normalized_pose_denominator']
    assert d == source['pose_key_denominator']
    poses = [(tuple(tuple(F(key[3*i+j],d) for j in range(3)) for i in range(3)),
              tuple(F(v,d) for v in key[9:]),F(1)) for key in source['normalized_pose_keys']]
    samples = [tuple(F(v,raw['sample_denominator']) for v in p) for p in raw['sample_numerators']]
    assert all(inside(p,strict=True) for p in samples)
    @cache
    def point(i,s):
        return transform(poses[i],samples[s])
    @cache
    def inverse(r):
        return inverse_rotation(r)
    seen = set()
    for ei,e in enumerate(raw['exclusions']):
        i,j = e['positions']
        assert i < j and (i,j) not in seen
        seen.add((i,j))
        a,b = e['sample_from'],e['containing_tile']
        assert {a,b} == {i,j}
        p = point(a,e['sample_index'])
        q = mv(inverse(poses[b][0]),sub(p,poses[b][1]))
        assert inside(q,strict=True),(ei,q)
        if (ei+1)%50000 == 0:
            print(f'rational overlap witness audit: {ei+1}/{len(raw["exclusions"])}',flush=True)
    output = dict(scope='Independent strict common-interior-point proof for each sampled non-overlap clause',
                  overlap_clauses=len(seen),distinct_sample_points=point.cache_info().currsize,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'incidence_sample_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

"""Audit Q012 integer relative products with independent Fraction formulas.

Check every cooccurring pair, including missing atlas-membership results,
then reconstruct every common-neighbor domain and compare the previous
sibling-only certificate. No global extension claim is made.
"""

import hashlib
import json
from collections import defaultdict
from functools import cache
from pathlib import Path

from geometry import I,ZERO,F,inverse_rotation,mm,mv,sub,encode
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent
IDENTITY = I,ZERO,F(1)


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json','star_parent_consistency.json')]
    atlas_raw,language,raw,old = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    index = {p:i for i,p in enumerate(atlas)}
    index[IDENTITY] = -1
    poses = atlas+[IDENTITY]
    stars = [tuple(s['neighbors']) for s in language['stars']]
    cooccurs = defaultdict(set)
    for s in stars:
        for q in s:
            cooccurs[q].update(s)
    @cache
    def inverse(r):
        return inverse_rotation(r)
    @cache
    def rotation(a,b):
        return mm(inverse(a),b)
    maps = {e['pair']:dict(e['entries']) for e in raw['intersection_maps']}
    checked = 0
    for q,rs in sorted(cooccurs.items()):
        expected = {}
        for r in sorted(rs|{-1}):
            a,b = poses[q],poses[r]
            rel = rotation(a[0],b[0]),mv(inverse(a[0]),sub(b[1],a[1])),F(1)
            if rel in index:
                expected[r] = index[rel]
            checked += 1
        assert expected == maps[q],q
        if (q+1)%250 == 0:
            print(f'rational pose rows audited: {q+1}/{len(atlas)}',flush=True)
    own = defaultdict(list)
    for si,s in enumerate(stars):
        for q in s:
            fingerprint = tuple(sorted(r for r in (*s,-1) if r in maps[q]))
            own[q,fingerprint].append(si)
    lookup = {}
    for di,d in enumerate(raw['domains']):
        key = d['pair'],tuple(d['fingerprint'])
        assert d['stars'] == own[key]
        assert key not in lookup
        lookup[key] = di
    assert set(lookup) == set(own)
    cases = []
    for si,s in enumerate(stars):
        expected = []
        for q in s:
            target = tuple(sorted(maps[q][r] for r in (*s,-1) if r in maps[q]))
            expected.append([q,lookup[maps[q][-1],target]])
        assert expected == raw['cases'][si]
        cases.append(dict(expected))
    for c in old['cases']:
        di = cases[c['star']][c['pair']]
        assert raw['domains'][di]['stars'] == c['compatible_stars']
    output = dict(scope='Fraction replay of all Q012 cooccurrences, domain partitions and sibling compatibility',
                  relative_pose_tests=checked,domains=len(lookup),cases=sum(map(len,raw['cases'])),
                  sibling_cases_rechecked=len(old['cases']),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'closed_star_compatibility_audit.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

"""Q012: common-neighbor compatibility for every legal star contact.

Exact integer arithmetic implements rational relative-pose composition on
the finite atlas. Domains are shared across cases rather than repeating
potentially large lists. Compatibility is necessary, not global extension.
"""

import hashlib
import json
from collections import defaultdict
from math import lcm
from pathlib import Path

from geometry import I,ZERO,F,inverse_rotation,encode
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent
IDENTITY = I,ZERO,F(1)


class ExactPoseIndex:
    """Relative poses via scaled integers; no rounding or float conversion."""
    def __init__(self,poses):
        self.poses = list(poses)+[IDENTITY]
        rotations = list(dict.fromkeys(p[0] for p in self.poses))
        inverse = [inverse_rotation(r) for r in rotations]
        self.denominator = lcm(*(v.denominator for r in rotations+inverse for row in r for v in row),
                               *(v.denominator for p in self.poses for v in p[1]))
        d = self.denominator
        def integer(x):
            assert (x*d).denominator == 1
            return int(x*d)
        self.rotations = [tuple(tuple(integer(v) for v in row) for row in r) for r in rotations]
        self.inverse = [tuple(tuple(integer(v) for v in row) for row in r) for r in inverse]
        self.translations = [tuple(integer(v) for v in p[1]) for p in self.poses]
        self.rotation_ids = [rotations.index(p[0]) for p in self.poses]
        self.rotation_lookup = {tuple(v*d for row in r for v in row):i for i,r in enumerate(self.rotations)}
        self.pose_lookup = {(rid,tuple(v*d for v in t)):(i if i < len(poses) else -1)
                            for i,(rid,t) in enumerate(zip(self.rotation_ids,self.translations))}
        self.products = {}

    def relative_id(self,q,r):
        qi,ri = self.rotation_ids[q],self.rotation_ids[r]
        key = qi,ri
        if key not in self.products:
            a,b = self.inverse[qi],self.rotations[ri]
            product = tuple(sum(a[i][k]*b[k][j] for k in range(3)) for i in range(3) for j in range(3))
            self.products[key] = self.rotation_lookup.get(product)
        rid = self.products[key]
        if rid is None:
            return None
        delta = tuple(a-b for a,b in zip(self.translations[r],self.translations[q]))
        t = tuple(sum(a*b for a,b in zip(row,delta)) for row in self.inverse[qi])
        return self.pose_lookup.get((rid,t))


def main():
    paths = [ROOT/'artifacts'/name for name in ('closed_contact_atlas.json','closed_star_language.json')]
    atlas_raw,language = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    stars = [tuple(s['neighbors']) for s in language['stars']]
    exact = ExactPoseIndex(atlas)
    cooccurs = defaultdict(set)
    for s in stars:
        for q in s:
            cooccurs[q].update(s)
    maps = {}
    inverse = {}
    for q,rs in cooccurs.items():
        maps[q] = {r:t for r in rs if (t := exact.relative_id(q,r)) is not None}
        inverse[q] = exact.relative_id(q,-1)
        assert inverse[q] is not None
        maps[q][-1] = inverse[q]
    print(f'exact relative products: {sum(map(len,cooccurs.values()))}; scale {exact.denominator}',flush=True)
    own = defaultdict(list)
    for si,s in enumerate(stars):
        for q in s:
            fingerprint = tuple(sorted(r for r in (*s,-1) if r in maps[q]))
            own[q,fingerprint].append(si)
    keys = sorted(own)
    domain_ids = {key:i for i,key in enumerate(keys)}
    domains = [own[k] for k in keys]
    cases = []
    for si,s in enumerate(stars):
        row = []
        for q in s:
            target = tuple(sorted(maps[q][r] for r in (*s,-1) if r in maps[q]))
            key = inverse[q],target
            assert key in domain_ids,(si,q)
            row.append((q,domain_ids[key]))
        cases.append(row)
    output = dict(scope='Necessary common-neighbor compatibility; no global extension or aperiodicity claim',
                  denominator=exact.denominator,
                  intersection_maps=[dict(pair=q,entries=sorted(m.items())) for q,m in sorted(maps.items())],
                  domains=[dict(pair=q,fingerprint=f,stars=s) for (q,f),s in zip(keys,domains)],
                  cases=cases,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'closed_star_compatibility.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=sum(map(len,cases)),domains=len(domains),
                          domain_members=sum(map(len,domains)),largest_domain=max(map(len,domains)))),flush=True)


if __name__ == '__main__':
    main()

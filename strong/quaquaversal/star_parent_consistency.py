"""Q011: test whether overlapping legal closed stars agree on sibling roles.

Each allowed star recognizes one child position. For a proposed sibling,
both centers see exactly the same tiles touching both centers. Comparing
these exact intersection fingerprints gives a necessary compatibility test
without enumerating global tilings. A failed test is unresolved, not a
realizable counterexample.
"""

import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path

from geometry import I,ZERO,F,child_maps,encode
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent
IDENTITY = I,ZERO,F(1)


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','closed_star_audit.json')]
    atlas_raw,language,audit = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    index = {p:i for i,p in enumerate(atlas)}
    index[IDENTITY] = -1
    stars = [tuple(s['neighbors']) for s in language['stars']]
    assert all(len(r) == 1 for r in audit['child_roles'])
    roles = [r[0] for r in audit['child_roles']]
    children = [p for _,p in child_maps()]
    sibling_edges = [[(j,index[relative(p,q)]) for j,q in enumerate(children)
                      if i != j and relative(p,q) in index] for i,p in enumerate(children)]
    sibling_ids = sorted({q for row in sibling_edges for j,q in row})
    inverse = {q:index[relative(atlas[q],IDENTITY)] for q in sibling_ids}
    # All entries are exact affine isometries. A missing result cannot touch
    # the root in a legal star, since the closed pair atlas is exhaustive.
    maps = {}
    for q in sibling_ids:
        maps[q] = {r:index[rel] for r,p in enumerate(atlas)
                   if (rel := relative(atlas[q],p)) in index}
        maps[q][-1] = inverse[q]
    own = defaultdict(list)
    for si,star in enumerate(stars):
        for q in sibling_ids:
            if q in star:
                fingerprint = tuple(sorted(r for r in (*star,-1) if r in maps[q]))
                own[q,fingerprint].append(si)
    cases = []
    unresolved = []
    for si,star in enumerate(stars):
        role = roles[si]
        for target_role,q in sibling_edges[role]:
            assert q in star
            fingerprint = tuple(sorted(maps[q][r] for r in (*star,-1) if r in maps[q]))
            compatible = own[inverse[q],fingerprint]
            assert compatible,(si,target_role,q)
            possible_roles = sorted({roles[t] for t in compatible})
            row = dict(star=si,sibling_role=target_role,pair=q,
                       compatible_stars=compatible,possible_roles=possible_roles)
            cases.append(row)
            if possible_roles != [target_role]:
                unresolved.append(len(cases)-1)
    output = dict(scope='Necessary common-neighbor compatibility of legal closed stars, for sibling-role agreement',
                  sibling_edges=sibling_edges,intersection_maps=[dict(pair=q,entries=sorted(m.items())) for q,m in maps.items()],
                  cases=cases,unresolved_cases=unresolved,
                  all_sibling_roles_agree=not unresolved,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'star_parent_consistency.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(cases),unresolved=len(unresolved),
                          compatible_counts=dict(Counter(len(c['compatible_stars']) for c in cases)),
                          all_sibling_roles_agree=not unresolved)),flush=True)


if __name__ == '__main__':
    main()

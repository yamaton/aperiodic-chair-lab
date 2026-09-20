"""Q011: add common-neighbor checks between disjoint sibling centers.

Unlike the first join, these centers are not in one another's closed star.
They may still see some of the same external tiles. All decisions use
exact poses; survivors remain only necessary local candidates.
"""

import hashlib
import json
from pathlib import Path

from geometry import I,ZERO,F,child_maps,encode
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent
IDENTITY = I,ZERO,F(1)


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','closed_star_audit.json','parent_star_join.json')]
    atlas_raw,language,audit,joined = [json.loads(p.read_text()) for p in paths]
    assert joined['status'] == 'enumeration_complete'
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    index = {p:i for i,p in enumerate(atlas)}
    index[IDENTITY] = -1
    stars = [tuple(s['neighbors']) for s in language['stars']]
    children = [p for _,p in child_maps()]
    directions = [(i,j,relative(p,q)) for i,p in enumerate(children) for j,q in enumerate(children)
                  if i != j and relative(p,q) not in index]
    maps = {}
    for i,j,q in directions:
        maps[i,j] = {r:index[t] for r,p in enumerate(atlas) if (t := relative(q,p)) in index}
    fingerprints = {}
    for i,j,q in directions:
        for si,star in enumerate(stars):
            if audit['child_roles'][si] == [i]:
                fingerprints[i,j,si] = (tuple(sorted(r for r in star if r in maps[i,j])),
                                        tuple(sorted(maps[i,j][r] for r in star if r in maps[i,j])))
    expected = {tuple(t) for t in audit['transitions']}
    survivors = []
    rejections = []
    for t in joined['tuples']:
        failed = next(((i,j) for i,j,q in directions if i < j and
                       fingerprints[i,j,t[i]][1] != fingerprints[j,i,t[j]][0]),None)
        if failed:
            rejections.append(dict(tuple=t,failed_pair=failed))
        else:
            survivors.append(t)
    assert expected <= {tuple(t) for t in survivors}
    extra = [t for t in survivors if tuple(t) not in expected]
    output = dict(scope='Exact common-neighbor filter for disjoint sibling centers; survivors need extension checks',
                  directed_noncontacting_sibling_pairs=[(i,j) for i,j,q in directions],
                  survivors=survivors,rejections=rejections,extra_tuples=extra,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_join_filter.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(input=len(joined['tuples']),survivors=len(survivors),extra=len(extra))),flush=True)


if __name__ == '__main__':
    main()

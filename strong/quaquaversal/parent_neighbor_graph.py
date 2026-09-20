"""Q012: exact pair graph of all exterior-neighborhood tile positions.

Each pair is separated, an allowed closed-atlas contact, or forbidden in a
tiling obeying the proposed closed-star rule. Forbidden includes both actual
overlap and a touching relative pose absent from the atlas. Integer affine
membership has no tolerance; edge clipping decides the remaining cases.
"""

import hashlib
import json
from math import lcm
from pathlib import Path

from geometry import F,inverse_rotation,encode
from contact_atlas import relative
from closed_stars import bounds
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in ('closed_contact_atlas.json','parent_external_domains.json')]
    atlas_raw,external = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in external['poses']]
    scale = poses[0][2]
    assert all(p[2] == scale for p in poses)
    rotations = list(dict.fromkeys(p[0] for p in poses))
    inverses = [inverse_rotation(r) for r in rotations]
    translations = [tuple(x/scale for x in p[1]) for p in poses]
    denominator = lcm(*(x.denominator for r in rotations+inverses+[p[0] for p in atlas] for row in r for x in row),
                      *(x.denominator for t in translations+[p[1] for p in atlas] for x in t))
    d = denominator
    def integer(x):
        assert (x*d).denominator == 1
        return int(x*d)
    rs = [tuple(tuple(integer(x) for x in row) for row in r) for r in rotations]
    invs = [tuple(tuple(integer(x) for x in row) for row in r) for r in inverses]
    ts = [tuple(integer(x) for x in t) for t in translations]
    rids = [rotations.index(p[0]) for p in poses]
    atlas_rotations = list(dict.fromkeys(p[0] for p in atlas))
    rotation_lookup = {tuple(integer(x)*d for row in r for x in row):i for i,r in enumerate(atlas_rotations)}
    atlas_lookup = {(atlas_rotations.index(p[0]),tuple(integer(x)*d for x in p[1])):i for i,p in enumerate(atlas)}
    products = {}
    def pair_id(i,j):
        a,b = rids[i],rids[j]
        key = a,b
        if key not in products:
            product = tuple(sum(invs[a][u][k]*rs[b][k][v] for k in range(3)) for u in range(3) for v in range(3))
            products[key] = rotation_lookup.get(product)
        rid = products[key]
        if rid is None:
            return None
        delta = tuple(y-x for x,y in zip(ts[i],ts[j]))
        t = tuple(sum(x*y for x,y in zip(row,delta)) for row in invs[a])
        return atlas_lookup.get((rid,t))
    boxes = [bounds(p) for p in poses]
    box_scale = lcm(*(x.denominator for b in boxes for interval in b for x in interval))
    boxes = [tuple((int(lo*box_scale),int(hi*box_scale)) for lo,hi in b) for b in boxes]
    edges,forbidden = [],[]
    checked = 0
    clipped = 0
    for i,p in enumerate(poses):
        for j in range(i+1,len(poses)):
            if any(hi < lo2 or hi2 < lo for (lo,hi),(lo2,hi2) in zip(boxes[i],boxes[j])):
                continue
            checked += 1
            q = pair_id(i,j)
            if q is not None:
                reverse = pair_id(j,i)
                assert reverse is not None
                edges.append((i,j,q,reverse))
            else:
                clipped += 1
                if edge_points(relative(p,poses[j]),first_only=True):
                    forbidden.append((i,j))
        if (i+1)%100 == 0:
            print(f'neighbor graph: {i+1}/{len(poses)}; edges {len(edges)}, forbidden {len(forbidden)}',flush=True)
    output = dict(scope='Exact necessary pair graph on the exterior-neighborhood position catalog',
                  integer_scale=denominator,bounding_box_scale=box_scale,checked_pairs=checked,
                  edge_clipping_tests=clipped,allowed_edges=edges,forbidden_pairs=forbidden,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'closed_stars.py',
                            ROOT/'reflected_controls.py',ROOT/'audit_closed_atlas.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_neighbor_graph.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(checked=checked,clipped=clipped,allowed=len(edges),forbidden=len(forbidden))),flush=True)


if __name__ == '__main__':
    main()

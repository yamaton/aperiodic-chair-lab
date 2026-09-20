"""Q006 counterexample: a periodic reflection tiling of the 30-60-90 triangle.

Side reflection is combined with z -> 1-z so every 3D pose is proper.
This yields a periodic prism tiling whose every contact belongs to the atlas.
"""

from collections import deque
import hashlib
import json
from itertools import product
from pathlib import Path

from geometry import (F,I,ZERO,vec,compose,vertices,separating_axis,contacts_fast,
                      encode,det,mm,transpose,G)
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    atlas_path = ROOT/'artifacts'/'contact_atlas.json'
    atlas = {raw_pose(r['pose']) for r in json.loads(atlas_path.read_text())['poses']}
    generators = [
        ((vec(-1,0,0),vec(0,1,0),vec(0,0,-1)),vec(0,0,1),F(1)),
        ((vec(1,0,0),vec(0,-1,0),vec(0,0,-1)),vec(0,0,1),F(1)),
        ((vec(F(1,2),F(-1,2),0),vec(F(-3,2),F(-1,2),0),vec(0,0,-1)),
         vec(F(1,2),F(3,2),1),F(1)),
    ]
    assert all(g in atlas for g in generators)
    assert (I,vec(0,0,1),F(1)) in atlas
    periods = vec(2,6,1)
    def normalize(p):
        r,t,s = p
        return r,(t[0]%periods[0],t[1]%periods[1],t[2]),s
    start = I,ZERO,F(1)
    known = {start:[]}
    queue = deque([start])
    while queue:
        p = queue.popleft()
        for i,g in enumerate(generators):
            q = normalize(compose(p,g))
            if q not in known:
                known[q] = known[p]+[i]
                queue.append(q)
        assert len(known) <= 1000,'Unexpected large quotient; this is not an impossibility result'
    poses = list(known)
    print('periodic orbit representatives',len(poses),flush=True)
    assert F(len(poses),2) == periods[0]*periods[1]*periods[2]
    assert all(det(p[0]) == 1 and mm(mm(transpose(p[0]),G),p[0]) == G for p in poses)
    assert all(all(0 <= v[2] <= 1 for v in vertices(p)) for p in poses)
    vs = [vertices(p) for p in poses]
    bounds = [tuple((min(v[k] for v in poly),max(v[k] for v in poly)) for k in range(3)) for poly in vs]
    # Use an automatically justified finite offset range.
    spans = [max(v[k] for poly in vs for v in poly)-min(v[k] for poly in vs for v in poly) for k in range(3)]
    radius = [int(span//period)+1 for span,period in zip(spans,periods)]
    certificates = []
    all_contacts = []
    for i,p in enumerate(poses):
        for offset in product(*(range(-n,n+1) for n in radius)):
            translation = tuple(a*b for a,b in zip(offset,periods))
            for j,q in enumerate(poses):
                if offset == (0,0,0) and i == j:
                    continue
                shifted_bounds = tuple((lo+d,hi+d) for (lo,hi),d in zip(bounds[j],translation))
                if any(ahi < blo or bhi < alo for (alo,ahi),(blo,bhi) in zip(bounds[i],shifted_bounds)):
                    continue
                moved = q[0],tuple(x+y for x,y in zip(q[1],translation)),q[2]
                witness = separating_axis(p,moved)
                assert witness is not None,(i,j,offset)
                certificates.append(dict(i=i,j=j,offset=offset,separator=witness))
                for c in contacts_fast([p,moved]):
                    rel = relative(p,moved)
                    assert rel in atlas,(i,j,offset,rel)
                    all_contacts.append(dict(i=i,j=j,offset=offset,fi=c['fi'],fj=c['fj'],relative_pose=rel))
    output = dict(scope='Exact periodic packing and volume-density coverage; all positive-area contacts in Q006 atlas',
                  result='Q006 pair-pose rule admits a periodic tiling',periods=periods,
                  tile_count=len(poses),poses=poses,generator_words=list(known.values()),
                  generators=generators,checked_offset_radius=radius,
                  separating_certificates=certificates,contacts=all_contacts,
                  volume_ratio=F(len(poses),2)/(periods[0]*periods[1]*periods[2]),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',atlas_path,Path(__file__))})
    (ROOT/'artifacts'/'atlas_periodic_reflections.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print(f'PASS: {len(poses)} tiles per cell; {len(all_contacts)} directed area contacts; no overlap; volume density 1',flush=True)


if __name__ == '__main__':
    main()

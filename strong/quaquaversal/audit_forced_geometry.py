"""Check Q015 rejection points without the producer's clipping decision."""

import hashlib
import json
from pathlib import Path

from geometry import F,inside,inverse_point
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','forced_outer_layer_3.json','forced_patch_geometry.json')]
    atlas_raw,source,raw = [json.loads(p.read_text()) for p in paths]
    atlas = {raw_pose(p['pose']) for p in atlas_raw['poses']}
    poses = [raw_pose(p) for p in source['poses']]
    for witness in raw['witnesses']:
        i,j = witness['tiles']
        q = relative(poses[i],poses[j])
        assert q == raw_pose(witness['relative_pose']) and q not in atlas
        points = [tuple(F(v) for v in p) for p in witness['common_points']]
        assert points and all(inside(p) and inside(inverse_point(q,p)) for p in points)
    rejected = 0
    for result in raw['results']:
        if 'forbidden_pair_witness' not in result:
            continue
        origin = source['results'][result['source_index']]
        assert (result['boundary_index'],result['cover_index']) == (origin['boundary_index'],origin['cover_index'])
        present = {i for i,di in origin['domains']}
        witness = raw['witnesses'][result['forbidden_pair_witness']]
        assert set(witness['tiles']) <= present
        rejected += 1
    assert rejected == raw['status_counts'].get('rejected',0)
    output = dict(scope='Point-in-both-polyhedra and atlas-absence certificates for geometric exclusions only',
                  rejected_patches=rejected,distinct_witnesses=len(raw['witnesses']),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'forced_geometry_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

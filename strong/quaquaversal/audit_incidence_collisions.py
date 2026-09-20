"""Audit that each reported colliding support is forced by a selected star.

Find independent sponsors by inverse pose composition. Check the common
point certificate and atlas absence, then classify the full intersection.
This rejects six finite assignments, not their parent cases.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import F,I,ZERO,compose,inside,inverse_point
from contact_atlas import relative
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points,dimension

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','expanded_arcs_2_seed.json',
              'neighbor_incidence_sat.json','incidence_model_geometry.json')]
    atlas_raw,language,source,sat,geometry = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    atlas_set = set(atlas)
    inverses = [relative(p,(I,ZERO,F(1))) for p in atlas]
    scale,d = F(sat['tile_scale']),sat['pose_key_denominator']
    poses = [(tuple(tuple(F(key[3*i+j],d) for j in range(3)) for i in range(3)),
              tuple(scale*F(v,d) for v in key[9:]),scale) for key in sat['normalized_pose_keys']]
    results = []
    for row in geometry['results']:
        if 'witness' not in row:
            continue
        model = sat['results'][row['model_index']]
        initial = source['results'][model['source_index']]
        domain_ids = dict(initial['domains'])
        selected = dict(model['selected_stars'])
        centers = {raw_pose(source['poses'][i]):i for i in selected}
        witness = geometry['witnesses'][row['witness']]
        sponsors = []
        for pi in witness['positions']:
            target = poses[pi]
            sponsor = None
            for q,inverse in enumerate(inverses):
                parent = compose(target,inverse)
                if parent in centers:
                    tile = centers[parent]
                    s = selected[tile]
                    if q in language['stars'][s]['neighbors']:
                        assert s in source['domain_pool'][domain_ids[tile]]
                        assert compose(parent,atlas[q]) == target
                        sponsor = dict(position=pi,center=tile,star=s,pair=q)
                        break
            assert sponsor is not None
            sponsors.append(sponsor)
        a,b = [poses[i] for i in witness['positions']]
        q = relative(a,b)
        assert q == raw_pose(witness['relative_pose']) and q not in atlas_set
        points = [tuple(F(v) for v in p) for p in witness['common_points']]
        assert points and all(inside(p) and inside(inverse_point(q,p)) for p in points)
        dim = dimension(edge_points(q))
        assert dim in (0,1,2,3)
        results.append(dict(model_index=row['model_index'],witness=row['witness'],sponsors=sponsors,intersection_dimension=dim))
    output = dict(scope='Independent sponsor and contact certificate replay for selected incidence assignments only',
                  results=results,dimensions=dict(Counter(r['intersection_dimension'] for r in results)),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',
                            ROOT/'audit_closed_atlas.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'incidence_collision_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(assignments=len(results),dimensions=output['dimensions'])),flush=True)


if __name__ == '__main__':
    main()

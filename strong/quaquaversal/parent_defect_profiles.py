"""Describe surviving parent covers by their nearest legal star.

Symmetric difference is a diagnostic only, not a constraint or a proof.
All parent contacts are classified by exact intersection dimension.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from reflected_controls import raw_pose
from audit_closed_atlas import edge_points,dimension

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','parent_boundary_cover_arcs.json','forced_outer_layer_3.json')]
    atlas_raw,language,boundary,source = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = list(atlas)
    index = {p:i for i,p in enumerate(poses)}
    parent_ids = []
    for raw in boundary['parents']:
        p = raw_pose(raw)
        if p not in index:
            index[p] = len(poses)
            poses.append(p)
        parent_ids.append(index[p])
    legal = [sum(1<<i for i in s['neighbors']) for s in language['stars']]
    dimensions = [dimension(edge_points(p)) for p in poses]
    assert all(d in (0,1,2) for d in dimensions)
    results = []
    counts = Counter()
    max_dimensions = Counter()
    for si,row in enumerate(source['results']):
        if 'domains' not in row:
            continue
        cover = boundary['results'][row['boundary_index']]['covers'][row['cover_index']]
        ids = {parent_ids[p] for p in cover['parents']}
        value = sum(1<<i for i in ids)
        distance,li = min(((value^v).bit_count(),i) for i,v in enumerate(legal))
        old = set(language['stars'][li]['neighbors'])
        added,removed = sorted(ids-old),sorted(old-ids)
        assert len(added)+len(removed) == distance > 0
        counts[distance] += 1
        max_dimensions[max(dimensions[i] for i in added+removed)] += 1
        results.append(dict(source_index=si,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                            nearest_legal_star=li,symmetric_difference=distance,added=added,removed=removed))
    output = dict(scope='Descriptive nearest-star profiles, not exclusions or realizability evidence',
                  parent_to_pose=parent_ids,pose_dimensions=dimensions,results=results,
                  symmetric_difference_counts=dict(counts),maximum_difference_dimension_counts=dict(max_dimensions),
                  additional_poses=[boundary['parents'][parent_ids.index(i)] for i in range(len(atlas),len(poses))],
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',ROOT/'audit_closed_atlas.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_defect_profiles.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),distance_counts=dict(counts),maximum_dimension_counts=dict(max_dimensions))),flush=True)


if __name__ == '__main__':
    main()

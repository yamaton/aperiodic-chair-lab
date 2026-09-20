"""Q018 follow-up: check the actual tiles selected by incidence assignments.

Selected stars force all their neighbor supports. A non-atlas intersection
between any two invalidates that assignment, not every assignment of the
parent case. Collision pairs are retained for a subsequent stronger SAT run.
"""

import hashlib
import json
from collections import defaultdict
from functools import cache
from pathlib import Path

from geometry import F,mm,mv,mul,add,I,ZERO,vertices,inside,inverse_point,encode
from contact_atlas import relative
from closed_stars import bins,disjoint
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','expanded_arcs_2_seed.json','neighbor_incidence_sat.json')]
    atlas_raw,language,source,sat = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    atlas_set = set(atlas)
    d = sat['pose_key_denominator']
    scale = F(sat['tile_scale'])
    poses = [(tuple(tuple(F(key[3*i+j],d) for j in range(3)) for i in range(3)),
              tuple(scale*F(v,d) for v in key[9:]),scale) for key in sat['normalized_pose_keys']]
    index = {p:i for i,p in enumerate(poses)}
    assert len(index) == len(poses)
    world = {}
    @cache
    def rotated(r,q):
        a = atlas[q]
        assert a[2] == 1
        return mm(r,a[0]),mul(scale,mv(r,a[1]))
    @cache
    def neighbor(tile,q):
        if tile not in world:
            world[tile] = raw_pose(source['poses'][tile])
        p = world[tile]
        assert p[2] == scale
        r,t = rotated(p[0],q)
        return index[r,add(p[1],t),scale]
    @cache
    def box(i):
        vs = vertices(poses[i])
        return tuple((min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3))
    @cache
    def cells(i):
        return tuple(bins(box(i),scale))
    safe = set()
    bad = {}
    witnesses = []
    results = []
    n = len(poses)
    for mi,model in enumerate(sat['results']):
        if model['status'] != 'sat':
            continue
        source_row = source['results'][model['source_index']]
        domain_ids = dict(source_row['domains'])
        selected = dict(model['selected_stars'])
        assert set(selected) == set(domain_ids)
        active = set()
        centers = set()
        for tile,s in selected.items():
            assert s in source['domain_pool'][domain_ids[tile]]
            if tile not in world:
                world[tile] = raw_pose(source['poses'][tile])
            centers.add(index[world[tile]])
            active.update(neighbor(tile,q) for q in language['stars'][s]['neighbors'])
        assert centers <= active
        grid = defaultdict(list)
        for i in sorted(active):
            for cell in cells(i):
                grid[cell].append(i)
        failure = None
        checked = 0
        # Optional outer supports are the new information in this test.
        order = sorted(active-centers)+sorted(centers)
        for i in order:
            candidates = sorted({j for cell in cells(i) for j in grid[cell] if j != i})
            for j in candidates:
                key = min(i,j)*n+max(i,j)
                if key in safe:
                    continue
                if key in bad:
                    failure = bad[key]
                    break
                if disjoint(box(i),box(j)):
                    safe.add(key)
                    continue
                q = relative(poses[i],poses[j])
                checked += 1
                if q in atlas_set:
                    safe.add(key)
                    continue
                points = edge_points(q,first_only=True)
                if points:
                    assert all(inside(p) and inside(inverse_point(q,p)) for p in points)
                    failure = len(witnesses)
                    bad[key] = failure
                    witnesses.append(dict(positions=(i,j),relative_pose=q,common_points=sorted(points)))
                    break
                safe.add(key)
            if failure is not None:
                break
        result = dict(model_index=mi,source_index=model['source_index'],boundary_index=model['boundary_index'],
                      cover_index=model['cover_index'],forced_centers=len(centers),selected_supports=len(active),
                      status='selected_assignment_has_forbidden_pair' if failure is not None else 'no_pair_obstruction_found',
                      checked_new_bounding_pairs=checked,active_positions=sorted(active))
        if failure is not None:
            result['witness'] = failure
        results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k != 'active_positions'}),flush=True)
    output = dict(scope='Geometry of selected finite incidence assignments; collisions reject assignments, not parent cases',
                  results=results,witnesses=witnesses,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'closed_stars.py',ROOT/'reflected_controls.py',
                            ROOT/'audit_closed_atlas.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'incidence_model_geometry.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')


if __name__ == '__main__':
    main()

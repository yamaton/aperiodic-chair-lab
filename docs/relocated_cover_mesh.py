"""Render the exact proportions of the movable-anchor dimension witness.

Each face is divided into eight reflection wedges. A triangular curved cap
and three flat strips fill each wedge, without overlapping square cutouts.
The mesh approximates the cubic surface; it is not a certified exact solid.
"""
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np

from triangular_cover_mesh import patch, export
from build_recut_visualization import data_from_frozen

ROOT = Path(__file__).resolve().parents[1]
DIVISIONS = 48


def cross2(a, b):
    return a[0]*b[1]-a[1]*b[0]


def area(poly):
    return sum(cross2(a, b) for a, b in zip(poly, poly[1:]+poly[:1]))/2


def flat_ring(inner, outer, divisions):
    """Fill the region between two CCW triangles, keeping every inner edge vertex."""
    inner, outer = np.array(inner), np.array(outer)
    parts = []
    for i in range(3):
        j = (i+1) % 3
        edge = [inner[j]+(inner[i]-inner[j])*k/divisions for k in range(divisions+1)]
        polygon = [outer[i], outer[j], *edge]
        # A wedge corner may lie on an inner edge's continuation. Choose
        # the other outer corner as fan apex, avoiding zero-area triangles.
        for start in (0, 1):
            loop = polygon[start:]+polygon[:start]
            tris = [[loop[0], a, b] for a, b in zip(loop[1:], loop[2:])]
            if all(cross2(t[1]-t[0], t[2]-t[0]) > 1e-14 for t in tris):
                parts.extend(tris)
                break
        else:
            raise AssertionError('Strip is not a valid positive fan')
    got = sum(cross2(t[1]-t[0], t[2]-t[0])/2 for t in parts)
    expected = area(list(outer))-area(list(inner))
    assert abs(got-expected) < 1e-12
    return [([np.array([x, y, 0.]) for x, y in tri], 0) for tri in parts]


def mesh_audit(path):
    """Check a welded, oriented, closed triangular surface, including seams."""
    mesh = np.load(path)
    vertices, faces = mesh['vertices'], mesh['faces']
    edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    directions = np.where(edges[:, 0] < edges[:, 1], 1, -1)
    unique, inverse, counts = np.unique(np.sort(edges, axis=1), axis=0,
                                         return_inverse=True, return_counts=True)
    assert np.all(counts == 2), dict(zip(*np.unique(counts, return_counts=True)))
    assert np.all(np.bincount(inverse, weights=directions) == 0)
    assert len(vertices)-len(unique)+len(faces) == 2
    p, q, r = (vertices[faces[:, i]] for i in range(3))
    assert np.all(np.linalg.norm(np.cross(q-p, r-p), axis=1) > 1e-13)
    volume = np.einsum('ij,ij->i', p, np.cross(q, r)).sum()/6
    assert volume > 0
    return dict(vertices=len(vertices), triangles=len(faces), edges=len(unique),
                every_edge_has_two_oppositely_directed_incidents=True,
                euler_characteristic=2, oriented_mesh_volume=float(volume))


def detail_mesh(port, width, depth, magnification):
    # A padded triangular crop entirely inside the actual port's wedge.
    inner = np.array([[-width, -width], [width, -width], [-width, 0.]])
    centroid = inner.mean(axis=0)
    outer = centroid+(inner-centroid)*1.125
    parts = [(ps, kind) for ps, kind in patch(port['key'], width, depth, 80) if kind]
    parts += flat_ring(inner, outer, 80)
    bottom = -max(width*.384, abs(port['key'])*depth*1.5)
    for a, b in zip(outer, np.roll(outer, -1, axis=0)):
        q = [np.array([*a, 0.]), np.array([*a, bottom]),
             np.array([*b, bottom]), np.array([*b, 0.])]
        parts.extend(([q[i] for i in ids], 0) for ids in ((0, 1, 2), (0, 2, 3)))
    parts.append(([np.array([*p, bottom]) for p in reversed(outer)], 0))
    chi = port['v_sign']
    transformed = []
    for ps, kind in parts:
        points = [(p-np.array([*centroid, 0.]))*np.array([1, chi, 1])*magnification for p in ps]
        if chi < 0:
            points.reverse()
        transformed.append((points, kind))
    return transformed


def prepare_relocated(folder):
    source_path = ROOT/'strong/audit/triangular_v1/candidate.json'
    evidence_path = ROOT/'strong/audit/port_dimensions.json'
    raw = source_path.read_bytes()
    source = json.loads(raw)
    evidence = json.loads(evidence_path.read_text())
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == evidence['source_candidate_sha256']
    witness = evidence['witness']
    a, b, w, depth = (Q(witness[k]) for k in ('a', 'b', 'width', 'height_unit'))
    assert (a, b, w, depth) == (Q(-1, 4), Q(7, 32), Q(3, 16), Q(1, 16))
    assert Q(witness['curved_zone_certificate']['uniform_clearance_lower_bound']) > 0
    assert Q(witness['maximum_depth']) == 2*depth < Q(1, 4)
    # Exact planar area and padded-crop containment before floating meshing.
    inner = [(a+w*u, b+w*v) for u, v in ((-1, -1), (1, -1), (-1, 0))]
    outer = [(Q(-1, 2), Q(0)), (Q(0), Q(0)), (Q(-1, 2), Q(1, 2))]
    assert area(inner) == w*w and area(outer) == Q(1, 8)
    centroid = tuple(sum(p[i] for p in inner)/3 for i in range(2))
    crop = [tuple(centroid[i]+Q(9, 8)*(p[i]-centroid[i]) for i in range(2)) for p in inner]
    assert all(Q(-1, 2) < x < -y < 0 for x, y in crop)

    records, faces = [], defaultdict(list)
    for index, p in enumerate(source['ports']):
        U, V, N = (tuple(p[k]) for k in ('u_axis', 'v_axis', 'outward_normal'))
        f = tuple(Q(x)-Q(3*u+v, 16) for x, u, v in zip(p['center'], U, V))
        center = tuple(f[i]+a*U[i]+b*V[i] for i in range(3))
        rec = dict(index=index, center=center, f=f, u=U, v=V, n=N, key=p['signed_key'])
        records.append(rec)
        faces[f, N].append(rec)
    assert len(faces) == 24 and all(len(ps) == 8 for ps in faces.values())
    assert sum(p['key'] for p in records) == 0
    flat = flat_ring(np.array(inner, dtype=float), np.array(outer, dtype=float), DIVISIONS)
    parts, error = [], 0.
    for (f, N), ports in faces.items():
        assert len({(p['u'], p['v']) for p in ports}) == 8
        # Ordered signed axes exhaust the eight distinct reflection wedges.
        for p in ports:
            U, V, N, f = (np.array(p[k], dtype=float) for k in ('u', 'v', 'n', 'f'))
            center = np.array(p['center'], dtype=float)
            for local, kind in flat:
                points = [f+q[0]*U+q[1]*V for q in local]
                if np.dot(np.cross(points[1]-points[0], points[2]-points[0]), N) < 0:
                    points.reverse()
                parts.append((points, kind))
            for local, kind in patch(p['key'], float(w), float(depth), DIVISIONS):
                if not kind:
                    continue
                points = [center+q[0]*U+q[1]*V+q[2]*N for q in local]
                for q in points:
                    displacement = q-center
                    x = (np.dot(displacement, U)/float(w)+1)/2
                    y = np.dot(displacement, V)/float(w)+1
                    expected = p['key']*float(depth)*27*x*y*(1-x-y)
                    error = max(error, abs(np.dot(displacement, N)-expected))
                if np.dot(np.cross(points[1]-points[0], points[2]-points[0]), N) < 0:
                    points.reverse()
                parts.append((points, kind))
    assert error < 1e-12
    export(folder/'chair.npz', parts)
    whole = mesh_audit(folder/'chair.npz')
    assert abs(whole['oriented_mesh_volume']-7) < 1e-10

    occurrences, cells = defaultdict(list), []
    for child_index, child in enumerate(source['children']):
        def rotate(p):
            return tuple(sum(Q(x)*y for x, y in zip(row, p)) for row in child['matrix'])
        for p in records:
            center = tuple(x+y for x, y in zip(child['center'], rotate(p['center'])))
            occurrences[center].append(dict(child_index=child_index, source_port_index=p['index'],
                center=center, key=p['key'], u=rotate(p['u']), v=rotate(p['v']), n=rotate(p['n'])))
        for cube in source['coarse_cubes']:
            corners = [tuple(child['center'][i]+sum(child['matrix'][i][j]*(cube[j]+bit[j]) for j in range(3))
                             for i in range(3)) for bit in product((0, 1), repeat=3)]
            cells.append(tuple(min(q[i] for q in corners) for i in range(3)))
    expected = {tuple(2*c+d for c, d in zip(cube, bit)) for cube in source['coarse_cubes'] for bit in product((0, 1), repeat=3)}
    assert len(cells) == len(set(cells)) == 56 and set(cells) == expected
    contacts = [ps for _, ps in sorted(occurrences.items()) if len(ps) == 2]
    assert len(contacts) == 384 and all(a['key'] == -b['key'] and a['u'] == b['u'] and a['v'] == b['v']
        and a['n'] == tuple(-x for x in b['n']) for a, b in contacts)
    # Retain the previous cover's actual pair, now at the relocated anchor.
    paired = sorted(next(ps for ps in contacts if {p['source_port_index'] for p in ps} == {40, 56}
                         and {p['child_index'] for p in ps} == {6, 7}), key=lambda p: -p['key'])
    def point(p, x, y):
        u, v = 2*x-1, y-1
        height = p['key']*depth*27*x*y*(1-x-y)
        return tuple(p['center'][i]+w*(u*p['u'][i]+v*p['v'][i])+height*p['n'][i] for i in range(3))
    for i in range(13):
        for j in range(13-i):
            assert point(paired[0], Q(i, 12), Q(j, 12)) == point(paired[1], Q(i, 12), Q(j, 12))

    data = data_from_frozen()
    assert data['placements']['eight'] == source['children']
    data.update(profile='triangular', variant='relocated', width=float(w), depth=float(depth),
                anchor_offsets=[str(a), str(b)], detail_magnification=8/3,
                feature_width_multiplier=1, feature_depth_multiplier=1)
    data['detail_ports'] = [dict(key=p['key'], v_sign=int(np.dot(np.cross(p['n'], p['u']), p['v']))) for p in paired]
    details = []
    for i, p in enumerate(data['detail_ports']):
        export(folder/f'detail-{i}.npz', detail_mesh(p, float(w), float(depth), data['detail_magnification']))
        details.append(mesh_audit(folder/f'detail-{i}.npz'))
    (folder/'scene.json').write_text(json.dumps(data))
    return dict(design='Relocated common-offset witness from PORT_DIMENSIONS.md',
        source_candidate_file=str(source_path.relative_to(ROOT)), source_candidate_sha256=digest,
        dimension_evidence_file=str(evidence_path.relative_to(ROOT)),
        dimension_evidence_sha256=hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
        anchor_offsets=[str(a), str(b)], rendered_width_parameter=str(w), rendered_height_unit=str(depth),
        feature_reach_bound=str(2*depth), design_width_relative_to_recorded_snapshot='12',
        design_depth_relative_to_recorded_snapshot='256', additional_feature_display_scaling=False,
        minimum_face_edge_margin='1/16', curved_zone_clearance_lower_bound='5/256',
        cap_edge_divisions=DIVISIONS, cap_triangles=192*DIVISIONS**2,
        maximum_sampled_surface_error=error, chair_mesh=whole, detail_meshes=details,
        flat_face_method='Eight wedges, each filled by one triangular cap and three flat polygon strips',
        flat_and_curved_projected_area_per_face='1', exact_wedge_area='1/8', exact_cap_area=str(w*w),
        retains_middle_half_of_carrier_cubes=True, vertex_coordinate_rounding_digits=12,
        contact_source_port_indices=[p['source_port_index'] for p in paired],
        contact_child_indices=[p['child_index'] for p in paired], contact_signed_keys=[p['key'] for p in paired],
        contact_frame_anchor=list(map(str, paired[0]['center'])), checked_internal_port_pairs=len(contacts),
        contact_shared_frames_and_opposite_keys=True, exact_contact_samples=91,
        detail_edge_divisions=80, detail_crop='Triangle expanded by 9/8 about its centroid; artificial backing and sides',
        detail_crop_inside_actual_port_wedge=True, detail_frames_properly_reoriented=True,
        eight_children_partition_scale_two_carrier=True, coarse_cells=56)

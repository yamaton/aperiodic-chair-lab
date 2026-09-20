"""Coordinate-derived triangular cap meshes for the Blender cover.

Only the rendering samples are approximate. Exact rational checks verify
the selected contact and the disclosed feature-box bounds before rendering.
"""
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'strong'))
from build_recut_visualization import data_from_frozen, face_mesh


def patch(key, width, depth, divisions):
    """Triangles filling the old square: cubic triangle plus its flat rest."""
    def point(i, j):
        x, y = i/divisions, j/divisions
        return np.array([width*(2*x-1), width*(y-1),
                         key*depth*27*x*y*max(0, 1-x-y)])
    result = []
    kind = 1 if key > 0 else 2
    for i in range(divisions):
        for j in range(divisions-i):
            result.append(([point(i,j), point(i+1,j), point(i,j+1)], kind))
            if i+j < divisions-1:
                result.append(([point(i+1,j), point(i+1,j+1), point(i,j+1)], kind))
    assert len(result) == divisions**2
    diagonal = [np.array([width*(1-2*j/divisions), width*(-1+j/divisions), 0.])
                for j in range(divisions+1)]
    diagonal.append(np.array([-width, width, 0.]))
    corner = np.array([width, width, 0.])
    result.extend(([corner, b, a], 0) for a, b in zip(diagonal, diagonal[1:]))
    areas = [(np.cross(ps[1]-ps[0],ps[2]-ps[0])[2]/2, kind) for ps,kind in result]
    assert all(area > 0 for area,_ in areas)
    assert np.isclose(sum(area for area,kind in areas if kind), width**2, rtol=1e-12, atol=0)
    assert np.isclose(sum(area for area,_ in areas), 4*width**2, rtol=1e-12, atol=0)
    return result


def export(path, parts):
    vertices, inverse = np.unique(np.round(np.array([p for p, _ in parts]).reshape(-1,3), 12),
                                  axis=0, return_inverse=True)
    np.savez_compressed(path, vertices=vertices, faces=inverse.reshape(-1,3),
                        kinds=[kind for _, kind in parts])
    return len(vertices), len(parts)


def detail_mesh(port, width, depth, magnification):
    """Crop reoriented by a proper motion; no change of the cap profile."""
    parts = patch(port['key'], width, depth, 80)
    edge = width*1.45
    # Four planar ring pieces around the old square, then artificial cut walls.
    inner = [(-width,-width), (width,-width), (width,width), (-width,width)]
    outer = [(-edge,-edge), (edge,-edge), (edge,edge), (-edge,edge)]
    bottom = -max(width*.384, abs(port['key'])*depth*1.5)
    def quad(points):
        parts.extend(([np.array(points[i]) for i in indices], 0)
                     for indices in ((0,1,2),(0,2,3)))
    for i in range(4):
        j = (i+1)%4
        quad([(*outer[i],0), (*outer[j],0), (*inner[j],0), (*inner[i],0)])
        quad([(*outer[j],0), (*outer[i],0), (*outer[i],bottom), (*outer[j],bottom)])
    quad([(*q,bottom) for q in reversed(outer)])
    # Original local frame has determinant chi. Display frame (X,chi*Y,Z)
    # has the same determinant, so their correspondence is a proper rotation.
    chi = port['v_sign']
    transformed = []
    for points, kind in parts:
        ps = [np.array(p)*np.array([1,chi,1])*magnification for p in points]
        if chi < 0:
            ps.reverse()
        transformed.append((ps, kind))
    return transformed


def prepare_triangular(folder, width_scale, depth_scale):
    snapshot = ROOT/'strong/audit/triangular_v1'
    raw = (snapshot/'candidate.json').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((snapshot/'manifest.json').read_text())['candidate_sha256']
    source = json.loads(raw)
    assert source['port_profile']['normalized_vertices'] == [[-1,-1],[1,-1],[-1,0]]
    assert source['port_profile']['polynomial'] == '27*lambda0*lambda1*lambda2'
    data = data_from_frozen()
    assert data['candidate_sha256'] == source['reference_candidate_sha256']
    assert data['placements']['eight'] == source['children']
    lookup = {(tuple(map(Q,p['center'])), tuple(p['outward_normal'])): p for p in source['ports']}
    for face in data['faces']:
        for port in face['ports']:
            p = lookup[tuple(map(Q,port['center'])), tuple(face['normal'])]
            assert port['u'] == p['u_axis'] and port['v'] == p['v_axis']
            port['key'] = p['signed_key']
    width, depth = Q(source['half_width'])*width_scale, Q(source['height_unit'])*depth_scale
    reach, margin = 2*depth, Q(5,16)-width
    gaps = {'same_unit_face':Q(1,8)-2*width, 'coplanar_faces':2*margin,
            'parallel_planes':1-2*reach, 'perpendicular_faces':margin-reach}
    assert min(gaps.values()) > 0 and reach < Q(1,4)
    data.update(profile='triangular', candidate_sha256=digest, width=float(width), depth=float(depth),
                feature_width_multiplier=width_scale, feature_depth_multiplier=depth_scale,
                detail_magnification=32/width_scale)
    parts, error, caps = [], 0., 0
    for face in data['faces']:
        normal = np.array(face['normal'])
        # Reuse only the carrier's flat strips; replace every square cap.
        for points, kind in face_mesh(face, float(width), 0, 1):
            if kind == 0:
                parts.extend(([points[i] for i in indices], 0) for indices in ((0,1,2),(0,2,3)))
        for port in face['ports']:
            center, u, v = (np.array(port[s]) for s in ('center','u','v'))
            for local, kind in patch(port['key'], float(width), float(depth), 24):
                points = [center+p[0]*u+p[1]*v+p[2]*normal for p in local]
                if np.dot(np.cross(points[1]-points[0],points[2]-points[0]),normal) < 0:
                    points.reverse()
                if kind:
                    caps += 1
                    for p in points:
                        displacement = p-center
                        x = (np.dot(displacement,u)/float(width)+1)/2
                        y = np.dot(displacement,v)/float(width)+1
                        assert min(x,y,1-x-y) > -1e-12
                        expected = port['key']*float(depth)*27*x*y*(1-x-y)
                        error = max(error,abs(np.dot(displacement,normal)-expected))
                parts.append((points,kind))
    assert caps == 192*24**2 and error < 1e-12
    vertex_count, triangle_count = export(folder/'chair.npz',parts)

    occurrences, cells = defaultdict(list), []
    for child_index, child in enumerate(source['children']):
        def rotate(p):
            return tuple(sum(Q(a)*b for a,b in zip(row,p)) for row in child['matrix'])
        for port_index,p in enumerate(source['ports']):
            center = tuple(a+b for a,b in zip(child['center'],rotate(tuple(map(Q,p['center'])))))
            occurrences[center].append(dict(child_index=child_index, source_port_index=port_index,
                center=center,key=p['signed_key'],u=rotate(p['u_axis']),v=rotate(p['v_axis']),
                n=rotate(p['outward_normal'])))
        for cube in source['coarse_cubes']:
            corners = [tuple(a+b for a,b in zip(child['center'],rotate(tuple(c+d for c,d in zip(cube,bit)))))
                       for bit in product((0,1),repeat=3)]
            cells.append(tuple(min(q[i] for q in corners) for i in range(3)))
    expected = {tuple(2*c+d for c,d in zip(cube,bit)) for cube in source['coarse_cubes'] for bit in product((0,1),repeat=3)}
    assert len(cells) == len(set(cells)) == 56 and set(cells) == expected
    contacts = [ps for _,ps in sorted(occurrences.items()) if len(ps)==2]
    assert contacts and all(a['key']==-b['key'] and a['u']==b['u'] and a['v']==b['v']
                           and a['n']==tuple(-x for x in b['n']) for a,b in contacts)
    paired = sorted(next(ps for ps in contacts if abs(ps[0]['key'])==2),key=lambda p:-p['key'])
    def point(p,x,y):
        u,v = 2*x-1,y-1
        height = p['key']*depth*27*x*y*(1-x-y)
        return tuple(p['center'][i]+width*(u*p['u'][i]+v*p['v'][i])+height*p['n'][i] for i in range(3))
    sample_count = 0
    for i in range(13):
        for j in range(13-i):
            assert point(paired[0],Q(i,12),Q(j,12)) == point(paired[1],Q(i,12),Q(j,12))
            sample_count += 1
    data['detail_ports'] = [dict(key=p['key'],v_sign=int(np.dot(np.cross(p['n'],p['u']),p['v']))) for p in paired]
    for i,p in enumerate(data['detail_ports']):
        assert p['v_sign'] == (1 if p['key']>0 else -1)
        export(folder/f'detail-{i}.npz', detail_mesh(p,float(width),float(depth),data['detail_magnification']))
    (folder/'scene.json').write_text(json.dumps(data))
    return dict(candidate_sha256=digest,candidate_file='strong/audit/triangular_v1/candidate.json',
        profile='scalene triangle cubic bubble',ports=192,unit_faces=24,signed_depth_keys=[-2,-1,1,2],
        feature_width_multiplier=width_scale,feature_depth_multiplier=depth_scale,
        rendered_width_parameter=str(width),rendered_height_unit=str(depth),feature_reach_bound=str(reach),
        minimum_face_edge_margin=str(margin),feature_box_separation_bounds={k:str(v) for k,v in gaps.items()},
        retains_middle_half_of_carrier_cubes=True,cap_edge_divisions=24,cap_triangles=caps,
        mesh_vertices=vertex_count,mesh_triangles=triangle_count,maximum_sampled_surface_error=error,
        patch_projected_area_checked=True,triangle_support_area_fraction_of_old_square='1/4',
        vertex_coordinate_rounding_digits=12,contact_source_port_indices=[p['source_port_index'] for p in paired],
        contact_child_indices=[p['child_index'] for p in paired],contact_signed_keys=[p['key'] for p in paired],
        contact_frame_anchor=list(map(str,paired[0]['center'])),contact_shared_frames_and_opposite_keys=True,
        exact_contact_samples=sample_count,checked_internal_port_pairs=len(contacts),
        detail_edge_divisions=80,detail_frames_properly_reoriented=True,
        eight_children_partition_scale_two_carrier=True,coarse_cells=56)

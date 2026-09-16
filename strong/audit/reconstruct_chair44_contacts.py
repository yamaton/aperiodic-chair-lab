#!/usr/bin/env python3
"""Reconstruct registered panel contacts from Chair44's rational pyramid geometry.

Reads released JSON as data only. Does not import or run released implementation.
Uses all 48 signed cubic frames, including reflections. This is a grid-model
check, not a proof that arbitrary physical tilings are registered.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def apply(matrix, point):
    return tuple(sum(x * y for x, y in zip(row, point)) for row in matrix)


def matrix(frame):
    perm, signs = frame
    return tuple(tuple(signs[i] if j == perm[i] else 0 for j in range(3)) for i in range(3))


def frames():
    for perm in itertools.permutations(range(3)):
        parity = (-1) ** sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
        for signs in itertools.product((-1, 1), repeat=3):
            yield matrix((perm, signs)), parity * signs[0] * signs[1] * signs[2]


def cell_image(rotation, cube):
    # The lower corner is the coordinatewise minimum of all eight image corners.
    corners = [apply(rotation, add(cube, offset)) for offset in itertools.product((0, 1), repeat=3)]
    return tuple(min(p[i] for p in corners) for i in range(3))


def expose(cubes):
    faces = {}
    for cube in cubes:
        for axis in range(3):
            for sign in (-1, 1):
                normal = tuple(sign if i == axis else 0 for i in range(3))
                if add(cube, normal) not in cubes:
                    center8 = tuple(8 * cube[i] + 4 + 4 * normal[i] for i in range(3))
                    faces[center8, normal] = {}
    return faces


def main():
    if not __debug__:
        raise SystemExit('Run without -O: this audit requires assertions.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    solid_path = args.release_root / 'solid/r44_solid.json'
    atlas_path = args.release_root / 'certificates/candidate_certificate.json'
    solid = json.loads(solid_path.read_text())
    cubes = set(map(tuple, solid['base_unit_cubes']))
    assert len(cubes) == 7
    panels = expose(cubes)
    assert len(panels) == 24
    eta, height = F(solid['base_halfwidth']), F(solid['height_unit'])
    assert eta == F(1, 100) and height == F(1, 10000)
    vertices = [tuple(map(F, p)) for p in solid['vertices']]
    vertex_index = {p: i for i, p in enumerate(vertices)}
    assert len(vertex_index) == len(vertices)
    triangles = {frozenset(t) for t in solid['triangles']}
    role_geometry = []
    for patch in solid['patches']:
        base = [tuple(map(F, p)) for p in patch['base']]
        apex = tuple(map(F, patch['apex']))
        key = patch['coefficient']
        assert 1 <= abs(key) <= 12
        assert key == solid['profile'][patch['role']]
        center = tuple(sum(p[i] for p in base) / 4 for i in range(3))
        normal = tuple((apex[i] - center[i]) / (key * height) for i in range(3))
        assert sorted(map(abs, normal)) == [0, 0, 1]
        axis = next(i for i in range(3) if normal[i])
        tangent = [i for i in range(3) if i != axis]
        expected_base = set()
        for signs in itertools.product((-1, 1), repeat=2):
            p = list(center)
            for i, sign in zip(tangent, signs):
                p[i] += eta * sign
            expected_base.add(tuple(p))
        assert set(base) == expected_base and len(base) == 4
        # Every pyramid facet appears in the actual mesh (orientation not audited).
        for i in range(4):
            tri = frozenset(vertex_index[p] for p in (apex, base[i], base[(i + 1) % 4]))
            assert tri in triangles
        owners = []
        for (face8, face_normal), ports in panels.items():
            if normal == face_normal and center[axis] == F(face8[axis], 8):
                if all(abs(center[i] - F(face8[i], 8)) + eta < F(1, 2) for i in tangent):
                    owners.append((face8, face_normal))
        assert len(owners) == 1
        center8 = tuple(8 * x for x in center)
        assert all(x.denominator == 1 for x in center8)
        center8 = tuple(map(int, center8))
        ports = panels[owners[0]]
        assert center8 not in ports
        ports[center8] = key
        role_geometry.append((patch['role'], owners[0], center8, key))
    assert len(role_geometry) == 192 and {x[0] for x in role_geometry} == set(range(192))
    assert all(len(ports) == 8 for ports in panels.values())

    accepted = set()
    counts = {1: {'geometric_contacts': 0, 'matching_contacts': 0},
              -1: {'geometric_contacts': 0, 'matching_contacts': 0}}
    by_frame = []
    for rotation, determinant in frames():
        moved_cubes = {cell_image(rotation, q) for q in cubes}
        moved_panels = {(apply(rotation, center8), apply(rotation, normal)):
                        {apply(rotation, p): key for p, key in ports.items()}
                        for (center8, normal), ports in panels.items()}
        shifts = set()
        for a, an in panels:
            for b, bn in moved_panels:
                if an == neg(bn):
                    shift8 = add(a, neg(b))
                    assert all(v % 8 == 0 for v in shift8)
                    shifts.add(tuple(v // 8 for v in shift8))
        geometric_count = matching_count = 0
        for shift in sorted(shifts):
            if cubes & {add(q, shift) for q in moved_cubes}:
                continue
            geometric_count += 1
            shift8 = tuple(8 * v for v in shift)
            matched_panels = 0
            fits = True
            for (center8, normal), ports in moved_panels.items():
                owner = (add(center8, shift8), neg(normal))
                if owner not in panels:
                    continue
                matched_panels += 1
                expected = {add(p, shift8): -key for p, key in ports.items()}
                if panels[owner] != expected:
                    fits = False
                    break
            assert matched_panels > 0
            if fits:
                matching_count += 1
                accepted.add((rotation, shift))
        counts[determinant]['geometric_contacts'] += geometric_count
        counts[determinant]['matching_contacts'] += matching_count
        by_frame.append({'matrix': rotation, 'determinant': determinant,
                         'geometric_contacts': geometric_count, 'matching_contacts': matching_count})

    # Read the claimed atlas only AFTER independently constructing every contact.
    certificate = json.loads(atlas_path.read_text())
    claimed = {(matrix(g), tuple(t)) for g, t in certificate['legal_contacts']}
    assert len(claimed) == len(certificate['legal_contacts']) == 44
    assert accepted == claimed
    assert counts[1] == {'geometric_contacts': 1194, 'matching_contacts': 44}
    assert counts[-1] == {'geometric_contacts': 1194, 'matching_contacts': 0}
    output = {
        'scope': 'Independent reconstruction of registered full-panel matching from rational pyramid bases/apices, all 48 frames. Not arbitrary-placement enforcement or a mesh boundary audit.',
        'source_hashes': {str(p.relative_to(args.release_root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (solid_path, atlas_path)},
        'carrier_cubes': 7, 'exposed_panels': 24, 'features': 192,
        'pyramid_facets_found_in_mesh': 768,
        'proper': counts[1], 'improper': counts[-1],
        'published_atlas_exactly_recovered': True,
        'by_frame': by_frame,
        'accepted': [{'matrix': r, 'shift': t} for r, t in sorted(accepted)],
    }
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k not in ('by_frame', 'accepted')}, indent=2))


if __name__ == '__main__':
    main()

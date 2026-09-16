#!/usr/bin/env python3
"""Compare Chair44 JSON/CSV data with our frozen chair; never execute release code.

Uses exact integer/rational arithmetic and Python's standard library only.
Run from the project root with uv run --locked python <this script> --release-root ...
"""
import argparse
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def matrix(frame):
    perm, signs = frame
    return tuple(tuple(signs[i] if j == perm[i] else 0 for j in range(3)) for i in range(3))


def apply(mat, vec):
    return tuple(sum(u * v for u, v in zip(row, vec)) for row in mat)


def multiply(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def transpose(mat):
    return tuple(zip(*mat))


def main():
    if not __debug__:
        raise SystemExit('Run without -O: exact comparison requires assertions.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-root', required=True, type=Path)
    parser.add_argument('--our-root', default=Path.cwd(), type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    release, ours = args.release_root.resolve(), args.our_root.resolve()
    names = {
        'ours': ['strong/audit/frozen_v1/candidate.json', 'strong/audit/coordinate_certificate.json', 'strong/audit/face_motifs.json'],
        'release': ['certificates/candidate_certificate.json', 'solid/r44_solid.json', 'solid/native_panels.csv'],
    }
    hashes = {label: {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names[label]} for label, root in [('ours', ours), ('release', release)]}
    candidate = read(ours / names['ours'][0])
    certificate = read(ours / names['ours'][1])
    motifs = read(ours / names['ours'][2])
    other = read(release / names['release'][0])
    solid = read(release / names['release'][1])
    with (release / names['release'][2]).open(newline='') as handle:
        panels = list(csv.DictReader(handle))
    P = matrix(((1, 2, 0), (1, 1, 1)))
    assert multiply(P, transpose(P)) == matrix(((0, 1, 2), (1, 1, 1)))

    def transformed_pose(frame, shift, source_center, target_center):
        mat = matrix(frame)
        return (multiply(multiply(P, mat), transpose(P)),
                apply(P, tuple(shift[i] + source_center * sum(mat[i]) - target_center for i in range(3))))

    def original_poses(key):
        return [(tuple(tuple(x[1][3 * i + j] for j in range(3)) for i in range(3)), tuple(x[0])) for x in certificate[key]]

    comparisons = {}

    def equal_sets(name, left, right, expected):
        left, right = list(left), list(right)
        assert len(left) == len(set(left)) == expected, (name, 'left count or duplicates')
        assert len(right) == len(set(right)) == expected, (name, 'right count or duplicates')
        assert set(left) == set(right), (name, 'unequal sets')
        comparisons[name] = {'our_count': len(left), 'release_count': len(right), 'sets_equal': True, 'no_duplicates': True}

    equal_sets('carrier_cubes', map(tuple, candidate['coarse_cubes']),
               (tuple(v - 1 for v in q) for q in solid['base_unit_cubes']), 7)
    equal_sets('children', ((tuple(map(tuple, q['matrix'])), tuple(q['center'])) for q in candidate['children']),
               (transformed_pose(g, t, 1, 2) for g, t in other['children']), 8)
    for their_key, our_key, center, count in [
        ('legal_contacts', 'legal_contacts', 1, 44),
        ('contact_states', 'closed_substitution_contacts', 1, 30),
        ('macro_legal', 'legal_macro_contacts', 2, 44),
    ]:
        equal_sets(our_key, original_poses(our_key),
                   (transformed_pose(g, t, center, center) for g, t in other[their_key]), count)

    ports = candidate['ports']
    by_center = {tuple(F(v) for v in p['center']): (i, p) for i, p in enumerate(ports)}
    assert len(by_center) == len(ports) == 192
    assert len(solid['patches']) == 192
    key_map, witnesses = {}, []
    for patch in solid['patches']:
        row = panels[patch['face']]
        assert int(row['panel']) == patch['face']
        axis = int(row['normal_axis'])
        normal = tuple(int(row['outward_sign']) if i == axis else 0 for i in range(3))
        facecenter = tuple(F(row['center_' + d]) for d in 'xyz')
        center = tuple(sum(F(q[i]) for q in patch['base']) / 4 for i in range(3))
        offset = tuple(center[i] - facecenter[i] for i in range(3))
        assert sorted(map(abs, offset)) == [0, F(1, 8), F(1, 4)]
        u = tuple(int(4 * d) if abs(d) == F(1, 4) else 0 for d in offset)
        v = tuple(int(8 * d) if abs(d) == F(1, 8) else 0 for d in offset)
        mapped_center = apply(P, tuple(facecenter[i] - 1 + F(3, 16) * u[i] + F(1, 16) * v[i] for i in range(3)))
        index, own = by_center[mapped_center]
        assert tuple(own['u_axis']) == apply(P, u)
        assert tuple(own['v_axis']) == apply(P, v)
        assert tuple(own['outward_normal']) == apply(P, normal)
        key, own_key = patch['coefficient'], own['signed_key']
        assert key == other['profile'][patch['role']] == solid['profile'][patch['role']]
        key_map.setdefault(abs(key), set()).add(own_key * (1 if key > 0 else -1))
        witnesses.append({'their_role': patch['role'], 'our_index': index, 'their_signed_key': key, 'our_signed_key': own_key})
    assert {w['their_role'] for w in witnesses} == set(range(192))
    assert {w['our_index'] for w in witnesses} == set(range(192))
    assert set(key_map) == set(range(1, 13))
    assert all(len(values) == 1 for values in key_map.values())
    assert {abs(next(iter(values))) for values in key_map.values()} == set(range(1, 13))

    # Independently recover our signed contact equations from frozen port coordinates.
    our_rows = set()
    for mat, shift in original_poses('closed_substitution_contacts'):
        for j, port in enumerate(ports):
            moved = apply(mat, tuple(F(x) for x in port['center']))
            moved = tuple(moved[i] + shift[i] for i in range(3))
            if moved not in by_center:
                continue
            i, q = by_center[moved]
            if apply(mat, port['outward_normal']) != tuple(-x for x in q['outward_normal']):
                continue
            assert apply(mat, port['u_axis']) == tuple(q['u_axis'])
            assert apply(mat, port['v_axis']) == tuple(q['v_axis'])
            our_rows.add((min(i, j), max(i, j), -1))
    role_map = {w['their_role']: w['our_index'] for w in witnesses}
    their_rows = [(min(role_map[i], role_map[j]), max(role_map[i], role_map[j]), sign) for i, j, sign in other['signed_rows']]
    equal_sets('signed_equations', our_rows, their_rows, 372)
    faces = {(tuple(f['center_times_2']), tuple(f['normal'])): f['motif'] for f in motifs['face_descriptors']}
    motif_map = []
    for row in panels:
        axis = int(row['normal_axis'])
        normal = tuple(int(row['outward_sign']) if i == axis else 0 for i in range(3))
        center2 = tuple(2 * (F(row['center_' + d]) - 1) for d in 'xyz')
        motif_map.append({'their_panel': int(row['panel']), 'our_motif': faces[(apply(P, center2), apply(P, normal))]})
    assert {m['their_panel'] for m in motif_map} == set(range(24))
    motif_counts = {m: sum(x['our_motif'] == m for x in motif_map) for m in 'ABC'}
    assert motif_counts == {'A': 8, 'B': 8, 'C': 8}
    out = {
        'source_hashes': hashes,
        'coordinate_maps': {
            'point': 'ours=P(theirs-(1,1,1)), P(x,y,z)=(y,z,x), determinant +1',
            'fine_contact': 'R_ours=P R P^-1; t_ours=P(t+R(1,1,1)-(1,1,1))',
            'child': 'R_ours=P R P^-1; t_ours=P(t+R(1,1,1)-2(1,1,1))',
            'macro_contact': 'R_ours=P R P^-1; t_ours=P(t+2R(1,1,1)-2(1,1,1))',
            'feature': 'Within each panel, preserve signs and short/long axes; change offset magnitudes 1/8->1/16 and 1/4->3/16, then apply point map.',
        },
        'exact_set_comparisons': comparisons,
        'port_comparison': {'count': 192, 'correspondence_bijective': True, 'reparameterized_centers_normals_u_v_match': True,
                            'signed_key_map': {str(k): next(iter(v)) for k, v in sorted(key_map.items())}, 'map_extended_to_negative_keys_oddly': True,
                            'absolute_key_map_bijective': True, 'witnesses': witnesses},
        'face_motif_correspondence': motif_map,
        'face_motif_counts': motif_counts,
        'physical_differences': {
            'ours': {'offset_magnitudes': ['1/16', '3/16'], 'half_width': candidate['half_width'], 'height_unit': candidate['height_unit'], 'cap_polynomial': candidate['cap_polynomial']},
            'release': {'offset_magnitudes': ['1/8', '1/4'], 'half_width': solid['base_halfwidth'], 'height_unit': solid['height_unit'], 'surface': 'square pyramids'},
        },
        'scope': 'Exact finite comparison of supplied data; not a verification of either physical-solid theorem, source provenance, or priority. No downloaded code was executed.',
    }
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'comparisons': comparisons, 'ports_bijective': True, 'motif_counts': motif_counts, 'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()

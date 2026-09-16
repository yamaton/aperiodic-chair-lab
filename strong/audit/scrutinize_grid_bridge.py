"""Adversarial arithmetic audit of the geometric grid-forcing hypotheses.

No project helper imports. Reads the frozen solid directly, independently
reconstructs its exposed faces/owners, and tests all periodic feature boxes.
The quantified geometric proof is in ../review/GEOMETRIC_GRID_SCRUTINY.md.
Run: uv run --locked python strong/audit/scrutinize_grid_bridge.py
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = '95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54'
ONE = (1, 1, 1)
ZERO = (0, 0, 0)


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def scale(k, a): return tuple(k*x for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def mv(r, v): return tuple(dot(row, v) for row in r)
def det(r):
    a, b, c = r
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def separation(a, b): return max(abs(a[0][i]-b[0][i])-a[1][i]-b[1][i] for i in range(3))
def lower(r, q): return scale(F(1, 2), sub(mv(r, add(scale(2, q), ONE)), ONE))


def run():
    raw = (HERE/'frozen_v1/candidate.json').read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED
    d = json.loads(raw)
    cells = set(map(tuple, d['coarse_cubes']))
    normals = tuple(tuple(s*int(i == a) for i in range(3)) for a in range(3) for s in (-1, 1))
    frames = [tuple(tuple(signs[i]*int(j == order[i]) for j in range(3)) for i in range(3))
              for order in permutations(range(3)) for signs in product((-1, 1), repeat=3)]
    assert len(frames) == 48
    w, delta = F(d['half_width']), F(d['height_unit'])
    alpha, beta = (F(d['cap_polynomial'][s]) for s in ('a', 'b'))
    assert (w, delta, alpha, beta) == (F(1, 64), F(1, 4096), F(1, 5), F(1, 7))
    h = max(abs(p['signed_key']) for p in d['ports'])*delta*(1+alpha+beta)
    assert h == F(141, 35840) and 0 < 2*h < F(1, 4)
    assert 12*(1+h)**2 < 16  # Diameter is less than four.
    face_owners = {(add(add(q, scale(F(1, 2), ONE)), scale(F(1, 2), n)), n): q
                   for q in cells for n in normals if add(q, n) not in cells}
    assert len(face_owners) == 24
    ports, per_face, chirality = [], defaultdict(list), defaultdict(set)
    for record in d['ports']:
        p = tuple(map(F, record['center']))
        u, v, n = (tuple(record[s]) for s in ('u_axis', 'v_axis', 'outward_normal'))
        assert all(a in normals for a in (u, v, n))
        assert dot(u, v) == dot(u, n) == dot(v, n) == 0
        f = sub(p, scale(F(1, 16), add(scale(3, u), v)))
        q = face_owners[f, n]  # Stronger than just checking half-integer parity.
        radius = tuple(h if n[i] else w for i in range(3))
        port = dict(p=p, u=u, v=v, n=n, f=f, owner=q, key=record['signed_key'], box=(p, radius))
        ports.append(port)
        per_face[f, n].append(port)
        chirality[port['key']].add(det((u, v, n)))
    assert len(ports) == 192 and set(per_face) == set(face_owners)
    expected_offsets = {(F(s*a, 16), F(t*b, 16)) for a, b in ((3, 1), (1, 3))
                        for s, t in product((-1, 1), repeat=2)}
    for (f, n), ps in per_face.items():
        tangent = [i for i in range(3) if not n[i]]
        assert len(ps) == 8
        assert {tuple(p['p'][i]-f[i] for i in tangent) for p in ps} == expected_offsets
    assert all(len(v) == 1 for v in chirality.values())
    assert all(chirality[k] == {-next(iter(chirality[-k]))} for k in chirality)

    # Coarse owners carry a common interior core before any tiling is assumed.
    cores = [(add(q, scale(F(1, 2), ONE)), (F(1, 4),)*3) for q in sorted(cells)]
    core_gaps = [separation(core, p['box']) for core in cores for p in ports]
    assert min(core_gaps) > 0
    edges = [(a, b) for a, b in combinations(sorted(cells), 2) if sum(abs(x-y) for x, y in zip(a, b)) == 1]
    reached = {next(iter(cells))}
    while True:
        new = reached | {b for a, b in edges if a in reached} | {a for a, b in edges if b in reached}
        if new == reached: break
        reached = new
    assert reached == cells
    corridor_gaps = []
    for a, b in edges:
        midpoint = scale(F(1, 2), add(add(a, b), ONE))
        radius = tuple(F(1, 4)+F(abs(a[i]-b[i]), 2) for i in range(3))
        corridor_gaps.extend(separation((midpoint, radius), p['box']) for p in ports)
    assert min(corridor_gaps) > 0

    count, poses, determinants = 0, set(), Counter()
    fractional_control = None
    for a, b in product(ports, repeat=2):
        if a['key'] != -b['key']: continue
        r = tuple(tuple(a['u'][i]*b['u'][j]+a['v'][i]*b['v'][j]-a['n'][i]*b['n'][j]
                        for j in range(3)) for i in range(3))
        t = sub(a['p'], mv(r, b['p']))
        assert r in frames and det(r) == 1
        assert all(x.denominator == 1 for x in t)
        assert add(mv(r, b['f']), t) == a['f']
        assert mv(r, b['n']) == scale(-1, a['n'])
        assert add(lower(r, b['owner']), t) == add(a['owner'], a['n'])
        poses.add((r, t)); count += 1; determinants[det(r)] += 1
        if fractional_control is None:
            # With equal polynomial coefficients, swapping tangent axes also
            # preserves a cap. It produces an off-grid local placement.
            swapped = tuple(tuple(a['v'][i]*b['u'][j]+a['u'][i]*b['v'][j]-a['n'][i]*b['n'][j]
                                  for j in range(3)) for i in range(3))
            shifted = sub(a['p'], mv(swapped, b['p']))
            assert any(x.denominator != 1 for x in shifted)
            assert det(swapped) == -1
            fractional_control = {'first_port': d['ports'][ports.index(a)],
                                  'second_port': d['ports'][ports.index(b)],
                                  'linear_part': swapped, 'determinant': det(swapped),
                                  'translation': list(map(str, shifted)),
                                  'scope': 'Local cap coincidence for the altered equal-coefficient polynomial with reflected copies allowed; no full tiling or proper-only counterexample claimed.'}
    assert count == 1536

    # The universal box family: 24 types modulo integer translations.
    templates = []
    for axis in range(3):
        tangent = [i for i in range(3) if i != axis]
        for offsets in sorted(expected_offsets):
            p = [F(0)]*3
            for i, off in zip(tangent, offsets): p[i] = F(1, 2)+off
            templates.append((tuple(p), tuple(h if i == axis else w for i in range(3)), axis))
    template_set = {(p, radii) for p, radii, _ in templates}
    transformed = 0
    for r, p in product(frames, ports):
        center = tuple(x % 1 for x in mv(r, p['p']))
        n = mv(r, p['n'])
        radii = tuple(h if n[i] else w for i in range(3))
        assert (center, radii) in template_set
        transformed += 1
    checks, minima, category_counts = 0, {}, Counter()
    for a, b, shift in product(templates, templates, product((-1, 0, 1), repeat=3)):
        moved = (add(b[0], shift), b[1])
        if a[:2] == moved: continue
        gap = separation(a[:2], moved)
        assert gap > 0
        if a[2] != b[2]: category = 'perpendicular_faces'
        elif shift[a[2]]: category = 'parallel_planes'
        elif shift == ZERO: category = 'same_unit_face'
        else: category = 'different_coplanar_faces'
        minima[category] = min(minima.get(category, gap), gap)
        category_counts[category] += 1
        checks += 1
    assert checks == 15528 and transformed == 9216
    # Outside these shifts a separating coordinate has center distance > 1;
    # the sum of any two box radii is <= 2*w < 1.
    assert h < w and 2*w < 1
    bounds = {'same_unit_face': F(3, 32), 'different_coplanar_faces': F(19, 32),
              'parallel_planes': 1-2*h, 'perpendicular_faces': F(19, 64)-h}
    assert all(minima[k] >= v > 0 for k, v in bounds.items())

    result = {'status': 'passed', 'candidate_sha256': EXPECTED,
              'scope': 'Exact finite hypotheses and controls; the all-tilings conclusion is a written proof.',
              'exposed_faces_reconstructed': len(face_owners), 'ports_per_face': 8,
              'ports_checked_on_actual_exposed_faces': len(ports),
              'core_box_checks': len(core_gaps), 'minimum_core_separation': str(min(core_gaps)),
              'connected_core_corridors': len(edges), 'corridor_box_checks': len(corridor_gaps),
              'minimum_corridor_separation': str(min(corridor_gaps)),
              'interior_ball_radius': '1/4', 'diameter_strict_upper_bound': '4',
              'packing_bound_for_tiles_meeting_radius_R_ball': '(4*R+17)^3',
              'cap_pairs_with_opposite_keys': count, 'relative_determinants': dict(determinants),
              'distinct_integer_poses': len(poses), 'adjacent_owner_implications_checked': count,
              'universal_grid_box_types': len(templates), 'all_frame_port_memberships': transformed,
              'nonidentical_periodic_box_checks': checks, 'box_pair_categories': dict(category_counts),
              'minimum_separating_gaps': {k: str(v) for k, v in sorted(minima.items())},
              'earlier_audit_conservative_bounds': {k: str(v) for k, v in sorted(bounds.items())},
              'far_shifts_separation_reason': 'A coordinate shift of magnitude >=2 gives center distance >1, whereas summed radii <=1/32.',
              'equal_coefficient_cap_control': fractional_control}
    (HERE/'grid_bridge_scrutiny.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'equal_coefficient_cap_control'}, indent=2))


if __name__ == '__main__':
    run()

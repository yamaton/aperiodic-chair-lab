"""Audit a scalene-triangle cubic cap with the two-depth recoding.

Symbolic identities and exact finite geometry support PORT_SIMPLIFICATION.md.
The all-isometries/local-to-global arguments remain written mathematics.
Never replaces frozen_v1 or an existing differing triangular_v1 snapshot.
"""

from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import sympy as sp
import verify_from_coordinates as geom

HERE = Path(__file__).resolve().parent
REFERENCE = '95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54'
VERTICES = ((-1, -1), (1, -1), (-1, 0))
AMPLITUDES = (1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def matvec(r, p):
    return tuple(dot(row, p) for row in r)


def triangle_stabilizer(vertices):
    dist = lambda i, j: sum((x-y)**2 for x, y in zip(vertices[i], vertices[j]))
    return [p for p in permutations(range(3))
            if all(dist(i, j) == dist(p[i], p[j]) for i, j in combinations(range(3), 2))]


def symbolic_audit():
    x, y, d, e, t, u, v = sp.symbols('x y d e t u v')
    bubble = 27*u*v*(1-u-v)
    line = sp.Poly(bubble.subs({u: x+d*t, v: y+e*t}), t)
    assert sp.expand(line.nth(3) + 27*d*e*(d+e)) == 0
    branch_coefficients = [sp.factor(line.nth(2).subs(d, 0)),
                           sp.factor(line.nth(2).subs(e, 0)),
                           sp.factor(line.nth(2).subs(e, -d))]
    assert branch_coefficients == [-27*e**2*x, -27*d**2*y, 27*d**2*(x+y-1)]
    for a, b in ((0, v), (u, 0), (u, 1-u)):
        assert sp.expand(bubble.subs({u: a, v: b}, simultaneous=True)) == 0
    physical = sp.expand(bubble.subs({u: (u+1)/2, v: v+1}, simultaneous=True))
    assert sp.Poly(physical, u, v).total_degree() == 3
    assert physical.subs({u: -sp.Rational(1, 3), v: -sp.Rational(2, 3)}) == 1
    integral = sp.integrate(physical, (v, -1, -(u+1)/2), (u, -1, 1))
    assert integral == sp.Rational(9, 20)
    # For a zero-boundary polynomial, each distinct edge-line factor divides
    # it. Enumerate the low-degree coefficient spaces as an exact control.
    def boundary_kernel(degree, edges):
        monomials = [u**i*v**j for i in range(degree+1) for j in range(degree+1-i)]
        coefficients = sp.symbols(f'c:{len(monomials)}')
        polynomial = sum(c*m for c, m in zip(coefficients, monomials))
        equations = []
        for a, b in edges:
            equations.extend(sp.Poly(polynomial.subs({u: a, v: b}, simultaneous=True), t).all_coeffs())
        matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
        return [sp.factor(sum(c*m for c, m in zip(vector, monomials))) for vector in matrix.nullspace()]
    tri_edges = ((-1, t), (t, -1), (t, -(t+1)/2))
    square_edges = ((-1, t), (1, t), (t, -1), (t, 1))
    assert boundary_kernel(2, tri_edges) == []
    triangle_basis = boundary_kernel(3, tri_edges)
    square_basis = boundary_kernel(4, square_edges)
    assert len(triangle_basis) == len(square_basis) == 1
    assert sp.cancel(triangle_basis[0]/physical).free_symbols == set()
    assert sp.cancel(square_basis[0]/((1-u*u)*(1-v*v))).free_symbols == set()
    square_symmetries = 0
    for swap, su, sv in product((False, True), (-1, 1), (-1, 1)):
        a, b = (su*v, sv*u) if swap else (su*u, sv*v)
        square_symmetries += sp.expand(square_basis[0].subs({u: a, v: b}, simultaneous=True)-square_basis[0]) == 0
    assert square_symmetries == 8
    assert triangle_stabilizer(VERTICES) == [(0, 1, 2)]
    assert len(triangle_stabilizer(((0, 0), (1, 0), (0, 1)))) == 2
    # A pyramid has an open planar facet 3*x when x < y and x < 1-x-y.
    # Translation along y preserves that open patch, without fixing its base.
    px, py, eps = F(1, 12), F(1, 3), F(1, 100)
    assert px < min(py, 1-px-py, py+eps, 1-px-py-eps)
    return dict(polynomial=str(sp.factor(physical)), degree=3,
                barycentric_polynomial=str(bubble), leading_line_coefficient=str(line.nth(3).factor()),
                quadratic_branch_coefficients=list(map(str, branch_coefficients)),
                integral_over_normalized_triangle=str(integral), maximum='1',
                maximum_reason='AM-GM for three nonnegative barycentric coordinates summing to one',
                side_squared_lengths=[1, 4, 5], triangle_vertex_stabilizer=[[0, 1, 2]],
                degree_two_triangle_boundary_kernel_dimension=0,
                degree_three_triangle_boundary_basis=list(map(str, triangle_basis)),
                degree_four_square_boundary_basis=list(map(str, square_basis)),
                degree_four_square_symmetries=int(square_symmetries),
                isosceles_triangle_control_symmetries=2,
                pyramid_control=dict(barycentric_point=[str(px), str(py)],
                                     local_uv_translation=['0', str(eps)],
                                     world_translation_length='1/6400',
                                     scope='Open planar-facet coincidence only, not a disjoint whole-tile placement'))


def save_snapshot(reference):
    candidate = deepcopy(reference)
    candidate['schema'] = 2
    candidate['convention'] = 'Proposed triangular cubic variant; all affine isometries considered in written registration argument.'
    candidate['reference_candidate_sha256'] = REFERENCE
    candidate['port_anchor_convention'] = 'center is the old port frame anchor, not the new triangle centroid'
    candidate.pop('cap_polynomial')
    candidate['port_profile'] = dict(kind='scalene_triangle_cubic_bubble',
        normalized_vertices=VERTICES, barycentric_coordinates=['(u+1)/2', 'v+1', '-(u+2*v+1)/2'],
        polynomial='27*lambda0*lambda1*lambda2', outside_triangle='0',
        surface='p + w*u*U + w*v*V + signed_key*delta*phi(u,v)*N',
        maximum='1', normalized_integral='9/20')
    for p in candidate['ports']:
        old = p['signed_key']
        chi = geom.determinant(tuple(p['u_axis'])+tuple(p['v_axis'])+tuple(p['outward_normal']))
        p['reference_signed_key'] = old
        p['signed_key'] = chi*AMPLITUDES[abs(old)-1]
    raw = (json.dumps(candidate, indent=2)+'\n').encode()
    folder = HERE/'triangular_v1'
    folder.mkdir(exist_ok=True)
    path = folder/'candidate.json'
    if path.exists():
        assert path.read_bytes() == raw, 'Refuse to overwrite differing triangular_v1; use a new snapshot version'
    else:
        path.write_bytes(raw)
    return candidate, sha256(raw).hexdigest()


def finite_audit(data, reference):
    w, delta = F(data['half_width']), F(data['height_unit'])
    assert (w, delta) == (F(1, 64), F(1, 4096))
    h = 2*delta
    cells = set(map(tuple, data['coarse_cubes']))
    ports, faces = [], defaultdict(list)
    for p in data['ports']:
        center = tuple(map(F, p['center']))
        u, v, n = (tuple(p[k]) for k in ('u_axis', 'v_axis', 'outward_normal'))
        f = tuple(center[i]-F(3*u[i]+v[i], 16) for i in range(3))
        owner = tuple(f[i]-F(n[i]+1, 2) for i in range(3))
        assert owner in cells and tuple(owner[i]+n[i] for i in range(3)) not in cells
        chi = geom.determinant(u+v+n)
        assert chi == (1 if p['signed_key'] > 0 else -1)
        vertices = [tuple(center[i]+w*a*u[i]+w*b*v[i] for i in range(3)) for a, b in VERTICES]
        assert all(abs(q[i]-f[i]) <= F(13, 64) for q in vertices for i in range(3) if not n[i])
        ports.append(dict(p=center, u=u, v=v, n=n, f=f, owner=owner, key=p['signed_key'], vertices=vertices))
        faces[f, n].append(ports[-1])
    assert len(faces) == 24 and all(len(ps) == 8 for ps in faces.values())
    assert sum(p['key'] for p in ports) == 0
    assert h < F(1, 64) < F(1, 4) and 3*F(1, 64)**2 < F(1, 4)**2
    poses, count = set(), 0
    for a, b in product(ports, repeat=2):
        if a['key'] != -b['key']:
            continue
        r = tuple(tuple(a['u'][i]*b['u'][j]+a['v'][i]*b['v'][j]-a['n'][i]*b['n'][j] for j in range(3)) for i in range(3))
        t = tuple(x-y for x, y in zip(a['p'], matvec(r, b['p'])))
        assert geom.determinant(sum(r, ())) == 1
        assert all(x.denominator == 1 for x in t)
        # Match actual three triangle vertices, not just the old anchor.
        for av, bv in zip(a['vertices'], b['vertices']):
            assert av == tuple(x+y for x, y in zip(t, matvec(r, bv)))
        inside_b = tuple(b['f'][i]-F(b['n'][i], 2) for i in range(3))
        assert tuple(x+y for x, y in zip(t, matvec(r, inside_b))) == tuple(a['f'][i]+F(a['n'][i], 2) for i in range(3))
        poses.add((r, t))
        count += 1
    assert count == 13312
    # Bounding boxes enclose the full new triangular supports. The complete
    # periodic box family is unchanged tangentially and strictly shallower.
    offsets = {(F(s*a, 16), F(t*b, 16)) for a, b in ((3, 1), (1, 3)) for s, t in product((-1, 1), repeat=2)}
    templates = []
    for axis in range(3):
        tangents = [i for i in range(3) if i != axis]
        for offset in sorted(offsets):
            center = [F(0)]*3
            for i, z in zip(tangents, offset):
                center[i] = F(1, 2)+z
            templates.append((tuple(center), tuple(h if i == axis else w for i in range(3))))
    rotations = geom.rotation_group()
    all_frames = [tuple(s*x for x in r) for r in rotations for s in (-1, 1)]
    template_set = set(templates)
    memberships = 0
    for r, p in product(all_frames, ports):
        center = tuple(x % 1 for x in geom.apply(r, p['p']))
        normal = geom.apply(r, p['n'])
        assert (center, tuple(h if normal[i] else w for i in range(3))) in template_set
        memberships += 1
    assert memberships == 9216
    old_h = max(abs(p['signed_key']) for p in reference['ports'])*delta*(1+F(reference['cap_polynomial']['a'])+F(reference['cap_polynomial']['b']))
    assert h < old_h
    separation = lambda a, b: max(abs(a[0][i]-b[0][i])-a[1][i]-b[1][i] for i in range(3))
    gaps = []
    for a, b, shift in product(templates, templates, product((-1, 0, 1), repeat=3)):
        moved = (tuple(x+y for x, y in zip(b[0], shift)), b[1])
        if a == moved:
            continue
        gap = separation(a, moved)
        assert gap > 0
        gaps.append(gap)
    assert len(gaps) == 15528 and h < w and 2*w < 1
    solid, old = geom.from_data(data), geom.from_data(reference)
    fine, oriented = geom.contact_catalogue(solid, rotations)
    old_fine, _ = geom.contact_catalogue(old, rotations)
    allowed = lambda cat: {q for q, value in cat.items() if value[1]}
    assert allowed(fine) == allowed(old_fine) and len(allowed(fine)) == 44
    children = [(tuple(c['center']), tuple(x for row in c['matrix'] for x in row)) for c in data['children']]
    macro = geom.assemble(children, solid, oriented)
    macro_contacts, _ = geom.contact_catalogue(macro, rotations)
    assert allowed(macro_contacts) == {(tuple(2*x for x in t), r) for t, r in allowed(fine)}
    assert len(fine) == 1194 and len(macro_contacts) == 6801
    assert all(all(x % 2 == 0 for x in t) for t, r in allowed(macro_contacts))
    return dict(ports=len(ports), exposed_faces=len(faces), key_counts=dict(sorted(Counter(p['key'] for p in ports).items())),
                opposite_key_frame_pairs=count, distinct_frame_locked_poses=len(poses),
                all_frame_maps_proper_integral=True, actual_triangle_vertices_match=True,
                adjacent_owner_checks=count, height_bound=str(h), minimum_face_edge_margin_lower_bound='19/64',
                signed_cap_volume_sum='0', total_volume='7', periodic_box_pair_checks=len(gaps),
                all_frame_box_memberships=memberships, feature_boxes_within_reference_boxes=True,
                minimum_periodic_box_gap=str(min(gaps)),
                far_box_reason='A coordinate shift of magnitude >=2 has center distance >1; summed radii <=1/32.',
                fine_geometric_contacts=len(fine), full_macro_geometric_contacts=len(macro_contacts),
                fine_fitting_contacts=len(allowed(fine)), full_macro_fitting_contacts=len(allowed(macro_contacts)),
                odd_macro_fitting_contacts=0, reference_fine_contact_sets_equal=True,
                macro_contacts_equal_doubled_reference=True,
                contact_scope='Exact frame/key contact atlas; equivalence to curved-surface matching uses the written rigidity lemma.')


def main():
    raw = (HERE/'frozen_v1/candidate.json').read_bytes()
    assert sha256(raw).hexdigest() == REFERENCE
    reference = json.loads(raw)
    symbolic = symbolic_audit()
    candidate, digest = save_snapshot(reference)
    finite = finite_audit(candidate, reference)
    result = dict(status='passed', reference_candidate_sha256=REFERENCE,
                  triangular_candidate_sha256=digest, symbolic=symbolic, finite=finite,
                  implementation='SymPy identities and rational port geometry; contact atlas uses verify_from_coordinates helpers.',
                  scope='Local algebraic identities and finite geometric hypotheses. Universal rigidity and registration are written deductions, not formal verification or independent review.')
    (HERE/'port_simplification.json').write_text(json.dumps(result, indent=2)+'\n')
    manifest = dict(schema=1, candidate_sha256=digest, reference_candidate_sha256=REFERENCE,
                    status='Research snapshot; exact curved profile, no certified mesh',
                    generator='strong/audit/simplify_ports.py', report='strong/PORT_SIMPLIFICATION.md')
    manifest_path = HERE/'triangular_v1/manifest.json'
    manifest_raw = json.dumps(manifest, indent=2)+'\n'
    if manifest_path.exists():
        assert manifest_path.read_text() == manifest_raw
    else:
        manifest_path.write_text(manifest_raw)
    print(json.dumps(dict(status='passed', candidate_sha256=digest, symbolic=symbolic, finite=finite), indent=2))


if __name__ == '__main__':
    main()

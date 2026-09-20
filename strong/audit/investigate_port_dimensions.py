"""Movable-anchor width/depth study; does not change either frozen solid.

Exact rational packing/frame checks and polynomial interval certificates.
The plotted depth envelopes are sufficient separation conditions, not a
classification of all admissible solids or manufacturing tolerances.
"""
from fractions import Fraction as Q
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
VERTICES = ((-1, -1), (1, -1), (-1, 0))
SOURCE_SHA = 'b1237ab5c2b7c75c565fb4f837a886aa2aafa990927bdbcda399a440cd68b3ce'


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def mv(r, v):
    return tuple(dot(row, v) for row in r)


def frames():
    return [((0, s), (t, 0)) if swap else ((s, 0), (0, t))
            for swap, s, t in product((False, True), (-1, 1), (-1, 1))]


def triangles(a, b, w):
    return [[tuple(a*x+b*y+w*(u*x+v*y) for x, y in zip(U, V))
             for u, v in VERTICES] for U, V in frames()]


def separation(a, b):
    """Strict separating-axis clearance, without normalizing each axis."""
    axes = []
    for tri in (a, b):
        for p, q in zip(tri, tri[1:]+tri[:1]):
            axes.append((q[1]-p[1], p[0]-q[0]))
    return max(max(min(dot(n, p) for p in a)-max(dot(n, p) for p in b),
                   min(dot(n, p) for p in b)-max(dot(n, p) for p in a))
               for n in axes)


def width_optima():
    # A triangle and its reflection cannot have disjoint interiors if the
    # triangle straddles that reflection axis. Thus the D4 orbit requires
    # the triangle to lie in one of eight wedges. Transform each wedge to
    # 0 <= y <= x <= 1/2, enumerating the eight relative orientations.
    records = []
    for U, V in frames():
        ds = [tuple(u*x+v*y for x, y in zip(U, V)) for u, v in VERTICES]
        beta = -min(y for x, y in ds)
        alpha = beta-min(x-y for x, y in ds)
        span = alpha+max(x for x, y in ds)
        w = Q(1, 2*span)
        points = [(w*(alpha+x), w*(beta+y)) for x, y in ds]
        assert all(0 <= y <= x <= Q(1, 2) for x, y in points)
        assert max(x for x, y in points) == Q(1, 2)
        records.append(dict(U=U, V=V, anchor_over_width=[alpha, beta],
                            outer_coordinate_over_width=span, maximum_width=str(w)))
    assert max(Q(r['maximum_width']) for r in records) == Q(1, 4)
    return records


def relocated_records(data, a, b, w):
    records = []
    for p in data['ports']:
        U, V, N = (tuple(p[k]) for k in ('u_axis', 'v_axis', 'outward_normal'))
        old = tuple(map(Q, p['center']))
        f = tuple(old[i]-Q(3*U[i]+V[i], 16) for i in range(3))
        pa = a[abs(p['signed_key'])] if isinstance(a, dict) else a
        pb = b[abs(p['signed_key'])] if isinstance(b, dict) else b
        center = tuple(f[i]+pa*U[i]+pb*V[i] for i in range(3))
        vertices = [tuple(center[i]+w*(u*U[i]+v*V[i]) for i in range(3))
                    for u, v in VERTICES]
        records.append(dict(U=U, V=V, N=N, old=old, f=f, p=center,
                            vertices=vertices, key=p['signed_key'], a=pa, b=pb))
    return records


def frame_audit(records, w):
    count, poses = 0, set()
    for a, b in product(records, repeat=2):
        if a['key'] != -b['key']:
            continue
        r = tuple(tuple(a['U'][i]*b['U'][j]+a['V'][i]*b['V'][j]
                        -a['N'][i]*b['N'][j] for j in range(3)) for i in range(3))
        delta = lambda field: tuple(x-y for x, y in zip(a[field], mv(r, b[field])))
        t = delta('p')
        assert t == delta('old') == delta('f')
        assert all(x.denominator == 1 for x in t)
        for av, bv in zip(a['vertices'], b['vertices']):
            assert av == tuple(x+y for x, y in zip(t, mv(r, bv)))
        poses.add((r, t))
        count += 1
    assert count == 13312 and len(poses) == 1410
    # All signed cubic frames preserve the universal eight-footprint family
    # on each unit face. This uses actual triangles, not unique anchors.
    from itertools import permutations
    frames3 = [tuple(tuple(signs[i] if j == perm[i] else 0 for j in range(3))
                     for i in range(3)) for perm in permutations(range(3))
               for signs in product((-1, 1), repeat=3)]
    templates = {(a, b): {tuple(tri) for tri in triangles(a, b, w)}
                 for a, b in {(p['a'], p['b']) for p in records}}
    assert all(len(ts) == 8 for ts in templates.values())
    total = 0
    for r, p in product(frames3, records):
        U, V, N, f, center = (mv(r, p[k]) for k in ('U', 'V', 'N', 'f', 'p'))
        assert center == tuple(f[i]+p['a']*U[i]+p['b']*V[i] for i in range(3))
        assert all(sorted(abs(x) for x in axis) == [0, 0, 1] for axis in (U, V, N))
        assert dot(U, V) == dot(U, N) == dot(V, N) == 0
        normal_axis = next(i for i in range(3) if N[i])
        tangent_axes = [i for i in range(3) if i != normal_axis]
        assert f[normal_axis].denominator == 1
        assert all((f[i]-Q(1, 2)).denominator == 1 for i in tangent_axes)
        moved_vertices = [mv(r, v) for v in p['vertices']]
        assert all(v[normal_axis] == f[normal_axis] for v in moved_vertices)
        projected = tuple(tuple(v[i]-f[i] for i in tangent_axes) for v in moved_vertices)
        assert projected in templates[p['a'], p['b']]
        total += 1
    assert total == 9216
    return dict(opposite_key_pairs=count, distinct_local_poses=len(poses),
                same_translation_as_reference=True, actual_vertices_match=True,
                all_signed_frame_memberships=total)


def level_dependent_audit(data, w):
    records = relocated_records(data, {1: Q(-1, 4), 2: Q(-31, 128)}, Q(7, 32), w)
    faces = defaultdict(list)
    for p in records:
        faces[p['f'], p['N']].append(p)
    gaps = []
    for (f, n), ps in faces.items():
        axes = [i for i in range(3) if n[i] == 0]
        tris = [[tuple(v[i] for i in axes) for v in p['vertices']] for p in ps]
        gaps.extend(separation(A, B) for A, B in combinations(tris, 2))
    assert len(gaps) == 672 and min(gaps) > 0
    counts = Counter(sum(abs(p['key']) == 2 for p in ps) for ps in faces.values())
    assert counts == {1: 16, 2: 8}
    return dict(low_anchor=['-1/4', '7/32'], high_anchor=['-31/128', '7/32'],
                same_face_pair_checks=len(gaps), all_strictly_separated=True,
                faces_by_number_of_high_ports=dict(sorted(counts.items())),
                contact_frame_checks=frame_audit(records, w),
                depth_clearance_reason='High ports move inward by U/128; nearest-edge distance increases by 1/128. The common-witness certificate still suffices.')


def polynomial_certificate():
    u, v, t = sp.symbols('u v t')
    psi = -sp.Rational(27, 4)*(u+1)*(v+1)*(u+2*v+1)
    peak = sp.Rational(27, 32)*(u+1)*(1-u)**2
    # Exact maximum in v for every fixed u, proved by a square identity.
    assert sp.expand(peak-psi-27*(u+1)*(u+4*v+3)**2/32) == 0
    margin = sp.Rational(1, 4)+sp.Rational(3, 16)*u-sp.Rational(1, 8)*peak
    intervals = []
    for j in range(4):
        poly = sp.Poly(margin.subs(u, (t+j)/2-1), t)
        coefficients = [sum(poly.nth(k)*sp.binomial(i, k)/sp.binomial(3, k)
                            for k in range(i+1)) for i in range(4)]
        assert all(c > 0 for c in coefficients)
        intervals.append(dict(u_interval=[str(Q(j, 2)-1), str(Q(j+1, 2)-1)],
                              bernstein_coefficients=list(map(str, coefficients))))
    minimum = min(Q(c) for interval in intervals for c in interval['bernstein_coefficients'])
    assert minimum == Q(5, 256)
    assert minimum-(Q(9, 64)-Q(1, 8)) == Q(1, 256) > 0
    # h < rho and sqrt(3)*rho < retained ball radius 1/4.
    assert Q(1, 8) < Q(1, 7) and 3*Q(1, 7)**2 < Q(1, 4)**2
    return dict(maximum_in_v=str(peak), square_identity=str(sp.factor(peak-psi)),
                edge_minus_height_polynomial=str(sp.factor(margin)),
                intervals=intervals, uniform_clearance_lower_bound=str(minimum),
                thicker_zone_height='9/64', thicker_zone_clearance_lower_bound='1/256',
                retained_core_radius='1/4', exhaustion_inset='1/7')


def depth_limit(w, constant, coefficient):
    """Algebraic minimum of (constant+coefficient*u)/max_v psi."""
    u = sp.symbols('u')
    p = sp.Rational(27, 32)*(u+1)*(1-u)**2
    d = sp.Rational(constant.numerator, constant.denominator)+sp.Rational(coefficient.numerator, coefficient.denominator)*u
    roots = sp.solve(sp.factor(sp.diff(d, u)*p-d*sp.diff(p, u)), u)
    critical = [r for r in roots if r.is_real and -1 < float(r) < 1]
    candidates = [(sp.simplify(d.subs(u, r)/p.subs(u, r)), r) for r in critical]
    value, point = min(candidates, key=lambda item: float(item[0]))
    return dict(width=str(w), u_at_minimum=str(point), exact_height=str(value), height=float(value))


def draw(path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    import numpy as np

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), gridspec_kw={'width_ratios': [1, 1, 1.65]})
    layouts = [(Q(3, 16), Q(1, 16), Q(1, 64), 'Recorded layout: w = 1/64'),
               (Q(-1, 4), Q(7, 32), Q(3, 16), 'Relocated witness: w = 3/16')]
    for ax, (a, b, w, title) in zip(axes[:2], layouts):
        for i, tri in enumerate(triangles(a, b, w)):
            ax.add_patch(Polygon([[float(x), float(y)] for x, y in tri],
                                 facecolor=plt.cm.tab10(i), edgecolor='white', linewidth=.5))
        ax.plot([-.5, .5, .5, -.5, -.5], [-.5, -.5, .5, .5, -.5], color='#39485a')
        ax.set(xlim=(-.55, .55), ylim=(-.55, .55), aspect='equal', title=title)
        ax.set_xticks([-.5, 0, .5]); ax.set_yticks([-.5, 0, .5])
        ax.set_xlabel('One unit face; actual triangle footprints')
    ax = axes[2]
    def numeric_bound(ws, C, sign):
        # Exact stationary quadratic: c*P-(C+c*u)*P'=0.
        answer = []
        for w in ws:
            c = sign*w
            roots = np.roots([2*c, 3*C+c, C+c])
            us = [float(r.real) for r in roots if abs(r.imag) < 1e-9 and -1 < r.real < 1]
            answer.append(min((C+c*u)/(27*(u+1)*(1-u)**2/32) for u in us))
        return np.array(answer)
    ws = np.linspace(.0001, .24999, 500)
    hs = numeric_bound(ws, .25, 1)
    ax.fill_between(ws, 0, hs, color='#88c9cf', alpha=.6, label='Relocated family: sufficient region')
    ax.plot(ws, hs, color='#137e86')
    oldws = np.linspace(.0001, .062499, 160)
    oldhs = numeric_bound(oldws, 5/16, -1)
    ax.plot(oldws, oldhs, color='#705ca8', label='Fixed old anchors: sufficient bound')
    ax.plot([1/16, 1/16], [0, oldhs[-1]], '--', color='#705ca8', linewidth=1)
    ax.scatter([1/64, 3/64, 3/16], [1/2048, 1/32, 1/8], color=['#705ca8', '#ae7232', '#063e4a'], zorder=4)
    for x, y, label, offset in [(1/64, 1/2048, 'Snapshot', (5, 9)),
                                (3/64, 1/32, 'Cover', (5, 9)),
                                (3/16, 1/8, '12x width / 256x depth', (-120, -25))]:
        ax.annotate(label, (x, y), xytext=offset, textcoords='offset points', fontsize=9)
    ax.set(xlim=(0, .26), ylim=(0, .36), xlabel='Width parameter w (long side = 2w)',
           ylabel='Maximum depth h (depth unit = h/2)', title='Moving anchors changes the tradeoff')
    ax.legend(loc='upper right', fontsize=8); ax.grid(alpha=.15)
    fig.suptitle('Exact triangular ports: geometric design study, not manufacturing limits', fontsize=13)
    fig.tight_layout()
    fig.savefig(path)
    fig.savefig(path.with_suffix('.png'), dpi=160)
    plt.close(fig)


def main():
    raw = (HERE/'triangular_v1/candidate.json').read_bytes()
    assert sha256(raw).hexdigest() == SOURCE_SHA
    data = json.loads(raw)
    a, b, w, h = Q(-1, 4), Q(7, 32), Q(3, 16), Q(1, 8)
    tris = triangles(a, b, w)
    gaps = [separation(A, B) for A, B in combinations(tris, 2)]
    assert len(gaps) == 28 and min(gaps) > 0
    assert min(Q(1, 2)-abs(x) for tri in tris for p in tri for x in p) == Q(1, 16)
    assert len({tuple(a*x+b*y for x, y in zip(U, V)) for U, V in frames()}) == 8
    oldtouch = triangles(Q(3, 16), Q(1, 16), Q(1, 16))
    assert min(separation(A, B) for A, B in combinations(oldtouch, 2)) == 0
    # Old anchoring fails immediately above 1/16, independently of depth.
    oldoverlap = triangles(Q(3, 16), Q(1, 16), Q(65, 1024))
    assert min(separation(A, B) for A, B in combinations(oldoverlap, 2)) < 0
    optima = width_optima()
    result = dict(scope='Movable anchors in the common D4 orbit; exact sufficient depth conditions, not unrestricted optimality.',
                  source_candidate_sha256=SOURCE_SHA, frozen_files_unchanged=True,
                  width_optimization=dict(wedge_cases=optima, supremum='1/4',
                      explanation='Upper bound attained with touching edges; strict clearances for every 0 < w < 1/4.'),
                  witness=dict(a=str(a), b=str(b), width=str(w), maximum_depth=str(h),
                      height_unit=str(h/2), width_multiplier='12', depth_multiplier='256',
                      short_side=str(w), long_side=str(2*w), support_area_per_face=str(8*w*w),
                      face_edge_clearance='1/16', same_face_triangle_pairs=28,
                      strict_separating_axis_minimum=str(min(gaps)),
                      contact_frame_checks=frame_audit(relocated_records(data, a, b, w), w),
                      curved_zone_certificate=polynomial_certificate()),
                  old_anchor_depth_limits=[depth_limit(W, Q(5, 16), -W) for W in (Q(1, 64), Q(3, 64), Q(1, 16))],
                  relocated_depth_limits=[depth_limit(W, Q(1, 4), W) for W in (Q(1, 64), Q(1, 8), Q(3, 16), Q(15, 64))],
                  relocated_limit_as_width_tends_to_quarter='2/27',
                  depth_dependent_anchor_witness=level_dependent_audit(data, w),
                  atlas_transfer='Frame-pose equality plus disjoint local modification zones preserves the existing fine and full macro predicates. This script does not rerun the atlas enumeration.',
                  not_claimed=['global optimum over independently placed or reshaped ports',
                               'necessary upper bound on depth', 'new Lean proof',
                               'tolerance or manufacturing certification'])
    output = HERE/'port_dimensions.json'
    output.write_text(json.dumps(result, indent=2)+'\n')
    figure = ROOT/'strong/artifacts/port-dimensions.svg'
    draw(figure)
    print(json.dumps(dict(output=str(output.relative_to(ROOT)), figure=str(figure.relative_to(ROOT)),
                          width_supremum='1/4', witness=result['witness']), indent=2))


if __name__ == '__main__':
    main()

"""Specify asymmetric polynomial ports and check their exact frame data.

The algebraic rigidity argument is written in RECUT_CHAIR.md. These checks
verify its polynomial identities and all finite port-frame correspondences;
they are not an automated proof about arbitrary Euclidean tilings.
"""

from fractions import Fraction
from itertools import product
import json

import sympy as sp

from chair_recut import CHILD_ROTATIONS, PORT_LOOKUP, PORTS, contact_types, rotate
from offset_dipoles import OUT


def port_frame(point, normal):
    axis = next(k for k in range(3) if normal[k])
    center = tuple(point[k] // 8 if k == axis else (point[k] + 4) // 8 for k in range(3))
    offset = tuple(point[k] - 8 * center[k] for k in range(3))
    frames = []
    for magnitude in (3, 1):
        k = next(k for k in range(3) if abs(offset[k]) == magnitude)
        frames.append(tuple((1 if offset[k] > 0 else -1) if j == k else 0 for j in range(3)))
    return center, *frames


def run():
    profile = json.loads((OUT / "chair_recut_synthesis.json").read_text())["profiles"][1]
    labels = profile["labels"]
    frames = [port_frame(p, n) for p, n in PORTS]
    records = [{"center": [str(Fraction(v, 16)) for v in p], "outward_normal": n,
                "u_axis": frames[i][1], "v_axis": frames[i][2], "signed_key": labels[i]}
               for i, (p, n) in enumerate(PORTS)]
    stabilizing_rotations = [r for r in CHILD_ROTATIONS[0]
                            if all(labels[PORT_LOOKUP[rotate(p, r), rotate(n, r)]] == labels[i]
                                   for i, (p, n) in enumerate(PORTS))]
    assert len(stabilizing_rotations) == 1
    fitting = 0
    for t, r, pairs in contact_types():
        if not all(labels[a] == -labels[b] for a, b in pairs):
            continue
        fitting += 1
        for a, b in pairs:
            assert frames[a][1] == rotate(frames[b][1], r)
            assert frames[a][2] == rotate(frames[b][2], r)
    poses = set()
    matches = 0
    for a, (pa, na) in enumerate(PORTS):
        for b, (pb, nb) in enumerate(PORTS):
            if labels[a] != -labels[b]:
                continue
            for r in range(24):
                if (rotate(nb, r) != tuple(-x for x in na)
                        or rotate(frames[b][1], r) != frames[a][1]
                        or rotate(frames[b][2], r) != frames[a][2]):
                    continue
                moved = rotate(pb, r)
                delta = tuple(pa[k] - moved[k] for k in range(3))
                assert all(x % 16 == 0 for x in delta)
                poses.add((tuple(x // 16 for x in delta), r))
                matches += 1
    u, v, t, a, b, du, dv, d = sp.symbols("u v t a b du dv d")
    phi = (1-u**2)*(1-v**2)*(1+u/5+v/7)
    along = sp.Poly(phi.subs({u: a+du*t, v: b+dv*t}), t)
    assert sp.factor(along.coeff_monomial(t**5)) == du**2*dv**2*(7*du+5*dv)/35
    assert sp.simplify(along.coeff_monomial(t**3).subs(du, 0) + (1-a*a)*dv**3/7) == 0
    assert sp.simplify(along.coeff_monomial(t**3).subs(dv, 0) + (1-b*b)*du**3/5) == 0
    diagonal = sp.Poly(phi.subs({u: a+5*d*t, v: b-7*d*t}), t)
    assert sp.simplify(diagonal.coeff_monomial(t**4) - 1225*d**4*(1+a/5+b/7)) == 0
    # Of the eight symmetries of the square's four side lines, only the
    # identity also preserves the fifth line 1+u/5+v/7=0.
    stabilizers = []
    for swap, su, sv in product((False, True), (-1, 1), (-1, 1)):
        x, y = (v, u) if swap else (u, v)
        if sp.expand(1+su*x/5+sv*y/7 - (1+u/5+v/7)) == 0:
            stabilizers.append((swap, su, sv))
    assert stabilizers == [(False, 1, 1)]
    integral = sp.integrate(phi, (u, -1, 1), (v, -1, 1))
    assert integral == sp.Rational(16, 9) and sum(labels) == 0
    result = {"status": "exact construction data and finite/symbolic checks passed",
              "construction_status": "Research candidate with a computer-assisted grid hierarchy proof and a proposed analytic grid-enforcement proof; not externally reviewed.",
              "coarse_shape": "Union of the seven closed unit cubes with lower corners in {-1,0}^3 except (0,0,0)",
              "placements": "Translations and proper rotations of one physical handedness",
              "half_width": "1/64", "height_unit": "1/4096",
              "port_formula": "p + (u/64)e_u + (v/64)e_v + (key/4096)(1-u^2)(1-v^2)(1+u/5+v/7)n, -1<=u,v<=1",
              "port_count": len(PORTS), "ports": records,
              "signed_key_sum": sum(labels), "exact_volume": "7",
              "proper_coarse_chair_symmetries_preserving_keys": len(stabilizing_rotations),
              "absolute_height_bound": str(Fraction(12, 4096) * (1+Fraction(1, 5)+Fraction(1, 7))),
              "checked_allowed_contact_types": fitting,
              "checked_matching_port_frames": matches,
              "distinct_integral_port_locked_poses": len(poses),
              "nonintegral_port_locked_poses": 0,
              "polynomial_rigidity_checks": {"highest_line_coefficient": str(sp.factor(along.coeff_monomial(t**5))),
                  "axis_parallel_and_oblique_line_cases": "passed",
                  "square_plus_fifth_line_stabilizer": "identity only", "cap_integral": str(integral)},
              "limit": "Symbolic identities support the written rigidity proof; they do not automatically certify the all-tilings argument or any polygonal mesh approximation."}
    (OUT / "recut_chair_exact.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "ports"}, indent=2))


if __name__ == "__main__":
    run()

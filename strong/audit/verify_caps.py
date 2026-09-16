"""Exact local cap audit from frozen coordinates; no project helper imports.

Symbolic identities and finite arithmetic support the accompanying written
proof. They do not quantify over Euclidean tilings or certify an STL.
"""

from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def act(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def subtract(a, b):
    return tuple(x-y for x, y in zip(a, b))


def det(m):
    a, b, c = m
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def symbolic_checks(a, b):
    u, v, t, x, y, d, e = sp.symbols("u v t x y d e")
    a, b = sp.Rational(a.numerator, a.denominator), sp.Rational(b.numerator, b.denominator)
    phi = (1-u*u)*(1-v*v)*(1+a*u+b*v)
    line = sp.Poly(phi.subs({u: x+d*t, v: y+e*t}), t)
    assert sp.expand(line.nth(5)-d*d*e*e*(a*d+b*e)) == 0
    vertical = sp.Poly(phi.subs({u: x, v: y+e*t}), t).nth(3)
    horizontal = sp.Poly(phi.subs({u: x+d*t, v: y}), t).nth(3)
    assert sp.expand(vertical + b*e**3*(1-x*x)) == 0
    assert sp.expand(horizontal + a*d**3*(1-y*y)) == 0
    oblique = sp.Poly(phi.subs({u: x+d*t, v: y-a*d*t/b}), t).nth(4)
    assert sp.factor(oblique-(a*a*d**4/b**2)*(1+a*x+b*y)) == 0
    for substitution in ({u: 1}, {u: -1}, {v: 1}, {v: -1}, {v: -(1+a*u)/b}):
        assert sp.simplify(phi.subs(substitution)) == 0
    integral = sp.integrate(phi, (u, -1, 1), (v, -1, 1))
    assert integral == sp.Rational(16, 9)

    def square_stabilizer(alpha, beta):
        result = []
        for swap, s, r in product((False, True), (-1, 1), (-1, 1)):
            mapped_u, mapped_v = (s*v, r*u) if swap else (s*u, r*v)
            if sp.expand(alpha*mapped_u+beta*mapped_v-alpha*u-beta*v) == 0:
                result.append({"swap": swap, "u_sign": s, "v_sign": r})
        return result

    stabilizer = square_stabilizer(a, b)
    assert stabilizer == [{"swap": False, "u_sign": 1, "v_sign": 1}]
    symmetric_control = square_stabilizer(a, a)
    assert len(symmetric_control) == 2
    return {"line_degree_five_coefficient_without_H": str(sp.factor(line.nth(5))),
            "constant_u_degree_three_coefficient": str(sp.factor(vertical)),
            "constant_v_degree_three_coefficient": str(sp.factor(horizontal)),
            "oblique_degree_four_coefficient": str(sp.factor(oblique)),
            "five_listed_lines_on_surface": True, "integral": str(integral),
            "fifth_line_square_stabilizer": stabilizer,
            "equal_coefficients_control_stabilizer": symmetric_control}


def run():
    raw = (HERE / "frozen_v1/candidate.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    manifest = json.loads((HERE / "frozen_v1/manifest.json").read_text())
    assert digest == manifest["candidate_sha256"]
    assert hashlib.sha256((HERE / "frozen_v1/proposal.md").read_bytes()).hexdigest() == manifest["archived_proposal_sha256"]
    data = json.loads(raw)
    width, depth = Q(data["half_width"]), Q(data["height_unit"])
    a, b = (Q(data["cap_polynomial"][k]) for k in ("a", "b"))
    assert a > 0 and b > 0 and a != b and a+b < 1
    ports = [{"p": tuple(map(Q, p["center"])), "n": tuple(p["outward_normal"]),
              "u": tuple(p["u_axis"]), "v": tuple(p["v_axis"]), "k": p["signed_key"]}
             for p in data["ports"]]
    counts = Counter(p["k"] for p in ports)
    assert set(counts) == set(range(-12, 0)) | set(range(1, 13))
    assert set(counts.values()) == {8} and sum(p["k"] for p in ports) == 0
    height = max(abs(p["k"]) for p in ports)*depth*(1+a+b)
    assert height < Q(1, 250) < Q(1, 4)
    boxes, margins = [], []
    for p in ports:
        axes = (p["u"], p["v"], p["n"])
        assert all(dot(x, y) == int(i == j) for i, x in enumerate(axes) for j, y in enumerate(axes))
        f = tuple(p["p"][i]-Q(3*p["u"][i]+p["v"][i], 16) for i in range(3))
        assert all(x.denominator == (1 if p["n"][i] else 2) for i, x in enumerate(f))
        margins.extend(Q(1, 2)-abs(p["p"][i]-f[i])-width for i in range(3) if not p["n"][i])
        radius = tuple(height if p["n"][i] else width for i in range(3))
        boxes.append(tuple((p["p"][i]-radius[i], p["p"][i]+radius[i]) for i in range(3)))
    assert min(margins) == Q(19, 64)
    assert all(any(x[1] < y[0] or y[1] < x[0] for x, y in zip(first, second))
               for first, second in combinations(boxes, 2))
    grid_gaps = {"same_unit_face": Q(1, 8)-2*width,
                 "different_coplanar_faces": 2*min(margins),
                 "parallel_grid_planes": 1-2*height,
                 "perpendicular_grid_faces": min(margins)-height}
    assert all(gap > 0 for gap in grid_gaps.values())

    poses, correspondences = set(), 0
    for first, second in product(ports, repeat=2):
        if first["k"] != -second["k"]:
            continue
        # This frame map is derived directly; no rotation-group indices.
        rotation = tuple(tuple(first["u"][i]*second["u"][j]
                               + first["v"][i]*second["v"][j]
                               - first["n"][i]*second["n"][j]
                               for j in range(3)) for i in range(3))
        if det(rotation) != 1:
            continue
        assert act(rotation, second["u"]) == first["u"]
        assert act(rotation, second["v"]) == first["v"]
        assert act(rotation, second["n"]) == tuple(-x for x in first["n"])
        shift = subtract(first["p"], act(rotation, second["p"]))
        assert all(x.denominator == 1 for x in shift)
        poses.add((rotation, shift))
        correspondences += 1

    # Counterfactual local control: keeping only the normal and key loses
    # the integral-translation conclusion, even within cube rotations.
    rotations = []
    for order, signs in product(permutations(range(3)), product((-1, 1), repeat=3)):
        matrix = tuple(tuple(signs[i]*int(j == order[i]) for j in range(3)) for i in range(3))
        if det(matrix) == 1:
            rotations.append(matrix)
    ambiguous, witness = set(), None
    for first, second in product(ports, repeat=2):
        if first["k"] != -second["k"]:
            continue
        for rotation in rotations:
            if act(rotation, second["n"]) != tuple(-x for x in first["n"]):
                continue
            shift = subtract(first["p"], act(rotation, second["p"]))
            if any(x.denominator != 1 for x in shift):
                ambiguous.add((rotation, shift))
                if witness is None:
                    witness = {"first_center": list(map(str, first["p"])),
                               "second_center": list(map(str, second["p"])),
                               "rotation": rotation, "translation": list(map(str, shift))}
    assert ambiguous
    result = {"status": "passed", "candidate_sha256": digest,
              "implementation": "Separate frozen-coordinate arithmetic and SymPy identities; no project helper imports",
              "scope": "Local algebraic identities, frame arithmetic, and feature bounds; global geometric lemmas remain written arguments",
              "uniformly_normalized_height": f"k*{depth/width}",
              "height_bound": str(height), "minimum_face_edge_margin": str(min(margins)),
              "all_feature_boxes_disjoint": True, "key_multiplicities": dict(sorted(counts.items())),
              "global_feature_box_separation_bounds": {k: str(v) for k, v in grid_gaps.items()},
              "volume": "7", "matching_frame_correspondences": correspondences,
              "distinct_frame_locked_poses": len(poses), "nonintegral_frame_locked_poses": 0,
              "polynomial_checks": symbolic_checks(a, b),
              "normal_and_key_only_control": {"nonintegral_local_poses": len(ambiguous), "example": witness,
                    "scope": "Local ambiguity without ordered frames, not a tiling or a counterexample to the actual cap"}}
    (HERE / "cap_verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()

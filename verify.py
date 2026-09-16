"""Numerical geometry checks and exact algebra; not an all-tilings proof."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
import sympy as sp

from geometry import Block, patch, triangles, polygon_faces


def verify():
    block = Block()
    rng = np.random.default_rng(20260915)
    xy = rng.uniform(-8, 8, (20000, 2))
    seam_error = max(float(np.max(np.abs(block.surfaces(xy, m)[1] -
                       block.surfaces(xy, m + 1)[0]))) for m in range(-8, 9))
    assert seam_error < 1e-12
    fault_error = float(np.max(np.abs(block.surfaces(xy, 0)[1] -
                        block.surfaces(xy, 1, [np.sqrt(2)/10, 0, 0])[0])))
    assert fault_error < 1e-12

    # Negative control: rotating a layer by an extra 1 degree breaks the seam.
    t = np.pi / 180
    wrong_xy = xy @ np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    wrong_error = float(np.max(np.abs(block.surfaces(xy, 0)[1] -
                                    block.surfaces(wrong_xy, 1)[0])))
    assert wrong_error > .1

    mesh = triangles(block.vertices)
    edges = Counter(tuple(sorted((int(f[k]), int(f[(k+1) % 3]))))
                    for f in mesh for k in range(3))
    assert set(edges.values()) == {2}
    signed_volume = sum(np.dot(p, np.cross(q, r)) / 6
                        for p, q, r in block.vertices[mesh])
    expected_volume = np.linalg.det(block.basis) * block.height
    assert abs(signed_volume - expected_volume) < 1e-12
    assert len(polygon_faces(block.vertices)) == 8

    tiles = patch(block, range(-2, 5), radius=2)
    hulls = [ConvexHull(v) for *_, v in tiles]
    bounds = [(v.min(axis=0), v.max(axis=0)) for *_, v in tiles]
    pair_count = 0
    max_overlap_radius = 0.
    for i, j in combinations(range(len(tiles)), 2):
        lo = np.maximum(bounds[i][0], bounds[j][0])
        hi = np.minimum(bounds[i][1], bounds[j][1])
        if np.any(hi - lo <= 1e-10):
            continue
        # Maximize the radius of a ball inside both convex polyhedra.
        planes = np.vstack([hulls[i].equations, hulls[j].equations])
        result = linprog([0, 0, 0, -1],
                         A_ub=np.c_[planes[:, :3], np.ones(len(planes))],
                         b_ub=-planes[:, 3], bounds=[(None, None)] * 4,
                         method="highs")
        assert result.success, result.message
        radius = float(result.x[3])
        max_overlap_radius = max(max_overlap_radius, radius)
        assert radius < 1e-9, (tiles[i][:3], tiles[j][:3], radius)
        pair_count += 1

    # Independent coverage check: hull halfspaces, not the surface formula.
    samples = rng.uniform([-.8, -.8, -.9], [.8, .8, .9], (12000, 3))
    counts = np.zeros(len(samples), dtype=int)
    for hull in hulls:
        inside = np.all(samples @ hull.equations[:, :3].T + hull.equations[:, 3] < -1e-10, axis=1)
        counts += inside
    assert np.all(counts == 1), dict(zip(*np.unique(counts, return_counts=True)))

    # Exact matrix in lattice coordinates: B^-1 R B.
    q = sp.Rational
    B = sp.Matrix([[1, q(1, 3)], [0, 2 * sp.sqrt(2) / 3]])
    R = sp.Matrix([[q(1, 3), 2 * sp.sqrt(2) / 3],
                   [-2 * sp.sqrt(2) / 3, q(1, 3)]])
    M = sp.simplify(B.inv() * R * B)
    assert M == sp.Matrix([[q(2, 3), 1], [-1, 0]])
    assert sp.simplify(R.T * R) == sp.eye(2) and R.det() == 1
    assert sp.simplify(R * B[:, 1]) == B[:, 0]

    # Finite searches only illustrate the infinite argument in RESEARCH.md.
    # A vector belongs to all N layer lattices iff M^-k v is integral.
    survivors = []
    candidates = [(Fraction(i), Fraction(j)) for i, j in product(range(-60, 61), repeat=2)
                  if i or j]
    for n in range(1, 9):
        survivors.append({"layers": n, "nonzero_vectors_in_coordinate_box_60": len(candidates)})
        kept = []
        for a, b in candidates:
            x, y = a, b
            for _ in range(n):
                x, y = -y, x + Fraction(2, 3) * y
            if x.denominator == y.denominator == 1:
                kept.append((a, b))
        candidates = kept

    periodic_control = Block(cosine=.5)
    assert np.max(np.abs(periodic_control.rotation(6) - np.eye(3))) < 1e-12
    assert np.max(np.abs(periodic_control.tile(6, 0, 0) -
                         periodic_control.tile(0, 0, 0) - [0, 0, 6*block.height])) < 1e-12

    return {
        "status": "passed; computational checks do not classify arbitrary tilings",
        "vertices": len(block.vertices), "polygonal_faces": 8, "stl_triangles": len(mesh),
        "watertight_edge_incidence": True,
        "angle_degrees": float(np.degrees(block.angle)),
        "volume": float(signed_volume), "analytic_volume": "4 sqrt(2) / 15",
        "seam_samples_per_interface": len(xy), "interfaces_checked": 17,
        "max_seam_error": seam_error, "single_fault_seam_error": fault_error,
        "wrong_angle_control_seam_error": wrong_error,
        "patch_tiles": len(tiles), "overlap_linear_programs": pair_count,
        "max_overlap_inscribed_radius": max_overlap_radius,
        "interior_coverage_samples": len(samples), "all_coverage_counts_equal_one": True,
        "exact_lattice_rotation": str(M), "finite_lattice_search": survivors,
        "rational_angle_control": "60 degrees repeats vertically after 6 layers",
    }


if __name__ == "__main__":
    report = verify()
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

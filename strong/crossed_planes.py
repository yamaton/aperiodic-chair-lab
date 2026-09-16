"""A provably strongly aperiodic 121-state matching system, NOT a monotile.

This implements the target logical mechanism before any claimed geometric
compression to one solid. All states are necessary possibilities, not 121
orientations of an identical cube.
"""

from itertools import product
import json
from pathlib import Path

import z3


# East, North, West, South. Jeandel--Rao, as tabulated by S. Labbe:
# https://www.labri.fr/perso/slabbe/docs/0.7/wang_tiles.html
WANG = ((2, 4, 2, 1), (2, 2, 2, 0), (1, 1, 3, 1), (1, 2, 3, 2),
        (3, 1, 3, 3), (0, 1, 3, 1), (0, 0, 0, 1), (3, 1, 0, 2),
        (0, 2, 1, 2), (1, 2, 1, 4), (3, 3, 1, 2))


def faces(a, b):
    """Face labels in +x,-x,+y,-y,+z,-z order, with axis-specific alphabets."""
    ae, an, aw, ass = WANG[a]
    be, bn, bw, bs = WANG[b]
    return (("x", ae, be), ("x", aw, bw),
            ("y", an, b), ("y", ass, b),
            ("z", a, bn), ("z", a, bs))


def planar_patch(n=12, periodic=False):
    solver = z3.Solver()
    solver.set(timeout=30000)
    states = {(i, j): z3.Int(f"t_{i}_{j}") for i, j in product(range(n), repeat=2)}
    edges = {(i, j): [z3.Int(f"edge_{i}_{j}_{d}") for d in range(4)] for i, j in states}
    for p, state in states.items():
        solver.add(z3.Or([z3.And(state == k, *[edges[p][d] == tile[d] for d in range(4)])
                          for k, tile in enumerate(WANG)]))
        for d, delta, opposite in ((0, (1, 0), 2), (1, (0, 1), 3)):
            q = (p[0] + delta[0], p[1] + delta[1])
            if periodic:
                q = tuple(v % n for v in q)
            if q in states:
                solver.add(edges[p][d] == edges[q][opposite])
    status = solver.check()
    if status != z3.sat:
        return str(status), None
    model = solver.model()
    patch = [[model[states[i, j]].as_long() for j in range(n)] for i in range(n)]
    for i, j in states:
        if i+1 < n:
            assert WANG[patch[i][j]][0] == WANG[patch[i+1][j]][2]
        if j+1 < n:
            assert WANG[patch[i][j]][1] == WANG[patch[i][j+1]][3]
    return "sat", patch


def run():
    out = Path(__file__).parent / "artifacts"
    n = 12
    status, planar = planar_patch(n)
    assert status == "sat"
    cube = {(i, j, k): (planar[i][j], planar[i][k]) for i, j, k in product(range(n), repeat=3)}
    checks = 0
    for p, state in cube.items():
        for axis in range(3):
            q = list(p)
            q[axis] += 1
            q = tuple(q)
            if q in cube:
                assert faces(*state)[2*axis] == faces(*cube[q])[2*axis+1]
                checks += 1
    periodic = []
    for size in range(1, 7):
        status, _ = planar_patch(size, periodic=True)
        assert status == "unsat"
        periodic.append({"planar_torus_size": size, "status": status})
    report = {"status": "verified matching-rule model; NOT a one-shape solution",
              "cube_state_count": len(WANG)**2, "patch_side": n,
              "patch_cells": n**3, "matched_neighbor_faces": checks,
              "planar_patch": planar, "small_periodic_controls": periodic,
              "states": [{"a": a, "b": b, "faces": faces(a, b)} for a, b in product(range(11), repeat=2)]}
    (out / "crossed_planes.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"121 symbolic states; {n**3} cells; {checks} matching interfaces; six periodic controls unsat.")


if __name__ == "__main__":
    run()

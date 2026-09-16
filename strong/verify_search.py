"""Independent SMT checks and exact voxel validation of search certificates."""

from itertools import permutations, product
import json
from pathlib import Path
import random

import numpy as np
import z3

from search_ports import DIRECTIONS, orientations, ROTATIONS


OUT = Path(__file__).parent / "artifacts"


def independent_states(tile):
    result = set()
    for axes in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            matrix = np.eye(3, dtype=int)[list(axes)] * np.array(signs)[:, None]
            if round(np.linalg.det(matrix)) != 1:
                continue
            state = [0] * 6
            for face, code in enumerate(tile):
                normal = tuple(matrix @ DIRECTIONS[face])
                arrow = tuple(matrix @ DIRECTIONS[(code % 12) // 2])
                state[DIRECTIONS.index(normal)] = 12 * (code // 12) + 2 * DIRECTIONS.index(arrow) + code % 2
            result.add(tuple(state))
    assert result == set(orientations(tile))
    return sorted(result)


def smt_open3(tile, dual):
    states = independent_states(tile)
    solver = z3.Solver()
    solver.set(timeout=10000)
    cells = list(product(range(3), repeat=3))
    values = {p: [z3.BitVec(f"f_{p[0]}_{p[1]}_{p[2]}_{d}", 7) for d in range(6)] for p in cells}
    for p in cells:
        solver.add(z3.Or([z3.And([values[p][d] == state[d] for d in range(6)]) for state in states]))
        for axis in range(3):
            q = list(p)
            q[axis] += 1
            q = tuple(q)
            if q in values:
                solver.add(values[p][2*axis] == (values[q][2*axis+1] ^ dual))
    # Deliberately no orientation anchoring: this checks the symmetry reduction.
    return str(solver.check())


def voxels(state):
    """Exact one-key solid, core [0,8)^3, shallow 2x2 off-center ports."""
    solid = set(product(range(8), repeat=3))
    for face, code in enumerate(state):
        assert code < 12, "voxel certificate here is for the one-key family"
        normal = DIRECTIONS[face]
        arrow = DIRECTIONS[code // 2]
        normal_axis = face // 2
        arrow_axis = (code // 2) // 2
        across_axis = 3 - normal_axis - arrow_axis
        center = 3.5 + 2 * arrow[arrow_axis]
        positions = [int(center-.5), int(center+.5)]
        plane = (8 if normal[normal_axis] > 0 else -1) if code % 2 else (7 if normal[normal_axis] > 0 else 0)
        for a, b in product(positions, (3, 4)):
            p = [0, 0, 0]
            p[normal_axis], p[arrow_axis], p[across_axis] = plane, a, b
            if code % 2:
                solid.add(tuple(p))
            else:
                solid.remove(tuple(p))
    assert len(solid) == 512
    return solid


def check_periodic_voxels(certificate):
    size = certificate["size"]
    states = certificate["states"]
    occupied = set()
    for cell, orientation in zip(product(range(size), repeat=3), certificate["assignment"]):
        for v in voxels(states[orientation]):
            p = tuple((v[k] + 8 * cell[k]) % (8 * size) for k in range(3))
            assert p not in occupied, (cell, orientation, p)
            occupied.add(p)
    assert len(occupied) == (8 * size) ** 3
    return len(occupied)


def run():
    rng = random.Random(20260915)
    results = []
    for filename, dual in (("port_search.json", 1), ("keyed_search.json", 1), ("dipole_search.json", 2)):
        if not (OUT / filename).exists():
            continue
        report = json.loads((OUT / filename).read_text())
        for outcome in ("no_open_3", "periodic_2", "periodic_3", "periodic_4", "periodic_6"):
            pool = [c for c in report["catalog"] if c["outcome"] == outcome]
            for case in rng.sample(pool, min(6, len(pool))):
                actual = smt_open3(case["tile"], dual)
                expected = "unsat" if outcome == "no_open_3" else "sat"
                assert actual == expected, (filename, case, actual)
                results.append({"family": filename, "tile": case["tile"], "expected": expected, "smt": actual})
        print(f"{filename}: independent SMT checks passed", flush=True)
    original = json.loads((OUT / "port_search.json").read_text())
    voxel_results = []
    for case in original["nontrivial_cases"]:
        if case["outcome"] == "periodic_6":
            count = check_periodic_voxels(case["checks"]["torus6"])
            voxel_results.append({"tile": case["tile"], "fundamental_domain_voxels": count,
                                  "overlaps": 0, "holes": 0})
    assert len(voxel_results) == 4
    output = {"status": "passed", "independent_unanchored_smt_checks": results,
              "exact_periodic_voxel_checks": voxel_results}
    (OUT / "verification.json").write_text(json.dumps(output, indent=2) + "\n")
    print(f"Verified {len(results)} SMT cases and four exact 6-cube periodic witnesses.")


if __name__ == "__main__":
    run()

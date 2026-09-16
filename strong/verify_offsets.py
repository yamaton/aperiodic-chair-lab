"""Independent geometry checks, SAT spot checks, and certificate audit."""

from collections import Counter
from itertools import permutations, product
import json

import numpy as np
import z3

from offset_dipoles import OUT
from refine_offsets import lattices, quotient
from search_ports import grid_problem


DIR = np.array(((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))


def matrices():
    result = []
    for order in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            r = np.eye(3, dtype=int)[list(order)] * np.array(signs)[:, None]
            if round(np.linalg.det(r)) == 1:
                result.append(r)
    return result


def fields(tile):
    # Physical outward height profile, expressed in world tangent coordinates.
    result = []
    for key, arrow, bias in tile:
        result.append({tuple(6 * (DIR[bias] + s * DIR[arrow])): s * (key + 1)
                       for s in (-1, 1)})
    return result


def rotated_fields(tile, r):
    result = [None] * 6
    for face, field in enumerate(fields(tile)):
        target = next(i for i, d in enumerate(DIR) if np.array_equal(d, r @ DIR[face]))
        result[target] = {tuple(r @ np.array(p)): height for p, height in field.items()}
    return result


def fit(a, b):
    return a == {p: -h for p, h in b.items()}


def solid(tile):
    voxels = set(product(range(32), repeat=3))
    for face, field in enumerate(fields(tile)):
        axis = face // 2
        tangents = [k for k in range(3) if k != axis]
        for position, height in field.items():
            for u, v, depth in product(range(2), range(2), range(abs(height))):
                p = [0, 0, 0]
                p[tangents[0]] = 15 + position[tangents[0]] + u
                p[tangents[1]] = 15 + position[tangents[1]] + v
                if height > 0:
                    p[axis] = 32 + depth if face % 2 == 0 else -1 - depth
                    voxels.add(tuple(p))
                else:
                    p[axis] = 31 - depth if face % 2 == 0 else depth
                    voxels.remove(tuple(p))
    assert len(voxels) == 32**3
    return voxels


def independent_sat(tile, size=3):
    states = [rotated_fields(tile, r) for r in matrices()]
    _, neighbors, _ = grid_problem(size, False)
    variables = [z3.Int(f"cell{i}") for i in range(len(neighbors))]
    solver = z3.Solver()
    solver.set(timeout=20000)
    solver.add([z3.And(v >= 0, v < 24) for v in variables])
    for i, links in enumerate(neighbors):
        for j, face in links:
            if j < i:
                continue
            solver.add(z3.Or(*[z3.And(variables[i] == s, variables[j] == t)
                               for s in range(24) for t in range(24)
                               if fit(states[s][face], states[t][face ^ 1])]))
    # No symmetry-breaking anchor; independent from the production search.
    return str(solver.check())


def run():
    initial = json.loads((OUT / "offset_dipoles_1.json").read_text())
    refined = json.loads((OUT / "offset_refinement.json").read_text())
    fixed_counts = []
    for r in matrices():
        mapping = [next(i for i, d in enumerate(DIR) if np.array_equal(d, r @ v)) for v in DIR]
        unseen, count = set(range(6)), 1
        while unseen:
            f = next(iter(unseen))
            cycle, current = [], f
            while current not in cycle:
                cycle.append(current)
                unseen.remove(current)
                current = mapping[current]
            count *= 8 if np.array_equal(np.linalg.matrix_power(r, len(cycle)), np.eye(3)) else 0
        fixed_counts.append(count)
    burnside = sum(fixed_counts) // 24
    assert burnside == initial["examined"] == 11072

    # Check the quotient's commuting translations and inverse edges.
    bases = list(lattices(12))
    assert len(bases) == 1325
    for basis in bases:
        _, graph = quotient(basis)
        for i, edges in enumerate(graph):
            for face in range(6):
                j = edges[face][0]
                assert graph[j][face ^ 1][0] == i
                for other in range(6):
                    assert graph[j][other][0] == graph[edges[other][0]][face][0]

    count, matched = 0, 0
    all_records = initial["certificates"] + refined
    for record in all_records:
        for name, check in record["checks"].items():
            if check["status"] != "sat":
                continue
            if name == "oblique":
                _, graph = quotient(check["basis_columns"])
            else:
                _, graph, _ = grid_problem(check["size"], check["periodic"])
            state_fields = [fields(s) for s in check["states"]]
            assert len(check["assignment"]) == len(graph)
            for i, links in enumerate(graph):
                for j, face in links:
                    assert fit(state_fields[check["assignment"][i]][face],
                               state_fields[check["assignment"][j]][face ^ 1])
                    matched += 1
            count += 1

    samples = []
    outcomes = sorted(set(c["outcome"] for c in initial["catalog"]))
    for outcome in outcomes:
        cases = [c for c in initial["catalog"] if c["outcome"] == outcome]
        for case in (cases[0], cases[len(cases) // 2], cases[-1]):
            result = independent_sat(case["tile"])
            expected = "unsat" if outcome.endswith("open_3") else "sat"
            assert result == expected, (case, result)
            samples.append({"tile": case["tile"], "classification": outcome,
                            "unanchored_open3": result})

    # Full voxel cover on an oblique quotient, not just abstract edge equality.
    example = next(c for c in refined if c["outcome"] == "periodic_oblique")
    check = example["checks"]["oblique"]
    basis = np.array(check["basis_columns"], dtype=int).T
    a, c, f = basis.diagonal() * 32
    b, d, e = basis[0, 1] * 32, basis[0, 2] * 32, basis[1, 2] * 32
    cells, _ = quotient(check["basis_columns"])
    occupancy = np.zeros((a, c, f), dtype=np.uint8)
    for cell, state in zip(cells, check["assignment"]):
        points = np.array(sorted(solid(check["states"][state]))) + np.array(cell) * 32
        q, points[:, 2] = np.divmod(points[:, 2], f)
        points[:, 0] -= q * d
        points[:, 1] -= q * e
        q, points[:, 1] = np.divmod(points[:, 1], c)
        points[:, 0] = (points[:, 0] - q * b) % a
        np.add.at(occupancy, tuple(points.T), 1)
    assert np.all(occupancy == 1)

    overrides = {tuple(map(tuple, r["tile"])): r["outcome"] for r in refined}
    totals = Counter(overrides.get(tuple(map(tuple, c["tile"])), c["outcome"])
                     for c in initial["catalog"])
    report = {"status": "passed", "burnside_orbit_count": burnside,
              "lattices_checked": len(bases), "sat_certificates_checked": count,
              "directed_interfaces_checked": matched, "independent_samples": samples,
              "exact_cover_example": {"tile": example["tile"], "basis_columns": check["basis_columns"],
                                      "covered_voxels": int(occupancy.size), "holes": 0, "overlaps": 0},
              "final_classifications": dict(totals), "new_family_total": sum(totals.values())}
    (OUT / "offset_verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "independent_samples"}, indent=2))


if __name__ == "__main__":
    run()

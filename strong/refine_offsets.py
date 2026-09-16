"""Search oblique repeat lattices and larger patches for offset-dipole blocks."""

from itertools import product
import json
import time

import z3

from offset_dipoles import OUT, compatible, compatibility, orientations, solve_graph
from search_ports import DIRECTIONS, grid_problem


def lattices(max_index):
    """All sublattices of Z^3 of index <= bound, in column Hermite form."""
    for index in range(1, max_index + 1):
        for a in range(1, index + 1):
            if index % a:
                continue
            for c in range(1, index // a + 1):
                if index % (a * c):
                    continue
                f = index // (a * c)
                for b, d, e in product(range(a), range(a), range(c)):
                    yield ((a, 0, 0), (b, c, 0), (d, e, f))


def quotient(basis):
    (a, _, _), (b, c, _), (d, e, f) = basis
    cells = list(product(range(a), range(c), range(f)))
    ids = {p: i for i, p in enumerate(cells)}

    def reduce(p):
        x, y, z = p
        q, z = divmod(z, f)
        x, y = x - q * d, y - q * e
        q, y = divmod(y, c)
        return ((x - q * b) % a, y, z)

    neighbors = [[(ids[reduce(tuple(p[k] + v[k] for k in range(3)))], face)
                  for face, v in enumerate(DIRECTIONS)] for p in cells]
    return cells, neighbors


def solve_sat(tile, size, periodic, seconds=20):
    started = time.monotonic()
    states = orientations(tile)
    allowed = compatibility(states)
    cells, neighbors, anchor = grid_problem(size, periodic)
    variables = [[z3.Bool(f"p{i}r{s}") for s in range(len(states))]
                 for i in range(len(cells))]
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=int(seconds * 1000))
    solver.add([z3.PbEq([(v, 1) for v in row], 1) for row in variables])
    if periodic or size % 2:
        solver.add(variables[anchor][0])
    for i, links in enumerate(neighbors):
        for j, face in links:
            solver.add([z3.Or(z3.Not(variables[i][s]),
                             *[variables[j][t] for t in range(len(states))
                               if mask & (1 << t)])
                        for s, mask in enumerate(allowed[face])])
    status = solver.check()
    result = {"status": str(status), "size": size, "periodic": periodic,
              "elapsed_seconds": time.monotonic() - started}
    if status == z3.sat:
        model = solver.model()
        assignment = [next(s for s, v in enumerate(row) if z3.is_true(model.eval(v)))
                      for row in variables]
        for i, links in enumerate(neighbors):
            for j, face in links:
                assert compatible(states[assignment[i]][face], states[assignment[j]][face ^ 1])
        result.update(assignment=assignment, states=states)
    return result


def run():
    initial = json.loads((OUT / "offset_dipoles_1.json").read_text())
    cases = [c for c in initial["catalog"] if c["outcome"] == "unresolved"]
    graphs = [(basis, quotient(basis)[1]) for basis in lattices(12)]
    print("Unresolved:", len(cases), "Lattices per case:", len(graphs), flush=True)
    records = []
    for case in cases:
        tile = case["tile"]
        record = {"tile": tile, "outcome": "unresolved", "checks": {}}
        states = orientations(tile)
        checked, unknown = 0, 0
        for basis, neighbors in graphs:
            # An oblique quotient is NOT invariant under all cube rotations.
            # In particular, fixing the origin's orientation would be unsound.
            result = solve_graph(states, neighbors, seconds=.1)
            checked += 1
            unknown += result["status"] == "unknown"
            if result["status"] == "sat":
                record["outcome"] = "periodic_oblique"
                record["checks"]["oblique"] = {**result, "basis_columns": basis}
                break
        record["lattice_search"] = {"maximum_index": 12, "checked": checked,
                                    "unknown": unknown}
        if record["outcome"] == "unresolved":
            for size, periodic in ((7, False), (8, True), (9, False),
                                   (12, True), (11, False)):
                result = solve_sat(tile, size, periodic)
                name = ("torus" if periodic else "open") + str(size)
                record["checks"][name] = result
                print(len(records), name, result["status"], flush=True)
                if periodic and result["status"] == "sat":
                    record["outcome"] = "periodic_" + str(size)
                    break
                if not periodic and result["status"] == "unsat":
                    record["outcome"] = "no_open_" + str(size)
                    break
        records.append(record)
        print(len(records), tile, record["outcome"], flush=True)
        (OUT / "offset_refinement.json").write_text(json.dumps(records) + "\n")


if __name__ == "__main__":
    run()

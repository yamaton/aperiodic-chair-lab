"""SAT-based second solver for the remaining one-solid candidate cases."""

from itertools import product
import json
from pathlib import Path
import time

import z3

from search_ports import compatibility, grid_problem, orientations


def solve_sat(tile, size, periodic, dual=2, seconds=30):
    started = time.monotonic()
    states = orientations(tile)
    allowed = compatibility(states, dual)
    cells, neighbors, anchor = grid_problem(size, periodic)
    variables = [[z3.Bool(f"c{i}s{s}") for s in range(len(states))] for i in range(len(cells))]
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=seconds * 1000)
    solver.add([z3.PbEq([(v, 1) for v in row], 1) for row in variables])
    if periodic or size % 2:
        solver.add(variables[anchor][0])
    clauses = []
    for i, links in enumerate(neighbors):
        for j, face in links:
            for s, mask in enumerate(allowed[face]):
                choices = [variables[j][t] for t in range(len(states)) if mask & (1 << t)]
                clauses.append(z3.Or(z3.Not(variables[i][s]), *choices))
    solver.add(clauses)
    status = solver.check()
    result = {"status": str(status), "size": size, "periodic": periodic,
              "elapsed_seconds": time.monotonic()-started}
    if status == z3.sat:
        model = solver.model()
        assignment = [next(s for s, v in enumerate(row) if z3.is_true(model.eval(v))) for row in variables]
        for i, links in enumerate(neighbors):
            for j, face in links:
                assert states[assignment[i]][face] == (states[assignment[j]][face ^ 1] ^ dual)
        result.update(assignment=assignment, states=states)
    return result


def run():
    out = Path(__file__).parent / "artifacts"
    initial = json.loads((out / "dipole_search.json").read_text())
    refined = json.loads((out / "dipole_refinement.json").read_text())
    classified = {tuple(c["tile"]): c for c in refined}
    records = []
    for case in initial["nontrivial_cases"]:
        if case["outcome"] != "unresolved":
            continue
        tile = case["tile"]
        previous = classified.get(tuple(tile))
        if previous and previous["outcome"] != "unresolved":
            continue
        print("Candidate", tile, flush=True)
        record = {"tile": tile, "outcome": "unresolved", "checks": {}}
        for size, periodic in ((7, False), (8, True), (10, True), (12, True), (9, False)):
            result = solve_sat(tile, size, periodic)
            name = ("torus" if periodic else "open") + str(size)
            record["checks"][name] = result
            print(name, result["status"], result["elapsed_seconds"], flush=True)
            if periodic and result["status"] == "sat":
                record["outcome"] = "periodic_" + str(size)
                break
            if not periodic and result["status"] == "unsat":
                record["outcome"] = "no_open_" + str(size)
                break
        records.append(record)
        (out / "sat_refinement.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    run()

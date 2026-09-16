"""Extract a small independently checked contradiction for the slow case."""

import json

import z3

from offset_dipoles import OUT
from open_chair_clusters import placements, region
from verify_open_chairs import independent_cover


def run():
    report = json.loads((OUT / "chair_screen_8_level5.json").read_text())
    tiles, _, _ = region(5)
    core = set(report["core_chairs"])
    index = 1
    shape = [(tuple(c), tuple(s)) for c, s in report["shapes"][index]["chairs"]]
    options = placements(shape, tiles, core)
    by_tile = {}
    for j, ids in enumerate(options):
        for i in ids:
            by_tile.setdefault(i, []).append(j)
    variables = [z3.Bool(f"p{j}") for j in range(len(options))]
    required = {i: z3.Bool(f"required{i}") for i in sorted(core)}
    solver = z3.Solver()
    solver.set(timeout=30000, unsat_core=True)
    for i, ids in by_tile.items():
        solver.add(z3.PbLe([(variables[j], 1) for j in ids], 1))
        if i in required:
            solver.add(z3.Implies(required[i], z3.Or(*[variables[j] for j in ids])))
    assert solver.check(*required.values()) == z3.unsat
    names = {str(v) for v in solver.unsat_core()}
    small = [i for i, v in required.items() if str(v) in names]
    # Delete unnecessary assumptions. A small witness makes the independent
    # checker fast; it is not necessary to claim a minimum-cardinality core.
    for i in list(small):
        trial = [j for j in small if j != i]
        if solver.check(*[required[j] for j in trial]) == z3.unsat:
            small = trial
    reduced = [ids for ids in options if set(ids).intersection(small)]
    sat, stats = independent_cover(reduced, set(small))
    assert not sat
    parity_obstruction = len(small) % 2 == 1 and all(len(set(ids) & set(small)) % 2 == 0 for ids in reduced)
    result = {"status": "independently verified unsatisfiable",
              "shape_index": index, "required_chairs": small,
              "all_placements_touching_required_chairs": reduced,
              "required_count": len(small), "placement_count": len(reduced),
              "backtracking": stats,
              "odd_required_set_even_intersections": parity_obstruction,
              "limit": "A sufficient contradiction certificate, not a claim of globally minimum size."}
    (OUT / "eight_chair_small_certificate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "all_placements_touching_required_chairs"}, indent=2))


if __name__ == "__main__":
    run()

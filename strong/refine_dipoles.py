"""Push surviving dipole candidates beyond the first periodicity screen."""

import json
from pathlib import Path

from search_ports import solve


def run():
    out = Path(__file__).parent / "artifacts"
    original = json.loads((out / "dipole_search.json").read_text())
    records = []
    for case in original["nontrivial_cases"]:
        if case["outcome"] != "unresolved":
            continue
        tile = case["tile"]
        record = {"tile": tile, "checks": {}, "outcome": "unresolved"}
        print("Candidate", tile, flush=True)
        for size, periodic in ((7, False), (8, True), (9, False), (10, True), (12, True)):
            result = solve(tile, size, periodic, seconds=5, node_limit=200000, dual=2)
            name = ("torus" if periodic else "open") + str(size)
            record["checks"][name] = result
            print(name, result["status"], result["nodes"], flush=True)
            if periodic and result["status"] == "sat":
                record["outcome"] = "periodic_" + str(size)
                break
            if not periodic and result["status"] == "unsat":
                record["outcome"] = "no_open_" + str(size)
                break
        records.append(record)
        (out / "dipole_refinement.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    run()

"""One solid with a tab AND a pocket on each face: complementary dipoles.

Unlike the sex-separated ports, a face can mate to its own rotated type.
The directed offset records the tab; the pocket is at the opposite offset.
Key types are arbitrary partitions of the six faces, up to color renaming.
"""

from itertools import product
import json
from pathlib import Path
import time

from search_ports import ROTATIONS, normalize_keys, orient, solve


def partitions(n, prefix=()):
    if len(prefix) == n:
        yield prefix
        return
    for key in range(max(prefix, default=-1) + 2):
        yield from partitions(n, prefix + (key,))


def candidates():
    seen = set()
    arrows = [tuple(d for d in range(6) if d // 2 != f // 2) for f in range(6)]
    for keys in partitions(6):
        for offsets in product(*arrows):
            tile = tuple(12 * keys[f] + 2 * offsets[f] for f in range(6))
            canonical = min(normalize_keys(orient(tile, r)) for r in ROTATIONS)
            if canonical not in seen:
                seen.add(canonical)
                yield canonical


def run():
    started = time.monotonic()
    stats = {"examined": 0, "periodic_2": 0, "periodic_3": 0,
             "periodic_4": 0, "periodic_6": 0, "no_open_3": 0,
             "no_open_5": 0, "unresolved": 0}
    catalog, special = [], []
    for tile in candidates():
        checks = {}
        outcome = None
        for size, periodic in ((2, True), (3, False), (3, True), (4, True), (6, True), (5, False)):
            result = solve(tile, size, periodic, seconds=.5, dual=2)
            checks[("torus" if periodic else "open") + str(size)] = result
            if periodic and result["status"] == "sat":
                outcome = "periodic_" + str(size)
                break
            if not periodic and result["status"] == "unsat":
                outcome = "no_open_" + str(size)
                break
        outcome = outcome or "unresolved"
        stats[outcome] += 1
        stats["examined"] += 1
        catalog.append({"tile": tile, "outcome": outcome})
        if outcome not in ("periodic_2", "no_open_3"):
            special.append({"tile": tile, "outcome": outcome, "checks": checks})
        if stats["examined"] % 1000 == 0:
            print(json.dumps(stats), flush=True)
    report = {"family": "one cube, six dipole faces, arbitrary face-key partition, four directions per face",
              "scope": "aligned cubic-grid tilings with all 24 proper cube rotations",
              "enumeration_complete": True, "dual_mask": 2, "stats": stats,
              "elapsed_seconds": time.monotonic()-started, "catalog": catalog,
              "nontrivial_cases": special}
    (Path(__file__).parent / "artifacts/dipole_search.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("catalog", "nontrivial_cases")}, indent=2))


if __name__ == "__main__":
    run()

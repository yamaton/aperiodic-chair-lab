"""One solid with two off-centre ports on each face; aligned-grid search.

A face is (key, arrow, bias). Ports lie at 6*bias +/- 6*arrow;
arrow and bias are perpendicular signed tangent coordinate directions.
The positive-arrow port is a tab, the negative-arrow port a pocket.
Matching requires equal key, opposite arrow, and equal bias.
Only proper rotations of the entire physical block are permitted.
"""

import argparse
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path
import time

from search_ports import DIRECTIONS, ROTATIONS, grid_problem


OUT = Path(__file__).parent / "artifacts"


def orient(tile, rotation):
    state = [None] * 6
    for face, (key, arrow, bias) in enumerate(tile):
        state[rotation[face]] = (key, rotation[arrow], rotation[bias])
    return tuple(state)


def orientations(tile):
    return list(dict.fromkeys(orient(tile, r) for r in ROTATIONS))


def canonical(tile):
    return min(orient(tile, r) for r in ROTATIONS)


def compatible(a, b):
    return a[0] == b[0] and a[1] == (b[1] ^ 1) and a[2] == b[2]


def compatibility(states):
    return [[sum(1 << j for j, other in enumerate(states)
                 if compatible(state[face], other[face ^ 1]))
             for state in states] for face in range(6)]


def solve_graph(states, neighbors, anchor=None, seconds=2, nodes_limit=200000):
    allowed = compatibility(states)
    domains = [(1 << len(states)) - 1] * len(neighbors)
    if anchor is not None:
        domains[anchor] = 1
    started = time.monotonic()
    deadline = started + seconds
    nodes = 0

    def visit(ds, seeds):
        nonlocal nodes
        nodes += 1
        if nodes > nodes_limit or time.monotonic() > deadline:
            raise TimeoutError
        queue = deque(seeds)
        while queue:
            i = queue.popleft()
            for j, face in neighbors[i]:
                mask, supported = ds[i], 0
                while mask:
                    bit = mask & -mask
                    supported |= allowed[face][bit.bit_length() - 1]
                    mask -= bit
                reduced = ds[j] & supported
                if not reduced:
                    return None
                if reduced != ds[j]:
                    ds[j] = reduced
                    queue.append(j)
        choices = [(d.bit_count(), i) for i, d in enumerate(ds) if d & (d - 1)]
        if not choices:
            assignment = [d.bit_length() - 1 for d in ds]
            # Self-edges of very small quotients need this explicit check:
            # arc consistency alone can support a different state at the same cell.
            for i, links in enumerate(neighbors):
                for j, face in links:
                    if not compatible(states[assignment[i]][face],
                                      states[assignment[j]][face ^ 1]):
                        return None
            return assignment
        _, i = min(choices)
        mask = ds[i]
        while mask:
            bit = mask & -mask
            mask -= bit
            child = ds.copy()
            child[i] = bit
            answer = visit(child, [i])
            if answer is not None:
                return answer
        return None

    try:
        assignment = visit(domains, range(len(neighbors)))
        status = "sat" if assignment is not None else "unsat"
    except TimeoutError:
        assignment, status = None, "unknown"
    result = {"status": status, "nodes": nodes,
              "elapsed_seconds": time.monotonic() - started}
    if assignment is not None:
        result.update(assignment=assignment, states=states)
    return result


def solve(tile, size, periodic, seconds=2):
    _, neighbors, anchor = grid_problem(size, periodic)
    result = solve_graph(orientations(tile), neighbors,
                         anchor if periodic or size % 2 else None, seconds)
    return {**result, "size": size, "periodic": periodic}


def refinements(keys=1):
    """Complete refinements of this key-count's old catalogue.

    Even the previously impossible base shapes are enumerated. A certificate
    that the coarse model has no open patch also excludes its refinements.
    """
    previous = json.loads((OUT / "dipole_search.json").read_text())
    seen = set()
    for case in previous["catalog"]:
        tile = case["tile"]
        if max(tile) // 12 + 1 != keys:
            continue
        choices = []
        for face, code in enumerate(tile):
            arrow = (code % 12) // 2
            choices.append([(code // 12, arrow, bias) for bias in range(6)
                            if bias // 2 not in (face // 2, arrow // 2)])
        for refined in product(*choices):
            normalized = canonical(refined)
            if normalized not in seen:
                seen.add(normalized)
                yield normalized, case["outcome"]


def run(keys=1, limit=0):
    started = time.monotonic()
    stats, catalog, certificates = Counter(), [], []
    for tile, coarse in refinements(keys):
        checks = {}
        if coarse.startswith("no_open_"):
            outcome = "inherited_" + coarse
        else:
            outcome = "unresolved"
            for size, periodic in ((2, True), (3, False), (3, True),
                                   (4, True), (5, False), (6, True), (7, False)):
                name = ("torus" if periodic else "open") + str(size)
                result = solve(tile, size, periodic, seconds=.3 if size < 5 else 1)
                checks[name] = result
                if periodic and result["status"] == "sat":
                    outcome = "periodic_" + str(size)
                    break
                if not periodic and result["status"] == "unsat":
                    outcome = "no_open_" + str(size)
                    break
        stats[outcome] += 1
        catalog.append({"tile": tile, "outcome": outcome})
        # Preserve every periodic certificate, and all nontrivial investigations.
        if outcome.startswith("periodic") or outcome == "unresolved" or len(checks) > 2:
            certificates.append({"tile": tile, "outcome": outcome, "checks": checks})
        if len(catalog) % 100 == 0:
            print(len(catalog), dict(stats), flush=True)
        if limit and len(catalog) >= limit:
            break
    report = {"family": "off-centre dipoles: arrow and perpendicular bias per face",
              "scope": "aligned cubic grid, 24 proper rotations, no reflections",
              "keys": keys, "enumeration_complete": not bool(limit),
              "examined": len(catalog), "stats": dict(stats),
              "elapsed_seconds": time.monotonic() - started,
              "catalog": catalog, "certificates": certificates}
    path = OUT / f"offset_dipoles_{keys}{'_sample' if limit else ''}.json"
    path.write_text(json.dumps(report, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("catalog", "certificates")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keys", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    run(args.keys, args.limit)

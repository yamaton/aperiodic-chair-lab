"""Search a concrete family of one-piece keyed cubes, allowing 24 rotations.

Each cube has three tabs and three pockets. Every port is offset in one of
four face-tangent directions. This is an exact matching model for aligned
8x8x8 voxel cores with shallow 2x2 ports. Unaligned tilings are NOT classified.
Periodic certificates disqualify candidates even without such a classification.
"""

import argparse
from collections import deque
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time


# Directions +x, -x, +y, -y, +z, -z. Port code = 2*arrow_direction + sex.
# Sex 1 is a tab, 0 is a pocket; matching ports have code xor 1.
DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def rotation_permutations():
    rotations = []
    for axes in permutations(range(3)):
        parity = (-1) ** sum(axes[i] > axes[j] for i in range(3) for j in range(i+1, 3))
        for signs in product((-1, 1), repeat=3):
            if parity * signs[0] * signs[1] * signs[2] != 1:
                continue
            mapping = []
            for vector in DIRECTIONS:
                transformed = tuple(signs[k] * vector[axes[k]] for k in range(3))
                mapping.append(DIRECTIONS.index(transformed))
            rotations.append(tuple(mapping))
    identity = tuple(range(6))
    rotations.remove(identity)
    return [identity] + sorted(rotations)


ROTATIONS = rotation_permutations()


def orient(tile, rotation):
    state = [0] * 6
    for face, code in enumerate(tile):
        state[rotation[face]] = 12 * (code // 12) + 2 * rotation[(code % 12) // 2] + code % 2
    return tuple(state)


def orientations(tile):
    return list(dict.fromkeys(orient(tile, rotation) for rotation in ROTATIONS))


def candidates():
    seen = set()
    arrows = [tuple(d for d in range(6) if d // 2 != face // 2) for face in range(6)]
    for tabs in combinations(range(6), 3):
        for offsets in product(*arrows):
            tile = tuple(2 * offsets[f] + int(f in tabs) for f in range(6))
            canonical = min(orient(tile, rotation) for rotation in ROTATIONS)
            if canonical not in seen:
                seen.add(canonical)
                yield canonical


def normalize_keys(tile):
    labels = {}
    result = []
    for code in tile:
        key = code // 12
        labels.setdefault(key, len(labels))
        result.append(12 * labels[key] + code % 12)
    return tuple(result)


def keyed_candidates(base_tiles):
    """All balanced two/three-key refinements of the given one-key tiles."""
    seen = set()
    for tile in base_tiles:
        tabs = [i for i, c in enumerate(tile) if c % 2]
        pockets = [i for i, c in enumerate(tile) if not c % 2]
        refinements = []
        for tab, pocket in product(tabs, pockets):
            refinements.append(tuple(c + (12 if i in (tab, pocket) else 0)
                                     for i, c in enumerate(tile)))
        for mates in permutations(pockets):
            keys = {}
            for key, (tab, pocket) in enumerate(zip(tabs, mates)):
                keys[tab] = keys[pocket] = key
            refinements.append(tuple(c + 12 * keys[i] for i, c in enumerate(tile)))
        for refinement in refinements:
            canonical = min(normalize_keys(orient(refinement, r)) for r in ROTATIONS)
            if canonical not in seen:
                seen.add(canonical)
                yield canonical


def compatibility(states, dual=1):
    return [[sum(1 << j for j, other in enumerate(states)
                 if state[face] == (other[face ^ 1] ^ dual))
             for state in states] for face in range(6)]


def grid_problem(size, periodic):
    cells = list(product(range(size), repeat=3))
    index = {p: i for i, p in enumerate(cells)}
    neighbors = [[] for _ in cells]
    for i, p in enumerate(cells):
        for face, direction in enumerate(DIRECTIONS):
            q = tuple(p[k] + direction[k] for k in range(3))
            if periodic:
                q = tuple(v % size for v in q)
            if q in index:
                neighbors[i].append((index[q], face))
    anchor = 0 if periodic else index[(size // 2,) * 3]
    return cells, neighbors, anchor


class SearchLimit(Exception):
    pass


def solve(tile, size, periodic, node_limit=100000, seconds=5, dual=1):
    states = orientations(tile)
    allowed = compatibility(states, dual)
    cells, neighbors, anchor = grid_problem(size, periodic)
    domains = [(1 << len(states)) - 1] * len(cells)
    # Cubic tori and odd open boxes can be rotated around the anchor.
    if periodic or size % 2:
        domains[anchor] = 1
    nodes = 0
    deadline = time.monotonic() + seconds

    def propagate(ds, seeds):
        queue = deque(seeds)
        while queue:
            i = queue.popleft()
            for j, face in neighbors[i]:
                mask = ds[i]
                supported = 0
                while mask:
                    bit = mask & -mask
                    supported |= allowed[face][bit.bit_length()-1]
                    mask -= bit
                new = ds[j] & supported
                if not new:
                    return False
                if new != ds[j]:
                    ds[j] = new
                    queue.append(j)
        return True

    def visit(ds, seeds):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or time.monotonic() > deadline:
            raise SearchLimit
        if not propagate(ds, seeds):
            return None
        choices = [(d.bit_count(), i) for i, d in enumerate(ds) if d & (d-1)]
        if not choices:
            return [d.bit_length()-1 for d in ds]
        _, i = min(choices)
        mask = ds[i]
        while mask:
            bit = mask & -mask
            mask -= bit
            child = ds.copy()
            child[i] = bit
            result = visit(child, [i])
            if result is not None:
                return result
        return None

    try:
        assignment = visit(domains, range(len(cells)))
    except SearchLimit:
        return {"status": "unknown", "nodes": nodes}
    if assignment is None:
        return {"status": "unsat", "nodes": nodes}
    # Validate every face, including wraparound, independently of propagation.
    for i, links in enumerate(neighbors):
        for j, face in links:
            assert states[assignment[i]][face] == (states[assignment[j]][face ^ 1] ^ dual)
    return {"status": "sat", "nodes": nodes, "size": size,
            "periodic": periodic, "assignment": assignment,
            "states": states}


def run(limit=0, keyed=False):
    start = time.monotonic()
    stats = {"examined": 0, "periodic_2": 0, "periodic_3": 0,
             "periodic_4": 0, "periodic_6": 0, "no_open_3": 0, "no_open_5": 0,
             "unresolved": 0}
    records = []
    catalog = []
    example = None
    if keyed:
        previous = json.loads((Path(__file__).parent / "artifacts/port_search.json").read_text())
        base_tiles = [c["tile"] for c in previous["catalog"] if c["outcome"] != "no_open_3"]
        stream = keyed_candidates(base_tiles)
    else:
        stream = candidates()
    for tile in stream:
        stats["examined"] += 1
        if stats["examined"] % 100 == 0:
            print(json.dumps(stats), flush=True)
        result = solve(tile, 2, True, seconds=.25)
        if result["status"] == "sat":
            outcome = "periodic_2"
            stats["periodic_2"] += 1
            if example is None:
                example = {"tile": tile, **result}
        else:
            open3 = solve(tile, 3, False, seconds=.5)
            if open3["status"] == "unsat":
                outcome = "no_open_3"
                stats["no_open_3"] += 1
            else:
                outcome = "unresolved"
                details = {"torus2": result, "open3": open3}
                for size in (3, 4, 6):
                    periodic = solve(tile, size, True, seconds=.5)
                    details[f"torus{size}"] = periodic
                    if periodic["status"] == "sat":
                        outcome = f"periodic_{size}"
                        break
                if outcome == "unresolved":
                    open5 = solve(tile, 5, False, seconds=1)
                    details["open5"] = open5
                    if open5["status"] == "unsat":
                        outcome = "no_open_5"
                stats[outcome] += 1
                records.append({"tile": tile, "outcome": outcome, "checks": details})
        catalog.append({"tile": tile, "outcome": outcome})
        if limit and stats["examined"] >= limit:
            break
    report = {"family": "one keyed cube, three tabs, three pockets, four port offsets per face",
              "keys": "two or three (balanced refinements)" if keyed else "one",
              "scope": "aligned cubic-grid tilings with all 24 proper cube rotations",
              "enumeration_complete": not bool(limit), "stats": stats,
              "elapsed_seconds": time.monotonic()-start,
              "periodic_example": example, "catalog": catalog, "nontrivial_cases": records}
    output = Path(__file__).parent / "artifacts"
    output.mkdir(exist_ok=True)
    filename = "keyed_search.json" if keyed else "port_search.json"
    (output / filename).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("periodic_example", "catalog", "nontrivial_cases")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0, help="0 enumerates the whole family")
    parser.add_argument("--keyed", action="store_true", help="refine the completed one-key catalog")
    args = parser.parse_args()
    run(args.limit, args.keyed)

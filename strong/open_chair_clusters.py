"""Whole-chair fusion with clusters permitted to cross the test boundary.

For each shape capable of covering a deep interior anchor, require an exact
cover of the core and allow partial coverage of a surrounding halo. Graph
distance certifies that every possible connected cluster touching the core
is fully represented. This is still coarse geometry, without X fillers.
"""

import argparse
from collections import Counter, deque
from itertools import product
import json
import time

import z3

from chair_clusters import key, patch
from chair_fusion import transforms
from offset_dipoles import OUT


def region(level):
    tiles = patch(level)
    owner = {}
    for i, (c, s) in enumerate(tiles):
        for p in product((-1, 1), repeat=3):
            if p != (1, 1, 1):
                q = tuple(2 * c[k] + s[k] * p[k] for k in range(3))
                assert q not in owner
                owner[q] = i
    adjacency, boundary = [set() for _ in tiles], set()
    for p, i in owner.items():
        for axis, sign in product(range(3), (-2, 2)):
            q = list(p)
            q[axis] += sign
            j = owner.get(tuple(q))
            if j is None:
                boundary.add(i)
            elif j != i:
                adjacency[i].add(j)
    distance = {i: 0 for i in boundary}
    queue = deque(boundary)
    while queue:
        i = queue.popleft()
        for j in adjacency[i]:
            if j not in distance:
                distance[j] = distance[i] + 1
                queue.append(j)
    assert len(distance) == len(tiles)
    return tiles, adjacency, distance


def shapes_at_anchor(tiles, adjacency, anchor, size):
    clusters = {frozenset([anchor])}
    for _ in range(size - 1):
        clusters = {cluster | {j} for cluster in clusters
                    for i in cluster for j in adjacency[i] if j not in cluster}
    return sorted({key([tiles[i] for i in sorted(cluster)]) for cluster in clusters}), len(clusters)


def placements(shape, tiles, core):
    variants = set()
    for axes, signs in transforms(True):
        variant = tuple(sorted((tuple(signs[k] * c[axes[k]] for k in range(3)),
                                tuple(signs[k] * s[axes[k]] for k in range(3)))
                               for c, s in shape))
        variants.add(variant)
    lookup = {tile: i for i, tile in enumerate(tiles)}
    by_direction = {}
    for i, (c, s) in enumerate(tiles):
        by_direction.setdefault(s, []).append(c)
    found = set()
    for variant in sorted(variants):
        base, direction = variant[0]
        for target in by_direction.get(direction, []):
            shift = tuple(target[k] - base[k] for k in range(3))
            ids = []
            for c, s in variant:
                i = lookup.get((tuple(c[k] + shift[k] for k in range(3)), s))
                if i is None:
                    break
                ids.append(i)
            else:
                if core.intersection(ids):
                    found.add(tuple(sorted(ids)))
    return sorted(found)


def cover(placement_list, core, seconds=20):
    by_tile = {}
    for p, ids in enumerate(placement_list):
        for i in ids:
            by_tile.setdefault(i, []).append(p)
    uncovered = sorted(core - by_tile.keys())
    if uncovered:
        return {"status": "unsat", "reason": "a core chair has no placement", "uncovered": uncovered}
    variables = [z3.Bool(f"cluster{p}") for p in range(len(placement_list))]
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=int(seconds * 1000))
    for i, ids in by_tile.items():
        terms = [(variables[p], 1) for p in ids]
        solver.add(z3.PbEq(terms, 1) if i in core else z3.PbLe(terms, 1))
    status = solver.check()
    result = {"status": str(status), "reason": "exact cover with optional halo"}
    if status == z3.sat:
        model = solver.model()
        selected = [ids for p, ids in enumerate(placement_list) if z3.is_true(model.eval(variables[p]))]
        counts = Counter(i for ids in selected for i in ids)
        assert max(counts.values()) == 1 and all(counts[i] == 1 for i in core)
        result["selected"] = selected
    return result


def run(level=4, size=4):
    started = time.monotonic()
    tiles, adjacency, distances = region(level)
    # A size-k connected cluster has graph diameter at most k-1. A missing
    # neighbor lies one step beyond a boundary chair. Distance >= k-1 thus
    # supplies enough halo for EVERY cluster containing a required chair.
    core = {i for i, d in distances.items() if d >= size - 1}
    if not core:
        raise ValueError("Patch too small to provide the required halo; increase --level")
    anchor = max(sorted(core), key=lambda i: distances[i])
    shapes, rooted_count = shapes_at_anchor(tiles, adjacency, anchor, size)
    print("Chairs", len(tiles), "core", len(core), "anchor", anchor,
          "depth", distances[anchor], "rooted clusters", rooted_count,
          "shape classes", len(shapes), flush=True)
    records, totals = [], Counter()
    for index, shape in enumerate(shapes):
        options = placements(shape, tiles, core)
        result = cover(options, core)
        totals[result["status"]] += 1
        records.append({"shape": shape, "placements": len(options), **result})
        if index % 25 == 0 or result["status"] != "unsat":
            print(index + 1, dict(totals), flush=True)
    report = {"status": "coarse fusion experiment, not a monotile construction",
              "level": level, "cluster_size": size, "chair_count": len(tiles),
              "core_chairs": sorted(core), "anchor": anchor, "anchor_depth": distances[anchor],
              "minimum_core_depth": size - 1, "rooted_connected_clusters": rooted_count,
              "candidate_shape_classes": len(shapes), "results": dict(totals), "records": records,
              "elapsed_seconds": time.monotonic() - started,
              "scope": "Face-connected clusters of whole coarse chairs, one proper-rotation class, in the specified substitution patch; halo coverage is optional.",
              "limits": "No fillers or markings. SAT does not establish infinite extension or force hierarchy in every geometric tiling."}
    path = OUT / f"open_chair_clusters_{size}_level{level}.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("records", "core_chairs")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=4)
    parser.add_argument("--size", type=int, default=4)
    args = parser.parse_args()
    run(args.level, args.size)

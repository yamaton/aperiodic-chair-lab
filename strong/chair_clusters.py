"""Look for four-chair clusters crossing first-level supertile boundaries.

Only face-connected clusters of whole coarse chairs are considered.
The fillers and their markings are deliberately not yet included: this is
a necessary coarse-geometry test for this particular fusion architecture.
"""

from collections import defaultdict
from itertools import combinations, product
import json
import time

import z3

from chair_fusion import transforms
from offset_dipoles import OUT


def patch(level):
    tiles = [((0, 0, 0), (1, 1, 1))]
    children = [((0, 0, 0), (1, 1, 1))]
    children.extend((tuple(-v for v in r), r) for r in product((-1, 1), repeat=3)
                    if r != (-1, -1, -1))
    for _ in range(level):
        tiles = [(tuple(2 * c[k] + s[k] * p[k] for k in range(3)),
                  tuple(s[k] * r[k] for k in range(3)))
                 for c, s in tiles for p, r in children]
    return tiles


def key(tiles):
    variants = []
    for axes, signs in transforms(True):
        centers = [tuple(signs[k] * c[axes[k]] for k in range(3)) for c, _ in tiles]
        directions = [tuple(signs[k] * s[axes[k]] for k in range(3)) for _, s in tiles]
        origin = tuple(min(c[k] for c in centers) for k in range(3))
        variants.append(tuple(sorted((tuple(c[k] - origin[k] for k in range(3)), s)
                                     for c, s in zip(centers, directions))))
    return min(variants)


def solve_cover(count, masks):
    full = (1 << count) - 1
    by_tile = [[m for m in masks if m & (1 << i)] for i in range(count)]
    failed = set()

    def visit(used):
        if used == full:
            return []
        if used in failed:
            return None
        choices = None
        for i in range(count):
            if used & (1 << i):
                continue
            options = [m for m in by_tile[i] if not m & used]
            if not options:
                return None
            if choices is None or len(options) < len(choices):
                choices = options
        for m in choices:
            result = visit(used | m)
            if result is not None:
                return [m, *result]
        failed.add(used)
        return None

    return visit(0)


def run():
    started = time.monotonic()
    tiles = patch(2)
    owner = {}
    for i, (c, s) in enumerate(tiles):
        for p in product((-1, 1), repeat=3):
            if p == (1, 1, 1):
                continue
            q = tuple(2 * c[k] + s[k] * p[k] for k in range(3))
            assert q not in owner
            owner[q] = i
    assert len(owner) == 7 * 64
    adjacency = [set() for _ in tiles]
    for p, i in owner.items():
        for axis, sign in product(range(3), (-2, 2)):
            q = list(p)
            q[axis] += sign
            j = owner.get(tuple(q))
            if j is not None and j != i:
                adjacency[i].add(j)
    clusters = {frozenset([i]) for i in range(len(tiles))}
    for _ in range(3):
        clusters = {cluster | {j} for cluster in clusters
                    for i in cluster for j in adjacency[i] if j not in cluster}
    # Independent enumeration over all C(64,4) subsets validates that the
    # incremental connected-set growth has neither missed nor added a cluster.
    independently_counted = 0
    for subset in combinations(range(len(tiles)), 4):
        unseen = set(subset[1:])
        reached = {subset[0]}
        while unseen:
            added = {j for j in unseen if adjacency[j] & reached}
            if not added:
                break
            reached |= added
            unseen -= added
        independently_counted += not unseen
    assert independently_counted == len(clusters)
    groups = defaultdict(list)
    for cluster in sorted(clusters, key=lambda c: tuple(sorted(c))):
        groups[key([tiles[i] for i in sorted(cluster)])].append(sum(1 << i for i in cluster))
    print("Connected four-chair placements:", len(clusters), "congruence classes:", len(groups), flush=True)
    full, eligible, solutions = (1 << len(tiles)) - 1, 0, []
    for shape, masks in groups.items():
        union = 0
        for mask in masks:
            union |= mask
        if union != full:
            continue
        eligible += 1
        result = solve_cover(len(tiles), masks)
        variables = [z3.Bool(f"cluster{i}") for i in range(len(masks))]
        solver = z3.Solver()
        for i in range(len(tiles)):
            solver.add(z3.PbEq([(v, 1) for v, m in zip(variables, masks) if m & (1 << i)], 1))
        sat_result = solver.check()
        assert sat_result == (z3.sat if result is not None else z3.unsat)
        if result is not None:
            solutions.append({"normalized_cluster": shape,
                              "partition": [[i for i in range(len(tiles)) if mask & (1 << i)]
                                            for mask in result]})
    report = {"status": "finite coarse-cluster experiment, not a monotile result",
              "level": 2, "chair_count": len(tiles), "connected_four_chair_placements": len(clusters),
              "proper_congruence_classes": len(groups), "classes_covering_each_chair_somewhere": eligible,
              "classes_admitting_an_exact_cover": len(solutions), "solutions": solutions,
              "independent_validation": {"all_four_subsets_checked": True,
                                         "eligible_classes_rechecked_with_z3": eligible},
              "elapsed_seconds": time.monotonic() - started,
              "scope": "One congruence class of face-connected four-chair clusters, 24 proper rotations; whole clusters lie inside this level-two supertile."}
    (OUT / "chair_clusters.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()

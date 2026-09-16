"""Check the open-core exclusions and the attachment parity obstruction."""

from collections import Counter
from itertools import combinations, product
import json

from chair_clusters import key, patch
from chair_fusion import transforms
from fused_chair import interior_points, rotate
from offset_dipoles import OUT
from open_chair_clusters import placements, region, shapes_at_anchor


def independent_cover(options, core):
    """Exact-cover search with mandatory propagation and optional halo."""
    masks = [sum(1 << i for i in ids) for ids in options]
    by_tile = {i: [j for j, ids in enumerate(options) if i in ids] for i in core}
    stats = Counter()

    def visit(remaining, used):
        stats["nodes"] += 1
        while remaining:
            chosen, choices = None, None
            for i in sorted(remaining):
                candidates = [j for j in by_tile[i] if not masks[j] & used]
                if not candidates:
                    stats["contradictions"] += 1
                    return False
                if choices is None or len(candidates) < len(choices):
                    chosen, choices = i, candidates
            if len(choices) == 1:
                j = choices[0]
                stats["forced_placements"] += 1
                used |= masks[j]
                remaining = remaining - set(options[j])
            else:
                for j in choices:
                    if visit(remaining - set(options[j]), used | masks[j]):
                        return True
                return False
        return True

    return visit(set(core), 0), dict(stats)


def run():
    report = json.loads((OUT / "open_chair_clusters_4_level4.json").read_text())
    tiles, adjacency, distances = region(4)
    core = set(report["core_chairs"])
    assert core == {i for i, d in distances.items() if d >= 3}
    anchor = report["anchor"]
    ball = {anchor}
    for _ in range(3):
        ball |= set().union(*(adjacency[i] for i in ball))
    # Exhaust all anchor-containing four-subsets of the radius-three ball;
    # this is independent of incrementally growing connected clusters.
    brute = set()
    for other in combinations(sorted(ball - {anchor}), 3):
        subset = {anchor, *other}
        reached = {anchor}
        while True:
            larger = reached | (set().union(*(adjacency[i] for i in reached)) & subset)
            if larger == reached:
                break
            reached = larger
        if reached == subset:
            brute.add(tuple(sorted(subset)))
    shapes, count = shapes_at_anchor(tiles, adjacency, anchor, 4)
    assert len(brute) == count == report["rooted_connected_clusters"]
    assert {key([tiles[i] for i in ids]) for ids in brute} == set(shapes)
    assert len(shapes) == report["candidate_shape_classes"]
    exact_checks = []
    for record in report["records"]:
        shape = tuple((tuple(c), tuple(s)) for c, s in record["shape"])
        options = placements(shape, tiles, core)
        assert len(options) == record["placements"]
        anchor_options = {tuple(ids) for ids in options if anchor in ids}
        assert anchor_options == {ids for ids in brute if key([tiles[i] for i in ids]) == shape}
        available = set().union(*(set(ids) for ids in options))
        if record["reason"] == "a core chair has no placement":
            assert sorted(core - available) == record["uncovered"]
        else:
            sat, stats = independent_cover(options, core)
            assert not sat and record["status"] == "unsat"
            exact_checks.append({"shape": record["shape"], **stats})

    # Check the exact centre recursion C_k = odd voxel centres union 2*C_(k-1).
    current = {c for c, _ in tiles}
    previous = {tuple(2 * v for v in c) for c, _ in patch(3)}
    s = 2**4
    odd = {p for p in product(range(-s + 1, s, 2), repeat=3) if min(p) < 0}
    assert current == odd | previous and not odd & previous
    interior = interior_points(4)
    pure_odd = [p for p in interior if all(v % 2 for v in p)]
    even_centers = [p for p in interior if p in current and all(v % 2 == 0 for v in p)]
    even_holes = [p for p in interior if p not in current and all(v % 2 == 0 for v in p)]
    assert pure_odd and all(p in current for p in pure_odd)
    assert even_centers and even_holes
    for axes, signs in transforms(False):
        for parity in product((0, 1), repeat=3):
            after = tuple(v % 2 for v in rotate(parity, axes, signs))
            assert sum(after) == sum(parity)
    result = {"status": "passed", "anchor_ball_chairs": len(ball),
              "independently_enumerated_rooted_clusters": len(brute),
              "shape_classes_checked": len(shapes), "exact_cover_cross_checks": exact_checks,
              "parity_checks": {"centre_recursion_exact": True,
                                "occupied_odd_interior_sites": len(pure_odd),
                                "occupied_even_interior_sites": len(even_centers),
                                "empty_even_interior_sites": len(even_holes),
                                "signed_permutations_checked": 48},
              "scope": "Finite certificates and algebraic checks supporting the conditional whole-piece fusion exclusions."}
    (OUT / "open_chair_verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "exact_cover_cross_checks"}, indent=2))


if __name__ == "__main__":
    run()

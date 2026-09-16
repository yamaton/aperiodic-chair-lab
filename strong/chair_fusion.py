"""A volume obstruction and bounded cluster test for Goodman-Strauss's pair.

This investigates fusing the already strongly aperiodic two-tile system.
It neither constructs a monotile nor claims to exhaust possible fusions.
"""

from fractions import Fraction
from itertools import combinations, permutations, product
import json

from offset_dipoles import OUT


def transforms(proper):
    for axes in permutations(range(3)):
        parity = (-1) ** sum(axes[i] > axes[j] for i in range(3) for j in range(i + 1, 3))
        for signs in product((-1, 1), repeat=3):
            if not proper or parity * signs[0] * signs[1] * signs[2] == 1:
                yield axes, signs


def normalize(cubes):
    origin = tuple(min(p[k] for p in cubes) for k in range(3))
    return tuple(sorted(tuple(p[k] - origin[k] for k in range(3)) for p in cubes))


def transformed(cubes, axes, signs):
    # Store doubled voxel centres, so signed rotations have no half-cell errors.
    return frozenset(tuple(signs[k] * p[axes[k]] for k in range(3)) for p in cubes)


def canonical(cubes, proper=True):
    return min(normalize(transformed(cubes, axes, signs)) for axes, signs in transforms(proper))


def connected(cubes):
    remaining = set(cubes)
    pending = [remaining.pop()]
    while pending:
        p = pending.pop()
        for axis, sign in product(range(3), (-2, 2)):
            q = list(p)
            q[axis] += sign
            q = tuple(q)
            if q in remaining:
                remaining.remove(q)
                pending.append(q)
    return not remaining


def run():
    # I has a square cross-section with half-width min(1/4, |x|).
    # Its three perpendicular copies have disjoint interiors and form X.
    i_volume = 2 * (4 * Fraction(1, 4)**3 / 3 + Fraction(3, 4) / 4)
    x_volume = 3 * i_volume
    # L gains the missing octant of X at its inner corner and loses
    # one octant at each of its seven outer corners.
    l_volume = 7 + x_volume / 8 - 7 * x_volume / 8
    x_per_l = (7 - l_volume) / x_volume
    i_per_l = (7 - l_volume) / i_volume
    assert (i_volume, x_volume, l_volume, x_per_l, i_per_l) == (
        Fraction(5, 12), Fraction(5, 4), Fraction(97, 16), Fraction(3, 4), Fraction(9, 4))

    # The paper's substitution S(L)=L union r(L-1), r != (-,-,-).
    base = frozenset(product((-1, 1), repeat=3)) - {(1, 1, 1)}
    children = [base]
    for signs in product((-1, 1), repeat=3):
        if signs != (-1, -1, -1):
            children.append(frozenset(tuple(signs[k] * (p[k] - 2) for k in range(3)) for p in base))
    whole = frozenset().union(*children)
    assert len(whole) == 56
    expected = frozenset(p for p in product((-3, -1, 1, 3), repeat=3)
                         if not all(x > 0 for x in p))
    assert whole == expected
    counts = {"bipartitions": 0, "both_connected": 0,
              "congruent_proper": 0, "congruent_with_reflections": 0}
    witnesses = []
    for rest in combinations(range(1, 8), 3):
        selected = (0, *rest)  # Count each unordered bipartition once.
        other = tuple(i for i in range(8) if i not in selected)
        a = frozenset().union(*(children[i] for i in selected))
        b = frozenset().union(*(children[i] for i in other))
        counts["bipartitions"] += 1
        counts["both_connected"] += connected(a) and connected(b)
        proper = canonical(a) == canonical(b)
        reflected = canonical(a, False) == canonical(b, False)
        counts["congruent_proper"] += proper
        counts["congruent_with_reflections"] += reflected
        if reflected:
            witnesses.append({"children_a": selected, "children_b": other,
                              "proper": proper, "voxels_a": sorted(a), "voxels_b": sorted(b)})
    report = {"source": "https://doi.org/10.1006/eujc.1998.0282",
              "status": "necessary conditions and finite cluster test; not a monotile",
              "volumes": {"I": str(i_volume), "X": str(x_volume), "L": str(l_volume)},
              "necessary_filler_ratios": {"X_per_L": str(x_per_l), "I_per_L": str(i_per_l)},
              "smallest_integral_fusion": {"L": 4, "X": 3},
              "level_one_coarse_test": counts, "witnesses": witnesses,
              "limits": ["Only whole-tile fusion with a fixed number of L and X pieces is addressed.",
                         "The cluster test requires four whole coarse chairs inside one level-one supertile.",
                         "Cross-boundary clusters, re-cut pieces, and other constructions are not excluded."]}
    (OUT / "chair_fusion.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()

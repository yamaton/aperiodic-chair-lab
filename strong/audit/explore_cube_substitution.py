"""Exact cube-label substitution and bounded coincidence exploration.

Reads only frozen coordinates; does not establish physical grid enforcement.
The subset search follows the coincidence-graph method of Frettloh and Sing
(2007); see ../review/LITERATURE_FOLLOWUP.md for attribution and scope.
Run from the project root with uv run --locked python <this file>.
"""

from collections import Counter, deque
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen_v1/candidate.json"
EXPECTED = "95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54"
LIMIT = 100_000


def mv(a, v):
    return tuple(sum(x * y for x, y in zip(row, v)) for row in a)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def det(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def lower_corner(rotation, cube):
    # Rotate its doubled center, then recover its lower corner.
    return tuple((x - 1) // 2 for x in
                 mv(rotation, tuple(2 * x + 1 for x in cube)))


def primitive_exponent(columns):
    n = len(columns)
    support = [set(c) for c in columns]
    for exponent in range(1, n * n + 2):
        if all(len(s) == n for s in support):
            return exponent
        new = [set().union(*(set(columns[j]) for j in s)) for s in support]
        if new == support:
            return None
        support = new
    return None


def coincidence(columns):
    """Close subsets under digit maps, retaining an explicit singleton word.

    Digits in a word are outermost-to-innermost: position after m digits
    is 2**(m-1)*d[0] + ... + d[m-1]. Complete closure without a singleton
    certifies failure of this criterion; hitting LIMIT means unknown.
    """
    initial = frozenset(range(len(columns)))
    paths = {initial: ()}
    queue = deque([initial])
    smallest = len(initial)
    while queue:
        states = queue.popleft()
        for digit in range(8):
            nxt = frozenset(columns[s][digit] for s in states)
            if nxt in paths:
                continue
            word = paths[states] + (digit,)
            paths[nxt] = word
            smallest = min(smallest, len(nxt))
            if len(nxt) == 1:
                return {"status": "coincidence", "word": word,
                        "output_state": next(iter(nxt)),
                        "visited_subsets": len(paths), "minimum_size": 1}
            queue.append(nxt)
            if len(paths) >= LIMIT:
                return {"status": "unknown_limit", "visited_subsets": len(paths),
                        "minimum_size": smallest}
    return {"status": "closed_without_coincidence", "visited_subsets": len(paths),
            "minimum_size": smallest,
            "subset_size_histogram": dict(sorted(Counter(map(len, paths)).items()))}


def main():
    raw = SOURCE.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED
    data = json.loads(raw)
    rotations = []
    for p in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            r = tuple(tuple(signs[i] if j == p[i] else 0 for j in range(3))
                      for i in range(3))
            if det(r) == 1:
                rotations.append(r)
    rotations.sort()
    rid = {r: i for i, r in enumerate(rotations)}
    cubes = [tuple(q) for q in data["coarse_cubes"]]
    children = [(tuple(c["center"]), tuple(map(tuple, c["matrix"])))
                for c in data["children"]]
    digits = list(product((0, 1), repeat=3))
    states = [(r, q) for r in rotations for q in cubes]
    sid = {s: i for i, s in enumerate(states)}
    columns = []
    tile_columns = []
    for r in rotations:
        child_cells = {}
        tile_columns.append([rid[mm(r, cr)] for _, cr in children])
        for c, cr in children:
            rc, rr = mv(r, c), mm(r, cr)
            for q in cubes:
                x = tuple(a + b for a, b in zip(rc, lower_corner(rr, q)))
                assert x not in child_cells
                child_cells[x] = sid[rr, q]
        expanded = set()
        for q in cubes:
            base = lower_corner(r, q)
            cells = [tuple(2 * x + d for x, d in zip(base, digit)) for digit in digits]
            expanded.update(cells)
            columns.append([child_cells[x] for x in cells])
        assert expanded == set(child_cells)
        assert len(expanded) == 56

    assert len(columns) == 168 and all(len(c) == 8 for c in columns)
    result = coincidence(columns)
    if result["status"] == "coincidence":
        position = (0, 0, 0)
        outputs = list(range(len(states)))
        sizes = [len(set(outputs))]
        for digit_index in result["word"]:
            position = tuple(2 * x + d for x, d in zip(position, digits[digit_index]))
            outputs = [columns[s][digit_index] for s in outputs]
            sizes.append(len(set(outputs)))
        assert len(set(outputs)) == 1
        result["residue_position"] = position
        result["modulus"] = 2 ** len(result["word"])
        result["image_sizes"] = sizes
        out_r, out_q = states[outputs[0]]
        result["output_label"] = {"rotation": out_r, "local_cube": out_q}

    # Cross-check every entry through depth three by directly expanding
    # chairs in coordinates, without using the cube-letter substitution.
    checked_cells = 0
    for r in rotations:
        patch = [((0, 0, 0), r)]
        for depth in range(1, 4):
            patch = [(tuple(2 * x + y for x, y in zip(c, mv(pr, cc))), mm(pr, cr))
                     for c, pr in patch for cc, cr in children]
            cells = {}
            for c, pr in patch:
                for q in cubes:
                    x = tuple(a + b for a, b in zip(c, lower_corner(pr, q)))
                    assert x not in cells
                    cells[x] = sid[pr, q]
            scale = 2 ** depth
            for q in cubes:
                base = lower_corner(r, q)
                for residue in product(range(scale), repeat=3):
                    s = sid[r, q]
                    for bit in reversed(range(depth)):
                        d = tuple((x >> bit) & 1 for x in residue)
                        s = columns[s][digits.index(d)]
                    x = tuple(scale * a + b for a, b in zip(base, residue))
                    assert cells[x] == s
                    checked_cells += 1

    # Does forgetting the three poses around the notch diagonal define a
    # letter-to-letter factor of this cube substitution? This is a stricter
    # test than mutual local derivability using a surrounding patch.
    coarse_labels = [(mv(r, (1, 1, 1)), lower_corner(r, q)) for r, q in states]
    groups = {}
    for i, label in enumerate(coarse_labels):
        groups.setdefault(label, []).append(i)
    conflicts = []
    for label, group in groups.items():
        for d in range(8):
            images = {coarse_labels[columns[s][d]] for s in group}
            if len(images) > 1:
                conflicts.append({"label": label, "digit": digits[d],
                                  "input_states": group, "outputs": sorted(images)})
    report = {
        "candidate_sha256": EXPECTED,
        "scope": "Exact finite substitution data; no cap-to-grid or spectral theorem verified.",
        "proper_rotations": len(rotations), "cube_states": len(states),
        "tile_orientation_primitive_exponent": primitive_exponent(tile_columns),
        "cube_substitution_primitive_exponent": primitive_exponent(columns),
        "direct_coordinate_crosscheck_cells": checked_cells,
        "orientation_row_sums": sorted(set(Counter(x for c in tile_columns for x in c).values())),
        "coincidence": result,
        "forget_pose": {"coarse_states": len(groups), "conflicts": len(conflicts),
                        "first_conflict": conflicts[0] if conflicts else None},
        "digits": digits,
        "states": [{"rotation": r, "local_cube": q} for r, q in states],
        "substitution_columns": columns,
    }
    output = HERE / "cube_substitution_exploration.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("states", "substitution_columns", "digits")}, indent=2))


if __name__ == "__main__":
    main()

"""Compare our cube substitution with Ben-Abraham--Flom's chair color code.

Source: Multidimensional color codes for chair tilings (2022), sections 2--3,
https://doi.org/10.1107/S2053273322004065 .
This checks a substitution factor, not equivalence of physical matching rules.
Run: uv run --locked python strong/audit/compare_published_chair_code.py
"""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "cube_substitution_exploration.json"
EXPECTED_TABLE = "163a4d6db496a61f08a67ffb68c9b446e368377500477e7e946ccadd337d0b10"
EXPECTED_CANDIDATE = "95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54"


def arrow(state):
    # Doubled vector from the unit cube's center toward its chair's notch.
    q = state["local_cube"]
    return tuple(-sum(row[j] * (2 * q[j] + 1) for j in range(3))
                 for row in state["rotation"])


def published_transition(c, digit):
    # The basic side-two cube has inward arrows s(d). Replace the arrow
    # diametrically opposite c by c (the rule in sections 2--3).
    basic = tuple(1 - 2 * x for x in digit)
    return c if basic == tuple(-x for x in c) else basic


def main():
    raw = SOURCE.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_TABLE
    data = json.loads(raw)
    assert data["candidate_sha256"] == EXPECTED_CANDIDATE
    assert sha256((HERE / "frozen_v1/candidate.json").read_bytes()).hexdigest() == EXPECTED_CANDIDATE
    digits = list(product((0, 1), repeat=3))
    assert data["digits"] == list(map(list, digits))
    colors = sorted(product((-1, 1), repeat=3))
    projection = list(map(arrow, data["states"]))
    assert len(projection) == 168 and set(projection) == set(colors)
    assert len(data["substitution_columns"]) == 168
    failures = []
    checked = 0
    for state, column in enumerate(data["substitution_columns"]):
        assert len(column) == 8
        for d, target in enumerate(column):
            expected = published_transition(projection[state], digits[d])
            checked += 1
            if projection[target] != expected:
                failures.append({"state": state, "digit": digits[d],
                                 "expected": expected, "actual": projection[target]})
    assert not failures, failures[:3]
    report = {
        "source_doi": "10.1107/S2053273322004065",
        "source_sections": "2--3 (inward body-diagonal arrows, opposite-cell replacement)",
        "scope": "Exact factor of substitution tables; not equality of tiling spaces or rules.",
        "candidate_sha256": EXPECTED_CANDIDATE,
        "input_table_sha256": EXPECTED_TABLE,
        "input_states": len(projection), "factor_states": len(colors),
        "checked_transitions": checked, "mismatches": len(failures),
        "colors": colors,
        "states_per_color": [Counter(projection)[c] for c in colors],
        "projection_to_color_index": [colors.index(c) for c in projection],
        "factor_columns": [[colors.index(published_transition(c, d)) for d in digits]
                           for c in colors],
        "digits": digits,
    }
    output = HERE / "published_chair_code_comparison.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {checked} transitions, 168 -> 8 states, zero mismatches.")
    print(f"Each arrow has 21 input labels. Report: {output.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main()

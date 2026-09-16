"""Check all integer-offset contacts of two complete recut chair groups.

Odd fine-grid offsets become half-integer offsets after deflation. Excluding
them is necessary before iterating the grouping argument on a common grid.
"""

from collections import defaultdict
from itertools import product
import json

from chair_recut import (IDENTITY, PORTS, VOXELS, contact_types, oriented_patch,
                         rotate)
from offset_dipoles import OUT


def macro_boundary(template, labels):
    voxels, ports = set(), defaultdict(list)
    for c, r in oriented_patch(template, 1):
        for p in VOXELS:
            moved = rotate(p, r)
            q = tuple(2 * c[k] + moved[k] for k in range(3))
            assert q not in voxels
            voxels.add(q)
        for (p, n), label in zip(PORTS, labels):
            moved = rotate(p, r)
            q = tuple(16 * c[k] + moved[k] for k in range(3))
            ports[q].append((rotate(n, r), label))
    outer = []
    for p, entries in ports.items():
        if len(entries) == 1:
            n, label = entries[0]
            outer.append((p, n, label))
        else:
            assert len(entries) == 2
            (a, la), (b, lb) = entries
            assert a == tuple(-x for x in b) and la == -lb
    assert len(voxels) == 56 and len(outer) == 768
    return voxels, outer


def face_profiles(ports, r):
    faces = defaultdict(list)
    for p, n, label in ports:
        p, n = rotate(p, r), rotate(n, r)
        axis = next(k for k in range(3) if n[k])
        center = tuple(p[k] // 8 if k == axis else (p[k] + 4) // 8 for k in range(3))
        offset = tuple(p[k] - 8 * center[k] for k in range(3))
        faces[center, n].append((offset, n[axis] * label))
    assert len(faces) == 96 and all(len(row) == 8 for row in faces.values())
    return {key: tuple(label for _, label in sorted(row)) for key, row in faces.items()}


def run():
    profile = json.loads((OUT / "chair_recut_synthesis.json").read_text())["profiles"][1]
    voxels, ports = macro_boundary(profile["template"], profile["labels"])
    orientations = [face_profiles(ports, r) for r in range(24)]
    oriented_voxels = [{rotate(p, r) for p in voxels} for r in range(24)]
    reference = orientations[IDENTITY]
    records, contact_count = [], 0
    for t in product(range(-4, 5), repeat=3):
        for r in range(24):
            shifted = {tuple(2 * t[k] + p[k] for k in range(3)) for p in oriented_voxels[r]}
            if voxels & shifted:
                continue
            contacts, mismatches = 0, 0
            for (p, n), value in orientations[r].items():
                q = tuple(2 * t[k] + p[k] for k in range(3))
                opposite = tuple(-x for x in n)
                other = reference.get((q, opposite))
                if other is not None:
                    contacts += 1
                    mismatches += value != other
            if contacts:
                contact_count += 1
                if not mismatches:
                    records.append({"shift": t, "rotation": r, "unit_faces": contacts})
    odd = [record for record in records if any(x % 2 for x in record["shift"])]
    types = contact_types()
    allowed = {(t, r) for t, r, pairs in types
               if all(profile["labels"][a] == -profile["labels"][b] for a, b in pairs)}
    deflated = {(tuple(x // 2 for x in record["shift"]), record["rotation"])
                for record in records if not any(x % 2 for x in record["shift"])}
    result = {"profile_index": 1, "geometric_macro_contacts_checked": contact_count,
              "compatible_macro_contacts": records,
              "compatible_contact_count": len(records),
              "half_integer_deflated_contacts": odd,
              "deflated_rules_equal_original": deflated == allowed,
              "scope": "Macrochairs have integer fine-grid centers and proper cube orientations; arbitrary real offsets and orientations are not covered."}
    (OUT / "chair_recut_macro.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "compatible_macro_contacts"}, indent=2))


if __name__ == "__main__":
    run()

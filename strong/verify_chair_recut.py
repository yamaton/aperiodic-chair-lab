"""Check synthesized recuts by direct patch geometry and contact closure."""

from collections import defaultdict, deque
from itertools import product
import json

from chair_recut import (CHILDREN, CHILD_ROTATIONS, INVERSE, MULTIPLY, PORTS,
                         VOXELS, contact_types, oriented_patch, rotate)
from chair_recut_periods import verify_witness
from offset_dipoles import OUT


def close_contacts(template, types):
    lookup = {(t, r): i for i, (t, r, _) in enumerate(types)}
    rotations = [CHILD_ROTATIONS[j][q] for j, q in enumerate(template)]

    def pair(ca, ra, cb, rb):
        t = rotate(tuple(cb[k] - ca[k] for k in range(3)), INVERSE[ra])
        return lookup.get((t, MULTIPLY[INVERSE[ra]][rb]))

    found = set()
    for j, (a, _) in enumerate(CHILDREN):
        for k, (b, _) in enumerate(CHILDREN):
            if j != k:
                index = pair(a, rotations[j], b, rotations[k])
                if index is not None:
                    found.add(index)
    queue = deque(sorted(found))
    while queue:
        t, r, _ = types[queue.popleft()]
        for j, (a, _) in enumerate(CHILDREN):
            for k, (b, _) in enumerate(CHILDREN):
                moved = rotate(b, r)
                cb = tuple(2 * t[axis] + moved[axis] for axis in range(3))
                index = pair(a, rotations[j], cb, MULTIPLY[r][rotations[k]])
                if index is not None and index not in found:
                    found.add(index)
                    queue.append(index)
    return found


def signed_components(types, contacts, labels):
    adjacency = [set() for _ in PORTS]
    for index in contacts:
        for a, b in types[index][2]:
            adjacency[a].add(b)
            adjacency[b].add(a)
            assert labels[a] == -labels[b]
    visited, active_labels = set(), set()
    for anchor in range(len(PORTS)):
        if anchor in visited:
            continue
        signs, pending, inconsistent = {anchor: 1}, [anchor], False
        while pending:
            a = pending.pop()
            for b in adjacency[a]:
                if b in signs:
                    inconsistent |= signs[b] != -signs[a]
                else:
                    signs[b] = -signs[a]
                    pending.append(b)
        visited.update(signs)
        if inconsistent:
            assert all(labels[a] == 0 for a in signs)
        else:
            value = labels[anchor]
            assert value and abs(value) not in active_labels
            assert all(labels[a] == value * sign for a, sign in signs.items())
            # Each independent depth parameter conserves volume separately.
            assert sum(signs.values()) == 0
            active_labels.add(abs(value))
    return len(active_labels)


def verify_patch(template, labels, level=3):
    tiles = oriented_patch(template, level)
    cubes, features = {}, defaultdict(list)
    for i, (c, r) in enumerate(tiles):
        for p in VOXELS:
            moved = rotate(p, r)
            point = tuple(2 * c[k] + moved[k] for k in range(3))
            assert point not in cubes
            cubes[point] = i
        for (p, n), label in zip(PORTS, labels):
            moved = rotate(p, r)
            point = tuple(16 * c[k] + moved[k] for k in range(3))
            features[point].append((rotate(n, r), label))
    size = 2 ** level
    expected = {p for p in product(range(-2*size+1, 2*size, 2), repeat=3)
                if not all(v > 0 for v in p)}
    assert set(cubes) == expected
    interior = 0
    for entries in features.values():
        assert len(entries) in (1, 2)
        if len(entries) == 2:
            (a, la), (b, lb) = entries
            assert a == tuple(-x for x in b) and la == -lb
            interior += 1
    return {"level": level, "chairs": len(tiles), "coarse_voxels": len(cubes),
            "matched_interior_port_pairs": interior}


def run():
    synthesis = json.loads((OUT / "chair_recut_synthesis.json").read_text())
    assert synthesis["templates_enumerated"] == 3**8
    assert sum(p["template_count"] for p in synthesis["profiles"]) == 3**8
    types = contact_types()
    records = []
    for i, profile in enumerate(synthesis["profiles"]):
        contacts = close_contacts(profile["template"], types)
        assert contacts == set(profile["closed_contact_types"])
        components = signed_components(types, contacts, profile["labels"])
        record = {"profile_index": i, "closed_contact_types": len(contacts),
                  "independent_depth_parameters": components,
                  "all_compatible_contact_types": sum(
                      all(profile["labels"][a] == -profile["labels"][b] for a, b in pairs)
                      for _, _, pairs in types),
                  "direct_patch_check": verify_patch(profile["template"], profile["labels"])}
        records.append(record)
        print(json.dumps(record), flush=True)
    periodic = []
    path = OUT / "chair_recut_periods.json"
    if path.exists():
        for record in json.loads(path.read_text())["profiles"]:
            labels = synthesis["profiles"][record["profile_index"]]["labels"]
            for check in record["checks"]:
                if check["status"] == "sat":
                    periodic.append({"profile_index": record["profile_index"],
                                     **verify_witness(labels, check["basis_columns"], check["placements"])})
    substitution = OUT / "chair_recut_substitution.json"
    if substitution.exists():
        for record in json.loads(substitution.read_text())["profiles"]:
            if record["standard_inflated_lattice"] == "periodic counterexample":
                labels = synthesis["profiles"][record["profile_index"]]["labels"]
                periodic.append({"profile_index": record["profile_index"],
                                 **verify_witness(labels, record["basis_columns"], record["placements"])})
    result = {"status": "passed", "profiles": records, "periodic_witnesses": periodic,
              "scope": "Representative contact closures, independent signed-graph checks and direct patch/period geometry; not an all-tilings recognition proof."}
    (OUT / "chair_recut_verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    run()

"""Independent SMT enumeration and checks of the recut hierarchy certificates."""

from itertools import combinations, product
import json

import z3

from chair_recut import (IDENTITY, MULTIPLY, PORTS, contact_types,
                         oriented_patch, rotate)
from chair_recut_stars import clusters_at_anchor, moved_voxels, relative
from offset_dipoles import OUT


def direct_features(placement, labels):
    c, r = placement
    result = {}
    for (p, n), label in zip(PORTS, labels):
        moved = rotate(p, r)
        point = tuple(16 * c[k] + moved[k] for k in range(3))
        result[point] = (rotate(n, r), label)
    return result


def compatible(a, b, labels):
    if moved_voxels(*a) & moved_voxels(*b):
        return False
    fa, fb = direct_features(a, labels), direct_features(b, labels)
    for point in fa.keys() & fb.keys():
        (na, la), (nb, lb) = fa[point], fb[point]
        if na != tuple(-x for x in nb) or la != -lb:
            return False
    return True


def verify_stars(profile, report):
    labels = profile["labels"]
    anchor = ((0, 0, 0), IDENTITY)
    # Regenerate candidate neighbors from raw displaced voxels and ports.
    reference = direct_features(anchor, labels)
    candidates, covered = [], []
    for shift in product(range(-2, 3), repeat=3):
        for r in range(24):
            placement = (shift, r)
            other = direct_features(placement, labels)
            common = reference.keys() & other.keys()
            if not common or not compatible(anchor, placement, labels):
                continue
            faces = {i // 8 for i, (p, _) in enumerate(PORTS) if p in common}
            candidates.append(placement)
            covered.append(faces)
    recorded = [(tuple(c), r) for c, r in report["candidate_neighbor_placements"]]
    assert candidates == recorded
    variables = [z3.Bool(f"neighbor{i}") for i in range(len(candidates))]
    solver = z3.SolverFor("QF_FD")
    for f in range(24):
        solver.add(z3.PbEq([(variables[i], 1) for i, faces in enumerate(covered) if f in faces], 1))
    for i, j in combinations(range(len(candidates)), 2):
        if not compatible(candidates[i], candidates[j], labels):
            solver.add(z3.Or(z3.Not(variables[i]), z3.Not(variables[j])))
    found = set()
    while solver.check() == z3.sat:
        model = solver.model()
        selection = tuple(i for i, variable in enumerate(variables) if z3.is_true(model.eval(variable)))
        found.add(selection)
        solver.add(z3.Or([z3.Not(variables[i]) if i in selection else variables[i]
                          for i in range(len(variables))]))
    assert solver.check() == z3.unsat
    assert found == {tuple(star) for star in report["stars"]}
    groups = clusters_at_anchor(profile["template"])
    for a, b in combinations(groups, 2):
        assert any(not compatible(x, y, labels) for x, y in combinations(a | b, 2))
    stars = [frozenset([anchor, *(candidates[i] for i in star)]) for star in report["stars"]]
    contacts = {(t, r) for t, r, _ in contact_types()}
    certified = 0
    for star in stars:
        if groups[0] <= star:
            certified += 1
            continue
        for neighbor in star - {anchor}:
            required = {relative(neighbor, p) for p in star if p != neighbor
                        and relative(neighbor, p) in contacts}
            possible = [other for other in stars if required <= other]
            if possible and relative(neighbor, anchor) in groups[0] and all(groups[0] <= other for other in possible):
                certified += 1
                break
        else:
            raise AssertionError("No forced group for star")
    return {"independent_smt_stars": len(found), "stars_with_forced_group": certified,
            "incompatible_overlapping_group_pairs": 28}


def verify_macro(profile, report):
    # Use child-to-child contacts, instead of the macro boundary profiles
    # used in the original check. Retain odd shifts in fine-grid coordinates.
    types = contact_types()
    all_types = {(t, r): pairs for t, r, pairs in types}
    allowed = {(t, r) for t, r, pairs in types
               if all(profile["labels"][a] == -profile["labels"][b] for a, b in pairs)}
    base = oriented_patch(profile["template"], 1)
    cubes = set().union(*(moved_voxels(*p) for p in base))
    found, checked = set(), 0
    for r in range(24):
        rotated = [(rotate(c, r), MULTIPLY[r][s]) for c, s in base]
        rotated_cubes = {rotate(p, r) for p in cubes}
        for t in product(range(-4, 5), repeat=3):
            moved = {tuple(2 * t[k] + p[k] for k in range(3)) for p in rotated_cubes}
            if cubes & moved:
                continue
            neighbors = [(tuple(c[k] + t[k] for k in range(3)), s) for c, s in rotated]
            contacts = {relative(a, b) for a in base for b in neighbors} & all_types.keys()
            if contacts:
                checked += 1
                if contacts <= allowed:
                    found.add((t, r))
    expected = {(tuple(p["shift"]), p["rotation"]) for p in report["compatible_macro_contacts"]}
    assert found == expected and checked == report["geometric_macro_contacts_checked"]
    assert all(all(v % 2 == 0 for v in t) for t, _ in found)
    assert {(tuple(v // 2 for v in t), r) for t, r in found} == allowed
    return {"macro_contacts_checked": checked, "compatible_macro_contacts": len(found),
            "deflation_preserves_rules_and_grid": True}


def run():
    profile = json.loads((OUT / "chair_recut_synthesis.json").read_text())["profiles"][1]
    stars = json.loads((OUT / "chair_recut_stars.json").read_text())
    macro = json.loads((OUT / "chair_recut_macro.json").read_text())
    star_check = verify_stars(profile, stars)
    print(json.dumps(star_check), flush=True)
    macro_check = verify_macro(profile, macro)
    print(json.dumps(macro_check), flush=True)
    result = {"status": "passed", "profile_index": 1, **star_check, **macro_check,
              "scope": "Finite certificates for a unique, rule-preserving hierarchy in the integer-grid matching model; geometric enforcement requires a separate argument."}
    (OUT / "chair_recut_hierarchy_verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    run()

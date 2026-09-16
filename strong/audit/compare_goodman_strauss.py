"""Exact comparison with Goodman-Strauss's three coarse contact families.

Published paper (1999): Lemma 2.2, markings on p.389, Proposition 4.6.
Author preprint: Lemma 1.2, markings in section 2, Theorem 3.6.
No claim of equivalence with the full marked L/I or L/X tiling spaces.
Run: uv run --locked python strong/audit/compare_goodman_strauss.py
"""

from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = "95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54"
ONE = (1, 1, 1)
ZERO = (0, 0, 0)
IDENTITY = (1, 0, 0, 0, 1, 0, 0, 0, 1)


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def neg(a): return tuple(-x for x in a)
def act(r, v): return tuple(sum(r[3*i+j]*v[j] for j in range(3)) for i in range(3))
def transpose(r): return tuple(r[3*j+i] for i in range(3) for j in range(3))
def mul(r, s): return tuple(sum(r[3*i+k]*s[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def determinant(r):
    a, b, c, d, e, f, g, h, i = r
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def gs_families():
    """Transcribe published Lemma 2.2 in (origin, missing-octant) form."""
    out = {}
    for axis in range(3):
        for sign in (-1, 1):
            t = tuple(2*sign*int(i == axis) for i in range(3))
            out[t, tuple(-1 if i == axis else 1 for i in range(3))] = "i"
            out[t, tuple(1 if i == axis else -1 for i in range(3))] = "ii"
    for s in product((-1, 1), repeat=3):
        if s != neg(ONE):
            out[ONE, s] = "iii"
            out[neg(s), s] = "iii"  # Inverse of x -> diag(s)x + 1.
    assert Counter(out.values()) == {"i": 6, "ii": 6, "iii": 14}
    return out


def marker(s, n):
    """Old diagonal arrow at endpoint c+n, expressed in world coordinates.

    n is a signed coordinate unit vector, s the missing-octant direction.
    Only arrow direction is encoded, not the outline of its black region.
    """
    sign = sum(a*b for a, b in zip(s, n))
    return tuple(sign*(a-sign*b) for a, b in zip(s, n))


def main():
    inputs = {}
    for name in ("frozen_v1/candidate.json", "face_motifs.json", "motif_grouping_certificate.json"):
        raw = (HERE / name).read_bytes()
        inputs[name] = (json.loads(raw), sha256(raw).hexdigest())
    data = inputs["frozen_v1/candidate.json"][0]
    assert inputs["frozen_v1/candidate.json"][1] == EXPECTED
    motifs = inputs["face_motifs.json"][0]
    certificate = inputs["motif_grouping_certificate.json"][0]
    assert motifs["candidate_sha256"] == certificate["candidate_sha256"] == EXPECTED
    rotations = sorted(r for p in permutations(range(3)) for signs in product((-1, 1), repeat=3)
                       if determinant(r := tuple(signs[i]*int(j == p[i]) for i in range(3) for j in range(3))) == 1)
    poses = {s: [r for r in rotations if act(r, ONE) == s]
             for s in product((-1, 1), repeat=3)}
    assert all(len(rs) == 3 for rs in poses.values())
    normals = [tuple(sign*int(i == axis) for i in range(3))
               for axis in range(3) for sign in (-1, 1)]
    base = set(map(tuple, data["coarse_cubes"]))

    @cache
    def placed(t, r):
        cells = {add(t, tuple((v-1)//2 for v in act(r, tuple(2*x+1 for x in q)))) for q in base}
        faces = {(add(tuple(2*x for x in t), act(r, f["center_times_2"])), act(r, f["normal"])):
                 (f["motif"], act(r, f["arrow"])) for f in motifs["face_descriptors"]}
        return cells, faces

    def shared(a, b):
        af, bf = placed(*a)[1], placed(*b)[1]
        return [(f, n, value, bf[f, neg(n)]) for (f, n), value in af.items() if (f, neg(n)) in bf]

    def fitting(a, b):
        if placed(*a)[0] & placed(*b)[0]:
            return False
        for _, n, (name, u), (other, v) in shared(a, b):
            if not ((name == other == "A" and v == cross(n, u)) or
                    ((name, other) in (("B", "C"), ("C", "B")) and v == neg(u))):
                return False
        return True

    anchor = ZERO, IDENTITY
    geometric, raw_contacts = set(), set()
    for r in rotations:
        rotated = placed(ZERO, r)[0]
        offsets = {sub(add(q, n), b) for q in base for n in normals
                   if add(q, n) not in base for b in rotated}
        for t in offsets:
            if not base & placed(t, r)[0] and shared(anchor, (t, r)):
                geometric.add((t, r))
                if fitting(anchor, (t, r)):
                    raw_contacts.add((t, r))
    saved = {(tuple(c["center"]), tuple(c["rotation"])) for c in certificate["contact_table"]}
    assert len(geometric) == 1194 and raw_contacts == saved and len(saved) == 44
    cover = {c: {(f, n) for f, n, _, _ in shared(anchor, c)} for c in raw_contacts}
    anchor_faces = set(placed(*anchor)[1])
    # Recheck the one-round impossible-face exclusions, without project imports.
    removed = {c for c in raw_contacts if any(
        not any(face in cover[b] and not cover[b] & cover[c] and fitting(b, c)
                for b in raw_contacts if b != c)
        for face in anchor_faces - cover[c])}
    saved_removed_ids = {x["candidate"] for batch in certificate["pruning"] for x in batch}
    saved_removed = {(tuple(c["center"]), tuple(c["rotation"]))
                     for c in certificate["contact_table"] if c["id"] in saved_removed_ids}
    assert removed == saved_removed and len(removed) == 14
    surviving = raw_contacts - removed
    families = gs_families()
    # Independently check the old axial arrow criterion for all eight notch
    # directions, including the directions excluded by its equality rule.
    arrow_tests = 0
    for n, s in product(normals, poses):
        t = tuple(2*x for x in n)
        assert (marker(ONE, n) == marker(s, neg(n))) == ((t, s) in families)
        arrow_tests += 1

    rows = []
    for (t, s), family in sorted(families.items()):
        raw_matrix, live_matrix = [], []
        for root in poses[ONE]:
            rr, ll = [], []
            for neighbor in poses[s]:
                # Express this contact in the decorated root's own frame.
                inv = transpose(root)
                relative_r = mul(inv, neighbor)
                relative = act(inv, t), relative_r
                legal = fitting((ZERO, root), (t, neighbor))
                assert legal == (relative in raw_contacts)
                rr.append(int(legal))
                ll.append(int(relative in surviving))
            raw_matrix.append(rr)
            live_matrix.append(ll)
        assert any(map(any, live_matrix))
        rows.append({"origin": t, "notch": s, "family": family,
                     "raw_pose_matrix": raw_matrix, "surviving_pose_matrix": live_matrix})
    # Ensure no contact outside the old families is hidden by the matrices.
    for c in raw_contacts:
        assert (c[0], act(c[1], ONE)) in families

    # Interpret the three poses using notch contacts, rather than arbitrary
    # key numbers. Each nonidentical notch direction picks one distinguished
    # world axis (the coordinate with the exceptional sign).
    identical_owner = next(x for x in rows if x["origin"] == ONE and x["notch"] == ONE)
    assert identical_owner["surviving_pose_matrix"] == [[int(i == j) for j in range(3)] for i in range(3)]
    routing = []
    for phase in range(3):
        options = [x for x in rows if x["origin"] == ONE and
                   any(x["surviving_pose_matrix"][phase])]
        directions = {x["notch"] for x in options}
        assert ONE in directions and len(directions) == 3
        axes = {next(i for i, v in enumerate(s) if s.count(v) == 1)
                for s in directions if s != ONE}
        assert len(axes) == 1
        routing.append({"root_pose": phase, "exceptional_sign_axis": "xyz"[axes.pop()],
                        "notch_owner_directions": sorted(directions)})
    groups = []
    for root in poses[ONE]:
        group = {}
        for child in data["children"]:
            cr = tuple(x for row in child["matrix"] for x in row)
            group[act(root, child["center"])] = mul(root, cr)
        groups.append(group)
    copying = [t for t in groups[0] if all(g[t] == r for g, r in zip(groups, poses[ONE]))]
    resetting = [t for t in groups[0] if len({g[t] for g in groups}) == 1]
    assert set(copying) == {ZERO, neg(ONE)} and len(resetting) == 6
    assert set(copying + resetting) == set(groups[0])

    # Look for a small coarse patch satisfying all pair-family constraints
    # but with incompatible required root phases. This is not a GS tiling.
    obstruction = None
    for a, b in combinations(rows, 2):
        pa = tuple(a["origin"]), poses[tuple(a["notch"])][0]
        pb = tuple(b["origin"]), poses[tuple(b["notch"])][0]
        if placed(*pa)[0] & placed(*pb)[0]:
            continue
        if shared(pa, pb):
            inv = transpose(pa[1])
            rel = act(inv, sub(pb[0], pa[0])), act(inv, tuple(b["notch"]))
            if rel not in families:
                continue
        allowed_a = {i for i, row in enumerate(a["surviving_pose_matrix"]) if any(row)}
        allowed_b = {i for i, row in enumerate(b["surviving_pose_matrix"]) if any(row)}
        if not allowed_a & allowed_b:
            obstruction = {"neighbors": [{k: x[k] for k in ("origin", "notch", "family")}
                                         for x in (a, b)],
                           "required_root_poses": [sorted(allowed_a), sorted(allowed_b)],
                           "scope": "Coarse three-chair patch only; not certified extendible in the old system."}
            break

    assert obstruction is not None
    face_counts = {}
    for family in ("i", "ii", "iii"):
        counts = Counter()
        for c in sorted(surviving):
            if families[c[0], act(c[1], ONE)] == family:
                names = Counter(first[0] for _, _, first, _ in shared(anchor, c))
                assert set(names) == set("ABC")
                counts[" ".join(f"{k}:{v}" for k, v in sorted(names.items()))] += 1
        face_counts[family] = dict(counts)
    report = {
        "status": "passed", "candidate_sha256": EXPECTED,
        "input_sha256": {name: entry[1] for name, entry in inputs.items()},
        "scope": "Grid pair relations and old axial arrow directions, not a full auxiliary-tile conjugacy.",
        "geometric_contacts_recomputed": len(geometric), "raw_contacts_recomputed": len(raw_contacts),
        "impossible_contacts_recomputed": len(removed), "surviving_contacts": len(surviving),
        "old_axial_arrow_tests": arrow_tests, "old_coarse_families": dict(Counter(families.values())),
        "old_coarse_contacts": len(families), "root_poses": poses[ONE],
        "neighbor_pose_convention": "Lexicographic order of proper matrices R with R(1,1,1)=notch.",
        "all_possible_pose_pairs": len(rows)*9,
        "raw_pose_pairs": sum(sum(map(sum, x["raw_pose_matrix"])) for x in rows),
        "surviving_pose_pairs": sum(sum(map(sum, x["surviving_pose_matrix"])) for x in rows),
        "surviving_lift_count_histogram": dict(sorted(Counter(sum(map(sum, x["surviving_pose_matrix"])) for x in rows).items())),
        "family_face_motif_counts_for_fixed_root": face_counts,
        "notch_owner_axis_routing": routing,
        "substitution_pose_copy_positions": sorted(copying),
        "substitution_pose_reset_positions": sorted(resetting),
        "coarse_patch_without_surviving_pose_lift": obstruction, "contacts": rows,
    }
    assert report["raw_pose_pairs"] == 132 and report["surviving_pose_pairs"] == 90
    (HERE / "goodman_strauss_comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = ["# Goodman-Strauss contact comparison: generated tables", "",
             "Generated by `uv run --locked python strong/audit/compare_goodman_strauss.py`.", "",
             "Each matrix has three rows (root poses) and three columns (neighbor poses).",
             "A 1 admits that pose pair. Matrices use lexicographically sorted proper rotations",
             "with the indicated missing-octant direction. Full conventions and input hashes are in",
             "[the JSON](goodman_strauss_comparison.json). See [the analysis](../review/GOODMAN_STRAUSS_COMPARISON.md).", "",
             "| Family | Origin | Notch direction | Raw matrix | Surviving matrix |",
             "|---|---|---|---|---|"]
    for x in rows:
        matrices = [" / ".join("".join(map(str, row)) for row in x[k])
                    for k in ("raw_pose_matrix", "surviving_pose_matrix")]
        lines.append(f"| {x['family']} | {tuple(x['origin'])} | {tuple(x['notch'])} | {' | '.join(matrices)} |")
    (HERE / "goodman_strauss_comparison_tables.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("contacts", "input_sha256")}, indent=2))


if __name__ == "__main__":
    main()

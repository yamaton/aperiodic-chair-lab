"""Independent raw-coordinate test of all 48 orientations, including mirrors.

No imports from the original geometry or audit implementation. Cube-adjacency
offsets give a complete contact enumeration. This checks finite lemmas; the
all-Euclidean-tilings implication is explained in FOLLOWUP_REFLECTIONS.md.
"""

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
IDENTITY = (1, 0, 0, 0, 1, 0, 0, 0, 1)
NORMALS = tuple(tuple(s if i == k else 0 for i in range(3)) for k, s in product(range(3), (-1, 1)))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(k, p):
    return tuple(k*x for x in p)


def act(r, p):
    return tuple(sum(r[3*i+j]*p[j] for j in range(3)) for i in range(3))


def det(r):
    a, b, c, d, e, f, g, h, i = r
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def cube_turn(r, q):
    center = act(r, tuple(2*x+1 for x in q))
    assert all(x % 2 for x in center)
    return tuple((x-1)//2 for x in center)


def all_orientations():
    return sorted(tuple(signs[i]*int(j == order[i]) for i in range(3) for j in range(3))
                  for order, signs in product(permutations(range(3)), product((-1, 1), repeat=3)))


def load_shape(data):
    cells = frozenset(map(tuple, data["coarse_cubes"]))
    faces = {(q, n): {} for q in cells for n in NORMALS if add(q, n) not in cells}
    ports = []
    for port in data["ports"]:
        p16 = tuple(16*Fraction(x) for x in port["center"])
        assert all(x.denominator == 1 for x in p16)
        p = tuple(map(int, p16))
        n, u, v = (tuple(port[k]) for k in ("outward_normal", "u_axis", "v_axis"))
        f = sub(p, add(scale(3, u), v))
        raw_owner = tuple(f[i]-8*n[i]-8 for i in range(3))
        assert all(x % 16 == 0 for x in raw_owner)
        owner = tuple(x//16 for x in raw_owner)
        assert (owner, n) in faces and p not in faces[owner, n]
        faces[owner, n][p] = (port["signed_key"], u, v)
        ports.append((p, n, u, v, port["signed_key"]))
    assert len(faces) == 24 and all(len(f) == 8 for f in faces.values())
    return cells, faces, ports


def turn(cells, faces, r):
    return (frozenset(cube_turn(r, q) for q in cells),
            {(cube_turn(r, q), act(r, n)): {act(r, p): (k, act(r, u), act(r, v))
               for p, (k, u, v) in features.items()} for (q, n), features in faces.items()})


def mismatches(first, second, shift):
    moved = {add(p, scale(16, shift)): (k, u, v) for p, (k, u, v) in second.items()}
    assert first.keys() == moved.keys()
    return [(p, first[p][0], moved[p][0]) for p in sorted(first)
            if first[p] != (-moved[p][0], moved[p][1], moved[p][2])]


def run():
    raw = (HERE / "frozen_v1/candidate.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((HERE / "frozen_v1/manifest.json").read_text())["candidate_sha256"]
    data = json.loads(raw)
    cells, faces, ports = load_shape(data)
    orientations = all_orientations()
    assert len(orientations) == 48 and Counter(map(det, orientations)) == {1: 24, -1: 24}
    geometric, legal, face_trials, face_matches = (Counter() for _ in range(4))
    allowed, witnesses, symmetries = [], [], []
    for ri, r in enumerate(orientations):
        parity = det(r)
        other_cells, other_faces = turn(cells, faces, r)
        if other_cells == cells and other_faces == faces:
            symmetries.append(r)
        for ai, ((a, n), af) in enumerate(sorted(faces.items())):
            for bi, ((b, m), bf) in enumerate(sorted(other_faces.items())):
                if m != neg(n):
                    continue
                shift = sub(add(a, n), b)
                failures = mismatches(af, bf, shift)
                face_trials[parity] += 1
                if not failures:
                    face_matches[parity] += 1
                elif parity == -1:
                    witnesses.append([ri, ai, bi, list(shift), *failures[0]])
        # Completeness: a face contact places some other cube directly
        # adjacent to an exposed cube face of the first chair.
        shifts = {sub(add(a, n), b) for a, n in faces for b in other_cells}
        for shift in sorted(shifts):
            moved_cells = {add(b, shift) for b in other_cells}
            if cells & moved_cells:
                continue
            shared = [(a, n) for a, n in faces if add(a, n) in moved_cells]
            if not shared:
                continue
            geometric[parity] += 1
            fits = all(not mismatches(faces[a, n], other_faces[sub(add(a, n), shift), neg(n)], shift)
                       for a, n in shared)
            if fits:
                legal[parity] += 1
                allowed.append((shift, r))
    assert symmetries == [IDENTITY]
    assert face_matches[-1] == legal[-1] == 0
    assert len(witnesses) == face_trials[-1]
    old = json.loads((HERE / "coordinate_certificate.json").read_text())
    assert old["candidate_sha256"] == digest
    assert set(allowed) == {(tuple(t), tuple(r)) for t, r in old["legal_contacts"]}

    key_chiralities = {}
    for _, n, u, v, key in ports:
        handedness = det(tuple(u)+tuple(v)+tuple(n))
        if key in key_chiralities:
            assert key_chiralities[key] == handedness
        key_chiralities[key] = handedness
    assert all(key_chiralities[-k] == -c for k, c in key_chiralities.items())
    frame_counts, frame_poses = Counter(), {1: set(), -1: set()}
    for pa, na, ua, va, ka in ports:
        for pb, nb, ub, vb, kb in ports:
            if ka != -kb:
                continue
            r = tuple(ua[i]*ub[j]+va[i]*vb[j]-na[i]*nb[j] for i in range(3) for j in range(3))
            assert r in orientations
            t16 = sub(pa, act(r, pb))
            assert all(x % 16 == 0 for x in t16)
            parity = det(r)
            frame_counts[parity] += 1
            frame_poses[parity].add((tuple(x//16 for x in t16), r))
    assert frame_counts[-1] == 0 and frame_counts[1] == 1536
    result = {"status": "passed", "candidate_sha256": digest,
              "implementation": "Raw rational ports, signed permutations, cube-center transforms, adjacency-generated offsets; no project helper imports",
              "orientations": 48, "geometric_contacts_by_determinant": dict(geometric),
              "legal_contacts_by_determinant": {s: legal[s] for s in (1, -1)},
              "face_trials_by_determinant": dict(face_trials),
              "matching_unit_faces_by_determinant": {s: face_matches[s] for s in (1, -1)},
              "improper_face_rejection_witnesses": len(witnesses),
              "full_keyed_solid_stabilizer": symmetries,
              "local_frame_chirality_by_signed_key": dict(sorted(key_chiralities.items())),
              "single_cap_frame_correspondences_by_determinant": {s: frame_counts[s] for s in (1, -1)},
              "distinct_single_cap_poses_by_determinant": {s: len(frame_poses[s]) for s in (1, -1)},
              "all_single_cap_translations_integral": True,
              "proper_legal_set_equals_original": True,
              "scope": "Finite contact and frame lemmas. A single opposite-key cap match already requires determinant +1. The written cap-rigidity and component-filling arguments are still needed to extend this to all Euclidean tilings."}
    certificate = {"candidate_sha256": digest, "orientations": orientations,
                   "witness_format": ["orientation_index", "first_face_index", "second_rotated_face_index", "translation", "port_position_times_16", "first_key", "second_key"],
                   "face_order": "lexicographic (owning cube lower corner, outward normal)",
                   "improper_face_rejections": witnesses, "legal_contacts": allowed}
    (HERE / "reflection_verification.json").write_text(json.dumps(result, indent=2)+"\n")
    (HERE / "reflection_certificate.json").write_text(json.dumps(certificate, separators=(",", ":"))+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()

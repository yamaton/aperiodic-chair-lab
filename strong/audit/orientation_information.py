"""Explain the frozen matching system and test forgetting its internal poses.

Uses the audited coordinate helpers. Unlike check_reflections.py this is
an analysis built on that implementation, not an independent verifier.
"""

from collections import Counter, defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path

import verify_from_coordinates as a


HERE = Path(__file__).resolve().parent
CYCLE = (0, 1, 0, 0, 0, 1, 1, 0, 0)
Z = (0, 0, 1)


def signed_quotient(solid):
    rotated = a.rotate_solid(solid, CYCLE)
    edges = defaultdict(set)
    for face, ports in solid.faces.items():
        for p, (key, _, _) in ports.items():
            other = rotated.faces[face][p][0]
            for sign in (-1, 1):
                edges[sign*key].add(sign*other)
                edges[sign*other].add(sign*key)
    mapping, components = {}, []
    for key in sorted(k for k in edges if k > 0):
        if key in mapping:
            continue
        component, queue = {key}, [key]
        for current in queue:
            for other in edges[current]:
                if other not in component:
                    component.add(other)
                    queue.append(other)
        assert not component & {-k for k in component}
        label = len(components)+1
        component = sorted(component, key=abs)
        components.append(component)
        for k in component:
            mapping[k], mapping[-k] = label, -label
    assert len(mapping) == 24
    return components, mapping


def canonical_profile(features, center16, normal, rotations):
    variants = []
    for r in rotations:
        if a.apply(r, normal) != Z:
            continue
        normalized = {a.apply(r, a.sub(p, center16)): (k, a.apply(r, u), a.apply(r, v))
                      for p, (k, u, v) in features.items()}
        word = tuple(normalized[p][0] for p in sorted(normalized))
        variants.append((word, r, normalized))
    word, r, normalized = min(variants, key=lambda x: x[0])
    assert sum(w == word for w, _, _ in variants) == 1
    return word, r, normalized


def motif_analysis(solid, macro, rotations):
    fine_profiles, big_profiles, macro_faces = {}, {}, {}
    for f, n in solid.faces:
        pieces = [ports for (g, m), ports in macro.faces.items()
                  if m == n and all(g[k] == 2*f[k] if n[k] else abs(g[k]-2*f[k]) == 1 for k in range(3))]
        assert len(pieces) == 4
        big = {p: value for ports in pieces for p, value in ports.items()}
        assert len(big) == 32
        macro_faces[f, n] = big
        fine_profiles[f, n] = canonical_profile(solid.faces[f, n], a.scale(8, f), n, rotations)
        big_profiles[f, n] = canonical_profile(big, a.scale(16, f), n, rotations)
    words = sorted({w for w, _, _ in fine_profiles.values()})
    big_words = sorted({w for w, _, _ in big_profiles.values()})
    assert len(words) == len(big_words) == 3
    ids = {w: "ABC"[i] for i, w in enumerate(words)}
    motifs = {ids[w]: next(P for word, _, P in fine_profiles.values() if word == w) for w in words}
    descriptors = []
    macro_correspondence = defaultdict(set)
    for (f, n), (word, r, normalized) in sorted(fine_profiles.items()):
        assert normalized == motifs[ids[word]]
        inverse = a.transpose(r)
        reconstructed = {a.add(a.apply(inverse, p), a.scale(8, f)):
                         (k, a.apply(inverse, u), a.apply(inverse, v))
                         for p, (k, u, v) in motifs[ids[word]].items()}
        assert reconstructed == solid.faces[f, n]
        big_word, big_r, _ = big_profiles[f, n]
        adjustment = a.multiply(big_r, inverse)
        macro_correspondence[ids[word]].add((big_words.index(big_word), adjustment))
        descriptors.append({"center_times_2": f, "normal": n, "motif": ids[word],
                            "arrow": a.apply(inverse, (1, 0, 0)), "canonical_to_tile": inverse})
    assert all(len(v) == 1 for v in macro_correspondence.values())
    rule_table = []
    for first, second in product(sorted(motifs), repeat=2):
        for r in rotations:
            if a.apply(r, Z) != a.scale(-1, Z):
                continue
            moved = {a.apply(r, p): (k, a.apply(r, u), a.apply(r, v))
                     for p, (k, u, v) in motifs[second].items()}
            if a.face_fit(motifs[first], moved, a.ZERO):
                rule_table.append({"first": first, "second": second, "second_to_first": r})
    # Compare whole macroface compatibility with its corresponding unit face,
    # for every pair and every aligned proper relative orientation.
    comparisons = 0
    for r in rotations:
        for (f, n), ports in solid.faces.items():
            for (g, m), other in solid.faces.items():
                if a.apply(r, m) != a.scale(-1, n):
                    continue
                delta = a.sub(f, a.apply(r, g))
                assert all(x % 2 == 0 for x in delta)
                shift = tuple(x//2 for x in delta)
                fine = {a.apply(r, p): (k, a.apply(r, u), a.apply(r, v)) for p, (k, u, v) in other.items()}
                big = {a.apply(r, p): (k, a.apply(r, u), a.apply(r, v)) for p, (k, u, v) in macro_faces[g, m].items()}
                assert a.face_fit(ports, fine, shift) == a.face_fit(macro_faces[f, n], big, a.scale(2, shift))
                comparisons += 1
    return {"motifs": {ids[w]: {"word": w, "occurrences": sum(v[0] == w for v in fine_profiles.values()),
                                "ports": [[p, *value] for p, value in sorted(motifs[ids[w]].items())]}
                       for w in words},
            "port_order": "lexicographic (u,v) at positions {(±1,±3),(±3,±1)}/16",
            "face_descriptors": descriptors, "matching_table": rule_table,
            "macroface_motif_correspondence": {k: sorted(v) for k, v in macro_correspondence.items()},
            "aligned_unit_vs_macroface_comparisons": comparisons,
            "aligned_unit_vs_macroface_disagreements": 0,
            "limit": "Aligned whole-face recurrence does not by itself exclude odd macro offsets; the earlier full macrocontact certificate handles those."}


def run():
    raw = (HERE / "frozen_v1/candidate.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((HERE / "frozen_v1/manifest.json").read_text())["candidate_sha256"]
    data = json.loads(raw)
    solid = a.from_data(data)
    rotations = a.rotation_group()
    children = [(tuple(c["center"]), tuple(x for row in c["matrix"] for x in row)) for c in data["children"]]
    catalogue, oriented = a.contact_catalogue(solid, rotations)
    macro = a.assemble(children, solid, oriented)
    original_macro, _ = a.contact_catalogue(macro, rotations)
    components, mapping = signed_quotient(solid)
    codes = {sign*k: (family, phase, sign) for family, keys in enumerate(components, 1)
             for phase, k in enumerate(keys) for sign in (-1, 1)}
    changed_faces, transitions = [], Counter()
    rotated = a.rotate_solid(solid, CYCLE)
    for (f, n), ports in sorted(solid.faces.items()):
        count = 0
        for p, (key, _, _) in ports.items():
            other = rotated.faces[f, n][p][0]
            family, phase, sign = codes[key]
            family2, phase2, sign2 = codes[other]
            assert (family, sign) == (family2, sign2)
            transitions[phase, phase2] += 1
            count += key != other
        if count:
            changed_faces.append({"center_times_2": f, "normal": n, "changed_ports": count})
    quotient_keys = [mapping[p["signed_key"]] for p in data["ports"]]
    quotient = a.from_data(data, quotient_keys)
    qcat, qorient = a.contact_catalogue(quotient, rotations)
    assert all(qcat[p][1] for p, (_, fits) in catalogue.items() if fits)
    quotient_symmetries = [r for r in rotations if a.rotate_solid(quotient, r).faces == quotient.faces]
    assert len(quotient_symmetries) == 3
    qmacro = a.assemble(children, quotient, qorient)
    qmacro_contacts, _ = a.contact_catalogue(qmacro, rotations)
    even = {p for p in qmacro_contacts if all(v % 2 == 0 for v in p[0])}
    qallowed = {p for p, (_, fits) in qmacro_contacts.items() if fits}
    assert qallowed == even
    # The repeated eight-chair group is a fundamental domain of 2*Lambda.
    residues = {(q[0] % 2, q[1] % 2, q[2] % 2,
                 (q[0]//2+2*(q[1]//2)+4*(q[2]//2)) % 7) for q in qmacro.cubes}
    assert len(residues) == 56
    periodic_contacts = [p for p in qmacro_contacts if p[1] == a.I
                         and all(v % 2 == 0 for v in p[0])
                         and (p[0][0]//2+2*(p[0][1]//2)+4*(p[0][2]//2)) % 7 == 0]
    assert periodic_contacts and all(qmacro_contacts[p][1] for p in periodic_contacts)
    failed_original = [p for p in periodic_contacts if not original_macro[p][1]]
    assert failed_original
    key_frames = defaultdict(set)
    for p, key in zip(data["ports"], quotient_keys):
        key_frames[key].add(a.determinant(tuple(p["u_axis"])+tuple(p["v_axis"])+tuple(p["outward_normal"])))
    assert all(len(v) == 1 for v in key_frames.values())
    assert all(key_frames[-k] == {-c for c in cs} for k, cs in key_frames.items())
    motif_result = motif_analysis(solid, macro, rotations)
    result = {"status": "passed", "candidate_sha256": digest,
              "implementation": "Analysis using the audited coordinate helpers; not an independent implementation",
              "signed_key_families": components, "signed_key_quotient": dict(sorted(mapping.items())),
              "phase_transition_counts_under_cycle": [[p, q, n] for (p, q), n in sorted(transitions.items())],
              "orientation_sensitive_faces": changed_faces,
              "orientation_sensitive_ports": sum(f["changed_ports"] for f in changed_faces),
              "orientation_invariant_ports": sum(transitions[p, p] for p in range(3)),
              "quotient_proper_self_symmetries": len(quotient_symmetries),
              "quotient_legal_contacts": sum(v[1] for v in qcat.values()),
              "quotient_legal_macrocontacts": len(qallowed),
              "quotient_deflated_rules": "all 1194 geometric proper contacts, no key restriction",
              "quotient_still_forces_handedness_at_each_cap": True,
              "periodic_quotient_witness": {"basis_columns": [[14, 0, 0], [-4, 2, 0], [-8, 0, 2]],
                  "placements": children, "quotient_port_keys": quotient_keys,
                  "fundamental_voxels": len(residues), "tiles_per_cell": 8,
                  "external_directed_macrocontacts_checked": len(periodic_contacts),
                  "external_contacts_rejected_by_original": len(failed_original),
                  "first_original_rejection": failed_original[0]},
              "ablation_scope": "A specific altered solid formed by identifying signed keys, including tab/pocket sign changes. Its periodicity does not imply periodicity of the frozen candidate or necessity of these exact keys for every possible construction."}
    (HERE / "orientation_information.json").write_text(json.dumps(result, indent=2)+"\n")
    (HERE / "face_motifs.json").write_text(json.dumps({"candidate_sha256": digest, **motif_result}, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("signed_key_quotient", "periodic_quotient_witness")}, indent=2))
    print(json.dumps({"motif_count": len(motif_result["motifs"]), "matching_table": motif_result["matching_table"],
                      "macroface_correspondence": motif_result["macroface_motif_correspondence"],
                      "macroface_comparisons": motif_result["aligned_unit_vs_macroface_comparisons"],
                      "periodic_external_contacts": len(periodic_contacts), "original_rejections": len(failed_original)}, indent=2))


if __name__ == "__main__":
    run()

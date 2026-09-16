"""Test how recut boundary rules behave when eight chairs are grouped."""

import json

from chair_recut import build_tables, contact_types, oriented_patch
from chair_recut_periods import verify_witness
from offset_dipoles import OUT


def run():
    synthesis = json.loads((OUT / "chair_recut_synthesis.json").read_text())
    types = contact_types()
    _, transitions, _ = build_tables(types)
    records = []
    basis = ((14, 0, 0), (-4, 2, 0), (-8, 0, 2))
    for i, profile in enumerate(synthesis["profiles"]):
        labels = profile["labels"]
        selected = [3 * j + q for j, q in enumerate(profile["template"])]
        allowed = {t for t, (_, _, pairs) in enumerate(types)
                   if all(labels[a] == -labels[b] for a, b in pairs)}
        induced = {t for t, matrix in enumerate(transitions)
                   if all(matrix[j][k] < 0 or matrix[j][k] in allowed
                          for j in selected for k in selected)}
        record = {"profile_index": i, "allowed_contacts": len(allowed),
                  "induced_parent_contacts": len(induced),
                  "rules_preserved_exactly": allowed == induced,
                  "induced_contact_type_ids": sorted(induced)}
        placements = oriented_patch(profile["template"], 1)
        try:
            witness = verify_witness(labels, basis, placements)
        except AssertionError:
            record["standard_inflated_lattice"] = "incompatible"
        else:
            record.update(standard_inflated_lattice="periodic counterexample",
                          basis_columns=basis, placements=placements, verification=witness)
        records.append(record)
        print(json.dumps({k: v for k, v in record.items()
                          if k not in ("placements", "induced_contact_type_ids")}), flush=True)
    result = {"status": "completed", "profiles": records,
              "limit": "Preservation of rules under substitution does not prove that every tiling decomposes into the substitution groups."}
    (OUT / "chair_recut_substitution.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    run()

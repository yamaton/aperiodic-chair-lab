"""Check every port in the phase-erased periodic tiling's finite quotient.

Uses raw cube/port parsing from the separate reflection checker, not the
contact or macro algorithms used to discover this periodic control.
"""

import hashlib
import json
from pathlib import Path

import check_reflections as r


HERE = Path(__file__).resolve().parent


def residue(q):
    return (q[0] % 2, q[1] % 2, q[2] % 2, (q[0]//2+2*(q[1]//2)+4*(q[2]//2)) % 7)


def evaluate(data, witness, keys):
    changed = {**data, "ports": [{**p, "signed_key": key} for p, key in zip(data["ports"], keys)]}
    cells, faces, _ = r.load_shape(changed)
    owners, placed_faces = {}, {}
    for tile, (translation, matrix) in enumerate(witness["placements"]):
        c, f = r.turn(cells, faces, tuple(matrix))
        for q in c:
            point = r.add(q, translation)
            assert point not in owners
            owners[point] = tile
        for (q, n), ports in f.items():
            key = r.add(q, translation), n
            assert key not in placed_faces
            placed_faces[key] = {r.add(p, r.scale(16, translation)): value for p, value in ports.items()}
    representatives = {residue(q): q for q in owners}
    assert len(representatives) == len(owners) == 56
    mismatched_faces, bad_ports, checked = 0, 0, 0
    for (q, n), ports in placed_faces.items():
        neighbor = r.add(q, n)
        representative = representatives[residue(neighbor)]
        shift = r.sub(neighbor, representative)
        assert residue(shift) == (0, 0, 0, 0)
        other = placed_faces[representative, r.neg(n)]
        failures = r.mismatches(ports, other, shift)
        checked += len(ports)
        bad_ports += len(failures)
        mismatched_faces += bool(failures)
    return {"fundamental_cubes": len(owners), "tiles": len(witness["placements"]),
            "unit_face_incidences": len(placed_faces), "port_incidences_checked": checked,
            "mismatched_unit_face_incidences": mismatched_faces, "mismatched_port_incidences": bad_ports}


def run():
    raw = (HERE / "frozen_v1/candidate.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    info = json.loads((HERE / "orientation_information.json").read_text())
    assert digest == info["candidate_sha256"]
    data = json.loads(raw)
    witness = info["periodic_quotient_witness"]
    control = evaluate(data, witness, witness["quotient_port_keys"])
    original = evaluate(data, witness, [p["signed_key"] for p in data["ports"]])
    assert control["mismatched_port_incidences"] == 0
    assert control["port_incidences_checked"] == 1536
    assert original["mismatched_port_incidences"] > 0
    result = {"status": "passed", "candidate_sha256": digest,
              "implementation": "Direct cube-residue quotient and port comparison using separate raw-coordinate reflection helpers",
              "basis_columns": witness["basis_columns"], "phase_erased_solid": control,
              "original_solid_on_same_placements": original,
              "scope": "An explicit periodic tiling of the altered signed-key quotient; not a periodic tiling of the frozen candidate."}
    (HERE / "periodic_ablation_verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()

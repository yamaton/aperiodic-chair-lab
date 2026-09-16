"""Test a concrete periodic tiling of the plain chair against the exact ports.

Uses frozen rational coordinates directly, without project geometry helpers.
This excludes one coarse periodic arrangement, not every possible period.
"""

from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
STATES = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
SHIFT = (-2, 1, 0)


def rotate(vector, state):
    return tuple(vector[i] for i in state)


def placed_ports(data, state, shift):
    return {
        (tuple(x+y for x, y in zip(rotate(tuple(map(Q, p["center"])), state), shift)),
         rotate(p["outward_normal"], state)):
        (p["signed_key"], rotate(p["u_axis"], state), rotate(p["v_axis"], state))
        for p in data["ports"]
    }


def run():
    raw = (HERE / "frozen_v1/candidate.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((HERE / "frozen_v1/manifest.json").read_text())["candidate_sha256"]
    data = json.loads(raw)
    cubes = {tuple(q) for q in data["coarse_cubes"]}
    residues = sorted((x+2*y+4*z) % 7 for x, y, z in cubes)
    assert residues == list(range(7))
    # The cubes represent every coset of this index-seven translation lattice.
    # Hence their translates partition all integer cells, not just a sample.
    assert (SHIFT[0]+2*SHIFT[1]+4*SHIFT[2]) % 7 == 0
    assert not cubes & {tuple(x+y for x, y in zip(q, SHIFT)) for q in cubes}
    assert all({rotate(q, s) for q in cubes} == cubes for s in STATES)
    rows, witness = [], None
    for first, second in product(range(3), repeat=2):
        a = placed_ports(data, STATES[first], (0, 0, 0))
        b = placed_ports(data, STATES[second], SHIFT)
        pairs = [(p, n, key_a, b[p, tuple(-x for x in n)])
                 for (p, n), key_a in a.items() if (p, tuple(-x for x in n)) in b]
        bad = [pair for pair in pairs if pair[2] != (-pair[3][0], pair[3][1], pair[3][2])]
        assert len(pairs) == 16 and len(bad) == 16
        rows.append({"first_pose": first, "second_pose": second,
                     "shared_ports": len(pairs), "mismatched_ports": len(bad)})
        if first == second == 0:
            p, n, ka, kb = bad[0]
            assert n == (-1, 0, 0) and ka[0] == -7 and kb[0] == 9 and ka[1:] == kb[1:]
            # At the common tangent center, phi(0,0)=1. The two boundary
            # x coordinates enclose a nonempty interval of interior overlap.
            depth = Q(data["height_unit"])
            left = p[0]+7*depth
            right = p[0]+9*depth
            overlap_point = ((left+right)/2, p[1], p[2])
            assert left < overlap_point[0] < right
            witness = {"base_port_center": list(map(str, p)), "keys": [ka[0], kb[0]],
                       "boundary_x_coordinates": [str(left), str(right)],
                       "point_in_both_tile_interiors": list(map(str, overlap_point))}
    result = {"status": "passed", "candidate_sha256": digest,
              "coarse_periodic_lattice": "x+2*y+4*z = 0 modulo 7",
              "lattice_basis_columns": [[7, 0, 0], [-2, 1, 0], [-4, 0, 1]],
              "coarse_cube_residues": residues, "tested_neighbor_shift": SHIFT,
              "all_nine_pose_pairs": rows, "physical_overlap_witness": witness,
              "scope": "Plain chairs tile periodically on this lattice. Its coarse arrangement cannot be decorated by the candidate, even with arbitrary choices among its three shape-preserving proper poses. This is not an exhaustive periodicity test."}
    (HERE / "periodic_chair_check.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()

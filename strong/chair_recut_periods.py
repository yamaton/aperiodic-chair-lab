"""Search periodic packings of the synthesized recut chairs.

Each quotient cell is a unit voxel, not a prescribed chair placement.
All integer chair centers and all 24 proper rotations are available.
Coarse exact coverage and equal signed boundary profiles enforce the fit.
"""

import argparse
from collections import Counter, defaultdict
from itertools import product
import json
import time

import z3

from chair_recut import PORTS, VOXELS, rotate
from offset_dipoles import OUT


def reducer(basis, scale=1):
    (a, _, _), (b, c, _), (d, e, f) = basis
    a, b, c, d, e, f = (scale * x for x in (a, b, c, d, e, f))

    def reduce(p):
        x, y, z = p
        q, z = divmod(z, f)
        x, y = x - q * d, y - q * e
        q, y = divmod(y, c)
        return ((x - q * b) % a, y, z)

    return reduce


def faces(labels, r):
    result = defaultdict(list)
    for (p, n), label in zip(PORTS, labels):
        p, n = rotate(p, r), rotate(n, r)
        axis = next(k for k in range(3) if n[k])
        # Face center in doubled coarse coordinates. Tangential coordinates
        # are odd multiples of 8; the port displacement has magnitude <= 3.
        center = tuple(p[k] // 8 if k == axis else (p[k] + 4) // 8
                       for k in range(3))
        offset = tuple(p[k] - 8 * center[k] for k in range(3))
        result[center].append((offset, n[axis] * label))
    assert len(result) == 24 and all(len(row) == 8 for row in result.values())
    return [(center, tuple(label for _, label in sorted(row)))
            for center, row in result.items()]


def verify_witness(labels, basis, placements):
    """Direct port-by-port check, independent of the face-token SAT model."""
    reduce = reducer(basis)
    reduce_port = reducer(basis, 16)
    counts = Counter()
    ports = defaultdict(list)
    for tile, (c, r) in enumerate(placements):
        for p in VOXELS:
            moved = rotate(p, r)
            counts[reduce(tuple(c[k] + (moved[k] - 1) // 2 for k in range(3)))] += 1
        for (p, n), label in zip(PORTS, labels):
            moved = rotate(p, r)
            point = reduce_port(tuple(16 * c[k] + moved[k] for k in range(3)))
            ports[point].append((rotate(n, r), label, tile))
    volume = basis[0][0] * basis[1][1] * basis[2][2]
    assert len(counts) == volume and set(counts.values()) == {1}
    for entries in ports.values():
        assert len(entries) == 2
        (a, la, _), (b, lb, _) = entries
        assert a == tuple(-x for x in b) and la == -lb
    assert sum(labels) == 0
    return {"coarse_voxels": volume, "matched_port_pairs": len(ports),
            "chair_count": len(placements), "signed_port_depth_sum": sum(labels)}


def solve(labels, basis, seconds=20):
    started = time.monotonic()
    cells = list(product(range(basis[0][0]), range(basis[1][1]), range(basis[2][2])))
    assert len(cells) % 7 == 0
    reduce, reduce_face = reducer(basis), reducer(basis, 2)
    orientations = [faces(labels, r) for r in range(24)]
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=int(seconds * 1000))
    cover = defaultdict(list)
    interface = defaultdict(dict)
    records = []
    for c in cells:
        for r in range(24):
            cubes = {reduce(tuple(c[k] + (rotate(p, r)[k] - 1) // 2 for k in range(3)))
                     for p in VOXELS}
            if len(cubes) != 7:
                continue  # The tile would overlap one of its own translates.
            required = {}
            for p, profile in orientations[r]:
                point = reduce_face(tuple(2 * c[k] + p[k] for k in range(3)))
                if point in required and required[point] != profile:
                    break  # Incompatible self-interface on this quotient.
                required[point] = profile
            else:
                variable = z3.Bool(f"chair{len(records)}")
                records.append((c, r, variable))
                for cube in cubes:
                    cover[cube].append(variable)
                for point, profile in required.items():
                    values = interface[point]
                    if profile not in values:
                        values[profile] = z3.Bool(f"face{point}profile{len(values)}")
                    solver.add(z3.Implies(variable, values[profile]))
    for c in cells:
        solver.add(z3.PbEq([(v, 1) for v in cover[c]], 1) if cover[c] else False)
    for values in interface.values():
        if len(values) > 1:
            solver.add(z3.PbLe([(v, 1) for v in values.values()], 1))
    built = time.monotonic()
    status = solver.check()
    result = {"status": str(status), "basis_columns": basis,
              "quotient_voxels": len(cells), "possible_placements": len(records),
              "build_seconds": built - started, "elapsed_seconds": time.monotonic() - started}
    if status == z3.sat:
        model = solver.model()
        placements = [(c, r) for c, r, v in records if z3.is_true(model.eval(v))]
        result.update(placements=placements,
                      verification=verify_witness(labels, basis, placements))
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def run(seconds):
    synthesis = json.loads((OUT / "chair_recut_synthesis.json").read_text())
    bases = [((14, 0, 0), (0, 2, 0), (0, 0, 2)),
             ((14, 0, 0), (0, 4, 0), (0, 0, 2)),
             ((14, 0, 0), (0, 4, 0), (0, 0, 4)),
             ((7, 0, 0), (0, 7, 0), (0, 0, 7))]
    records = []
    output = OUT / "chair_recut_periods.json"
    for i, profile in enumerate(synthesis["profiles"]):
        record = {"profile_index": i, "checks": [], "outcome": "unresolved"}
        records.append(record)
        for basis in bases:
            print(f"Profile {i}, lattice {basis}", flush=True)
            result = solve(profile["labels"], basis, seconds)
            record["checks"].append(result)
            print(f"  {result['status']} ({result['elapsed_seconds']:.2f}s)", flush=True)
            if result["status"] == "sat":
                record["outcome"] = "periodic"
            output.write_text(json.dumps({"profiles": records,
                "scope": "Periodic integer-grid packings with all 24 proper rotations; no orientation anchor on rectangular quotients.",
                "limit": "Failure on the tested quotients does not establish aperiodicity."}, indent=2) + "\n")
            if record["outcome"] == "periodic":
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=20)
    run(parser.parse_args().seconds)

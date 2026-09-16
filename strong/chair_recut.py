"""Exact contact-language synthesis for recut, oriented chair substitutions.

This is an exploratory geometric matching model, not a monotile theorem.
One chair has 24 boundary squares, each with eight small possible ports.
The substitution chooses one of three proper poses for each of eight children.
Closing the finite contact language makes the fit constraints independent of
the size of a sampled patch.
"""

from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile
import time

from chair_fusion import transforms
from offset_dipoles import OUT


ROTATIONS = tuple(transforms(True))


def rotate(p, r):
    axes, signs = ROTATIONS[r]
    return tuple(signs[k] * p[axes[k]] for k in range(3))


BASIS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ROTATION_LOOKUP = {tuple(rotate(p, r) for p in BASIS): r for r in range(24)}
IDENTITY = ROTATION_LOOKUP[BASIS]
MULTIPLY = tuple(tuple(ROTATION_LOOKUP[tuple(rotate(rotate(p, b), a) for p in BASIS)]
                       for b in range(24)) for a in range(24))
INVERSE = tuple(next(b for b in range(24) if MULTIPLY[a][b] == IDENTITY)
                for a in range(24))
VOXELS = frozenset(product((-1, 1), repeat=3)) - {(1, 1, 1)}
CHILDREN = (((0, 0, 0), (1, 1, 1)),) + tuple(
    (tuple(-x for x in r), r) for r in product((-1, 1), repeat=3)
    if r != (-1, -1, -1))
CHILD_ROTATIONS = tuple(tuple(r for r in range(24) if rotate((1, 1, 1), r) == s)
                        for _, s in CHILDREN)


def boundary_ports():
    result = []
    offsets = sorted({(a * x, b * y) for a, b in product((-1, 1), repeat=2)
                      for x, y in ((1, 3), (3, 1))})
    for voxel in sorted(VOXELS):
        for axis, sign in product(range(3), (-1, 1)):
            other = list(voxel)
            other[axis] += 2 * sign
            if tuple(other) in VOXELS:
                continue
            normal = tuple(sign if k == axis else 0 for k in range(3))
            center = tuple(8 * (voxel[k] + normal[k]) for k in range(3))
            tangents = [k for k in range(3) if k != axis]
            for offset in offsets:
                point = list(center)
                for k, value in zip(tangents, offset):
                    point[k] += value
                result.append((tuple(point), normal))
    assert len(result) == len(set(result)) == 192
    return tuple(result)


PORTS = boundary_ports()
PORT_LOOKUP = {port: i for i, port in enumerate(PORTS)}


def contact_types():
    """All nonoverlapping integer-center, proper-rotation face contacts."""
    result = []
    for shift in product(range(-2, 3), repeat=3):
        for r in range(24):
            other_voxels = {tuple(2 * shift[k] + rotate(p, r)[k] for k in range(3))
                            for p in VOXELS}
            if VOXELS.intersection(other_voxels):
                continue
            pairs = []
            for j, (p, n) in enumerate(PORTS):
                moved = rotate(p, r)
                point = tuple(16 * shift[k] + moved[k] for k in range(3))
                opposite = tuple(-x for x in rotate(n, r))
                i = PORT_LOOKUP.get((point, opposite))
                if i is not None:
                    pairs.append((i, j))
            if pairs:
                assert len(pairs) % 8 == 0
                result.append((shift, r, tuple(pairs)))
    return result


def relative_type(ca, ra, cb, rb, lookup):
    shift = rotate(tuple(cb[k] - ca[k] for k in range(3)), INVERSE[ra])
    r = MULTIPLY[INVERSE[ra]][rb]
    return lookup.get((shift, r), -1)


def build_tables(types):
    lookup = {(t, r): i for i, (t, r, _) in enumerate(types)}
    choices = [(j, q) for j in range(8) for q in range(3)]
    seeds = []
    for j, q in choices:
        row = []
        for k, u in choices:
            row.append(relative_type(CHILDREN[j][0], CHILD_ROTATIONS[j][q],
                                     CHILDREN[k][0], CHILD_ROTATIONS[k][u], lookup)
                       if j != k else -1)
        seeds.append(row)
    transitions = []
    for t, r, _ in types:
        other_centers = [tuple(2 * t[a] + rotate(c, r)[a] for a in range(3))
                         for c, _ in CHILDREN]
        other_rotations = [[MULTIPLY[r][rb] for rb in allowed]
                           for allowed in CHILD_ROTATIONS]
        transitions.append([
            [relative_type(CHILDREN[j][0], CHILD_ROTATIONS[j][q],
                           other_centers[k], other_rotations[k][u], lookup)
             for k, u in choices] for j, q in choices])
    symmetries = [[PORT_LOOKUP[(rotate(p, r), rotate(n, r))] for p, n in PORTS]
                  for r in CHILD_ROTATIONS[0]]
    return seeds, transitions, symmetries


def oriented_patch(template, level):
    patch = [((0, 0, 0), IDENTITY)]
    selected = [CHILD_ROTATIONS[j][q] for j, q in enumerate(template)]
    for _ in range(level):
        patch = [(tuple(2 * c[k] + rotate(p, r)[k] for k in range(3)),
                  MULTIPLY[r][selected[j]])
                 for c, r in patch for j, (p, _) in enumerate(CHILDREN)]
    return patch


def run():
    started = time.monotonic()
    types = contact_types()
    print(f"Exact geometry: {len(PORTS)} ports, {len(types)} directed contact types", flush=True)
    seeds, transitions, symmetries = build_tables(types)
    with tempfile.TemporaryDirectory(prefix="chair-recut-") as folder:
        folder = Path(folder)
        source = Path(__file__).with_name("chair_recut_screen.cpp")
        binary = folder / "screen"
        subprocess.run(["g++", "-O3", "-std=c++17", str(source), "-o", str(binary)], check=True)
        tables = folder / "tables.txt"
        with tables.open("w") as stream:
            stream.write(f"{len(PORTS)} {len(types)}\n")
            for _, _, pairs in types:
                stream.write(" ".join(map(str, [len(pairs), *(v for pair in pairs for v in pair)])) + "\n")
            for row in seeds:
                stream.write(" ".join(map(str, row)) + "\n")
            for matrix in transitions:
                for row in matrix:
                    stream.write(" ".join(map(str, row)) + "\n")
            for row in symmetries:
                stream.write(" ".join(map(str, row)) + "\n")
        output = folder / "result.json"
        subprocess.run([str(binary), str(tables), str(output)], check=True)
        result = json.loads(output.read_text())
    result.update(
        status="completed contact-language synthesis, not a monotile theorem",
        port_count=len(PORTS), contact_type_count=len(types),
        model="Eight fixed child poses in an oriented chair substitution; eight centered generic-orbit ports per unit boundary square; equal-width signed-depth ports.",
        limits=["Only stationary substitution pose templates are enumerated.",
                "A compatible boundary profile need not force the hierarchy in arbitrary tilings.",
                "The model assumes the coarse integer-grid chair placement is recognizable."],
        elapsed_seconds=time.monotonic() - started)
    OUT.mkdir(exist_ok=True)
    (OUT / "chair_recut_synthesis.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "profiles"}, indent=2), flush=True)


if __name__ == "__main__":
    run()

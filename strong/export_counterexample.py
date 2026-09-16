"""Export a rejected single-solid candidate and check its actual periodic packing."""

from collections import Counter
from itertools import product
import json
from pathlib import Path
import struct

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from search_ports import DIRECTIONS


OUT = Path(__file__).parent / "artifacts"


def solid_voxels(state):
    # Key type k uses depth k+1. Ports stay at least four units from edges.
    solid = set(product(range(32), repeat=3))
    for face, code in enumerate(state):
        depth = code // 12 + 1
        assert depth <= 3
        arrow = DIRECTIONS[(code % 12) // 2]
        normal_axis = face // 2
        arrow_axis = (code % 12) // 4
        across_axis = 3 - normal_axis - arrow_axis
        normal_sign = DIRECTIONS[face][normal_axis]
        for sex in (1, -1):
            start = 12 + 8 * arrow[arrow_axis] * sex
            for a, b, d in product(range(start, start+8), range(12, 20), range(depth)):
                plane = (32+d if normal_sign > 0 else -1-d) if sex == 1 else (31-d if normal_sign > 0 else d)
                p = [0, 0, 0]
                p[normal_axis], p[arrow_axis], p[across_axis] = plane, a, b
                if sex == 1:
                    solid.add(tuple(p))
                else:
                    solid.remove(tuple(p))
    assert len(solid) == 32**3
    return solid


def surface(solid):
    faces, normals = [], []
    # Unit quads give conforming edges for the STL topology check.
    for p in sorted(solid):
        for face, normal in enumerate(DIRECTIONS):
            q = tuple(p[k] + normal[k] for k in range(3))
            if q in solid:
                continue
            axis = face // 2
            u, v = [k for k in range(3) if k != axis]
            corners = []
            for a, b in ((0, 0), (1, 0), (1, 1), (0, 1)):
                point = list(p)
                point[axis] += int(normal[axis] > 0)
                point[u] += a
                point[v] += b
                corners.append(point)
            corners = np.array(corners)
            if np.dot(np.cross(corners[1]-corners[0], corners[2]-corners[0]), normal) < 0:
                corners = corners[::-1]
            faces.append(corners)
            normals.append(normal)
    return np.array(faces), np.array(normals)


def run():
    refined = json.loads((OUT / "dipole_refinement.json").read_text())
    case = next(c for c in refined if c["outcome"] == "periodic_12")
    certificate = case["checks"]["torus12"]
    grid = np.array(certificate["assignment"]).reshape((12,)*3)
    states = certificate["states"]
    translations = [(1, 1, 0), (2, -2, 0), (0, 0, 3)]
    for t in translations + [(4, 0, 0), (0, 4, 0)]:
        assert np.array_equal(np.roll(grid, t, axis=(0, 1, 2)), grid)
    determinant = abs(round(np.linalg.det(np.array(translations))))
    assert determinant == 12

    # Validate geometry in a rectangular 4x4x3 fundamental region, including wraps.
    shape = np.array([4, 4, 3]) * 32
    occupancy = np.zeros(tuple(shape), dtype=np.uint8)
    cache = {}
    for cell in product(range(4), range(4), range(3)):
        orientation = int(grid[cell])
        if orientation not in cache:
            cache[orientation] = np.array(sorted(solid_voxels(states[orientation])))
        points = (cache[orientation] + np.array(cell) * 32) % shape
        np.add.at(occupancy, tuple(points.T), 1)
    assert np.all(occupancy == 1)

    solid = solid_voxels(case["tile"])
    quads, normals = surface(solid)
    tris = np.concatenate([quads[:, [0, 1, 2]], quads[:, [0, 2, 3]]])
    tri_normals = np.concatenate([normals, normals])
    edges = Counter(tuple(sorted((tuple(t[i]), tuple(t[(i+1) % 3])))) for t in tris for i in range(3))
    assert set(edges.values()) == {2}
    volume = np.einsum("ij,ij->i", tris[:, 0], np.cross(tris[:, 1], tris[:, 2])).sum() / 6
    assert volume == 32**3
    with (OUT / "rejected-dipole-block.stl").open("wb") as f:
        f.write(b"REJECTED: admits translation (1,1,0); core side 32 mm".ljust(80, b" "))
        f.write(struct.pack("<I", len(tris)))
        for normal, tri in zip(tri_normals, tris):
            f.write(struct.pack("<12fH", *normal, *tri.flatten(), 0))

    fig = plt.figure(figsize=(12, 6), facecolor="#101c29")
    for position, azimuth in ((121, -50), (122, 130)):
        ax = fig.add_subplot(position, projection="3d")
        ax.set_facecolor("#101c29")
        ax.set_axis_off()
        ax.view_init(25, azimuth)
        ax.set_proj_type("ortho")
        ax.add_collection3d(Poly3DCollection(quads, facecolors="#e3aa78", linewidth=0,
                           shade=True, lightsource=matplotlib.colors.LightSource(315, 45)))
        ax.auto_scale_xyz(*quads.reshape((-1, 3)).T)
        ax.set_box_aspect([1, 1, 1])
    fig.suptitle("A genuine single solid — rejected by a periodic counterexample", color="#eff4fc", fontsize=17)
    fig.text(.5, .07, "Six faces carry offset tabs and pockets. A valid packing repeats along (1, 1, 0).",
             color="#c8d6e5", ha="center", fontsize=12)
    fig.text(.5, .025, "This model is NOT a strongly aperiodic monotile. Opposite views of the same block.",
             color="#e9b17f", ha="center", fontsize=11)
    fig.savefig(OUT / "rejected-dipole-block.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    result = {"status": "rejected: explicit periodic tiling", "tile": case["tile"],
              "proven_periods_in_block_units": translations,
              "translation_lattice_fundamental_cells": determinant,
              "voxel_coverage_region_blocks": [4, 4, 3], "coverage_voxels": int(occupancy.size),
              "holes": 0, "overlaps": 0, "stl_watertight": True,
              "block_volume_mm3": float(volume), "stl_triangles": len(tris),
              "certificate": {"size": [4, 4, 3], "states": states,
                              "assignment": grid[:4, :4, :3].tolist()}}
    (OUT / "geometric_counterexample.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "certificate"}, indent=2))


if __name__ == "__main__":
    run()

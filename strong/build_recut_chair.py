"""Export reviewable approximations of the exact polynomial-port candidate.

The mesh is a visualization, not the exact algebraic surface used by the
proposed grid-enforcement proof. No manufacturing-tolerance claim is made.
"""

from collections import Counter
from itertools import product
import json
import struct

import numpy as np

from chair_recut import PORTS, oriented_patch
from chair_recut_geometry import port_frame
from offset_dipoles import OUT


def mesh(labels, divisions=4):
    width = 1 / 64
    steps = np.linspace(-1, 1, divisions + 1)
    grid = sorted({-.5, .5, *(offset / 16 + width * s
                              for offset in (-3, -1, 1, 3) for s in steps)})
    quads, colors = [], []

    def add(points, normal, color):
        points = np.asarray(points)
        if np.dot(np.cross(points[1]-points[0], points[2]-points[0]), normal) < 0:
            points = points[::-1]
        quads.append(points)
        colors.append(color)

    for start in range(0, len(PORTS), 8):
        p, n = PORTS[start]
        center, _, _ = port_frame(p, n)
        center, normal = np.array(center) / 2, np.array(n)
        axes = [k for k in range(3) if not n[k]]
        centers = [np.array(PORTS[i][0]) / 16 for i in range(start, start+8)]
        for a, b in product(range(len(grid)-1), repeat=2):
            midpoint = center.copy()
            midpoint[axes] += [(grid[a]+grid[a+1])/2, (grid[b]+grid[b+1])/2]
            if any(all(abs(midpoint[k]-c[k]) < width for k in axes) for c in centers):
                continue
            points = []
            for x, y in ((grid[a], grid[b]), (grid[a+1], grid[b]),
                         (grid[a+1], grid[b+1]), (grid[a], grid[b+1])):
                q = center.copy()
                q[axes] += [x, y]
                points.append(q)
            add(points, normal, 0)
        for i in range(start, start+8):
            p, n = PORTS[i]
            _, eu, ev = port_frame(p, n)
            p, eu, ev, n = np.array(p)/16, np.array(eu), np.array(ev), np.array(n)

            def cap(u, v):
                phi = (1-u*u)*(1-v*v)*(1+u/5+v/7)
                return p + width*(u*eu+v*ev) + labels[i]/4096*phi*n

            for a, b in product(range(divisions), repeat=2):
                add([cap(steps[a], steps[b]), cap(steps[a+1], steps[b]),
                     cap(steps[a+1], steps[b+1]), cap(steps[a], steps[b+1])],
                    n, 1 if labels[i] > 0 else 2)
    vertices, ids, faces = [], {}, []
    for quad in quads:
        face = []
        for p in quad:
            key = tuple(round(float(x), 12) for x in p)
            if key not in ids:
                ids[key] = len(vertices)
                vertices.append(key)
            face.append(ids[key])
        faces.append(face)
    return np.array(vertices), faces, colors


def validate(vertices, faces):
    triangles = [tri for a, b, c, d in faces for tri in ((a, b, c), (a, c, d))]
    directed = Counter((a, b) for tri in triangles for a, b in zip(tri, (*tri[1:], tri[0])))
    assert all(count == 1 and directed[b, a] == 1 for (a, b), count in directed.items())
    assert len(vertices) - len(directed)//2 + len(triangles) == 2
    volume = sum(np.dot(vertices[a], np.cross(vertices[b], vertices[c])) for a, b, c in triangles) / 6
    assert abs(volume - 7) < 1e-9
    return triangles, {"vertices": len(vertices), "triangles": len(triangles),
                       "closed_oriented_manifold": True, "euler_characteristic": 2,
                       "volume": float(volume),
                       "limit": "This triangulation approximates the curved candidate; algebraic surface rigidity is not a property verified for this mesh."}


def run():
    profile = json.loads((OUT / "chair_recut_synthesis.json").read_text())["profiles"][1]
    vertices, faces, colors = mesh(profile["labels"])
    triangles, verification = validate(vertices, faces)
    with (OUT / "recut-chair-approximation.stl").open("wb") as stream:
        stream.write(b"Approximation only: see RECUT_CHAIR.md".ljust(80, b"\0"))
        stream.write(struct.pack("<I", len(triangles)))
        for a, b, c in triangles:
            points = vertices[[a, b, c]]
            normal = np.cross(points[1]-points[0], points[2]-points[0])
            normal /= np.linalg.norm(normal)
            stream.write(struct.pack("<12fH", *normal, *points.flatten(), 0))
    (OUT / "recut_chair_mesh_verification.json").write_text(json.dumps(verification, indent=2)+"\n")
    preview_vertices, preview_faces, preview_colors = mesh(profile["labels"], 2)
    from build_recut_visualization import run as build_visualization
    build_visualization()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from render_eight_chairs import mesh as coarse_mesh

    fig = plt.figure(figsize=(12, 6), facecolor="#101b29")
    ax = fig.add_subplot(121, projection="3d")
    ax.set_facecolor("#101b29")
    palette = ("#b4c4d5", "#4be0bd", "#edab79")
    ax.add_collection3d(Poly3DCollection(preview_vertices[preview_faces],
                          facecolors=[palette[c] for c in preview_colors], linewidths=0, antialiased=False,
                          shade=True, lightsource=matplotlib.colors.LightSource(300, 45)))
    ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), zlim=(-1.1, 1.1))
    ax.set_box_aspect((1, 1, 1)); ax.view_init(23, 38); ax.set_axis_off()
    ax.set_title("One chair, 192 curved ports", color="#edf4ff", fontsize=15)
    ax = fig.add_subplot(122, projection="3d")
    ax.set_facecolor("#101b29")
    from chair_recut import rotate
    chairs = [(c, rotate((1, 1, 1), r)) for c, r in oriented_patch(profile["template"], 1)]
    quads, group_colors = coarse_mesh(chairs)
    ax.add_collection3d(Poly3DCollection(quads, facecolors=group_colors, edgecolors="#172235",
                          linewidths=.4, shade=True, lightsource=matplotlib.colors.LightSource(300, 45)))
    ax.set(xlim=(-2.1, 2.1), ylim=(-2.1, 2.1), zlim=(-2.1, 2.1))
    ax.set_box_aspect((1, 1, 1)); ax.view_init(23, 38); ax.set_axis_off()
    ax.set_title("The forced group in the grid model", color="#edf4ff", fontsize=15)
    fig.suptitle("Recut chair: a proposed strongly aperiodic construction", color="#edf4ff", fontsize=18)
    fig.text(.5, .04, "Left: mesh approximation; teal = tabs, orange = pockets. Right: coarse geometry, eight congruent chairs.",
             ha="center", color="#b6c9dc", fontsize=10)
    fig.subplots_adjust(left=.01, right=.99, bottom=.09, top=.86, wspace=.01)
    fig.savefig(OUT / "recut-chair.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(json.dumps(verification, indent=2), flush=True)
    print(OUT / "recut-chair.html", flush=True)


if __name__ == "__main__":
    run()

"""Export the block and a self-contained, offline interactive explanation."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from geometry import Block, polygon_faces, patch, triangles


OUT = Path("artifacts")
COLORS = ["#64d6c1", "#73bdec", "#a49bea", "#ea9bbe", "#f2b78b", "#e4d481", "#a5d594"]


def export_stl(block):
    # 30 mm rhombus sides, with lowest vertex on z=0.
    vertices = (block.vertices + [0, 0, block.height]) * 30
    lines = ["solid scd_biprism"]
    for face in triangles(vertices):
        p, q, r = vertices[face]
        normal = np.cross(q-p, r-p)
        normal /= np.linalg.norm(normal)
        lines.append("  facet normal " + " ".join(f"{x:.12g}" for x in normal))
        lines.append("    outer loop")
        for vertex in (p, q, r):
            lines.append("      vertex " + " ".join(f"{x:.12g}" for x in vertex))
        lines.extend(["    endloop", "  endfacet"])
    lines.append("endsolid scd_biprism")
    (OUT / "block-30mm.stl").write_text("\n".join(lines) + "\n")
    faces = polygon_faces(block.vertices)
    obj = ["# SCD biprism; units mm; rhombus side 30 mm"]
    obj += ["v " + " ".join(f"{x:.12g}" for x in v) for v in vertices]
    obj += ["f " + " ".join(str(i+1) for i in face) for face in faces]
    (OUT / "block-30mm.obj").write_text("\n".join(obj) + "\n")
    (OUT / "block.scad").write_text(
        "// SCD biprism, one physical handedness. No clearance or connectors.\n"
        "side = 30; h = 2/5; lambda = 1/3;\n"
        "a = [1,0,0]; b = [1/3,2*sqrt(2)/3,0];\n"
        "c = lambda*b + [0,0,h]; d = lambda*a - [0,0,h];\n"
        "scale(side) translate([0,0,h])\n"
        "polyhedron(points=[[0,0,0],a,b,a+b,c,a+c,d,b+d],\n"
        "  faces=" + json.dumps([list(reversed(f)) for f in faces]) + ");\n")


def render(block):
    fig = plt.figure(figsize=(14, 7), facecolor="#101c29")
    title = "ONE BLOCK · NO TRANSLATIONAL REPEAT"
    fig.suptitle(title, color="#f0f5fb", fontsize=20, weight="bold", y=.95)
    axes = [fig.add_subplot(121, projection="3d"), fig.add_subplot(122, projection="3d")]
    faces = polygon_faces(block.vertices)
    for ax in axes:
        ax.set_facecolor("#101c29")
        ax.set_axis_off()
        ax.view_init(24, -62)
        ax.set_proj_type("ortho")
    for face in faces:
        axes[0].add_collection3d(Poly3DCollection([block.vertices[face]],
              facecolors="#64d6c1", edgecolors="#142d3c", linewidths=1.2,
              shade=True, lightsource=matplotlib.colors.LightSource(azdeg=315, altdeg=45)))
    axes[0].auto_scale_xyz(*block.vertices.T)
    axes[0].set_box_aspect(np.ptp(block.vertices, axis=0))
    axes[0].set_title("Convex biprism · 8 vertices · 8 faces", color="#c2d0df", pad=5)
    all_vertices = []
    for m, i, j, vertices in patch(block, range(5), radius=1):
        all_vertices.extend(vertices)
        axes[1].add_collection3d(Poly3DCollection([vertices[f] for f in faces],
              facecolors=COLORS[m], edgecolors="#1b3547", linewidths=.35,
              shade=True, lightsource=matplotlib.colors.LightSource(azdeg=315, altdeg=45)))
    all_vertices = np.array(all_vertices)
    axes[1].auto_scale_xyz(*all_vertices.T)
    axes[1].set_box_aspect(np.ptp(all_vertices, axis=0))
    axes[1].set_title("45 identical blocks · 5 interlocking layers", color="#c2d0df", pad=5)
    fig.text(.5, .09, "Each layer turns 70.528779…°; the infinite stack has no nonzero translation symmetry.",
             ha="center", color="#c2d0df", fontsize=12)
    fig.text(.5, .045, "Known SCD construction. Rotations and translations only. Screw symmetry remains possible.",
             ha="center", color="#94a6bb", fontsize=10)
    fig.subplots_adjust(left=.01, right=.99, top=.83, bottom=.13, wspace=.01)
    fig.savefig(OUT / "overview.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    block = Block()
    export_stl(block)
    render(block)
    data = {"vertices": block.vertices.tolist(), "faces": polygon_faces(block.vertices),
            "angle": float(block.angle), "height": block.height,
            "basis": block.basis.tolist(), "colors": COLORS}
    (OUT / "geometry.json").write_text(json.dumps(data, indent=2) + "\n")
    (OUT / "explorer.html").write_text(Path("viewer.html").read_text())
    print("Wrote STL, OBJ, OpenSCAD, PNG, geometry JSON and offline explorer to artifacts/.")


if __name__ == "__main__":
    main()

"""Visualize the twelve coarse groups surviving the occurrence screen."""

from itertools import product
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from offset_dipoles import OUT


COLORS = ("#70b4d3", "#e7b66c", "#ca879c", "#8dbe95",
          "#9f9cd0", "#e08f74", "#8dc9c2", "#c5c780")


def mesh(chairs):
    owner = {}
    for i, (c, s) in enumerate(chairs):
        for p in product((-1, 1), repeat=3):
            if p == (1, 1, 1):
                continue
            q = tuple(2 * c[k] + s[k] * p[k] for k in range(3))
            assert q not in owner
            owner[q] = i
    quads, colors = [], []
    for p, i in sorted(owner.items()):
        for axis, sign in product(range(3), (-1, 1)):
            q = list(p)
            q[axis] += 2 * sign
            if tuple(q) in owner:
                continue
            tangents = [k for k in range(3) if k != axis]
            corners = []
            for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                v = np.array(p, dtype=float) / 2
                v[axis] += sign / 2
                v[tangents] += np.array([a, b]) / 2
                corners.append(v)
            normal = np.eye(3)[axis] * sign
            if np.dot(np.cross(corners[1] - corners[0], corners[2] - corners[0]), normal) < 0:
                corners.reverse()
            quads.append(corners)
            colors.append(COLORS[i])
    return np.array(quads), colors


def run():
    report = json.loads((OUT / "chair_screen_8_level5.json").read_text())
    fig = plt.figure(figsize=(14, 11), facecolor="#101b29")
    for i, record in enumerate(report["shapes"]):
        ax = fig.add_subplot(3, 4, i + 1, projection="3d")
        ax.set_facecolor("#101b29")
        ax.set_axis_off()
        quads, colors = mesh(record["chairs"])
        ax.add_collection3d(Poly3DCollection(quads, facecolors=colors,
                           edgecolors="#172235", linewidths=.15, shade=True,
                           lightsource=matplotlib.colors.LightSource(300, 45)))
        ax.auto_scale_xyz(*quads.reshape((-1, 3)).T)
        extent = np.ptp(quads.reshape((-1, 3)), axis=0)
        ax.set_box_aspect(extent)
        ax.view_init(23, 38)
        ax.set_proj_type("ortho")
        valid = record["cover"]["status"] == "sat"
        label = "standard supertile; no new solution" if valid else "cannot cover the padded core"
        ax.set_title(f"{i + 1:02d}  {label}", color="#dfe8f5", fontsize=9, pad=0)
    fig.suptitle("Eight-chair groups: twelve local survivors", color="#edf4ff", fontsize=20, y=.98)
    fig.text(.5, .942, "2,288,650 connected placements screened. Colors identify the eight constituent chairs.",
             ha="center", color="#b6c9dc", fontsize=12)
    fig.text(.5, .03, "Coarse geometry only. These are not strongly aperiodic monotiles.",
             ha="center", color="#e6b379", fontsize=13)
    fig.subplots_adjust(left=.01, right=.99, bottom=.07, top=.91, wspace=.03, hspace=.06)
    fig.savefig(OUT / "eight-chair-groups.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(OUT / "eight-chair-groups.png")


if __name__ == "__main__":
    run()

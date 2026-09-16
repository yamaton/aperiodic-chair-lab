"""Draw the exact three-motif encoding and its three internal chair poses."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


HERE = Path(__file__).resolve().parent


def run():
    motifs = json.loads((HERE / "face_motifs.json").read_text())
    info = json.loads((HERE / "orientation_information.json").read_text())
    assert motifs["candidate_sha256"] == info["candidate_sha256"]
    active = {(tuple(f["center_times_2"]), tuple(f["normal"])) for f in info["orientation_sensitive_faces"]}
    bg, white, muted = "#0c1725", "#edf5fc", "#a8bacb"
    colors = {"A": "#e9b875", "B": "#ac9ddd", "C": "#63c7ad"}
    fig = plt.figure(figsize=(14, 9), facecolor=bg)
    for panel, (name, motif) in enumerate(motifs["motifs"].items(), 1):
        ax = fig.add_subplot(2, 3, panel)
        ax.set_facecolor(bg)
        for p, key, _, _ in motif["ports"]:
            ax.scatter(p[0], p[1], s=760, facecolor=colors[name], edgecolor=white, linewidth=.6)
            ax.text(p[0], p[1], f"{key:+d}", color=bg, ha="center", va="center", fontsize=12, fontweight="bold")
        ax.annotate("", xy=(2.6, -4.4), xytext=(-2.6, -4.4), arrowprops={"arrowstyle": "->", "color": white, "lw": 2})
        ax.text(0, -5.1, "Face arrow U", color=muted, ha="center", fontsize=10)
        ax.set(xlim=(-4.5, 4.5), ylim=(-5.6, 4.2), aspect="equal")
        ax.set_axis_off()
        rule = "A meets A: exchange U and V" if name == "A" else f"{name} meets {'C' if name == 'B' else 'B'}: reverse U"
        ax.set_title(f"Pattern {name} · 8 faces\n{rule}", color=white, fontsize=13, pad=14)
    cycle = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    for phase in range(3):
        rotation = np.linalg.matrix_power(cycle, phase)
        ax = fig.add_subplot(2, 3, phase+4, projection="3d")
        ax.set_facecolor(bg)
        quads, palette, arrows = [], [], []
        for f in motifs["face_descriptors"]:
            center = np.array(f["center_times_2"])/2
            n = np.array(f["normal"])
            u = np.array(f["arrow"])
            v = np.cross(n, u)
            quad = [rotation @ (center+s*u/2+t*v/2) for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            sensitive = (tuple(f["center_times_2"]), tuple(f["normal"])) in active
            quads.append(quad)
            palette.append(colors[f["motif"]] if sensitive else "#a9bbc8")
            if sensitive:
                arrows.append((rotation @ (center+.014*n-.21*u), rotation @ (.42*u)))
        ax.add_collection3d(Poly3DCollection(quads, facecolors=palette, edgecolors="#31485a", linewidths=.6,
                            shade=True, lightsource=matplotlib.colors.LightSource(315, 45)))
        for start, direction in arrows:
            ax.quiver(*start, *direction, color="#142537", linewidth=2, arrow_length_ratio=.3)
        ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), zlim=(-1.1, 1.1))
        ax.set_box_aspect((1, 1, 1)); ax.view_init(28, 42); ax.set_axis_off()
        ax.set_title(f"Internal pose {phase}", color=white, fontsize=15, pad=4)
    fig.suptitle("Three face patterns carry the chair's orientation information", color=white, fontsize=20, y=.98)
    fig.text(.5, .923, "Top: exact signed depth keys, viewed along the outward normal. Port pattern enlarged; U × V = outward normal.",
             color=muted, ha="center", fontsize=10)
    fig.text(.5, .055, "Bottom: same coarse chair in three poses. Only six faces change: three at the notch and three at the opposite corner.",
             color=muted, ha="center", fontsize=11)
    fig.text(.5, .027, "Colors and arrows summarize the physical port patterns; they are not additional assembly rules.",
             color=muted, ha="center", fontsize=10)
    fig.subplots_adjust(left=.04, right=.96, top=.85, bottom=.11, hspace=.1, wspace=.1)
    fig.savefig(HERE.parent / "artifacts/orientation-information.png", dpi=160, facecolor=bg)
    plt.close(fig)
    print("Wrote strong/artifacts/orientation-information.png")


if __name__ == "__main__":
    run()

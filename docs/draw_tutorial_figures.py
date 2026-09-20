"""Rebuild the tutorial's vector diagrams from the repository root.

Run with: uv run --locked python docs/draw_tutorial_figures.py
These are explanatory carrier/estimate diagrams, not curved-solid meshes.
"""

from itertools import product
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.patches import Circle, Polygon, Rectangle
import numpy as np


OUT = Path(__file__).resolve().parent / "figures"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "svg.fonttype": "none",
    "svg.hashsalt": "aperiodic-chair-tutorial-v1",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def parent_layers():
    # Table order in tutorial Section 4.1: Q, D---, D--+, ..., D++-.
    origins = [(0, 0, 0), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1),
               (-1, 1, 1), (1, -1, -1), (1, -1, 1), (1, 1, -1)]
    rotations = [lambda x, y, z: (x, y, z), lambda x, y, z: (x, y, z),
                 lambda x, y, z: (x, z, -y), lambda x, y, z: (z, -y, x),
                 lambda x, y, z: (y, -z, -x), lambda x, y, z: (-y, x, z),
                 lambda x, y, z: (-x, y, -z), lambda x, y, z: (-z, -x, y)]
    # Doubled cube centers avoid lower-corner rotation errors and floats.
    centers = [p for p in product((-1, 1), repeat=3) if p != (1, 1, 1)]
    owners = {}
    for label, (origin, rotate) in enumerate(zip(origins, rotations)):
        for center in centers:
            transformed = tuple(2 * t + c for t, c in zip(origin, rotate(*center)))
            cube = tuple((c - 1) // 2 for c in transformed)
            assert cube not in owners, (label, cube)
            owners[cube] = label
    expected = {p for p in product(range(-2, 2), repeat=3)
                if not all(c >= 0 for c in p)}
    assert set(owners) == expected and len(owners) == 56
    palette = ["#dbe9f3", "#f2d4b5", "#c6e3d2", "#edc5cf",
               "#d8d0ef", "#f2e2a5", "#b9e1e5", "#dedbd5"]
    fig, axes = plt.subplots(2, 2, figsize=(8, 8), layout="constrained")
    for z, ax in zip(range(-2, 2), axes.flat):
        for x, y in product(range(-2, 2), repeat=2):
            label = owners.get((x, y, z))
            ax.add_patch(Rectangle((x, y), 1, 1,
                facecolor=palette[label] if label is not None else "white",
                edgecolor="#657782", linewidth=0.8,
                hatch="//" if label is None else None))
            if label is not None:
                ax.text(x + 0.5, y + 0.5, str(label), ha="center", va="center",
                        fontsize=18, color="#172b3a", weight="bold")
        ax.set(xlim=(-2.15, 2.15), ylim=(-2.15, 2.15), aspect="equal",
               xticks=range(-2, 3), yticks=range(-2, 3), xlabel="x", ylabel="y",
               title=f"Layer {z} < z < {z + 1}")
        ax.spines[["left", "bottom"]].set_visible(False)
    fig.suptitle("Eight children fill one doubled carrier\n"
                 "0 = central child; 1–7 = table order; hatching = missing corner",
                 fontsize=14)
    save(fig, "tutorial-parent-layers.svg")


def square_cap_rigidity():
    fig = plt.figure(figsize=(10, 4.7), layout="constrained")
    ax = fig.add_subplot(121, projection="3d")
    u, v = np.meshgrid(np.linspace(-1, 1, 61), np.linspace(-1, 1, 61))
    phi = (1 - u * u) * (1 - v * v) * (1 + u / 5 + v / 7)
    ax.plot_surface(u, v, phi, cmap="viridis", linewidth=0, alpha=0.95)
    ax.set(xlabel="u", ylabel="v", zlabel="height / (kδ)",
           title="Physical cap: −1 ≤ u, v ≤ 1", zlim=(0, 1.2))
    ax.view_init(elev=25, azim=-60)
    ax = fig.add_subplot(122)
    ax.add_patch(Rectangle((-1, -1), 2, 2, facecolor="#d9edef", edgecolor="none"))
    for value in (-1, 1):
        ax.axvline(value, color="#217b83", linewidth=1.5)
        ax.axhline(value, color="#217b83", linewidth=1.5)
    line_u = np.linspace(-8, 4, 100)
    ax.plot(line_u, -7 - 7 * line_u / 5, color="#bd5c3b", linewidth=2)
    ax.annotate("1 + u/5 + v/7 = 0", xy=(-4, -1.4), xytext=(-7.4, 3),
                arrowprops={"arrowstyle": "->", "color": "#bd5c3b"}, fontsize=10)
    ax.text(0, 0, "cap\nsquare", ha="center", va="center", fontsize=9)
    ax.plot(0, 0, ".", color="#172b3a", markersize=3)
    ax.set(xlim=(-8, 4), ylim=(-8, 4), aspect="equal", xlabel="u", ylabel="v",
           title="Five lines on the continued graph (z = 0)")
    save(fig, "tutorial-cap-rigidity.svg")


def cap_rigidity():
    candidate = json.loads((OUT.parent.parent / "strong/audit/triangular_v1/candidate.json").read_text())
    vertices = candidate["port_profile"]["normalized_vertices"]
    assert vertices == [[-1, -1], [1, -1], [-1, 0]]
    fig = plt.figure(figsize=(11, 5), layout="constrained")
    ax = fig.add_subplot(121, projection="3d")
    n = 36
    xy = np.array([(i/n, j/n) for i in range(n+1) for j in range(n+1-i)])
    x, y = xy.T
    u, v = 2*x-1, y-1
    height = 27*x*y*(1-x-y)
    ax.plot_trisurf(mtri.Triangulation(u, v), height, cmap="viridis", linewidth=0, alpha=.95)
    ax.set(xlabel="u", ylabel="v", zlabel="height / (kδ)",
           title="Physical triangular cap (k > 0)", zlim=(0, 1.1))
    ax.set_box_aspect((1, .7, .65))
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, -.5, 0])
    ax.set_zticks([0, .5, 1])
    ax.view_init(elev=27, azim=-63)
    ax = fig.add_subplot(122)
    ax.add_patch(Polygon(vertices, facecolor="#d9edef", edgecolor="none"))
    ax.axvline(-1, color="#217b83", linestyle="--", linewidth=1)
    ax.axhline(-1, color="#217b83", linestyle="--", linewidth=1)
    line_u = np.linspace(-1.7, 1.65, 100)
    ax.plot(line_u, -(line_u+1)/2, color="#217b83", linestyle="--", linewidth=1)
    ax.plot([-1, 1, -1, -1], [-1, -1, 0, -1], color="#217b83", linewidth=2.5)
    ax.text(-1.13, -1.15, "A", ha="right")
    ax.text(1.1, -1.15, "B")
    ax.text(-1.1, .08, "C", ha="right")
    ax.text(0, -1.23, "long leg 2w", ha="center", va="top")
    ax.text(-1.13, -.5, "w", ha="right", va="center")
    ax.text(.24, -.5, "√5w", rotation=-27)
    ax.scatter([0], [0], color="#bd5c3b", marker="x", s=50, label="anchor p: (0, 0)")
    ax.scatter([-1/3], [-2/3], color="#172b3a", s=30, label="centroid: (−1/3, −2/3)")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.16), frameon=False, fontsize=10)
    ax.set(xlim=(-1.65, 1.65), ylim=(-1.55, .65), aspect="equal", xlabel="u", ylabel="v",
           title="Three lines recover the unequal sides")
    save(fig, "tutorial-triangular-cap-rigidity.svg")


def interior_bounds():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), layout="constrained")
    ax = axes[0]
    rho = 0.14  # Exaggerated for visibility; diagram labels state this.
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="#eff3f5", edgecolor="#172b3a"))
    ax.add_patch(Rectangle((rho, rho), 1 - 2 * rho, 1 - 2 * rho,
                          facecolor="#c6e3d2", edgecolor="#217b83"))
    c, y = (0.02, 0.04), (rho, rho)
    ax.plot(*c, "o", color="#bd5c3b")
    ax.plot(*y, "o", color="#217b83")
    ax.annotate("c", c, xytext=(-12, -15), textcoords="offset points")
    ax.annotate("y", y, xytext=(7, 3), textcoords="offset points")
    ax.annotate("", xy=y, xytext=c, arrowprops={"arrowstyle": "->"})
    ax.text(0.5, 0.55, "retained interior\nof the cube's owner B", ha="center")
    ax.annotate("", xy=(rho, 0.9), xytext=(0, 0.9),
                arrowprops={"arrowstyle": "<->", "color": "#172b3a"})
    ax.text(rho / 2, 0.94, "ρ", ha="center")
    ax.set(xlim=(-0.12, 1.12), ylim=(-0.12, 1.12), aspect="equal",
           title="Clamp into retained material\nInset ρ exaggerated; actual ρ = 1/64")
    ax.axis("off")
    ax = axes[1]
    # At z=-2, the section of 4L is the full square: its missing positive
    # octant starts at z=0. Highlight the negative cube's central section.
    for x, y in product((-4, 0), repeat=2):
        ax.add_patch(Rectangle((x, y), 4, 4, facecolor="#dbe9f3",
                              edgecolor="#172b3a"))
    ax.add_patch(Rectangle((-4, -4), 4, 4, facecolor="#c6e3d2", edgecolor="#217b83"))
    ax.add_patch(Circle((-2, -2), 1.9, facecolor="#eef6f7", edgecolor="#217b83"))
    ax.plot(-2, -2, ".", color="#172b3a")
    ax.annotate("", xy=(-0.1, -2), xytext=(-2, -2), arrowprops={"arrowstyle": "->"})
    ax.text(-2, -2.5, "radius 2 − h", ha="center", fontsize=10)
    ax.text(2, 2, "also present\nat z = −2", ha="center", va="center", fontsize=10)
    ax.set(xlim=(-4.5, 4.5), ylim=(-4.5, 4.5), aspect="equal",
           xticks=(-4, 0, 4), yticks=(-4, 0, 4), xlabel="x", ylabel="y",
           title="Growing interior: level m = 2\nSection z = −2; boundary reach exaggerated")
    save(fig, "tutorial-interior-bounds.svg")


def handshakes():
    fig, axes = plt.subplots(1, 3, figsize=(10, 4), layout="constrained")
    for ax, second, title in zip(axes, [(0, 1), (0, -1), (-1, 0)],
                                 ["A / A: allowed", "A / A: forbidden", "B / C: allowed"]):
        ax.add_patch(Rectangle((-1.1, -1.1), 2.2, 2.2,
                              facecolor="#f1f6f7", edgecolor="#657782"))
        ax.annotate("", xy=(0.9, 0), xytext=(0, 0),
                    arrowprops={"arrowstyle": "->", "lw": 3, "color": "#176b91"})
        ax.annotate("", xy=np.array(second) * 0.9, xytext=(0, 0),
                    arrowprops={"arrowstyle": "->", "lw": 3, "color": "#bd5c3b"})
        ax.text(0.55, 0.12, "U₁ = +x", color="#176b91", fontsize=10)
        if second == (0, 1):
            ax.text(0.1, 0.7, "U₂ = +y", color="#bd5c3b", fontsize=10)
        elif second == (0, -1):
            ax.text(0.1, -0.8, "U₂ = −y", color="#bd5c3b", fontsize=10)
        else:
            ax.text(-1, 0.12, "U₂ = −x", color="#bd5c3b", fontsize=10)
        ax.plot(0, 0, "o", color="#172b3a", markersize=4)
        ax.set(xlim=(-1.2, 1.2), ylim=(-1.55, 1.3), aspect="equal", title=title)
        ax.text(0, -1.4, "n₁ = +z (out), n₂ = −z (in)", ha="center", fontsize=9)
        ax.axis("off")
    fig.suptitle("Opposing panels, viewed in one common x–y frame", fontsize=14)
    save(fig, "tutorial-handshakes.svg")


def parent_flow():
    fig, ax = plt.subplots(figsize=(9, 6), layout="constrained")
    ax.set(xlim=(0, 10), ylim=(0, 8))
    ax.axis("off")

    def box(x, y, text, color="#eef6f7"):
        ax.text(x, y, text, ha="center", va="center", fontsize=11,
                bbox={"boxstyle": "round,pad=0.6", "fc": color, "ec": "#217b83"})

    def arrow(start, end, label="", offset=(0, 0)):
        ax.annotate("", xy=end, xytext=start,
                    arrowprops={"arrowstyle": "->", "color": "#46545d", "lw": 1.5})
        middle = (np.array(start) + end) / 2 + offset
        if label:
            ax.text(*middle, label, ha="center", va="center", fontsize=10,
                    bbox={"fc": "white", "ec": "none", "pad": 2})

    box(5, 7.2, "Inspect a chair Q in its own frame")
    box(5, 5.8, "One of the six oriented triggers present?")
    arrow((5, 6.8), (5, 6.2))
    box(1.8, 4.3, "Yes: Q is a center\nparent(Q) = Q", "#c6e3d2")
    box(7.5, 4.3, "No: inspect notch owner P")
    arrow((3.5, 5.4), (1.8, 4.9), "yes")
    arrow((6.5, 5.4), (7.5, 4.7), "no")
    box(5.5, 2.7, "Different orientation:\nQ is a trigger for P")
    box(8.6, 1.25, "Same orientation:\nforced neighbor S\nis a trigger for P")
    arrow((6.8, 3.9), (5.5, 3.2))
    arrow((8.7, 3.9), (8.6, 1.95))
    box(4.5, 0.7, "P is a center; parent(Q) = P", "#c6e3d2")
    arrow((5.5, 2.2), (4.5, 1.1))
    arrow((7.35, 0.95), (6.1, 0.75))
    save(fig, "tutorial-parent-flow.svg")


def parity_descent():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), layout="constrained",
                             gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axes[0]
    for y, start, title in [(2.4, 0, "Pairs start at even integers"),
                             (0.8, 1, "Shift by 1: starts land inside old pairs")]:
        for x in range(8):
            ax.add_patch(Rectangle((x, y), 1, 0.65, facecolor="#f4f6f8",
                                  edgecolor="#d0d8dd"))
        for x in range(start, 7, 2):
            ax.add_patch(Rectangle((x, y), 2, 0.65, facecolor="none",
                                  edgecolor="#217b83" if start == 0 else "#bd5c3b", lw=2))
        ax.text(0, y + 0.87, title, fontsize=10)
    for x in range(9):
        ax.text(x, 2.15, str(x), ha="center", fontsize=10)
        if x % 2 == 0:
            ax.plot([x, x], [0.6, 3.1], ":", color="#8b9ca6", zorder=0)
    ax.set(xlim=(-0.2, 8.2), ylim=(0, 4), title="Parity: a one-dimensional analogy")
    ax.axis("off")
    ax = axes[1]
    for y, label, color in [(3.25, "v = (12, 4, 0)", "#dbe9f3"),
                             (1.9, "v/2 = (6, 2, 0)", "#dbe9f3"),
                             (0.55, "v/4 = (3, 1, 0)\nOdd coordinates: contradiction", "#f3d9d1")]:
        ax.text(0.5, y, label, ha="center", va="center", fontsize=12,
                bbox={"boxstyle": "round,pad=0.6", "fc": color, "ec": "#657782"})
    for y in (2.8, 1.45):
        ax.annotate("", xy=(0.5, y - 0.5), xytext=(0.5, y), arrowprops={"arrowstyle": "->"})
        ax.text(0.56, y - 0.25, "deflate", fontsize=10, va="center")
    ax.set(xlim=(0, 1), ylim=(0, 4), title="Each new legal tiling repeats the test")
    ax.axis("off")
    save(fig, "tutorial-parity-descent.svg")


def seam_cost():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.7), layout="constrained")
    ax = axes[0]
    for x, y in product((0, 16), repeat=2):
        ax.add_patch(Rectangle((x, y), 16, 16, facecolor="#f2d4b5", edgecolor="#bd5c3b", lw=1.5))
        ax.add_patch(Rectangle((x + 2, y + 2), 12, 12, facecolor="#c6e3d2", edgecolor="none"))
        ax.text(x + 8, y + 8, "copied\nlegal interior", ha="center", va="center", fontsize=10)
    ax.set(xlim=(-1, 33), ylim=(-1, 33), aspect="equal", xticks=[0, 16, 32],
           yticks=[0, 16, 32], xlabel="x (lattice units)", ylabel="y (lattice units)",
           title="Repeated state windows: L = 16, r = 2\nOnly orange seam layers can acquire violations")
    ax = axes[1]
    sizes = np.linspace(4, 64, 200)
    ax.plot(sizes, 1 - (1 - 2 / sizes) ** 3, color="#217b83", lw=2,
            label="3D boundary-layer fraction")
    ax.plot(sizes, 6 / sizes, "--", color="#bd5c3b", lw=2, label="Upper bound 6r/L")
    ax.set(xlabel="L/r", ylabel="Fraction / bound", ylim=(0, 1.6), xlim=(4, 64),
           title="Fixed interaction range, growing repeat cell")
    ax.legend(fontsize=9)
    save(fig, "tutorial-seam-cost.svg")


def interference():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
    ax = axes[0]
    angle = 2 * np.pi / 3
    second = np.array([np.cos(angle), np.sin(angle)])
    total = second + [1, 0]
    for end, color, label in [([1, 0], "#176b91", "wave 1"),
                               (second, "#bd5c3b", "wave 2"),
                               (total, "#217b83", "sum")]:
        ax.annotate("", xy=end, xytext=(0, 0), arrowprops={"arrowstyle": "->", "lw": 2.5, "color": color})
        ax.text(end[0], end[1] + 0.12, label, ha="center", fontsize=10, color=color)
    ax.plot([1, total[0]], [0, total[1]], ":", color="#8b9ca6")
    ax.plot([second[0], total[0]], [second[1], total[1]], ":", color="#8b9ca6")
    ax.axhline(0, color="#d0d8dd", lw=1)
    ax.axvline(0, color="#d0d8dd", lw=1)
    ax.set(xlim=(-1.2, 1.4), ylim=(-0.3, 1.35), aspect="equal", xlabel="Real part",
           ylabel="Imaginary part", title="Add complex amplitudes\nExample phase difference: 2π/3")
    ax = axes[1]
    phase = np.linspace(0, 2 * np.pi, 200)
    ax.plot(phase, 1 + np.cos(phase), color="#217b83", lw=2)
    ax.scatter([0, np.pi / 2, np.pi, 2 * np.pi], [2, 1, 0, 2], color="#bd5c3b", zorder=3)
    ax.scatter([angle], [0.5], color="#176b91", marker="D", zorder=4)
    ax.annotate("Left example: S = 1/2", xy=(angle, 0.5), xytext=(0.45, 0.9),
                arrowprops={"arrowstyle": "->", "color": "#176b91"},
                fontsize=9, color="#176b91")
    ax.set(xlim=(-0.1, 2 * np.pi + 0.1), ylim=(-0.1, 2.3),
           xticks=[0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
           xticklabels=["0", "π/2", "π", "3π/2", "2π"],
           xlabel="Phase difference θ = q · d", ylabel="S = 1 + cos θ",
           title="Square the magnitude; divide by N = 2")
    ax.text(np.pi, 0.2, "cancellation", ha="center", fontsize=10)
    save(fig, "tutorial-interference.svg")


if __name__ == "__main__":
    parent_layers()
    square_cap_rigidity()
    cap_rigidity()
    interior_bounds()
    handshakes()
    parent_flow()
    parity_descent()
    seam_cost()
    interference()
    print("Wrote nine tutorial SVG diagrams, including the preserved square comparison; the 56-cube partition was checked.")

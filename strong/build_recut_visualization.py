"""Offline visualization of the frozen solid, assemblies, and a failed contact."""

from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OUT = HERE / "artifacts"


def apply(matrix, point):
    return tuple(sum(a*b for a, b in zip(row, point)) for row in matrix)


def data_from_frozen():
    raw = (HERE / "audit/frozen_v1/candidate.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((HERE / "audit/frozen_v1/manifest.json").read_text())["candidate_sha256"]
    source = json.loads(raw)
    cubes = set(map(tuple, source["coarse_cubes"]))
    faces = []
    for cube in sorted(cubes):
        for axis, sign in product(range(3), (-1, 1)):
            normal = tuple(sign if k == axis else 0 for k in range(3))
            if tuple(a+b for a, b in zip(cube, normal)) in cubes:
                continue
            center = tuple(Fraction(2*cube[k]+1+normal[k], 2) for k in range(3))
            ports = []
            for p in source["ports"]:
                point = tuple(map(Fraction, p["center"]))
                if tuple(p["outward_normal"]) == normal and all(
                        point[k] == center[k] if k == axis else abs(point[k]-center[k]) < Fraction(1, 2)
                        for k in range(3)):
                    ports.append({"center": list(map(float, point)), "key": p["signed_key"],
                                  "u": p["u_axis"], "v": p["v_axis"]})
            assert len(ports) == 8
            faces.append({"center": list(map(float, center)), "normal": normal,
                          "axes": [k for k in range(3) if k != axis], "ports": ports})
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    origin = {"center": [0, 0, 0], "matrix": identity}
    children = source["children"]
    patch = [origin]
    for _ in range(2):
        patch = [{"center": [2*a+b for a, b in zip(parent["center"], apply(parent["matrix"], child["center"]))],
                  "matrix": (np.array(parent["matrix"]) @ np.array(child["matrix"])).tolist()}
                 for parent in patch for child in children]
    target = (Fraction(-1), Fraction(5, 16), Fraction(-9, 16))
    valid = []
    for child in children[1:]:
        for port in source["ports"]:
            point = tuple(a+b for a, b in zip(child["center"], apply(child["matrix"], tuple(map(Fraction, port["center"])))))
            if point == target and apply(child["matrix"], port["outward_normal"]) == (1, 0, 0):
                assert port["signed_key"] == 7
                valid.append(child)
    assert len(valid) == 1
    return {"schema": 2, "candidate_sha256": digest, "faces": faces,
            "width": float(Fraction(source["half_width"])), "depth": float(Fraction(source["height_unit"])),
            "placements": {"one": [origin], "eight": children, "many": patch,
                           "valid": [origin, valid[0]],
                           "periodic": [origin, {"center": [-2, 1, 0], "matrix": identity}]},
            "contact_center": list(map(float, target)), "contact_u": [0, -1, 0], "contact_v": [0, 0, -1]}


def face_mesh(face, width, depth, divisions=4):
    """Disjoint flat strips around square holes, plus polynomial cap quads."""
    center, axes = np.array(face["center"]), face["axes"]
    offsets = [np.array(p["center"])-center for p in face["ports"]]
    xs, ys = [sorted({-.5, .5, *(float(p[k])+s*width for p in offsets for s in (-1, 1))}) for k in axes]
    result = []

    def flat(x0, x1, y0, y1):
        points = []
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            q = center.copy()
            q[axes] += (x, y)
            points.append(q)
        result.append((points, 0))

    for y0, y1 in zip(ys, ys[1:]):
        start = None
        for x0, x1 in zip(xs, xs[1:]):
            hole = any(abs((x0+x1)/2-p[axes[0]]) < width and abs((y0+y1)/2-p[axes[1]]) < width for p in offsets)
            if not hole and start is None:
                start = x0
            if hole and start is not None:
                flat(start, x0, y0, y1)
                start = None
        if start is not None:
            flat(start, xs[-1], y0, y1)
    steps = np.linspace(-1, 1, divisions+1)
    for port in face["ports"]:
        def cap(u, v):
            phi = (1-u*u)*(1-v*v)*(1+u/5+v/7)
            return (np.array(port["center"])+width*(u*np.array(port["u"])+v*np.array(port["v"]))
                    + port["key"]*depth*phi*np.array(face["normal"]))
        for i, j in product(range(divisions), repeat=2):
            result.append(([cap(steps[i], steps[j]), cap(steps[i+1], steps[j]),
                            cap(steps[i+1], steps[j+1]), cap(steps[i], steps[j+1])], 1 if port["key"] > 0 else 2))
    for points, _ in result:
        if np.dot(np.cross(points[1]-points[0], points[2]-points[0]), face["normal"]) < 0:
            points.reverse()
    return result


def figure(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    background, text, muted = "#0c1725", "#edf5fc", "#a8bacb"
    colors = ["#a8c5da", "#e9b875", "#a698da", "#80b89a", "#dc9fa4", "#7fbbbd", "#b9c580", "#c29c7e"]
    fig = plt.figure(figsize=(14, 10), facecolor=background)
    for panel, (name, gap, title) in enumerate((("one", 0, "One modified solid"), ("eight", .28, "Eight congruent copies · separated")), 1):
        ax = fig.add_subplot(2, 2, panel, projection="3d")
        ax.set_facecolor(background)
        for i, placement in enumerate(data["placements"][name]):
            rotation = np.array(placement["matrix"])
            shift = np.array(placement["center"])*(1+gap)
            quads, palette = [], []
            for face in data["faces"]:
                for points, kind in face_mesh(face, data["width"]*3, data["depth"]*12):
                    quads.append(np.array(points) @ rotation.T + shift)
                    palette.append((colors[i % len(colors)], "#4ddfbd", "#ef986e")[kind])
            ax.add_collection3d(Poly3DCollection(quads, facecolors=palette, linewidths=0,
                                                antialiased=False, zsort="average", shade=True,
                                                lightsource=matplotlib.colors.LightSource(315, 45)))
        limit = 1.25 if name == "one" else 2.5
        ax.set(xlim=(-limit, limit), ylim=(-limit, limit), zlim=(-limit, limit))
        ax.set_box_aspect((1, 1, 1)); ax.view_init(25, 42); ax.set_axis_off()
        ax.set_title(title, color=text, fontsize=16, pad=3)
    u = np.linspace(-1, 1, 301)
    phi = (1-u*u)*(1+u/5)
    for panel, (key, title) in enumerate(((7, "Valid contact: matching tab and pocket"), (9, "Periodic attempt: tab is too deep")), 3):
        ax = fig.add_subplot(2, 2, panel)
        ax.set_facecolor("#142438")
        pocket, tab = 7*phi, key*phi
        ax.fill_between(u, pocket, 12, color="#84b9db", alpha=.35)
        ax.fill_between(u, -2, tab, color="#e9b875", alpha=.38)
        ax.plot(u, pocket, color="#97ceef", linewidth=2.5, label="Pocket: 7 depth units")
        ax.plot(u, tab, color="#edc485", linewidth=2, linestyle="--", label=f"Tab: {key} depth units")
        if key != 7:
            ax.fill_between(u, pocket, tab, color="#f66d7f", alpha=.9, label="Interior overlap")
            ax.annotate("Both solids occupy this region", xy=(0, 8), xytext=(-.92, 10.7),
                        color=text, fontsize=10, arrowprops={"arrowstyle": "->", "color": text})
        else:
            ax.text(0, 10.6, "One shared boundary · no overlap", color=text, ha="center", fontsize=11)
        ax.set(xlim=(-1, 1), ylim=(-2, 12), xlabel="Across one port (u)", ylabel="Depth units (1 / 4096)")
        ax.set_title(title, color=text, fontsize=15, pad=14)
        ax.tick_params(colors=muted); ax.xaxis.label.set_color(muted); ax.yaxis.label.set_color(muted)
        for spine in ax.spines.values():
            spine.set_color("#32475d")
        ax.legend(loc="lower center", fontsize=9, facecolor=background, edgecolor="#32475d", labelcolor=text)
    fig.suptitle("The recut chair and how its surfaces meet", color=text, fontsize=23, y=.97)
    fig.text(.5, .923, "Teal = tabs   ·   Orange = pockets   ·   Body colors identify identical copies", ha="center", color=muted, fontsize=12)
    fig.text(.5, .035, "3D features enlarged: width ×3, depth ×12. Cross-sections exaggerate vertical scale. Exact curved solid remains a research proposal.",
             ha="center", color=muted, fontsize=10)
    fig.subplots_adjust(left=.07, right=.98, top=.88, bottom=.1, hspace=.28, wspace=.2)
    fig.savefig(OUT / "recut-chair-placements.png", dpi=150, facecolor=background)
    plt.close(fig)


def run():
    data = data_from_frozen()
    template = (HERE / "recut_viewer.html").read_text()
    assert template.count("__DATA__") == 1
    (OUT / "recut-chair.html").write_text(template.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    figure(data)
    print(f"Built frozen-candidate viewer: {len(data['faces'])} faces; placements 1, 8, 64; valid and failing contact pairs.")


if __name__ == "__main__":
    run()

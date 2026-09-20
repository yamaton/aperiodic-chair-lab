"""Render a square, triangular, or relocated chair in Blender; run with uv."""

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "strong"))
from build_recut_visualization import data_from_frozen, face_mesh


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(folder, width_scale, depth_scale):
    data = data_from_frozen()
    source = json.loads((ROOT / "strong/audit/frozen_v1/candidate.json").read_text())
    assert source["cap_polynomial"]["a"] == "1/5"
    assert source["cap_polynomial"]["b"] == "1/7"
    width = Q(source["half_width"]) * width_scale
    depth = Q(source["height_unit"]) * depth_scale
    reach = 12 * depth * Q(47, 35)
    margin = Q(5, 16) - width
    gaps = {"same_unit_face": Q(1, 8)-2*width,
            "coplanar_faces": 2*margin, "parallel_planes": 1-2*reach,
            "perpendicular_faces": margin-reach}
    assert all(gap > 0 for gap in gaps.values()), "Enlarged feature boxes must remain separated"
    assert reach < Q(1, 4), "Features must retain each carrier cube's middle half"
    data.update(width=float(width), depth=float(depth),
                feature_width_multiplier=width_scale, feature_depth_multiplier=depth_scale,
                detail_magnification=32 / width_scale)
    divisions = 24
    quads, kinds = [], []
    error = 0.0
    for face in data["faces"]:
        parts = face_mesh(face, data["width"], data["depth"], divisions)
        cap_parts = [points for points, kind in parts if kind]
        assert len(cap_parts) == 8 * divisions**2
        for i, port in enumerate(face["ports"]):
            points = np.array(cap_parts[i*divisions**2:(i+1)*divisions**2])
            delta = points - port["center"]
            u = delta @ np.array(port["u"]) / data["width"]
            v = delta @ np.array(port["v"]) / data["width"]
            assert np.max(np.abs(u)) <= 1 + 1e-12
            assert np.max(np.abs(v)) <= 1 + 1e-12
            expected = port["key"] * data["depth"] * (1-u*u)*(1-v*v)*(1+u/5+v/7)
            error = max(error, float(np.max(np.abs(delta @ np.array(face["normal"]) - expected))))
        for points, kind in parts:
            quads.append(points)
            kinds.append(kind)
    assert error < 1e-12
    vertices, inverse = np.unique(np.round(np.array(quads).reshape(-1, 3), 12), axis=0, return_inverse=True)
    np.savez_compressed(folder / "chair.npz", vertices=vertices,
                        faces=inverse.reshape(-1, 4), kinds=kinds)

    # Recover the two actual ports at the existing viewer's valid contact.
    target = tuple(map(Q, data["contact_center"]))
    paired = []
    for placement in data["placements"]["valid"]:
        matrix = placement["matrix"]
        def rotate(p):
            return tuple(sum(Q(a)*b for a, b in zip(row, p)) for row in matrix)
        for index, port in enumerate(source["ports"]):
            local_center = tuple(map(Q, port["center"]))
            center = tuple(a+b for a, b in zip(placement["center"], rotate(local_center)))
            if center == target:
                paired.append({"source_port_index": index, "key": port["signed_key"],
                               "center": center, "u": rotate(port["u_axis"]),
                               "v": rotate(port["v_axis"]), "n": rotate(port["outward_normal"])})
    assert len(paired) == 2
    a, b = paired
    assert a["key"] == -b["key"] and abs(a["key"]) == 7
    assert a["u"] == b["u"] and a["v"] == b["v"]
    assert a["n"] == tuple(-x for x in b["n"])
    def point(port, u, v):
        height = port["key"]*depth*(1-u*u)*(1-v*v)*(1+u/5+v/7)
        return tuple(port["center"][k] + width*(u*port["u"][k]+v*port["v"][k])
                     + height*port["n"][k] for k in range(3))
    for u, v in product([Q(i, 4) for i in range(-4, 5)], repeat=2):
        assert point(a, u, v) == point(b, u, v)

    # Independently check that the eight recorded placements partition 2L.
    cells = []
    for child in source["children"]:
        for cube in source["coarse_cubes"]:
            corners = [tuple(child["center"][i] + sum(child["matrix"][i][j]*(cube[j]+d[j]) for j in range(3))
                             for i in range(3)) for d in product((0, 1), repeat=3)]
            cells.append(tuple(min(c[i] for c in corners) for i in range(3)))
    expected = {tuple(2*c[i]+d[i] for i in range(3)) for c in source["coarse_cubes"] for d in product((0, 1), repeat=3)}
    assert len(cells) == len(set(cells)) == 56 and set(cells) == expected
    data["detail_ports"] = [{"key": p["key"], "v_sign": int(np.dot(np.cross(p["n"], p["u"]), p["v"]))}
                            for p in sorted(paired, key=lambda p: -p["key"])]
    (folder / "scene.json").write_text(json.dumps(data))
    return {"candidate_sha256": data["candidate_sha256"], "ports": 192, "unit_faces": 24,
            "feature_width_multiplier": width_scale, "feature_depth_multiplier": depth_scale,
            "rendered_half_width": str(width), "rendered_height_unit": str(depth),
            "feature_reach_bound": str(reach), "minimum_face_edge_margin": str(margin),
            "feature_box_separation_bounds": {name: str(gap) for name, gap in gaps.items()},
            "retains_middle_half_of_carrier_cubes": True,
            "cap_divisions_per_axis": divisions, "maximum_sampled_surface_error": error,
            "vertex_coordinate_rounding_digits": 12,
            "contact_source_port_indices": [p["source_port_index"] for p in paired],
            "contact_signed_keys": [p["key"] for p in paired],
            "contact_shared_frames_and_opposite_keys": True, "exact_contact_samples": 81,
            "eight_children_partition_scale_two_carrier": True, "coarse_cells": 56}


def compose(folder, output, width_scale, depth_scale):
    data = json.loads((folder / 'scene.json').read_text())
    triangular = data.get('profile') == 'triangular'
    relocated = data.get('variant') == 'relocated'
    canvas = Image.new("RGB", (2400, 1060), "#0c1725")
    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    regular = ImageFont.truetype(font_path, 27)
    small = ImageFont.truetype(font_path, 21)
    headings = [("01  /  ONE BLOCK", "Relocated ports / actual proportions" if relocated else "Triangular ports / two depth levels" if triangular else "192 curved tabs and pockets"),
                ("02  /  MATCHING SURFACES", "One recorded tab / pocket pair"),
                ("03  /  EIGHT COPIES", "The recorded parent assembly")]
    for i, (heading, subtitle) in enumerate(headings):
        x = i*800
        draw.text((x+48, 52), heading, font=regular, fill="#edf5fc")
        draw.text((x+48, 97), subtitle, font=small, fill="#a8bacb")
        panel = Image.open(folder / f"panel-{i}.png").convert("RGBA")
        canvas.paste(panel, (x, 155), panel)
    key = data['detail_ports'][0]['key']
    draw.text((1010, 790 if triangular else 760), f"TAB  +{key}", font=small, fill="#65d6ba", anchor="mt")
    draw.text((1400, 790 if triangular else 760), f"POCKET  -{key}", font=small, fill="#e9b875", anchor="mt")
    detail_label = "2.67x close-up / uniform magnification" if relocated else "32x close-up / uniform magnification" if (width_scale, depth_scale) == (1, 1) else "Close-up / same enlarged surface profile"
    draw.text((1200, 875), detail_label, font=small, fill="#a8bacb", anchor="mt")
    draw.line((800, 45, 800, 970), fill="#26374a", width=1)
    draw.line((1600, 45, 1600, 970), fill="#26374a", width=1)
    proportions = "exact design proportions" if relocated else "original feature proportions" if (width_scale, depth_scale) == (1, 1) else f"features enlarged: width {width_scale}x, depth {depth_scale}x"
    label = "Relocated triangular candidate" if relocated else "Triangular cubic candidate" if triangular else "Frozen port layout"
    draw.text((48, 994), f"{label}  /  {proportions}  /  visualization mesh",
              font=small, fill="#a8bacb")
    canvas.save(output, optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blender", default="/mnt/d/apps/blender/5.2.1/blender.exe")
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--variant", choices=['square','triangular','relocated'], default='square')
    parser.add_argument("--feature-width-scale", type=int, default=1)
    parser.add_argument("--feature-depth-scale", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if min(args.feature_width_scale, args.feature_depth_scale, args.samples) <= 0:
        parser.error("Feature scales and sample count must be positive")
    if args.variant == 'relocated' and (args.feature_width_scale, args.feature_depth_scale) != (1, 1):
        parser.error('The relocated witness uses its checked design dimensions; leave both display scales at 1')
    default_name = {'square':'aperiodic-chair-cover-blender.png',
                    'triangular':'aperiodic-chair-cover-triangular.png',
                    'relocated':'aperiodic-chair-cover-relocated.png'}[args.variant]
    output = (args.output or ROOT / 'docs/figures' / default_name).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    windows = args.blender.lower().endswith(".exe")
    def native(path):
        return subprocess.check_output(["wslpath", "-w", str(path)], text=True).strip() if windows else str(path)
    with tempfile.TemporaryDirectory(prefix="chair-cover-") as temporary:
        folder = Path(temporary)
        if args.variant == 'relocated':
            from relocated_cover_mesh import prepare_relocated
            report = prepare_relocated(folder)
        elif args.variant == 'triangular':
            from triangular_cover_mesh import prepare_triangular
            report = prepare_triangular(folder, args.feature_width_scale, args.feature_depth_scale)
        else:
            report = prepare(folder, args.feature_width_scale, args.feature_depth_scale)
        worker = ROOT / "docs/blender_chair_cover.py"
        subprocess.run([args.blender, "--background", "--factory-startup", "--python-exit-code", "1",
                        "--python", native(worker), "--", native(folder), str(args.samples)], check=True)
        compose(folder, output, args.feature_width_scale, args.feature_depth_scale)
        report.update(json.loads((folder / "render.json").read_text()))
    report.update({"status": "passed", "image_sha256": sha(output),
                   "composition_font": "DejaVuSans.ttf", "image_dimensions": [2400, 1060],
                   "driver_sha256": sha(Path(__file__)), "blender_script_sha256": sha(worker),
                   "mesh_exporter_sha256": sha(ROOT / "strong/build_recut_visualization.py"),
                   "scope": "Rendering provenance and finite geometry checks; no new tiling theorem or mesh certification."})
    if args.variant in ('triangular', 'relocated'):
        report['triangular_mesh_exporter_sha256'] = sha(ROOT / 'docs/triangular_cover_mesh.py')
    if args.variant == 'relocated':
        report['relocated_mesh_exporter_sha256'] = sha(ROOT / 'docs/relocated_cover_mesh.py')
    output.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print(output)


if __name__ == "__main__":
    main()

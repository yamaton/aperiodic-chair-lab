"""Run the compiled cluster screen under uv, then exact-cover its survivors."""

import argparse
from pathlib import Path
import json
import subprocess
import tempfile

from chair_fusion import transforms
from fused_chair import rotate
from offset_dipoles import OUT
from open_chair_clusters import cover, placements, region


def signature(i, tiles, adjacency):
    c, direction = tiles[i]
    variants = []
    for axes, signs in transforms(True):
        if rotate(direction, axes, signs) != (1, 1, 1):
            continue
        variants.append(tuple(sorted((rotate(tuple(tiles[j][0][k] - c[k] for k in range(3)), axes, signs),
                                      rotate(tiles[j][1], axes, signs)) for j in adjacency[i])))
    return min(variants)


def run(level=5, size=8, seconds=180):
    tiles, adjacency, distances = region(level)
    core = {i for i, distance in distances.items() if distance >= size - 1}
    if not core:
        raise ValueError("Increase level to provide sufficient halo")
    root = max(sorted(core), key=lambda i: distances[i])
    signatures = {}
    for i in sorted(core):
        signatures.setdefault(signature(i, tiles, adjacency), i)
    priorities = [i for i in signatures.values() if i != root]
    targets = priorities + [i for i in sorted(core) if i != root and i not in priorities]
    # Every core chair must occur in a copy, not just one representative of
    # each immediate neighborhood. The compiled screen makes this affordable.
    print("Tiles", len(tiles), "core", len(core), "anchor", root,
          "anchor depth", distances[root], "target chairs", len(targets), flush=True)
    radius = 2**level
    with tempfile.TemporaryDirectory(prefix="aperiodic-chair-") as temporary:
        temporary = Path(temporary)
        source = Path(__file__).with_name("eight_chair_screen.cpp")
        executable = temporary / "screen"
        subprocess.run(["g++", "-std=c++17", "-O3", str(source), "-o", str(executable)], check=True)
        input_path, output_path = temporary / "input.txt", temporary / "screen.json"
        with input_path.open("w") as stream:
            print(len(tiles), radius, root, size, seconds, len(targets), file=stream)
            for i, (c, direction) in enumerate(tiles):
                code = sum((v > 0) << k for k, v in enumerate(direction))
                print(*c, code, len(adjacency[i]), *sorted(adjacency[i]), file=stream)
            for axes, signs in transforms(True):
                print(*axes, *signs, file=stream)
            print(*targets, file=stream)
        subprocess.run([str(executable), str(input_path), str(output_path)], check=True)
        report = json.loads(output_path.read_text())
    report.update(level=level, cluster_size=size, total_chairs=len(tiles), root=root,
                  core_chairs=sorted(core), targets=targets,
                  scope="One proper congruence class of face-connected whole-chair clusters; coarse geometry only, with sufficient halo.")
    path = OUT / f"chair_screen_{size}_level{level}.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    for index, record in enumerate(report["shapes"]):
        shape = tuple((tuple(c), tuple(s)) for c, s in record["chairs"])
        options = placements(shape, tiles, core)
        result = cover(options, core, seconds=30)
        record.update(placements=len(options), cover=result)
        if index % 25 == 0 or result["status"] != "unsat":
            print("Exact cover", index + 1, "/", len(report["shapes"]), result["status"], flush=True)
        if index % 25 == 0 or result["status"] != "unsat":
            checkpoint = path.with_suffix(".tmp")
            checkpoint.write_text(json.dumps(report, indent=2) + "\n")
            checkpoint.replace(path)
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("shapes", "core_chairs", "targets", "rejected_at_target", "rejection_examples")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=5)
    parser.add_argument("--size", type=int, default=8)
    parser.add_argument("--seconds", type=int, default=180)
    args = parser.parse_args()
    run(args.level, args.size, args.seconds)

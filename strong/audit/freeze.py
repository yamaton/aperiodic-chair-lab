"""Freeze the proposed solid and its explicitly stated substitution.

This copies construction data, not search conclusions. Existing snapshots
are never replaced. Run from the repository root with uv.
"""

import hashlib
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).with_name("frozen_v1")


def run():
    if DEST.exists():
        raise SystemExit("Snapshot already exists; refusing to replace it.")
    raw = (ROOT / "strong/artifacts/recut_chair_exact.json").read_bytes()
    source = json.loads(raw)
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    # Transcribed from the displayed maps in RECUT_CHAIR.md, section 3.
    children = [
        {"center": [0, 0, 0], "matrix": identity},
        {"center": [1, 1, -1], "matrix": [[0, 0, -1], [-1, 0, 0], [0, 1, 0]]},
        {"center": [1, -1, 1], "matrix": [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]},
        {"center": [1, -1, -1], "matrix": [[0, -1, 0], [1, 0, 0], [0, 0, 1]]},
        {"center": [-1, 1, 1], "matrix": [[0, 1, 0], [0, 0, -1], [-1, 0, 0]]},
        {"center": [-1, 1, -1], "matrix": [[0, 0, 1], [0, -1, 0], [1, 0, 0]]},
        {"center": [-1, -1, 1], "matrix": [[1, 0, 0], [0, 0, 1], [0, -1, 0]]},
        {"center": [-1, -1, -1], "matrix": identity},
    ]
    data = {"schema": 1, "convention": "proper rotations and translations; one physical handedness",
            "coarse_cubes": [p for p in product((-1, 0), repeat=3) if p != (0, 0, 0)],
            "ports": source["ports"], "half_width": source["half_width"],
            "height_unit": source["height_unit"],
            "cap_polynomial": {"formula": "(1-u^2)(1-v^2)(1+a*u+b*v)", "a": "1/5", "b": "1/7"},
            "children": children}
    DEST.mkdir()
    candidate = json.dumps(data, indent=2).encode() + b"\n"
    (DEST / "candidate.json").write_bytes(candidate)
    proposal = (ROOT / "strong/RECUT_CHAIR.md").read_bytes()
    (DEST / "proposal.md").write_bytes(proposal)
    manifest = {"snapshot": "frozen_v1", "date": "2026-09-15",
                "candidate_sha256": hashlib.sha256(candidate).hexdigest(),
                "archived_proposal_sha256": hashlib.sha256(proposal).hexdigest(),
                "source_geometry_sha256": hashlib.sha256(raw).hexdigest(),
                "source_files": {}}
    for name in ("chair_recut.py", "chair_recut_screen.cpp", "chair_recut_stars.py",
                 "chair_recut_macro.py", "verify_chair_recut_hierarchy.py", "chair_recut_geometry.py"):
        manifest["source_files"][name] = hashlib.sha256((ROOT / "strong" / name).read_bytes()).hexdigest()
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps({"snapshot": str(DEST), "candidate_sha256": manifest["candidate_sha256"]}))


if __name__ == "__main__":
    run()

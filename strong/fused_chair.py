"""Synthesize filler ownership for a fixed eight-chair / six-cross block.

An eight-chair substitution cluster has three proper rotations preserving
its missing-octant direction. A fixed asymmetric selection of six X pieces
could use those rotations to assign fillers differently in each occurrence.
This first stage tests geometry/ownership only, before the X markings.
"""

import argparse
from collections import Counter, defaultdict
from itertools import product
import json
import time

import z3

from chair_clusters import patch
from chair_fusion import transforms
from offset_dipoles import OUT


SITES = tuple(p for p in product((-1, 0, 1), repeat=3)
              if p not in ((0, 0, 0), (1, 1, 1)))


def rotate(vector, axes, signs):
    return tuple(signs[k] * vector[axes[k]] for k in range(3))


def interior_points(level):
    # Coarse patch support is [-s,s]^3 minus the positive octant cube.
    # The complete radius-two box about each point lies within this support.
    # Any missing chair capable of supplying one of these points would have
    # its entire support inside that box, contradicting the existing tiling.
    s = 2**level
    return [p for p in product(range(-s + 2, s - 1), repeat=3)
            if min(p) <= -2]


def run(level=3, seconds=60):
    started = time.monotonic()
    tiles = patch(level)
    centers = {c for c, _ in tiles}
    core = set(interior_points(level))
    rotations = list(transforms(True))
    shape = [z3.Bool(f"attach{q}") for q in range(len(SITES))]
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=seconds * 1000)
    solver.add(z3.PbEq([(v, 1) for v in shape], 6))
    contributions = defaultdict(list)
    poses, pose_rotations = {}, {}
    for i, (c, direction) in enumerate(tiles):
        allowed = [(axes, signs) for axes, signs in rotations
                   if rotate((1, 1, 1), axes, signs) == direction]
        assert len(allowed) == 3
        pose_rotations[i] = allowed
        pose = [z3.Bool(f"tile{i}pose{r}") for r in range(3)]
        poses[i] = pose
        solver.add(z3.PbEq([(v, 1) for v in pose], 1))
        for r, (axes, signs) in enumerate(allowed):
            for q, site in enumerate(SITES):
                moved = rotate(site, axes, signs)
                p = tuple(c[k] + moved[k] for k in range(3))
                if p in core:
                    contributions[p].append(z3.And(pose[r], shape[q]))
    for p in sorted(core):
        terms = contributions[p]
        target = int(p not in centers)
        if not terms:
            assert target == 0, ("missing possible filler", p)
        elif target:
            solver.add(z3.PbEq([(v, 1) for v in terms], 1))
        else:
            solver.add([z3.Not(v) for v in terms])
    print("Macrochairs", len(tiles), "interior vertices", len(core),
          "candidate attachment sites", len(SITES), flush=True)
    status = solver.check()
    result = {"status": str(status), "level": level, "macrochairs": len(tiles),
              "interior_vertices": len(core), "attachment_site_count": len(SITES),
              "attached_crosses_per_block": 6, "base_chairs_per_block": 8,
              "proper_internal_orientations": 3,
              "scope": "Identical eight-chair substitution clusters with six whole X fillers chosen from 25 nearby sites. Markings not included; arbitrary cuts not included.",
              "elapsed_seconds": time.monotonic() - started}
    if status == z3.sat:
        model = solver.model()
        attached = [site for v, site in zip(shape, SITES) if z3.is_true(model.eval(v))]
        orientations = [next(r for r, v in enumerate(poses[i]) if z3.is_true(model.eval(v)))
                        for i in range(len(tiles))]
        counts = Counter()
        for i, (c, _) in enumerate(tiles):
            axes, signs = pose_rotations[i][orientations[i]]
            for site in attached:
                moved = rotate(site, axes, signs)
                counts[tuple(c[k] + moved[k] for k in range(3))] += 1
        assert all(counts[p] == int(p not in centers) for p in core)
        result.update(attachment_sites=attached, macrochair_orientations=orientations,
                      independently_checked_core_vertices=len(core))
    (OUT / f"fused_chair_level{level}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "macrochair_orientations"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=3)
    parser.add_argument("--seconds", type=int, default=60)
    args = parser.parse_args()
    run(args.level, args.seconds)

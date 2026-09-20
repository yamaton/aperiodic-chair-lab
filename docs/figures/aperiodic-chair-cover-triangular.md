# README cover: triangular cubic ports

This earlier illustration is preserved. The current README uses the
[relocated-port cover at actual design proportions](aperiodic-chair-cover-relocated.md).

[Cover image](aperiodic-chair-cover-triangular.png) ·
[Rendering receipt](aperiodic-chair-cover-triangular.json) ·
[Earlier square-port cover](aperiodic-chair-cover-enlarged.md)

This Blender cover depicts the separate
[triangular_v1 candidate](../../strong/audit/triangular_v1/candidate.json).
It uses the exact candidate's 192 port frame anchors, ordered axes, signed
keys ±1 and ±2, and eight child placements. The profile is the cubic bubble
on the scalene triangle, not the earlier square polynomial.

For visibility, all three panels use **3× scaling in both tangent directions
and 64× scaling in normal depth**. The image footer and README caption
disclose both factors. These are display alterations, not a newly certified
physical solid or a tolerance study. The lower-degree profile is still
curved; the image is not a polyhedral replacement design.

The composition retains the earlier camera, lighting and palette for the
whole-chair views:

- One chair, with teal protrusions and amber recesses. All ports use the
  same two absolute depth levels; colors add no matching constraints.
- A **+2/-2** pair from an actual internal contact of the eight-child
  assembly. The two neighborhoods are independently reoriented by proper
  rotations to expose their surfaces; they are displayed apart, not in
  their mating pose. Their apparent mirror relation is from viewing the
  two opposite sides of one matching interface. The camera is raised to
  make the triangular boundaries visible. Flat cut sides are artificial
  crop boundaries. Uniform magnification of **32/3** follows the same
  disclosed feature enlargement used on the whole chair.
- Eight identical chairs in the recorded child placements. Body colors
  identify the children. The complete assembly is shown at half the
  single-chair scale, preserving its feature proportions.

## Reproduce

From the repository root, using the locked Python environment and the
Windows Blender installation via WSL:

```sh
uv run --locked python docs/render_chair_cover.py \
  --variant triangular \
  --blender /mnt/d/apps/blender/5.2.1/blender.exe --samples 64 \
  --feature-width-scale 3 --feature-depth-scale 64 \
  --output docs/figures/aperiodic-chair-cover-triangular.png
```

The driver uses `wslpath` for Windows paths, prepares meshes, launches
Blender and composes three transparent renders. The triangular variant
defaults to this output filename; square remains the default variant for
the earlier reproduction commands. The old PNGs and receipts are preserved.

The selected rendering uses Blender 5.2.1 LTS, Cycles, OptiX and 64 samples.
No bevel, subdivision or displacement modifier changes the mesh; curved
patches use interpolated shading normals. Hardware-dependent rendering is
not promised to yield identical image hashes across systems.

## Geometry checks and provenance

The [mesh exporter](../triangular_cover_mesh.py) verifies the new snapshot
hash and its correspondence to the old frame layout. It samples the cubic
over a triangular lattice and fills the rest of each old port square with
flat triangles. Positive projected areas and total areas check the patch's
orientation and coverage: the triangular support occupies one quarter of
the old square. Whole-chair cap edges use 24 subdivisions, and the close-up
uses 80. The complete chair mesh contains 110,592 curved triangles; the
receipt records the total mesh size and the sampled-coordinate error.

The exporter checks all **384 internal port pairs** in the recorded
eight-chair group for matching anchors and ordered axes, opposite normals
and opposite keys. The displayed pair has source port indices **40 and 56**
in children **7 and 6**, respectively (all indices zero-based). Its common
frame anchor is `(-27/16, -25/16, 0)`. Exact rational evaluation agrees at
**91 triangular-lattice samples**. The matching frames and opposite keys
also explain coincidence of the entire specified polynomial graphs; a
sample test alone would not establish that implication.

The enlarged width parameter is 3/64, depth unit 1/64, and maximum reach
1/32. Feature-box separation bounds remain positive:

| Configuration | Lower bound |
|---|---:|
| Distinct ports on one unit face | 1/32 |
| Different coplanar faces | 17/32 |
| Parallel grid planes | 15/16 |
| Perpendicular grid faces | 15/64 |

The face-edge margin is at least 17/64, and each carrier cube retains its
middle half. An independent corner calculation checks that the eight child
placements partition exactly 56 cells of the doubled carrier.

The JSON receipt records these checks, input and source hashes, rendering
settings and the final image hash. They establish rendering provenance and
bounded geometric checks, not a certified aperiodic mesh, print or enlarged
solid. See the [shape report](../../strong/PORT_SIMPLIFICATION.md) for the
exact candidate and the distinction between written arguments and finite
checks. Both mathematical snapshots remain unchanged.

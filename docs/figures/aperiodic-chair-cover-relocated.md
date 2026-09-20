# README cover: relocated triangular ports at their design proportions

[Cover image](aperiodic-chair-cover-relocated.png) ·
[Rendering receipt](aperiodic-chair-cover-relocated.json) ·
[Earlier triangular cover](aperiodic-chair-cover-triangular.md)

This Blender cover depicts the common-offset witness in
[the dimension study](../../strong/PORT_DIMENSIONS.md), also taught in
[tutorial Section 10](../APERIODIC_CHAIR_TUTORIAL.md#101-move-and-enlarge-the-ports-while-preserving-the-rules).
It uses the same 192 ordered port frames, signed keys and eight child
placements as `triangular_v1`, with the following parameter changes:

| Parameter, in carrier-cube side units | Rendered design |
|---|---:|
| Anchor p relative to face center f | `p=f-U/4+7V/32` |
| Width parameter / short triangle leg | 3/16 |
| Long triangle leg | 3/8 |
| Lower / higher peak depth | 1/16 / 1/8 |

These are the candidate's **actual design proportions**, with no extra
width or depth exaggeration. Relative to the recorded small triangular
snapshot, the design has 12× width and 256× depth; relocation is essential.
The cover does not simply enlarge the old ports at their old positions.
The triangle profile remains the cubic bubble `27 lambda0 lambda1 lambda2`.

The image has three panels:

- One chair. Teal marks protrusions and amber marks recesses; color adds
  no matching constraint.
- The +2/-2 ports from a recorded internal contact, shown apart and each
  independently reoriented by a proper rotation to expose its surface.
  The crop is the triangle expanded uniformly by 9/8 about its centroid;
  its rim stays inside the actual face wedge, clear of other ports.
  The backing and side walls are artificial crop boundaries. An additional
  **uniform magnification of 8/3** applies to the complete crop, preserving
  the cap's aspect ratios.
- The eight congruent chairs in the recorded child placements, with body
  colors identifying children. The whole assembly is uniformly reduced
  to half the single-chair display scale.

The previous triangular cover and its rendering receipt are preserved. Its
3× width / 64× depth display settings are the earlier illustration marked
“Cover” in the dimension-study plot; the new cover corresponds to the plot's
12× width / 256× depth candidate instead. The older square covers are also
preserved. Neither mathematical snapshot has been replaced.

## Reproduce

From the repository root:

```sh
uv run --locked python docs/render_chair_cover.py \
  --variant relocated \
  --blender /mnt/d/apps/blender/5.2.1/blender.exe --samples 64 \
  --output docs/figures/aperiodic-chair-cover-relocated.png
```

The relocated variant uses the checked design dimensions and requires both
optional display-scale arguments to remain at 1. The driver supports the
earlier `square` and `triangular` variants with their previous defaults.
It prepares meshes, uses `wslpath` for Windows Blender, renders three
transparent panels, and composes the 2400×1060 PNG. The final render uses
Blender 5.2.1 LTS, Cycles, OptiX and 64 samples, following a 16-sample preview.
Hardware-dependent rendering is not promised to be pixel-identical.

## Mesh construction and checks

The old square cutouts overlap at these dimensions, so the new
[mesh exporter](../relocated_cover_mesh.py) divides each face into eight
reflection wedges. Within each wedge it samples one curved triangular cap
and triangulates three flat strips between the support and wedge boundary.
Both sides of every cap edge share the same boundary subdivisions. Exact
areas are 1/8 per wedge, 9/256 per cap, and 1 for the complete face projection.
The close-up uses the same construction with a padded triangular outer boundary.

The single-chair mesh uses 48 subdivisions per cap edge: 442,368 curved
triangles and 470,592 total triangles, with 235,298 welded vertices.
Every mesh edge has exactly two oppositely directed incident triangles,
the Euler characteristic is 2, and the signed mesh volume agrees with 7
to floating-point precision. All triangles have positive area. The sampled
surface-coordinate error is below 1e-12. The two cropped meshes, with 80
subdivisions per cap edge, pass the same seam and orientation checks.
There are no geometry modifiers; only curved-face shading normals are smoothed.

The exporter also checks all **384 internal port pairs** in the eight-chair
assembly: shared anchors and ordered axes, opposite normals and keys.
The displayed ports remain indices **40 and 56**, in children **7 and 6**
(zero-based), now sharing anchor `(-5/4,-55/32,0)`. All 91 exact rational
triangle samples of that contact agree. The full polynomial coincidence
follows from the shared frames and opposite keys, not from sampling alone.
An independent corner calculation checks the exact 56-cell child partition.

The receipt hashes the source triangular snapshot, dimensional evidence,
mesh exporters, Blender worker, composition driver and final image. It
records the geometric checks and display transformations. The dimension
study provides the exact curved-solid separation argument; these meshes
approximate that surface and are not certified aperiodic or tolerance-tested
manufactured blocks.

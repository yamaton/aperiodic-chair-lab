# Cover rendered from the frozen chair

**Original-proportion square reference:** the README now uses the
[triangular cubic cover](aperiodic-chair-cover-triangular.md). The earlier
[square version with enlarged features](aperiodic-chair-cover-enlarged.md)
is also preserved.
This image and its original receipt are preserved; its source hashes record
the scripts at the time of rendering, before display-scale options were added.

[Cover image](aperiodic-chair-cover-blender.png) ·
[Rendering and geometry receipt](aperiodic-chair-cover-blender.json)

The README cover is a Blender render of the frozen v1 candidate, replacing
the earlier AI concept illustration. It uses the existing coordinate-driven
mesh exporter, not geometry reconstructed from that illustration.

The three views show:

- One chair, with all 192 ports at their specified positions, frames and
  signed depths. Width and depth multipliers are both **1**.
- Cropped neighborhoods of the recorded valid contact's +7 and -7 ports,
  each rigidly reoriented to expose its surface. Every length is magnified
  by **32**, so width-to-depth ratios remain unchanged. The flat sides are
  artificial crop boundaries, not edges of the complete chair. The two
  cropped surfaces are displayed separately, not in their mating pose.
- The eight recorded child placements, forming the scale-two chair. The
  whole assembly is displayed at half the single-chair scale, to compare
  silhouettes. Colors identify children; teal and orange identify tabs and
  pockets. Color is not an additional matching rule.

The candidate specifies port half-width 1/64 and depth unit 1/4096.
Its actual features are consequently small in the full-object views.
The close-up and raking lighting reveal the curvature without exaggerating
the relief. No bevel, subdivision or displacement modifier changes the mesh.
Cap shading interpolates normals; the underlying surfaces are triangulated
approximations of the specified polynomials. This is neither a certified
aperiodic mesh nor a manufacturing design.

## Reproduce

From the repository root, in WSL with the user's Windows Blender installation:

```sh
uv run --locked python docs/render_chair_cover.py \
  --blender /mnt/d/apps/blender/5.2.1/blender.exe --samples 64
```

The driver uses `wslpath` to pass UNC paths to Blender. It prepares temporary
mesh data, invokes [the Blender worker](../blender_chair_cover.py), and
composes three transparent renders into the PNG. It uses the locked Python
environment, Pillow and the DejaVu Sans font installed in WSL; Blender uses
its own embedded Python runtime. Pass `--blender /path/to/blender` for a
Linux installation, or `--output /path/to/cover.png` for a separate render.
The default output is this figure and its adjacent JSON receipt.

Blender 5.2.1 LTS rendered the selected image with Cycles, 64 samples and
OptiX. The receipt records the detected devices. Rendering results may vary
with Blender version, hardware and denoising; this is not a promise of
identical image hashes across systems.

## Checks and scope

The driver verifies the frozen candidate hash against its manifest. It
checks every sampled cap vertex against the frozen port's local frame and
polynomial before rounding mesh coordinates to 12 decimal places. It also
checks the chosen contact's coincident centers, matching ordered tangent
frames and opposite signed depths/normals, plus 81 exact rational surface
samples. Finally, it independently checks that the eight placements cover
exactly the 56 distinct unit cells of the scale-two carrier.

The JSON receipt records those checks, render settings, source and output
hashes. These are bounded rendering/geometry checks, not new proofs of
tilability, forced hierarchy, aperiodicity or mesh equivalence. The current
mathematical scope remains in [PROOF_STATUS.md](../PROOF_STATUS.md).

Frozen research data and the previous reproducible figures are unchanged.

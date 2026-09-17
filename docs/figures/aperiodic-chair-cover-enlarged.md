# README cover with enlarged surface features

[Cover image](aperiodic-chair-cover-enlarged.png) ·
[Rendering receipt](aperiodic-chair-cover-enlarged.json) ·
[Original-proportion reference](aperiodic-chair-cover-blender.md)

At the user's request, this Blender cover enlarges the specified ports by
**3× in both tangent directions and 12× in normal depth**. Port centers,
ordered frames, signed keys, asymmetric polynomial and child placements
come from the unchanged frozen v1 data. The same factors apply to every
port, in all three panels. Both the image footer and README caption disclose
the enlargement.

The center panel shows cropped neighborhoods of the recorded +7/-7 contact
pair, independently rotated to expose their surfaces. After feature
enlargement, the crops are uniformly magnified by 32/3 for display. Their
flat sides are artificial crop boundaries. The eight-chair assembly is
displayed at half the single-chair scale to compare the silhouettes.
Colors distinguish tabs, pockets and children; they are not extra rules.

## Reproduce

From the repository root in WSL:

```sh
uv run --locked python docs/render_chair_cover.py \
  --blender /mnt/d/apps/blender/5.2.1/blender.exe --samples 64 \
  --feature-width-scale 3 --feature-depth-scale 12 \
  --output docs/figures/aperiodic-chair-cover-enlarged.png
```

The driver defaults to width/depth multipliers of 1; the enlargement is
explicit. The original-proportion image and its receipt are not overwritten
by this command. See the [original rendering notes](aperiodic-chair-cover-blender.md)
for Blender, font and WSL path requirements.

## Checks and limitations

The driver checks the frozen hash, all sampled whole-chair cap vertices
against the rescaled polynomial, 81 exact rational samples of the displayed
contact, its ordered frames/opposite keys, and the eight-child partition of
the 56-cell scale-two carrier. For the enlarged features, the conservative
reach is 423/8960 and the face-edge margin is 17/64. The feature-box
separation bounds remain positive: 1/32 for distinct ports on one unit face,
17/32 for different coplanar faces, 4057/4480 for parallel grid planes, and
1957/8960 for perpendicular faces. Each carrier cube retains its middle half.
These are finite/arithmetic rendering checks, recorded with source and image
hashes in the receipt.

This is a **visualization variant**, not a new frozen design or a completed
audit of an enlarged physical solid. The sampled mesh does not inherit the
analytic curved-surface theorem. The full mathematical scope remains in
[PROOF_STATUS.md](../PROOF_STATUS.md). Frozen evidence and existing research
figures are unchanged.

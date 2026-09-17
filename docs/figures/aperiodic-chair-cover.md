# README cover illustration

**Superseded concept draft:** README now uses the
[Blender rendering from frozen coordinates](aperiodic-chair-cover-blender.md).
This draft is retained for provenance, not used as a geometry reference.

Generated 17 September 2026 with the built-in image generation tool.
Final asset: [aperiodic-chair-cover.png](aperiodic-chair-cover.png).

This is an AI-generated editorial illustration, not a render from the frozen
coordinates. The chair silhouette was corrected against
[the existing figure](../../strong/artifacts/recut-chair.png). Port assignments,
profiles, seams and proportions are schematic; the surface relief is enlarged.
The circular detail illustrates the idea of a curved tab and pocket, not a
verified mating pair. Colors distinguish protrusions and recesses.

An initial assembly view was omitted because the generated child subdivision
was inaccurate. The final cover makes no claim to depict an eight-child
partition or a legal tiling. Existing generated evidence is unchanged.

## Initial generation prompt

```text
Use case: scientific-educational.
Asset type: Wide README cover illustration for Aperiodic Chair Lab, a computational mathematics and interactive assembly project.
Primary request: A beautifully clear, precise-looking scientific 3D editorial illustration that connects the microscopic curved matching features of a single chair block to assembly into a larger block of the same chair shape. The tiny physical surface structure must be the visual focus, not just a generic voxel object.

Scene/backdrop: Clean deep navy background, matching the project's existing scientific figures. Quiet studio lighting with strong readable edge definition, subtle ambient shadows, no decorative laboratory props, no scenery.
Subject geometry: A solid 2 by 2 by 2 cube with exactly ONE unit cube removed from its upper front corner, exposing a concave trihedral notch: a horizontal square floor and two vertical square inner walls. This seven-cube solid is the 3D chair. It is NOT furniture, NOT an arch, NOT a hollow box, and has no legs. Show it in an isometric view looking into the removed corner. Every coarse edge follows one of three orthogonal spatial axes.

Composition: Landscape cover, approximately 2:1. A large single pale slate-blue chair occupies the left half, with its fine surface features strongly visible. A smaller assembled scale-two chair occupies the right half, divided by seams into eight congruent chair-shaped children in muted teal, ochre, lavender, sage and blue. Its overall silhouette is the same cube-minus-one-corner shape as the single chair. Use a gentle partially separated assembly treatment only if the geometry stays intelligible. Thin restrained connectors relate single piece, local detail and larger assembly; keep generous breathing space.
Fine structure: Each exposed UNIT SQUARE of the main chair carries exactly eight small square-footprint curved ports arranged in a compact eight-position ring, two near each side of the ring, leaving the face center empty. These are small asymmetric smoothly bulging caps and corresponding recessed pockets, NOT round drilled holes, random dots, screws, gears or printed circuit traces. Raised caps are teal; recessed pockets have warm orange interiors. Give the features enough exaggerated width and relief to read clearly at README size. Reproduce this structured decoration on exterior faces AND all three faces inside the notch. Keep the surfaces otherwise clean.
Macro detail: Integrate a spacious close-up near the lower center, connected by a thin callout line to one face. Show two opposing square face fragments, slightly separated, one bearing teal smoothly curved asymmetric bumps and the other orange complementary cavities; visibly communicate protrusion meeting matching recess with surface profile and a small directional orientation arrow on each fragment. These ports have square footprints and smooth off-center bulges; avoid pyramids and rounded pegs. This enlarged detail should be large enough to show curved surface relief, not an unreadable tiny inset.
Style/medium: Polished physically lit 3D scientific illustration, satin material, crisp geometry, highly readable restrained composition. Color identifies relief and constituent pieces; no neon glow or sci-fi ornament.
Text: No title, no labels, no equations, no letters, no watermark. The README supplies the title and caption.
Constraints: The image is a conceptual visualization with magnified features, not an exact coordinate diagram or a photograph of a manufactured result. Do not draw an arbitrary repeating tiled floor or imply a finite patch proves aperiodicity. Prioritize recognizable chair shape, readable face decoration and curved matching contact.
```

## Geometry correction prompt

References: the initial generated draft and `strong/artifacts/recut-chair.png`.

```text
Use case: precise-object-edit.
Edit image 1 (the newly generated navy cover with teal bumps and orange pockets). Image 2 is the authoritative geometry reference from this project; use it to correct the shapes, not as an additional panel.
Keep image 1's navy background, satin material, large readable teal raised curved caps and orange curved cavities, wide cover composition and central circular contact close-up. Change the coarse geometries of BOTH main objects to match image 2 precisely.
CRITICAL LEFT OBJECT: Copy the left silhouette and THREE INNER NOTCH FACES of image 2. A true 2x2x2 cube minus just its top-front corner cube. Top horizontal face is L-SHAPED comprising THREE unit squares. The recessed notch has TWO perpendicular vertical walls AND one horizontal floor. Image 1 incorrectly has a flat backrest and is missing an entire row of two cubes. Restore that missing cube so there is a second vertical inner wall. The shape must visibly have exactly seven unit cubes, equal dimensions in all three axes, not furniture. Orient the view symmetrically into the notch, matching image 2.
CRITICAL RIGHT OBJECT: Copy the right silhouette and exact visible seam/color regions from image 2. It is the SAME cube-minus-corner shape with a 4-unit bounding cube and a 2-unit corner removed, with grid lines dividing exterior into unit square faces. It is NOT a stairway or stack of cubes. Outer object has only two main height levels, four units tall and two units tall. Use precisely the reference's child-color arrangement, including pink upper left, lavender upper right, blue recess, gold lower front, green lower left, terracotta lower right, teal upper back. Make it an assembled group with touching seams, not exploded. Do not invent cube children. Decorate its visible unit squares with small matching ports.
Port pattern: eight ports per UNIT face in a ring with empty center; two on each side of the ring. Square footprints, smooth asymmetric caps and recesses. Place on inner notch faces too. These are exaggerated illustrative relief details. Keep left decoration prominent. Leave top margin so neither object touches the image boundary.
No text, no equations, no watermark. Preserve the circular magnification inset with opposing curved tab and pocket. Prioritize the reference's geometry over artistic improvisation.
```

## Final edit prompt

Reference: the corrected generated draft.

```text
Use case: precise-object-edit.
Make a final refined scientific README cover from this image.
Preserve the LEFT seven-cube chair shape exactly: a 2x2x2 cube with one upper front corner removed, two inner vertical notch walls and a square floor. Preserve its navy background, blue-gray satin solid, square-footprint smoothly asymmetric teal protrusions and orange recessed pockets.
Remove the entire right multicolored object: it incorrectly suggests a group of cube-shaped tiles. Replace that right-hand content with a beautifully rendered larger close-up of one teal asymmetric curved tab opposite one matching orange cavity, floating on two small opposing square surface fragments. Adapt the current center circular inset to occupy the right half, using a thin restrained circle frame and a subtle single connector from a port on the main block. Show the two surfaces separated, so the smooth complementary convex/concave geometry and square footprints can be understood clearly. Just ONE enlarged tab and ONE corresponding pocket, not multiple. Omit the arrows; geometry alone should communicate matching. Preserve the asymmetric smoothly bulging cap, not a pyramid or round peg.
Rebalance into a wide 2:1 landscape composition with the single full chair filling the left 55 percent and macro matching detail filling the right 40 percent, with generous outer margins. Main chair stays approximately the current size, centered vertically; inset slightly smaller than the full chair. Do not crop the chair or make anything touch the edges. No title, labels, equations, watermarks, other objects or extra markings. Clean calm polished scientific illustration. The visible main faces each have one eight-port ring per unit square, empty center. No random extra ports or textures. This is an illustrative magnification, not a coordinate-accurate evidence figure.
```

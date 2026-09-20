# Q006–Q008: rules on relative poses and whole face-stars

These rules are allowed to inspect multiple tile poses directly. They are
stronger than matching equal scalar colors at points, so Q002b's obstruction
does not automatically apply. Geometric realization by one solid is separate.

## Q006: the complete substitution-closed pair atlas still permits periodicity

Normalize each sibling contact to a canonical root prism. There are 21
distinct directed relative poses at the first level. Subdivide both sides
of every contact and repeat. Exact closure has counts
21 -> 49 -> 76 -> 86 -> 91 -> 91. The resulting 91 poses include every
positive-area pair contact in every finite supertile, by induction.

The elementary two-prism box filling fails four of its ten directed
contacts. That finite failure was **not** treated as evidence of aperiodicity.
A different periodic filling defeats the entire 91-pose rule.

Reflect the 30–60–90 triangular cross-section across each side while also
reversing z about 1/2. The combined 3D transformations are all proper. All
three side-neighbor poses, and vertical stacking by one unit, belong to the
closed atlas. Enumerating their orbit modulo translations (2,0,0), (0,6,0),
(0,0,1) in rational coordinates yields **24 prisms per cell**.

`atlas_periodic_reflections.py` does not rely on an illustration or on a
reflection-group classification. It checks exact separating axes for all
potentially touching periodic copies, using a bounding-box-derived finite
offset range, and verifies that the cell's volume density is 1. A periodic,
locally finite union of closed solids with disjoint interiors and density 1
has no hole: a missing point would have an open neighborhood of positive
missing volume. All **120 directed area contacts** lie in the atlas.

Thus **any pair-pose rule accepting every quaquaversal substitution contact
also accepts this periodic tiling**, within the modeled positive-area pair
contact semantics. Extra edge/vertex or larger-neighborhood rules can change
the question.

```sh
uv run --locked python strong/quaquaversal/contact_atlas.py
uv run --locked python strong/quaquaversal/atlas_periodic_reflections.py
```

## Q007: root-star overapproximation

`atlas_stars.py` covers the root's 60 boundary panels using neighbors from
the 91-pose atlas and excludes 1,137 neighbor-overlap pairs. The enumeration
reached the explicit 10,000-model limit. This is **unknown/incomplete**, not
an exhaustive count. It does not impose neighbor/neighbor atlas legality
or filling around the exterior edges and vertices of the star. Preserve
the result as an overapproximation, not as a language of realizable tilings.

Q006's actual periodic witness makes finishing this overapproximation
irrelevant to proving that particular pair rule aperiodic.

## Q008: observed complete face-star language

`star_language.py` extracts complete face-stars from a specified finite
supertile, then tests subdivided versions of the periodic reflection tiling.
Each star records all its root-relative neighbor poses. Full coverage of
all 60 root panels is checked. Observed stars are only a **lower bound** on
the intended language; an unobserved star is not proved forbidden.

**Result:** the level-3 proper supertile has 80 distinct complete face-stars.
The once-subdivided 24-prism periodic tiling has 192 prisms and eight distinct
face-stars. All eight occur in the sample. Therefore a rule inspecting only
the root and all its positive-area neighbors, while accepting the actual
quaquaversal language, also accepts this periodic tiling. This is stronger
than the pair-rule obstruction. It does not include neighbors touching only
on edges or vertices, or arbitrary larger-radius neighborhoods.

```sh
uv run --locked python strong/quaquaversal/atlas_stars.py
uv run --locked python strong/quaquaversal/star_language.py
```

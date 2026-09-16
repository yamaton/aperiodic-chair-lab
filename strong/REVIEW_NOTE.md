# Recut chair: a concise request for mathematical review

*16 September 2026. Research proposal; external review and priority unresolved.*

## Proposed claim

There is one compact solid `T` with connected interior and volume 7 that
tiles Euclidean three-space by congruent copies, and every such tiling has
a finite symmetry group. Copies may be placed by arbitrary Euclidean
isometries, including reflections. This excludes every nonzero translation
and every infinite-order screw; it does not assert a trivial symmetry group.

This is the claim to assess, not an assertion of independent mathematical
acceptance. The exact curved solid is essential; its STL is only a picture.

## Specification

Start with unit cubes having lower corners in `{-1,0}³ \ {(0,0,0)}`.
The 24 exposed faces each carry eight disjoint caps. For face center `f`,
outward normal `n`, and ordered signed coordinate axes `u_axis,v_axis`:

```text
p + (u/64)u_axis + (v/64)v_axis + (k/4096)φ(u,v)n,
p = f + (3u_axis+v_axis)/16,        -1 ≤ u,v ≤ 1,
φ(u,v) = (1-u²)(1-v²)(1+u/5+v/7).
```

The 192 signed keys, frames, and eight child placements are in
[the frozen coordinates](audit/frozen_v1/candidate.json), SHA-256
`95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54`.

Three oriented face patterns describe the complete table; see
[their explicit words and handshake rules](FOLLOWUP_REFLECTIONS.md#2-three-oriented-face-patterns-describe-the-full-table)
and [figure](artifacts/orientation-information.png). These are physical
surface features, not independently imposed colored matching rules.

## Proof dependencies and evidence

| Step | Argument or check |
|---|---|
| A solid exists | Disjoint feature boxes, unchanged connected cube cores, zero signed cap-volume sum. |
| A tiling exists | Eight children form a scale-two coarse chair; a closed 30-contact substitution language builds arbitrarily large valid patches; compactness supplies a full tiling. |
| Open cap coincidence determines a frame | The full polynomial graph has exactly five lines, whose arrangement fixes its plane, square center, and ordered tangent axes. Polynomial continuation extends an open coincidence to that graph. |
| Arbitrary tilings lie on one grid | Local finiteness and boundary coverage force open cap contacts; frame identification makes relative translations integral. A cap-contact component occupies every coarse grid cube, with complementary graph interfaces. |
| Reflections do not add mixed tilings | Each key has a fixed local frame determinant, opposite keys have opposite determinants, and a cap match therefore has determinant +1. The component argument forces one handedness globally. |
| Grouping is forced | A/B/C face rules yield 44 contacts; 14 leave a face impossible to cover. Six diagonal contacts force a central neighborhood. Every other chair selects its notch owner as parent, and all seven outer children select the same center. The older 33-star certificate agrees. |
| Rules recur | Of 6,801 macrocontact placements, including misregistered ones, exactly 44 fit; offsets are even, and deflation returns the original 44-contact language. |
| Symmetry is finite | Iterated unique grouping puts a translation period in every `2^m Z³`, hence makes it zero. Boundary planes restrict rotational parts to a finite group; absence of translations makes the symmetry group finite. |

Detailed arguments and certificates are in the [audit](audit/README.md).
There are separate finite implementations and [internal AI reviews](audit/SUBAGENT_REVIEWS.md);
these are not external human reviews or a machine-checked formal proof.
The [reflection check](audit/reflection_verification.json) covers all 48
frame orientations and confirms all 1,536 opposite-key cap correspondences
are proper.

The [local parent proof](MOTIF_GROUPING.md) and [illustrated face layout](artifacts/motif-face-layout.png)
explain grouping without following the full port table or all complete
neighborhoods. Its independent motif checker regenerates the original 33
stars only as a comparison; the grouping implication uses local face
propagation and a uniquely determined parent map.

## Controls and relation to earlier work

The plain seven-cube chair has a periodic lattice tiling. Its proposed
decorations reject that tiling. A specified signed-key quotient erasing
the three internal poses permits a periodic eight-chair tiling with basis
`(14,0,0),(-4,2,0),(-8,0,2)`. Every interface was checked separately. That
altered solid still forces handedness, separating this property from the
recursive information. The [follow-up record](FOLLOWUP_REFLECTIONS.md)
contains the controls and a six-depth alternative with the same contact
language; the twelve-depth frozen solid remains the review target.

The coarse chair and its hierarchy are established prior art. The closest
comparison is Goodman-Strauss, *An Aperiodic Pair of Tiles in Eⁿ for All
n≥3*, European Journal of Combinatorics 20 (1999), 385–395:
[author preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).
His construction uses a chair and a second tile to transmit hierarchical
information. The question here is whether distinguishable rotations of
one physically decorated chair implement the asserted rules without that
second tile. Our search has not established novelty; see the
[source-by-source comparison](audit/LITERATURE_REVIEW.md).

## Focused questions for a reviewer

1. Does open-cap rigidity apply to arbitrary isometries and all contact
   configurations, with no hidden face-to-face assumption?
2. Does the cap-contact component argument exclude shifted, interpenetrating
   coarse supports and separate components before assuming a global grid?
3. Does the local parent rule imply unique grouping for every infinite
   tiling, and does macrocontact recurrence suffice to iterate it? The older
   33-star and child-role certificates provide a second route to compare.
4. Is existence by compactness justified by valid patches containing balls
   of arbitrarily large radius?
5. Is the one-chair oriented rule system already present in the literature,
   perhaps in an equivalent encoding?

No outside communication has been sent. This is a local review artifact.

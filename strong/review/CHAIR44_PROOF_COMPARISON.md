# Chair44 and our candidate: proof comparison and a reusable lemma

*16 September 2026. Follow-up to the [exact correspondence](TSIOKOS_CHAIR44_COMPARISON.md).
Written deductions and independent finite checks; not a full validation of the
published physical theorem. Frozen candidate unchanged.*

## What this comparison adds

**Subsequent continuation:** the [independent companion replay](CHAIR44_COMPANION_REPLAY.md)
now verifies the entire off-grid candidate/collision census, including all
299,975 boxes. The [pinned build record](CHAIR44_BUILD_REPRODUCTION.md) tracks
the successful unchanged-source build and fresh reproduction of all 169 axiom
lines. Its final theorem uses 21 disclosed native hooks and the three standard
logical axioms. The release controls have one missing-archive packaging failure;
all four logical negative controls and positive scope regressions passed.
These updates supersede the earlier next-work status below.

1. An independent reconstruction of Chair44's registered contact atlas from
   its rational pyramid geometry, rather than comparison of supplied atlases.
2. A check connecting its exact solid data to the literals used by its Lean
   definitions, plus a deeper source-level review of the companion argument.
3. A written bijection between the complete legal **grid-model tiling spaces**.
4. An attributed simplification of our component-exhaustion proof, adapted
   from Chair44's formal argument.

All references to released source below use commit
`137e46b15d36266c37879478cfc62af6e4469147` of
[six-birds-tiles](https://github.com/ioannist/six-birds-tiles/tree/137e46b15d36266c37879478cfc62af6e4469147).
The local PDFs are versions 1 and 2; version 2 is the current manuscript
used for comparison. This source comparison does not establish priority.

## 1. Independently recovering their grid contacts

[`reconstruct_chair44_contacts.py`](../audit/reconstruct_chair44_contacts.py)
reads only released JSON, using integer and rational arithmetic. It:

- Derives all 24 exposed panels from the seven carrier cubes.
- Recovers each feature's center, normal and signed height from its four
  base vertices and apex. Checks that the base really is the stated square,
  lies strictly inside its unique carrier panel, and has the stated width.
- Finds all 768 pyramid facets in the actual mesh triangle list, ignoring
  orientation for this incidence check. It does not audit the rest of the
  mesh boundary or prove that the mesh bounds the formal solid.
- Applies all 48 signed cubic frames. Enumerates candidate integer shifts
  by equating opposing face centers; rejects overlapping carrier cells and
  compares the entire eight-feature profile on every shared panel.
- Only then reads the claimed atlas and compares the complete sets.

| Relative frame | Disjoint face-contact placements | Complete profiles match |
|---|---:|---:|
| Proper | 1,194 | 44 |
| Improper | 1,194 | 0 |

All 44 reconstructed poses equal the release's atlas exactly. The earlier
coordinate comparison then identifies these with our certified grid contacts.
Completeness here is over integer shifts and cubic frames: any face contact
equates two face centers, so its translation occurs in this enumeration.
This does not assert that arbitrary Euclidean placements have those forms.
Nor does full-panel matching mean that every mismatched pair physically
overlaps: a mismatched interface may instead leave a gap.

## 2. The formal object agrees with the supplied geometry

[`check_chair44_lean_literals.py`](../audit/check_chair44_lean_literals.py)
parses the literal panel and mesh data in `Generated/CoreData.lean`. It
reconstructs features using the definitions inspected in `FiniteModel.lean`
and `LogicalSpineFoundation.lean`:

| Correspondence | Exact check |
|---|---:|
| Lean panels versus native panel CSV | 24 |
| Reconstructed feature bases, apices and signed coefficients versus JSON | 192 |
| Lean vertex array versus JSON | 2,138 |
| Lean triangle array versus JSON | 4,272 |

The half-width is `1/100` and the height unit `1/10000` throughout. This
closes a concrete data-correspondence concern. The formulas were transcribed
from inspected, hashed Lean source; the Python program is not a Lean parser
or elaborator and does not prove their surrounding analytic properties.

The deeper source review followed the concrete tent solid `Q` through
generic edge partners, whole-feature partners, feature rigidity, the finite
mate census and registered mates. No hidden grid premise or concrete defect
was found in that bounded inspection. Actual `Tiling Q` supplies coverage and
disjoint interiors. We did **not** cold-build Lean, reproduce its axiom audit,
or audit every analytic lemma. Statement scope, data agreement and proof
correctness remain distinct questions.

The separate [source-review memo](CHAIR44_FORMAL_SOURCE_AUDIT.md) records the
specific definitions, intermediate interfaces and remaining analytic leaves.

## 3. Bijection of the legal grid models

This is a written consequence of exact contact equality, stronger than
similarity of substitution pictures. It is not yet a theorem connecting the
two Lean libraries.

Let `e=(1,1,1)`, let `P(x,y,z)=(y,z,x)`, and set `A(x)=P(x-e)`.
Write `B_t` for their carrier and `B_o` for ours. Then `A(B_t)=B_o`.
For each proper grid placement `g(x)=Rx+t`, define

```text
Phi(g) = A g A^-1
R' = P R P^-1
t' = P(t + R e - e).
```

This gives an invertible map of proper grid placements and an invertible
map of unit carrier cells. It preserves composition:
`Phi(gh)=Phi(g)Phi(h)`. For any placement family `T`, let
`Phi(T)={Phi(g):g in T}`. Then:

1. Carrier coverage and unique cell ownership are preserved, because `A`
   bijects the grid cubes and maps each placed carrier to its counterpart.
2. Face adjacency is preserved. The relative pose of the transformed pair
   is `Phi(g^-1 h)`, and the entire legal atlas transforms to our atlas.
   Therefore every shared panel matches on one side exactly when it matches
   on the other. Nonadjacent pairs have no interface obligation.
3. The inverse transformation gives the converse. Thus the sets of **all**
   legal proper grid tilings are in bijection, including any tilings not
   obtained from a particular substitution seed.

The feature-position reparameterization and signed-key permutation do not
assert congruence of the solids. They identify the matching rules, whose
complete contact relations are independently checked above.

Translations transform by `v -> P v`. Hence translation periods, or their
absence, correspond. More generally the stabilizers of the **decorated
placement families** are conjugate under `A`. This latter statement concerns
the grid representation; identifying it with the unlabelled physical tile
symmetry group requires the respective geometric registration and absence
of self-isometries.

The eight-child rule also corresponds. A doubled parent uses
`A_2(x)=P(x-2e)`, so a child pose transforms by `A_2 g A^-1`, with translation
`P(t+R e-2e)`. These are exactly the eight compared child poses. The analogous
formula at level `n` uses `A_(2^n)(x)=P(x-2^n e)`. The shift of origin with
scale must be accounted for; simply reusing the fine-pose formula for child
positions gives the wrong offsets.

## 4. Which proof steps are shared, and which differ?

| Step | Our development | Chair44 release |
|---|---|---|
| Local finiteness | Disjoint equal interior balls | Same argument |
| Acquiring a feature partner | Finite closed cover gives an open cap coincidence | Generic edge sectors force complementary feature edges |
| Extending to the full feature | Polynomial continuation and intrinsic five-line arrangement | Connected edge graph, solid-angle bound and finite disjoint closed cover |
| Recovering a frame | Ordered cap axes determine one frame | Square pyramid retains eight planar symmetries |
| Enforcing integer proper placement | Anchored offsets cancel; signed-key handedness fixes determinant | Finite companion census and forced-third-partner collisions |
| Covering the carrier grid | The partner owns the outward adjacent cube; propagate | Same after the census establishes registration |
| Unique grouping | Six trigger implications and notch owner | 33 first shells, central completions and 28 parent conflicts |
| Legal deflation | Exact contact recurrence and common parity | Same mechanism |
| Excluding periods | Halving plus strong induction on an integer norm | Halving tower and intersection of `2^n Z^3` |
| Full physical symmetry bound | Written argument; not yet in our Lean development | Claimed formal theorem, bound 24 |

Our simpler grouping proof is an implementation of the recognition mechanism
in Goodman-Strauss's 1999 chair work; see [the attribution](../MOTIF_GROUPING.md).
It is a useful proof presentation difference, not a new conceptual parent rule.

The two single-feature candidate counts measure different geometric
ambiguities. Our 1,536 opposite-key cap pairs determine 86 distinct necessary
integer, proper poses. These are not all legal whole-chair contacts. Their
square pyramids yield 6,862 eighth-grid candidates; 1,545 collide immediately,
and a further 5,273 are rejected with forced companions, leaving 44. The
manuscript records 299,975 option-collision witnesses. This turn reconstructed
the final registered atlas, **not** that entire off-grid companion census.

Both proofs also keep the existence obligation separate from forced
hierarchy. Our written existence route uses expanding patches, recentering and
a diagonal subsequence; our Lean theorem still assumes `LegalTiling`. Their
release includes an existence theorem. Neither unique parenthood nor matching
contact counts alone establishes that an infinite tiling exists. A hierarchy
also need not imply that one tile's ancestors exhaust space.

## 5. An attributed simplification of our geometric argument

The following is adapted from Chair44's alternative formal proof of component
coverage, described in `paper/tex/sec5_registration.tex:123` and implemented
in `lean/R44/R44/Proved/CarrierCoreCover.lean:72`. It shortens the route after
Section 6 of our [geometric scrutiny](GEOMETRIC_GRID_SCRUTINY.md).

### General retained-core lemma

Suppose a packing by congruent solids has a subfamily whose unit-grid carrier
cubes cover space. Suppose every such owned cube contains its inset closed
cube `[rho,1-rho]^3` in the **interior** of its physical owner. Suppose every
tile has an open interior ball of radius `r`, and `sqrt(3) rho < r`.
Then every tile of the packing belongs to the subfamily.

**Proof.** For any tile `T`, choose the center `c` of its interior ball.
Choose a carrier cube `a+[0,1]^3` of a subfamily tile `S` containing `c`.
Clamp each coordinate of `c` into `[a_i+rho,a_i+1-rho]`, producing `y`.
Each coordinate moves at most `rho`, hence
`||y-c||^2 <= 3 rho^2 < r^2`. By the retained-core assumption, `y` is in
the interior of `S`; by the ball bound it is in the interior of `T`.
Disjointness of tile interiors forces `S=T`. This holds for every tile.

### Applying the lemma to our caps

The normal displacement of every cap is at most

```text
h = 12 (1/4096) (1 + 1/5 + 1/7) = 141/35840.
rho = 1/64,       r = 1/4.
h < rho < 1/2,   3 rho^2 = 3/4096 < 1/16 = r^2.
```

All feature base planes of a registered component lie on integer coordinate
planes. A point in an inset cube is at least `rho>h` from all those planes,
so has an open neighborhood inside its own carrier cube unaffected by any
cap's addition or removal. It is therefore in the physical tile's interior.
The radius-`1/4` interior ball was already established in our solid.

Our Section 6 proves that the cap-connected component owns every grid cube.
The lemma now shows that every actual tile belongs to this component.
**Only then** does the original tiling's coverage imply that the component's
physical solids cover space. No assumption of physical component coverage is
hidden in the proof.

For the registration implication, this replaces the larger global
feature-box coverage argument and subsequent second-component exclusion.
It does not construct a tiling from a carrier covering, and it does not
remove the solid-definition or interface-realization obligations needed for
existence. Local feature separation still has those uses.

This is a written adaptation with exact rational bounds, not a new Lean
theorem. The source and the attribution should remain attached to it.

## 6. Validation, limits and next target

All new Python work used `uv` and the standard library. The coordinator
implemented the geometric atlas reconstruction; separate subagents inspected
the two geometric arguments and the formal object/companion chain. The
geometry reviewer also reviewed the new atlas enumerator. These are AI
reviews, not human expert review. No released implementation was executed.

From our repository root, with `RELEASE` below replaced by the path to the
extracted pinned release:

```sh
uv run --locked python strong/audit/reconstruct_chair44_contacts.py \
  --release-root RELEASE --output strong/audit/chair44_reconstructed_contacts.json
uv run --locked python strong/audit/check_chair44_lean_literals.py \
  --release-root RELEASE --output strong/audit/chair44_lean_literals.json
```

Results: [reconstructed contacts](../audit/chair44_reconstructed_contacts.json)
and [literal correspondence](../audit/chair44_lean_literals.json). Each records
input hashes. The latter also hashes its checker and explicitly marks the
manually inspected formula boundary.

Negative controls changed one claimed atlas translation and, separately,
one pyramid apex coordinate. The corresponding checker rejected each and
wrote no success report. Exact `Fraction` arithmetic also verified the
retained-core inequalities displayed above. Report links and source hashes
were checked; no frozen design or Lean source changed.

The immediate next verification target is a clean reproduction of the
released Lean 4.31.0 / Mathlib 4.31.0 development and its final axiom audit.
Our Lean 4.34.0 toolchain cannot substitute for its pinned environment.
After that, independently replay the off-grid companion census and scrutinize
the analytic lemmas linking the solid to it. The present results strengthen
confidence in the shared finite system; they do not close those obligations.

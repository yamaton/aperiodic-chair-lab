# Proof dependencies and adversarial review questions

*16 September 2026. Preparation audit, not external validation.*

The [brief](BRIEF.md) states the proposed finite-symmetry theorem. This
record separates the mathematical implications from what the programs
establish. It also makes the existence argument more explicit. No new
counterexample or identified fatal gap was found in this preparation pass;
that is not evidence equivalent to an outside review.

For the later focused review of the arbitrary-placement-to-grid steps, see
[Geometric grid scrutiny](GEOMETRIC_GRID_SCRUTINY.md), including exact
face-owner checks and independent periodic-box enumeration.

## Dependency order

```text
exact solid, fixed-size interior ball, finite algebraic boundary patches
  -> local finiteness in any tiling
  -> open cap coincidence
  -> full cap frame and integral relative placement
  -> one-handed cap-contact components on grids
  -> a component occupies every grid cube and physically fills space
  -> every physical tiling obeys the finite grid matching rules
  -> local parent rule and unique grouping
  -> even macro offsets and recurrence of rules
  -> no translations and a finite full symmetry group

Separately: substitution contact closure + expanding interior balls
  -> existence of at least one infinite tiling.
```

The “separately” matters: forcing every possible tiling to be aperiodic
would be vacuous if there were none.

## A. Exact solid and regularity

In each feature box, use orthonormal coordinates
`x=p+w*u*e_u+w*v*e_v+s*n`, with `|u|,|v|≤1`, `|s|≤h`,
`w=1/64`, and `h=141/35840`. Replace the original condition `s≤0` by
`s≤k*δ*φ(u,v)`, where `δ=1/4096`. Outside these boxes retain the coarse
chair. The graphs equal zero on square edges, so the prescriptions agree
there; the conservative height bound puts them inside the boxes.

The polynomial factor `1+u/5+v/7` is strictly positive on the square.
Positive keys add outward columns, negative keys remove inward columns.
No modification reaches a cube's middle half. Adjacent cube cores connect
through unchanged internal faces, and each added column attaches to the
body. This supplies connected interior, regular closedness, and a fixed
interior ball. The signed volume correction is
`w² δ (16/9) Σk = 0`.

**Checked:** exact key sum, integral, coordinate bounds, and box separation.
**Written:** these facts imply the asserted topological properties of the
piecewise defined solid. A reviewer should check seams and the inward-side
convention, not assume the rendered mesh is the definition.

## B. Open coincidence and frame rigidity

Use a uniform scaling in all three coordinates to get `z=Hφ(u,v)`.
The ambient defining polynomial is irreducible because it is monic and
linear in z. Restriction of a transformed equation to an open graph patch
vanishes identically as a polynomial in u,v, so the whole algebraic graphs
coincide. Comparing degree gives proportional defining equations.

Exactly five straight lines lie on that full graph: `u=±1`, `v=±1`, and
`1+u/5+v/7=0`, all in the base plane. They identify the square and its
center. The fifth line removes the square's nonidentity symmetries,
identifying ordered tangent axes. Its location outside the physical square
does not matter: continuation concerns the algebraic graph, not extra
physical material.

Local finiteness must precede the covering argument. A compact tile with
a fixed interior ball admits only finitely many congruent copies meeting
a bounded region in an interior-disjoint tiling. A cap is then covered by
finitely many neighboring closed boundary patches. These cannot all have
empty relative interior. Planar patches and seams cannot cover an open
part of a nonplanar cap; one neighboring cap coincides openly.

**Checked:** the line-classification coefficients and the square/fifth-line
stabilizer. **Written:** polynomial continuation, finite boundary coverage,
and the passage from local graph sides to opposite signed keys.

**Question:** is there a contact configuration omitted by this finite
closed-cover argument? A bounded periodic search cannot answer that question.

## C. Grid propagation without assuming the grid globally

One cap match gives equal ordered tangent axes, opposite base normals,
opposite keys, and translation `p_A-Rp_B=f_A-Rf_B` with integer entries.
The signed-key chirality table forces `det(R)=+1`, even when the initial
model allows improper isometries. Thus each cap-contact component has a
single cubic frame, integer coset, and handedness.

Each component tile contains the unmodified middle of every coarse cube
it owns. Two component tiles therefore cannot own the same cube. Every
exposed cube face has a cap whose matched neighbor owns the adjacent cube.
Closure under lattice adjacency makes the component own all grid cubes.

Coarse coverage alone does not complete the argument: pockets could leave
holes. Across each face all cap matches must belong to its unique opposite
coarse owner. Whole bounded cap matching, disjoint global feature boxes,
and complementary graph sides then fill every box and all the space outside
them. A second component would overlap the interior of this first one.

**Checked:** every opposite-key frame correspondence is proper and integral;
feature separation bounds are positive.
**Written:** ownership propagation and physical filling. These are the
highest-priority implications for outside review.

## D. Existence: explicit expanding balls and a compactness argument

Let the level-m coarse substitution patch have support `2^m L`.
It contains the cube `[-2^m,0]^3`. Its actual curved boundary differs from
the coarse support only in feature boxes of normal reach at most h on the
exposed boundary; all internal matching interfaces fill complementarily.
Consequently it contains the open ball centered at

```text
c_m=(-2^(m-1),-2^(m-1),-2^(m-1))
```

with radius `2^(m-1)-h`, for m≥1. These radii tend to infinity. Translating
by `-c_m` is an integer translation, preserving the finite orientation/grid
placement model.

Encode tile placements by occupancy bits indexed by `Z³ × {24 orientations}`.
Use a diagonal subsequence so that every finite set of bits stabilizes.
For any fixed bounded window, sufficiently large recentered patches cover
it and a margin larger than a tile diameter. Coverage and legal contacts
there depend on finitely many bits, so the limit satisfies both. This
constructs an infinite valid grid tiling and, by complementary interfaces,
an infinite tiling of the exact solid.

**Checked:** the eight-child coarse partition and closure of all contacts
under substitution. **Written:** the growing-ball estimate and compactness.
The proof does not require the curved boundary of a supertile to be a
scaled original boundary, or nested recentered patches.

## E. Grouping, recurrence, and representation of physical orientations

The [Lean milestone](../../formal/README.md) formalizes normalized-grid
macrocontact recurrence and its exhaustive enumeration. Consult its current
validation status; it does not formalize grouping or iteration for all tilings.

The [local parent proof](../MOTIF_GROUPING.md) proves unique grouping in
the common grid. Its six trigger implications use finite enumeration of
contacts and forced face coverage. An independent star computation agrees,
but is not a premise of the new implication proof.

Grouping alone does not force recurrence: the 6,801 macrocontact test
includes all integral fine-grid offsets, including odd offsets. The 44
fitting contacts are exactly twice the 44 fine contacts. Face connectivity
puts all parent centers in one coset of `2Z³`. Deflation repeats the
abstract matching system.

A physical tile must not have an unaccounted self-isometry identifying two
states. Open planar patches identify coordinate axes and their plane levels
`{-1,0,1}`, forcing a self-isometry's translation part to vanish. The finite
48-frame check finds only the identity preserving the decorated solid.
Thus the orientation-sensitive parent rule is intrinsic to physical tile
placements, rather than to an arbitrary choice of labels.

**Checked:** all contact sets, local implications, macro offsets, and keyed
frame stabilizer. **Written:** applicability to every infinite tiling,
connectivity of the grouped face graph, and iteration without a hidden
global alignment assumption.

## F. Periods and screws

Once grouping is unique and recurrent, any translation period belongs to
`2^m Z³` for every m and must vanish. A tile-preserving isometry permutes
the three globally common planar normal axes, so its linear part lies in
the finite signed-permutation group. Two symmetries with the same linear
part differ by a translation. Absence of nonzero translations therefore
makes the whole symmetry group finite, excluding infinite-order screws.

This is a written implication, not the outcome of searching a bounded list
of screw motions. It does not assert that every stabilizer is trivial.

## Novelty assessment is a separate dependency

Goodman-Strauss already supplies the chair and hierarchy, marked recutting,
and a two-tile realization. General substitution-enforcement methods are
also older. The item to compare is the particular **one congruence class**
of oriented chair patterns and its exact solid realization. Failure to find
it in a search is not proof of priority. An equivalent encoding or a known
obstruction would materially change the assessment.

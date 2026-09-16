# Frozen recut-chair audit

*15 September 2026. Internal audit, not external mathematical review.*

**Result:** a separate implementation from explicit coordinates reproduces
the finite hierarchy certificates. Exact local cap checks also pass. The
written geometric argument has been expanded below to expose its assumptions
and intermediate steps. This audit found no counterexample or unresolved
logical gap in that argument; this is a report of the audit, not a claim of
independent mathematical acceptance or novelty.

The subsequent [three subagent reviews](SUBAGENT_REVIEWS.md) found no
substantive defect, requested three clarifications now incorporated below,
and supplied an additional independent finite cross-check. These are AI
reviews, not external human endorsements.
The separate [literature review](LITERATURE_REVIEW.md) identifies close
predecessors and the concrete differences needing an expert comparison.

**Subsequent extension, 16 September:** the [follow-up record](../FOLLOWUP_REFLECTIONS.md)
extends the proposed claim to reflected copies by a single-cap handedness
invariant, with a separate 48-orientation checker. It also reduces the
description to three face motifs and supplies a periodic altered-solid
control. The original frozen snapshot and the proper-copy audit below
remain unchanged. See the [current review note](../REVIEW_NOTE.md).

The later [local parent proof](../MOTIF_GROUPING.md) derives unique grouping
from A/B/C faces and arrows. Its checker imports no project implementation,
reconstructs the frozen ports from motifs, and independently reproduces
the 33 stars. The grouping proof itself uses local face propagation instead
of the star enumeration. Run `uv run --locked python strong/audit/motif_grouping.py`.

## 1. What is frozen

- [Candidate](frozen_v1/candidate.json): seven coarse cubes, 192 signed ports,
  their rational positions and ordered frames, the polynomial, its scale,
  and eight explicit child placements.
- [Archived proposal](frozen_v1/proposal.md): the proposal before this audit.
  Its relative links retain the original `strong/` context.
- [Manifest](frozen_v1/manifest.json): hashes of those files and the original
  implementation sources. The source hashes record provenance; those
  implementations are not inputs to the new checkers.

Candidate SHA-256:

```text
95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54
```

The snapshot contains construction data, not assumed contact tables or
claimed enumeration counts. `freeze.py` refuses to replace an existing
snapshot. A changed candidate should get a new version.

### Proposed theorem to review

Let `T` be the regular closed solid specified by the frozen data: the
seven-cube chair with each specified face square replaced by its signed
polynomial graph. Allow translated and properly rotated copies of **one
physical handedness**. A tiling covers all of Euclidean three-space with
pairwise disjoint tile interiors.

The proposed claim is:

1. `T` is compact, has connected interior, and has volume 7.
2. At least one such tiling exists.
3. Every such tiling has a finite group of isometries preserving its tiles.
   In particular, it has no nonzero translation or infinite-order screw.

This original audit statement concerns the exact curved solid and proper
copies. Reflected copies are handled by the subsequent extension linked
above; triangulated approximations remain outside the proposed theorem.

## 2. Reproduce the audit

From the repository root, use the existing locked environment:

```sh
uv run --locked python strong/audit/verify_from_coordinates.py
uv run --locked python strong/audit/verify_caps.py
```

The first script uses only the Python standard library. The second uses
SymPy for polynomial identities. Neither imports the original search or
geometry code, and neither reads its generated contact tables.

Both were written by the same assistant that developed the candidate.
Separate implementation reduces shared-code risk; it does not supply an
independent researcher, a proof-assistant formalization, or external review.

### Finite hierarchy results

| Check | Regenerated result |
|---|---:|
| Proper cube rotations | 24 |
| Proper coarse-chair / keyed-chair symmetries | 3 / 1 |
| Geometric directed face contacts | 1,194 |
| Compatible contacts | 44 |
| Closed substitution contact language | 30 |
| Complete local neighborhoods | 33 |
| Nodes in exhaustive neighborhood search | 105 |
| Neighborhoods forcing membership in an eight-chair group | 33 |
| Incompatible pairs of competing group roles | 28 of 28 |
| Geometric macro contacts, including odd offsets | 6,801 |
| Compatible macro contacts | 44 |
| Compatible macro offsets all even | Yes |
| Deflated contact set equals the original set | Yes |

The checker generates rotations by quarter turns, transforms each cube
through its eight corners, derives exposed faces from occupancy, and
compares explicit port dictionaries. It assembles the macro boundary by
cancelling internal faces. Its complete neighborhood search is an exact
cover backtracking search, with the whole search tree recorded.

[Results](coordinate_verification.json) and
[finite certificates](coordinate_certificate.json) include the candidate
hash. The certificates record actual matrices and translations, local
neighborhoods, forcing witnesses, and conflicting tiles for all 28 role
pairs. A reviewer can regenerate them without trusting the synthesis.

### Local cap results

| Check | Result |
|---|---:|
| Opposite-key correspondences with compatible proper frames | 1,536 |
| Distinct relative placements from these correspondences | 86 |
| Noninteger translations among those placements | 0 |
| Maximum absolute height bound | 141/35840 |
| Minimum clearance from a port square to its unit-face edge | 19/64 |
| Bounding boxes of distinct features disjoint | Yes |
| Stabilizer of square plus fifth line | Identity only |
| Signed volume correction | 0 |

The 86 placements are possible **single-port** matches. Some overlap other
parts of the chairs or fail other ports; this does not conflict with the
44 legal whole-chair contacts. See [cap results](cap_verification.json).

### Controls that should fail or admit periods

1. **Erase all keys.** The coarse chair tiles by translations in the kernel
   of `q ↦ q_x+2q_y+4q_z (mod 7)`. Its seven cubes represent all seven
   residues. The new checker accepts the resulting periodic contacts.
   A subsequent [direct physical check](LITERATURE_REVIEW.md#6-figure-2-and-the-ordinary-chairs-periodic-tilings)
   shows why that periodic arrangement fails with the actual curved ports,
   including an explicit interior-overlap point.
2. **Swap two different positive keys.** Volume stays 7, but four contacts
   needed by the original substitution fail. This breaks that certificate;
   it does not prove that the modified shape cannot tile by another method.
3. **Forget the ordered tangent frame.** Opposite keys and normals alone
   admit 4,360 distinct noninteger local placements, even using just cube
   rotations. These are local ambiguities, not verified whole tilings.
4. **Make the polynomial's two linear coefficients equal.** Swapping the
   two square axes becomes a symmetry. The actual unequal coefficients
   eliminate this ambiguity.

## 3. Geometric audit, with the missing details made explicit

These are mathematical arguments. The scripts verify supporting identities
and finite arithmetic; they do not automatically prove this section.

### A. The physical scale preserves the rigidity argument

Write the cap as

```text
p + w u e_u + w v e_v + k δ φ(u,v) n,
w=1/64, δ=1/4096.
```

Use orthonormal local coordinates and divide **all three ambient
coordinates** by `w`. This is a uniform similarity, so conjugating an
isometry still gives an isometry. The normalized graph is

```text
z = H φ(u,v),     H=kδ/w=k/64 ≠ 0.
```

Scaling only the tangent coordinates would not justify an argument about
Euclidean isometries. The original proof left this normalization implicit.

### B. An open coincidence identifies the entire algebraic graph

For `P_H(u,v,z)=z-Hφ(u,v)`, divide any polynomial by this monic polynomial
in `z`. The remainder is a polynomial in `u,v`. If an isometry makes an
open patch of two graphs coincide, substituting the first graph in the
transformed second equation makes that remainder vanish on an open subset
of the plane. It therefore vanishes identically.

Thus the first defining polynomial divides the transformed second one.
Both have total degree five, unchanged by an invertible affine isometry,
so the quotient is a nonzero constant. The whole algebraic surfaces agree.
This justifies continuation beyond the bounded physical patch; it does not
assume that the unbounded surface is part of the tile.

### C. Exactly five lines recover the local frame

Substitute `(u,v,z)=(x+dt,y+et,c+ft)` in the graph equation. Since `H≠0`,
the coefficient of degree five forces

```text
d²e²(d/5+e/7)=0.
```

If `d=0,e≠0`, the cubic coefficient forces `x=±1`. If `e=0,d≠0`, it
forces `y=±1`. Otherwise `e=-7d/5`, and the quartic coefficient forces
`1+x/5+y/7=0`. In each case the whole right side vanishes, giving a
horizontal line in `z=0`. The case `d=e=0` cannot describe a nonconstant
line on a graph. These exhaust all straight lines on the surface.

The resulting arrangement consists of two parallel pairs bounding a square
and a fifth line. An isometry must preserve the two parallel pairs as a
set, so it preserves the square and its center. The fifth line's positive,
unequal coefficients eliminate every nonidentity symmetry of the square.
Consequently the isometry fixes the ordered tangent axes and base center.
Its only remaining choice is the sign of the perpendicular direction;
the height coefficient must have equal magnitude.

Matching the normalized graph therefore also matches the **entire bounded
cap square**, because its domain is the same square recovered by the lines.

### D. Every cap has an open cap match

First justify local finiteness without assuming a grid. The compact tile
has diameter bounded by a constant and contains an open ball of fixed
radius. Tiles meeting any bounded set have their chosen interior balls in
a larger bounded set. Those balls have disjoint interiors, so there are
only finitely many such tiles.

Let `x` lie on the interior of a cap patch. Approach `x` through points
outside its tile. Since the tiling covers space and is locally finite,
some other closed tile contains a subsequence and hence contains `x`.
It cannot contain `x` in its interior: every neighborhood of `x` meets
the first tile's interior. Thus the other tile contains `x` on its boundary.
The same argument applies to every point of the cap.

Inside a smaller open cap patch, only finitely many other tiles can
participate. Each boundary has finitely many closed plane or polynomial
patches and seams. These give a finite relatively closed cover of the cap.
If every intersection had empty relative interior, they could not cover
an open cap patch. At least one intersection therefore contains an open
cap subset. It cannot come from a seam, which has dimension at most one,
or a plane, since `φ` is not affine on any open set. It comes from a
neighboring cap, giving the open coincidence in B.

For the polynomial step, the relevant condition is that the polynomial's
**pullback to the parametrized cap is not identically zero**: such a
pullback cannot vanish on an open set. Merely being a nonzero polynomial
in ambient space is insufficient; the cap's own equation is a counterexample
to that imprecise wording in the first audit.

This explicitly rules out covering a cap solely by isolated contacts,
curves, or finitely many flat facets. Local finiteness rules out an infinite
accumulation of ever smaller contact pieces from different tiles.

### E. Opposite interiors determine the sign and grid placement

On an open coincident graph, the two regular solids must occupy opposite
local sides. Once the tangent frame is fixed by C, the two possible base
normals have opposite signs. Equal base normals would give the same inward
side and an interior overlap. Therefore `Rn_B=-n_A` and `k_B=-k_A`, while
`Re_u,B=e_u,A` and `Re_v,B=e_v,A`.

The frame map is explicitly

```text
R = e_u,A e_u,Bᵀ + e_v,A e_v,Bᵀ − n_A n_Bᵀ.
```

Its entries are signed coordinate permutations. Restrict to determinant
`+1` for the proposed one-handed convention. The translation obeys

```text
t = p_A−Rp_B = f_A−Rf_B ∈ Z³.
```

The port offsets cancel exactly. The last assertion follows because the
two face centers have integer normal coordinates and half-integer tangent
coordinates on the same coordinate axes. Their entire unit faces agree,
with opposite outward normals. The face's owning coarse cube is then on
the opposite side; this follows from how exposed faces were defined.

### F. A connected component of matched tiles fills space

Join tiles whenever they share one of the open cap matches above. In one
component, composing E gives a common cubic frame and one integer-grid
coset. Two component tiles cannot own the same coarse cube: each contains
that cube's unmodified middle half, causing an interior overlap.

Consider any occupied cube and any adjacent cube. If the adjacent cube
belongs to the same chair, it is already occupied. Otherwise their shared
face is an exposed face of that chair. It has ports, and D supplies a cap
match. By E the matched tile lies in the same component and owns the
adjacent cube. The occupied cells are thus closed under lattice adjacency.
Since the cubic lattice is connected, this component owns every cube.

Across a particular exposed unit face, every cap's matching tile must own
the same adjacent cube. Coarse ownership is unique, so all these matches
belong to the same neighboring chair. By C each match is of the entire
bounded cap. All the other portions of the face remain flat.

To justify physical filling throughout the grid, enclose each feature in
its tangent square times the normal interval `[-h,h]`, where
`w=1/64`, `h=141/35840`, and its face-edge clearance is `m=19/64`.
The eight-center pattern is invariant under square symmetries, so these
boxes occupy the same locations on every unit grid face. Distinct feature
locations have strictly positive separation:

| Location of two features | Gap in a separating coordinate |
|---|---:|
| Same unit face | At least `1/8−2w = 3/32` |
| Different coplanar unit faces | At least `2m = 19/32` |
| Distinct parallel grid planes | At least `1−2h = 17779/17920` |
| Perpendicular grid faces | At least `m−h = 10499/35840` |

For the last case, one feature stays at least `m` from every integer
coordinate plane perpendicular to its own face, whereas the perpendicular
feature lies within `h` of one such plane. Opposing matched features
occupy the same box; these are the intended exception.

Outside the boxes, the physical tiles agree with the complete coarse-cube
partition. Inside each box, only its two opposite coarse owners participate,
and their matching graph inequalities occupy complementary closed sides.
Thus they fill the box, including its boundary. This proves physical
coverage without leaving holes near seams or edges.

A second component has an open interior ball. The first component already
fills that ball, and its locally finite union of boundaries has empty
interior. The ball would therefore overlap a tile interior from the first
component. This is impossible. All tiles belong to the one grid component.

## 4. From the finite calculations to strong aperiodicity

The following implications still require reading the combinatorial
argument, rather than treating counts as a proof:

1. **Existence:** the eight coarse children partition `2L`. Substitution
   closure verifies every new face contact. Features away from edges cannot
   create additional interactions between coarse edge-only neighbors.
   Iterated patches contain larger and larger interior balls. Translate
   those balls to a fixed origin and use a diagonal subsequence in the
   finite-state grid placement space to obtain an infinite valid tiling.
2. **Forced grouping:** every actual complete neighborhood is among the
   enumerated 33. Each certificate either supplies a central group directly
   or forces a neighboring central group containing the anchor. Enumeration
   may include nonextendible neighborhoods; including them only strengthens
   the universal check.
3. **Unique grouping:** any chair's eight possible child roles determine
   eight possible parent placements. Every pair of distinct roles has an
   explicit overlap or mismatch witness. Thus complete groups partition
   the tiling uniquely.
4. **Recurrence:** macrocontacts are enumerated at every integer fine-grid
   offset allowed by their bounds, including odd offsets. Every compatible
   offset is even, and deflation gives exactly the original 44 rules.
   Connectivity of the macro face graph puts all centers in one coset of
   `2Z³`. This repeats the abstract matching system; the grouped curved
   boundary need not be a scaled copy of a single tile.
5. **No translation:** intrinsic grouping preserves any translation
   symmetry. Repeated deflation forces its vector into every `2^m Z³`,
   whose intersection is `{0}`.
6. **Finite full symmetry group:** the tile's open planar boundary patches
   identify three perpendicular normal axes. Any tiling symmetry must
   permute those axes, so there are at most 48 possible linear parts,
   even if orientation-reversing symmetries are counted. Two symmetries
   with the same linear part differ by a translation. Since none is
   nonzero, there are finitely many symmetries and no infinite-order screw.

The separate checker also confirms that the key pattern destroys the
coarse chair's nonidentity proper symmetries. Distinct oriented states in
the finite computation are therefore distinct physical tile placements.
There is no additional self-isometry with a displaced center: the open
planar patches identify the three coordinate axes. The planes containing
those patches occur at levels exactly `{-1,0,1}` along each axis. Preserving these three-level
sets forces the translation part to be zero. The tile's proper stabilizer
therefore reduces to the cube rotations already checked.

## 5. What to hand an outside reviewer

Start with the frozen candidate, this audit, the two short verification
programs, and the [active proposal](../RECUT_CHAIR.md). The STL and viewer
are illustrations; they are not the defining construction.

Ask the reviewer to try to break these specific claims:

1. Does open coincidence of these polynomial caps necessarily identify
   the bounded cap's center and full frame under an arbitrary isometry?
2. Does D cover every possible non-face-to-face tiling contact?
3. Does the coarse ownership argument in F preclude a second unlocked
   component or an unfilled region near a seam?
4. Are the neighborhood enumeration and its forced-central-neighbor
   implication complete? Are all eight roles handled without imposing
   an extra global assumption?
5. Does exact macro rule recurrence justify unbounded unique deflation?
6. Under which conventions about reflections and strong aperiodicity
   should the proposed result be stated, and how does it relate to the
   existing three-dimensional chair literature?

**Remaining work:** external mathematical review and literature comparison.
No reviewer has been contacted by this audit, and no novelty claim follows
from its computational results. Simplifying the shape or replacing exact
curves with finite planar features would be a separate construction problem.

### Literature checkpoints

A targeted search on 15 September 2026 provides context, not an exhaustive
priority search:

- The authors' [hat proof, Section 4 and Appendix A](https://strauss.hosted.uark.edu/distribution/papers/einstein.pdf)
  separately verifies neighborhood enumeration by backtracking and justifies
  the underlying grid assumption. Its treatment also explains why including
  nonextendible neighborhoods can be safe. These are methodological precedents
  for the audit, not a proof of the present chair.
- Kaplan's [2025 survey](https://arxiv.org/html/2509.12216v1), in its closing
  discussion of aperiodicity, distinguishes the SCD screw symmetry from the
  stronger three-dimensional target. That dated discussion does not establish
  the literature's complete status today.
- Goucher's [2013 construction account](https://cp4space.hatsya.com/2013/08/26/a-more-aperiodic-monotile/)
  explicitly retains screw symmetry. Removing translations in a different
  3D construction is therefore insufficient for comparison with this claim.

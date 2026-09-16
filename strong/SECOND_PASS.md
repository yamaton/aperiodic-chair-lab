# Second pass: constrained twists and cluster fusion

**No strongly aperiodic monotile was found.** This pass adds a complete
11,072-design matching family and tests a concrete way to combine an existing
strongly aperiodic pair into one block. It uses `uv` throughout.

Across both passes, **65,216 designs have been analyzed**: 22,132 admit
explicit periodic tilings and 43,084 cannot tile the prescribed cubic grid.
Of the new designs, 512 are excluded by their previously checked, less
restrictive matching models. They did not need another solver call.
The grid exclusions do not classify arbitrary Euclidean placements.

## 1. A genuinely different interface

The earlier dipole family fixes the direction of a tab/pocket pair but leaves
its midpoint at the face centre. This family moves the midpoint sideways,
constraining the neighboring block's twist as well.

Start with a 32-unit cube. On each face select perpendicular signed tangent
directions `a` and `b`. There are eight choices. Put two 2×2 ports at

```text
tab centre:     face centre + 6b + 6a
pocket centre:  face centre + 6b − 6a
```

Each port has depth one. Both stay away from the edges. The core remains
connected. The triple `(key, a, b)` in the data uses directions
`0…5 = +x, −x, +y, −y, +z, −z`; this complete run uses only key zero.

Opposing aligned faces fit exactly when their arrows `a` are opposite and
their offsets `b` are equal. These conditions follow from the actual two port
positions; there are no painted labels or assembly instructions.

The 24 proper rotations act on all six faces together. Burnside's counting
formula independently verifies the enumeration:

```text
(8⁶ + 6·8³ + 8·8²) / 24 = 11,072.
```

The terms count the identity, six half-turns about opposite edge midpoints,
and eight third-turns about body diagonals. The other rotations fix no full
assignment of these oriented interfaces.

### Results

| Verdict | Designs |
|---|---:|
| Periodic 2³ certificate | 1,632 |
| Periodic 3³ certificate | 112 |
| Periodic 4³ certificate | 3,436 |
| Periodic 8³ certificate | 8 |
| Oblique periodic certificate | 16 |
| No open 3³ patch, directly checked | 5,324 |
| No open 3³ patch, inherited from the coarse model | 512 |
| No open 5³ patch | 24 |
| No open 7³ patch | 8 |
| **Total** | **11,072** |

The listed repeat sizes are certificates, not claims of minimal periods.
The first pass through this family left 32 cases unresolved. Refinement
found 16 oblique repeats, eight cubic 8³ repeats, and eight impossible 7³
open patches. Timeouts remain recorded as `unknown` in intermediate checks.

## 2. Searching for slanted repeats directly

Checking only cubic boxes is inefficient: a small fundamental region can
have slanted sides. The new solver works on integer-lattice quotients with
column bases in Hermite normal form:

```text
(a,0,0), (b,c,0), (d,e,f),
a,c,f > 0; 0 ≤ b,d < a; 0 ≤ e < c.
```

The repeat region contains `acf` cells. There are 1,325 such lattices with
index at most 12. The refinement enumerates them until it finds a witness,
or exhausts that bounded list, then tries larger cubic SAT problems.

An important implementation detail: an oblique quotient need not survive
a cube rotation. Consequently its solver **does not fix the origin block's
orientation**. That otherwise tempting optimization could lose solutions.

One rejected shape has faces, ordered +x, −x, +y, −y, +z, −z:

```text
(0,2,4), (0,2,5), (0,0,5), (0,4,0), (0,0,2), (0,2,0).
```

A certified tiling repeats along

```text
(3,0,0), (0,4,0), (0,1,1).
```

Their determinant is 12. Exact voxel coverage of this oblique fundamental
region checks **393,216 voxels**, each covered once. This is a physical
periodic tiling, so it rejects the shape even without a theorem forcing
arbitrary tilings to align with the grid.

Independent verification also checked 8,856 returned patch/torus certificates
and 1,887,600 directed neighbor interfaces using geometric height profiles.
Twenty-one sampled cases were rechecked with an unanchored Z3 model and
independently generated rotation matrices. The quotient graphs were checked
for inverse and commuting translation steps.

## 3. Can an existing hierarchical pair be fused into one block?

Goodman-Strauss's construction uses a modified 3D chair and filler pieces;
its hierarchy excludes infinite-order symmetries. In three dimensions the
paper also gives a two-piece version using a cross-shaped filler `X`.
See [the original paper](https://doi.org/10.1006/eujc.1998.0282), especially
§§2–5 ([PDF](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Goodman2.pdf)).

The following volume calculation is our test of a fusion strategy, not a
claim that the paper supplies a monotile.

Write `L₀` for the unmodified chair, a 2×2×2 cube with one unit corner cube
removed. Its volume is seven. The paper's thin double-ended filler `I`
has square cross-sections with half-width `min(1/4, |x|)`. Thus

```text
vol(I) = 2[ ∫₀^(1/4) 4x² dx + ∫_(1/4)^1 1/4 dx ] = 5/12.
vol(X) = 3 vol(I) = 5/4.
```

The modified chair gains one octant of `X` at its inner corner and loses
seven octants at its outer corners:

```text
vol(L) = 7 + vol(X)/8 − 7 vol(X)/8 = 97/16.
```

These are the base shapes before replacing surface markings with bumps.
Matching bumps can be chosen as complementary volume transfers. The fusion
test concerns groups of the original marked pieces.

The associated coarse chairs tile space and each occupies volume seven.
Boundary errors vanish in the density calculation because all pieces have
bounded size. The required mean filler count per chair is therefore

```text
X pieces per L = (7 − 97/16) / (5/4) = 3/4.
```

**Necessary condition:** if each proposed identical block is a rigid union
of `m` whole `L` pieces and `n` whole `X` pieces, then `n/m = 3/4`.
The smallest possible such inventory is **four chairs plus three crosses**.
Attaching an integer number of whole fillers to just one chair cannot work.
For the `I` version, the corresponding minimum is four chairs plus nine `I`s.

### Testing that smallest inventory

First ignore the crosses and their markings: congruence of the coarse chair
clusters is a prerequisite for a fusion that preserves this decomposition.

- A first-level supertile contains eight chairs. All 35 unordered splits
  into two groups of four fail congruence, even allowing reflections.
- A second-level supertile contains 64 chairs. It has 3,173 face-connected
  four-chair placements, falling into 255 classes under proper rotations.
- Only three classes can reach every chair somewhere. None can cover all
  64 chairs by disjoint copies. An independent Z3 exact-cover formulation
  confirms all three exclusions.
- A second enumeration checked all `C(64,4) = 635,376` four-chair subsets
  to verify the connected-cluster count.

The second test permits clusters to cross first-level boundaries, but keeps
them inside the second-level boundary. **It does not exclude an infinite
fusion whose clusters cross that outer boundary**, disconnected coarse
clusters connected through fillers, accidental congruence that does not
preserve the chair decomposition, or cutting and redistributing pieces.

## 4. What remains worth pursuing

Neither the one-cell connector designs nor the tested whole-piece fusions
yield a candidate. A next construction needs freedom these tests omit:
clusters crossing larger hierarchy boundaries, or a new dissection that
builds state-carrying connectors into the large pieces themselves.

For such a candidate, three distinct obligations remain:

1. Construct an infinite space filling with one congruent solid.
2. Show that every tiling recovers the intended hierarchy or matching system.
3. Use that forced structure to exclude translations and infinite-order screws.

A large finite patch alone would satisfy none of these infinite claims.

## Reproduce this pass

The first-pass dipole catalogue is an input to the refinement enumeration.
All commands run from the project root:

```sh
uv run --locked python strong/offset_dipoles.py
uv run --locked python strong/refine_offsets.py
uv run --locked python strong/verify_offsets.py
uv run --locked python strong/chair_fusion.py
uv run --locked python strong/chair_clusters.py
uv run --locked python strong/summarize.py
```

Results: [combined summary](artifacts/research_summary.json),
[new geometric verification](artifacts/offset_verification.json),
[volume and first cluster test](artifacts/chair_fusion.json),
[larger cluster test](artifacts/chair_clusters.json).

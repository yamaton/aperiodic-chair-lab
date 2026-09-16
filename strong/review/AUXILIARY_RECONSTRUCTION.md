# Can the auxiliary markings be reconstructed locally?

*16 September 2026. Written arguments with exact finite witnesses; not
externally reviewed. The frozen candidate and v1 review packet are unchanged.*

## Answer and scope

The proposed direct identification encounters an obstruction, not merely a
missing lookup table.

**Forward:** there is no translation-equivariant rule with a fixed finite
radius that converts every tiling in our decorated substitution hull into
Goodman-Strauss's original marked `L/I` system **while retaining the same
coarse chair placements**. Two identical decorated neighborhoods require
different old arrows. Substitution enlarges the identical neighborhoods
without removing the conflict. This is a written all-radius argument,
with its initial witness and first three scales checked exactly.

**Reverse:** on the full old `L/I` space, no coarse-chair-preserving conversion
to our decorated system can commute with all proper cubic rotations. A
specific old tiling has a threefold symmetry fixing a chair; none of our
three decorations of that chair preserves it. This obstruction does not
even require locality. A translation-equivariant inverse using a fixed
coordinate frame is **not settled** by this argument.

These statements address the natural correspondence under discussion.
They do not exclude an unrelated conjugacy that changes the chair
placements, a nonlocal forward construction, or correspondences between
suitably restricted tiling spaces. They do not prove the proposed physical
monotile theorem or establish novelty.

There is also a separate **source-model discrepancy for the connected
`L/X₂` variant**. The transcribed geometry and markings give a small cavity
where every orientation of `X₂` is blocked. Section 5 records the witness
and assumptions for scrutiny; it must not be silently treated as a verified
correction to the published paper.

## 1. What is being compared

Source: Goodman-Strauss, *A Pair of Aperiodic Tiles in Eⁿ* (1999),
[published scan](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Goodman2.pdf),
[author preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).
The source basis is the marked-end definitions on p.389, grouping of `I`
pieces into crosses, the chain-filling argument in Lemma 4.3, and the
connected modification on p.394. Relevant scan pages were re-inspected.
The earlier [pair comparison](GOODMAN_STRAUSS_COMPARISON.md) supplies the
coordinate conventions. All deductions and witnesses below are our analysis.

A local conversion of radius r determines the output near a point by the
input within distance r, using the same rule at every translated point.
The radius must be uniform over all inputs. Knowing that a particular
arrow can eventually be found by walking along a chain is insufficient.

We first work with oriented coarse chairs and their A/B/C decorations on
the grid. Passing to our actual solid would require the existing proposed
geometric correspondence. Bounded feature sizes do not repair an
arbitrarily-large-neighborhood obstruction.

For the old recutting, a chair at `(c,R)` has notch direction `s=R(1,1,1)`.
Its marked square at `c+n`, with n a signed coordinate unit vector, has arrow

```
A(s,n) = (n·s) [s - (n·s)n].
```

An auxiliary cross at v has arm ends at `v±e_a`. Crosses at `v` and `v+2e_a`
meet at an end square. In the original `L/I` system, the `I` on each axis
carries a transverse diagonal arrow at both ends. Along a straight chain
that arrow must be constant. A chair at either end fixes it.

Cross locations themselves are local: collect outside corners of the
coarse chairs and remove locations occupied by chair inside corners.
For the interior witnesses below, all eight incident octants are outside
corners. Exact old-solid geometry is checked separately in Section 5.
The obstruction is in the markings, not locating these cavities.

## 2. Forward obstruction: an explicit pair of crosses

Let D be our decorated substitution and inspect `D³(L)` with the identity
root pose. Define

```
a = (-4, 0, -4),     b = (-4, 0, 4).
```

Both are complete cross cavities. At each point, the eight chairs owning
the eight incident unit cubes have origins at relative positions
`(±1,±1,±1)`. Their **full proper rotation matrices agree**, position by
position, after translating a to b. Thus the input decorations agree on a
patch covering the cube of half-side 1 around the cross. This compares
actual poses, not just the unmarked chair shapes.

But the old arrows on the y arms are different:

| Cross | Negative-y endpoint chair | Its notch | Positive-y endpoint chair | Its notch | Forced arrow |
|---|---|---|---|---|---|
| a | `(-4,-4,-4)` | `+++` | `(-4,4,-4)` | `+-+` | `(1,0,1)` |
| b | `(-4,-4,4)` | `++-` | `(-4,4,4)` | `+--` | `(1,0,-1)` |

The intermediate crosses are at y = -2 and +2. Each endpoint independently
forces the listed arrow; the two ends agree with one another. Hence every
old marked completion retaining these chairs must distinguish a and b.
No choice of markings on undetermined chains can remove this constraint.

The [JSON certificate](../audit/auxiliary_reconstruction.json) lists all
eight shared rotation matrices and the complete endpoint chains.

### Why this rules out every fixed radius

Apply D another m times. The two cross positions become `2^m a` and `2^m b`.

1. **The identical input patch grows.** Substituting equal decorated chair
   patches gives equal decorated patches. Their coarse supports cover
   cubes of half-side `2^m` around the two points.
2. **The endpoint orientations remain unchanged.** Each chair has a
   central child at twice its origin, with the same pose.
3. **No new chair interrupts the relevant chain.** Under one substitution,
   every noncentral child has all three center coordinates odd. The
   dilated chain has two fixed even transverse coordinates, so none of
   those children lies on it. Any central child on the segment would come
   from a chair already on the previous segment. There was none.
4. **The intervening slots remain cross cavities.** At an integer vertex
   other than a parent chair's inside corner, the incident subdivided
   cubes present outside corners of the outer children. The old recutting
   removes their cross octants. Along the interior segment these assemble
   into complete crosses, spaced by 2.
5. The y arrows consequently remain `(1,0,1)` and `(1,0,-1)`.

Choose m so the common input patch contains the proposed radius-r
neighborhood, with a fixed margin for tile extent. Translation equivariance
would give the same output arrow at both crosses. The endpoint conditions
require different arrows: contradiction.

The finite substitution patches used here occur in complete decorated
substitution tilings. One can use the established primitivity and legal
substitution, or embed each patch in larger supertiles whose supports
exhaust space and take a limit. This part uses the existing grid-system
existence/legality results; it is not a consequence of one finite patch
alone. There is no need to assume equality of the full local-rule space
with the substitution hull: an obstruction on that hull is already enough.

**Checked scales:** depths 3, 4, 5; 512, 4,096, 32,768 chairs; common patches
of 8, 64, 512 chairs covering cubes of half-side 1, 2, 4. The proof above,
not extrapolation of these three tests, supplies arbitrary m.

This is stronger than the possibility of ambiguous infinite chains:
**finite chains alone already obstruct locality.**

## 3. Reverse obstruction from an explicit symmetric old tiling

Here the target is the original `L/I` system, in which undetermined axes
can receive independent diagonal markings. The argument must not be
transferred without proof to the connected `X₂` variant.

Let S be the coarse chair substitution and set

```
P_n = S^(2n)(L) + a_n (1,1,1),     a_n = (4^n - 1)/3.
```

These patches are nested. In `S²(L)`, the child chair at `(-1,-1,-1)`
has the same coarse orientation as the root. At level 2n its translated
origin in `P_(n+1)` is

```
a_(n+1) - 4^n = a_n.
```

Their supports exhaust space: the negative outer coordinate tends to
minus infinity, while the missing positive octant starts at `a_n`, which
tends to plus infinity. The union is a complete coarse substitution tiling
T containing the chair at the origin.

Every P_n is invariant under the cyclic coordinate permutation

```
C(x,y,z) = (z,x,y).
```

The old recut chair and its markings have this symmetry too. Fill the
auxiliary axes as follows:

- If a chain has a chair endpoint, use its forced arrow. Endpoint
  consistency follows from the old chain-filling argument; any two
  finite endpoints already occur in a sufficiently large P_n.
- On a chain without chair endpoints, use the positive transverse
  diagonal: components +1 off the chain axis and 0 along it.

This assignment respects C. It gives an old marked `L/I` tiling U with
`C(U)=U`. In particular, the chair at the origin is fixed by C.

Suppose a chair-preserving map F commuted with C and produced a tiling by
our decorated chairs. Then

```
C(F(U)) = F(C(U)) = F(U).
```

The decorated chair at the origin would have to be fixed. But its three
possible poses are `I`, `C`, and `C²`, which C permutes without a fixed
choice. The A/B/C descriptors also directly verify that C is not a
symmetry of the decorated chair. This is a contradiction.

Thus no such rotation-equivariant map exists on the **full old space**.
The argument allows either handedness: the analogous three poses in the
other handedness likewise have no fixed choice under C.

### Three lifts and what this does not prove

The same nested construction using D instead of S works in each of the
three root poses. The `(-1,-1,-1)` child of D² copies its parent pose, so
the decorated patches are nested as well. They give three distinct grid
tilings over the same coarse T. They differ on the chairs along the body
diagonal; off that line the pose is eventually reset. This makes the
symmetry-breaking choice concrete.

A rule allowed to use an externally fixed coordinate frame need not
commute with C. Therefore the symmetry argument does **not** exclude every
translation-equivariant local selection of a valid decorated lift. Nor
have we proved that every old marked tiling admits any such lift. Those
are separate questions. The forward obstruction already rules out the
natural mutual local reconstruction, even with only translation equivariance.

## 4. What this says about the extra information

The two systems enforce related hierarchies while storing information in
different places. An old cross can carry an arrow selected by a distant
chair on an axial chain. Our identical local decorated patches need not
contain that arrow, even though the surrounding hierarchy eventually
specifies it. Conversely, the full old `L/I` space can retain a rotational
symmetry that our three pose choices break.

Consequently, the three internal poses are not simply a bounded-radius
replacement for all the old auxiliary markings. This is a concrete
obstruction to the proposed encoding dictionary, not evidence by itself
that the solid construction is correct or historically new.

## 5. Connected-cross discrepancy to resolve before further claims

The source's connected 3D variant uses `X₂`, with only one opposite pair
of ends marked and its other ends white. In the following **transcribed
fixed-chair model**, the depth-three coarse patch cannot be filled with
that cross alone.

At

```
v = (-4,-2,0)
```

there is a complete cross cavity. Its three possible marked axes are
excluded by immediate neighboring crosses:

| Proposed axis at v | Neighbor cross w | Axis forced at w by a chair endpoint |
|---|---|---|
| x | `(-2,-2,0)` | z |
| y | `(-4,-4,0)` | z |
| z | `(-4,-2,-2)` | x |

Each neighbor differs from v by exactly 2 along the proposed axis, so their
arm ends meet. If v marked that axis, its neighbor would have to mark the
same axis. But the neighbor already needs the different listed axis.
With one marked axis allowed, all three choices at v fail. Full endpoint
chains are in the JSON.

This check uses only **marked versus white**, not our interpretation of
the transverse arrow direction. I also checked the old recut geometry
independently of the center/chain computation:

- Interpreting the pictured I as a symmetric double cone with truncated
  arms, X is exactly the union of three bars with axial half-length 1
  and transverse half-width 1/4.
- On the exact quarter-unit grid, X occupies 80 cells; the old recut chair
  occupies 388 cells. No approximation is involved for these old solids.
- All 512 recut chairs in the patch have disjoint interiors.
- In the unit-half-side box around v and each listed neighbor, the
  uncovered region is exactly one full X, with no other void.

**Interpretation needing review:** the printed I formula has `x₁` in the
minimum, whereas the symmetric biprism picture requires `|x₁|`. The model
uses the pictured symmetric form. More substantially, the connected
variant's statement about exactly one determined chain at each vertex
does not match this transcription. A targeted search did not locate a
clarification, but was not a comprehensive erratum search.

This is a specific question about our reading of the connected modification,
not a declaration that the published aperiodic-pair theorem is false.
The main `L/I` construction permits all three axes of a cross to carry
markings independently and does not have this one-axis obstruction.
Before comparing full `L/X₂` spaces, reconcile this witness with the
intended geometry/markings or obtain expert clarification. No inquiry
has been sent and the prepared v1 inquiry was not altered.

## 6. Reproduce and resume

```sh
uv run --locked python strong/audit/reconstruct_gs_auxiliary.py
```

[Script](../audit/reconstruct_gs_auxiliary.py) ·
[Exact results and witnesses](../audit/auxiliary_reconstruction.json)

The program imports no project implementation. It checks a second,
signed-diagonal transcription of S against the decorated substitution,
5,376 matching unit-face pairs at depth three, the arrow conflict and
its first three inflated witnesses, exact old recut cavities, and finite
cyclic-symmetry claims. Infinite-radius and infinite-tiling conclusions
are the written arguments above, not assertions proved by finite testing.

Next tasks should reflect the negative result:

1. Scrutinize the inflation proof and the source-model discrepancy before
   seeking any equivalence claim.
2. If useful, study a nonlocal completion relation to the original `L/I`
   space, distinguishing forced finite chains from free infinite ones.
3. Investigate a translation-only inverse or a restricted old tiling space;
   do not presume a two-sided local correspondence.

No frozen geometry, dependencies, delivery artifacts, or outreach changed.

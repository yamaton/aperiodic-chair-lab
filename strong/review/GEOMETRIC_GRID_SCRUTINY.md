# Scrutiny of the geometric grid argument

*16 September 2026. Exact frozen candidate; internal mathematical scrutiny.*

The [short manuscript](CURVED_GRID_NOTE.md) consolidates the registration
argument into five lemmas using the attributed §8a route. The
[current dependency table](../../docs/PROOF_STATUS.md) records how this
written geometry relates to the completed Lean grid theorems.

## Outcome and scope

I have not found a counterexample or an unfilled logical step in the
geometric bridge after rederiving its implications. The argument can be
stated without assuming a common grid, face-to-face contacts, or one
handedness at the outset. Its most delicate implications are made explicit
below and their finite hypotheses have a new checker.

**Claim examined:** if congruent copies of the exact candidate tile form
an interior-disjoint covering of R³, then, after one global Euclidean
change of frame, every placement has an integer origin and a proper cubic
orientation, every coarse unit cube has exactly one owner, and every
exposed unit-face interface obeys the specified cap matching rules.

This is a written proof about arbitrary tilings, supported by finite
arithmetic. The program does not quantify over arbitrary real placements.
The existence and recursive-aperiodicity arguments are separate; the
present claim alone would be vacuous if the tile did not tile at all.
No assertion concerns the approximate STL or tolerance in a manufactured
object. The frozen solid, proposal, and v1 review packet are preserved.

## 1. Exact hypotheses recovered from the frozen coordinates

Write a port as

```
p + w u U + w v V + k δ φ(u,v) N,       -1 ≤ u,v ≤ 1,
φ(u,v) = (1-u²)(1-v²)(1+u/5+v/7),
w=1/64, δ=1/4096.
```

U,V are ordered axes **in the coarse face plane**. They are not the tangent
vectors to the curved graph at its center. N is the coarse outward normal.
Inside its feature box the tile is on the side `s ≤ kδφ(u,v)`; outside the
boxes it agrees with its seven-cube coarse chair.

The new [checker](../audit/scrutinize_grid_bridge.py) reads the frozen JSON
without importing any project implementation and establishes:

- The coarse chair has exactly 24 exposed unit faces. Each of the 192
  recorded ports lies on one of those actual faces; every face has eight.
- For every port, `f=p-(3U+V)/16` is that unit face's center, and its owner
  is the cube with lower corner `q=f-N/2-(1,1,1)/2`. The cube q belongs to
  the chair and `q+N` does not. Checking half-integer parity alone would
  not establish this ownership fact.
- All keys are nonzero. On the square, `0≤(1-u²)(1-v²)≤1` and
  `23/35≤1+u/5+v/7≤47/35`, giving the conservative normal reach
  `h=12δ(47/35)=141/35840 < 1/4`; all tangent squares stay `19/64` from face edges.
- The middle half of each owned cube is untouched: 1,344 core/feature-box
  checks have positive separation. These cores contain open balls of
  radius 1/4. Nine unchanged corridors connect the seven cores, with
  1,728 further separation checks.
- The tile lies in `[-1-h,1+h]³`, so its diameter is less than 4.
- The eight feature locations on a unit face form the complete square
  symmetry orbit of the offset `(3,1)/16`.

The graph is continuous and equals the original face level on its square
edges. Inside each box its subgraph is regular closed, with the usual two
local sides at every interior graph point. The strict box clearance makes
these prescriptions compatible with the coarse body. Thus the cap patches
really are boundary patches, rather than surfaces buried in the same tile.
The connected-core checks provide the interior balls used below; those
checks alone are not a proof that every part of the solid is connected to
the cores.

## 2. Local finiteness comes before any grid

Choose one radius-1/4 interior ball in the prototile and its congruent image
in each tile. The chosen balls of distinct tiles have disjoint interiors.
If a tile meets a ball of radius R, its chosen center is within distance
R+4 of that ball's center, using the tile diameter bound. Its chosen ball
therefore lies within radius `R+17/4`.

Comparing volumes gives the explicit finite bound

```
number of tiles meeting B_R ≤ (4R+17)^3.
```

This holds regardless of translations, orientations, reflections, or
contact types. In particular, tiles cannot accumulate infinitely around a
single cap. No assertion that the tile origins already form a discrete
lattice is needed here.

## 3. A whole curved cap must acquire an open cap contact

Fix an interior point x of a cap on tile A. Approach x from the exterior
side of A. Those approaching points belong to other tiles because the
collection covers space. Local finiteness supplies a subsequence belonging
to one other tile B. Closedness gives `x∈B`.

The point x cannot be interior to B: arbitrarily near x there are interior
points of A, which would then also lie inside B. Thus x lies on B's boundary.
This applies to every point of a relatively open cap patch.

Only finitely many other tiles meet its compact closure. Each boundary is
covered by finitely many closed planar pieces and closed polynomial cap
pieces. Their intersections with the original cap give a finite relatively
closed cover. A finite union of relatively closed sets with empty interior
cannot cover a nonempty open set. At least one intersection has relative
interior in the original cap.

A plane cannot contain an open piece of the nonaffine graph. An edge or
seam cannot contain a two-dimensional open piece. We may consequently
shrink to an open coincidence of two cap interiors.

**What this establishes:** every cap has at least one neighboring cap
with an open coincidence. It does not initially assert that all cap points
have the same neighbor. That stronger conclusion follows below from
rigidity and unique cube ownership.

## 4. Open coincidence fixes the complete base frame

Uniformly scale all three local coordinates by 1/w. The cap lies on

```
z=Hφ(u,v),       H=kδ/w=k/64 ≠ 0.
```

Uniform scaling conjugates an ambient isometry to an ambient isometry;
scaling the two face coordinates alone would not do so.

Let `P_H=z-Hφ`. Pull back the moved second graph equation to the first
parametrized graph. It vanishes on an open set in `(u,v)`, hence is the
zero polynomial. Polynomial division by the monic polynomial P_H then
shows that P_H divides the moved defining equation. Both polynomials
have total degree five, so the quotient is a nonzero constant. The entire
algebraic graphs coincide under the isometry.

To classify their straight lines, substitute

```
(u,v,z)=(x+dt,y+et,c+ft).
```

The degree-five coefficient, apart from H, is `d²e²(d/5+e/7)`.

- If `d=0`, `e≠0`, the cubic coefficient forces `x=±1`.
- If `e=0`, `d≠0`, it forces `y=±1`.
- If `d≠0` and `e≠0`, then `e=-7d/5`, and the quartic coefficient forces
  `1+x/5+y/7=0`.
- If `d=e=0`, the graph forces `f=0`, giving no nonconstant line.

In each of the first three cases φ is identically zero along the line,
so z is zero too. These are exactly five lines in one plane: two parallel
pairs bounding a square and one unpaired line. The arrangement intrinsically
identifies the base plane, square, and center. The fifth line distinguishes
the ordered axes: no nonidentity square symmetry preserves
`1+u/5+v/7=0`: the nonzero constant term fixes the proportionality factor
between equations of that line, leaving its two unequal positive coefficients
to fix the axes. This holds for improper as well as proper ambient isometries.

Only reversal of the base normal remains possible. The recovered square
is exactly the physical cap domain, so open coincidence identifies the
**whole bounded cap**, not just a potentially displaced fragment of it.
The fifth line is outside the physical square; it is used only after
polynomial continuation, not as an additional physical feature.

## 5. Opposite sides determine a discrete neighbor and its cube

Normalize A's placement to the identity, and write B's placement as
`x↦t+Rx`, initially allowing any orthogonal R.

The preceding lemma gives

```
R U_B=U_A,    R V_B=V_A,    R N_B=σ N_A,    k_A=σ k_B,
```

where `σ=±1`. If `σ=+1`, the two subgraph interiors occupy the same side
of the coincident graph in an open neighborhood, contradicting interior
disjointness. Therefore `σ=-1` and `k_B=-k_A`.

Consequently

```
R = U_A U_Bᵀ + V_A V_Bᵀ - N_A N_Bᵀ,
t = p_A - R p_B = f_A - R f_B.
```

R is a signed coordinate permutation. Because the normal coordinates of
both face centers are integral and their two face coordinates are
half-integral on corresponding axes, `t∈Z³`.

This face-center equality is stronger than an integral shift alone. It
identifies exactly the same unit square with opposite outward normals.
The second face's cube center becomes

```
t + R(f_B-N_B/2) = f_A+N_A/2.
```

Thus B owns precisely the outward adjacent cube `q_A+N_A`.
The checker verifies this statement for **all 1,536 opposite-key port
pairs**, including pairs that other parts of the chair later disqualify.
There are 86 distinct integer relative placements among these necessary
single-cap possibilities; this is not the 44 whole-chair contact count.

Let `χ=det[U,V,N]`. The frozen records have one χ for each signed key and
`χ(-k)=-χ(k)`. Therefore

```
det R = -χ_A χ_B = +1.
```

Properness is derived, not imposed. Every matched pair has the same
physical handedness, even though reflected copies were initially allowed.

### A useful failed weakening

If the two polynomial coefficients were equal, exchanging U and V would
also preserve a cap. For the frozen offset pattern, the corresponding
local cap match can have a nonintegral translation. The checker records
one such altered-cap witness, with translation `(-2,-1/8,1/8)` and an
orientation-reversing linear part of determinant -1. This control uses
reflected copies; it does not show failure in a proper-rotations-only model. This is not a full tiling counterexample;
it demonstrates why fixing the ordered face axes is essential to this
particular grid argument. Matching only normals and key magnitudes would
be insufficient.

## 6. A cap-connected component owns the entire coarse grid

Connect two tiles when caps coincide on an open patch. Fix one component
and use any member's placement as the global reference frame. Compositions
of the relative maps above lie in `Z³ ⋊ O`, where O is the group of proper
cubic rotations. Every tile in this component therefore has an integer
origin, a common cubic frame, and the same handedness.

Two distinct component tiles cannot own the same coarse cube, since both
would contain its untouched middle half, giving interior overlap.

Now take any owned cube q and a face-neighbor q+N. If the same chair owns
both, there is nothing to prove. Otherwise the face is an actual exposed
face of the chair owning q. It has eight caps; choose any one. Section 3
supplies a cap match, and Section 5 puts the matching tile in this same
component owning q+N.

The owned cubes are nonempty and closed under every step of lattice
adjacency. The connectedness of the cubic lattice implies that every
cube is owned, uniquely within the component.

**This does not yet prove physical coverage.** Pockets remove material
from coarse cubes. Nor has any other component been excluded yet.

## 7. Physical coverage: all ports have the same opposite owner

Across an exposed face of A, each of its eight caps has a matching tile.
Every such matching tile must own the same outward adjacent cube. By
uniqueness of component ownership they are all **the same tile B**.
Rigidity identifies each entire cap square, so the eight matches give the
complete complementary interface with B. Distinct cap centers make the
correspondence injective; B has exactly eight ports on its opposite face,
so none is omitted.

It remains to rule out interference between different feature locations.
The feature boxes form a universal periodic family: **24 box types modulo
integer translations** (three face-normal axes, eight positions each).
The checker maps all 192 ports in all 48 cubic frames into this family:
9,216 memberships, including reflections.

For these 24 types, it checks all nonidentical pairs at relative integer
shifts in `{-1,0,1}³`: **15,528 exact box comparisons**. Larger shifts cannot
intersect: some center coordinate differs by more than 1, while the sum
of the corresponding half-widths is at most 1/32. Thus this finite check
covers the infinite family, with the explicit separation bounds:

| Locations | Separating-coordinate gap |
|---|---:|
| Same unit face | `3/32` |
| Different coplanar faces | `19/32` |
| Different parallel grid planes | `17779/17920` |
| Perpendicular faces | `10499/35840` |

Within the component, unique coarse ownership now implies that only the
two opposing owners can have occurrences at the same feature location.
Their matching features share a box; distinct locations are separated.

Now distinguish two regions:

- **Outside actual feature boxes:** each component tile agrees with its
  coarse chair. Unique ownership of every cube gives complete coverage.
- **Inside an actual feature box:** among the component tiles, only the
  owners of the two opposite cubes can contribute. Other features are
  separated, and the box is away from cube edges. In common coordinates
  these two owners occupy `s≤g(u,v)` and `s≥g(u,v)`, respectively. Their
  union fills the box, including its boundary and seams.

Template boxes on an internal face of one coarse chair are merely virtual
locations: there is no port there and the material is unchanged. They
must not be treated as an interface requiring two distinct owners.

The selected component therefore fills all of R³. This proof does not
first assume that off-grid tiles are absent: the statements about who
can contribute to a box concern **members of this component**.

## 8. Only now exclude a second component

Suppose a tile from another component exists. It contains an open ball.
The first component already covers that ball. Only finitely many of its
tiles meet a smaller compact ball, and their closed boundaries have empty
interior. A point of the second tile's open ball consequently lies in the
interior of a first-component tile. This violates interior disjointness.

There is exactly one cap-contact component. All tiles have the common grid
and handedness derived above, and their physical interfaces reproduce the
finite cap rules. This completes the geometric bridge.

## 8a. Shorter component-exhaustion route from the Chair44 comparison

The later [proof comparison](CHAIR44_PROOF_COMPARISON.md#5-an-attributed-simplification-of-our-geometric-argument)
adapts Tsiokos's retained-core argument, described in Chair44's registration
section and formalized in `Proved/CarrierCoreCover.lean`. After Section 6,
it can replace Sections 7–8 **for the registration implication**:

Take any actual tile T and the center c of an open radius-1/4 ball in its
interior. The component's carrier cubes cover c; choose one such cube owned
by S. Clamp c into that cube's inset `[1/64,63/64]^3`, obtaining y. Since
`h=141/35840<1/64`, y has an open neighborhood inside S unaffected by caps.
Also `||y-c||²≤3/4096<1/16`, so y is in T's interior ball. Interior
disjointness gives S=T. Every actual tile therefore belongs to the component,
whose physical coverage now follows from coverage by the original tiling.

This uses carrier coverage to prove membership before inferring physical
coverage. It does not construct an infinite tiling or remove local feature
separation obligations. The earlier global-box argument and its certificates
remain preserved. This shorter proof is written mathematics with exact bounds,
reviewed by a subagent; it has not been formalized in Lean. Attribution to
Chair44's formal argument is essential.

## 9. What changed, and what still needs review

The frozen geometry has not changed. This scrutiny adds:

1. An explicit packing bound independent of any grid assumption.
2. Direct checks that every recorded port belongs to its claimed exposed
   face and that each single-cap match owns the correct adjacent cube.
3. A complete finite reduction for separation of the infinite feature-box
   family, checked in all 48 frames.
4. An explicit justification that all eight cap mates are the same
   neighboring chair, followed by a distinction between actual feature
   boxes and unused template locations.
5. A clear order: component cube coverage, component physical coverage,
   then exclusion of other components.

The analytic continuation, line classification, closed-cover argument,
and coverage implications are written mathematics. Supporting arithmetic
is reproducible, but independent human scrutiny or formal verification of
those implications has not occurred. No new fatal gap has been identified
by this pass; that is the outcome of scrutiny, not a proof of absence of
all possible errors.

## Independent subagent scrutiny

Three bounded reviews were completed in parallel:

| Reviewer | Scope | Outcome |
|---|---|---|
| `cap_rigidity_scrutiny` | Polynomial continuation, five lines, base frame, opposite sides, reflections | No substantive defect found; clarified base-plane axes and the nonzero-direction case split. |
| `global_grid_scrutiny` | Local finiteness, boundary coverage, ownership, actual filling, other components | No substantive defect found conditional on cap rigidity; clarified component-only statements and unused internal-face boxes. |
| `literature_review`, reassigned to code audit | Primary checker and an alternate computation | No arithmetic defect found; corrected the negative control's improper-isometry terminology. |

The first two reviewers started with fresh conversation context. The third
reused an earlier literature-review thread. All used the same model family
and could read the supplied project arguments; these are independent
assignments and partly independent implementations, not independent human
endorsements. None edited the repository. The parent incorporated their
clarifications and they checked the relevant revisions.

The implementation reviewer independently searched all 48 frames, mapped
all eight vertices of each owning cube, and derived the periodic box family
from transformed ports rather than a prescribed pattern. Its wider shift
range `{-2,-1,0,1,2}³` checked **71,976** nonidentical box pairs. The portable
[alternate checker](../audit/grid_bridge_crosscheck.py) and
[its results](../audit/grid_bridge_crosscheck.json) preserve those paths.
Both checkers have passed after the changes. They share mathematical
premises such as the height-bound derivation; their independence concerns
the arithmetic implementations.

## Reproduction

```sh
uv run --locked --offline python strong/audit/scrutinize_grid_bridge.py
uv run --locked --offline python strong/audit/grid_bridge_crosscheck.py
```

[Exact results](../audit/grid_bridge_scrutiny.json) ·
[Earlier analytic audit](../audit/README.md) ·
[Full theorem dependencies](DEPENDENCY_AUDIT.md)

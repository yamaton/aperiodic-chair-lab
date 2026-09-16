# A recut chair with a recursive matching rule

*Research proposal, 15 September 2026.*

**Later context:** the [Chair44 comparison](review/TSIOKOS_CHAIR44_COMPARISON.md)
identifies an equivalent published matching system with different surface
geometry. Read this proposal with that comparison and the
[current formal scope](../formal/README.md). The frozen coordinates are
preserved; this document does not establish a distinct matching-system discovery.

**This pass produces a substantially stronger candidate:** one connected
chair-shaped solid with 192 small curved tabs and pockets. Its matching rules
on an integer grid force a unique hierarchy. That statement has independent
computational checks. Below is also a proposed analytic argument that the
curved ports force the grid in arbitrary Euclidean tilings.

Taken together, the arguments propose a strongly aperiodic construction
using **arbitrary Euclidean congruent copies, including reflected copies**.
The subsequent [handedness argument](FOLLOWUP_REFLECTIONS.md) shows why
matching caps force every tiling to use one handedness throughout, reducing
the claim to the original proper-rotation hierarchy.
This is not a claim of an independently established new monotile theorem:
the full argument, especially the passage from curved surface contacts to a
global grid, needs mathematical review. No novelty or priority claim is made.

![The modified solid, its eight-chair group, and matching versus overlapping contacts](artifacts/recut-chair-placements.png)

- [Standalone interactive viewer](artifacts/recut-chair.html), usable offline
  in Firefox: one solid, eight- and 64-copy placements, a valid contact, and
  the failed periodic contact. Drag to rotate, scroll to zoom, and separate
  the eight-copy group to inspect its pieces.
- [Downloadable placement and contact figure](artifacts/recut-chair-placements.png).
- [Exact rational surface specification](artifacts/recut_chair_exact.json).
- [Approximate STL](artifacts/recut-chair-approximation.stl).
- [Independent hierarchy verification](artifacts/chair_recut_hierarchy_verification.json).
- [Frozen-coordinate audit and reviewer package](audit/README.md): a new
  verifier with no search-code imports, exact local cap checks, and an
  expanded geometric argument. The internal audit passed; external review
  remains outstanding.
- [Three subagent reviews](audit/SUBAGENT_REVIEWS.md), their findings and
  resolutions, and an additional finite cross-check implementation.
- [Prior-literature comparison](audit/LITERATURE_REVIEW.md), especially
  Goodman-Strauss's earlier two-tile construction and the different role
  of orientation states here. Priority remains unresolved.
- [Follow-up research record](FOLLOWUP_REFLECTIONS.md): reflections, three
  face patterns, an explicit periodic control, and six-depth recoding.
- [Concise expert-review note](REVIEW_NOTE.md).

The viewer and STL approximate the curved surfaces. **The proposed analytic
rigidity argument does not certify a triangulated or manufactured version.**
The viewer defaults to enlarged features (width ×3, depth ×12), with an
actual-proportions option. The cross-sections show the real depth-7/depth-7
match and depth-7/depth-9 mismatch at an enlarged vertical scale. Body
colors distinguish copies, and port colors distinguish tabs from pockets;
these colors are not extra matching rules.

## 1. What changed

Whole-filler fusion kept the chair groups intact. Its parity obstruction
also applies to adding nonempty fragments inside the same symmetric filler
regions: a fragment still collides when its destination is occupied by a
whole cross. Subdivision alone does not remove that collision.

Here material is both removed and added directly on the chair's boundary.
The starting coarse shape is the seven-cube chair

```text
L = union of the seven unit cubes with lower corners in {-1,0}³ \ {(0,0,0)}.
```

It has 24 exposed unit-square faces. The recuts can distinguish the three
proper rotational poses that leave the unmarked chair's missing corner
unchanged. Those poses carry information through the substitution.

The coarse hierarchy comes from the chair construction studied in
[Goodman-Strauss's aperiodic pair](https://doi.org/10.1006/eujc.1998.0282).
That paper supplies a different, multiple-piece construction; it is not a
source for the one-solid claim proposed here. The role of transmitting
information between successive levels is described in the author's
[construction poster](https://strauss.hosted.uark.edu/distribution/tilings/enap.pdf).

## 2. Exact definition of the candidate

### Port positions and frames

On each unit-square face, choose its center `f` and its outward coordinate
normal `n`. There are eight port centers

```text
p = f + (a e_i + b e_j)/16,
(a,b) ∈ {(±1,±3), (±3,±1)},
```

where `e_i,e_j` are the positive coordinate axes tangent to the face.

For each port, define the ordered, signed coordinate directions:

- `e_u`: the direction of the offset component with magnitude 3;
- `e_v`: the direction of the offset component with magnitude 1.

Thus `p = f + (3e_u+e_v)/16`. This ordering matters: the cap will have an
asymmetric shape that remembers both directions.

Each port has a nonzero signed integer key `k`, with `1 ≤ |k| ≤ 12`.
The exact data file explicitly lists all 192 positions, normals, frames,
and keys. Its ordering is generated in [chair_recut.py](chair_recut.py),
and its keys are profile **1** (zero-based) in the
[synthesis record](artifacts/chair_recut_synthesis.json).
Only the identity proper symmetry of the coarse chair preserves these keys;
within a fixed grid frame, its three otherwise equivalent poses are distinct.

### Curved boundary

Replace the small square patch centered at `p` with

```text
p + (u/64)e_u + (v/64)e_v + (k/4096) φ(u,v)n,

φ(u,v) = (1-u²)(1-v²)(1+u/5+v/7),    -1 ≤ u,v ≤ 1.
```

A positive key adds a tab; a negative key cuts a pocket. Material lies on
the inward side of this graph. The rest of the coarse chair is unchanged.
The graph meets the original face at the square's boundary, so no vertical
side walls are needed.

Inside the square, `φ>0`. Its absolute height is at most
`12(1+1/5+1/7)/4096 = 141/35840 < 1/250`. The ports lie well inside their
unit faces, are mutually separated, and do not reach the middle half of any
coarse unit cube. The resulting regular closed solid is bounded and has
connected interior: the unit-cube cores and their internal connections
remain, the pockets are shallow, and each tab is attached along an open patch.

The signed keys sum to zero. Since

```text
∫[-1,1]² φ(u,v) du dv = 16/9,
```

the added and removed volumes cancel exactly. The solid has volume **7**.

## 3. Existence: one shape fits through every substitution level

Use eight children at centers `c_j`, with these proper rotations `R_j`:

| j | Center | R_j(x,y,z) |
|---|---|---|
| 0 | (0,0,0) | (x,y,z) |
| 1 | (1,1,-1) | (-z,-x,y) |
| 2 | (1,-1,1) | (-x,y,-z) |
| 3 | (1,-1,-1) | (-y,x,z) |
| 4 | (-1,1,1) | (y,-z,-x) |
| 5 | (-1,1,-1) | (z,-y,x) |
| 6 | (-1,-1,1) | (x,z,-y) |
| 7 | (-1,-1,-1) | (x,y,z) |

The union of the coarse children is `2L`. To substitute a chair with center
`c` and orientation `R`, place children at `2c+Rc_j` with orientations
`RR_j`.

For the discrete contact analysis, a directed contact type `(t,R)` places
one chair at the origin with identity orientation, and its neighbor at
integer center `t` with relative orientation `R`. There are 1,194 geometrically
possible face-contact types under the 24 proper cube rotations, excluding
coarse overlaps. A contact fits when every shared port has the opposite key.

Starting with contacts inside the eight-child group and repeatedly
substituting both members of every contact gives a **closed set of 30 contact
types**. All obey the candidate's rules. Closure is a finite calculation:
two face-contacting children of different parents must descend from
face-contacting parents, since each coarse child is contained in its parent.
There are finitely many relative positions and orientations to consider.

Consequently every finite substituted patch fits. Such patches contain
balls of arbitrarily large radius after suitable translations. Compactness
of the finite-state integer-grid placement space gives an infinite tiling.
The small recuts fit because opposite caps have equal keys in magnitude and
aligned ordered frames. This is an existence argument, not an inference
from just one finite patch.

As an implementation check, the 512-chair patch was verified directly:
3,584 coarse voxels without overlap and 43,008 matched interior port pairs.
The contact closure was separately regenerated in Python.

## 4. Every valid grid tiling has a unique eight-chair grouping

**Simpler subsequent proof:** [A local parent rule](MOTIF_GROUPING.md)
derives this grouping directly from A/B/C face patterns and arrows.
Six diagonal contacts identify a center; otherwise the notch owner is the
parent. Local face propagation replaces complete-star enumeration, and
agreement of the seven children on their parent replaces the 28 competing
group comparisons. The original certificate-based proof is retained below
as a cross-check.

This section assumes integer chair centers in one cubic frame. Section 7
addresses why the curved geometry might enforce that assumption.

### Complete face-neighborhoods

Of the 1,194 possible directed contacts, exactly **44** fit the keys. A
complete face-neighborhood, or star, consists of all chairs sharing a
positive-area face with a fixed chair.

Every exposed unit face of that chair must be covered exactly once by a
neighbor. Candidate neighbors must also be mutually nonoverlapping and
match wherever they touch each other. Exhausting those conditions produces
exactly **33 stars**. A separate SMT enumeration, built from displaced
voxels and individual ports, produces the same 33 and proves there are no
others in this model.

Some stars might not extend to infinite tilings. Including them is safe for
the following universal argument: every star that occurs in an infinite
tiling is among the enumerated ones.

### A forced central chair

Exactly one of the 33 stars contains the seven outer children around its
anchor, with the rotations in Section 3. In that case the anchor is a group
center.

For each other star, the certificate identifies a neighboring chair whose
own star must be that central star. The check uses necessary compatibility:
the neighbor's star must contain the anchor and every member of the
anchor's star that also touches the neighbor. Every enumerated star meeting
those requirements is central, and its group contains the anchor.

Thus **every chair belongs to a complete group of the specified type**.
This argument does not assume that a chosen finite outer boundary is tiled.
It uses complete local face-neighborhoods.

### Uniqueness

A fixed oriented chair has eight possible roles in such a group, each of
which determines the parent center and orientation. For each of the 28
pairs of different roles, the two proposed groups cannot coexist: their
union either overlaps coarse chair interiors or violates a port match.

Therefore no chair belongs to two different groups. Since every chair
belongs to at least one, the groups partition the tiling uniquely.

The [star certificate](artifacts/chair_recut_stars.json) records the
neighborhoods and forcing witnesses. The independent checker verifies both
the complete enumeration and the grouping implications.

## 5. The grouped tiling has the same rules and a common grid

Grouping alone is insufficient. The parent chairs might slide relative to
one another, or obey weaker rules.

The coarse group is `2L`, and its center is the central child's integer
center. We check all possible contacts of two groups at **integer fine-grid
offsets**, including offsets with odd coordinates. Those odd offsets would
be half-integer offsets after scaling down by two.

There are **6,801** nonoverlapping face-contact possibilities for the coarse
groups in this enumeration. Exactly **44** match their exposed port profiles.
Every compatible offset has all coordinates even. After dividing the
offset by two, the allowed contact set is exactly the original 44.

The check was repeated by examining child-to-child contacts instead of
comparing the exposed macro boundaries. Both methods agree.

The face-adjacency graph of the grouped grid tiling is connected. Hence its
centers all lie in one coset of `2Z³`. Translate that coset to the origin
and scale down by two: the result is another valid tiling of the same
**abstract grid matching system**. It is not necessary for the grouped
curved boundary to be a literal scaled copy of the original curved boundary;
what recurs is exactly the set of allowed contacts.

Evidence: [macro contacts](artifacts/chair_recut_macro.json) and
[independent hierarchy checks](artifacts/chair_recut_hierarchy_verification.json).

## 6. Consequence in the grid model: no translations or infinite-order screws

The unique grouping is determined by the tiling, so every translation
symmetry preserves it. A period vector must therefore lie in `2Z³`.
The deflated tiling obeys the same rules and again groups uniquely, forcing
the original period to lie in `4Z³`. Iterating gives

```text
t ∈ ⋂_{m≥0} 2^m Z³ = {0}.
```

Thus every valid grid tiling lacks nonzero translations. The tiles use a
finite set of orientations. A symmetry has one of finitely many possible
linear parts, and two symmetries with the same linear part differ by a
translation. The full symmetry group is consequently finite. In particular,
there is no infinite-order screw symmetry.

This is the computer-assisted hierarchy result. The remaining geometric
issue is whether a tiling can evade the grid model.

## 7. Proposed geometric enforcement by asymmetric polynomial caps

This is the part of the construction most in need of independent scrutiny.
It is a mathematical argument supported by exact identities and finite
frame checks, not a solver verdict about all Euclidean tilings.

### 7.1 A cap remembers its center and ordered axes

Consider the whole algebraic surface

```text
z = h(1-u²)(1-v²)(1+u/5+v/7),   h ≠ 0.
```

For a physical cap, obtain these coordinates by dividing all three local
ambient coordinates by its half-width `w=1/64`. This **uniform** scaling
preserves isometries under conjugation and gives `h=k/64`. Scaling only
the tangent coordinates would not justify the Euclidean rigidity argument.

It contains exactly five straight lines, all in the plane `z=0`:

```text
u=1, u=-1, v=1, v=-1, 1+u/5+v/7=0.
```

To check that this list is complete, substitute a line
`u=a+dt, v=b+et, z=c+ft`. The degree-five coefficient on the right is
proportional to `d²e²(d/5+e/7)`.

- If `d=0` and `e≠0`, the cubic coefficient forces `a=±1`.
- If `e=0` and `d≠0`, it forces `b=±1`.
- Otherwise `d/5+e/7=0`; the quartic coefficient forces
  `1+a/5+b/7=0`.
- A vertical line is impossible because the surface is a graph.

In each allowed case the right side vanishes identically, giving one of
the five listed horizontal lines.

An isometry carrying an open patch of one such algebraic surface to an open
patch of another carries the whole algebraic surface to the other. Here
the defining polynomial is irreducible (it is linear in `z`), and an open
surface coincidence forces the transformed irreducible polynomials to
agree up to a nonzero scalar.

More explicitly, substitute the first graph into the transformed second
surface equation. The resulting polynomial in `(u,v)` vanishes on an open
set, so it vanishes identically. Division by the first graph's defining
polynomial shows divisibility; both irreducible surface equations have
degree five, so they differ only by a nonzero scalar.

The isometry therefore carries the five-line arrangement to the five-line arrangement.
The two parallel pairs determine the square, its center, and its axes.
The fifth line breaks all eight square symmetries except the identity in
the ordered `(u,v)` frame: its two positive, unequal coefficients distinguish
both axes and both signs. All five lines determine the base plane. Reflection
through that plane exchanges `h` with `-h`; an isometry cannot change `|h|`.

Thus an open cap match fixes the cap center, its ordered tangent axes, and
the magnitude of its key. This reasoning uses the analytic continuation
of the bounded cap, not physical extensions of the five lines.

### 7.2 A cap must meet another cap

A tiling by this bounded solid is locally finite: every tile contains a
fixed-radius interior ball, those balls have disjoint interiors, and only
finitely many can lie near a bounded region.

Every point in the interior of a cap lies on another tile's boundary:
approach it through exterior points, use local finiteness to select a
subsequence belonging to one other tile, and use that tile's closedness.
The point cannot be in the other tile's interior without overlapping the
first tile's interior. See the [expanded audit](audit/README.md#d-every-cap-has-an-open-cap-match)
for the finite-boundary-covering argument.

An open part of a curved cap lies against the boundaries of finitely many
neighboring tiles. Flat faces cannot share an open patch of the nonplanar
cap. Distinct algebraic surfaces cannot share an open patch unless their
surface equations agree as above. Consequently some neighboring cap has
an open coincidence with it. One can express this using the finite union
of the intersections of the neighboring boundary patches with the cap;
without an open coincident patch those lower-dimensional intersections
cannot cover the cap.

On a common boundary patch, the tile interiors must lie on opposite sides.
The two outward base normals are therefore opposite, and their signed keys
are opposite. The ordered tangent axes coincide.

### 7.3 One cap match forces an integer relative placement

Each port's ordered axes are signed coordinate axes. Matching them and
opposing the base normals forces the relative map to be a signed coordinate
permutation. It is proper even if reflected copies are initially allowed:
the frozen keys have fixed frame chirality `c(k)=det[e_u,e_v,n]` with
`c(-k)=-c(k)`, so a match gives `det(R)c(-k)=-c(k)` and `det(R)=+1`.
See the [separate check and global handedness reduction](FOLLOWUP_REFLECTIONS.md#1-reflections-a-local-invariant-gives-a-global-reduction).

Write the port positions in their local tile frames as

```text
p_A = f_A + (3e_u,A+e_v,A)/16,
p_B = f_B + (3e_u,B+e_v,B)/16.
```

If the relative placement is `x ↦ t+Rx`, the cap match gives
`p_A=t+Rp_B` and identifies the two ordered axes. The small offsets cancel:

```text
t = f_A - Rf_B.
```

A unit face center has an integer normal coordinate and half-integer
tangent coordinates. Because the matched normals identify the same normal
axis, this difference is an integer vector. The unit faces themselves
coincide and have opposite outward normals.

The exact check enumerates 1,536 matching port/frame correspondences and
finds no noninteger relative translations. This supports the arithmetic
argument; it is not a substitute for the cap-rigidity argument.

### 7.4 The locked component must fill the whole space

Join two tiles when they have one of these cap matches. In a connected
component of this graph, all coarse chairs share one cubic frame and one
integer-grid coset, by the preceding argument.

Two coarse chairs in that component cannot cover the same unit cube: both
physical solids contain that cube's unmodified middle half, which would
give an interior overlap. Thus their coarse unit cubes have disjoint interiors.

Every exposed unit face of each coarse chair has curved ports. A cap match
supplies a tile in the same component on the other side of that **whole unit
face**, occupying the adjacent coarse unit cube. Hence the component's set
of occupied unit cubes has no boundary in the connected cubic lattice. It
must be all of that lattice.

There is only one coarse owner of the cube across a given unit face, so all
of that face's cap matches go to that owner. The recut boundaries fit there;
away from the small port patches the two boundaries are the common flat
face. Consequently the physical component fills space as well. No second
component can be inserted without an interior overlap.

If this argument is sound, every Euclidean tiling is an integer-grid tiling
of the verified matching system. Sections 3–6 then supply existence and
strong aperiodicity for the exact curved solid.

## 8. What the search rejected, and why this survivor differs

There are `3^8 = 6,561` stationary assignments of child poses in this model.
Closing each contact language and solving the signed matching equations
produces three maximal matching-profile classes (modulo the chair's proper
symmetries, key renaming, and independent key sign conventions).

| Profile index | Templates represented | Independent depth keys | Allowed contacts | After grouping |
|---|---:|---:|---:|---|
| 0 | 6,555 | 4 | 186 | All 1,194 parent contacts become legal |
| **1** | **3** | **12** | **44** | **Exactly the same 44 contacts** |
| 2 | 3 | 12 | 62 | 398 parent contacts become legal |

Profiles 0 and 2 admit explicit periodic tilings: substitute their eight
children into the ordinary chair's translational tiling. The resulting
period lattice has columns

```text
(14,0,0), (-4,2,0), (-8,0,2).
```

Its determinant is 56, with eight chairs. Direct checking confirms 56
coarse voxels and 768 matched port pairs per quotient. These counterexamples
also fit the asymmetric cap frames, since the fine-grid unit faces align.

Earlier rectangular repeat tests missed these slanted packings. One of
those tests timed out and remains recorded as unknown. The explicit oblique
witnesses supersede those tests for profiles 0 and 2. For profile 1, the
hierarchy argument is the evidence against *all* periods in the grid model;
absence of a small periodic witness is not the proof.

The 6,561 count describes pose templates in this new synthesis model. It is
separate from the previous 65,216 connector designs and the 2,288,650 rooted
eight-chair placements.

## 9. Review priorities and limits

The [internal audit](audit/README.md) addresses priorities 1 and 2 below
with a fuller argument and a separate coordinate-only implementation.
It found no gap or counterexample; it does not replace external review.

1. Audit the analytic coincidence and component-filling arguments in
   Section 7. They carry the passage from a grid matching system to a solid.
2. Review the independent finite certificates and the proof that they imply
   unique recursive grouping. The checkers are independently implemented
   in places, but they are not an external mathematical review.
3. Review the [reflection extension](FOLLOWUP_REFLECTIONS.md): the local
   determinant invariant excludes mixed-handed cap contacts, and the
   component argument reduces all tilings to one handedness. The original
   hierarchy certificates continue to use the 24 proper frame orientations.
4. Do not transfer the proposed theorem to the approximate STL or to
   ordinary rectangular ports. The special curved caps are used precisely
   to identify a contact from an open surface patch.
5. Investigate simpler shapes or a polyhedral realization only after the
   exact construction has survived these checks.

The proposal does not require an unbounded tile, infinitely many features,
painted labels, external assembly instructions, or disconnected components.
It does require exact, small, nonpolyhedral boundary features. Whether the
complete argument is correct and whether an equivalent construction already
exists in the literature remain separate questions.

## 10. Reproduce

Use the locked `uv` environment from the repository root. The synthesis
compiles a small C++17 helper with `g++`.

To check the frozen candidate without rerunning the synthesis:

```sh
uv run --locked python strong/audit/verify_from_coordinates.py
uv run --locked python strong/audit/verify_caps.py
```

To reproduce the original search and exports:

```sh
uv run --locked python strong/chair_recut.py
uv run --locked python strong/chair_recut_substitution.py
uv run --locked python strong/chair_recut_stars.py
uv run --locked python strong/chair_recut_macro.py
uv run --locked python strong/verify_chair_recut.py
uv run --locked python strong/verify_chair_recut_hierarchy.py
uv run --locked python strong/chair_recut_geometry.py
uv run --locked python strong/build_recut_chair.py
node strong/verify_recut_viewer.cjs
```

The optional historical rectangular-period experiment is
`uv run --locked python strong/chair_recut_periods.py`.

To regenerate only the visualization from the frozen candidate:

```sh
uv run --locked python strong/build_recut_visualization.py
node strong/verify_recut_viewer.cjs
```

The optional real-browser check is `node strong/verify_recut_firefox.cjs`.
It uses the available Playwright and Firefox installations; set
`PLAYWRIGHT_MODULE` and `FIREFOX_PATH` to override their local paths.

The standalone viewer was also opened directly from `file://` in Firefox;
all five modes, both feature scales, separation, orbit, zoom, and a narrow
screen layout passed without page errors or external network requests.
See the [browser check](artifacts/recut_chair_firefox.json).

Artifacts: [synthesis](artifacts/chair_recut_synthesis.json),
[contact closure and patch verification](artifacts/chair_recut_verification.json),
[substitution and periodic witnesses](artifacts/chair_recut_substitution.json),
[stars](artifacts/chair_recut_stars.json), [macro contacts](artifacts/chair_recut_macro.json),
[independent hierarchy verification](artifacts/chair_recut_hierarchy_verification.json),
[exact cap data and symbolic checks](artifacts/recut_chair_exact.json),
[mesh checks](artifacts/recut_chair_mesh_verification.json).

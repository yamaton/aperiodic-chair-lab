# What the search taught us

*Research reflection, 15 September 2026.*

**Subsequent exploration:** [the recut-chair proposal](strong/RECUT_CHAIR.md)
now develops the recutting direction discussed here. It has a verified
recursive grid matching system and a proposed analytic grid-enforcement
argument. The note below records what was known before that proposal.
The subsequent [frozen-candidate audit](strong/audit/README.md) records a
further lesson: a boundary feature must fix a full local frame, and a
separate component argument must propagate those local matches globally.
Its controls expose the failure of matching only normal directions and depths.
The next [follow-up record](strong/FOLLOWUP_REFLECTIONS.md) separates local
handedness from recursive orientation information: erasing the latter in
a specified way produces a periodic solid that still forces handedness.
It also identifies three face patterns and a six-depth recoding preserving
the reference contact language.
The [local parent proof](strong/MOTIF_GROUPING.md) then identifies a short
recognition rule: six diagonal contacts mark a group center; otherwise the
notch owner is the parent. Agreement of every child on that parent proves
unique grouping. Fourteen locally fitting contacts fail a nearby face-cover
test, leaving exactly the 30-contact substitution language.
The [information-transfer analysis](strong/INFORMATION_TRANSFER.md) now shows
that preserving those rules does not require twelve distinct numerical depths:
two suffice in an explicit recoding. Five forbidden equality patterns exactly
describe the admissible twelve-amplitude family. Some distinctions govern
aligned parent contacts; others prevent parents from matching at odd offsets.
The aligned substitution reaches a symbolic fixed point after one grouping.
The [port-shape follow-up](strong/PORT_SIMPLIFICATION.md) moves orientation
information from an asymmetric polynomial factor into a scalene triangular
footprint. This lowers the surface degree from five to three while retaining
open-patch rigidity by a written argument and the same finite contact atlas.
The [dimension study](strong/PORT_DIMENSIONS.md) then removes the arbitrary
anchor coordinates from the constraints: they cancel from every cap match.
Moving the eight triangular ports yields a strictly separated 12×-width,
256×-depth witness. Width approaches 16× within the common D4 orbit family;
curved-zone inequalities permit much greater depths than the old box bounds.
These are exact-design deductions, not manufacturing tolerances or a global
optimization over all possible placements and shapes.

We set out to find one three-dimensional block that fills space but forces
every tiling to have no nonzero translation and no infinite-order screw
symmetry. **We have not found that block.** We have, however, learned things
that change how another attempt should be designed.

This note records those lessons, their arguments, and their limits. “Learned
here” means that the investigation brought them into focus; it does **not**
assert that they are new to mathematics. The underlying SCD, Wang-tile, and
chair constructions belong to the researchers credited in the linked reports.
Our contribution here is the particular exploration, its certificates, and
the deductions we made while testing it. We have not conducted a priority
search for these deductions.

## 1. Eliminating screws can be a consequence of controlling orientations

The SCD biprism gave us a concrete space filling without translation symmetry,
but its layers can repeat under a rotation combined with a vertical shift.
An irrational turning angle prevents a translation from emerging after a
finite number of layers; it does not prevent a screw symmetry.

The useful change of viewpoint was this:

> For a polyhedral tiling with only finitely many tile orientations, absence
> of translation symmetry already implies that the entire symmetry group is
> finite.

Here a symmetry must preserve the tiling as a collection of tiles. To see the
claim, fix one tile. The linear part of a symmetry takes its orientation to
one of finitely many orientations, with only finitely many choices coming
from the tile's own symmetries. There are therefore finitely many possible
linear parts. Two isometries with the same linear part differ by a
translation. If nonzero translation symmetries are absent, there can be at
most one symmetry for each linear part.

In a cubic frame, a screw with a quarter-turn becomes a translation after
four repetitions. This is the simplest picture of the argument.

**Why retain this:** a construction can separate two jobs: force a finite
set of orientations, then forbid translations. It need not fight every
possible screw directly. The difficult qualification is *force*: displaying
one tiling in a cubic frame does not prove that every tiling uses that frame.

See the [finite-orientation argument](strong/README.md#1-a-mechanism-that-removes-screw-symmetry).

## 2. Two intersecting planar systems can remove the third-dimensional period

Extruding a planar aperiodic tiling leaves a repeat in the extrusion
direction. We found a clean way to remove that freedom at the level of
matching rules.

Take two planar aperiodic Wang tilings, `A(i,j)` and `B(i,k)`, and put the pair

```text
C(i,j,k) = (A(i,j), B(i,k))
```

at each cubic cell. Local rules copy `A` unchanged in the `k` direction and
`B` unchanged in the `j` direction, while enforcing each planar tiling's
matching conditions.

A translation `(p,q,r)` preserving this configuration would make `(p,q)` a
period of `A` and `(p,r)` a period of `B`. Planar aperiodicity forces both
pairs to vanish, hence `p=q=r=0`. Conversely, any two valid infinite planar
tilings give a valid infinite three-dimensional configuration. Together
with the finite frame, this supplies the desired symmetry conclusion.

Using the eleven Jeandel–Rao tiles produces 121 labelled cube states.
**That is a matching system, not one geometric block.** The unresolved step
is making one solid enforce these states and their synchronization in every
tiling. Rotations of a single block in a proper cubic frame provide at most
24 orientations, so they cannot directly stand for the full 121-state
catalogue. Clusters or other encodings could have more possibilities.

**Why retain this:** we have a precise logical structure that would suffice.
Future geometry can be assessed against it, rather than merely against the
appearance of nonrepetition.

Details and attribution: [crossed-plane construction](strong/README.md#4-a-positive-construction-at-the-matching-rule-level).

## 3. A hidden periodic tiling can be much smaller than the box used to find it

Some connector designs resisted small cubic repeat tests. That was initially
encouraging, but their repeats had slanted fundamental regions.

One rejected block admits the translation lattice generated by

```text
(1,1,0), (2,-2,0), (0,0,3).
```

Its fundamental volume is only 12 block cells. A much larger cubic witness
had obscured this small repeat. We checked an associated rectangular repeat
by exact voxel occupancy, including the connectors across its boundaries.

This led to searching integer lattices directly, using Hermite normal form
to list distinct sublattices. There are 1,325 sublattices of index at most 12
in the bounded enumeration we used.

There was also a useful implementation trap: fixing one block's orientation
can be a valid symmetry reduction in a cubic test region, but fail on an
oblique quotient. Rotating the blocks may rotate the period lattice into a
different test problem. The oblique solver therefore leaves that orientation
unfixed.

**Why retain this:** failure to find a short axis-aligned repeat is weak
evidence. The geometry of the period lattice matters, and a solver's symmetry
reductions must preserve the boundary conditions as well as the tile rules.

Evidence: [periodic solid](strong/artifacts/geometric_counterexample.json)
and [oblique search](strong/SECOND_PASS.md#2-searching-for-slanted-repeats-directly).

## 4. More face distinctions do not automatically buy aperiodicity

A cube with one arbitrary color on each face always admits a periodic
matching arrangement if proper rotations are allowed. At cell `(i,j,k)`,
use the orientation

```text
diag((-1)^(i+j), (-1)^(j+k), (-1)^(i+k)).
```

Its determinant is positive. Across each interface, both cubes present the
same original face, so its color matches itself. The arrangement repeats
after two cells along every axis, however the six colors were chosen.

Directed, displaced tabs and pockets contain additional information: they
can constrain how neighboring faces twist relative to each other. We
explored several such families, including interfaces whose tab-and-pocket
midpoint was itself displaced.

Across the recorded families, **65,216 designs** were classified:

| Outcome | Designs |
|---|---:|
| Explicit periodic witness | 22,132 |
| Impossible in the prescribed aligned cubic-grid model | 43,084 |
| Unresolved within those families | 0 |

The counts do not describe all possible connectors or all solids. Nor does
grid impossibility exclude arbitrary staggered or differently oriented
Euclidean tilings. A verified physical periodic packing, however, does
disqualify its shape: one periodic tiling is enough.

**Why retain this:** the kind of information carried by a boundary matters
more than the number of visually distinct features. Added restrictions can
also destroy tilability before they destroy periodicity. These particular
searches ended on those two sides without producing a candidate between them.

Evidence: [combined results](strong/artifacts/research_summary.json) and
[connector models](strong/README.md#2-actual-single-solid-search-families).

## 5. Filler ownership is a mathematical constraint

A tempting route starts with a known aperiodic pair and glues its pieces
together into congruent larger blocks. In the chair-and-cross construction
we studied, volume balance requires four modified chairs for every three
cross fillers. This makes four chairs plus three crosses, or eight plus six,
natural first candidates.

But a volume balance is only an average. It says nothing about whether the
same rigid attachment pattern can assign every filler to exactly one block.

For the standard eight-chair substitution group, that assignment meets a
parity obstruction. In suitable integer coordinates, the group centers have
the form

```text
C = O ∪ 2C′,
O = all triples of odd integers,
E = all triples of even integers.
```

Every site of `O` is occupied. Some sites of `E` are occupied and others
require fillers. The extra whole crosses would have to sit at a fixed set
of offsets from each group center, rotated with that group.

Signed coordinate permutations preserve the classes “all even,” “all odd,”
and “mixed parity.” Consequently:

- An all-even offset collides with an occupied odd site at every odd center.
- An all-odd offset collides with an occupied odd site at every even center.
- A mixed-parity offset reaches only mixed-parity sites from either kind of
  center, so it cannot fill the empty all-even sites.

No fixed whole-cross attachment pattern works, **regardless of its reach**.
Allowing longer arms cannot repair this obstruction. The argument is
conditional on these standard groups, their hierarchical placement, and
whole fillers at the specified sites; it says nothing comparable about
pieces that have been cut up and reassigned.

**Why retain this:** empty space is not a neutral leftover. Its locations
carry hierarchical information, and deciding which congruent block owns
that space can be the central obstruction.

Derivation and attribution: [attachment parity argument](strong/OPEN_FUSION.md#why-extending-the-attachment-range-cannot-rescue-this-design).

## 6. Finite exclusions become useful when their boundary assumptions are proved

An early fusion test kept clusters inside a finite supertile. A failure
there could simply mean that a valid infinite grouping crosses its boundary.

We replaced that restriction with a required interior core and an optional
surrounding halo. For a face-connected group of `k` chairs, every member is
at most `k−1` adjacency steps from any chosen member. Sufficient padding
therefore contains every possible group touching the core. We require exact
coverage of the core and forbid overlaps everywhere, while leaving halo
coverage optional.

This turns a finite failure into a genuine obstruction for the specified
grouping problem: a placement outside the patch cannot rescue the core.
Applying it to infinite substitution tilings also uses the fact that those
tilings contain the tested supertile patches.

For four-chair groups, all 206 proper congruence classes at the chosen
anchor failed. The larger eight-chair screen enumerated **2,288,650 rooted
placements**. Twelve shapes could occur at every core chair individually;
only the standard substitution group could cover them simultaneously.

These are whole-chair, face-connected groupings under proper rotations,
preserving the chair decomposition. The rooted-placement count is not a
count of distinct solid designs and is not added to the connector total.

**Why retain this:** the distance-to-boundary argument is part of the result,
not bookkeeping. So is the distinction between “can occur everywhere” and
“can be chosen everywhere without conflicts.”

Evidence: [four-chair core](strong/OPEN_FUSION.md#1-four-chair-clusters-can-now-cross-the-boundary)
and [eight-chair enumeration](strong/EIGHT_CHAIRS.md).

## 7. The best result of a large computation can be a small explanation

One of the twelve eight-chair survivors produced a relatively expensive
independent exclusion. Extracting a smaller certificate revealed three
required chairs. Exactly three possible cluster occurrences touch them:

| Occurrence | First chair | Second chair | Third chair |
|---|---|---|---|
| A | covered | covered | — |
| B | covered | — | covered |
| C | — | covered | covered |

Writing `a,b,c` for the decisions to select those occurrences, exact coverage
would require

```text
a+b=1,  a+c=1,  b+c=1.
```

Summing gives `2(a+b+c)=3`, impossible for integers. The padded neighborhood
and a separate enumeration establish that no omitted occurrence touches the
three chairs.

This is more informative than the solver's verdict. It identifies a parity
invariant: every available group covers an even number of the selected
sites, but there are an odd number to cover.

**Why retain this:** computation can locate the obstruction, after which
certificate reduction can reveal the reason. Finding small weighted or
modular counting obstructions is a concrete strategy for future searches;
we have demonstrated the parity version in this case.

Evidence: [three-chair certificate](strong/artifacts/eight_chair_small_certificate.json)
and [independent verification](strong/artifacts/eight_chair_verification.json).

## 8. Fusion can erase the information that forced the hierarchy

The only successful coarse eight-chair grouping has the shape of a 4×4×4
cube with a 2×2×2 corner removed. It appears naturally in the aperiodic
hierarchy. Yet its unmarked union has a periodic translational tiling.

There is a short explanation. For the seven-cube chair
`{0,1}³` with `(1,1,1)` removed, the map

```text
(x,y,z) ↦ x+2y+4z (mod 7)
```

takes its seven cubes to all seven residues exactly once. Translations by
the kernel lattice therefore tile the integer grid. Scaling by two gives
the 56-cube coarse survivor, with period lattice

```text
(14,0,0), (-4,2,0), (-8,0,2).
```

The determinant is 56, and exact quotient occupancy confirms the packing.
This is a statement about the unmarked coarse shape, not a disproof of
every hypothetical keyed modification.

**Why retain this:** being a cluster in an aperiodic tiling does not make a
shape aperiodic. Once internal boundaries or markings disappear, the shape
may admit new arrangements. Any successful fusion must preserve enough
information on its remaining geometry to force the intended structure.

Evidence: [periodic control](strong/EIGHT_CHAIRS.md#3-the-survivor-has-a-periodic-unmarked-packing).

## 9. What these lessons suggest next

The strongest change in our working hypothesis concerns **recutting and
redistributing material**. Rigidly attaching whole filler pieces makes every
congruent group inherit the same ownership pattern, which the parity
argument defeats. A new dissection could change what counts as a group
center, split filler responsibilities across boundaries, or preserve
hierarchical information on newly exposed surfaces.

This is a direction, not a construction. We have no coordinates for such a
block and no proof that recutting can accomplish it. A useful next attempt
should answer a specific question from the following list.

| Question | What would constitute progress? |
|---|---|
| Can new cuts escape the filler parity obstruction? | A specified dissection with congruent resulting pieces and exact coverage. |
| Can one solid represent two intersecting aperiodic fields? | A geometric encoding with a decoding argument for every allowed arrangement. |
| Can geometry force the finite frame? | A proof excluding unintended relative orientations and offsets. |
| Can a hierarchy survive fusion? | Boundary features that force recovery of the intended groups in every tiling. |
| Can other failed covers yield small invariants? | Independently checked counting or modular certificates. |

Larger whole-piece groups also remain open. Within the tested face-connected
fusion route, volume balance and the four- and eight-chair exclusions make
12 chairs plus 9 crosses the next possible size. This is a lower bound for
that route, not for arbitrary monotiles, and there is no evidence yet that
increasing the size resolves its structural difficulties.

## 10. What a successful conclusion would still have to establish

Three obligations should remain separate throughout further work:

1. **Existence:** one congruent solid really tiles all of three-dimensional
   space.
2. **Enforcement:** every tiling of that solid recovers the intended matching
   rules or hierarchy; alternative assemblies cannot bypass them.
3. **Symmetry:** that forced structure excludes nonzero translations and
   infinite-order screws.

A finite patch can test an implementation and expose contradictions. A
periodic witness can reject a candidate outright. But a large patch without
an observed repeat does not settle any of these three obligations by itself.

The lasting result of this exploration is a clearer account of where the
difficulty lies: enforcing an infinite structure with the boundary of one
congruent solid, while still allowing space to be filled. We now have a
sufficient symmetry mechanism, several precisely bounded obstructions, and
small certificates explaining some failures. Those are useful constraints
on the next idea even though the requested block remains unfound.

### Evidence and reproducibility

This is a synthesis of the completed experiments, not a new search run.
The linked reports contain the models, limitations, source attribution,
artifacts, and reproduction commands. Python work uses the locked `uv`
environment; representative checks are:

```sh
uv run --locked python strong/verify_offsets.py
uv run --locked python strong/verify_open_chairs.py
uv run --locked python strong/verify_eight_chairs.py
```

Start with the [combined result index](strong/artifacts/research_summary.json)
for counts, the [strong aperiodicity report](strong/README.md) for the logical
construction, and the [eight-chair report](strong/EIGHT_CHAIRS.md) for the
latest verified exclusions.

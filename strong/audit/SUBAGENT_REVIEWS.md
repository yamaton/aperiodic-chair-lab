# Three adversarial subagent reviews

*15 September 2026.*

**Outcome:** none of three separately started reviewers found a substantive
defect in the proposed theorem under its stated assumptions. They identified
three proof clarifications, now incorporated in the [audit](README.md), and
produced an additional implementation checking the finite calculations.

This record summarizes their returned reviews and the primary agent's
responses. These were AI subagents using the same model, each started with
fresh context and a bounded review assignment. They did not receive the
conversation history or one another's findings before submitting their
initial reviews. They did read the supplied proposal and audit, including
their stated conclusions. Their agreement is **not** three independent
human endorsements, formal verification, or evidence of novelty; common
model and mathematical blind spots remain possible.

## Material reviewed

All reviewers received the same frozen construction:

```text
candidate.json SHA-256:
95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54

archived proposal.md SHA-256:
d7280e4c04ddeaf2db51a06da057137d9a42b720755b274a7e8350eafbf8c701
```

The initial coordinate checker and audit document hashes were:

```text
verify_from_coordinates.py:
d1450f8a83427ab324da9f7c4f2b847fc17159a70d0bf9a7659ded3833064cfe

README.md before review amendments:
446640952f74dd10e3e907518a4db698ac9a54a2ec94e93d25733c09a8d296d4
```

The reviewers were instructed to seek counterexamples, incomplete
enumerations, and hidden assumptions; to distinguish actual gaps from
missing exposition; to use `uv` for Python; and to leave repository files
unchanged. The frozen construction remains unchanged after their reviews.

## Review 1: arbitrary Euclidean placements and cap geometry

Reviewer: `/root/geometry_review`.

**Verdict:** no counterexample or fatal gap found in the passage from
arbitrary Euclidean tilings to a common integer grid.

The reviewer independently rederived:

- Extension of open graph coincidence by polynomial division.
- The exhaustive five-line classification and recovery of the bounded
  square, center, and ordered tangent axes.
- Local finiteness and mandatory open cap contact, without assuming a grid.
- Opposite interior sides, opposite keys, and integral relative placement.
- Propagation of a matched component to every coarse cube.

A separate exact-rational check confirmed that all 24 actual exposed coarse
faces carry exactly the eight specified ports.

### G1. Polynomial restriction wording — corrected

The first audit said a nonzero polynomial restricted to the cap cannot
vanish on an open set. As written, that is imprecise: a nonzero **ambient**
polynomial can vanish on the entire cap, as its defining polynomial does.

The intended condition is a pullback to the cap's two parameters that is
**not identically zero**. The revised §3D first uses the finite closed cover
argument to obtain an open boundary-patch coincidence, then states the
polynomial condition correctly. The reviewer classified this as a wording
clarification, with no surviving obstruction to the argument.

### G2. Global feature separation — proof expanded

The first finite clearance check concerns one tile. The physical filling
argument also needs feature separation across the entire common grid.
The reviewer supplied a complete case split with positive lower bounds:

| Feature locations | Coordinate separation |
|---|---:|
| Same unit face | `3/32` |
| Distinct coplanar faces | `19/32` |
| Distinct parallel planes | `17779/17920` |
| Perpendicular faces | `10499/35840` |

Opposing matching features share a box. Outside all feature boxes, the
physical tiling is the coarse-cube partition. Inside a box, its two owners
occupy complementary closed sides of one graph, so no holes remain.

This proof is now in §3F, and `verify_caps.py` checks the additional rational
bounds. The reviewer judged this missing exposition fully resolvable with
the existing construction, without an additional hypothesis.

**Limits:** this review did not independently verify the finite hierarchy,
reflected-copy model, approximate mesh, or priority.

## Review 2: finite contact enumeration and recursive grouping

Reviewer: `/root/finite_review`.

**Verdict:** no substantive defect found in the finite grid verification.

Besides running a staged copy of the original verifier, the reviewer wrote
[reviewer_crosscheck.py](reviewer_crosscheck.py). It independently generates:

- Rotations from signed permutations.
- Rotated cubes from their centers.
- Contact translations from adjacent cube pairs, avoiding the original
  bounding-box enumeration.
- Pair conflicts from direct cube and port comparisons.
- Complete neighborhoods by choosing the first uncovered face.
- Macro boundaries from coarse-cube ownership.

It imports `verify_from_coordinates.py` **for comparisons against fresh
results**, not to implement those alternate calculations. It reads no
previous result JSON. This is an independent cross-check implementation,
not a completely dependency-free second verifier.

| Independent calculation | Result |
|---|---:|
| Fine geometric / legal contacts | 1,194 / 44 |
| Complete neighborhoods | 33 |
| Coexisting pairs among eight competing group roles | 0 of 28 |
| Macro geometric / legal contacts | 6,801 / 44 |
| All macro placements and compatibility flags equal original | Yes |
| All compatible macro offsets even; deflation reproduces rules | Yes |

The reviewer separately checked the forcing implication for every
neighborhood and the geometric conflict for every pair of competing roles.
Direct substitution expansion passed at levels 1, 2, and 3:

| Level | Tiles | Coarse cubes | Matched internal unit faces |
|---|---:|---:|---:|
| 1 | 8 | 56 | 48 |
| 2 | 64 | 448 | 576 |
| 3 | 512 | 3,584 | 5,376 |

Preserved [output](reviewer_crosscheck_output.txt) and script hash:

```text
035956c021509daf96cc994b41bc650834db3668e26d00ed61ea306193f1d25a
```

Reproduce from the repository root:

```sh
uv run --locked python strong/audit/reviewer_crosscheck.py
```

**Scope observation:** the coordinate checker does not inspect the cap
polynomial or enforce its height clearance. Its success alone certifies
only the grid system. This is intentional and documented: the cap checker
and geometric proof carry the additional physical obligations.

## Review 3: complete theorem and hidden assumptions

Reviewer: `/root/theorem_review`.

**Verdict:** no genuine defect found in the full scoped logical chain,
conditional on correct finite enumerations.

This reviewer began from the archived proposal, inspected the complete
coordinate-checker source, and independently checked the rational solid
data, feature isolation, key multiplicities, proper child rotations, and
the partition of `2L` into 56 cubes. The review covered whole-space
existence by compactness, cap rigidity, global grid propagation, conservative
neighborhood forcing, unique grouping, unbounded deflation, and finite
tile-preserving symmetry group.

### T1. Exclude off-center self-isometries — clarified

The coordinate check excludes nonidentity keyed cube rotations, but the
physical pose argument should also explain why a self-isometry cannot have
a displaced center. Open planar patches determine the three normal axes;
planes containing those patches occur at levels exactly `{-1,0,1}`. Preserving
those finite level sets forces zero translation. Thus the proper physical
stabilizer reduces to the already checked cube rotations. This explanation
has been added to §4 of the audit.

### Essential scope retained

- Only translated and properly rotated copies of one handedness are covered.
- The solid has the exact polynomial boundary, not an approximate mesh.
- Symmetry means an isometry preserving the collection of tiles.

Omitting these conditions would overstate the reviewed result. No such
omission was found in the audit's theorem statement.

**Limits:** the reviewer read the finite algorithms but did not independently
regenerate their full enumerations. The largest remaining uncertainty it
identified was a common modeling or implementation mistake in those steps;
Review 2 supplies an additional attack on that risk. Novelty and the
reflected-copy model were not examined by this reviewer.

## Disposition

All three requested clarifications have been incorporated. The amended cap
checker passes through `uv`. No change to the candidate geometry, key data,
substitution, or claimed scope was needed.

The geometry reviewer also checked the amendments and confirmed that G1/G2
were resolved and the self-isometry argument was valid. Its follow-up caught
two terminology issues, also corrected: the comparison planes in the
perpendicular-face case are perpendicular to the first face; and a plane
containing a reentrant level-0 patch is not a supporting plane of the whole
solid.

A fourth subagent completed a separate [literature review](LITERATURE_REVIEW.md).
It found close prior art, particularly Goodman-Strauss's 1999 pair, but no
source identifying the exact one-chair rule system. Priority remains
unresolved. None of these reviews replaces external expert review.

## Subsequent geometry review: reflected copies, 15–16 September

The geometry reviewer was reactivated for the bounded question of whether
the new single-cap determinant invariant extends the proposal to arbitrary
congruent copies. It independently read the frozen JSON and recomputed the
frame triple products: eight occurrences per signed key, one chirality per
key, opposite chiralities for opposite keys, and 1,536 proper opposite-key
correspondences with no improper ones.

It confirmed that polynomial cap rigidity does not assume determinant +1;
a reflection preserves signed height relative to the transformed outward
normal. Opposite interiors require opposite signed keys. Thus a matching
cap forces equal placement handedness. The existing component-filling
argument makes handedness global; a global reflection reduces the remaining
case to the proper-copy hierarchy. It found no gap in this extension.

This reviewer checked the invariant separately and read the reflection
enumerator, but did not rerun that full enumerator. The independent raw-data
enumeration is [check_reflections.py](check_reflections.py). The [follow-up
record](../FOLLOWUP_REFLECTIONS.md) gives the argument and all counts.
The frozen candidate is unchanged; the proposed scope is extended. Exact
curved geometry and the need for external mathematical review remain.

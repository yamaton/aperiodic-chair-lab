# Attempt register

The main objective remains open. Counts below describe the indicated model,
not all possible markings or solids. Every experiment will preserve its
results in `artifacts/` with a reproduction command.

| ID | Family / task | Status | Next decision |
|---|---|---|---|
| Q000 | Exact Conway–Radin child reconstruction | Passed | 8 proper maps, 28 separation certificates, 14 contacts, 40 face-coverage checks, interior address |
| Q001 | One constant matching symbol per carrier face | Rejected | Actual two-prism periodic counterexample |
| Q002 | Whole-face scalar polynomial markings | Rejected for degrees 0–6 | Only two constant equality classes; signed kernel zero |
| Q002b | Arbitrary pointwise markings, fixed proper child poses | Rejected by written proof + exact certificate | Six odd-length contact paths imply every periodic-cell contact |
| Q003 | Multiple decorated types via hereditary panels | Geometry hypotheses checked; explicit decorations pending | 60 panels, 38 vertices, 96 segments pass the finite audit |
| Q004 | All 256 child words, face polynomials degree <=2 | Rejected | All 512 equality/opposite families admit periodic controls after at most two levels |
| Q005 | 60-panel constants, all 256 child words | Rejected in positive-area model | Two remaining families admit a four-prism periodic control |
| Q006 | Substitution-compatible pair poses | Rejected | Closed 91-pose atlas admits a 24-prism periodic tiling |
| Q007 | Root-star overapproximation | Unknown at 10,000-model limit | Preserved as incomplete; not needed to reject Q006 |
| Q008 | Complete face-star rules | Rejected for rules accepting the quaquaversal language | A periodic 192-prism cell uses only observed stars |
| Q009 | Closed stars including edge/vertex contacts | In progress | Level-4 sample has 741 stars; 31 of 62 periodic control stars remain unobserved, hence unresolved |
| Q010 | Pointwise function groupoids for reflected words | Next attempt | Retain panel-frame permutations, not just constant values |

## Q000 — geometry

`uv run --locked python strong/quaquaversal/verify_geometry.py`

Exact arithmetic in rational coordinates with physical metric diag(3,1,1).
All children lie in the parent. SAT covectors separate every pair's interiors,
and volumes sum to the parent's volume. Every child's face has full exact area
coverage by internal contacts or a parent boundary. The paper's address
(2B,2B,4A) gives a scale-1/8 interior child with identity rotation, providing
the standard expanding-patch existence mechanism for the unmarked rule.
Evidence: `artifacts/geometry_and_constant_rules.json`.

## Q001 — constant face information fails

The two-prism periodic control requires only face pairs already present in
the first-level assembly. Thus even an arbitrary allowed-pair predicate on
the five face identities cannot distinguish this periodic filling. Equality
colors reduce to two classes {bottom,top,long} and {square,hypotenuse}.
Constant signed-relief equations force all five values to zero.
This rejects the whole stated family, not only one coloring.

## Q002 — polynomial trial, followed by a stronger deduction

`uv run --locked python strong/quaquaversal/polynomial_rules.py`

Exact coefficient nullspaces were computed for total degrees 0 through 6.
Every equality kernel has dimension 2, with the constant bases from Q001;
every opposite-sign kernel has dimension 0. No polynomial degree beyond 6
was inferred from that finite experiment.

Instead Q002b proves the stronger arbitrary-function obstruction in
[PERIODIC_OBSTRUCTION.md](PERIODIC_OBSTRUCTION.md), checked by
`uv run --locked python strong/quaquaversal/periodic_obstruction.py`.
This closes the fixed-pose, pointwise one-decoration family and motivates
changing the family rather than indefinitely increasing polynomial degree.

## Q003 — multiple decorations and the general theorem

`uv run --locked python strong/quaquaversal/refine_vertices.py`

Starting from the six carrier vertices, propagate sibling incidence and
hereditary incidence into canonical tile coordinates. Three further points
are forced, and the next round adds none. They are (1/2,1/2,0), (1/2,0,1/2),
and (1/2,1/2,1). This is a necessary-vertex check, **not** sufficient
verification of hereditary panel hypotheses or an explicit rule set.
Evidence: `artifacts/vertex_refinement.json`.

## Q004 — allow distinct handedness at child positions

`uv run --locked python strong/quaquaversal/reflected_search.py`

The carrier's improper self-symmetry z -> 1−z leaves its support fixed but
changes a decoration's handedness. Enumerate all 256 child words, ordered
(1A,2A,3A,4A,1B,2B,3B,4B). This changes an assumption of Q002b.
At degrees <=2, only masks 111 and 144 have nonzero opposite-sign kernels,
of dimensions 1,3,6 at degrees 0,1,2. They are complementary words.
Mask 144 reflects 1B and 4B. Inspecting the basis reveals that this freedom
is supported entirely on an exterior triangular face unused by siblings.
It is not evidence for an infinite matching-rule construction.

`uv run --locked python strong/quaquaversal/reflected_controls.py`

Of 512 degree-two families (256 words times equality/opposite), 472 admit
a two-prism periodic cell for **every** marking in the family. The other
40 require further work, including 38 equality families and two opposite
families. Each cell allows either handedness independently at its two sites.
No failed finite counterexample search is called aperiodicity.

`uv run --locked python strong/quaquaversal/reflected_second_level.py`

This applies the stationary child word twice, reconstructs 64 actual copies,
extracts every area contact, and rechecks the 40 unresolved polynomial
families. All 38 equality kernels collapse to two constant classes; both
signed kernels become zero. All four handedness choices of the two-prism
cell are then accepted. This rejects all 512 degree-two families, not
arbitrary functions under reflected child words.

## Q003 follow-up — panel incidence matters

The first 51-panel refinement had ten missing vertex incidences despite
passing area comparisons. It remains as a failed attempt. Seeding lines at
the missing points yields 60 panels. Area, vertex and segment checks pass;
see [MULTITYPE_ROUTE.md](MULTITYPE_ROUTE.md) for counts and commands.
An explicit decorated inventory and its reduction to one shape remain work.

## Q005 — piecewise constants and a delayed periodic counterexample

```sh
uv run --locked python strong/quaquaversal/piecewise_search.py
uv run --locked python strong/quaquaversal/piecewise_deeper.py
uv run --locked python strong/quaquaversal/piecewise_periodic_grid.py
```

Use one scalar per panel, imposing positive-area contacts as equality or
opposite-sign equations. Only equality masks 111 and 144 escape the
two-prism tests after two levels. Both retain three classes at level 3
(512 children), including checkerboard-like square/hypotenuse-face patterns.

Two boxes along u give a counterexample: both prisms in one box use one
handedness; both in the next use the other. This four-prism pattern repeats.
All 20 directed contacts were replayed against exact panel equations after
SAT found the witness. Because the labels are equality classes, it works
for every choice of the three values, including coalesced colors.
Independent edge/vertex labels are outside this family.

## Q006–Q008 — stronger neighborhoods

[RELATIVE_POSE_RULES.md](RELATIVE_POSE_RULES.md) gives the 91-pose closure,
the 24-prism periodic reflection filling, and the full-face-star control.
Q007's 10,000 models impose only root/neighbor atlas legality and neighbor
nonoverlap. This capped enumeration does not certify extension to a tiling.

For Q008, a proper level-3 patch (512 prisms) supplies 80 complete face-stars.
The once-subdivided periodic reflection tiling has 192 prisms and eight
distinct face-stars, all observed in the sample. This is a positive periodic
witness, not an inference from a missing pattern.
Evidence: `artifacts/star_language_3_1.json`.

## Next attempts

- Q009: include edge-only and vertex-only neighbors. Test closed root stars
  against the subdivided periodic controls. If every closed star of a
  periodic tiling occurs in the intended language, try proving that further
  subdivisions give legal patches at every fixed radius. This could reject
  finite-radius rules on the unmarked language; it is not established yet.
- Q010: extend Q002b to reflected words by retaining the actual affine map
  between panels. Compose these identifications, with domain certificates,
  to try deriving periodic target maps for arbitrary functions. First check
  whole-panel compatibility for reflected words; do not assume it.
- Q003: construct explicit skeleton/vertex-wire labels for the multiple-type
  route, then investigate a recut which preserves that information.

## Full checkpoint reproduction

`uv run --locked python strong/quaquaversal/reproduce.py`

This runs 18 commands in dependency order and checks input hashes. Expected
failed attempts are preserved and checked as such. It is a finite
reproduction command, not an unattended discovery process or a proof of the
unresolved objective.

## Q009 initial probe

`uv run --locked python strong/quaquaversal/closed_stars.py`

Closed intersection uses exact separating-axis tests, with rational spatial
bins for a conservative broad phase. Only strictly interior sample tiles
are used, so their whole closed neighborhoods are present. At sample level
3, 95 distinct neighborhoods are observed; none of the eight closed-star
types in the periodic level-1 control is observed. This is **unknown**, not
a proof that these stars never occur. The next probe increased the sample
to level 4 (4096 tiles) and the periodic control to level 2 (1536 tiles):
741 sample stars and 62 periodic stars occur, of which 31 remain unobserved.
This is still unknown. Preserve both JSON files; the samples differ, so
neither count is an exhaustive language census.

`uv run --locked python strong/quaquaversal/closed_stars.py --sample-level 4 --periodic-level 2`

[SYMMETRY_LEMMA.md](SYMMETRY_LEMMA.md) separately proves the conditional
finite-group conclusion from symmetry-preserving prism hierarchies at all
scales, using packing rather than a finite orientation assumption.

A useful next step is a substitution-closed **closed-contact** atlas,
including lower-dimensional contacts. If it stabilizes, it may certify a
specific control pair forbidden, rather than merely unobserved. A bounded
growth prefix must still be recorded as unknown.

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
| Q009 | Closed contacts and complete closed-star language | Pair rules rejected; stronger star rule remains open | 1,291 pairs admit the periodic control; 6,840 closed stars exclude it at every subdivision level >=2 |
| Q010 | Pointwise function groupoids for reflected words | Rejected for all 512 stated families | Arbitrary equality/scalar-opposite functions admit two- or four-prism periodic witnesses |
| Q011 | Recognize and desubstitute the closed-star rule | One-level grouping supported; recursive legality open | 41,719 sibling checks pass; 52,485 extra parent-neighborhood tuples remain unresolved |
| Q012 | Extend candidate parent neighborhoods through external stars | Exact filters reduce extras; recursive legality open | 3,025 extra root tuples and 9,357 nonlanguage parent covers remain |
| Q013 | Condition exterior stars on each complete parent cover | Partial exclusion | 3,373 covers rejected; 5,984 remain unresolved |
| Q014 | Repeated necessarily present exterior neighbors | Partial exclusion | Four layers leave 744 covers, with full survivor-domain audits |
| Q015 | Geometric pair tests in expanded forced patches | Partial exclusion | 17 of the 1,076 layer-3 patches rejected by eight intersection witnesses |
| Q016 | Arc consistency in expanded forced patches | Partial exclusion | A further forced layer and arc round now leave 246 covers |
| Q017 | Six binary-choice pilot cases | No additional parent exclusions | 12 branches; two failures belong to a parent already rejected without branching |
| Q018 | Simultaneous optional-neighbor presence | Pilot insufficient | Six satisfiable assignments each have a certified forbidden geometric pair |
| Q019 | Add sampled interior non-overlap | Pilot insufficient | 209,371 audited pair clauses; all six pilot cases remain satisfiable |
| Q020 | Complete-star extension of optional neighbors | Six verified choice cuts | All six Q019 assignments fail; each yields a two-choice forbidden conjunction, not a parent exclusion |
| Q021 | Learn immediate complete-neighbor-star cuts | Six revised assignments survive | 117 new audited binary cuts; original 246 parent cases remain unresolved |
| Q022 | Propagate between optional neighbors | All six Q021 assignments eventually rejected | Five immediate arc cuts of lengths 3, 3, 3, 5, 2; the last assignment fails a deeper layer |
| Q023 | Integrate neighbor arcs into SAT refinement | Six revised finite models survive | 34 further audited cuts; all 45,403 final domains independently agree |
| Q024 | Apply learned cuts to the full parent frontier | Domains narrowed; no new parent exclusions | 77 star values removed in 18 cases, followed by 150 arc reductions; 246 cases remain |
| Q025 | Extend the narrowed full fine frontier | Partial exclusion | Forced layer rejects 11 and fine arcs reject 30 more: 246 → 235 → 205 |
| Q026 | Choice proofs through multiple forced/arc layers | Eight-choice cut independently verified | 163 cuts total; the new proof also rejects Q023 model 5, not its whole parent case |
| Q027 | Necessary compatibility in the parent-star vocabulary | Partial exclusion | Coarse support removes 28 further cases after Q025, leaving 177 unresolved parents |
| Q028 | Reapply cuts and extend the full fine frontier | Partial exclusion | Two star values removed; forced layer leaves 170 and fine arcs leave 130 |
| Q029 | Conditional arcs among neighbors of each parent star | Partial exclusion | Initial 17 exclusions overlap fine results; feedback on 130 extras removes 48 more, leaving 82 |
| Q030 | Recognize siblings in the enlarged parent language | One grouping step verified for 7,000-star rule | Supports two nested groupings for original-rule tilings; all-scale closure remains open |
| Q031 | Eight-sibling CSP for each of 160 extra stars | No additional exclusions | All 160 have checked tuples in the finite relaxation; no tiling claim |
| Q032 | Expand all 82 conditional parent patches by one forced layer, then propagate arcs | No additional exclusions | 15,782 audited domain reductions; all 82 survive; explicit parent-scale continuation saved |

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

- Research is held at the Q032 checkpoint for the user's requested review;
  see [the Japanese status note](RESEARCH_STATUS_JA.md).
- On resumption, continue the parent-scale `coarse_arc_seed_1.json`, with
  82 live cases, using the explicit atlas/rule propagators. The first wider
  layer excluded none. Keep coarse world IDs separate from fine cut IDs;
  the fine frontier is still `coarse_arc_frontier_2.json`.
  [CONDITIONAL_PARENT_PATCHES.md](CONDITIONAL_PARENT_PATCHES.md) gives the
  two-level grouping, failed sibling-CSP attempt and wider-layer result.
  Any coarse feedback must use a complete necessary frontier.
- Extend the SAT models using [layered domain certificates](DOMAIN_CERTIFICATES.md).
  Q026 now lifts the old two-layer failure to eight original choices, also
  refuting Q023 model 5. Preserve finite limits as unknown and retain tile
  presence dependencies when removing premises.
- Q003: construct explicit skeleton/vertex-wire labels for the multiple-type
  route, then investigate a recut which preserves that information.

## Q009 follow-up — closed contact and star closure

[CLOSED_STAR_RULES.md](CLOSED_STAR_RULES.md) gives definitions, the written
closure argument, audit scope and commands. Pair closure stabilizes at
1,291 poses (91 face, 247 edge-only, 953 point-only), independently checked
by edge clipping. The 24-prism periodic control satisfies this entire atlas.
The interior-supertiling closed-star language instead closes at 6,840 types.
The periodic control has a reachable bad-star self-loop, so no subdivision
at level >=2 makes it legal for the closed-star rule. This rejects one
control family, not all periodic tilings.

## Q010 — pointwise identifications retain frame information

[POINTWISE_GROUPOIDS.md](POINTWISE_GROUPOIDS.md) records the stronger
obstruction for arbitrary equality functions and real scalar opposite-sign
functions. All 256 stationary reflected words, in both matching conventions,
have exact periodic witnesses. Equality words 111/144 require four prisms;
the other 510 cases require two. Certificate replay checks 243,360 map
derivations and 5,140 periodic contacts. Arbitrary involutions with multiple
fixed symbols are outside the scalar zero-cycle argument.

## Q011 — one recognizable level, not yet recursive legality

Each of 6,840 allowed closed stars determines a unique child role. All
41,719 root/touching-sibling cases agree on the sibling role after comparing
common-neighbor fingerprints. The connected sibling graph then gives one
partition into eight-child parents, as argued in CLOSED_STAR_RULES.md.
The parent tiling has not been proved to obey the same rule.

A complete join of the eight child-star domains produces 58,740 tuples,
including all 6,255 tuples arising from legal parent stars. The remaining
52,485 are necessary local candidates, not tilings. Adding fingerprints
between disjoint sibling centers rejects none. This failed strengthening
is preserved in `parent_join_filter.json`; Q012 now extends the neighborhood.

## Full checkpoint reproduction

[PARENT_EXTENSION.md](PARENT_EXTENSION.md) records Q012–Q014, their audit
scope, the preserved capped-run assertion failure, and all commands. Exterior
domain intersections leave 11,560 root tuples; arc consistency leaves 9,280.
Their 16,197 boundary covers contain all 6,840 genuine parent stars and 9,357
nonlanguage covers. Fixing each cover's roles leaves 5,984 nonlanguage covers;
one additional forced layer leaves 4,035. None is claimed to be a tiling.

`uv run --locked python strong/quaquaversal/reproduce.py`

Q014–Q016 follow-up: [PARENT_PROPAGATION.md](PARENT_PROPAGATION.md) records
the next three forced layers (1,554, 1,076, 744 survivors), geometric
exclusions and expanded arc propagation. The latter leaves 350 unresolved
parent covers. Every retained domain and every logged reduction has now
been audited; this does not establish infinite extension or aperiodicity.

Further continuation now leaves 246 covers. The binary pilot adds no parent
exclusions. Optional-presence and sampled-overlap SAT assignments fail when
complete neighbor stars are requested, yielding six verified binary choice
cuts for the next attempt. [OPTIONAL_NEIGHBOR_RULES.md](OPTIONAL_NEIGHBOR_RULES.md)
distinguishes these assignment rejections from whole-parent exclusions.

Q021 learns 117 additional audited binary cuts; all six pilot cases admit
revised assignments passing the immediate complete-neighbor-star check.
Q022 rejects five of those assignments when optional neighbors constrain
each other, yielding five separately checked cuts of lengths 3, 3, 3, 5, 2.
One frozen assignment remains unresolved; none of these cuts excludes an
original parent case without further choices. The Q021 duplicate-cut
implementation failure and its correction are preserved in the artifacts.

Q023 integrates the arc oracle and learns 34 more cuts (162 total). All six
revised assignments pass, with full independent domain comparison. Q024
uses these cuts on the full frontier, removing 77 star values in 18 cases;
150 further arc reductions leave all 246 parent cases unresolved. The new
full seed is `choice_cut_frontier_seed.json`. The last frozen Q022 model
has separately failed one layer farther out (38 audited arc reductions).

Q025–Q027 now leave 177 parent cases: 11 exclusions in a forced layer,
30 in fine arc propagation, and 28 additional exclusions from the possible
parent-star vocabulary. Every survivor domain and exclusion has its stated
independent audit. Q026 supplies an eight-choice layered certificate and
the 163-cut catalog. See [coarse constraints](COARSE_PARENT_RULES.md) and
[the proof format](DOMAIN_CERTIFICATES.md); the main objective remains open.

Q028–Q031 now leave 82 cases. Fine propagation removes seven then 40, and
conditional coarse feedback removes 48 more. The earlier standalone 17
coarse exclusions overlap fine ones and are not added twice. The enlarged
7,000-star language has one verified recognizable grouping step, giving
two nested steps for original-rule tilings. All 160 eight-sibling probes
remain satisfiable in their finite relaxation. None proves infinite extension.

Q032 expands the complete 82-case parent-scale frontier by one forced layer
and arc consistency. All 82 survive; 15,782 reductions have separate replay.
The adapters and retained domains are audited, and the continuation seed is
`coarse_arc_seed_1.json`. Finite survival is still unknown, not a tiling witness.

This now runs 136 commands in dependency order and checks input hashes. Expected
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

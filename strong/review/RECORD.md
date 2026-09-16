# Outside-review preparation record

## 16 September 2026 — preparation chronology

- User requested the next milestone and a handoff record for interruption.
- Created repository-root `HANDOFF.md` before continuing substantive work.
- User selected **“Prepare for Goodman-Strauss.”** No sending instruction
  has been given; no email or other message has been sent.
- Re-read the active cap/grid proof and finite checkers. No new mathematical
  counterexample or identified fatal gap was found in this pass.
- Wrote `DEPENDENCY_AUDIT.md` to separate mathematical implications from
  machine-checked identities and finite enumerations. Made the existence
  argument explicit with interior-ball radius `2^(m-1)-141/35840` and a
  diagonal limit of finite-state placements.
- Prepared a brief asking about prior equivalence and the cap-to-grid
  passage, with explicit disclosure of substantial AI assistance.
- Confirmed the intended address on the author's
  [Bridges 2025 profile](https://gallery.bridgesmathart.org/exhibitions/bridges-2025-exhibition-of-mathematical-art/chaim-goodman-strauss):
  `chaimgoodmanstrauss@gmail.com`. This is a public listed address, not a
  delivery test. Also checked his [personal website](https://chaimgoodmanstrauss.com/).
- Reopened the [aperiodic-pair author preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).
  It explicitly distinguishes absence of infinite cyclic symmetry from
  mere absence of translations, and describes a two-tile construction.
  Its 1998 preprint date differs from the 1999 publication date.
- The original twelve-depth frozen candidate is the review target. Its
  hash, geometry, and archived proposal have not been changed.

## Earlier checkpoint

Build the portable PDF/HTML/source archive; run its reproduction entry
point; test its file integrity and offline brief; record exact output
hashes and checks here. Update `HANDOFF.md` after completion.

The local preparation tasks above were subsequently completed as recorded
below. External correctness and novelty assessment remain pending until a
human expert actually reviews the material.

## Completed delivery preparation

- Wrote the exact unsent inquiry and an 840-word mathematical brief. The
  PDF is two pages, approximately 235 KB, with no assumed author identity.
- Added `verify_package.py`, which validates frozen inputs and archive
  hashes when present, then runs four primary checks and two controls in a
  disposable copy. Original supplied certificates are not overwritten.
- All six checks passed in the working environment: coordinate hierarchy,
  cap identities, reflected contacts, local parent rule, ordinary-chair
  periodic control, and phase-erased periodic control.
- Added `build_package.py`. It gathers the linked source closure and exact
  data, preserves source paths, creates PDF and standalone MathML HTML, and
  hashes the supplied files. The archived proposal keeps its original bytes;
  its historical relative-link base remains `strong/`, documented in the
  package README.
- The first PDF attempt failed because LuaLaTeX's installed font tooling
  was incomplete. Switched to available pdfLaTeX; the two-page PDF then
  built successfully. No new Python dependencies were added.
- Inspected both PDF pages and extracted their text. Formulas, scope,
  AI-assistance disclosure, and reproduction command are readable.
- Tested the workspace and extracted-archive HTML in headless Firefox.
  The first mobile check found native MathML overflow; added an HTML scroll
  container for display equations. Both final pages now pass at desktop
  and 390-pixel mobile width with zero external requests and page errors.
- Reran all six mathematical checks from the actual extracted archive.
  All 63 supplied-file hashes and 124 local document links passed, and the
  supplied files remained unchanged by the runner.
- Updated root `AGENTS.md` to direct resuming agents to `HANDOFF.md`.
- No outside communication was sent, no expert replied, and the candidate
  remains a proposal. There is no new mathematical validation attributable
  to the intended recipient.

## Final artifacts and hashes

| Artifact | Location |
|---|---|
| Initial attachment | [review-brief.pdf](../artifacts/review-brief.pdf) |
| Offline preview | [review-brief.html](../artifacts/review-brief.html) |
| Source/data package | [review-goodman-strauss-v1.zip](../artifacts/review-goodman-strauss-v1.zip) |
| Build metadata | [review_package_build.json](../artifacts/review_package_build.json) |
| Working-copy reproduction | [review_reproduction.json](../artifacts/review_reproduction.json) |
| Extracted-package reproduction | [review_recipient_reproduction.json](../artifacts/review_recipient_reproduction.json) |
| Delivery/integrity checks | [review_delivery_verification.json](../artifacts/review_delivery_verification.json) |
| Firefox checks | [review_brief_firefox.json](../artifacts/review_brief_firefox.json) |

Archive: 1,556,314 bytes; 63 files in its checksum manifest plus the manifest.

```text
ZIP SHA-256
96cc6c2af19dd93622abf757ff385bcd5052e7a83a221a2dedf572b4aa628f5c

PDF SHA-256
d716f8132dc7f4e59910378bb7a0fcd142a3ff2b64857765c8dace0697f83072

Workspace HTML SHA-256
04babf3309194cf888c21eba484f5cf3ca634f7d06576218bb3798c88ac7edf9

Unchanged candidate SHA-256
95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54
```

## Outstanding external milestone

The user must supply the sender signature and decide whether to send the
prepared inquiry. The proposed initial attachment is the short PDF; the
larger archive is available if requested. There is no agreed review date
or commitment from Goodman-Strauss. Record any actual sending and response
here, separating acknowledgment, suggested references, identified gaps,
and substantive validation.

If the work is interrupted now, resume from [HANDOFF.md](../../HANDOFF.md).
A prepared and verified package does not complete the external-review milestone.

## Subsequent scrutiny addendum — 16 September 2026

After the user said they would review and send the inquiry personally,
they requested further scrutiny and research connections. Preserved the
v1 delivery artifacts and unsent inquiry; created
`SCRUTINY_ADDENDUM.md` rather than silently revising their attachment.

- Re-examined the cap-to-grid implication order, explicitly separating
  frame rigidity, coarse ownership, and physical filling of feature boxes.
  No new counterexample or fatal gap was identified; no external validation
  is implied by this internal pass.
- Read primary sources on recognizability, substitution addresses, geometric
  FLC, and Lee–Moody's model-set treatment of n-dimensional chairs. Their
  coincidence criterion suggested a concrete orientation-sensitive test.
- Added `../audit/explore_cube_substitution.py`, a standalone integer
  calculation reading the frozen candidate, and its complete JSON tables.
- Found the three-digit synchronization word `(000),(001),(000)` with
  image sizes `168,42,6,1`. Cross-checked all 98,112 cube labels in direct
  coordinate expansions through depth three, covering every orientation.
  Both calculation paths are in one program, not independent reviews.
- Established finite primitivity exponents 2 (24 orientation states) and
  3 (168 cube states), and a well-defined 56-state coarse quotient.
- Wrote the conditional dyadic factor, singleton-fiber almost-everywhere,
  unique invariant measure, and pure point measurable spectrum arguments
  for the full grid local-rule space. Kept exceptional fibers, minimality,
  and the equality with a substitution hull unresolved.
- Sharpened the conditional all-tilings symmetry bound to 24 and showed
  that nontrivial symmetries require a Haar-null set of dyadic addresses.
- Used `uv run --locked python` for the calculations. No new dependency,
  construction change, external message, or package rebuild.

- Verified the candidate, ZIP, PDF, and HTML hashes still equal the recorded
  v1 hashes. All five local references in the new addendum resolve.

The earlier preparation record above describes the unchanged v1 package.

## Further literature search — 16 September 2026

User requested continued search for analogous studies. Added
`LITERATURE_FOLLOWUP.md` with primary links, specific sections read, model
differences, and follow-up tasks. Identified direct methodological precedents
for the coincidence search, self-simulation, one-shape orientation coding,
and geometric homochirality. Updated attribution in the scrutiny addendum
and the new cube-substitution script's docstring; no algorithm changed.

Especially useful findings: Frettlöh–Sing Theorem 4.4; Joshi–Yassawi's
reverse-reading/semigroup treatment of unresolved positions; Robinson's
full versus minimal tiling spaces; Demaine et al. §7's explicit gaps and
imposed lattice; Spectre Lemma 2.1; and Vereshchagin's 2026 v2 Lemma 2 on
allowed crowns. The last is a planar preprint, not an immediately applicable
3D theorem. The report distinguishes tiling-space symmetries from individual
tiling stabilizers and records the remaining source-hypothesis audits.

No exact duplicate of the frozen system was identified in this search;
no novelty conclusion follows. No geometry redesign, package rebuild,
outreach, or external review occurred. Next suggested computation is a
complete crown-language comparison, not another pair-contact count.

## Direct predecessor search — 16 September 2026

User emphasized that a direct predecessor may exist and asked for a deeper
search. Added `DIRECT_PRIOR_ART_AUDIT.md` with primary sources, reading
scopes, specific model differences, and incomplete retrieval branches.

- Found Ben-Abraham–Flom (2022)'s explicit eight-color 3D chair code.
  Added `../audit/compare_published_chair_code.py` and
  `../audit/published_chair_code_comparison.json`. Used `uv` to verify the
  projection `pi(R,q)=-R(2q+1)` on all 1,344 substitution transitions:
  zero mismatches, eight colors, 21 labels per color. This is a finite
  substitution-factor check; it does not compare full tiling spaces or
  prove physical enforcement.
- Found Fletcher (2010/2011), whose Example 2 uses orientations of one
  labeled cube to represent 21 Wang cubes, retaining a one-corona atlas.
- Found Hibma's undated chair-to-identical-cross-shapes exploration,
  including his explicit periodicity objection to the proposed rules.
- Revisited Goodman-Strauss's original markings, bumps/nicks statement,
  connected pair, old circulated variants, and atlas survey. Inspected
  Culik–Kari, Schmitt's publisher abstract, Greenfeld–Tao's nonabelian
  model, Stade's second-tile geometric conversion, and Kim's 2026 v2
  connected-polycube simulation. Full reading scopes are in the report.
- Named retrieval gaps: old Goodman-Strauss versions, Schmitt full texts,
  Fletcher thesis. No comprehensive citation-index census completed.
- Updated the handoff, review index, and scrutiny addendum. No geometry
  changes, dependencies, package rebuild, outgoing message, or outside review.

The mathematical mechanisms have closer precedents than our first search
showed. No full duplicate was identified among inspected sources; novelty
remains unestablished. Next comparison target is the old markings/auxiliary
tiles versus our actual three motifs, not just their substitution pictures.

Validation: the exact comparison passed; local links in the new audit,
review index, and scrutiny addendum resolve. Candidate/PDF/HTML/ZIP hashes
were rechecked and equal the recorded frozen v1 values.

## Actual markings and auxiliary pieces — 16 September 2026

User requested the focused comparison with Goodman-Strauss's original
markings and auxiliary pieces. Added `GOODMAN_STRAUSS_COMPARISON.md`,
`../audit/compare_goodman_strauss.py`, and its JSON and readable matrices.
Read the author preprint and visually inspected published pages 388–394,
covering the coarse contact lemma, marking definitions, auxiliary-chain
proof, grouping proof, and connected-pair modification. Recorded the
published/preprint numbering and the inconsistent later axial offset;
the computation uses the geometrically consistent Lemma 2.2 formula.

- Translated the old diagonal-arrow rule into coordinates and checked all
  48 signed-axis/notch-direction cases.
- Recomputed 1,194 geometric contacts, 44 fitting contacts, and the 14
  impossible-face exclusions directly from A/B/C descriptors, without
  importing the project's implementation. This relies on the earlier
  cap-to-motif validation; it is not a new arbitrary-placement audit.
- Established exact projection onto the 26 old coarse contact pairs,
  allowing all three root poses. Of 234 pose assignments, 132 fit the
  immediate rules and 90 survive local exclusions. Recorded every matrix.
- Found a three-chair coarse pair-language patch whose two contacts
  require incompatible root poses. It is not certified extendible in the
  old marked system and is not a counterexample to that construction.
- Interpreted the three poses by the exceptional-sign axis of the notch
  owner; verified same-direction owners copy the pose. In the eight-child
  substitution, two positions copy and six reset the parent pose.
- Recognized the central-trigger/notch-owner proof mechanism in the old
  Proposition 4.6 and corrected attribution in `../MOTIF_GROUPING.md`.
- Compared the auxiliary chains functionally and recorded the remaining
  need for an exact local marking map and inverse. Neither full tiling-space
  equivalence nor a complete duplicate has been established.
- The existing phase-erased periodic control fails the old coarse family
  constraints at 72 of 192 directed unit-face incidences. It cannot settle
  whether those coarse constraints alone force aperiodicity.

Used `uv run --locked python strong/audit/compare_goodman_strauss.py`.
No dependencies, frozen geometry, delivery artifacts, or inquiry changed;
no package rebuild, external review, or outreach. Updated the review index,
direct prior-art audit, and handoff. The current description is a proposed
geometric realization with extra pose constraints of a known chair-forcing
mechanism; correctness and novelty still require review.

Validation: the comparison passed, including the same-direction pose-copy
assertion; all 44 local links across the affected documents resolve.
Candidate, PDF, HTML, and ZIP hashes equal the recorded frozen v1 values.

## Auxiliary reconstruction — 16 September 2026

User requested sustained work on reconstructing the old auxiliary markings
locally and reversing the reconstruction. Added `AUXILIARY_RECONSTRUCTION.md`,
`../audit/reconstruct_gs_auxiliary.py`, and
`../audit/auxiliary_reconstruction.json`.

### Main findings

- Found two cross slots in the same D³ patch, `(-4,0,-4)` and `(-4,0,4)`,
  whose eight surrounding decorated chair placements agree exactly after
  translation. Old y-chain endpoints require different arrows `(1,0,1)`
  and `(1,0,-1)`.
- Wrote an inflation argument preserving the conflict while enlarging
  the common input patch without bound. Consequently no fixed-radius,
  translation-equivariant forward conversion retaining the coarse chairs
  exists on the decorated substitution hull. The written argument uses
  the existing grid substitution legality/existence results; the script
  checks the seed and depths 3, 4, 5, not all infinitely many scales.
- Constructed an old `L/I` tiling invariant under cyclic coordinate
  permutation, using nested patches `S^(2n)(L)+(4^n-1)/3 * (1,1,1)` and
  equivariant choices on undetermined chains. The chair at the origin is
  fixed, while our three poses have no fixed choice. This rules out a
  coarse-chair-preserving rotation-equivariant inverse on the full old
  space. It does not rule out a translation-only inverse using a fixed
  coordinate frame. Three decorated nested limits give explicit lifts of
  the common coarse tiling with different body-diagonal poses.

### Source-model discrepancy kept separate

Re-inspected published pages 389, 391, and 394 and the author preprint.
The transcribed connected `X₂` model, with exactly one marked axis, has no
orientation fitting the cross cavity at `(-4,-2,0)` in S³. Its x, y, z
neighbors force respectively z, z, x axes, blocking all three choices.
The program records the forcing endpoints and independently verifies the
actual old cavities using exact quarter-grid CSG. It interprets the printed
I definition according to the symmetric biprism picture (`|x₁|` in the
width bound). This is a discrepancy to reconcile with the source, not an
externally validated correction to the published paper. The original `L/I`
system has independent cross axes and does not have this one-axis obstruction.
A targeted web search did not locate clarification; no comprehensive
erratum search was conducted and no message was sent.

### Verification and preservation

The standalone script imports no project implementation, checks a second
signed-diagonal transcription of the old substitution, 5,376 matching
unit-face pairs at depth three, the inflated witnesses, 512 nonoverlapping
old recut chairs, six exact cross cavities, and finite symmetry/nesting
claims. Used `uv run --locked python`; no dependency changes.

Updated the comparison report, review index, and handoff to replace the
assumption that a larger local dictionary will suffice. The frozen solid,
v1 PDF/HTML/ZIP, and inquiry are preserved. No external mathematical review
or novelty conclusion is implied. The main new mathematical insight is a
specific difference in where the two systems store hierarchical information.

Validation: the final reconstruction audit passed, including the nested
patch inclusions. All 32 local links in the affected reports/index/handoff
resolve. Candidate, PDF, HTML, and ZIP hashes match the frozen v1 values.


## Geometric grid scrutiny — 16 September 2026

User requested scrutiny of the arbitrary-Euclidean-placement grid argument,
then explicitly authorized consulting subagents. Added
`GEOMETRIC_GRID_SCRUTINY.md`, a self-contained sequence of geometric lemmas,
with `../audit/scrutinize_grid_bridge.py` and its JSON. Preserved the second
arithmetic implementation as `../audit/grid_bridge_crosscheck.py` and JSON.

The main checker verifies actual face ownership of all 192 ports on 24
faces; all 1,536 opposite-key transforms and their outward-adjacent cube
owners; 86 distinct necessary single-cap placements; properness without
filtering improper cases; and core/corridor clearance. A radius-1/4 ball
and diameter below 4 give the written packing bound `(4R+17)^3`, before
any common grid is assumed.

All 192 ports under 48 cubic frames enter 24 periodic feature-box types.
The primary check tests 15,528 nonidentical box pairs; a written bound
excludes all larger translation offsets. The alternate implementation
searches all frames instead of using the matrix formula, transforms all
eight cube vertices to check ownership, and derives box types from actual
ports. It checks 71,976 box pairs in the larger shift window. Both passed
using `uv run --locked --offline python`.

Three bounded subagent reviews:

- `cap_rigidity_scrutiny`: independently rederived continuation, the five
  lines, base-frame identification, opposite graph sides, and the signed-key
  chirality rule. Its unfiltered calculation found 1,536 proper matches and
  zero improper matches. No substantive defect found.
- `global_grid_scrutiny`: checked the cover and component arguments,
  conditional on cap rigidity, and independently checked face coverage,
  center patterns, key chiralities, and integral shifts. No circular step
  found when component filling precedes exclusion of other components.
- `literature_review`, reassigned to implementation review: supplied the
  alternate arithmetic paths and caught an imprecise control label. The
  equal-coefficient cap example uses a determinant -1 isometry and therefore
  assumes reflections are allowed. Its JSON now states that explicitly.

The first two agents began with fresh context; the third retained the
older literature-review context. All are AI reviews with shared model and
supplied project arguments, not independent human endorsements. No agent
edited project files. The parent incorporated clarifications and the
reviewers checked the revised proof/code sections.

Clarifications now included: axes lie in the coarse face plane, not the
curved graph's tangent plane; the fifth-line constant term fixes its affine
proportionality factor; the oblique-line case has both direction components
nonzero; all eight cap mates on one face have the same unique opposite
owner; inside-box claims initially concern only the chosen component;
virtual boxes on internal faces require no second owner. The earlier live
audit no longer phrases properness as an initial restriction.

No counterexample or substantive geometric gap was found. The all-tilings
claims remain written arguments requiring external scrutiny; finite checks
alone do not establish them. This pass does not newly verify hierarchy,
existence, novelty, or approximate/manufactured geometry. Updated the
handoff, README, project index, review index, and dependency audit. The
frozen candidate and v1 PDF/HTML/ZIP remain unchanged. No outreach or push
of these new changes occurred.

## First Lean milestone — 16 September 2026

User approved introducing Lean for the macrocontact recurrence lemma.
The development is in [formal/](../../formal/README.md), separate from the
frozen review packet. The target is the unconditional normalized-grid
equivalence `macroContact r t ↔ ∃ s, t=2s ∧ fineContact r s`, for all integer
translations and all 24 listed proper cubic frames. It does not presume
even offsets, the 30 substitution contacts, or a search radius.

**Completed:** the full 24-orientation build and final axiom audit passed.
All 48 concrete certificate checks succeeded. The universal recurrence
theorem, even-offset corollary, 44-contact counts, list uniqueness, and
construction integrity statements compile. `formal/verification.json`
records the checked source hashes and transitive axiom dependencies.

Lean reconstructs faces and the eight-child boundary from frozen source
literals. A generic face-witness proof establishes enumeration completeness.
The certificate checker verifies every positive contact and every negative
overlap/mismatching-face witness, and checks coverage of all touching
offsets. Its soundness theorem turns these finite certificates into a
statement quantified over the entire integer lattice.

The source exporter pins the frozen JSON hash and uses exact rational
conversion. Geometry caches are only optimizations: Lean proves them equal
to reconstructed solids. The Python generator is not a trusted oracle for
the finite lemmas. The source-to-JSON correspondence is still checked outside
Lean, and the geometric interpretation of the definitions remains explicit.
Construction checks include exact assignment of all 192 ports, disjoint
children with matching internal faces, the doubled coarse chair, and equality
of complete macro face records to child faces after cancelling interiors.

Two subagents contributed:

- `lean_recurrence_design_review`: independent design recommendation,
  `Model.lean`, `Integrity.lean`, and review of the other agent's checker and
  the root agent's coordinate construction/exporter. It requested the
  explicit child-boundary equality and clarified the normalized-frame scope.
- `lean_recurrence_theorem`: generic certificate soundness and recurrence
  logic, followed by review of the final integration. It checked the complete
  `Fin.cases` selector and suggested checking the exact audit theorem-name
  set. It did not independently reimplement its own certificate checker.

These are AI collaborators with overlapping premises, not external human
validation. The root agent implemented the frozen-data bridge, coordinate
construction, untrusted witnesses/caches, concrete checks, final theorem,
verification driver, and documentation. The earlier generic direct-evaluation
recurrence prototype was superseded by the smaller certificate proof.

The first evaluation attempts were computationally wasteful, not failed
mathematical statements. Direct evaluation of all contacts was stopped for
resource use. Indexed witnesses, proved geometry caches, and four independent
proof batches preserve the theorem while reducing checking cost. Contact-list
order differs across scales, so recurrence uses membership equivalence;
separate uniqueness proofs justify the number of distinct contacts.

The four final certificate batches finished in 245–279 seconds each on this
machine, running concurrently. Two proof-wrapper elaboration errors were
fixed after the concrete checks passed: supplying the expected dependent
function type to the `Fin.cases` selector, and parenthesizing a Boolean
conjunction before its equality to `true`. No construction or contact changed.
The final audit contains only standard `propext`, `Classical.choice`, and
`Quot.sound` where needed; concrete count and compatibility proofs have no
axioms. No `sorryAx`, project-specific axiom, or native-evaluation axiom occurs
in the audited dependencies. Tiny adversarial controls reject missing
coverage, noncontacts, out-of-range indices, false overlap witnesses, and
false/nonopposed mismatches. All 44 oriented fine contacts also match the
earlier independent coordinate checker exactly.

Toolchain: Lean 4.34.0, official release, commit
`293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, bundled Std only. The Linux archive
SHA-256 `caaa98356098c85dc0fcbbd28e1ec66f39eb6551829972b752ff20e1286b646b`
matches the GitHub release asset digest. The toolchain was extracted under
`/tmp`; it is not a project dependency installed through uv. All Python work
used uv. Lean sources, generated certificates and result summaries are
tracked; `.lake/` build products are ignored.

No physical-solid, arbitrary-Euclidean-placement, global grouping,
existence, aperiodicity, or novelty theorem is claimed by this milestone.
No frozen candidate, inquiry, PDF/HTML/ZIP, or published repository was changed.

## Independent review of the first Lean milestone — 16 September 2026

At the user's explicit request, spawned `independent_lean_milestone_review`
with fresh context and no implementation assignment. It reviewed the contact
definitions, enumeration completeness, certificate soundness, coordinate
construction, frame enumeration, source export, concrete proof assembly,
final theorem and validation driver. Its authored report is
[`formal/INDEPENDENT_REVIEW.md`](../../formal/INDEPENDENT_REVIEW.md).

**Outcome:** no material defect found; no implementation fix requested.
The reviewer independently ran the incremental verifier and an expanded
Lean axiom audit. Both passed. It explicitly limits the result to normalized
integer-grid contact recurrence and identifies the external JSON-to-Lean
bridge and physical interpretation as remaining trust/scope boundaries.

Its new Python probe imports no project helpers: face ownership uses geometric
containment, cube transformations use all eight vertices, the macro boundary
uses internal-face cancellation, rotations use permutation/sign enumeration
and determinant, and translation candidates use adjacency of occupied cubes.
Complete cached face records match this independently reconstructed geometry.
Across all 24 orientations it finds 1,194 fine and 6,801 macro disjoint
geometric contacts; exactly 44 fit at each scale, with exact doubling for
each matrix. It also checks all 48 cancelled internal child interfaces.

Preserved the probe byte-for-byte as `formal/independent_review_probe.py`
(SHA-256 `8eff4bea7187115c0773b3fcf7371eb628eb5cd0ec0ef73e222006b508297979`).
The coordinating agent reran it through uv from its permanent path and saved
`formal/independent_review_results.json`; that run also passed. The report
includes commands and the source of the expanded temporary Lean audit.

The saved verification report matches all 17 current Lean source hashes and
the frozen candidate. No Lean source, generated formal certificate, original
verification report, or frozen review artifact changed. Updated the formal
README, handoff, and review index. Changes remain local. This fresh agent
review is independent of authorship, but is still an AI review; it reused
compiled Lean artifacts rather than performing a cold rebuild or auditing
the Lean kernel.

## Internal next-step review — 16 September 2026

After committing the completed work, the user requested a review and the
next step besides external reviews. Re-read the formal recurrence statement,
coordinate/placement definitions, dependency audit, local grouping proof,
and grouping certificate structure. Consulted the fresh milestone reviewer
again on priority and prerequisites. No new defect was identified.

Recorded `formal/NEXT_MILESTONE.md`: the next target is universal unique
parent grouping and legal deflation. The first bounded step is a precise
definition of arbitrary legal grid tilings, frame composition/inversion and
covariance, and coverage-implied neighboring faces. Then connect the existing
14 exclusions, six forcing chains and exceptional notch argument to every
legal tiling. Reuse the Lean port rules, or explicitly formalize the motif
correspondence; avoid an assumed replacement rule system. Finally prove
parent adjacency connectivity, common parity and preservation of legality
under deflation. Existence remains a separate, necessary branch.

Updated the handoff and formal README to link the plan. No Lean source,
certificate, frozen construction or verification result changed. This entry
records an implementation target and review assessment, not a newly completed
mathematical milestone.

## Arbitrary grid-tiling bridge completed — 16 September 2026

Implemented the user's approved first bounded step of `formal/NEXT_MILESTONE.md`.
`Frames.lean` defines proper cubic frames and integral motions, with composition,
inversion and actions on cube lower corners and scaled point coordinates.
`Covariance.lean` proves that the full existing face/port model transforms
consistently, including arbitrary relative contact offsets. `Boundary.lean`
checks the actual exposed boundary in all 24 orientations and proves its
translation transport. No frozen geometry or prior certificate was altered.

`Tiling.lean` defines arbitrary placement sets with coverage, unique ownership
and interface matching only. It proves common-motion invariance, derives
an actual neighbor of every exposed face from coverage, and normalizes any
touching pair into the 44 certified contacts. A combined neighbor theorem is
ready for the next contact-exclusion proofs. Arbitrarily placed macro pairs
also inherit the existing recurrence; no parent partition is assumed or proved.

Three subagents separately authored the frame, covariance and boundary modules.
The boundary contributor then performed a read-only cross-review of the
coordinator's tiling module, including both final corollaries, and reproduced
its build. It found no material issue and highlighted the proper-grid,
discrete-model and conditional-existence scope. This is internal AI
cross-review, not independent external validation of the entire addition.

Ran the full `formal/verify.py --write-report` through uv with Lean 4.34.0.
Deterministic source checks, build, independent contact-table comparison and
all 16 axiom audits passed. The updated report contains 21 Lean source hashes;
axioms remain restricted to `propext`, `Classical.choice`, and `Quot.sound`.
This reused existing compiled finite-proof batches, rather than rebuilding
the whole project cold. The substantive record and reproduction command are
in `formal/GRID_TILING_BRIDGE.md`; README, index, plan and handoff are updated.

Next: prove the 14 contact exclusions for arbitrary `LegalTiling`, then the
forcing chains and unique parent partition. Existence, legal deflation and
the complete aperiodic-solid theorem remain outside the completed step.
Changes remain local; no outreach, commit or push was performed this turn.

## Universal grouping formalized — 16 September 2026

At the user's request, first committed the completed grid-tiling bridge as
`ff440f1` (`Prove grid-tiling covariance and coverage-derived neighbors`).
Then implemented step B of the formal plan, without changing frozen geometry
or the earlier contact certificates.

`Occurrences.valid_occurrences` connects arbitrary `LegalTiling` coverage
and compatibility to the actual 44-contact catalogue. Generated grouping
data checks face coverage, pair incompatibility witnesses and relative
motions against the full frozen port model. `LocalRules` proves generic
exclusion and forcing-chain soundness. `LocalGrouping` instantiates all 14
exclusions, six central forcing chains, notch uniqueness and the exceptional
same-orientation notch case. The proof does not assume the A/B/C rule bridge
or enumerate the 33 complete stars.

`Chair.ChairGrouping.universal_grouping` gives every actual tile a unique
containing center. The intrinsic parent selects self when triggered and
otherwise the unique notch owner. Its fibers are exactly the eight-chair
groups. Further theorems identify all full group occurrences with centers,
prove uniqueness of any covering by such occurrences, and prove covariance
of the parent under every proper grid motion. A checked permutation identifies
the eight distinct group placements with the frozen substitution children.
The recognition mechanism retains its Goodman-Strauss attribution.

Three subagents separately implemented finite data, generic/concrete local
propagation, and the generic/concrete partition proofs. The coordinating agent
implemented the tiling-to-catalogue bridge and reviewed their integration.
Contributors cross-reviewed modules they did not author; no material issue
was found. This is internal AI review, not fresh independent whole-proof or
external human review.

The full uv verifier passed all three deterministic regeneration checks,
the Lean build, independent contact-table comparison and 31 theorem axiom
audits. The 28-source manifest is updated. Dependencies remain within
`propext`, `Classical.choice` and `Quot.sound`. Earlier compiled proof batches
were reused; this was not a cold whole-project rebuild. Added
`formal/UNIVERSAL_GROUPING.md` and updated handoff, README, index and plan.

The grouping addition remains local and uncommitted. No push or outreach was
performed. Next is common parent parity and legal deflation. Nonemptiness,
iteration and the complete physical finite-symmetry theorem remain separate
formal obligations.

## Common parity and legal deflation formalized — 16 September 2026

Completed step C of the formal plan. Generic `LegalSolidTiling` expresses
coverage, unique cube ownership and interface matching for the macro solid.
Universal grouping and complete child-boundary inheritance prove that the
actual group centers form such a macro tiling. No supplied parent tiling or
alignment is assumed.

The macro-boundary records are checked in every proper orientation and
transported through arbitrary translations. Unit-step induction proves
integer-grid connectivity. Coverage supplies owners along those paths;
distinct adjacent owners give actual macro contacts, whose recurrence forces
equal origin parity. Hence every parent origin has the same residue modulo
two, even when parent frames differ.

Exact scaling checks include the lower-corner corrections of rotated cubes.
Sampling one subcube transfers coverage and unique ownership to the halved
placements. For matching, adjacent coarse owner cubes lift to adjacent macro
owner cubes, giving a genuine macro contact; recurrence then supplies the
fine contact and its full port match. No direct scaling identity between
individual fine and macro decorations is assumed.

`LegalTiling.grouping_deflation` combines assembly, derived parity and legal
deflation under the sole premise `LegalTiling T`. A noncomputable choice of
origin gives `iteratedDeflation`; legality holds at every finite depth and
each successor is proved to be the grouping/deflation of its predecessor.
These are conditional statements, not a proof of initial nonemptiness or
aperiodicity.

Three subagents implemented assembly, boundary/parity and scaling. The
coordinator implemented generic contact lemmas, deflation and iteration,
then reviewed integration. Contributors cross-reviewed the deflation proof,
the parity argument and the final iteration statement; no material defect
was found. This was internal AI cross-review, not external validation.

The full uv verifier passed deterministic regeneration, the Lean project
build, contact-table comparison and 44 axiom audits. The report now hashes
36 Lean sources. Only `propext`, `Classical.choice`, and `Quot.sound` occur.
Macro-boundary kernel checking took about 109 seconds; previous finite proof
batches were reused. A duplicate boundary build was stopped to avoid repeating
the memory-intensive computation. Frozen geometry and prior certificates
are unchanged.

Added `formal/LEGAL_DEFLATION.md` and updated README, index, plan and handoff.
Changes remain local and uncommitted; no commit, push or outreach occurred.
Next: transport and halve translation periods, then exclude nonzero periods.
Initial existence and the complete physical finite-symmetry theorem remain
separate formal obligations.

## Grouping and deflation committed locally — 16 September 2026

At the user's request, committed the completed universal grouping and legal
deflation development together with the generated witnesses, verification
manifest and research records. Before committing, checked that all 36 Lean
source hashes and the frozen candidate match the successful manifest, which
records 44 axiom audits. No proof source changed after that verification.
Updated the active handoff and report status; historical implementation
entries above retain their original chronology. No push or outreach occurred.

## Translation periods halve and vanish — 16 September 2026

Implemented the requested next proof after commit `7d84070`. The new
`TranslationPeriod` definition requires bidirectional invariance of the
entire decorated placement set under an integer translation. A theorem
identifies it with equality under the existing `moveTiling` action.
Intrinsic center recognition preserves every such period.

`LegalTiling.period_even` obtains an actual center from macro coverage and
uses the common parity of it and its translated copy to write the period
as twice an integer vector. `LegalTiling.period_halves` then transports the
half-period to the existing legally deflated tiling, using the exact identity
between inflation and translation. No special alignment choice is required.

The final `LegalTiling.translation_period_zero` uses well-founded descent on
the sum of absolute coordinates. Its predicate says that the vector is a
period of some legal tiling, so the witnessing tiling may change under
deflation. The final theorem has only `LegalTiling T` and `TranslationPeriod T v`
as premises and concludes `v = zero`. A second theorem states the same result
using translated-set equality. Initial existence, general Euclidean placement
and full finite symmetry remain outside this result.

Two subagents implemented translation transport and arithmetic descent.
The coordinator implemented the evenness/halving bridge, final exclusion,
and verifier integration. A fresh third agent, with no authorship role in
these modules, reviewed the new proof and traced grouping, assembly, parity
and deflation dependencies. It found no material defect or requested change.
It independently ran the final module and Audit.lean using cached dependencies.
This is independent AI review of new-proof authorship, not external human
validation or a cold rebuild of the entire dependency chain.

The full uv verifier passed three deterministic regeneration checks, project
build, independent contact-table comparison and 52 axiom audits. The manifest
contains 40 Lean source hashes; dependencies remain restricted to `propext`,
`Classical.choice` and `Quot.sound`. No earlier proof source or frozen geometry
changed. Added `formal/TRANSLATION_EXCLUSION.md` and updated handoff, README,
plan and index. Work remains local and uncommitted; no push or outreach occurred.

Next: use the trivial translation stabilizer to make the proper-frame map
injective on grid symmetries, giving a finite bound of 24. Initial tiling
existence and the exact physical-solid bridge remain separate proof branches.

## Translation exclusion committed locally — 16 September 2026

At the user's request, committed the translation-period definitions,
transport, halving and exclusion proofs with the updated verification manifest
and research records. Before committing, checked that all 40 Lean source
hashes and the frozen candidate match the successful manifest recording 52
axiom audits. No proof source changed after verification. No push or outreach
was performed.

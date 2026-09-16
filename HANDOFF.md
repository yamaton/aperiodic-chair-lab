# Research handoff

*Updated 16 September 2026. Read this first when resuming.*

## Repository organization

Project name: **Aperiodic Chair Lab** (`aperiodic-chair-lab`).
[Project index](docs/INDEX.md) maps the research and reproduction commands;
[repository record](docs/REPOSITORY.md) explains the initial Git snapshot,
name change, evidence policy, and compatibility path. Existing research
paths and frozen delivery artifacts are preserved. The user subsequently
authorized pushing the initial commit `ba4b070` to the private GitHub origin
`yamaton/aperiodic-chair-lab`; that push is complete. Later research changes
remain local unless pushed in a separately authorized action. No reviewer
outreach has been authorized or sent.

## Active objective

**First Lean milestone completed:** read `formal/README.md`. Lean now proves
`macroContact r t ↔ ∃ s, t=2s ∧ fineContact r s` for every integer translation
and all 24 listed proper cubic orientations, with the first solid/group
normalized to identity at the origin. The 44 distinct contacts at each scale
agree with the earlier independent Python table. Finite certificates use
kernel reduction; the final axiom audit found only standard logical axioms,
no `sorryAx`, custom axioms, or native evaluation dependencies.

Generic face-witness completeness, certificate soundness, exact source-port
assignment, child compatibility, doubled coarse support, and equality of
the complete macro boundary to uncancelled child faces are checked. Python
exports frozen data and proposes witnesses; Lean checks their mathematical
content. The source JSON correspondence is reproducibly checked outside
Lean. `formal/verification.json` records source hashes and axiom dependencies.

**Fresh independent agent review completed:** `formal/INDEPENDENT_REVIEW.md`
was written by a new agent with no implementation role. It found no material
defect and requested no fix. Incremental Lean reproduction and an expanded
axiom audit passed. Its separate standard-library Python probe reconstructs
faces by geometric containment, moves cubes by all eight corners, cancels
child interfaces, and enumerates shifts by cube adjacency. It recovers all
1,194/6,801 geometric contacts and 44/44 accepted contacts with exact
same-frame doubling. The script and output are preserved as
`formal/independent_review_probe.py` and `independent_review_results.json`.
At that review, no Lean source changed and all 17 then-current source hashes
matched. The subsequent addition below updates the verification manifest.
This remains AI review of the normalized-grid milestone, not external human
validation or a cold independent rebuild of every compiled proof.

Lean 4.34.0 lives at `/tmp/lean-4.34.0-linux/bin/lake` in this session; no
Mathlib dependency. Reproduce from the root using `uv run --locked python
formal/verify.py --lake /tmp/lean-4.34.0-linux/bin/lake --write-report`, or
omit `--lake` when the pinned toolchain is installed through elan. Four
independent proof batches reduce cold build time; preserve source certificates
and ignore `.lake/`. All final checks passed; frozen artifacts are unchanged.

**First grid-tiling step completed:** read
[`formal/GRID_TILING_BRIDGE.md`](formal/GRID_TILING_BRIDGE.md).
Four new modules (`Frames`, `Covariance`, `Boundary`, `Tiling`) prove proper
grid motion algebra and contact covariance, exact exposed-face ownership,
preservation of `LegalTiling` under a common motion, and coverage-derived
neighbors whose relative placements belong to the 44-contact lists.
`LegalTiling` assumes only coverage, unique cube ownership and matching;
there is no grouping or parity premise. Recurrence now also applies to
arbitrarily placed macro pairs, without asserting those macros form groups
in an arbitrary fine tiling. The full uv verifier passed with 16 audited
theorem declarations and 21 source hashes. A contributor to the boundary
module cross-reviewed the coordinator's tiling proofs and found no material
issue; this was internal review, not a fresh review of the whole addition.

Next: derive the 14 impossible-contact exclusions from `LegalTiling`, using
`exposed_face_neighbor_accepted` to supply actual neighbors. Then formalize
the six forcing chains, exceptional notch case and unique parent partition,
followed by common parity and legal deflation. Existence, arbitrary Euclidean
grid enforcement, and the full
finite-symmetry theorem remain separate obligations. Do not describe this
milestone as a formalization of the complete physical monotile theorem.
The [next-milestone review](formal/NEXT_MILESTONE.md) gives the precise target
and acceptance criteria; step A is complete. Connect the existing local
grouping witnesses to the new definition. Reuse the proven frozen-port rules or formally bridge
the motif encoding before relying on A/B/C rules in Lean.

**Focused geometric scrutiny completed:**
`strong/review/GEOMETRIC_GRID_SCRUTINY.md` rewrites the arbitrary-placement
bridge in a noncircular order: local finiteness, open cap coincidence,
rigidity, adjacent cube ownership, component grid coverage, actual material
coverage, then exclusion of other components. No substantive defect or
counterexample was found; external mathematical validation is still absent.
Three user-authorized subagents separately reviewed cap rigidity, global
coverage, and the new arithmetic checker. Their scope and corrections are
recorded in the report; their agreement is not independent human review.

New `strong/audit/scrutinize_grid_bridge.py` checks every actual exposed
face/port and all 1,536 opposite-key placements, verifying that each owns
precisely the outward adjacent cube. All relative determinants are +1,
with 86 distinct local placements. These are single-cap necessities, not
44 whole-chair contacts. It maps all 192 ports in 48 frames to 24 periodic
box types and verifies 15,528 nearby box pairs; a written far-shift bound
makes that enumeration exhaustive over the infinite grid family.
`strong/audit/grid_bridge_crosscheck.py` independently searches frames,
transforms eight cube corners, derives box types from ports, and tests
71,976 pairs with a larger translation window. Both passed using `uv`.
Result JSONs sit beside the scripts.

Important clarifications: axes are in the cap's base plane; properness is
derived without discarding improper candidates; inside-box assertions
concern only the selected component until it has filled space. Unused
internal-face template boxes are not exposed interfaces. The altered
symmetric-cap negative control uses an improper map, so its off-grid
example requires reflected copies and is not a proper-only counterexample.
The frozen candidate and v1 delivery artifacts are unchanged. This work
strengthens the geometric argument; it does not independently verify the
full aperiodicity theorem, novelty, or manufactured approximations.


**Auxiliary reconstruction follow-up: obstructions found.** Read
`strong/review/AUXILIARY_RECONSTRUCTION.md` first. The natural forward map
is not merely unconstructed: a written argument rules out any fixed-radius,
translation-equivariant conversion retaining the same coarse chairs from
our decorated substitution hull to the old `L/I` system. Crosses at
`(-4,0,-4)` and `(-4,0,4)` in D³ have identical surrounding decorated chairs
but forced y-arm arrows `(1,0,1)` and `(1,0,-1)`. Inflation makes the common
input neighborhoods arbitrarily large while preserving this difference.
The initial witness and depths 3–5 are checked; the all-radius statement
is a written proof using the existing legal substitution/existence results.

Reverse: a nested old `L/I` tiling has a threefold rotation fixing its
chair at the origin; none of our three poses of that chair is fixed.
Thus no coarse-chair-preserving, rotation-equivariant inverse exists on
the full old space. Translation-only inverse selection remains open.
Three decorated nested limits over the same coarse tiling make the
symmetry-breaking choice explicit. Do not claim every abstract conjugacy
or every nonlocal correspondence is excluded.

**Source-model discrepancy, not an established correction to the paper:**
in the transcribed connected `X₂` model, the cross at `(-4,-2,0)` has all
three marked-axis choices blocked by adjacent forced crosses. Exact
quarter-grid CSG confirms the cavities. Reconcile the geometry/marking
interpretation with the published connected variant before claims about
its full tiling space. The original `L/I` construction does not impose
the problematic one-marked-axis restriction. No expert has reviewed this.

Reproduce: `uv run --locked python strong/audit/reconstruct_gs_auxiliary.py`.
Results: `strong/audit/auxiliary_reconstruction.json`. No frozen candidate,
v1 PDF/HTML/ZIP, or unsent inquiry changed. Next: scrutinize the two written
obstructions and the connected-variant transcription, then investigate
nonlocal completion or a restricted/translation-only inverse if useful.
The earlier request for a two-sided local dictionary should not be resumed
as though the forward obstruction had not been found.

**Actual-markings comparison completed to the finite pair level:**
`strong/review/GOODMAN_STRAUSS_COMPARISON.md` compares the original arrows,
auxiliary chains, connected `L/X₂` variant, and grouping proof with our rules.
The grouping mechanism is already in Goodman-Strauss's Proposition 4.6;
attribution has been added to `strong/MOTIF_GROUPING.md`.
Our contacts project onto exactly his 26 coarse contacts when all three
root poses are allowed. Of 234 pose assignments over those pairs, 132 fit
the immediate rules and 90 survive the 14 local exclusions. Every surviving
contact uses all three motif names; A/B/C do not label his three families.
The three poses distinguish the exceptional-sign axis of a nonidentical
notch owner. Two substitution children copy the parent pose; six reset it.
Run `uv run --locked python strong/audit/compare_goodman_strauss.py`;
the JSON and readable matrices sit beside the script.

The auxiliary-piece comparison remains partial: no bounded-radius map to
the exact old cross markings, inverse lifting rule, or equivalence of full
tiling spaces is proved. A three-chair coarse pair-language patch has no
surviving pose lift, but has NOT been shown extendible in the old marked
system. Next focused task is to construct that auxiliary-marking map or
identify an obstruction (now addressed by the follow-up above). Frozen geometry, v1 delivery artifacts, and the
unsent inquiry remain unchanged. No external validation or novelty claim.

**Deeper direct-prior-art pass completed:**
`strong/review/DIRECT_PRIOR_ART_AUDIT.md` records closer predecessors and
unresolved retrievals. New exact check: our 168 cube labels project onto
Ben-Abraham–Flom's published eight-color chair substitution (2022), using
`pi(R,q)=-R(2q+1)`. All 1,344 digit transitions agree; each color has 21
input labels. Run `uv run --locked python strong/audit/compare_published_chair_code.py`;
output is `strong/audit/published_chair_code_comparison.json`. This proves
a substitution factor, not equivalence of full tiling spaces or local rules.

Fletcher (2010/2011), §3 Example 2, already encodes 21 Wang cubes in
orientations of one asymmetrically labeled cube, retaining an external
one-corona atlas. Hibma's undated “3D Chair Tiles” page explicitly attempts
a chair-derived identical-shape construction and finds periodic placements
under its proposed rules. Both are newly identified close precedents.
Also checked Culik–Kari (1995), Schmitt's 1997 abstract, Stade (2025),
Kim's connected-polycube simulation (2026 v2), and Greenfeld–Tao's
nonabelian tile. See report for exact reading scopes and model differences.

The follow-up above addresses the old markings at the pair level;
equality of projected substitutions does not settle forcing-rule
equivalence, and the full auxiliary-information map remains open. Retrieval of his
1995/1997 circulated versions, Schmitt's full papers, and Fletcher's thesis
remains open. No complete duplicate identified, no novelty conclusion.
The frozen candidate and all v1 delivery artifacts remain unchanged;
the inquiry remains unsent. Previous pass details follow.

**Latest literature pass completed:** see
`strong/review/LITERATURE_FOLLOWUP.md` for primary-source comparisons and
reading scopes. Direct precedents found: Frettlöh–Sing (2007) coincidence
graphs; Joshi–Yassawi reverse-reading automata for exceptional addresses;
Durand–Romashchenko–Shen self-simulation; Fernique–Ollinger sofic hierarchies;
Demaine et al. rotation-encoded one-tile simulations (gaps and imposed
lattice, so not our solid theorem); Spectre Lemma 2.1 curved-boundary
homochirality; Robinson full space versus minimal hull; and chair extended
symmetries, which must not be confused with individual tiling stabilizers.
Also inspected Vereshchagin's new arXiv:2606.25005v2 (10 August 2026):
Lemma 2 suggests a crown-language test for hierarchy versus substitution
tilings. Its development is planar; a 3D adaptation requires proof.

Recommended next finite task: compare complete labeled cube-vertex crowns
(2×2×2 blocks) allowed by our rules with a certified substitution closure,
including owner consistency. Pair-contact equality alone cannot settle
full local-rule space = substitution hull. Alternative next task: adapt
the reverse-reading/semigroup method to classify exceptional address
fibers; avoiding one reset word is not sufficient to identify them.
No exact duplicate was identified; this is not a priority conclusion.
Attribution was added to the scrutiny addendum and new exploration script.
The v1 review packet, unsent inquiry, and frozen solid remain unchanged.

**Latest scrutiny pass completed:** the user is reviewing the writeup and
plans to send it personally. Subsequent work is recorded separately in
`strong/review/SCRUTINY_ADDENDUM.md`; the existing v1 PDF, inquiry, ZIP, and
frozen construction were preserved. No outreach occurred.

New exact computation: `strong/audit/explore_cube_substitution.py` constructs
168 cube labels `(orientation, local cube)` directly from the frozen data.
The digit word `(000),(001),(000)` synchronizes all 168 labels to one:
image sizes `168 -> 42 -> 6 -> 1`, residue `(0,0,2)` modulo 8, output
`R(x,y,z)=(x,z,-y), q=(-1,0,-1)`. Direct chair expansion cross-checks
98,112 cube labels through depth three. Tile-orientation primitivity
exponent is 2; cube-label exponent is 3. Forgetting the three internal
poses yields a well-defined 56-label substitution (zero digit-map conflicts).
Tables/results: `strong/audit/cube_substitution_exploration.json`.
Reproduce with `uv run --locked python strong/audit/explore_cube_substitution.py`.

The addendum proves written implications, conditional on the existing
hierarchy: the **full grid local-rule space** maps onto Z_2^3 by nested parent
origin cosets; synchronization makes almost every address fiber singleton;
there is a unique invariant probability measure with pure point measurable
Z³ spectrum. These deductions have not received outside review. Do not
claim the script verifies their analysis, minimality, all singleton fibers,
or equality of the full local-rule space with the substitution hull.
The handedness argument sharpens the full symmetry bound from 48 to 24;
the necessary symmetry equation `(I-R)a=t` excludes all nonidentity
symmetries for Haar-almost every address, not for every address.

Primary connections: Lee–Moody, *Lattice Substitution Systems and Model Sets*
(n-dimensional chairs and modular coincidence); Solomyak on recognizability;
Goodman-Strauss's *Addressing in substitution tilings* (available manuscript
is a 2004 draft); geometric versus symbolic FLC work by Hellouin de Menibus,
Lutfalla, and Vanier. URLs, scopes, and caveats are in the addendum.
Next mathematical directions: shorten the synchronization certificate;
classify exceptional address fibers and possible finite rotations; review
the physical grid bridge and one-congruence-class novelty externally.

Prepare the recut-chair candidate for an outside tiling expert to assess
correctness and novelty. User requested proceeding with that milestone and
a record that another agent can resume. **No outside reviewer has validated
the construction. No message has been sent.**

**Local preparation is complete.** User explicitly selected **Chaim
Goodman-Strauss** on 16 September: “Prepare for Goodman-Strauss.” This
authorizes preparing the inquiry, not sending it.

Ready outputs:

- `strong/review/INQUIRY_GOODMAN_STRAUSS.md`: exact draft, suggested
  attachment, verified public recipient address; sender name remains blank.
- `strong/artifacts/review-brief.pdf`: inspected two-page initial attachment.
- `strong/artifacts/review-brief.html`: offline MathML preview, Firefox-tested.
- `strong/artifacts/review-goodman-strauss-v1.zip`: portable source package,
  1,556,314 bytes, with root `START_HERE.html` and 63 hashed supplied files.
- `strong/review/DEPENDENCY_AUDIT.md`: proof dependencies, adversarial
  questions, and explicit expanding-ball existence argument.
- `strong/review/RECORD.md`: chronology, contact provenance, checks, hashes,
  and unresolved external milestone. `strong/review/README.md` is the index.

Archive SHA-256:
`96cc6c2af19dd93622abf757ff385bcd5052e7a83a221a2dedf572b4aa628f5c`.

Checks completed:

- Four primary computations plus two periodic controls passed in a temporary
  copy, then passed again from the extracted archive.
- All 63 manifest hashes and 124 local document links passed; supplied files
  were unchanged by reproduction.
- PDF has two pages and readable extracted text; both pages visually inspected.
- Workspace and archive HTML passed offline Firefox desktop/mobile checks,
  native MathML, zero network requests, and zero page errors.
- Evidence: `strong/artifacts/review_reproduction.json`,
  `review_recipient_reproduction.json`, `review_delivery_verification.json`,
  `review_brief_firefox.json`, and `review_package_build.json`.

**Next outstanding action:** the user reviews/signs the inquiry and decides
whether to send it. If explicitly instructed to send, confirm the provided
sender identity, use the reviewed body and PDF, and record what was actually
sent. Until then, do not send anything or claim an expert response exists.
There are no running checks or pending agent tasks from this preparation.

To reproduce the review package checks:

```sh
uv run --locked python strong/review/verify_package.py
```

The full build/delivery commands and optional browser dependencies are in
`strong/review/README.md`. Rebuilding changes archive/PDF hashes; refresh the
delivery check and records if any bundled source changes. Do not rerun the
old synthesis merely to resume this milestone.

An external inquiry has been prepared locally. Sending an email or another
message requires an explicit user instruction; do not interpret this record
as authorization to contact someone. Do not claim external review complete
merely because the package or internal checks are complete.

## Mathematical target and status

One compact, connected-interior solid that tiles R³, with every tiling
having a finite symmetry group, even allowing reflected copies. Here
“strongly aperiodic” means no translations or infinite-order screws;
some literature reserves that term for trivial symmetry groups. State the
finite-group property explicitly.

The exact twelve-depth polynomial-cap solid remains a **research proposal**.
Its finite grid hierarchy has several implementation checks and internal AI
reviews. The proposed analytic proof that arbitrary physical tilings lie on
one grid has not been externally accepted. Novelty is unresolved. Successful
grid computations alone do not establish the physical-solid theorem.

## Canonical inputs and reading order

- `AGENTS.md`: use `uv` for all Python; preserve provenance and uncertainty.
- `strong/REVIEW_NOTE.md`: short claim, proof dependencies, review questions.
- `strong/MOTIF_GROUPING.md`: latest, simpler unique-grouping proof.
- `strong/audit/README.md`: expanded cap-rigidity and global-grid arguments.
- `strong/FOLLOWUP_REFLECTIONS.md`: handedness, motifs, periodic control,
  six-depth recoding, and chronological record.
- `strong/audit/LITERATURE_REVIEW.md`: close prior art and comparison limits.
- `strong/audit/SUBAGENT_REVIEWS.md`: completed internal review findings.
- `strong/RECUT_CHAIR.md`: full active proposal; older proof retained.

Never modify `strong/audit/frozen_v1/`. The defining file is
`strong/audit/frozen_v1/candidate.json`, SHA-256:

```text
95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54
```

## Results already established by finite checks

- Seven-cube coarse chair; 24 faces; 192 exact polynomial caps.
- 1,194 proper geometric contacts, 44 fitting; 33 complete neighborhoods.
- Eight-child substitution closure has 30 contacts.
- 6,801 macrocontacts, exactly 44 fitting; all offsets even; deflation
  recovers the original 44-contact language.
- All 48 frame orientations checked: no improper cap/face/chair matches.
  Signed-key local frame chirality forces equal handedness at a cap match.
- Three oriented face motifs reconstruct all ports. Only six faces change
  under the chair's three internal cyclic poses.
- Erasing phase by a specified signed-key quotient produces a different
  periodic solid. Its eight-chair lattice witness has 56 cubes per cell
  and 1,536 directed port incidences, all matched. Original keys reject it.
- A six-depth alternate assignment preserves both 44-contact sets. It is
  not the frozen review target. Three depths add 147 contacts and remain
  unclassified; do not infer periodicity from that count.

Latest grouping advance, verified with `uv`:

- `strong/audit/motif_grouping.py` imports no project implementation.
- It reconstructs all 192 ports from A/B/C patterns and arrows.
- Fourteen of the 44 fitting contacts fail a neighboring-face coverage test.
  The surviving 30 equal the substitution closure.
- Six mixed-sign diagonal contacts force the entire central neighborhood
  by singleton face coverage. Otherwise the notch owner is the parent.
- One identically oriented notch case uses an axial neighbor; an alternative
  would create forbidden C/C contact.
- All seven outer children select the same center, proving unique grouping
  without the old 28 competing-role checks.
- A separate exact-cover stage reproduces all 33 old stars as comparison.

Outputs: `strong/audit/motif_grouping_verification.json`,
`motif_grouping_certificate.json`, `motif_grouping_tables.md`.
Figures: `strong/artifacts/motif-face-layout.png`, `motif-parent-rule.png`.

## Environment and reproduction

Work from repository root. `uv run --locked python <script>` is required;
the existing home uv cache may need the approved `uv run` escalation.
Python 3.13+; dependencies locked in `uv.lock`. No usable Git repository
was found here (`git status` reports not a repository); preserve files
directly and use content hashes rather than assuming commits exist.

Primary audit commands:

```sh
uv run --locked python strong/audit/verify_from_coordinates.py
uv run --locked python strong/audit/verify_caps.py
uv run --locked python strong/audit/check_reflections.py
uv run --locked python strong/audit/motif_grouping.py
```

Optional controls and illustrations are documented in the linked records.
The offline viewer is `strong/artifacts/recut-chair.html`; it and the STL
approximate the exact surfaces and are not certified aperiodic artifacts.

## Do not repeat or overclaim

- Earlier SCD and whole-chair searches are historical; do not restart them.
- A previous user correctly noticed the coarse chair in Goodman-Strauss's
  Figure 2. The plain chair tiles periodically. Only the decorated candidate
  carries the current claim; exact physical mismatches were recorded.
- Internal subagents are not independent human experts. Prior review agents
  completed their tasks; there is no pending human response.
- The user asked whether this might be Annals-level. The stated assessment
  was conditional potential significance, not a prediction of acceptance.
- Do not create a goal-tool objective, publish, contact researchers, or
  replace the frozen geometry without the relevant user instruction.

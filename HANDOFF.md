# Research handoff

*Updated 17 September 2026. Read this first when resuming.*

## Repository organization

Project name: **Aperiodic Chair Lab** (`aperiodic-chair-lab`).
[Project index](docs/INDEX.md) maps the research and reproduction commands;
[repository record](docs/REPOSITORY.md) explains the initial Git snapshot,
name change, evidence policy, and compatibility path. Existing research
paths and frozen delivery artifacts are preserved. The user subsequently
authorized pushing the initial commit `ba4b070` to the private GitHub origin
`yamaton/aperiodic-chair-lab`; that push is complete. The subsequent read-only
publication review observed remote `main` at tutorial commit `3984e42`,
matching local HEAD; this preparation did not perform that synchronization.
The user subsequently authorized publication with “Let's publish it.”
Commit `ab17536` was pushed and the repository made PUBLIC on 16 September
2026, retaining the existing history and author identity after the email
disclosure. Keep unrelated future changes local unless publishing is
authorized. No reviewer outreach has been authorized or sent.

## Active objective

**Interactive refactoring in progress (19 September):** the user authorized
sequential refactoring with an independent review before each local commit.
Stage 1 extracts contact presentation to `feedback.js` and shares CSS colors with
Canvas. Six browser suites passed; the reviewer confirmed 54 equivalent
classifications with no required fixes. See `docs/assembly/REFACTOR_REVIEW.md`.
Next: state-update/render sequencing and repeated frame calculations, then shared
browser-check setup. Keep exact engine/history behavior and standalone packaging.

**Valid contact feedback added locally (19 September):** the user's follow-up
confirmed that valid unselected contacts had no dedicated overlay. All valid
preview contacts now have green solid borders and a light green tint, visible
from either contacting side through the pieces and selection/hover. The selected
face retains a thicker border. Invalid overlays are drawn after green overlays
so shared edges retain the warning. Per-face green can coexist with invalid
contacts and overlap; overall attachment rules are unchanged. Motion/inspection
withhold all contact overlays, and attachment removes the preview effects.
The expanded `verify-arrow-effects.cjs` checks visible contact-side counts from
opposite views, four valid contacts, mixed validity/overlap, hover/focus, completion
of rotation, and attachment/Undo. Sources and standalone HTML are updated locally.
All six browser suites passed on the rebuilt standalone HTML, including the
expanded contact-effect checks. Two independent agents subsequently reviewed this
follow-up; see the addendum in `docs/assembly/EFFECT_REVIEW.md`. No reproducible
defect was reported. Rendering checks covered 40 frames/121 contact borders across
base and parent levels; state checks covered 151 assertions across two levels,
rotation, history and inspection. The user requested a local commit, with this
review completed first. Publication remains pending.

**Arrow-only mismatch effect added locally (19 September):** pending contacts
with compatible motifs (A/A or B/C) but incompatible arrows now have red
dashed borders, a light face tint and thick emphasized arrows in the main 3D
view and comparison cards. At the user's latest request, arrow-only failures
use the same red border and tint as motif failures; dashed versus solid borders
distinguish the two. Contact annotations are drawn over the pieces and
selection/hover so they stay visible. Overall failure status is red for both.
The user's B-target/A-moving report also reproduced a missed motif-failure cue:
selection green won in the scene, and comparison cards kept their default green.
Motif-invalid contacts now have red solid borders and tint above selection/hover
on both contacting sides and red comparison cards. Checks cover all six invalid
ordered motif pairs and the real B-target/A-picker click, focus and hover sequence.
Following the user's rotation feedback, overlap no longer suppresses per-face
arrow warnings: dashed red contact cues coexist with the red overlap warning
and disabled Attach button. During separation/rotation/approach, all contact
feedback is withheld and the comparison/status show a localized adjusting
message. Arrival updates scene and DOM feedback together without replacing
the piece picker or its keyboard focus; comparison height is preserved.
Reduced-motion and hidden-tab completion also refresh the DOM feedback.
The cue is static, including reduced motion; orientation, placement rules and
history are unchanged. `node docs/assembly/verify-arrow-effects.cjs` exercises
actual canvas strokes, both motif pairings, per-contact comparison, mixed
failures, overlap, hover/focus, motion, history and locales. The regression also
rotates the first guided placement four times, checking three overlapping
arrow-mismatch poses, arrival timing and return to the original valid pose.
Updated sources,
standalone HTML and verification records remain local and unpublished. The new
arrow-effect checks and existing effects, motion, browser, demo and locale
suites passed; all six browser records match the final standalone HTML.

Two independent AI agents reviewed the contact effects at the user's request;
see `docs/assembly/EFFECT_REVIEW.md`. No reproducible product defect was reported.
The rendering reviewer checked 523 representative candidates across all 24 initial
target faces, 1,236 contact comparisons and 1,046 views. The state reviewer checked
24 rotations/interruptions, history, language changes, reduced motion, simulated
hidden-tab completion and inspection during motion after parent promotion.
The review did not change application code or publish/commit the pending work.
The user subsequently requested a local commit of the contact-effect changes,
generated HTML, verification records and review notes. Publication remains pending.

**Assembly placement animation implemented locally (19 September):** selecting
the second face now rotates the pending piece about its centroid (360 ms), then
moves it into preview contact (300 ms). Changing an existing preview or using
the 90-degree controls first separates it along the old target normal (200 ms).
Target reselection clears the moving face and animates back to staging. New
requests start from the current displayed pose; Attach waits until arrival.
`docs/assembly/motion.js` interpolates display-only rigid poses; grid checks and
history keep exact destination poses. Undo/Redo, cancellation, restart and
inspection discard stale motion. Reduced motion skips it; hidden tabs settle it.
The embedded demo pauses piece motion and finishes the previous animation when
manually stepping. `node docs/assembly/verify-motion.cjs` checks all 576 discrete
rotation pairs plus browser motion/state regressions. The motion, engine,
browser, effects, demo and locale suites passed; all five HTML-based records
match the rebuilt standalone artifact. This is a visual explanation of placement,
not collision-free physical path planning. Changes remain local and unpublished.

Two independent AI agents reviewed the animation at the user's request; see
`docs/assembly/MOTION_REVIEW.md`. Neither reported a reproducible product defect
in the checked scope. Additional checks covered 30 rapid target/candidate changes,
inspection during motion after parent promotion, and 10,000 deterministic
interrupted rotations. The motion and demo suites also passed independently.
One test-coverage suggestion was applied: demo pause verification now requires
an active motion phase before asserting that the paused pose stays fixed.
The strengthened demo suite passed on the same standalone HTML.
Application code is unchanged by this review; physical mobile devices, other
browser engines and player trials remain outside the checked scope.

**Assembly attention effects added locally (19 September):** the face-selection
phase gently pulses the bonded assembly; after a target-face click, the
orientation phase pulses the pending piece. Hover replaces whole-block
attention with a bright panel outline and fill. After the user's clarification,
target selection leaves the pending piece in its separate staging pose, with
no moving face preselected. Only selecting the second face (in the main view,
picker or explicit candidate list) positions it against the assembly. The
staging pose stays clear of the whole bonded group. The isolated piece picker
shares attention suppression and supports keyboard focus; reduced motion
uses a static highlight. Selecting both faces only previews a placement;
the explicit Attach button commits the bond. Sources and standalone
`docs/assembly.html` are updated. `node docs/assembly/verify-effects.cjs`
checks visible animation, hover, uncommitted selection, history, phase
transitions, reduced motion and mobile touch. Existing browser, demo and
locale checks cover the remaining interactions. Changes remain local.

Two independent AI agents reviewed the face-selection flow and effects.
They confirmed all 24 initial target choices preserve the detached pose,
second-face placement, Undo/Redo, and Firefox pointer/touch-emulation/keyboard
behavior. One P2 finding was stale attachment advice after target reselection.
Target selection now clears the old hint and restarts its sequence; the
browser regression covers both the same and a different target, and confirms
the first renewed hint leaves the piece detached. No other product issue was
confirmed in their checked scope; real-device touch and other browsers remain
unchecked. This is an AI implementation review, not a player trial.

**README cover with enlarged features rendered locally:** at the user's
request, the README now uses `docs/figures/aperiodic-chair-cover-enlarged.png`,
with the prescribed ports widened 3× and deepened 12× for visibility. The
caption and image disclose these factors. It shows one chair, a close-up of
the recorded +7/-7 pair with the same enlarged profile, and the eight-child
assembly. The original-proportion Blender image is preserved separately.
The uv driver
`docs/render_chair_cover.py` invokes Blender through WSL paths; its companion
worker renders with Cycles. The figure's `.md` documents reproduction and
mesh scope; its `.json` records source hashes, sampled surface checks, exact
contact checks, positive feature-box clearance bounds and the 56-cell carrier
partition. This is a visualization variant, not a newly certified physical
solid or a change to frozen v1. The earlier AI concept
image and prompts remain as a superseded draft, unused by README.
Frozen evidence is unchanged. The user requested a local commit of the cover,
rendering scripts and provenance; publication remains pending.

**README now leads with the interactive builder:** the opening explains the
activity and links directly to `assembly/`, its `?demo=1` demonstration and
the project home. The entry table starts with building; research background
and the unchanged Chair44 attribution follow the entry routes. Offline play
instructions and the three maintained languages are included. This README
reorganization is being committed locally at the user’s request; publication
remains pending.

**Japanese home introduction revised locally:** replace the mixed Japanese/
English “chair” wording with “ブロック” and describe connecting pieces followed
by the goal of building a larger block of the same shape. The remaining four
generic “chair” mentions in Japanese UI copy (metadata and parent completion/
shape messages) also use “ブロック”; proper names remain intact. The user
requested a local commit of these edits. Publication remains pending.

**Heading punctuation adjusted locally:** remove terminal periods/full stops
from home and assembly headings in Japanese, English and Simplified Chinese.
Body sentences, demo captions, internal punctuation and question marks are
preserved. Inactive translations remain untouched. This follow-up to commit
`d1a9265` is being recorded in a local commit at the user’s request; publication
remains pending.

**Three maintained UI languages:** the user chose Japanese, English and
Simplified Chinese to limit ongoing maintenance. Only top-level JSON files in
`docs/locales/` enter the menu, generated HTML and required validation.
Arabic, German, Spanish, French and Russian catalogs are preserved unchanged
in `docs/locales/inactive/`; routine UI work need not update them. See
`docs/locales/README.md` for reactivation and fallback behavior. Shared RTL
support is retained. Chinese has not had native-speaker review. The user
requested a local commit of the project home and localization changes;
publication remains pending.

**Interactive-first project home prepared locally:** the user requested a
multilingual Pages landing page focused on entering the assembly activity.
`docs/site-index.html`, `site.css`, `site.js` and `site-preview.cjs` replace
the old Markdown landing page. Three-language calls to action lead to
`assembly/` or directly to its demonstration; mathematical reading, the
curved-shape viewer and research evidence remain secondary resources.
`docs/site-language.js` shares language preferences, with query parameters
preserving the selected language even without storage. `build-site.mjs`
packages the activity alongside the existing tutorial, viewer and download,
and the Pages workflow watches the new sources. The generated `_site/` is
local only; `docs/site_preview_verification.json` records navigation and
language checks under the project subpath. This update has not been deployed. The original live record in `docs/pages_verification.json` is unchanged.

**Interactive assembly prototype implemented locally:** the user requested
starting the prototype after the UX reviews. Open `docs/assembly.html` in a
browser; [prototype notes](docs/assembly/README.md) cover the build and scope.
It has exact grid contact checks, a rigid target plus one moving piece,
shared-frame face comparison, guided/free assembly, Undo/Redo, eight-child
recognition, parent promotion and nested read-only inspection. The UI is
available in Japanese, English and Simplified Chinese, and the HTML is standalone/offline. Rebuild with
`node docs/build-assembly.cjs`; verify using the verification scripts in `docs/assembly/`.
The finite verifier reproduces 1,194/44 base contacts and 6,801/44 macro
contacts. Firefox exercises two parent levels and desktop/mobile interactions.
These checks are not player trials or new mathematical proofs. Candidate
thumbnails and curved surfaces are among the documented simplifications.
The prototype has not been deployed; existing published viewers are unchanged.
Following the user's face-selection feedback, both target and moving-piece
faces can be clicked. A separate rotatable moving-piece view exposes hidden
faces and supports keyboard selection; numbered dropdowns are now collapsed
fallbacks. Viewing the piece preserves placement and Undo/Redo. The offline
Firefox checks cover desktop/mobile selection and these state invariants.
The language selector translates controls, hints, contact results, and
accessibility labels without changing the assembly or history. It uses the
browser language initially and remembers an explicit choice when storage is
available. `docs/locales/*.json` holds the shared message catalogs; `docs/build-locales.cjs` validates and embeds them.
The header now opens a short four-step multilingual operation guide,
embedded from `docs/assembly/guide.html`: choose the two faces, compare arrows,
then attach. Diagrams show the A/A and B/C matching examples. Parent assembly
is an optional next step; opening help preserves the pending piece and history.
The English undergraduate mathematics text is linked separately at the bottom,
not presented as the play tutorial. Browser checks cover both guide languages,
mobile fit, focus return, and Escape while inspecting children.
The guide now includes “Watch the actions”: a multilingual cursor demo
of target/piece face selection, comparison, rotation and the first attachment.
An embedded isolated copy of the same application performs the real UI actions;
the player's state, camera and history stay intact. Pause, step, replay, closing
during playback, reduced motion and mobile layout are covered by
`node docs/assembly/verify-demo.cjs` and `docs/assembly_demo_verification.json`.
`docs/assembly/demo.js` controls playback; the build embeds both documents offline.
At the user's request, two independent agents reviewed demo UX and state handling.
[Review record](docs/assembly/DEMO_REVIEW.md) tracks a narrow-viewport SVG picking
failure, off-screen controls, and an undersized comparison highlight. Fixes use
measured face centering, a viewport-height dialog with a landscape layout, and
a highlight spanning both comparison cards. Regression checks include 667×375,
750×600 and 320×568; independent follow-up confirmed the original picking issue fixed.
The user requested a local commit of the specification, prototype, guides,
demo and review fixes. Publishing this prototype has not been authorized.

**Interactive assembly teaching draft:** the user requested a specification
after brainstorming a matching-rule assembly activity. The central clarified
interaction is a fixed bonded assembly plus one moving piece, not a global
eight-object display limit. [The draft](docs/INTERACTIVE_ASSEMBLY_SPEC.md)
sets out contact comparison in a shared frame, explicit attachment and Undo,
eight-child recognition, effective-parent visualization, scale changes and
read-only inspection of children. It separates agreed direction, recommended
initial behavior, mathematical scope and later features. The draft and
reviews preceded the local implementation described above.
At the user's request to prioritize player UX, the draft was revised to
guide the first complete parent, separate guidance from free exploration,
offer placement candidates from a target-face selection, reveal explanations
progressively, and preserve the work while browsing parent/child levels.
The Undo/Redo contradiction was corrected: undoing a bond restores a movable
piece without preventing immediate Redo. Acceptance criteria now include
history branching, returning from inspection and early first-time-player trials.
The user then requested another self-review and independent reviews with
player UX as the priority. Two agents reviewed first-time interaction and
state transitions separately. The [review record](docs/INTERACTIVE_ASSEMBLY_REVIEW.md)
tracks findings and revisions: identifiable candidates, comparison-frame
rotation, honest guidance progress, paused editing during inspection,
mode changes that preserve history, and explicit material/level transitions.
Both reviewers confirmed their findings were addressed in bounded follow-ups;
a further contact-explanation/rotation-axis ambiguity was also corrected and
rechecked. These are specification reviews, not implemented UI tests or player trials.

**Tutorial project-site publication:** the user authorized publishing the
tutorial as a GitHub Pages project site. The published inherited address is
`https://tritonlab.io/aperiodic-chair-lab/`; the existing user site owns the
custom domain. [Deployment documentation](docs/PAGES.md) records the build,
link rewriting, offline edition and browser checks. Publication includes
the previously local tutorial commit `497d73e`. Only this repository's
Pages configuration is involved; user-site configuration remains untouched.
Deployment of `179848c` succeeded in
[Actions run 35179418123](https://github.com/yamaton/aperiodic-chair-lab/actions/runs/35179418123).
The [live Firefox record](docs/pages_verification.json) confirms output hashes,
desktop/mobile presentation, navigation, viewer controls and offline download.
The existing root site still returns HTTP 200 with unchanged Pages settings.
The local-only descriptions below record earlier stages, before this
publication authorization. No reviewer outreach is authorized.

**Undergraduate tutorial expanded after review:**
[`docs/APERIODIC_CHAIR_TUTORIAL.md`](docs/APERIODIC_CHAIR_TUTORIAL.md) now
works through coordinate conventions, contact enumeration, the six triggers,
the exceptional notch case, the parent-map partition, macrocontact recurrence,
global parity and legal deflation. It develops the five-step curved-cap
registration argument and the expanding-ball/diagonal-selection existence
argument, while retaining their written-versus-Lean scope. Physics additions
define a soft bit-state model, compare canonical weights, bound seam costs,
and derive two-marker interference. The status table includes the proper-grid
24-symmetry bound. There are 19 exercises with answers and, at the user's
request for more diagrams, ten figures (eight new reproducible SVGs).
[`docs/INDEX.md`](docs/INDEX.md#undergraduate-tutorial) records the figure/HTML
build and optional Firefox check. The figure generator checks its exact
56-cube carrier partition; the motif grouping and curved-grid-note audit
both pass without changing their preserved evidence. The HTML edition is
regenerated with embedded figures and MathML; its presentation check records
desktop/mobile layout, local links, and artifact hashes. These are teaching
and presentation changes, not new formal theorems or independent human
review. The user subsequently requested a local commit of this tutorial
revision. No push or outreach was authorized or performed for it.

At the user's further request, three agents independently reviewed
mathematical correctness, first-time undergraduate progression, and
figures/exercises/mobile presentation. The
[review and disposition record](docs/TUTORIAL_REVIEW.md) preserves their
findings and bounded follow-up assessments. No major mathematical error
was reported; revisions supply the first forced-contact elimination,
explicit changes of coordinates, elementary polynomial-factor/degree steps,
a geometric roadmap and wave/complex-number prerequisites. Exercises now
have a reading route and in-text checkpoints. Ten figures can be enlarged
and panned in the offline HTML with keyboard support; the verifier tests
all ten at both viewport widths, focus restoration, and the no-JavaScript
fallback. Follow-up reviewers found the main explanation gaps addressed.
Actual undergraduate reading trials remain separate from these AI reviews.

**Dependency consolidation and grid symmetry completed:**
[`docs/PROOF_STATUS.md`](docs/PROOF_STATUS.md) is now the current claim table,
with exact assumptions, evidence classes, dependencies and remaining scope.
[`formal/GRID_SYMMETRY.md`](formal/GRID_SYMMETRY.md) records the new Lean
result: every `LegalTiling` has an exhaustive list of at most 24 proper grid
symmetries. `Chair/Symmetry.lean` proves identity/composition/inverse closure,
same-frame cancellation to a translation, frame injectivity and both a
distinct-list bound and full finite enumeration. No additional premise was
added to `LegalTiling`. The full verifier passed with 62 audited declarations
and 41 Lean source hashes, using only the standard three logical axioms.
Earlier compiled modules were reused. At the user's subsequent request,
two fresh agents independently reviewed the Lean addition and geometric
manuscript, finding no material defect. See the
[review record](strong/review/FOLLOWUP_INDEPENDENT_REVIEW.md). The Lean reviewer
reproduced the direct checks and all 62 axiom entries/41 hashes; the geometry
reviewer supplied an independent finite/symbolic probe, preserved and rerun
as `strong/audit/review_curved_grid_note.py`. The coordinator also reviewed
the work and clarified two minor wording/provenance points. No proof source
or frozen geometry changed during review. This is AI review, not human review.

[`CURVED_GRID_NOTE.md`](strong/review/CURVED_GRID_NOTE.md) is a short manuscript
of the physical-to-grid registration theorem, with five explicit lemmas,
the frozen data specification and the attributed Chair44 retained-core step.
Its analytic geometry remains written mathematics, separate from Lean;
it does not prove initial existence or certify meshes. Both geometric
arithmetic checkers were rerun successfully with unchanged results.
README, formal scope and review navigation point to these current documents;
older frozen artifacts are preserved. Changes are local; no publication or
outreach was authorized for this work. Next formal branch: initial tiling
existence. Next geometric obligations: semantic review and faithful transport
of physical symmetries, as separated in the new dependency table.

**Repository published:** https://github.com/yamaton/aperiodic-chair-lab.
The initial public preparation commit is `ab17536`; GitHub confirmed PUBLIC
visibility and the matching remote commit. The publication record is in
`docs/PUBLICATION_REVIEW.md`. No history rewrite or outreach occurred.

**Publication preparation:** see
[publication review](docs/PUBLICATION_REVIEW.md), [provenance](docs/PROVENANCE.md),
[licensing scope](LICENSING.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
The README now leads with the exact Chair44 overlap, verification, teaching
and physical experiments. Historical proposal entry points are contextualized;
frozen files, proof sources, evidence logs and Git history are unchanged.
The prepared defaults are MIT for original code/machine-readable data and
CC BY 4.0 for prose, figures and models, with explicit third-party exceptions.

**Historical privacy finding:** the ten commits in the preparation audit used
a personal Gmail author/committer identity. The user authorized publication
after this disclosure; that identity and history were retained. The pre-release
GitHub snapshot in `docs/publication_github.json` records PRIVATE visibility
at its check time and is not current visibility. The heuristic scanner found
no suspected credentials; its scope and limits are recorded in
`docs/publication_audit.json`. It is a historical preparation snapshot.

**Undergraduate tutorial added:** [offline illustrated edition](docs/APERIODIC_CHAIR_TUTORIAL.html)
and [Markdown source](docs/APERIODIC_CHAIR_TUTORIAL.md) explain the chair,
local matching, unique parents, period halving, finite symmetry, the geometric
bridge and existence, then physical observables, defects and printable ports.
Seven exercises have answers. It distinguishes our formal grid results,
the reproduced Chair44 physical theorem and proposed printing work. This is
exposition, not a new proof or interface implementation. The project index
contains the Pandoc rebuild command; frozen research artifacts are unchanged.
The subsequent reading-flow pass defines the grid model before using it,
introduces parity with paired intervals, explains the finite orientation
count and scattering formula through examples, and marks specialized proof
details optional. Common parity is explicitly a separate proved input.

**Pinned Chair44 build/replay completed:** see
[`CHAIR44_BUILD_REPRODUCTION.md`](strong/review/CHAIR44_BUILD_REPRODUCTION.md).
The unchanged release compiled with Lean 4.31.0 and all nine pinned
dependencies. Cold project build took 1,120.40 seconds; promoted-library
build and fresh axiom audit passed. All 169 reproduced axiom lines exactly
equal the shipped log. Final theorem dependencies are the standard three
logical axioms plus 21 disclosed native-evaluation hooks, with no `sorryAx`.
All 83 source/configuration hashes match the release and remained unchanged.
Evidence is preserved in `strong/audit/chair44_build/`, including the fresh
and shipped logs, receipts and assessment. The source build is no longer running.

The unmodified release controls returned exit 1 **only** because a historical
delivery ZIP is absent from the public snapshot. Both proof builds,
admission/import checks, all four negative controls and positive scope
regressions passed. Do not label the complete control suite PASS. The release
generator's `--check` passed too. This reproduces the formal theorem with its
native-computation trust boundary; it is not human review or a theorem for
our different curved-cap solid. The original source-only reservations below
are superseded as to compilation, not full manuscript/definition auditing.

Reusable temporary checkout: `/tmp/chair44-build/release/lean/R44`, with
original phase logs at `/tmp/chair44-build/reproduction-1`.
Mathlib's cached library artifacts are in authorized RAM-backed storage
`/dev/shm/chair44-mathlib-lib`, linked from the dependency build directory;
the sandbox's separate `/dev/shm` means builds need the same execution
permission as the launched build. All 8,542 dependency cache files were
successfully re-extracted after a disk-full interruption. Do not repeat the
completed build/replay without a changed source or specific unresolved concern.

The new [companion replay](strong/review/CHAIR44_COMPANION_REPLAY.md) passed:
6,862 candidates, 1,545 direct collisions, 5,273 forced-companion rejections,
299,975 exact collision boxes, exactly 44 proper integral survivors. A fresh
reviewer reran it and found no material issue. Three mutations were rejected.
Scripts and hashed results are in `strong/audit/`; this independent finite
result assumes the continuous companion/retained-core lemmas.

**Direct overlap discovered — reassess before outreach:**
[`Chair44 comparison`](strong/review/TSIOKOS_CHAIR44_COMPARISON.md) records
Tsiokos's September 15–16 Zenodo preprint and pinned source release. An exact
`uv` comparison identifies the same eight child poses, 44 fine contacts,
30 closed contacts, 44 macro contacts, 372 signed equations and 192 feature
roles after coordinate conversion and key relabelling. The physical shapes
differ (square pyramids versus our curved caps). Their released Lean endpoint
states existence and finite symmetry for arbitrary physical tilings; source
definitions were inspected and its build/axiom audit are now reproduced above.
The entire geometric semantic chain has not received independent human review.
Our matching system cannot be presented as a distinction from this release.
Priority and independence are not established by this comparison. The old
Goodman-Strauss inquiry/brief predates this finding and needs reframing.

The user's latest interest is physical implications, core lessons, and a
3D-printable interface. The proposed next milestone is broad keyed relief
patterns, contact-test coupons, then eight- and 64-chair assemblies. This
redesign has not been implemented or verified. At a 25 mm unit-cube scale,
the current cap keys differ by only 0.0061 mm at their centers. Preserve the
frozen design and distinguish printable demonstrations from an exact-solid
theorem. Study tolerances, assembly paths and defects; diffraction requires
physical contrast such as markers or distinguishable interfaces.

A concise statement-to-geometry audit remains useful. The isolated build
and off-grid replay are complete. Our kernel-checked grid development remains
an independent cross-check, not a distinct matching-system claim.

**Proof comparison advanced:** read
[`CHAIR44_PROOF_COMPARISON.md`](strong/review/CHAIR44_PROOF_COMPARISON.md).
Our own pyramid-geometry enumerator independently recovers the 44 proper
registered contacts and no improper contacts among 2,388 carrier contacts.
A second checker matches all 192 features, 2,138 vertices and 4,272 triangles
to the released Lean data. A bounded source audit found no hidden grid
premise or concrete defect in the inspected physical-companion chain; it
is not a cold build or complete proof audit. Both checkers and hashed results
are under `strong/audit/`; those two checkers do not execute the downloaded
implementation. The subsequent build does execute the inspected release.

The report gives a written bijection of the complete legal grid models and
an attributed improvement to our geometry: after carrier-grid coverage,
clamp any actual tile's interior-ball center into a component carrier's
retained core to force common ownership. The exact bounds are
`141/35840 < rho=1/64` and `3rho² < (1/4)²`. This replaces the long component
physical-coverage/exclusion route for registration, not existence. It is
recorded as Section 8a of the geometric scrutiny, with attribution to
Tsiokos's formal argument. The subsequent Lean 4.31.0 / Mathlib 4.31.0 build
and axiom audit are complete as recorded above; our 4.34.0 toolchain is
different. No Lean source or frozen design was changed for this reproduction.

Our grid symmetry bound below remains useful but is no longer the first
priority for assessing a distinct contribution. The comparison report links
the script, exact results, version 2 PDF and metadata. The initial comparison
was data-only; the later build executed the inspected release. Both
user-supplied root PDFs (v1 and v2) are complete and
checksum-match their respective Zenodo records. Root v2 is byte-for-byte
identical to the saved v2 used in the comparison. Both were left untouched.
Translation exclusion is committed as `45d0bee`; the comparison, replay and
build evidence are included in the subsequent local research commits.
No outreach or push occurred.

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

**Universal grouping completed:** read
[`formal/UNIVERSAL_GROUPING.md`](formal/UNIVERSAL_GROUPING.md).
`Chair.ChairGrouping.universal_grouping` proves that every actual tile of any
`LegalTiling` belongs to a unique center's eight-child group. The intrinsic
parent is self when triggered and otherwise the notch owner. Parent fibers
are exactly the groups; every occurrence of the specified group has a trigger,
and any covering by group occurrences gives this same partition. Each group
has eight distinct decorated placements and agrees with the frozen children.
`parent_covariant` proves that the parent map commutes with all proper grid
motions. Coverage, the 14 exclusions, six forcing chains and exceptional
notch case are connected using exact port/cube witnesses; no motif-rule
equivalence or complete-star enumeration is assumed.

The full uv verifier passed with 31 audited declarations and 28 Lean source
hashes. Internal cross-reviews of the tiling bridge, local implications and
concrete partition found no material issue. The previous bridge was committed
as `ff440f1` at the user's request; grouping is now committed locally with
the deflation development below.
No push or outreach occurred. Source map, commands and review provenance are
in the new report; `formal/generate_grouping.py --check` is now part of the
driver. Preserve its generated `Chair/GroupingData.lean` witnesses.

**Common parity and legal deflation completed:** read
[`formal/LEGAL_DEFLATION.md`](formal/LEGAL_DEFLATION.md).
`LegalTiling.assemble` gives a legal macro tiling of actual group centers.
`LegalSolidTiling.macro_common_parity` propagates origin parity along unit
cube paths using coverage and actual macro contacts. Exact doubled support
and contact recurrence establish `LegalSolidTiling.deflate`. The combined
`LegalTiling.grouping_deflation` assumes only the initial `LegalTiling` and
derives both alignment and another legal fine tiling. `iteratedDeflation`
and its legality/step theorems give a chosen sequence at every finite depth.
No initial tiling existence or period-exclusion theorem is implied.

The latest full uv verifier passed with 44 audited declarations and 36 Lean
source hashes, using only the standard three logical axioms. Three agents
implemented assembly, boundary/parity and scaling; contributors cross-reviewed
the coordinator's deflation/iteration and the parity argument. No material
issue was found. This remains internal review. At the user's request, grouping
and deflation are committed together locally with their verification manifest
and records. No push or outreach occurred.
The macro-boundary finite check takes about 109 seconds and substantial memory;
avoid duplicate builds of it. Earlier compiled proof batches were reused.

**Translation periods excluded:** read
[`formal/TRANSLATION_EXCLUSION.md`](formal/TRANSLATION_EXCLUSION.md).
`LegalTiling.translation_period_zero` proves every integer translation period
of any `LegalTiling` is zero. `TranslationPeriod` is bidirectional invariance
of the decorated placement set, with a proved equivalence to `moveTiling`
equality. Periods preserve actual group centers; common parity and macro
coverage force each period to be even. `LegalTiling.period_halves` produces
the half-period in the legally deflated tiling. Strong induction on the sum
of absolute coordinates excludes nonzero periods across the class of legal
tilings, allowing the witnessing tiling to change at each halving.

The latest full uv verifier passed with 52 audited declarations and 40 Lean
source hashes. No new axiom or finite geometric certificate was introduced.
A third agent with no authorship role reviewed the four new modules and
traced their dependencies, reproduced direct Lean checks and the axiom audit,
and found no material defect. This is independent AI review of this addition,
not external human validation of the full construction. The preceding work
was committed as `7d84070`; translation exclusion is now committed locally
at the user's request. No push or outreach occurred.

The subsequently completed [grid symmetry step](formal/GRID_SYMMETRY.md)
defines proper grid symmetries and proves that two with the same frame
differ by a translation. Their frame map is injective, bounding the group
by 24. Initial tiling existence,
arbitrary Euclidean grid enforcement and the full physical finite-symmetry
theorem remain separate formal obligations. The conditional grid theorem
does not yet establish a physical aperiodic monotile.
The [next-milestone review](formal/NEXT_MILESTONE.md) gives the precise target
and acceptance criteria; steps A, B and C are complete. The existing proofs
use the frozen-port rules directly.

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
Python 3.13+; dependencies locked in `uv.lock`. A local Git repository now
exists; preserve research evidence and content hashes alongside commits.

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

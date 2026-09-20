# Research handoff

*Updated 20 September 2026. Read this first when resuming.*

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

**Quaquaversal matching-rule research started locally (20 September UTC):**
the user requested sustained attempts, preserving failed approaches and
continuing toward aperiodic matching rules. The active goal is in
`strong/quaquaversal/README.md`; `ATTEMPTS.md` records scope and commands.
Exact rational-metric reconstruction verifies the eight proper child maps,
28 pair separations, 14 contacts, 40 face-coverage checks and the paper's
interior three-step address. A new written obstruction
`strong/quaquaversal/PERIODIC_OBSTRUCTION.md` derives all contacts of a
two-prism periodic tiling from odd-length sibling contact paths. It rules
out arbitrary pointwise colors or involutive complements for one decoration
with the recorded proper child poses; it does not cover arbitrary recuts or
other handedness assignments. An exact script checks the domain/path
certificates. A separate degree-0..6 polynomial check agrees.
Follow-up results now reject all 512 degree-two equality/signed families
under 256 stationary handedness words (Q004), and all 60-panel constant
families (Q005, including a delayed four-prism periodic witness). Q003's
first 51-panel refinement failed vertex incidence; the preserved second
60-panel refinement passes exact area, vertex and segment audits, supporting
the known multiple-decoration theorem route without yet constructing its
decorated inventory. `MULTITYPE_ROUTE.md` records this distinction.
Q006's relative-pose atlas closes at 91 directed contacts, but an exact
24-prism periodic reflection tiling satisfies it. Q008 strengthens the
rule to full positive-area face-stars: a 512-prism proper patch supplies
80 observed stars, and a 192-prism periodic cell uses only eight of them.
Thus this stronger rule still fails. `RELATIVE_POSE_RULES.md` explains both
witnesses. Q007's 10,000 root-star models are a capped overapproximation,
not an exhaustive or realizable-star count.
**Q009/Q011 now have a stronger positive intermediate result:** closed-pair
closure has 1,291 poses (91 face, 247 edge, 953 point contacts); an independent
edge-clipping audit agrees, but the 24-prism periodic control satisfies all
these pair rules. Full interior-supertiling closed stars instead stabilize
at 6,840 types. The audited descendant closure makes this a complete language
for the stated interior-supertiling definition, not merely a sample. The
periodic control has a reachable bad-star self-loop, so every subdivision
at level >=2 remains forbidden for this stronger rule. Each legal star
recognizes exactly one child role. All 41,719 common-neighbor sibling tests
force the expected sibling role, supporting a recognizable one-level parent
partition. **Recursive parent legality is still unproved.** The eight-child
star join enumerates 58,740 necessary tuples, including all 6,255 genuine
tuples; 52,485 extras remain unknown. Comparing disjoint siblings rejects
none of them. `CLOSED_STAR_RULES.md` gives the arguments and precise gap.
**Q012–Q014 subsequently advanced these extension checks:** all 290,189
closed-star incidences now have compatibility domains, audited with rational
arithmetic. Simultaneous external domains reduce 58,740 root tuples to
11,560; external arc consistency reduces them to 9,280 (3,025 extra).
Independent synchronous propagation agrees on all 11,560 cases. Boundary
exact covers from the narrowed roles produce all 6,840 genuine parent stars
plus 9,357 distinct nonlanguage covers. Fixing all roles of each cover at
once rejects 3,373; adding one forced outer layer rejects another 1,949.
**4,035 nonlanguage covers remain unresolved.** The final rejections have
explicit empty-domain witnesses checked with sets and exact placements.
`PARENT_EXTENSION.md` records counts, arguments, commands and audit scope.
An initial boundary enumeration hit a cover cap and failed its final
genuine-count assertion; its source/failure are preserved. The repaired,
stronger arc-domain run completes without a cap and separately checks all
6,840 genuine cover witnesses.
**Resume with Q014's next layer**, from `artifacts/forced_outer_layer.json`:
survivors use its shared `poses` (10,240 positions) and `domain_pool`
(17,747 lists), and identify their parent cover by `boundary_index` and
`cover_index` in `parent_boundary_cover_arcs.json`. Repeat necessary forced
neighbor propagation on narrowed domains with explicit finite bounds.
Most old domains were singleton, so their exterior consequences matter.
Then add pairwise compatibility in the expanded patch or branch on domains
if propagation stalls. Do not call survivors realizable counterexamples.
All evidence is retained in exact JSON. No worker is left running at this
checkpoint.
**Q010 completed:** affine whole-panel groupoids give periodic witnesses for
all 256 stationary handedness words, for arbitrary pointwise equality or
real scalar opposite-sign functions. Only equality words 111/144 require
four prisms; the other 510 families require two. The audit replays 243,360
derivations and 5,140 periodic contacts. `POINTWISE_GROUPOIDS.md` limits the
scalar zero-cycle argument; arbitrary multi-fixed-symbol involutions and
independent edge labels are not covered. The constructive Q003 skeleton/
vertex-wire inventory remains another route.
`uv run --locked python strong/quaquaversal/reproduce.py` now lists 41
dependency-ordered commands; `--audit-only` checks retained hashes and result
expectations. The original 18-command replay passed, and all subsequent
commands have also run separately; the expanded combined replay has not yet
been run. It is a finite reproduction command, not a discovery loop.
`SYMMETRY_LEMMA.md` supplies a
conditional packing proof of finite symmetry groups from recognizable
prism supertiles, without assuming finitely many orientations.
The target is NOT achieved; no all-tilings hierarchy proof, single-solid
construction, external review, or new Lean claim. No publication or outreach.

**Five-agent independent review completed locally (19 September):** the user
requested independent review of the changes across the project. Separate
agents with no authoring-conversation fork reviewed geometry/dimensions,
constraint/information transfer, the rule lab, tutorial/docs, and Blender
geometry/provenance. No P1/P2 correctness issue was identified. Three P3
findings were fixed: the dimension checker now tests actual transformed
triangles against independently generated templates (plus all axes and
face-grid parity); the tutorial distinguishes the current and earlier covers
and limits its square-rendering description to Figure 1; README labels its
viewer as the square-port reference. The responsible reviewers independently
confirmed each fix. Both witnesses' 9,216 template memberships still pass,
and the dimensional JSON is byte-for-byte unchanged, preserving cover provenance.
Reviewers additionally re-derived the analytic transfer and symbolic counts,
replayed the atlas audits, compared 916,992 randomized rule-lab decisions,
and checked actual mesh faces, all 384 contact vertex sets and proper crops.
The coordinator rebuilt HTML, refreshed Firefox presentation checks, and
rebuilt the local site. Full record: `strong/review/PORT_UPDATE_REVIEW.md`;
`strong/review/port-update-review/` preserves five reports, four historical
probes, the 73-file pre-review baseline, manifests and final validation.
This is internal independent AI review, not external human acceptance or
a new Lean/printing certificate. No open reviewer finding within scope;
existing research limitations remain. No commit, publication or outreach.

**Relocated Blender cover rendered locally (19 September):** the user asked
to regenerate the cover after the dimensional tutorial update. README now
uses `docs/figures/aperiodic-chair-cover-relocated.png`, 2400×1060, depicting
the actual common-offset witness a=-1/4, b=7/32, w=3/16, delta=1/16, with
no additional feature enlargement. The three panels retain one chair,
the actual +2/-2 port pair, and the recorded eight-child assembly. Detail
uniform magnification is 8/3, and the whole assembly is shown at half scale.
`docs/render_chair_cover.py --variant relocated --samples 64` now reproduces
it; earlier square/triangular variants retain their defaults. New
`docs/relocated_cover_mesh.py` replaces overlapping square cutouts with
eight wedges per face, each filled by a cap and three flat strips. The
detail crop is a 9/8-expanded triangle inside the actual wedge, with
explicitly artificial side/backing geometry. No Blender worker changes.
A 16-sample preview and final 64-sample Cycles/OptiX render in Blender
5.2.1 LTS were visually inspected. Geometry checks passed: 470,592 triangles,
235,298 vertices, all edges paired with opposite winding, Euler characteristic
2, volume 7 to floating precision, sampled cap error below 2e-16, closed
detail meshes, 384 matched internal port pairs and the 56-cell child partition.
Source ports 40/56 in children 7/6 are unchanged; their relocated common
anchor is (-5/4,-55/32,0), checked at 91 rational triangle samples.
New adjacent notes/JSON receipt record reproduction, transformations and
eight matching input/source/image hashes. All three earlier cover PNGs
still match their preserved receipts. README, docs/INDEX and earlier
triangular-cover notes point to the new cover. Both mathematical snapshots
are unchanged; this is mesh visualization, not a manufacturing certificate.
No commit, publication, outreach, or tutorial HTML change in this render turn.

**Tutorial updated for movable dimensions locally (19 September):** the user
requested applying the dimension study to the tutorial. Section 7 now labels
the small dimensions as the recorded example, proves registration using
general offsets alpha,beta (including depth-dependent offsets), and states
the clamping inequalities with rho=1/64 for the reference and rho=1/7 for
the larger candidate. Section 10 compares both candidates at a 25 mm carrier
edge: the relocated legs are 9.375/4.6875 mm and depths 1.5625/3.125 mm.
It explains the specified family's width supremum, curved-zone separation,
and the distinction between sufficient depth bounds and manufacturing limits.
Figure 11 embeds the existing `strong/artifacts/port-dimensions.svg`; its
source/evidence hashes are now included in the presentation receipt.
Exercises 5 and 14 and their answers, the status table, further reading,
`docs/INDEX.md`, and `docs/TUTORIAL_REVIEW.md` were updated.
Pandoc rebuilt the standalone HTML without warnings. Final Firefox checks
passed at 1200/390 px: 11 embedded figures, all enlargement controls, 732
MathML expressions, 56 local links, JavaScript-disabled reading, no page
overflow, external requests or page errors. The dimension section, table
at both widths and enlarged mobile Figure 11 were visually inspected.
All receipt hashes match; the local Pages build passed its 89-link check.
The existing snapshots, meshes and cover remain unchanged. This is a local
tutorial update, not a new mathematical review, Lean proof, publication,
commit or outreach.

**Movable-anchor width/depth investigation (19 September):** the user requested
a deeper dimensional audit and explicitly rejected treating the old fixed
positions as a design-wide constraint. `strong/PORT_DIMENSIONS.md` now permits
common offsets a,b in p=f+aU+bV: they cancel exactly from every frame-locked
contact translation. For eight supports in the existing D4 face orbit and
the same 1:2 right triangle, an eight-wedge packing argument gives supremum
w=1/4 (16× recorded width), with strict separation for every smaller width.
The old 1/16 limit is only for the old anchors.
A concrete witness a=-1/4, b=7/32, w=3/16, delta=1/16 gives 12× width and
256× depth. Same-face triangles and outer face edges remain separated.
Symmetric curved zones |s|<=h psi satisfy h psi<distance to every face edge;
perpendicular-zone intersection would imply both |s_A|<|s_B| and its reverse.
An exact four-interval Bernstein certificate gives clearance >=5/256.
h=1/8 retains radius-1/4 core balls; rho=1/7 replaces the old arbitrary
1/64 inset in the component-exhaustion argument. The same fine/full-macro
predicates transfer by identical frame maps and separated local interfaces.
`uv run --locked python strong/audit/investigate_port_dimensions.py` produces
`strong/audit/port_dimensions.json` and `strong/artifacts/port-dimensions.svg`
(plus PNG), checks all eight width cases, 28 triangle pairs, 13,312 old/new
frame maps, 9,216 signed-frame memberships and the exact clearance polynomial.
Offsets can also differ between the two depth levels: a second checked
witness moves only high ports inward by U/128 and preserves all 13,312 maps
and all 672 actual same-face pairs. The 16 faces with seven low ports retain
the w<=1/4 wedge bound even in this four-parameter placement family.
Depth envelopes are sufficient, not necessary or globally optimized over a,b.
The existing snapshots, tutorial, cover and meshes are unchanged. Rendering
this witness would need a new face triangulation: enclosing squares overlap
even though the actual triangles do not. No new Lean scope, fabricated-solid
claim, commit, publication, or outreach.

**Triangular Blender cover rendered locally (19 September):** the user
requested rerendering the cover after the tutorial/shape update. README now
uses `docs/figures/aperiodic-chair-cover-triangular.png`: one chair, the actual
internal +2/-2 contact pair, and the recorded eight-child assembly. All three
panels use the same disclosed feature multipliers, width 3 and depth 64;
the close-up then applies uniform 32/3 magnification and the assembly is
shown at half the single-chair scale. Camera elevation increases for the
close-up to expose the triangular footprint. Old square covers/receipts
remain intact and link to the current version.
`docs/render_chair_cover.py --variant triangular` uses new
`docs/triangular_cover_mesh.py` with the existing Blender worker. The default
square variant retains the earlier reproduction commands. A 16-sample
preview informed the selected scales; the final 2400×1060 image used Blender
5.2.1 LTS / Cycles / OptiX / 64 samples and was visually inspected.
Mesh preparation checked triangular support and patch projected areas,
all sampled curved vertices (maximum error about 4.16e-17), 384 internal
port correspondences, 91 exact rational samples of the displayed contact,
the 56-cell child partition, positive feature-box separation and retained
cores. The area/orientation check caught and corrected reversed flat filler
triangles before the final rendering. Source port indices 40/56 in children
7/6 (zero-based) provide the shown pair. Input/source/image hashes match
`docs/figures/aperiodic-chair-cover-triangular.json`; reproduction and scope
are in the adjacent `.md`. No mathematical snapshot, existing viewer,
published site, commit or outreach was changed. The enlarged mesh is an
illustration, not a certified exact solid or manufacturing design.

**Tutorial updated for triangular ports locally (19 September):** the user
requested the tutorial update after the shape-simplification investigation.
`docs/APERIODIC_CHAIR_TUTORIAL.md` now uses the two-depth triangular cubic
candidate as the geometric main example. Section 3 explains distributed
depth encoding; Section 4.4 distinguishes preserved contact information
from numerical depths and mentions the symbolic fixed point. Section 7.1
teaches barycentric coordinates, the three-line open-patch rigidity proof,
the centroid/anchor distinction and registration transfer. Section 10 has
the new footprint/depth dimensions and preserves the unresolved fabrication
scope. Exercises 5, 13 and 19, answers and the evidence table were updated.
The square-cap formula and SVG remain as comparisons; whole-chair renderings
and the older viewer are explicitly labelled as the earlier square design.
New `docs/figures/tutorial-triangular-cap-rigidity.svg` is generated with the
existing figure script, which now writes nine SVGs including the preserved
comparison. The offline HTML still embeds ten figures.
The independent triangular checker now also verifies all 2,304 aligned panel
comparisons (192 fits, identical A/B/C rules) and trivial self-symmetry among
48 signed frames, supporting the tutorial's rule/symmetry transfer claims.
`docs/PROOF_STATUS.md` and `docs/TUTORIAL_REVIEW.md` distinguish these new
written deductions and finite checks from the earlier review and Lean scope.
Pandoc and the local Pages build passed; Firefox presentation checks cover
desktop/mobile, all figures and enlargement controls, no-JavaScript reading,
669 MathML expressions, 55 local links and zero external requests/page errors.
The latest hashes are in `docs/tutorial_verification.json`. Figure 7 was
visually inspected, including enlarged mobile presentation. No publication,
commit, frozen-data change or Lean rebuild; the existing grid theorem is
unchanged.

**Simpler port candidate investigated locally (19 September):** the user asked
to pursue a simpler shape with two depth levels and full frame rigidity.
`strong/PORT_SIMPLIFICATION.md` proposes a standard cubic triangle bubble
on a scalene right-triangle footprint, lowering polynomial degree 5 to 3.
Its three straight lines on the algebraic continuation recover the scalene
triangle and ordered axes from any open patch, including arbitrary tilted
or reflected isometries. A written transfer of the existing registration
argument is included, not a new Lean theorem or independent human review.
Degree 3 is minimal in the single-polynomial polygon-supported zero-boundary
class; a square would need degree >=5 for full ordered-frame rigidity.
An explicit planar-facet sliding control explains why a pyramid needs a
different proof, not why all polyhedral alternatives would be impossible.
`strong/audit/triangular_v1/` is a separate immutable research snapshot:
same 192 frame anchors, new triangular supports and two-depth signed keys.
The original `frozen_v1/` is unchanged. Primary checks passed via
`uv run --locked python strong/audit/simplify_ports.py`; standalone replay
`node strong/audit/crosscheck_triangular_ports.cjs` checked actual triangle
vertices, all 13,312 opposite-key pairs (1,410 distinct local poses), and
exact equality of the 44 fine and 44 full macro contact sets, with no odd
macro offsets. Primary checks also cover 15,528 periodic box separations,
9,216 frame/box memberships, volume 7 and height <=1/2048.
Evidence: `strong/audit/port_simplification.json` and
`strong/audit/triangular_ports_crosscheck.json`. The comparison figure
`strong/artifacts/port-simplification.png` is regenerated by
`uv run --locked python strong/audit/draw_port_simplification.py`.
This is algebraic simplification, not a tolerance or fabrication result;
no certified mesh, viewer replacement, commit, publication or outreach.

**Information transfer classified locally (19 September):** following the
constraint-cycle investigation, the user asked which remaining distinctions
survive across hierarchy levels. `strong/INFORMATION_TRANSFER.md` gives an
exact symbolic classification in the fixed twelve-component recoding family:
both the original 44 fine contacts and the 44 full macrocontacts are preserved
iff five specified simultaneous-equality patterns are avoided. Aligned
parent predicates depend only on two collective phase-word equality tests,
giving 44, 111 or 1,194 contacts. The symbolic substitution operator satisfies
T(F0)=F1 and T(F1)=F1. The other equality tests protect against odd parent
offsets, so the aligned count alone is insufficient.
A new two-depth witness raises only chirality-corrected components 2 and 9;
1,224 of 2,048 binary partitions preserve both full contact sets. This reduces
the prior six-depth witness without modifying frozen geometry. Minimality
is only within positive chirality-aligned amplitudes, not arbitrary solids.
`uv run --locked python strong/audit/analyze_information_transfer.py` passed;
the standalone `node strong/audit/crosscheck_information_transfer.cjs` replay
independently checked 9,189 symbolic predicates, including actual 64-child
second-level boundaries, and all 13,312 opposite-key cap-frame maps.
Results: `strong/audit/information_transfer.json` and
`strong/audit/information_transfer_crosscheck.json`. This is a proper-grid
classification and aligned hierarchy identity, not a new arbitrary-placement
proof or a classification of the 111-contact regime. UI and frozen data
unchanged in this follow-up; no commit, publication or outreach.

**Constraint-cycle explanation audited locally (19 September):** the user
noticed the graph retains one freedom after additional edges and asked about
symmetries/conservation. New `strong/CONSTRAINT_BALANCE.md` proves that the
depth-independent port chirality chi=det[u,v,n] flips at every proper
registered grid contact. Thus every selected equation graph is bipartite;
y_i=chi_i*x_i turns x_i+x_j=0 into y_i=y_j. This explains solvability for all
stationary templates, not just the successful recurrence candidate.
`uv run --locked python strong/audit/check_constraint_balance.py` passed:
independent raw-coordinate reconstruction of 1,194 contacts, 7,740 distinct
potential port-pair edges, no frame or chirality violations. The universal
graph is connected and retains one scalar. Each of the successful profile's
12 components has 16 vertices, 31 edges, rank 15 and 16 cycle dependencies.
An artificial same-chirality chord forces its component to zero; it is not
a geometric contact. Equal positive/negative counts in every selected
component also explain volume cancellation as amplitudes vary. An intrinsic
D4 permutation action on port sites gives graph automorphisms, not rigid
symmetries of the decorated solid. Recurrence/aperiodicity remain separate.
Results: `strong/audit/constraint_balance.json`. The UI and frozen geometry
were not changed in this follow-up. No commit, publication or outreach.

**Interactive matching-rule lab implemented locally (19 September):** following
the discussion of deflation, algebraic constraints and uniqueness, the user
requested an intuitive interactive treatment. The assembly header now opens
an independent three-stage dialog: reveal actual signed-contact graph edges
(one original family goes from 16 freedoms to 1), change family depths/signs,
then compare the fine and aligned-parent contact sets. Presets include the
recorded six-depth recoding (44/44) and all positive depths equal (228/44).
The three recorded maximal profile representatives give 186/1194, 44/44 and
62/398; witnesses distinguish parent-only, child-only and shared contacts.
Drawings use the actual representative child poses. The lab never writes to
assembly state and is translated into Japanese, English and Simplified Chinese.
`docs/assembly/build_rule_data.py` exports equations from preserved contact
closures, with `--check` for reproducibility. No frozen research data changes.
`node docs/assembly/verify-rule-lab.cjs` independently replays six assignments
from raw frozen port coordinates (14,328 decisions), checks every family's
graph freedom, and exercises offline controls, three languages/screen widths,
focus return and history preservation. The engine check, data reproduction
check and all eight browser suites passed; all browser records match the
final standalone HTML. Desktop/mobile layouts, witness geometry and negative
relief profiles were visually inspected. `docs/assembly.html#rules` opens the
lab directly. See `docs/assembly/README.md` for reproduction and scope.
This lab compares only aligned proper integer-grid contacts, not arbitrary
edited designs' odd offsets, recognizability or infinite tilability. Its
uniqueness discussion is restricted to the recorded maximal profile classes.
Changes are local; no commit or publication was requested.

**Parent four-panel experiment implemented locally (19 September):** the user
found deflation abrupt and requested an interactive algebraic explanation.
Grouping now initially retains child markings. Selecting a parent face in 3D
or the face list highlights its four panels and shows their normalized word
beside the parent symbol. Choosing the opposing motif and quarter-turns updates
four panel results and the coarse result together, with a Boolean-product
equation and the three-pattern dictionary. Opposing panels share one viewing
frame; the second is viewed through its back. `parent-rules.js` derives words
from the preserved child boundary, rather than storing a new motif table.
`parent-lab.js` / `.html` implement read-only choices separate from history.
Parent face clicks select the experiment; the existing child-inspection button
still opens interiors. Japanese, English and Simplified Chinese are maintained.
`node docs/assembly/verify-parent.cjs` checks all 2,304 aligned panel comparisons
(192 fitting), all 24 rotated selection maps, three languages/screen widths,
two levels and preserved history. This aligned-panel check does not replace
the complete macrocontact census, parity argument or physical geometry proof.
See `docs/assembly/README.md` for operation and reproduction. The user requested
a local commit of the experiment and language-specific judgments. Publication
was not requested.
The engine check and all seven browser suites passed on the initial experiment
HTML. Desktop and narrow-screen parent diagrams were visually inspected.
The user's localization follow-up now uses locale-specific judgments on panels:
Japanese “○ 合う / × 合わない”, English “✓ Match / ✕ No match”, and Chinese
“✓ 对得上 / ✕ 对不上”. This supersedes the intermediate all-numeric panel labels.
Equations keep 1/0, with a translated legend linking each judgment to its number.
Accessible descriptions use the same translated words. Multiplication signs in
equations retain their arithmetic meaning. The parent and locale suites cover this update;
the other five browser records refer to the preceding experiment build.

**Interactive refactoring completed locally (19 September):** the user authorized
sequential refactoring with an independent review before each local commit.
Stage 1 extracts contact presentation to `feedback.js` and shares CSS colors with
Canvas. Six browser suites passed; the reviewer confirmed 54 equivalent
classifications with no required fixes. See `docs/assembly/REFACTOR_REVIEW.md`.
Stage 2 separates state updates from rendering and shares exact results per frame.
Camera-only direct rule calls fell from check/exposed/placedFaces=2/13/13 to 1/1/2.
Six browser suites passed and the independent reviewer found no required fixes.
Stage 3 shares browser lifecycle, monitoring, HTML/hash and reporting helpers in
`browser-check.cjs`; all six suites passed again. The independent reviewer checked
success/failure cleanup, environment overrides and suite-specific diagnostics.
All three stages were reviewed before their local commits. Exact engine/history
behavior and standalone packaging are preserved. No publication was requested.

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

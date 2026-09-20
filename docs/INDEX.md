# Project index

Start with the [README](../README.md) for scope and the
[handoff](../HANDOFF.md) for the latest state. This index organizes the
existing paths so older commands, citations, and frozen evidence remain usable.

For the present mathematical claims, read the [dependency table](PROOF_STATUS.md),
the [proper grid symmetry result](../formal/GRID_SYMMETRY.md), and the
[short curved-to-grid manuscript](../strong/review/CURVED_GRID_NOTE.md).

## Quaquaversal matching-rule research

[Research entry point](../strong/quaquaversal/README.md),
[attempt register and commands](../strong/quaquaversal/ATTEMPTS.md), and
[primary-source notes](../strong/quaquaversal/LITERATURE.md).
The first result is a [periodic obstruction for one fixed
decoration](../strong/quaquaversal/PERIODIC_OBSTRUCTION.md), with exact
contact-path certificates. [Stronger pose and face-star rules](../strong/quaquaversal/RELATIVE_POSE_RULES.md)
also have explicit periodic counterexamples. The
[multiple-decoration route](../strong/quaquaversal/MULTITYPE_ROUTE.md)
has a checked 60-panel boundary structure; no successful monotile is claimed.
[Pointwise panel-map obstructions](../strong/quaquaversal/POINTWISE_GROUPOIDS.md)
now cover all 256 stationary handedness words in the stated matching models.
The [closed-star rule](../strong/quaquaversal/CLOSED_STAR_RULES.md) instead has
6,840 allowed neighborhoods and supports recognizable grouping of one parent
level. Recursive parent legality remains open.
[Exterior extension checks](../strong/quaquaversal/PARENT_EXTENSION.md)
now leave 4,035 nonlanguage parent covers after one additional forced layer;
the next experiments propagate these domains farther.

## Public presentation and provenance

- [AI assistance, attribution and chronology](PROVENANCE.md).
- [Historical-material guide](HISTORICAL_MATERIAL.md), including unsent review packets.
- [Licensing scope](../LICENSING.md) and [third-party notices](../THIRD_PARTY_NOTICES.md).
- [Publication review](PUBLICATION_REVIEW.md), [local audit](publication_audit.json)
  and [read-only GitHub snapshot](publication_github.json); scanner
  [controls](check_publication_audit.py) and [results](publication_controls.json).

## Undergraduate tutorial

The README's [Blender cover](figures/aperiodic-chair-cover-relocated.md)
now shows the relocated triangular candidate at its actual design proportions,
an actual matching +2/-2 pair and the eight-child assembly. The design uses
12× width and 256× depth relative to the small snapshot, with no extra
feature exaggeration. The linked receipt records the new wedge-based mesh,
closed-seam and contact checks; earlier covers remain available.

[Interactive assembly prototype](assembly.html) opens offline in a browser:
face matching, a fixed assembly plus one moving piece, undo, and parent/child
exploration. Its interface supports [Japanese, English and Simplified Chinese](locales/README.md) and includes a short illustrated
“How to play” guide; the longer mathematics tutorial is a separate resource.
After grouping, a face experiment compares the four child-panel contacts with
the effective parent symbol, using quarter-turn controls and a Boolean-product
equation. [Aligned panel checks and UI record](assembly_parent_verification.json).
The guide also offers a cursor demonstration with pause, step and replay.
Selecting both faces animates separation (for an existing preview), rotation,
and approach; bonding still requires the explicit Attach button.
[Build, checks and current limitations](assembly/README.md).

[Read online](https://tritonlab.io/aperiodic-chair-lab/tutorial/) ·
[Download HTML](https://tritonlab.io/aperiodic-chair-lab/downloads/tutorial.html) ·
[Site build and deployment](PAGES.md).

The local Pages build now starts with a three-language home page whose
primary links open the assembly activity and its operation demonstration.
This redesign has not yet been deployed; [local browser checks](site_preview_verification.json).

[Interactive assembly specification draft](INTERACTIVE_ASSEMBLY_SPEC.md)
records the proposed fixed assembly + moving piece interaction, contact-face
comparison, guided first-parent construction, reversible editing, and
eight-child/parent inspection that preserves ongoing work. The prototype
implements the core interaction; its notes distinguish remaining design work.
The [player UX review record](INTERACTIVE_ASSEMBLY_REVIEW.md) records the
coordinator's reread, two independent AI reviews and the resulting clarifications.

[How one shape can enforce order without repetition](APERIODIC_CHAIR_TUTORIAL.html)
develops the local parent proof, parity and legal deflation, period halving,
the five-step curved-surface registration argument, and the existence limit.
Eleven figures and 19 worked exercises connect these to physical implications
and printable-interface proposals. The geometric main example now uses
two-depth triangular cubic ports, with the earlier square cap retained
for comparison. Depth encoding, the three-line rigidity proof, print-scale
estimates and exercises reflect the new candidate. Movable offsets and a
12×-width, 256×-depth example distinguish recorded dimensions from design
constraints, with a comparison figure and updated Exercises 5 and 14; Lean scope remains
the preserved grid model. Finite census data remain in the linked
complete tables. The HTML opens
offline with embedded figures, styling and native MathML; links to project
reports require the repository. [Markdown source](APERIODIC_CHAIR_TUTORIAL.md).
[Firefox verification record](tutorial_verification.json) records desktop
and mobile checks, local links, offline resources and artifact hashes.
The [independent tutorial review](TUTORIAL_REVIEW.md) records mathematical,
first-reader, and presentation findings, the applied changes, and follow-up
checks. It is AI review, not a student comprehension trial.
The later [five-agent review of the current port, tutorial, rule-lab and
rendering changes](../strong/review/PORT_UPDATE_REVIEW.md) records independent
re-derivations and probes, three corrected findings, and preserved reviewer reports.

Rebuild the nine tutorial vector diagrams (including the preserved square-cap
comparison), the dimension-study figure, and HTML from the repository root:

```sh
uv run --locked python docs/draw_tutorial_figures.py
uv run --locked python strong/audit/investigate_port_dimensions.py
pandoc docs/APERIODIC_CHAIR_TUTORIAL.md --from=markdown-implicit_figures --to=html5 \
  --standalone --embed-resources --math-method=mathml --toc --toc-depth=2 \
  --resource-path=docs --css=tutorial.css \
  --include-after-body=docs/tutorial-controls.html \
  --output=docs/APERIODIC_CHAIR_TUTORIAL.html
```

Optional Firefox presentation check (requires an existing Playwright and
Firefox installation; configure `PLAYWRIGHT_MODULE` and `FIREFOX_PATH` if
they differ from the script's local defaults):

```sh
node docs/verify_tutorial.cjs
```

This regenerates `tutorial_verification.json` with file hashes and checks
embedded images, MathML, local links, and desktop/mobile layout. It does not
verify the mathematical claims. The figure generator checks the 56-cube
partition used in its group diagram; diagrams omit the curved decorations
or exaggerate dimensions wherever their captions say so.
The Pandoc input option keeps the explicit captions visible in both Markdown
and HTML without also turning image alt text into a duplicate caption.
The embedded controls let readers enlarge and pan diagrams offline, with
keyboard activation, Escape/Close, and focus restoration. Without JavaScript,
the text, original figures, and formulas remain readable; the extra controls
are absent.

## Current chair research

| Subject | Report | Reproduction or evidence |
|---|---|---|
| Chair44 direct overlap | [Exact comparison and revised assessment](../strong/review/TSIOKOS_CHAIR44_COMPARISON.md) | [Comparator](../strong/audit/compare_chair44.py), [exact results](../strong/audit/chair44_comparison.json) |
| Chair44 proof comparison and shorter registration proof | [Proof comparison](../strong/review/CHAIR44_PROOF_COMPARISON.md), [formal-source audit](../strong/review/CHAIR44_FORMAL_SOURCE_AUDIT.md) | [Independent atlas reconstruction](../strong/audit/reconstruct_chair44_contacts.py), [Lean literal check](../strong/audit/check_chair44_lean_literals.py) |
| Chair44 off-grid census and build reproduction | [Companion replay](../strong/review/CHAIR44_COMPANION_REPLAY.md), [build record](../strong/review/CHAIR44_BUILD_REPRODUCTION.md) | [Replay](../strong/audit/replay_chair44_companions.py), [corruption controls](../strong/audit/check_chair44_replay_mutations.py), [build driver](../strong/audit/build_chair44_release.py) |
| Lean contact recurrence and arbitrary grid tilings | [Scope and reproduction](../formal/README.md), [tiling bridge](../formal/GRID_TILING_BRIDGE.md) | [Recurrence](../formal/Chair/Recurrence.lean), [tiling theorems](../formal/Chair/Tiling.lean), [verification driver](../formal/verify.py) |
| Universal unique grouping in Lean | [Proof record and scope](../formal/UNIVERSAL_GROUPING.md) | [Grouping theorem](../formal/Chair/Grouping.lean), [local forcing](../formal/Chair/LocalGrouping.lean) |
| Common parity and legal deflation in Lean | [Proof record and scope](../formal/LEGAL_DEFLATION.md) | [Combined theorem and iteration](../formal/Chair/Hierarchy.lean), [deflation proof](../formal/Chair/Deflation.lean) |
| Translation-period exclusion in Lean | [Proof record and scope](../formal/TRANSLATION_EXCLUSION.md) | [Final theorem](../formal/Chair/TranslationExclusion.lean), [period halving](../formal/Chair/PeriodHalving.lean) |
| Proper grid symmetry bound in Lean | [At most 24 symmetries](../formal/GRID_SYMMETRY.md) | [Frame injection and exhaustive list](../formal/Chair/Symmetry.lean) |
| Current proof dependencies | [Claim/evidence table](PROOF_STATUS.md) | [Lean manifest](../formal/verification.json) |
| Short geometric manuscript | [From curved contacts to one grid](../strong/review/CURVED_GRID_NOTE.md) | Frozen coordinates and finite checks linked in the manuscript |
| Independent review of the symmetry/geometric follow-up | [Review findings and limits](../strong/review/FOLLOWUP_INDEPENDENT_REVIEW.md) | [Independent geometric probe](../strong/audit/review_curved_grid_note.py), [result](../strong/audit/curved_grid_note_review.json) |
| Arbitrary placements → one grid | [Geometric scrutiny](../strong/review/GEOMETRIC_GRID_SCRUTINY.md) | [Primary checker](../strong/audit/scrutinize_grid_bridge.py), [alternate checker](../strong/audit/grid_bridge_crosscheck.py) |
| Proposed exact solid and hierarchy | [Recut chair](../strong/RECUT_CHAIR.md) | [Frozen-coordinate audit](../strong/audit/README.md) |
| Reflections and face patterns | [Follow-up](../strong/FOLLOWUP_REFLECTIONS.md) | [Reflection checker](../strong/audit/check_reflections.py) |
| Why redundant matching constraints remain consistent | [Chirality, cycle balance and volume neutrality](../strong/CONSTRAINT_BALANCE.md) | [Coordinate audit](../strong/audit/check_constraint_balance.py), [exact results](../strong/audit/constraint_balance.json) |
| Which distinctions survive grouping | [Five forbidden equality patterns and a two-depth witness](../strong/INFORMATION_TRANSFER.md) | [Symbolic analysis](../strong/audit/analyze_information_transfer.py), [independent replay](../strong/audit/crosscheck_information_transfer.cjs), [results](../strong/audit/information_transfer.json) |
| Simpler port geometry | [Scalene triangular cubic cap](../strong/PORT_SIMPLIFICATION.md) | [New snapshot](../strong/audit/triangular_v1/README.md), [primary checks](../strong/audit/simplify_ports.py), [independent replay](../strong/audit/crosscheck_triangular_ports.cjs) |
| Movable-anchor width/depth bounds | [Dimension study and larger witness](../strong/PORT_DIMENSIONS.md) | [Exact checker](../strong/audit/investigate_port_dimensions.py), [evidence](../strong/audit/port_dimensions.json), [layout/parameter figure](../strong/artifacts/port-dimensions.svg) |
| Local eight-chair grouping | [Parent rule](../strong/MOTIF_GROUPING.md) | [Grouping checker](../strong/audit/motif_grouping.py) |
| Proof dependencies and existence | [Dependency audit](../strong/review/DEPENDENCY_AUDIT.md) | [Review verifier](../strong/review/verify_package.py) |
| Substitution dynamics | [Scrutiny addendum](../strong/review/SCRUTINY_ADDENDUM.md) | [Cube exploration](../strong/audit/explore_cube_substitution.py) |
| Prior work | [Literature follow-up](../strong/review/LITERATURE_FOLLOWUP.md), [direct predecessors](../strong/review/DIRECT_PRIOR_ART_AUDIT.md) | [Published chair-code comparison](../strong/audit/compare_published_chair_code.py) |
| Old markings versus our face patterns | [Contact comparison](../strong/review/GOODMAN_STRAUSS_COMPARISON.md) | [Exact checker](../strong/audit/compare_goodman_strauss.py) |
| Local reconstruction obstructions | [Latest argument](../strong/review/AUXILIARY_RECONSTRUCTION.md) | [Witness checker](../strong/audit/reconstruct_gs_auxiliary.py) |

These are research arguments and finite certificates, with the limitations
stated in each report. In particular, the latest connected-cross discrepancy
is an unresolved source-model question, not an established correction to
the published paper.

## Earlier experiments and lessons

- [Findings and methodological lessons](../FINDINGS.md).
- [Strong-aperiodicity search](../strong/README.md),
  [second pass](../strong/SECOND_PASS.md),
  [open fusion](../strong/OPEN_FUSION.md), and
  [eight-chair exploration](../strong/EIGHT_CHAIRS.md).
- [SCD derivation](../RESEARCH.md), [geometry](../geometry.py),
  [verification](../verify.py), and [exports](../build.py).
  SCD admits screw symmetry and is a reproduction of a known construction.

## Viewers and review material

- Current candidate: [chair viewer](../strong/artifacts/recut-chair.html).
- Earlier SCD model: [viewer](../viewer.html) or
  [exported explorer](../artifacts/explorer.html).
- [Outside-review index](../strong/review/README.md) and
  [research/review chronology](../strong/review/RECORD.md).
- Frozen v1 delivery: [PDF](../strong/artifacts/review-brief.pdf),
  [HTML](../strong/artifacts/review-brief.html),
  [ZIP](../strong/artifacts/review-goodman-strauss-v1.zip).
  Later research addenda are separate; the inquiry remains unsent.

The viewers work directly from disk. Meshes approximate the exact surfaces;
they do not inherit the proposed exact-solid theorem automatically.

## Directory map

```text
README.md, HANDOFF.md, AGENTS.md   overview, current state, working guidance
docs/                            navigation and repository record
formal/                          Lean definitions, certificates, and recurrence proof
strong/*.md                      chair proposal and earlier search reports
strong/*.py, strong/*.cpp         construction and search implementations
strong/audit/                    coordinate verifiers, witnesses, certificates
strong/audit/frozen_v1/           immutable candidate snapshot
strong/review/                   literature, scrutiny, correspondence drafts
strong/artifacts/                search evidence, figures, viewers, review packet
geometry.py, verify.py, build.py  original SCD implementation
artifacts/, viewer.html          original SCD outputs and offline viewer
pyproject.toml, uv.lock           Python environment and locked dependencies
```

## Commands

Run from the repository root, using Python 3.13+ through `uv`:

```sh
uv sync --locked

# Lean recurrence milestone (requires the pinned Lean toolchain).
uv run --locked python formal/verify.py

# Verify the frozen snapshot hashes without regenerating evidence.
uv run --locked python strong/review/verify_package.py --hashes-only

# Run the six primary checks in a temporary copy.
uv run --locked python strong/review/verify_package.py

# Recheck the geometric bridge hypotheses; these write their result JSON.
uv run --locked python strong/audit/scrutinize_grid_bridge.py
uv run --locked python strong/audit/grid_bridge_crosscheck.py

# Reproduce the latest comparisons; these write their result JSON/tables.
uv run --locked python strong/audit/compare_goodman_strauss.py
uv run --locked python strong/audit/reconstruct_gs_auxiliary.py

# Earlier SCD work.
uv run --locked python verify.py
uv run --locked python build.py
```

Some searches require `g++` with C++17 support. Browser checks use Node.js;
Firefox checks additionally need Playwright and Firefox, configured through
`PLAYWRIGHT_MODULE` and `FIREFOX_PATH`. PDF/package generation needs Pandoc
and LaTeX. None of these extra tools is needed to open the existing viewers.

Preserve the frozen snapshot and v1 delivery artifacts. Inspect `git diff`
after generators run; evidence changes should accompany an explanatory
research record. See [repository policy](REPOSITORY.md).

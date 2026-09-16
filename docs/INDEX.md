# Project index

Start with the [README](../README.md) for scope and the
[handoff](../HANDOFF.md) for the latest state. This index organizes the
existing paths so older commands, citations, and frozen evidence remain usable.

## Undergraduate tutorial

[How one shape can enforce order without repetition](APERIODIC_CHAIR_TUTORIAL.html)
introduces the chair, local grouping, period halving, physical implications,
and printable-interface proposals, with worked exercises. The HTML opens
offline with embedded figures, styling and native MathML; links to project
reports require the repository. [Markdown source](APERIODIC_CHAIR_TUTORIAL.md).
[Firefox verification record](tutorial_verification.json) records desktop
and mobile checks, local links, offline resources and artifact hashes.

Rebuild the HTML from the repository root with Pandoc:

```sh
pandoc docs/APERIODIC_CHAIR_TUTORIAL.md --from=markdown --to=html5 \
  --standalone --embed-resources --math-method=mathml --toc --toc-depth=2 \
  --resource-path=docs --css=tutorial.css \
  --output=docs/APERIODIC_CHAIR_TUTORIAL.html
```

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
| Arbitrary placements → one grid | [Geometric scrutiny](../strong/review/GEOMETRIC_GRID_SCRUTINY.md) | [Primary checker](../strong/audit/scrutinize_grid_bridge.py), [alternate checker](../strong/audit/grid_bridge_crosscheck.py) |
| Proposed exact solid and hierarchy | [Recut chair](../strong/RECUT_CHAIR.md) | [Frozen-coordinate audit](../strong/audit/README.md) |
| Reflections and face patterns | [Follow-up](../strong/FOLLOWUP_REFLECTIONS.md) | [Reflection checker](../strong/audit/check_reflections.py) |
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

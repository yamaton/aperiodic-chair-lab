# Lean proofs: grouping, deflation and translation exclusion

*16 September 2026. Lean 4.34.0, bundled Std, no Mathlib dependency.*

**Completed:** the full 24-orientation build, construction integrity checks,
and final axiom audit passed. The [verification record](verification.json)
identifies the exact source hashes and theorem dependencies. This establishes
the normalized-grid recurrence statement below, not the entire proposed
aperiodic-solid theorem.

**Grid-tiling bridge completed:** [result and proof map](GRID_TILING_BRIDGE.md).
Arbitrary legal grid tilings now have a precise definition. Common proper
grid motions preserve legality, coverage supplies actual face neighbors,
and those neighbors normalize to the certified contact lists. The recurrence
also applies to arbitrarily placed macro pairs.

**Universal grouping verified:** [proof and scope](UNIVERSAL_GROUPING.md).
Every legal grid tiling has an intrinsic parent assignment into the specified
eight-chair groups. The proof connects coverage to the 14 contact exclusions,
six forcing chains and exceptional notch case using the actual frozen ports.
**Common parity and legal deflation verified:** [proof and scope](LEGAL_DEFLATION.md).
The assembled parents have a common origin residue modulo two; halving their
aligned placements yields another `LegalTiling`. A chosen sequence repeats
this operation legally at every finite depth.

**Translation exclusion verified:** [proof and scope](TRANSLATION_EXCLUSION.md).
Every integer translation period of any `LegalTiling` is zero. Periods
preserve group centers, must be even by common parity, and halve under legal
deflation; descent on an integer norm excludes nonzero periods. Initial tiling
existence and the full finite-symmetry conclusion remain separate targets.

## Precise target

For the first chair/group at the origin in the identity frame, every listed
proper cubic orientation `r`, and **every** integer vector `t`, prove:

```text
macroContact r t ↔ ∃ s : Int³, t = 2s ∧ fineContact r s.
```

The main theorem is [`Chair.macro_contact_recurrence`](Chair/Recurrence.lean).
It retains the same orientation `r` on both sides. Its corollary makes all
three macro-offset coordinates even. The accepted lists contain 44 distinct
oriented contacts at each scale, before removing local dead ends. No
assumption restricts the universe to the 30 substitution contacts.

Here a contact means:

1. The occupied unit cubes have disjoint interiors (distinct lower corners).
2. At least one pair of exposed unit faces coincides with opposite normals.
3. Every coincident opposing face has matching ports in both directions:
   positions and ordered axes agree, and signed keys are opposite.

The explicit face-contact requirement matters: a distant disjoint placement
is not a contact. All 24 decorated frames remain distinct states; we never
identify the three poses sharing the same unmarked chair support.

## Why the computation is exhaustive

A touching face pair has doubled centers `a` and `b`, satisfying
`a = b + 2t`. Consequently `t = (a-b)/2`. Lean proves this for arbitrary
integer vectors and uses the face witness in the contact definition to put
every contact into the finite list derived from all opposing face pairs.
There is no assumed search radius or precondition that offsets are even.

Python proposes accepted offsets and rejection witnesses. Each rejected
offset names either two overlapping cells or two opposing faces that fail
the matching rule. Out-of-range indices fail. Lean checks every witness,
checks accepted contacts in full, and checks that the two lists cover every
touching offset. The generic soundness theorem then identifies the accepted
list with the complete contact language on the infinite integer lattice.

This is a proof about all offsets supported by finite certificates, rather
than an observation that one bounded search found 44 results.

## Construction and trust boundary

[`generate_input.py`](generate_input.py) exports only the frozen seven cells,
192 ports, and eight child placements. It pins the candidate's SHA-256 and
converts rational positions exactly to integer sixteenths. Lean reconstructs
faces, rotations, the child cells, and the macro boundary from those literals.
The JSON-to-Lean export is reproducibly checked in Python; Lean does not
parse the JSON or certify its SHA-256 itself. The correspondence of these
definitions with the intended geometric model remains a review obligation.

[`Integrity.lean`](Chair/Integrity.lean) checks that:

- The 192 ports are assigned exactly once to 24 faces, eight per face.
- The eight distinct children have disjoint cells and matching internal faces.
- Their 56 cells equal the doubled chair and expose 96 unit faces.
- The complete macro face records equal the placed-child boundary after
  cancelling internal opposing faces.
- The 24 enumerated matrices are proper signed permutations. Every ordered
  pair of perpendicular signed coordinate axes appears with its positively
  oriented third axis.

Generated geometry caches are optimizations: Lean first proves them equal
to its own reconstruction. Generated witness tables have no assumed validity.
The Python search and the old Python contact table are not proof premises.

Finite certificates use `decide +kernel`; the small rotation checks use
`decide_cbv`. Both produce kernel-checked proofs. No `native_decide`, `sorry`,
or project-specific axiom is used. [`Audit.lean`](Audit.lean) reports the
transitive axiom dependencies, and the driver rejects dependencies beyond
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`.

## Scope and remaining work

These are **integer-grid matching and conditional tiling theorems**. They do
not yet formalize:

- The curved physical solid or the arbitrary-placement-to-grid argument.
- Initial tiling existence or the finite-symmetry conclusion.
- Reflections, novelty, or the behavior of meshes and manufactured objects.

Those statements must not be hidden in the interpretation of this result.
The next symmetry target is injectivity of the proper-frame map on grid
symmetries, giving a finite bound of 24. Initial existence is a separate branch.
The [next-milestone plan](NEXT_MILESTONE.md) specifies the unrestricted tiling
definition, universal grouping theorem, and global parity/deflation obligations.

## Reproduce

Install the toolchain pinned in [`lean-toolchain`](lean-toolchain), normally
through elan. From the repository root, with `lake` available:

```sh
uv run --locked python formal/verify.py
```

For a directly extracted Lean distribution:

```sh
uv run --locked python formal/verify.py --lake /path/to/lean/bin/lake
```

Add `--write-report` to update the tracked validation summary. The driver
checks deterministic regeneration, builds the Lean project, audits axioms,
and compares all 44 fine contacts with the earlier coordinate checker.
A cold build is substantial; successful incremental checks reuse `.lake/`.
The build limits Lean to four threads per module. Build outputs are ignored.
The first run used `/tmp/lean-4.34.0-linux/bin/lake`; tools in `/tmp` are not
part of the repository and may disappear between sessions.

To deliberately regenerate source certificates:

```sh
uv run --locked python formal/generate_input.py
uv run --locked python formal/generate_certificates.py
uv run --locked python formal/generate_grouping.py
```

The contact generator regenerates `Witnesses.lean`, `Cache.lean`, `Checked.lean`, the
four `Batches/Batch*.lean` proof modules, and `certificate_summary.json`.
The independent batches bound peak memory and run concurrently. Review diffs
and rebuild after regeneration.
The grouping generator emits `GroupingData.lean`; its old motif-certificate
input supplies proposed witnesses, all checked against the actual Lean model.

## File map

| File | Role |
|---|---|
| [Model](Chair/Model.lean) | Contact semantics and generic enumeration completeness |
| [Geometry](Chair/Geometry.lean), [Input](Chair/Input.lean), [Candidate](Chair/Candidate.lean) | Coordinate construction and normalized contact definitions |
| [Certificate](Chair/Certificate.lean) | Generic certificate checker and soundness theorem |
| [Witnesses](Chair/Witnesses.lean), [Cache](Chair/Cache.lean), [Checked](Chair/Checked.lean) | Untrusted data and checked concrete certificates |
| [Integrity](Chair/Integrity.lean) | Construction and boundary checks |
| [Recurrence](Chair/Recurrence.lean) | Unconditional normalized recurrence theorem and counts |
| [Frames](Chair/Frames.lean), [Covariance](Chair/Covariance.lean) | Placement algebra and frame covariance of full contact records |
| [Boundary](Chair/Boundary.lean), [Tiling](Chair/Tiling.lean) | Exposed-face ownership, arbitrary tilings and the contact-certificate bridge |
| [GroupingData](Chair/GroupingData.lean), [generator](generate_grouping.py) | Checked finite grouping witnesses and exact frozen-child correspondence |
| [Neighborhood](Chair/Neighborhood.lean), [Occurrences](Chair/Occurrences.lean) | Every legal tiling supplies complete local face options and sound conflicts |
| [LocalRules](Chair/LocalRules.lean), [LocalGrouping](Chair/LocalGrouping.lean) | Generic propagation and concrete contact exclusions/forcing |
| [Partition](Chair/Partition.lean), [Grouping](Chair/Grouping.lean) | Intrinsic parent assignment and universal unique grouping |
| [SolidTiling](Chair/SolidTiling.lean), [SolidContacts](Chair/SolidContacts.lean) | Generic solid coverage, ownership and adjacency-to-contact proofs |
| [MacroAssembly](Chair/MacroAssembly.lean), [MacroBoundary](Chair/MacroBoundary.lean), [MacroParity](Chair/MacroParity.lean) | Legal macro assembly and globally forced parity |
| [Scaling](Chair/Scaling.lean), [Deflation](Chair/Deflation.lean), [Hierarchy](Chair/Hierarchy.lean) | Exact scaling, legal deflation and every-finite-depth iteration |
| [Translations](Chair/Translations.lean), [PeriodHalving](Chair/PeriodHalving.lean) | Genuine translation periods, center transport and halving |
| [IntegerDescent](Chair/IntegerDescent.lean), [TranslationExclusion](Chair/TranslationExclusion.lean) | Descent across legal tilings and exclusion of every nonzero integer period |
| [Verifier](verify.py) | Source correspondence, build, axiom audit, independent comparison |
| [Controls](Chair/Controls.lean) | Deliberately incomplete/incorrect certificates must fail |

## Exploration record

The initial direct evaluation rebuilt all contacts using repeated large
list traversals. Both proof-producing evaluation and direct kernel reduction
were too expensive in that form; the benchmark runs were stopped. This was
a resource problem, not a mathematical counterexample. Indexed rejection
witnesses and proved normalization caches make the proof substantially
smaller while retaining exhaustiveness. Plain list equality was also the
wrong recurrence test because the two enumerations have different orders;
the final statement compares membership, and counts use separate uniqueness
proofs.

Two subagents contributed generic definitions/proofs and construction checks.
They also reviewed each other's integration where applicable; neither is an
independent human reviewer. Their roles and final verification are recorded
in the [research chronology](../strong/review/RECORD.md).

## Independent agent review of the normalized recurrence

A fresh agent that did not author this formalization subsequently reviewed
the milestone. Its [assessment](INDEPENDENT_REVIEW.md) found no material
defect and requested no implementation change. It reproduced the incremental
Lean checks, expanded the axiom audit, and independently reconstructed the
geometry and all contact sets without importing project helper modules.

The preserved [independent probe](independent_review_probe.py) and
[results](independent_review_results.json) recover 1,194 fine and 6,801 macro
disjoint geometric contacts, with exactly 44 fitting contacts at each scale
and exact same-frame doubling. Run from the repository root:

```sh
uv run --locked python formal/independent_review_probe.py
```

This is a review independent of implementation authorship, not an external
human review or a verification of the complete physical theorem. The review
documents its commands, alternative arithmetic methods, trust assumptions,
and the fact that its Lean build reused cached artifacts.
The later grid-tiling addition has the internal cross-review described in
[its record](GRID_TILING_BRIDGE.md); it was not covered by that earlier review.
The grouping addition likewise has its own [implementation and review
record](UNIVERSAL_GROUPING.md), separate from the first milestone's review.

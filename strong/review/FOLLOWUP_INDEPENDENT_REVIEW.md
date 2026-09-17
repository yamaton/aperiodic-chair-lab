# Independent review of grid symmetry and the short geometric manuscript

*16 September 2026. Requested after implementation; local review record.*

## Outcome

Two fresh AI agents, neither involved in implementing this addition, reviewed
the Lean symmetry result and the short curved-to-grid manuscript separately.
**Neither found a material mathematical or implementation defect.** The
coordinator also rechecked the definitions, argument and presentation, and
made two minor documentation clarifications described below. No Lean proof,
solid coordinate, certificate or verification manifest changed during review.

This is an independent agent review in the sense of no implementation role
and fresh conversation context. The agents could read the same repository
arguments and used the same model family. It is not external human review,
nor a complete independent audit of the earlier formal development.

## Lean reviewer: `review_grid_symmetry`

The reviewer inspected [Symmetry.lean](../../formal/Chair/Symmetry.lean),
the existing motion/tiling/translation definitions, the audit driver and
the [scope report](../../formal/GRID_SYMMETRY.md).

- Symmetry is equality of the **entire** decorated placement set under the
  existing group action. Identity, composition and inverse closure are valid.
- Equal-frame cancellation has the correct order: `g ∘ h⁻¹` translates by
  `g.shift - h.shift`. The existing translation-exclusion theorem then gives
  frame injectivity, without adding assumptions to `LegalTiling`.
- The distinct-list bound and the exhaustive-list theorem both prove their
  stated claims. In particular, the latter proves both directions of
  membership and does not assume finiteness of the symmetry set.
- Classical choice selects a representative for each occurring frame;
  documentation correctly distinguishes this from a decision algorithm.
- The result concerns proper integer-grid motions. Initial existence,
  arbitrary physical placements and the physical-solid theorem remain outside
  its scope.

The reviewer ran, from the repository root:

```sh
/tmp/lean-4.34.0-linux/bin/lake -d formal env lean formal/Chair/Symmetry.lean
/tmp/lean-4.34.0-linux/bin/lake -d formal env lean formal/Audit.lean
```

Both passed. A separate read-only Python check through `uv` confirmed that
all **41 source hashes** and **62 fresh axiom entries** match
[verification.json](../../formal/verification.json), and that the declaration
names match `verify.py`. Only `propext`, `Classical.choice`, and `Quot.sound`
occur. Imported compiled dependencies were reused. The reviewer did not
repeat the full generator pipeline, cold-build old proof batches or Chair44,
or independently reprove all earlier translation-exclusion dependencies.

## Geometry reviewer: `review_curved_note`

The reviewer inspected the [short manuscript](CURVED_GRID_NOTE.md), frozen
coordinates and supporting reports, and checked the scope table in
[PROOF_STATUS.md](../../docs/PROOF_STATUS.md).

The reviewer found the five-lemma chain coherent: interior-ball packing
precedes the finite boundary-cover argument; polynomial division extends
open coincidence to the entire algebraic graph; the line classification
fixes the full base frame; opposite local sides and handedness force a
proper integral adjacent owner; carrier coverage and retained-core clamping
exhaust the actual tiling without assuming prior component material coverage.
Unique ownership then makes all eight cap mates the same neighboring tile.

A newly written exact-arithmetic/SymPy probe imports no project helper code.
It independently checks the frozen hash and cells, every port's axes and
actual face, key chirality, box separation, all 1,536 opposite-key placements,
properness, integrality and adjacent ownership using all eight cube corners.
It recovers 86 poses and checks the four line-coefficient identities, the
trivial fifth-line square stabilizer, and retained-core/diameter bounds.

The coordinator preserved the probe byte-for-byte as
[review_curved_grid_note.py](../audit/review_curved_grid_note.py), inspected it
and reran it successfully. Its result is recorded in
[curved_grid_note_review.json](../audit/curved_grid_note_review.json).
Reproduce with assertions enabled, from the repository root:

```sh
uv run --locked python strong/audit/review_curved_grid_note.py
```

The probe checks finite and symbolic hypotheses; the reviewer separately
examined the analytic/topological reasoning. The reviewer did not reprove
infinite tiling existence, audit all of the physical-symmetry transport
argument, or run Lean. No missing formalization was treated as a mathematical
counterexample.

## Coordinator self-review and changes

The coordinator revisited the bidirectional definition of a translation
period, the absence of grouping or finiteness assumptions in `LegalTiling`,
the composition order, completeness of the symmetry list, and the separation
of the existence and physical-to-grid branches. The cap proof was rechecked
for normal-sign conventions, all line-direction cases and the use of
carrier coverage in the clamping step. No substantive correction was found.

Two low-impact wording issues were corrected:

1. The grid-symmetry report previously called the mapped rotation list a
   “sublist in the sense of set inclusion.” It now says “a list of distinct
   entries from the 24 listed rotations,” explicitly making order irrelevant.
   The Lean proof already used set-style list inclusion, not ordered sublists.
2. The review index now explicitly restricts its link to the earlier
   independent formal review to the normalized recurrence milestone. Expanding
   the surrounding description to the full development could otherwise make
   that older review appear to cover later grouping and symmetry additions.

The Lean reviewer also requested updating the “no fresh independent reviewer”
status after this review. Current scope documents and the handoff now link
this record; the implementation chronology remains distinguished from the
subsequent review.

## Reviewed inputs

These hashes identify the inputs at the start of review. Subsequent manuscript
and status-table edits only add review-provenance links; the mathematical
content of those two documents is unchanged. The Lean source and manifest
remain byte-for-byte unchanged.

| Input | SHA-256 |
|---|---|
| `formal/Chair/Symmetry.lean` | `510d72e3679ce931c544ba8d8a14efdd06d3bc8820a39dca40406c91975db9dd` |
| `formal/verification.json` | `b3d2a1e46ec7281175bad41cafb408308136abf56e28bc9ff1baf9a98d745114` |
| `strong/review/CURVED_GRID_NOTE.md` | `33324a2491ea4e44e504c08c9b81bcc89c1a58bc3c0981c7c360ba0b8d6406d5` |
| `docs/PROOF_STATUS.md` | `af08f0289ca179b9e88dcf52ae28cd1a26786378241de2b5dcaccfb26e0cdbe2` |
| Independent geometry probe | `da0878ddd92602b73017edbef65f1401b78e5ef5d2bbf4f15cfd6f58a32ce1d9` |

No new proof claim, commit, publication or outreach resulted from this review.

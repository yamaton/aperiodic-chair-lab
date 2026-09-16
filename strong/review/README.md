# Outside-review preparation: Goodman-Strauss

*16 September 2026. Prepared locally; no inquiry sent, no external review received.*

The user selected Chaim Goodman-Strauss as the intended initial recipient.
The immediate purpose is a limited correctness/novelty assessment, not a
journal recommendation or endorsement.

**New overlap, 16 September:** the [Chair44 comparison](TSIOKOS_CHAIR44_COMPARISON.md)
identifies our exact discrete system in Tsiokos's public construction, with a
different physical realization and a stronger claimed formal theorem. The
draft and frozen attachment below predate this finding and require reframing
before use. They remain preserved as historical material.

## Start here

- [Chair44 exact comparison](TSIOKOS_CHAIR44_COMPARISON.md): source versions,
  coordinate equivalence, actual Lean scope, chronology limits and revised work.
- [Chair44 proof comparison](CHAIR44_PROOF_COMPARISON.md): independent atlas
  reconstruction, formal-data checks, grid-model bijection and an attributed
  shorter registration argument; [source audit](CHAIR44_FORMAL_SOURCE_AUDIT.md).
- [Chair44 companion replay](CHAIR44_COMPANION_REPLAY.md): independent
  reconstruction of off-grid candidates and all 299,975 collision boxes;
  [pinned build reproduction](CHAIR44_BUILD_REPRODUCTION.md) tracks compilation
  and a fresh axiom audit separately.
- [Draft inquiry](INQUIRY_GOODMAN_STRAUSS.md): proposed recipient, subject,
  and exact body; the sender must supply their name.
- [Short mathematical brief](BRIEF.md): initial attachment source.
- [Lean recurrence milestone](../../formal/README.md): formal contact semantics,
  exhaustive certificate checking, and the precise normalized-grid scope.
  A [fresh independent agent review](../../formal/INDEPENDENT_REVIEW.md)
  found no material defect and supplies a separate geometric reconstruction.
  This development is separate from the frozen v1 review packet.
- [Geometric grid scrutiny](GEOMETRIC_GRID_SCRUTINY.md): expanded arbitrary-
  placement proof, exact ownership and feature-box checks, and three
  adversarial subagent reviews.
- [Dependency audit](DEPENDENCY_AUDIT.md): where the proof is mathematical,
  what is actually checked, and the most important failure modes to examine.
- [Further scrutiny addendum](SCRUTINY_ADDENDUM.md): subsequent rigidity
  exposition, 2-adic addresses, exact synchronization witness, and conditional
  dynamical/symmetry deductions. **Not included in the frozen v1 package.**
- [Literature follow-up](LITERATURE_FOLLOWUP.md): close precedents for
  coincidence graphs, orientation encoding, chirality, self-simulation,
  exceptional fibers, and three concrete research follow-ups.
- [Direct prior-art audit](DIRECT_PRIOR_ART_AUDIT.md): exact projection onto
  the published eight-color chair code; Fletcher's 3D orientation encoding;
  Hibma's chair-based attempt; older and recent geometric simulations.
- [Goodman-Strauss markings comparison](GOODMAN_STRAUSS_COMPARISON.md):
  exact 26-contact projection, additional pose constraints, attribution of
  the parent mechanism, and the unresolved auxiliary-piece correspondence.
- [Auxiliary reconstruction follow-up](AUXILIARY_RECONSTRUCTION.md):
  an all-radius obstruction to the natural forward map, a symmetry
  obstruction to a rotation-equivariant inverse, and a connected-cross
  source-model discrepancy requiring scrutiny.
- [Preparation record](RECORD.md): actions, sources, and completion status.
- [Agent handoff](../../HANDOFF.md): complete project state and next steps.

Generated outputs: [two-page PDF](../artifacts/review-brief.pdf),
[offline HTML brief](../artifacts/review-brief.html), and
[source archive](../artifacts/review-goodman-strauss-v1.zip).
The ZIP preserves source paths, includes a root `START_HERE.html`, exact
construction data, programs, certificates, and a file-hash manifest.

## Reproduce

From the repository/package root:

```sh
uv run --locked python strong/review/verify_package.py
```

This verifies source hashes when an archive manifest is present, then runs
four primary checks and two controls in a temporary copy. It does not
overwrite the supplied evidence. The scripts execute with the interpreter
selected by `uv`; assertions must remain enabled. An optional JSON report
can be requested with `--report /path/to/report.json`.

To build the documents and archive locally:

```sh
uv run --locked python strong/review/verify_package.py --report strong/artifacts/review_reproduction.json
uv run --locked python strong/review/build_package.py
uv run --locked python strong/review/check_delivery.py
```

Building requires `pandoc` and `pdflatex`; verifying the mathematics does
not. The locked environment may download dependencies on first use.
The HTML brief does not load external assets and uses native MathML.
The optional delivery check also uses `pdfinfo`, `pdftotext`, Node.js,
Playwright, and Firefox. Browser paths can be supplied with
`PLAYWRIGHT_MODULE` and `FIREFOX_PATH`, as in the existing viewer checks.

## Contact provenance

Suggested recipient: **Chaim Goodman-Strauss**,
`chaimgoodmanstrauss@gmail.com`.
This address is explicitly listed on his author-supplied
[Bridges 2025 exhibition profile](https://gallery.bridgesmathart.org/exhibitions/bridges-2025-exhibition-of-mathematical-art/chaim-goodman-strauss),
checked 16 September 2026. His [personal website](https://chaimgoodmanstrauss.com/)
is linked by that profile. The address has not been tested for delivery.

The reason to approach him is the close relation to his earlier
[aperiodic pair construction](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).
Its author preprint is dated 17 February 1998; the published paper is from
1999. Neither the coarse chair nor its eight-child hierarchy is claimed new.

## Sending and response tracking

The instruction received was **“Prepare for Goodman-Strauss.”** It did not
authorize sending. The draft is ready for user review and signature.
If the user later explicitly instructs sending, use the approved sender
identity and preserve the exact final message and attachment hashes in
`RECORD.md`. A reply must be quoted or summarized accurately and attributed;
do not turn an acknowledgment into validation. Until an actual reply exists,
external correctness and novelty assessment remain pending.

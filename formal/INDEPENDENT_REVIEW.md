# Independent review of the first Lean milestone

*16 September 2026. Review of the existing formalization, without implementation changes.*

## Findings

**No material defect found in the stated normalized integer-grid recurrence
milestone.** The final theorem does quantify over every integer offset, retains
the same orientation on both sides, and is supported by exhaustive certificate
checking. This conclusion is about the definitions and scope below; it is not
verification of the full proposed physical monotile or finite-symmetry theorem.

I am a fresh AI reviewer who did **not** author the existing formalization. This
is an independent agent review of that implementation, not an independent human
mathematical review. I inspected the source before relying on reproduction
results and wrote a separate coordinate probe without importing project helpers.

### Informational: the external source bridge remains outside Lean

`generate_input.py:26–43` hashes and parses the frozen JSON, converts rational
port positions exactly, and exports cells, ports and child placements.
`generate_input.py:71–73` checks deterministic equality with `Input.lean`.
These are external Python checks, not Lean theorems about JSON parsing or hashes.
The README acknowledges this at `README.md:57–63`. I found the exporter faithful
to these grid records and independently reconstructed the cached geometry from
the JSON. The curved cap functions, cap depth interpretation and physical solid
are not part of this export or this theorem. This is an acknowledged trust and
scope boundary, not a discovered defect.

### Informational: normalization and iteration remain separate obligations

`Candidate.lean:14–21` fixes the first object at the origin in its identity
frame and rotates the second object. `Recurrence.lean:28–39` proves precisely
the resulting contact equivalence. It does not itself prove covariance under
changing both frames, grouping of arbitrary tilings, common global parity,
existence, or indefinite iteration. `README.md:86–100` states these limitations
correctly. In particular, pairwise even offsets in this normalized theorem do
not already establish the full hierarchy or finite-symmetry conclusion.

## Mathematical and implementation review

All Lean file references below are relative to `formal/Chair/`.

- **The claim is unrestricted and nonvacuous.** The theorem takes
  `(r : Fin 24) (t : V3)` with no hypothesis bounding `t` or assuming evenness
  (`Recurrence.lean:28–39`). `V3` has three `Int` fields (`Model.lean:5–9`).
  Both sides use the same `r`. Certificate soundness, the two count theorems and
  per-orientation distinctness establish 44 distinct oriented contacts at each
  scale (`Recurrence.lean:9–23,46–56`), rather than an empty-language equivalence.
- **The contact predicate is not weakened to one good interface.** It requires
  disjoint occupied cubes, an actual opposing face pair, and fitting at every
  opposing face pair (`Model.lean:82–89`). Every port must find a counterpart in
  both directions, with its position, signed key and both ordered axes checked
  (`Model.lean:56–70`). A distant placement is excluded; one successful face
  cannot conceal another mismatched face. These are grid matching semantics,
  not assertions about curved physical solids.
- **Enumeration is exhaustive without a search radius.** An actual touching
  face gives `a.center2 = b.center2 + 2t`. The integer arithmetic lemma recovers
  `t` exactly, including negative coordinates (`Model.lean:18–23`). The proof
  then places that offset in the generated touching list
  (`Certificate.lean:44–58`). Integer division can generate extraneous offsets
  from other pairs, but the `opposed` test filters them; it cannot lose the
  actual witness. The proof does not assume the generated Python list complete.
- **The checker has a sound rejection path and checks coverage.** Invalid
  indices return false. Overlap witnesses exhibit occupied cubes at the same
  translated position; mismatch witnesses must first exhibit opposed faces
  (`Certificate.lean:12–42`). Every accepted offset is checked in full, every
  rejected offset gets a valid witness, and every touching offset must occur in
  one of those lists (`Certificate.lean:62–86`). Duplicate certificate rows do
  not undermine language soundness; distinctness is checked separately for
  the reported accepted counts.
- **No frame subset is hidden in the proof assembly.** `Geometry.lean:20–31`
  enumerates perpendicular signed coordinate columns and their cross product,
  with length 24 and no duplicates. `Integrity.lean:59–80` checks properness
  and proves coverage of those completed coordinate frames. `Checked.lean:65–68`
  and `124–127` assemble all 24 cases; their terminal `Fin.elim0` leaves no
  remaining case. I independently generated proper signed permutation matrices
  using permutations, signs and determinant, and obtained exactly the same set.
- **The macro object is the actual decorated child boundary in this model.**
  `Candidate.lean:6–12` reconstructs from the frozen cells, ports and children.
  `Integrity.lean:19–55` checks assignment, counts, distinctness, doubled support
  and child frames; `67–70` checks every distinct child pair. The full face
  records, including ports, agree with the uncancelled child boundary
  (`Integrity.lean:82–99`). Thus the macro check has not silently discarded a
  troublesome outer interface. My independent geometric probe recovered all
  24 fine faces, all 96 macro faces and cancellation of 48 internal face pairs.
- **Caches and proposed witnesses are not axioms.**
  `Cache.lean:132–133` proves equality of caches with reconstructed objects.
  Every batch checks its actual certificate after rewriting by these
  equalities, using `decide +kernel`; the four batches cover indices 0–23.
  `generate_certificates.py:175–206` generates this complete assembly.
  The source scan found no `sorry`, custom axiom, `native_decide`, `extern`,
  `unsafe`, or `implemented_by` declaration in the project Lean modules.

## Checks actually run

Commands were run from the repository root, using the pinned Lean 4.34.0
distribution. No source certificates, frozen data or verification report were
regenerated or modified during this review.

```sh
uv run --locked python formal/verify.py --lake /tmp/lean-4.34.0-linux/bin/lake
uv run --locked python /tmp/independent_chair_review.py
/tmp/lean-4.34.0-linux/bin/lake -d formal env lean /tmp/IndependentChairAudit.lean
sha256sum /tmp/independent_chair_review.py /tmp/IndependentChairAudit.lean
```

1. **Existing verifier: passed.** Deterministic input and certificate checks
   passed; the incremental Lean build completed successfully (18 jobs); the
   final theorem and all eight declarations in `Audit.lean` passed the axiom
   audit; all 44 fine contacts matched the existing coordinate certificate.
   This reused `.lake/` artifacts and was **not** a cold rebuild. The saved
   `verification.json` was inspected but was not treated as proof by itself.
2. **Fresh independent coordinate probe: passed.** The probe reads frozen JSON
   directly. It assigns ports by geometric containment in face interiors,
   transforms each cube by all eight corners, cancels internal child faces
   while checking their complete port data, and compares the resulting complete
   face records with the literal Lean caches. It constructs all proper signed
   permutations independently. For contact enumeration it derives offsets
   from adjacency of occupied cubes, rather than copying the generator's
   face-center enumeration. It checks every coincident interface and compares
   exact accepted sets by matrix with `certificate_summary.json`.

   | Quantity across all 24 orientations | Fine | Macro |
   |---|---:|---:|
   | Offsets with opposing faces, including overlaps | 1,410 | 9,033 |
   | Disjoint geometric face contacts | 1,194 | 6,801 |
   | Accepted decorated contacts | 44 | 44 |

   The macro accepted set was exactly twice the fine accepted set for each
   individual matrix. The probe imports only Python standard-library modules.
   This check supplements, and does not replace, the Lean completeness proof.
3. **Expanded axiom audit: passed.** In addition to `Audit.lean`, I printed
   dependencies of certificate soundness, touching enumeration completeness,
   rejection soundness, both cache equalities, doubled support, rotation
   properness/completeness, assigned-port distinctness, child-frame membership,
   and both assembled certificate theorems. No dependency outside `propext`,
   `Classical.choice` and `Quot.sound` appeared. Both cache equalities had no
   axiom dependencies; the two assembled certificate theorems used `propext`.

The coordinating agent preserved the Python probe unchanged as
[`independent_review_probe.py`](independent_review_probe.py) and reran it
successfully, saving [`independent_review_results.json`](independent_review_results.json).
Its durable reproduction command is:

```sh
uv run --locked python formal/independent_review_probe.py
```

Probe SHA-256 (the preserved Python file has the same hash):

```text
8eff4bea7187115c0773b3fcf7371eb628eb5cd0ec0ef73e222006b508297979  /tmp/independent_chair_review.py
7832a2c5242de3a315344ff650c1f97a2de26ce89b0f3c6c0505701f966f01bb  /tmp/IndependentChairAudit.lean
```

The supplemental Lean audit file contains the following; save it under `/tmp`
and use the command above to reproduce without changing the Lean source set:

```lean
import Chair
#print axioms Chair.certificate_contact_iff_mem
#print axioms Chair.contact_mem_touchingCandidates
#print axioms Chair.rejectCheck_sound
#print axioms Chair.fine_eq_cached
#print axioms Chair.macro_eq_cached
#print axioms Chair.macro_cells_exactly_doubled
#print axioms Chair.rotation_frames_proper
#print axioms Chair.completed_coordinate_frame_mem_rotations
#print axioms Chair.fine_assigned_ports_distinct
#print axioms Chair.child_frames_are_rotations
#print axioms Chair.fine_certificates
#print axioms Chair.macro_certificates
```

I changed only this review file in the repository; the coordinating agent
preserved the separate probe and its result.

## Review limits and disposition

No implementation fix is requested by this review. The normalized grid
recurrence milestone is supported by the inspected proof structure, successful
incremental reproduction, expanded axiom audit and independent coordinate
checks. Trust still includes Lean's kernel and toolchain, the external
JSON-to-literal bridge, and the mathematical interpretation of the grid model.
I did not independently recheck every compiled proof from a clean cache,
audit Lean's implementation, or formalize the physical interpretation.

The proper next claim remains **normalized integer-grid contact recurrence**.
Unique parent grouping, frame covariance, global parity and iteration,
existence, arbitrary Euclidean grid enforcement, reflections, and the full
finite-symmetry theorem require their own arguments and verification.

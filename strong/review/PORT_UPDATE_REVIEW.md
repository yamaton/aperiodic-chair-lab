# Independent AI review of the port, tutorial and rendering changes

*19 September 2026. Requested by the user; local working-tree review.*

Five separate reviewer agents examined the changes without inheriting the
authoring conversation. They read repository guidance and source, re-derived
the relevant arguments, and ran their own read-only checks. The coordinator
reviewed their findings and made the corrections below. This is independent
AI review within the same project, not external human acceptance, a new Lean
proof, or validation of manufactured blocks.

**Outcome:** no P1/P2 correctness defect was identified in the reviewed
changes. Three P3 issues were found and corrected. The reviewers responsible
for those findings independently confirmed the corrections. No finding
remains open within the assigned scopes; the research limitations remain.

## Scope and division of work

The [baseline manifest](port-update-review/baseline.json) records HEAD and
SHA-256 values for the 73 changed/new files present when review began. The
review covers the port simplification/dimension work, its information-transfer
foundations, tutorial and rendering updates, and the rule-lab changes still
in the same working tree. It does not re-review all historical research.

| Reviewer | Assigned scope | Independent work and result |
|---|---|---|
| `review_geometry` | Cubic port rigidity, movable dimensions, packing, registration and atlas transfer | Re-derived the all-isometries and geometric arguments; Python and standalone JS checks passed. Independently checked 18,432 actual transformed-triangle memberships and 112 mixed-depth slot pairs. One audit-accuracy finding, corrected. [Full report](port-update-review/geometry.md) |
| `review_information` | Constraint balance, five forbidden equality patterns, recoding and aligned recurrence | Re-derived ranks, signed-volume identity, binary counts and fixed-point scope. Three replay outputs matched the preserved JSON. No actionable finding. [Full report](port-update-review/information.md) |
| `review_rulelab` | Interactive constraint/depth lab, data/model, localization and integration | Reconstructed 1,194 geometric contacts independently and compared 916,992 decisions across 384 mixed-sign assignments. Existing tests and extra native-keyboard/modal probes passed. No actionable finding. [Full report](port-update-review/rulelab.md) |
| `review_tutorial` | Full tutorial diff, exercises, units, figures, proof scopes, offline presentation and provenance | Rebuilt identical HTML; verified desktop/mobile/no-JavaScript reading, all figure controls, local destinations and receipt hashes. Two presentation findings, corrected. [Full report](port-update-review/tutorial.md) |
| `review_rendering` | Actual exported geometry, flat/cap coverage, contacts, crop orientation, image framing and receipts | Rebuilt meshes and independently checked actual coordinates, face coverage, all 384 internal vertex-set correspondences, proper crop transforms and camera bounds. Earlier triangular variant and preserved images checked. No actionable finding. [Full report](port-update-review/rendering.md) |

## Findings and corrections

Line references in the raw reviews identify the pre-correction files.

| Finding | Correction | Follow-up |
|---|---|---|
| P3: `frame_audit` called 9,216 covariance/orthogonality checks “template memberships” without comparing actual triangle templates | Passed width explicitly; generated the eight ordered 2D templates independently for each offset pair; checked all signed axes, face-center integer/half-integer coordinates, transformed vertex planes, and actual projected triangle membership | Geometry reviewer reran both updated witnesses: 9,216 actual memberships each, unchanged recorded results and hashes; no new issue |
| P3: tutorial Figure 11's “Cover” marker and opening could be mistaken for the current relocated cover | Opening now identifies Figure 1 as the square reference; Figure 11 explicitly links and distinguishes the earlier enlarged triangular cover from the current relocated cover | Tutorial reviewer confirmed the source corrections; coordinator rebuilt and checked the final HTML |
| P3: README's “Inspect the candidate” linked to the earlier square-port viewer without labeling it | Renamed the row “Inspect the square-port reference” | Tutorial reviewer confirmed the distinction |

The membership correction strengthens the checker without changing the
candidate, dimensions, finite results or evidence schema. The regenerated
`port_dimensions.json` is byte-for-byte unchanged, so the current cover's
input hash and rendering provenance remain valid. The comparison figure
was not regenerated because its geometry and data did not change. Both
frozen mathematical snapshots and all cover images remain unchanged.

## Final validation and evidence

The coordinator reran the complete exact dimension calculation with only
figure output disabled, compared its JSON byte for byte, regenerated the
standalone tutorial using the documented Pandoc command, and reran its
Firefox presentation check and local Pages build. The refreshed
[tutorial receipt](../../docs/tutorial_verification.json) describes the final
artifact. Final commands and hashes are summarized in
[the coordinator receipt](port-update-review/final-checks.json).

The raw reports are preserved verbatim, including their follow-up replies
and explicit limits. [The archive manifest](port-update-review/manifest.json)
hashes those reports, the baseline, and four additional reviewer probes.
Those probes are historical review aids, not new production entry points:
they run from the repository root, use the documented local Firefox setup
and `/tmp` output paths, and describe the baseline reviewed here. The rendering
probe may reuse its temporary mesh directory; a fresh independent repetition
should use an empty output directory. Its original reviewed run built fresh
meshes. The tutorial probe expects the baseline link count and writes its
own temporary results; use the maintained `docs/verify_tutorial.cjs` for the
updated artifact. Python probes require `uv run --locked python`.

No script or finite patch test establishes an arbitrary-placement theorem
by itself. The reviewers did not certify a mesh as aperiodic, evaluate
manufacturing tolerances, conduct a student or screen-reader trial, prove
optimality over arbitrary port shapes/placements, or obtain human expert
review. No commit, publication or outreach was performed.

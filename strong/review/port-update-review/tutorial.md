# Independent tutorial/documentation review

Read-only review of the current working-tree tutorial changes, including the complete Markdown diff, generated HTML correspondence, figure generator/checker changes, current proof-status/index/readme changes, receipt, PORT_SIMPLIFICATION.md, PORT_DIMENSIONS.md and relevant INFORMATION_TRANSFER.md passages. Read AGENTS.md and the current HANDOFF.md status before assessing the claims.

No mathematical or rendering blocker found in this scope. Two low-priority presentation consistency findings remain:

1. **P3 — Name the earlier cover in Figure 11's caption.** `docs/APERIODIC_CHAIR_TUTORIAL.md:1473` calls the plot's old `(w,h)=(3/64,1/32)` marker “the cover” / “the separately enlarged illustration.” README now shows the relocated `(3/16,1/8)` witness at actual design proportions. The dimension-study generator still emits the bare label `Cover` (`strong/audit/investigate_port_dimensions.py:220`). The new cover notes explicitly explain that this marker belongs to the earlier triangular cover (`docs/figures/aperiodic-chair-cover-relocated.md:41`), but a tutorial reader is not given that explanation/link. Label it “Earlier triangular cover,” and distinguish/link the current cover in the caption. The tutorial opening's “existing whole-chair renderings still show that earlier [square] design” (`:52`) should likewise be narrowed to Figure 1 to avoid contradicting the current README rendering. Reproduced by comparing Figure 11, README hero/caption, and the current cover notes.

2. **P3 — Label README's viewer as the square reference.** `README.md:41` still invites readers to “Inspect the candidate” through the unchanged square-port viewer, immediately below the new relocated-triangle hero. Tutorial further reading correctly identifies this same viewer as the earlier square reference (`docs/APERIODIC_CHAIR_TUTORIAL.md:1661`). Carry that distinction into the README row so the reader does not mistake the viewer's surface or dimensions for the current hero candidate. Reproduced by following the repository viewer link and comparing its reference with the tutorial's explicit label.

## Mathematical and pedagogical assessment

- The triangular barycentric weights, normalized cubic, centroid, maximum height, unequal side lengths, and anchor distinction are consistent. The polynomial divisibility/equal-total-degree argument and three-line classification recover the metric frame without illegitimate anisotropic metric assumptions.
- Step C's common-offset cancellation, optional per-depth offsets, integral registration and handedness determinant equation are consistent with the stated hypotheses.
- Step E states both necessary inequalities for this sufficient clamping argument and uses correct values for the recorded and relocated examples. No accidental reuse of rho=1/64 for h=1/8 found.
- Section 10's leg/depth/scale table and Exercises 5/13/14/19 with their solutions are correct. The distinction between physical unit length and coordinate offsets is explicit. The old square-cap bound and triangular area ratio are correctly restricted to equal w.
- The width supremum 1/4 is restricted to the stated D4/right-triangle placement family, and the depth/zone bounds are explicitly sufficient rather than globally necessary or manufacturing limits. The perpendicular-zone inequality reasoning is valid.
- The information-transfer words and aligned fixed-point discussion agree with their linked report and preserve the distinction between aligned tests, complete macro tests and grouping proof.
- Proof-status and review-history additions appropriately distinguish frozen grid/Lean results, new written geometry, finite checks and the earlier square-edition AI review. No new human or formal geometric review is implied.

## Checks actually run

- All 18 SHA-256 entries in `docs/tutorial_verification.json` independently recomputed: zero mismatches.
- Documented Pandoc command rebuilt HTML into `/tmp/aperiodic-independent-tutorial-rebuilt.html`: zero warnings; `cmp` found byte-for-byte equality with `docs/APERIODIC_CHAIR_TUTORIAL.html`. This also checks embedded images/formulas/styles against the current source build without changing repo artifacts.
- Independent Playwright/Firefox 155.0 script `/tmp/aperiodic-independent-tutorial.cjs` run with offline mode at widths 1200 and 390: 11 loaded embedded figures, 732 MathML nodes, 56 local link destinations present, tutorial fragment IDs valid, no page overflow, no HTTP(S) requests or JS page errors. All 11 figure controls activated by keyboard and restored focus after Escape at both widths.
- JavaScript-disabled offline mobile reading: all 11 images loaded, 732 MathML nodes, no overflow.
- Visually inspected independent screenshots of the mobile dimension table, mobile Section 10 introduction, and enlarged desktop Figures 7 and 11. Numeric columns and formulas are readable; enlargement intentionally scrolls Figure 11 horizontally.
- Results: `/tmp/aperiodic-independent-tutorial-result.json`. Screenshots: `/tmp/aperiodic-independent-{table,dimensions}-{1200,390}.png` and `/tmp/aperiodic-independent-enlarged-{7,11}-{1200,390}.png`.

## Limits

No source, snapshot, receipt, or generated repository file was modified. This review did not rerun geometry atlases, Lean, mesh checks, external web citations or deployed-site checks; those are outside this assigned documentation/presentation scope. The independent browser script checks tutorial fragment IDs and all linked file existence, not Markdown target-heading slugs. It is an internal AI review, not a human student trial or external mathematical acceptance.

## Follow-up on coordinator's fixes

Independently reread the changed Markdown and README. Both P3 findings are addressed: the opening now limits the square-rendering description to Figure 1, Figure 11 identifies and links both the current relocated cover and the earlier 3x/64x triangular cover represented by the historical marker, and README now labels its viewer row “Inspect the square-port reference.” The marker can remain unchanged because its historical meaning is now explicit. HTML rebuild and receipt refresh after these text edits are being handled by the coordinator; the original browser/hash results above describe the pre-fix artifact.

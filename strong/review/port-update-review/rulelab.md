# Rule-lab independent review

Scope: current working-tree additions/changes in docs/assembly/rule-{lab,model,data}*, build_rule_data.py, verify-rule-lab.cjs, build-assembly.cjs, assembly app/page/locales integration, assembly.html and the corresponding README scope statements. Read AGENTS.md and current HANDOFF.md. No repository files or receipts changed.

## Findings

No actionable correctness/regression finding identified within this scope.

The graph's component-count freedom calculation is valid for these exported graphs: an independent signed traversal found no odd-cycle inconsistency, and the component count equals the number of independent families. This is a restricted-data result; the generic freedom helper would not model an arbitrary inconsistent signed graph, which the UI does not supply.

The depth-preservation indicator compares both complete Boolean contact sets against the profile baseline; the coarse-graining indicator compares fine and parent sets, not merely their cardinalities. Profile/preset resets clear stale parent reveal state and recreate the family controls where needed. Current UI and README scope restrict the comparison to the 1,194 aligned proper-grid contacts, exclude arbitrary edited odd offsets/recognizability/infinite tilability, and restrict uniqueness to the recorded template classes.

## Checks actually run

- `uv run --locked python docs/assembly/build_rule_data.py --check`: passed.
- In-memory `require('./docs/build-assembly.cjs')()` comparison with existing docs/assembly.html: exact equality, no output file written.
- Existing verify-rule-lab.cjs compiled via a /tmp wrapper with its JSON receipt path replaced by /tmp/aperiodic-review-rule-verification.json: passed 14,328 raw-coordinate decisions, all graph families, nine language/width combinations, offline operation, history isolation, Ctrl+Z shielding, Escape, focus return and the #rules deep link. Original repository receipt not written.
- /tmp/aperiodic-rule-independent.cjs: independently enumerated geometric contacts from the frozen seven carrier cubes and 24 rotation matrices, recovering the full 1,194 pose set. Independently reconstructed port transformations and parent boundaries from raw frozen coordinates without ChairEngine. Checked each internal port pair has opposite normals and opposite profile labels; all external pairs align the ordered tangent frames. Compared all fine/parent decisions for 128 random mixed-sign assignments in each of three profiles (384 assignments; 916,992 decisions). All matched rule-model.js. Independently traversed exported graphs with alternating signs and checked the number of free signed components. Passed.
- /tmp/aperiodic-rule-probe.cjs in offline Firefox at 390×700: fifty native Tab presses remained within the modal; native Home/End/ArrowRight edits worked with negative depths; native keyboard family selection preserved focus and updated the selected depth; close/reopen retained lab state; profile 0 graph reached 48→1 freedom; six-depth preset safely switched four-family profile 0 back to twelve-family profile 1. No page errors.

## Limits

Firefox only; no screen-reader testing or complete accessibility audit. The browser suite's generated screenshots were not visually inspected in this review. Random assignments supplement, rather than establish an exhaustive classification over all depth recodings. Tests concern recorded proper aligned-grid contacts and graph equations, not arbitrary Euclidean placement, physical nonintersection after arbitrary parameter edits, recognizability, infinite tilability, or human validation of the mathematical construction. The full research synthesis/uniqueness classification was not rerun.

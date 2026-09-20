# Constraint balance and information transfer review

Result: no actionable correctness or proof-scope finding in the assigned files.

Reviewed `strong/CONSTRAINT_BALANCE.md`, `strong/INFORMATION_TRANSFER.md`, the three named audit implementations and saved JSON, relevant `verify_from_coordinates.py` helpers, frozen candidate geometry, and synthesis/UI selected-edge inputs. Read project guidance and the relevant current handoff entries. No project files or saved evidence were mutated.

## Reproduction

Executed both Python main functions under `uv run --locked python` with `Path.write_text` redirected to `/tmp/aperiodic-review-information/`, and executed the standalone Node checker with its sole `writeFileSync` redirected there. All assertions passed. Each regenerated JSON was structurally identical to the corresponding saved report.

- Constraint balance: 1,194 proper geometric contacts; 7,740 universal port-pair edges; no chirality or frame mismatch. Universal rank 191/nullity 1. Selected ranks/nullities are 188/4, 180/12, 180/12. Successful graph has twelve 16-vertex, 31-edge components and 192 row dependencies.
- Information transfer: 1,194 fine and 6,801 full macro contacts; 19 and 21 distinct predicates; five identical minimal forbidden patterns. Binary preserving partitions: 1,224/2,048.
- Standalone JS replay: 9,189 symbolic predicates, including 1,194 actual 64-child aligned second-level predicates, and 13,312 opposite-key cap maps. Reference/two-depth allowed sets agree; no odd allowed macro offsets. All cap maps proper and integral.

## Independent mathematical checks

The 3/1 offset determines ordered tangent axes on a registered common face. Reversed normals and proper rotations therefore reverse chi. Switching x_i by chi_i gives the ordinary equality graph, proving nullity/components and row dependencies without relying on floating rank. Equal bipartition sizes are separately checked, and exact integration gives signed cap volume x_i/9437184, agreeing with the report.

The bounded fine and full macro enumerations are complete for positive-area registered contacts: base carriers lie in [-1,1]^3, macro carriers in [-2,2]^3, so the respective coordinate shift bounds +/-2 and +/-4 suffice. The primary implementation independently derives these bounds from cubes (`analyze_information_transfer.py:55`).

Partition implication/minimal-antichain direction is correct (`analyze_information_transfer.py:49`); unconditional predicates have precisely the original 44 poses, and each forbidden minimum has a contact witness. Thus the iff is symbolic over all real amplitude values, not an inference from binary sampling (`INFORMATION_TRANSFER.md:62`).

Independently recomputed binary combinatorics: among first-eight 2-color assignments, inclusion-exclusion intersection sums for the four bad matchings are 64,20,10,2, giving 256-64+20-10+2=204 valid assignments. Last-four validity is 16-4=12, giving 204*12/2=1224 modulo color exchange. Aligned-only count is (256-16)*16/2=1920. Two high entries, one per group, break every bad pattern. A single positive amplitude satisfies all bad patterns, so the stated restricted two-value minimality is valid.

The scale operator checks are equality of canonical partitions, not just counts or witness checks (`analyze_information_transfer.py:108`). Direct macro boundaries agree with T(F0), and T(F1)=F1 on the entire aligned domain. Self-similarity of the prescribed carrier partition justifies iterating the same dependency operator. JS reconstructs actual second-level boundaries (`crosscheck_information_transfer.cjs:68`).

## Scope and limitations

The all-real classification is an abstract proper-grid interface equation statement; it does not certify arbitrary large/zero physical cap designs. The report explicitly presents it as symbolic and separately excludes zero physical caps. Full macro checks cover integer offsets at the first grouping; higher-level fixed-point claims cover aligned fixed-template supertiles, as expressly stated at `INFORMATION_TRANSFER.md:157`. The replay's second-level pose domain is sourced from the first-level aligned table, but completeness follows from the same scaled carrier geometry and the primary set-domain identity; no unsupported full higher-level odd-offset census is claimed.

No arbitrary-Euclidean analytic audit, recognizability proof for edited/111-contact rules, Lean recoding theorem, or fabricated-solid certification was performed or inferred. Those limitations are stated in the reviewed report. This review did not rerun the original 6,561-template search or audit unrelated older theorem claims.

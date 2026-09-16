# Provenance, AI assistance and interpretation

## What the project is

Aperiodic Chair Lab records an exploration of three-dimensional matching
rules, formal proofs in a discrete model, comparisons with published work,
and explanations aimed at students and physical experimentation. The human
maintainer uses the GitHub handle **yamaton**. No academic affiliation or
external endorsement is asserted.

The project was developed with substantial AI assistance. AI agents wrote
and revised search code, geometric arguments, Lean proofs, literature notes,
verification scripts, visualizations and documentation. The human maintainer
set directions, supplied questions and sources, and reviewed the work.
Git authorship does not imply that every line was written manually.

## What “independent” means here

- A separate implementation reconstructs data or checks a claim without
  importing the original implementation, within its stated scope.
- An independent agent review uses an AI agent without authorship of the
  particular change. It is not independent human mathematical review;
  agents can share training, assumptions and failure modes.
- A reproduced Lean build checks a formal statement under the recorded
  axioms and computational trust assumptions. It does not automatically
  validate the correspondence between that statement and informal prose.

The checks are useful evidence, with different limitations. Each report
states which of these activities actually occurred. No outside expert has
reviewed or endorsed this project. The Goodman-Strauss inquiry is an unsent
historical draft, not correspondence received from him.

## Relation to earlier and overlapping work

The chair hierarchy and recognition mechanism have predecessors in
Goodman-Strauss's 1999 construction. Earlier investigations in this repository
also reproduce the known SCD construction, which allows screw symmetry.
The [third-party notices](../THIRD_PARTY_NOTICES.md) identify these sources.

The exact [Chair44 comparison](../strong/review/TSIOKOS_CHAIR44_COMPARISON.md)
identifies the same discrete decorated-chair system in Tsiokos's public
release after coordinate conversion and key relabelling. The surfaces differ:
square pyramids in Chair44 and asymmetric curved caps here. That difference
does not establish a distinct discovery of the matching system.

Our contributions are best assessed as checks, formalization of the grid
argument, exposition, and investigation of another geometric realization.
Novel printable interfaces and physical behavior remain future work.

## What the dates establish

The project's notes and frozen manifest contain dates from 15–16 September
2026. Its first Git commit, `ba4b070`, is an accumulated workspace snapshot,
not a commit-by-commit reconstruction of the earlier exploration.

The saved Zenodo records timestamp Chair44 v1 at
`2026-09-15T23:30:43.260897+00:00` and v2 at
`2026-09-16T09:36:26.413556+00:00`. The exact-comparison report separates these
public deposit times from the release's own earlier development claims.

These records identify artifacts and recorded chronology. They do not
establish private discovery priority, independent invention, or copying
between projects. We make none of those claims. Subsequent public availability
of this repository would not retroactively establish an earlier publication.

## How to read the archive

Start with the current README and comparison reports. The
[historical-material guide](HISTORICAL_MATERIAL.md) identifies superseded
proposals and review packets. Old statements such as “no duplicate identified”
describe the search at that stage, not our current assessment.

Frozen inputs, negative controls, failed searches and exact logs are retained
so later readers can inspect changes in the reasoning. Corrections go into
new reports or clearly marked updates rather than silently rewriting the
evidence. A smaller or clearer proof can be valuable without a novelty claim.

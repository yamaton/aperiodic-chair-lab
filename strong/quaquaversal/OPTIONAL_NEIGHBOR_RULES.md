# Optional neighbors, pilot branches and verified choice cuts

This continues [PARENT_PROPAGATION.md](PARENT_PROPAGATION.md). Recursive
parent legality remains unproved. This checkpoint ends at **246** unresolved
parent covers; its six-case pilots reject assignments or branches, not whole
parent cases. Subsequent [fine and coarse propagation](COARSE_PARENT_RULES.md)
reduces the full frontier to **177**. [Layered choice proofs](DOMAIN_CERTIFICATES.md)
also add a 163rd verified cut.

## Main continuation: 350 to 246

A forced layer from `expanded_arc_seed.json` rejects 35 of 350 cases and
leaves 315. The full explicit-set audit checks 29,145,299 domain
intersections and 3,801,491 distinct placements, including every retained
domain. Expanded arc consistency then rejects 69 of the 315, leaving 246.
Its 512,877 reductions and 185,698 distinct used geometric edges are
independently replayed. There are 47,234,830 directed edge occurrences
across these finite patches.

`expanded_arcs_2_seed.json` is this stage's baseline continuation seed. It retains
128,780 shared positions, the narrowed domain pool and the 246 live cases.
These position counts include older cases and are not patch tile counts.

## Q017: a binary-branch pilot that added no parent exclusions

Select six of the earlier 350 cases. For each, take a nearest-to-parent-center
tile with exactly two possible stars and test both choices. The 12 branches
are an exhaustive split of those six selected domains, not a search of all
350 cases. A new forced layer rejects two branches, but both belong to the
same parent already rejected by the unbranched layer. Arc consistency on
the original branched patches rejects none of the 12 branches.

The seed, both experiments and audits are retained under `branch_probe_*`.
`audit_branch_probe.py` verifies the exact partition of each original domain
and reports zero additional parent exclusions. This failed strengthening is
preserved; it is not evidence that all branching strategies fail.

## Q018: simultaneous neighbor-presence choices

The next pilot uses six live cases from the 246-case seed. Each existing
center chooses exactly one star in its domain. All centers predicting the
same neighbor pose must agree whether that tile is present, even when the
centers themselves do not touch. Already forced positions must be present.
These are finite necessary constraints, encoded in Z3 with explicit timeouts.
Only six pilot cases were tested.

All six instances are satisfiable. Selected assignments are preserved in
`neighbor_incidence_sat.json`; the producer replays all incidence equalities
and exactly-one choices on each model. This does **not** prove geometric or
infinite extension: optional neighbors have no complete stars assigned yet,
and conflicts between distinct optional supports are initially omitted.

Reconstructing the actual selected supports exposes a forbidden pair in
each of the six assignments. An independent audit finds a selected-star
sponsor for each offending support and checks the common-point/atlas-absence
witness. Three witnesses are point-only contacts, one is a face contact,
and two have positive-volume overlap. These invalidate six particular
assignments; other assignments for the same parent cases remain possible.

## Q019: sampled interior non-overlap is still insufficient

To improve the SAT relaxation, sample the centroid and six centroid-to-vertex
midpoints of every potential prism. All seven are strictly interior points.
If another potential prism contains one of them in its interior, the two
supports cannot coexist. On the shared 33,601-position pilot catalog, this
gives 209,371 pair exclusions. The producer uses exact scaled integers;
an independent Fraction audit checks all 209,371 common-interior witnesses,
using 125,375 distinct sample points.

The six SAT instances remain satisfiable after adding the applicable sampled
overlap clauses. The applicable clause counts are 4,793; 5,372; 4,254;
10,682; 3,010; and 3,367. Samples only detect some overlaps and do not detect
all forbidden point/edge/face contacts. The new models therefore remain
finite assignments, not tilings. No timeout or unsatisfiable instance occurs
in this pilot.

## Q020: optional neighbors need complete stars

Freeze each Q019 model's selected stars at its existing centers, then run
one forced-neighbor extension. All six assignments now give an empty domain
at some required neighbor. This reveals a condition omitted from presence
and sampled-overlap constraints: a present optional tile must itself admit
a complete allowed star compatible with every center that requires it.

`audit_incidence_star_cuts.py` verifies exact neighbor placements and the
compatibility-set intersections. Greedily deleting unnecessary premises
reduces each contradiction to **two center-star choices**. It does not
assert global minimum clause size. The six verified cuts are stored in
`incidence_star_cuts.json` as forbidden conjunctions of `(tile, star)` pairs,
with their target pose and the empty-intersection witnesses.

Each cut is necessary for an actual admitted tiling: its selected centers
force the target tile, while the two prescribed center stars leave that tile
no possible complete star. None of these six cuts has both antecedents
already fixed in the original parent-domain problem. Thus they reject the
six model assignments, with **zero direct parent exclusions** at this stage.

## Q021: necessary cuts change the models but do not exclude the cases

`neighbor_star_cut_sat.py` adds the six audited Q020 cuts to the same six
Q019 pilot problems. Each satisfying assignment is checked for a nonempty
complete-star domain at every tile it requires. An empty intersection gives
a necessary forbidden conjunction of selected center stars; those cuts are
added before asking for another assignment. A cut is applied in another
case only when its fixed center IDs and selected star values are present.

This adds **117 cuts**, all of length two, giving 123 including Q020.
`audit_neighbor_star_cuts.py` independently checks the 234 rational neighbor
placements and the empty intersections using explicit sets. None of the
new cuts excludes its source parent without additional choices. All six
cases eventually pass the immediate complete-neighbor-star test, after
4, 5, 3, 2, 2, and 3 SAT calls respectively. No solver timeout, UNSAT, or
16-round cap occurs. These are finite assignments, not tilings: compatible
stars at different optional neighbors have not yet been chosen jointly.

The first implementation stopped on an assertion because the same newly
found cut could be discovered at several neighbors in one model. It wrongly
treated a cut discovered earlier in that model as already installed in the
solver. `neighbor_star_cut_initial.py` and
`neighbor_star_cut_initial_failure.json` preserve this implementation failure.
The repaired producer distinguishes previously installed cuts from newly
discovered duplicates. This was not a mathematical contradiction.

The final selected stars are frozen in `neighbor_star_cut_seed.json` for
deeper extension. The first forced layer has six survivors. A dedicated
snapshot, `audit_forced_domains_complete.py`, handles a missing zero-count
category in the producer's status dictionary; the original audit source is
preserved because older artifacts bind its hash.

## Q022: compatibility between optional neighbors gives stronger cuts

The first forced layer is independently checked in full: 979,677 domain
intersections and 661,624 distinct exact placements, with all six assignments
surviving. Expanded arc consistency on those patches then rejects **five
assignments**, leaving one. Its 2,829 logged reductions and 2,799 distinct
used edges are independently replayed. These are assignment counts, not
reductions of the 246-case parent frontier.

`audit_neighbor_arc_cuts.py` traces each empty domain backward through the
recorded reductions. It reconstructs the relevant initial domains from the
original selected center stars, then deletes unnecessary choice premises.
Crucially, after deleting a premise, every tile used in the proof must still
be forced present by at least one remaining premise. A domain calculation
at an unforced optional position would not justify a cut.

The five resulting cuts have lengths **3, 3, 3, 5, and 2**. Their certificates
use 3, 2, 2, 12, and 2 arc steps, respectively. Each contains its selected
center-star hypotheses, geometric neighbor requirements, and the reduction
trace leading to an empty domain. `verify_neighbor_arc_cut_certificate.py`
checks these certificates separately from the extraction search, using
Fraction geometry and explicit sets. None has all hypotheses fixed in the
original parent problem: direct parent exclusions remain zero.

The single surviving frozen assignment is model 5, original full-frontier
`source_index=6`, parent key `(boundary_index=515, cover_index=0)`. Surviving
arc consistency does not assert a consistent joint star assignment, still
less infinite extension. Its narrowed domains are in
`neighbor_star_cut_arcs.json`, using the pose table in
`neighbor_star_cut_layer_1.json`.

That remaining frozen assignment has now also failed: another forced layer
survives, but the subsequent arc run rejects it after 38 reductions. All
292,009 forced intersections/placements and all 38 arc steps have independent
audits. `neighbor_star_cut_layer_2.json` and `neighbor_star_cut_arcs_2.json`
preserve the extension and failure. Q026 has now lifted this failure through
both layers to an eight-choice certificate; see [the proof and audit](DOMAIN_CERTIFICATES.md).

## Q023: integrate optional-neighbor arcs into SAT refinement

`neighbor_arc_cut_sat.py` starts with the 123 Q021 and five Q022 cuts.
`neighbor_arc_oracle.py` applies necessary arc consistency after the immediate
complete-star test passes. An empty domain yields a backward-sliced proof;
choice deletion is allowed only while every proof tile remains forced.
Round limits and solver timeouts remain unknown, and UNSAT would still await
certificate audit. This run has none of those outcomes.

The six cases pass after **3, 4, 2, 4, 12, and 1** SAT calls. There are
**34 new cuts**: 20 immediate-neighbor contradictions and 14 arc-derived
contradictions. Including inherited cuts there are 162: 155 of length two,
three of length three, one of length four, and three of length five.
`audit_neighbor_arc_sat.py` independently verifies every new certificate
with explicit sets and rational geometry: 139 placements and 38 arc steps.
Direct parent exclusions remain zero.

The six final assignments are frozen in `neighbor_arc_sat_seed.json`.
A separate generic forced/arc run independently checks 980,036 domain
intersections, 657,809 distinct placements, and 13,606 arc reductions on
11,025 distinct edges. `compare_arc_oracle.py` compares all **45,403** final
domain records against the oracle output; every domain agrees. Thus the
reported finite arc fixed points are checked, but joint star choices at the
optional neighbors and infinite extension remain open.

## Q024: return the learned cuts to the full frontier

The fixed-center cuts also constrain cases outside the six-case SAT pilot.
If all but one antecedent of a forbidden conjunction are already fixed,
the remaining star choice can be removed. An absent center is never silently
assumed present. `choice_cut_domains.py` applies this unit propagation to
all 246 unresolved parent cases, removing **77 star values in 18 cases**.
`audit_choice_cut_domains.py` independently replays every removal, checks all
retained domains, and verifies that no further unit consequence remains.

Only the changed 18 cases are sent to another arc run. They all survive,
with 150 additional reductions on 83 distinct used edges, independently
audited. The updated domains are merged with the 228 unchanged cases in
`choice_cut_frontier_seed.json`, the new full frontier. It has the same
128,780-position pose table and still **246 unresolved parent cases**.
The merge checks domain containment and the current audit hashes; it is not
an additional search or proof of infinite extension.

## Next attempt

The Q021 implementation now adds the verified center-choice cuts to Q019. For a cut
`[(i,s),(j,t)]`, forbid choosing star `s` at center `i` together with star `t`
at center `j`. Apply a cut only when its fixed geometric center IDs refer to
the same pose table; if a center is absent from a pilot problem, do not
silently assert that it exists. A star unavailable in a center's domain makes
that conjunction impossible already.

Continue forced-neighbor/arc propagation from `choice_cut_frontier_seed.json`,
including another unit-cut pass if arc propagation has fixed new premises.
For the SAT route, extend the six Q023 finite assignments and lift deeper
failures through both forced and arc operations into original-choice
certificates. The existing arc-only certificate cannot silently treat
derived domains or optional tile presence as unconditional. Preserve limits
and timeouts as unknown.
An unsatisfiable parent instance will require an appropriately checked solver
certificate or an independently replayable exhaustive argument; do not infer
it merely because several sampled assignments fail.

The original Q018 and Q019 producers remain separate, source-bound experiment
snapshots. Prefer a new cut-enabled producer rather than silently changing
the meaning of their retained artifacts. The six-case pilot is not the whole
246-case frontier. The current full frontier is `choice_cut_frontier_seed.json`;
`expanded_arcs_2_seed.json` remains the original Q018–Q023 SAT input snapshot.

## Reproduction and scope

The dependency order is in `reproduce.py`. The new SAT/optional-star commands
are `neighbor_incidence_sat.py`, `incidence_model_geometry.py`,
`audit_incidence_collisions.py`, `incidence_sample_exclusions.py`,
`audit_incidence_samples.py`, `neighbor_incidence_geometry_sat.py`,
`incidence_model_star_seed.py`, the generic forced propagator on that seed,
and `audit_incidence_star_cuts.py`. Exact arguments appear in the reproduction
list. Q021–Q022 add `neighbor_star_cut_sat.py`, `audit_neighbor_star_cuts.py`,
one forced layer and its full audit, expanded arcs and their audit,
`audit_neighbor_arc_cuts.py`, and `verify_neighbor_arc_cut_certificate.py`.
Q023–Q024 and the deeper old-model failure are also in the dependency list,
which now has 100 commands. All are finite experiments.
All were run separately; the enlarged combined sequence was not rerun
from the beginning. No publication, outside review, Lean proof, or solid
realization is claimed.

`SYMMETRY_LEMMA.md` now also states the proper-isometry variant: if a recognizable
hierarchy at every scale is preserved only by orientation-preserving
symmetries, packing makes that subgroup finite and its index is at most two
in the full symmetry group. This conditional observation does not supply the
still-missing hierarchy.

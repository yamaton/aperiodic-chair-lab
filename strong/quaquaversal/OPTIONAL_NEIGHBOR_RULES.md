# Optional neighbors, pilot branches and verified choice cuts

This continues [PARENT_PROPAGATION.md](PARENT_PROPAGATION.md). Recursive
parent legality remains unproved. The global unresolved parent-cover count
is **246**; all later six-case pilots described here reject assignments or
branches, not these parent cases as a whole.

## Main continuation: 350 to 246

A forced layer from `expanded_arc_seed.json` rejects 35 of 350 cases and
leaves 315. The full explicit-set audit checks 29,145,299 domain
intersections and 3,801,491 distinct placements, including every retained
domain. Expanded arc consistency then rejects 69 of the 315, leaving 246.
Its 512,877 reductions and 185,698 distinct used geometric edges are
independently replayed. There are 47,234,830 directed edge occurrences
across these finite patches.

`expanded_arcs_2_seed.json` is the latest full continuation seed. It retains
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

## Next attempt

Add the verified center-choice cuts to the Q019 SAT model. For a cut
`[(i,s),(j,t)]`, forbid choosing star `s` at center `i` together with star `t`
at center `j`. Apply a cut only when its fixed geometric center IDs refer to
the same pose table; if a center is absent from a pilot problem, do not
silently assert that it exists. A star unavailable in a center's domain makes
that conjunction impossible already.

Recheck the model. For a new satisfying assignment, repeat complete-neighbor
extension and extract more verified cuts; optionally check exact geometric
conflicts too. Preserve timeouts and a finite cut-round limit as unknown.
An unsatisfiable parent instance will require an appropriately checked solver
certificate or an independently replayable exhaustive argument; do not infer
it merely because several sampled assignments fail.

The original Q018 and Q019 producers remain separate, source-bound experiment
snapshots. Prefer a new cut-enabled producer rather than silently changing
the meaning of their retained artifacts. The six-case pilot is not the whole
246-case frontier. The current full frontier remains `expanded_arcs_2_seed.json`.

## Reproduction and scope

The dependency order is in `reproduce.py`. The new SAT/optional-star commands
are `neighbor_incidence_sat.py`, `incidence_model_geometry.py`,
`audit_incidence_collisions.py`, `incidence_sample_exclusions.py`,
`audit_incidence_samples.py`, `neighbor_incidence_geometry_sat.py`,
`incidence_model_star_seed.py`, the generic forced propagator on that seed,
and `audit_incidence_star_cuts.py`. Exact arguments appear in the reproduction
list. All were run separately; the enlarged combined sequence was not rerun
from the beginning. No publication, outside review, Lean proof, or solid
realization is claimed.

`SYMMETRY_LEMMA.md` now also states the proper-isometry variant: if a recognizable
hierarchy at every scale is preserved only by orientation-preserving
symmetries, packing makes that subgroup finite and its index is at most two
in the full symmetry group. This conditional observation does not supply the
still-missing hierarchy.

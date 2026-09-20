# Conditional parent patches and a second recognizable grouping

The full unresolved frontier is now **82** parent covers. Q029 strengthens
the direct parent-language test. Q030 verifies a recognizable
grouping step for the resulting enlarged language. Q031 then tries to exclude
the remaining extra stars by an eight-sibling CSP; that attempt adds no
exclusions. The all-scales hierarchy objective remains open.

## Q028: another complete fine propagation round

`propagate_choice_cuts.py` generalizes unit-cut propagation to later seeds,
checking the catalog's exact pose-table prefix. This avoids mistaking a
changed full-input hash for a change of geometric coordinates. The 163 cuts
remove two star values from parent case `(259,1)`; all 177 cases remain.
`audit_choice_cut_pass.py` independently replays every removal and every
retained domain.

The next forced layer excludes seven covers, leaving 170. Its full audit
checks 45,887,796 intersections and 8,942,668 distinct exact placements.
Fine arc consistency then excludes 40 more, leaving 130; 614,903 reductions
and 288,767 distinct used geometric edges are independently replayed.
The shared pose catalog grows to 274,091 entries, including positions from
failed cases. The graph's 61,729,024 directed edge occurrences are not a
distinct-edge or patch-size count.

## Q029: neighbors of a fixed parent star must agree with one another

Start with the complete 177-case frontier from Q027. Its parent stars lie
in the original 6,840-star language plus these 177 extras. For a proposed
root star `s`, the root and every neighbor pose in `s` are necessarily
present. At a neighbor `q`, initialize the possible stars to
`C(s,q) ∩ A`, where `C` is the coarse compatibility table and `A` the current
global parent-star vocabulary. The root itself has domain `{s}`.

Apply necessary arc consistency between these forced positions whenever
their relative pose belongs to the audited vocabulary. If any domain becomes
empty, no actual parent tiling using `A` can have root star `s`. Remove such
stars simultaneously and repeat with the smaller vocabulary. This is stronger
than merely requiring each neighbor to have some compatible star separately.
It still omits some geometric conflicts and does not prove that surviving
star choices extend jointly or infinitely.

`audit_coarse_support_domains.py` first recomputes every support set by a
different representation of shared-position signatures: all 300,497
incidences and 16,334 distinct support domains over 7,075 possible stars.
Both directions of set equality are checked, so no target is silently omitted
before an arc proof uses that table. The existing exact map and reciprocity
audits supply the geometric part of the fingerprint condition.

`coarse_star_arc_filter.py` removes nine extras, then eight, then stabilizes
with **160** extras. Its independent replay checks all 505 conditional
patches, 14,442 reductions, and 1,104 distinct rational geometric edges,
including every retained conditional domain. These are exclusions of possible
parent-star types, not rejections of selected SAT assignments. They may overlap
fine-level exclusions, so counts must be combined by case key.

The 17 first-pass exclusions all lie among Q028's fine exclusions, so their
intersection still has 130 cases. Repeating the conditional parent-patch
test with only those 130 extras excludes **48** more, then stabilizes at
**82**. That second run has 212 conditional patches, 4,004 reductions and
692 distinct geometric edges, all independently replayed.

`merge_coarse_star_filter.py` and its separate auditor check full case coverage
and preserve retained fine domains exactly. The final full seed is
`coarse_arc_frontier_2.json`, with 82 live records among 170 stored records,
the 274,091-position fine pose table, and the fine arc domain pool. Overall
the reduction from 177 is `7 + 40 + 48 = 95`; do not add the overlapping 17.
The parameterized producers/auditors can continue from later complete seeds.

## Q030: the 7,000-star enlarged rule has one recognizable grouping

Let `E` consist of the original 6,840 stars and those 160 extra stars.
`enlarged_sibling_roles.py` checks the following finite hypotheses directly:

1. Every star in `E` contains the mandatory touching-sibling pattern of
   exactly one of the eight child roles.
2. For each such sibling contact, every compatible target star in `E` has
   the required sibling role. All 42,658 incidences and 811,528 target
   alternatives are checked.
3. The sibling-contact graph on the eight child roles is connected. Exact
   child geometry verifies each relative pose and the identities relating
   the proposed parent frames.

These facts give the same one-step grouping argument as in
[CLOSED_STAR_RULES.md](CLOSED_STAR_RULES.md), now for the enlarged rule:
give a tile its unique role and the corresponding proposed parent frame.
Every touching sibling required by that role is present in its complete
star. Compatibility forces that sibling's expected role, hence the same
parent frame. Connectivity yields all eight children of that parent.
Their supports fill the parent prism by the verified substitution geometry.
Each tile has only one role and parent frame, so the eight-child groups
partition the tiling. Any other substitution grouping would have to use
the same mandatory sibling patterns and therefore the same roles and frames.
Thus the grouping is unique and equivariant under proper isometries.

Consequently an original-rule tiling has **two nested recognizable grouping
levels**: its first parent tiling obeys `E` by the complete-frontier bounds
and Q029 exclusions, and a tiling obeying `E` has the grouping just proved.
The corresponding supports are `2P` and `4P` relative to the original tile.
This does not assert that parents of `E`-tilings again obey `E`, so it does
not supply the arbitrarily many levels needed by `SYMMETRY_LEMMA.md`.

This is a written argument supported by exact finite checks. It is not a
new Lean theorem or an externally reviewed result.

## Q031: the eight-sibling extension attempt is insufficient

An extra star in any `E`-tiling would occur in an eight-child parent.
For each of the 160 extras, fix that star at its recognized role and solve
the necessary compatibility constraints among eight sibling stars in `E`.
A finite exhaustive failure could exclude the star; a node limit is unknown.

All **160** tests find compatible tuples, using 452 search nodes in total.
No node limit or UNSAT result occurs. `audit_enlarged_sibling_probe.py`
checks all witnesses and their 8,000 directed sibling incidences. This
attempt therefore adds **zero exclusions**. The tuples satisfy only the
stated sibling compatibility relaxation; their outer neighborhoods need
not coexist geometrically and they are not tiling witnesses.

The unresolved alternatives are to impose wider coarse patch constraints,
describe possible grandparents of `E`-tilings, or continue the complementary
fine-domain propagation. Simply showing two grouping levels is insufficient
to conclude finite symmetry groups.

## Q032: one wider parent-scale layer adds no exclusions

The final Q029 conditional patches have now been expanded one forced-neighbor
layer outward. `prepare_coarse_expansion.py` creates explicit parent-scale
atlas, compatibility and seed inputs. The active vocabulary is the original
6,840 plus 82 extras, restricted from the audited 7,075-star support table.
The separate adapter audit checks all 82 cases, 3,572 seed-domain records,
and 1,291 used inverse pairs. The atlas retains all 1,295 poses for stable
indices; the four extra poses are unused by this active vocabulary.

The new generic producers/auditors accept explicit atlas and rule paths and
check coordinate-level tags. Parent world tiles have scale 1, unlike the
scale-1/2 fine world. Their pose IDs must never receive the fine 163-choice
cuts. The 160 sibling witnesses from Q031 still belong to the older
7,000-star relaxation, not automatically to the current 6,922-star language.

`propagate_rule_domains.py` adds only neighbors present in every possible
star at a known tile, unions possible target stars for each source, and
intersects constraints from different sources. All **82** cases survive.
Its separate explicit-set/rational audit checks 140,525 domain intersections
and 36,676 distinct placements. The shared world table grows to 4,648 poses.

`rule_arc_consistency.py` then constrains the already forced tiles against
one another. All **82** again survive: **zero additional parent exclusions**.
The separate replay checks 15,782 domain reductions and 6,850 distinct
geometric edges. These counts are reductions of possible stars at individual
tiles, not numbers of parent cases excluded. Surviving domains are necessary
conditions only; no infinite extension or geometric patch witness is claimed.

The lossless continuation artifact is `coarse_arc_seed_1.json`, using the
arc domains and the forced layer's parent-scale pose table. The fine frontier
remains `coarse_arc_frontier_2.json`; neither replaces the other's coordinate
namespace. Both have 82 live case keys. No second coarse expansion has run.
At the user's request, research is being held at this checkpoint for a
[status review](RESEARCH_STATUS_JA.md).

On resumption, another coarse forced layer and arc replay can use the same
parameterized scripts. A separate, unimplemented strengthening could exploit
Q030's recognizable grouping to exclude compatible star pairs whose proposed
parents overlap in their interiors. That test would need exact overlap
witnesses and a separate checker; it cannot assume that grandparents already
obey the same star rule. Any global elimination must cover the full necessary
frontier, not just selected SAT assignments.

## Reproduction

The exact dependency order and paths are in `reproduce.py`. The new checks
are `audit_coarse_support_domains.py`, `coarse_star_arc_filter.py`,
`audit_coarse_star_arcs.py`, `enlarged_sibling_roles.py`,
`enlarged_sibling_probe.py`, and `audit_enlarged_sibling_probe.py`.
All results retain input hashes. Original snapshot files are preserved.
Q032 adds `prepare_coarse_expansion.py`, `audit_coarse_expansion_inputs.py`,
`propagate_rule_domains.py`, `audit_rule_domains.py`, `rule_arc_consistency.py`,
`audit_rule_arcs.py`, and `prepare_rule_arc_seed.py`, in that order with their
default paths. The enlarged reproduction list has 136 commands. Each new command was run
separately; the entire historical sequence has not been rerun from scratch.

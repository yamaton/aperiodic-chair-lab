# Fine propagation and direct parent-star constraints

This Q025–Q027 checkpoint reduces the full unresolved frontier from **246 to
177**. The [conditional parent-patch continuation](CONDITIONAL_PARENT_PATCHES.md)
now leaves **82**. These are necessary exclusions of parent neighborhoods in original
closed-star-rule tilings. No surviving cover is asserted to extend to a
tiling, and recursive hierarchy enforcement remains open.

## Q025: extend the narrowed fine frontier

Start with `choice_cut_frontier_seed.json`, the Q024 full frontier. One
forced-neighbor layer leaves 235 of 246 covers. The full independent audit
checks 39,563,364 set intersections and 6,370,963 distinct rational placements,
including every retained domain and all 11 rejected witnesses.

Expanded arc consistency on these 235 patches rejects another 30, leaving
205. All 620,066 recorded reductions and 240,751 distinct used geometric
edges are independently replayed. The original graph discovery reports
56,697,206 directed edge occurrences; that is not a count of distinct edges.

The resulting pose table has 195,032 entries, including retained positions
from rejected cases. It is not the size of any one patch.

## Q027: prune possible stars of the parent tiling itself

One-level recognizable grouping gives a parent tiling for any tiling obeying
the original 6,840-star rule. The earlier complete cover enumeration and
the necessary Q025 tests imply that every parent star belongs to the old
language or one of the 235 surviving nonlanguage covers. Thus **7,075**
stars form an overapproximation of every possible parent star at this stage.
This statement concerns the full frontier, not a selected SAT pilot.

These stars use a 1,295-pose vocabulary: the old 1,291 closed-contact poses
and four more poses already present in the cover enumeration. The four
additional poses have nonempty closed intersections with the root prism;
their geometry is checked exactly. All 7,075 stars contain the mandatory
touching-sibling pattern for exactly one of the eight child roles. This
last observation is only a local role test; it does not prove a new hierarchy
for the enlarged rule.

For a source star `S` containing neighbor `q`, any actual neighbor tile must
have some target star `T` containing `q^-1`. The two complete stars must
agree on tiles visible at both centers. The stored partial coordinate map
`M_q(r)=q^-1 r` expresses such shared positions; the root is included as
the identity pose. Equality of the two shared-position sets is necessary.
The map need not inspect every geometric contact, but every retained map
entry must be exact and paired with its inverse entry. An inverse neighbor
pose outside the whole vocabulary leaves no possible target star at all.

Iteratively remove a star if one of its neighbors has no compatible target
among the still-live stars. Soundness follows by induction: if an actual
parent tiling used a star removed in this round, its actual neighbor would
have to use a star already removed or fail the necessary shared-position
test. Both are impossible. Hence removing these stars cannot remove a star
that occurs in a parent tiling of an original-rule tiling.

`coarse_parent_language.py` removes 27 extras in the first round and 13 in
the second, leaving 195 extras. `audit_coarse_parent_language.py` checks
452 added exact map entries and 93,494 reciprocal entries. For each rejected
star it compares **every** still-live target containing the inverse neighbor,
without trusting the producer's support buckets: 59,585 comparisons in total.
All 6,840 original stars remain.

## Combine the two necessary tests

After the fine arc run, only 205 extras remain possible. Starting the same
coarse support pruning from those 205 removes 26 then two more, leaving
**177**. The new full seed is `coarse_refined_frontier.json`. It retains the
fine arc domains exactly for each surviving case and uses the 195,032-position
pose table from `choice_cut_forced_1.json`.

| Test | Input covers | Additional exclusions | Remaining |
|---|---:|---:|---:|
| Q025 forced layer | 246 | 11 | 235 |
| Q025 fine arcs | 235 | 30 | 205 |
| Q027 coarse support after fine arcs | 205 | 28 | 177 |

The standalone coarse exclusion count of 40 overlaps the fine exclusions;
it must not be added to 11 and 30. `audit_coarse_refinement.py` independently
checks the combined live vocabulary, exhaustively checks each of its new
coarse exclusions, and verifies every retained domain and case identifier.

The seed's result indices are local to this new artifact. Continue using
`boundary_index`/`cover_index` as the stable parent-case key; pose IDs retain
the earlier pose-table prefix. Records without `domains` are rejected cases,
not input patches for further propagation.

## Next steps and limits

Continue fine propagation and audited choice-cut unit consequences from the
177-case seed, then feed any further full-frontier exclusions back into the
coarse vocabulary. A further coarse pass must start from a complete necessary
frontier; restricting it to a few chosen examples would be unsound.

Separately, [Q026 domain certificates](DOMAIN_CERTIFICATES.md) now carry
conditional contradictions through multiple forced and arc layers. The
163-cut catalog can strengthen SAT experiments. Its last eight-choice cut
excludes an assignment rather than a whole parent case.

Even if every currently considered pattern survives a finite test, that does
not prove infinite extension. At present 177 nonlanguage parent stars remain
unexcluded, so the proof that parents obey the original rule is unfinished.
No all-tilings hierarchy, geometric monotile realization, external review,
or new Lean proof is claimed.

The exact commands and dependencies are in `reproduce.py`. Every new search
and audit ran separately; the entire enlarged historical sequence was not
rerun from its beginning.

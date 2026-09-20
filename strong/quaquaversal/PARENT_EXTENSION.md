# Extending the recognized parent neighborhood

Q012–Q014 continue the unresolved recursive-legality problem from
[CLOSED_STAR_RULES.md](CLOSED_STAR_RULES.md). Every exclusion below is a
necessary-condition exclusion within the proposed 6,840-closed-star rule.
No surviving finite candidate is claimed to extend to a tiling. No
aperiodicity, single-solid realization, or external-review claim is made.

## Q012: simultaneous exterior stars

Generalize the sibling intersection-fingerprint test to all 290,189
root/neighbor incidences of the allowed stars. There are 105,242 distinct
compatibility domains, sharing lists of possible neighboring stars.
An exact scaled-integer implementation is independently checked using
Fraction arithmetic on all 253,296 relevant relative products. This also
replays the earlier 41,719 sibling checks.

Each of the 58,740 eight-child tuples fixes a geometric neighborhood of the
proposed parent. If two root children see the same external tile, that tile
must admit one closed star compatible with both. Intersecting these domains
rejects 47,180 tuples, leaving 11,560, including every genuine tuple. The
remaining extra count falls from 52,485 to 5,305. A separate set-based audit
checks placement, exhaustive tuple accounting and 1,295,259 intersections.

All possible tiles in these neighborhoods occupy 1,446 distinct positions.
Their pair graph has 79,636 allowed undirected atlas contacts and 125,077
forbidden intersecting pairs; 246,793 bounding-box-compatible pairs were
examined, including 167,157 edge-clipping tests. A forbidden pair means
overlap or a touching pose outside the allowed atlas. None of the retained
11,560 tuples is rejected by that shortcut.

Arc consistency also compares external tiles with one another: remove a
candidate star whenever it has no compatible star at a neighboring tile,
and repeat. It rejects another 2,280 tuples. There remain 9,280 tuples:
6,255 genuine and 3,025 extra. An audit checks all 159,272 directed edge
poses with rational formulas, then independently replays synchronous domain
updates rather than the producer's queue. All 11,560 outcomes and surviving
domains agree after 36,916 synchronous rounds in total.

## Recovering parent supports is still insufficient

For an external tile with possible child role `i`, the proposed parent is
its pose composed with the inverse of child map `i`. Every child of this
parent touching the root parent must be present in the fixed neighborhood
and have its correct role. Neighboring parents cannot overlap in their
interiors. These give a finite boundary exact-cover problem.

The stronger arc domains leave 1,295 possible parent poses, four outside the
original 1,291-pose atlas. Exhaustive boundary-cover enumeration on the
9,280 tuples produces 16,197 covers: exactly the 6,840 genuine parent stars,
plus 9,357 distinct nonlanguage covers. No case reaches the cover limit in
this run. All covers are legal for 5,196 tuples; 4,084 tuples retain at
least one nonlanguage cover. Every known parent-star cover is separately
checked against its child tuple, its admissible parents, and full boundary
coverage, independently of when it occurs in the enumeration.

The first boundary-cover run, before arc propagation, hit the 10,000-cover
limit in one case and then failed a final implementation assertion because
only 6,838 genuine covers had been enumerated. Its source and failure record
are preserved as `parent_boundary_cover_initial.py` and
`parent_boundary_cover_initial_failure.json` in `artifacts/`. This was not a
mathematical exclusion. The repaired script checks genuine witnesses
directly and preserves capped cases as unknown. The stronger run above
completes without a cap.

## Q013: fix all roles of one cover together

The boundary cover had tested each tile's proposed role individually.
Restrict all exterior star domains to the cover's chosen roles at once,
then repeat arc consistency. Of the 9,357 nonlanguage covers, 3,373 now
contradict the star constraints and 5,984 survive.

These surviving covers concern 3,993 root tuples: all 3,025 extra tuples and
968 genuine tuples having spurious alternative parent covers. Across their
663,862 tile-domain occurrences, 614,792 are already singleton stars. This
suggests testing what those stars force beyond the current patch.

## Q014: one additional forced layer

For a tile with domain `D`, a relative neighbor pose is forced only when it
occurs in **every** star in `D`. The neighboring tile may use any star
compatible with at least one member of `D`, so take a union of compatibility
domains. If several centers force the same tile, intersect their allowed
domains. Empty intersections are contradictions; optional neighbors are not
assumed to exist.

One such expansion rejects 1,949 of the 5,984 nonlanguage covers, leaving
4,035 unresolved covers. The shared position catalog grows to 10,240 tiles,
and surviving domains use 17,747 shared lists. A separate explicit-set audit
replays every rejected cover's empty-intersection witness and exact geometric
placement. That audit does not certify realizability of survivors.

## Next step and data navigation

This is the first exterior-extension checkpoint. Subsequent
[repeated propagation](PARENT_PROPAGATION.md) reduces its 4,035 survivors
to 350; resume from `expanded_arc_seed.json` as described there. The older
navigation below describes the preserved input to that continuation.

Continue from `artifacts/forced_outer_layer.json`. Each surviving record has
tile/domain IDs into that file's `poses` and `domain_pool`; its parent cover
is identified by `boundary_index` and `cover_index` in
`parent_boundary_cover_arcs.json`. `source_index` points back to
`parent_cover_star_constraints.json`.

Repeat necessary forced-neighbor propagation on the expanded domains,
allowing existing domains to shrink and thereby force new neighbors. Use
explicit round/patch bounds and retain survivors as unknown. If propagation
stalls, check all pairwise compatibility within the expanded patch, then
branch on remaining finite domains or investigate structured surviving
faults. More distant forced tiles must never be silently discarded as
evidence of impossibility. The desired conclusion remains recursive parent
legality in arbitrary tilings, followed by the finite-symmetry argument.

## Reproduction

After the Q011 checkpoint, run:

```sh
uv run --locked python strong/quaquaversal/closed_star_compatibility.py
uv run --locked python strong/quaquaversal/audit_star_compatibility.py
uv run --locked python strong/quaquaversal/parent_external_domains.py
uv run --locked python strong/quaquaversal/audit_external_domains.py
uv run --locked python strong/quaquaversal/parent_neighbor_graph.py
uv run --locked python strong/quaquaversal/parent_star_arc_consistency.py
uv run --locked python strong/quaquaversal/audit_parent_arcs.py
uv run --locked python strong/quaquaversal/parent_boundary_cover.py --arcs --output strong/quaquaversal/artifacts/parent_boundary_cover_arcs.json
uv run --locked python strong/quaquaversal/parent_cover_star_constraints.py
uv run --locked python strong/quaquaversal/forced_outer_layer.py
uv run --locked python strong/quaquaversal/audit_outer_rejections.py
```

All these commands ran separately for this checkpoint. The expanded combined
`reproduce.py` sequence has not been rerun from its beginning. Source hashes,
explicit witnesses and retained bounds identify the scope of each result.

# Repeated exterior propagation and expanded-patch constraints

Continuation of [PARENT_EXTENSION.md](PARENT_EXTENSION.md). The objective
is still open: recursive parent legality and finite symmetry of every
admitted tiling have not been proved. The counts below concern unresolved
parent-cover candidates, not actual infinite tilings.

## Q014: further necessary layers

`propagate_forced_domains.py` repeats the exact synchronous operation from
the first forced layer. A neighbor must occur in every possible star of its
center to be forced. Its domain is the union of the compatible choices;
constraints from different centers are intersected. No optional neighbor
is assumed to exist. Each round is explicitly bounded to one expansion.

| Layer | Input covers | Rejected in this layer | Surviving covers | Shared position catalog |
|---|---:|---:|---:|---:|
| 1, previous checkpoint | 5,984 | 1,949 | 4,035 | 10,240 |
| 2 | 4,035 | 2,481 | 1,554 | 26,428 |
| 3 | 1,554 | 478 | 1,076 | 49,035 |
| 4 | 1,076 | 332 | 744 | 74,903 |

Position-catalog counts include positions retained from earlier failed
cases; they are not tile counts of any one patch. At layer 3, individual
surviving patches have between 828 and 2,139 forced tiles.

The audit gap before this continuation was also closed: all 9,357 Q013
cover-role domain computations were replayed with synchronous updates,
agreeing on the 3,373 rejections and 5,984 survivors in 17,472 rounds.

`audit_forced_domains.py` independently uses explicit sets and rational
placements to replay **every retained domain**, as well as all rejected
empty-domain witnesses. Thus the audits check that the surviving domains
were not made artificially small. Layer 1 checks 18,897,273 intersections;
layers 2, 3 and 4 check 24,088,323, 33,572,182 and 39,348,389 respectively.
The layer-4 audit checks 2,501,738 distinct relative placements. These are
finite computational certificates, not Lean verification or external review.

## Descriptive parent defects

For each of the 1,076 layer-3 survivors, compare its parent-star pose set
with all 6,840 legal stars and choose a minimum symmetric difference,
breaking ties by the legal-star ID. In 855 cases all differing contacts
are point-only; in 220 the maximum differing contact dimension is one;
in one case it is two. Fifteen covers use a parent pose outside the original
closed atlas. The most common symmetric-difference size is three (635 cases).

`parent_defect_profiles.json` retains the chosen nearest legal star and all
added/removed pose IDs. These profiles guide further attempts; similarity
to a legal star is neither an exclusion nor an extension certificate.

## Q015: geometric collisions in forced patches

The expanded patches can contain pairs forced by different centers which
were never geometrically checked together. Exact integer bounding boxes
and atlas membership reduce the pair search. For a non-atlas relative pose,
edge clipping decides whether the supports touch or overlap. A positive
intersection outside the atlas is forbidden by the proposed closed-star
rule, regardless of whether it has volume, area, length, or just one point.

Testing all 1,076 layer-3 patches rejects 17 and leaves 1,059 unresolved.
There are eight distinct geometric witnesses. A separate audit recomputes
each relative pose, proves it is outside the atlas, and verifies the recorded
common points lie in both closed polyhedra. Each rejected patch actually
contains the two witness tiles. The audit covers exclusions; it makes no
realizability claim for the survivors.

## Q016: use contacts within the expanded patch

Further forced expansion is not the only available strengthening. In a
current finite patch, enumerate possible relative neighbors of each tile
from the union of its star domain. If such a neighbor is already present,
require their star domains to be mutually compatible. This can delete
choices even when that relative neighbor was not previously shared by
every star in the center's domain.

`expanded_arc_consistency.py` applies these constraints to the 744 layer-4
survivors and rejects 394, leaving 350 unresolved. There are 55,167,408
directed edge occurrences across the finite patches. Exact scaled integers
implement pose composition. Every actual
domain reduction is logged as a triple `(center, neighbor, relative-pose-ID)`.
`audit_expanded_arcs.py` replays all 1,054,536 reductions with rational geometry
and explicit sets, checking 242,468 distinct used edges without trusting the
integer placement index. All 394 rejected and 350 retained domain results
agree. Any geometric
contacts the discovery procedure misses only weaken this necessary test.

`prepare_forced_seed.py` combines its surviving domains with earlier Q015
geometric exclusions using the fixed parent-cover keys. The resulting
`expanded_arc_seed.json` preserves the original pose table and narrowed
domains, ready for another bounded forced-propagation round. None of its
350 survivors is one of the earlier geometric rejections, so combining that
filter causes no further reduction at this checkpoint. The seed has 74,903
shared positions and 22,558 domain lists; only 350 records have `domains`.

The next commands are:

```sh
uv run --locked python strong/quaquaversal/propagate_forced_domains.py --input strong/quaquaversal/artifacts/expanded_arc_seed.json --output strong/quaquaversal/artifacts/forced_after_arcs_1.json
uv run --locked python strong/quaquaversal/audit_forced_domains.py --input strong/quaquaversal/artifacts/forced_after_arcs_1.json --source strong/quaquaversal/artifacts/expanded_arc_seed.json --output strong/quaquaversal/artifacts/forced_after_arcs_1_audit.json
```

Then, if survivors remain, repeat expanded-patch arc consistency using its
`--input`/`--output` arguments, audit with the corresponding `--source`, and
prepare a continuation seed with the corresponding `--poses-source`. These
next propagation commands have not run at this checkpoint.

## Reproduction

The full command order is in `reproduce.py`. The new reusable commands are:

```sh
uv run --locked python strong/quaquaversal/audit_cover_domains.py
uv run --locked python strong/quaquaversal/propagate_forced_domains.py
uv run --locked python strong/quaquaversal/audit_forced_domains.py
uv run --locked python strong/quaquaversal/parent_defect_profiles.py
uv run --locked python strong/quaquaversal/forced_patch_geometry.py
uv run --locked python strong/quaquaversal/audit_forced_geometry.py
uv run --locked python strong/quaquaversal/expanded_arc_consistency.py
uv run --locked python strong/quaquaversal/audit_expanded_arcs.py
uv run --locked python strong/quaquaversal/prepare_forced_seed.py
```

For later layers, pass explicit `--input` and `--output` paths to the
propagator; pass the corresponding `--input`, `--source` and `--output` to
the full-domain audit. The initial layer additionally needs the documented
`--source-poses` argument because its earlier input did not embed positions.
All exclusions, surviving domains, bounds and source hashes remain local.

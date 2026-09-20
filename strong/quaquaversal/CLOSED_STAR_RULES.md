# Closed-star rules and the remaining parent-language problem

Q009 and Q011, local research checkpoint. The proposed rule allows exactly
the 6,840 closed neighborhoods listed in `artifacts/closed_star_language.json`,
up to a proper rigid motion. A closed neighborhood includes every tile
touching the root, even at just an edge or a point. The root is not included
in the stored neighbor list. These are finite geometric neighborhood rules,
**not** yet face markings or a recut solid.

Exact calculations support a recognizable **one-level** partition into
eight-child quaquaversal parents. Recursive legality of those parents remains
open. Therefore no aperiodicity or finite-symmetry theorem is claimed for
this rule. The arguments and certificates below have not received external
review or Lean verification.

## Closed contacts are insufficient

The directed contact atlas stabilizes at 1,291 relative poses. An independent
edge-clipping audit classifies 91 positive-area contacts, 247 edge-only
contacts, and 953 point-only contacts. It replays every generation witness
and checks 6,776 bounding-box-compatible child pairs for closure.

The original 24-prism periodic reflection tiling satisfies this entire
atlas, including its lower-dimensional contacts. Thus adding edge and vertex
**pair** information to Q006 still does not enforce aperiodicity.

## The complete interior-supertiling star language

Define the language to consist of closed stars whose root support is strictly
inside some finite proper-copy substitution iterate. This deliberately does
not assert that arbitrary infinite-hierarchy faults introduce no other stars.

The complete parent star determines the stars of all eight root children:
any tile touching a root child belongs either to the root parent or to a
parent touching that parent. Subdivide all these parents and retain the
children touching the selected root child. The audited closed atlas makes
this an exact finite operation on neighbor-pose IDs.

Start with a complete star observed inside a level-3 supertile. Its descendant
stars are again genuine interior-supertiling stars. Conversely, every star
in the defined language occurs inside some iterate of the root prototile,
which is part of the seed star. Repeatedly subdividing that seed therefore
produces the star. Thus stabilization of this operation proves completeness
for the stated language; it is stronger than absence from a finite sample.

The closure has 6,840 stars and stops adding stars at round 11. The independent
audit reconstructs the seed in the 512-tile patch, tests its neighbors using
edge clipping, recomputes all child-contact lifts by the same independent
predicate, and replays every star's provenance and all 54,720 transitions.
All previously sampled complete stars occur in this closure.

The standard expanding interior address from Q000 supplies an infinite
tiling obeying this language. This is existence, not hierarchy enforcement.

## A periodic obstruction persists through subdivision

The level-2 subdivision of the 24-prism periodic control has 1,536 tiles per
cell and 62 star types. Eighteen types are outside the now-complete language.
They are forbidden for this proposed rule, rather than merely unobserved.

Closing just these bad stars under child subdivision, while discarding legal
descendants, produces 47 bad types. A recorded reachable self-loop proves
that some bad star survives at **every** subsequent subdivision level. This
rejects this particular infinite family of periodic controls. It does not
reject all periodic tilings. At level 10, the control has 25,769,803,776 tiles
per period cell; a multiplicity recurrence, not explicit tile enumeration,
finds 2,136 bad tiles and 34 bad star types.

## Recognizing and grouping one parent level

Every one of the 6,840 legal stars appears among child descendants in exactly
one of the eight child positions. The numbers by position
`(1A,2A,3A,4A,1B,2B,3B,4B)` are
`(2010,543,334,967,1424,390,444,728)`.
This defines a geometric child-role function on allowed root stars.

Local role recognition alone is insufficient: neighboring tiles might infer
different parents. The next certificate checks their common neighbors.
For a root star and a prescribed touching sibling, any actual neighboring
star must agree on all tiles seen by both centers. Transforming those tiles
into the neighbor frame gives an exact intersection fingerprint. Enumerate
every allowed neighbor star with that fingerprint. All 41,719 root/sibling
cases force exactly the expected sibling role; none is unresolved.

The following grouping argument is conditional only on these finite tables
and their geometric interpretation being correct. For a tile of role `i`,
its proposed parent pose is its pose composed with the inverse of child map
`i`. The star contains every touching sibling in that proposed parent.
The fingerprint certificate forces each sibling's role, so it infers the
same parent. The sibling-contact graph is connected. Propagating along it
produces all eight children. Their supports fill the proposed parent exactly.
Every tile has one role and hence one parent; the eight-child blocks partition
the tiling. Proper isometries preserve this construction.

The first fingerprint test may admit some unrealizable pairs: when a
relative pose is outside the closed atlas, it does not itself perform an
extra geometric intersection test. This weakens its necessary compatibility
condition. The successful role agreement remains sufficient despite that
overapproximation.

## Why this is not an infinite hierarchy proof

We must still show that the recovered parent tiling, after rescaling, obeys
the same 6,840-star rule. Closing the language under **subdivision** proves
the opposite implication, not this required one.

The 6,840 legal parent stars produce 6,255 distinct ordered tuples of eight
child stars. A complete constraint join using the certified sibling overlap
conditions admits 58,740 tuples. All genuine tuples are present, but 52,485
extra tuples remain. Adding common-neighbor checks between disjoint sibling
centers rejects none of these extras. These are preserved necessary local
candidates, not realized counterexamples and not infinite tilings.

The follow-up [exterior-neighborhood experiments](PARENT_EXTENSION.md) and
[repeated propagation](PARENT_PROPAGATION.md) now apply these extension and
role constraints, leaving 350 nonlanguage parent covers. They remain
unresolved finite candidates. Work continues with wider propagation and, if needed, explicit
hierarchy labels. A finite-symmetry conclusion needs grouping at arbitrarily
many scales, as explained in `SYMMETRY_LEMMA.md`.

## Reproduction

Run from the repository root, after the earlier geometry and sample scripts:

```sh
uv run --locked python strong/quaquaversal/closed_contact_atlas.py
uv run --locked python strong/quaquaversal/audit_closed_atlas.py
uv run --locked python strong/quaquaversal/closed_star_language.py
uv run --locked python strong/quaquaversal/audit_star_language.py
uv run --locked python strong/quaquaversal/star_parent_consistency.py
uv run --locked python strong/quaquaversal/parent_star_join.py
uv run --locked python strong/quaquaversal/parent_join_filter.py
```

Each script writes exact JSON with source hashes and replayable witnesses.
The full dependency order is in `reproduce.py`; `--audit-only` checks the
retained hashes and checkpoint expectations without repeating the searches.

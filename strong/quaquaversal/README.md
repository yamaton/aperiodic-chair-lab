# Quaquaversal matching-rule investigation

Started 20 September 2026 (UTC), at the user's request. Work remains local.

## Target and boundaries

Find finite, explicit matching rules compatible with the Conway–Radin
quaquaversal substitution and prove that **every** legal tiling has a finite
Euclidean symmetry group. The main research target is one decorated prototile
(and ultimately a geometric realization), rather than silently replacing it
by an arbitrary number of independently decorated prisms. Multiple-decoration
constructions are useful intermediate results and will be labelled as such.

The carrier is the right triangular prism with triangle sides 1, sqrt(3), 2
and height 1. Eight half-size copies form one parent. Substitution existence
does not by itself force that substitution in arbitrary legal tilings.

## Research protocol

1. Reproduce exact child geometry and coverage before searching markings.
2. Give each attempted family a persistent identifier and record its domain,
   assumptions, checks, witnesses, and outcome in `ATTEMPTS.md` and JSON.
3. Reject a candidate on an actual contradiction or periodic witness. A
   timeout or an incomplete search is **unknown**, not an impossibility proof.
4. After failure, change a stated assumption or rule family and continue.
5. Separate local-rule soundness, infinite existence, hierarchy enforcement,
   symmetry exclusion, and single-solid realization.

The target remains open. A first written obstruction rules out **all
pointwise one-decoration rules in the fixed proper-copy assembly**, not just
simple colors. See [the proof and exact certificate](PERIODIC_OBSTRUCTION.md).
Further finite families with reflected child assignments also have periodic
counterexamples. Even the closed 91-contact pose atlas and all observed
complete face-star rules admit explicit periodic fillings; see
[relative-pose rules](RELATIVE_POSE_RULES.md).
The [60-panel hierarchy route](MULTITYPE_ROUTE.md) supplies verified geometric
data for multiple decorated types; its explicit label inventory is pending.
[Pointwise map certificates](POINTWISE_GROUPOIDS.md) now reject all 256
stationary reflected words for equality and real scalar opposite-sign
markings. A stronger [6,840-type closed-star rule](CLOSED_STAR_RULES.md)
excludes the known periodic control and supports recognizable grouping of
one parent level. Recursive parent legality remains open. Subsequent
[exterior-neighborhood checks](PARENT_EXTENSION.md) and
[repeated propagation](PARENT_PROPAGATION.md) reduce the unresolved
possibilities to 246 nonlanguage parent covers. Further [fine and coarse
parent constraints](COARSE_PARENT_RULES.md) now leave **177**, with audited
domain and exclusion certificates. The current full seed is
`coarse_refined_frontier.json`. [Optional-neighbor pilots](OPTIONAL_NEIGHBOR_RULES.md)
and [layered domain proofs](DOMAIN_CERTIFICATES.md) provide 163 verified
forbidden combinations of center-star choices. Finite SAT models still
require deeper extension checks. Infinite extension of the remaining cases
and recursive hierarchy remain open.
See [attempts and commands](ATTEMPTS.md) and [primary sources](LITERATURE.md).
No novelty, external review, or fabrication claim is made.

Reproduce the current checkpoint from the repository root:

```sh
uv run --locked python strong/quaquaversal/reproduce.py
```

This replays both positive checks and expected failures. Exact JSON witnesses,
search results and replay logs are in `artifacts/`. No script silently treats
an incomplete search as aperiodicity or impossibility.
For a quick check of retained source hashes and result expectations, add
`--audit-only`; that mode does not rerun the geometric/search calculations.

## Coordinates

The scripts use rational coordinates `(u,y,z)`, representing physical
coordinates `(sqrt(3)*u,y,z)`. Thus the carrier is
`u >= 0, y >= 0, u+y <= 1, 0 <= z <= 1`, with metric
`diag(3,1,1)`. This keeps all eight maps rational without approximating sqrt(3).

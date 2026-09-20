# A periodic obstruction for one fixed decoration

**Result Q002b (20 September 2026):** for the recorded proper-copy
Conway–Radin substitution, any single pointwise face coloring that permits
the eight-child assembly also permits an explicit two-prism periodic tiling.
The result applies to arbitrary color functions, not just finitely many
colors, polynomials, or continuous functions.

The same conclusion holds when the rule requires an involutive complement
across each interface: matching c with J(c), where J²=id. Signed scalar
normal relief, with J(h)=−h, is one example at the interface-rule level.
This is **not** a classification of arbitrary recut solids, non-pointwise
rules, multiple independent decorations, or different child handedness words.

## Definition of the family

Use the carrier and proper child poses in `geometry.py`. Let B and T denote
the bottom and top triangular faces; L the long-leg rectangular face; S the
square face; H the hypotenuse rectangular face. Face charts are:

- B(a,b)=(a,b,0), T(a,b)=(a,b,1), a,b>=0, a+b<=1;
- L(a,b)=(a,0,b), S(a,b)=(0,a,b), H(a,b)=(a,1−a,b), 0<=a,b<=1.

Each coordinate triple represents physical (sqrt(3)u,y,z). The functions
B,T,L,S,H are the same on every congruent copy; copies use the listed proper
poses. Equality is required at every shared face point. Allowing exceptional
edge values does not affect the argument on open faces.

## Sibling identities

The first-level assembly requires, among other identities:

1. T(a,b)=B(a,b) (1A/1B).
2. S(a,b)=S(b,a) (1A/2A).
3. S(a,b)=S(a,1−b) (1B/2B).
4. H(a,b)=H(1−a,b) (2A/3A).
5. T(a,b)=L(1−a,b) (2A/4A).
6. T(a,b)=L(a,1−b) (3A/4A).
7. L(a,b)=L(a,1−b) (3B/4B).

Each triangular identity holds over its entire triangular domain, and each
square/rectangle identity over its entire unit-square chart. All of these
are actual area contacts, not an extension across a gap.

Identities 2,3,2 imply S(a,b)=S(1−a,b), using three contacts.
Identities 5 and 6 imply L(a,b)=L(1−a,1−b): use 5 backwards and 6
for a>=b, and 6 backwards and 5 for a<=b. Applying 7 then gives
L(a,b)=L(1−a,b), again with three contacts.

Thus horizontal reflection is permitted on **every** rectangular side face,
and identical points match between the triangular ends.

## The periodic counterexample

In each rational-coordinate unit box place P and its image under
(u,y,z) -> (1−u,1−y,z). These two congruent prisms partition the box.
Repeat with translations by (1,0,0), (0,1,0), (0,0,1), whose physical
lengths are sqrt(3), 1, 1. The side contacts use precisely
(a,b)->(1−a,b) on L,S,H; end contacts use the identity between T and B.
The identities above therefore make the whole periodic tiling legal.

Every derivation uses an **odd** number of contacts (one or three).
Replacing equality by involutive complementation preserves the conclusion,
because an odd composition of J is J. For a normal-relief realization,
this certifies interface compatibility only; a proposed displaced solid
still needs global noncollision and coverage checks.

## Exact certificate

`periodic_obstruction.py` reconstructs the 14 sibling contacts directly from
the rational solids, pulls each contact polygon into its two face charts,
and verifies six piecewise affine path certificates. At each step it checks
the entire input convex polygon lies inside the actual contact domain.
Three affine-independent probes prove equality of each composed affine map;
the two domains for L partition its square with disjoint interiors.
The derived maps are then compared with all ten directed contacts of the
two-tile periodic cell, including neighbors across the cell boundaries.

```sh
uv run --locked python strong/quaquaversal/verify_geometry.py
uv run --locked python strong/quaquaversal/periodic_obstruction.py
```

Evidence: `artifacts/geometry_and_constant_rules.json` and
`artifacts/periodic_obstruction.json`. This is a written deduction with exact
finite certificates, not an external mathematical review or a Lean proof.

## What changes next

Searching more elaborate scalar patterns within this family cannot solve
the problem. Q004 changes child handedness assignments. Q003 explores
multiple marked types with a forced hierarchy. Both genuinely change a
hypothesis of this obstruction; merely increasing polynomial degree does not.

# Why extra contact equations do not destroy the last freedom

*19 September 2026. Analysis prompted by the interactive rule lab. The frozen
solid and existing interface are unchanged.*

There is a geometric explanation for the observed plateau. In this proper
integer-grid port model, **every possible contact reverses a depth-independent
local chirality**. The equation graph is consequently bipartite before any
depth keys are assigned. A change of signs turns its equations into equality
along edges. Every connected component retains exactly one free scalar.
This is stronger than observing that the saved successful assignment fits.
It also applies to the unsuccessful substitution profiles.

## 1. A coloring supplied by geometry, not by the solution

At port i, let u_i and v_i be the ordered signed tangent axes and n_i the
outward base normal. Define

    chi_i = det[u_i, v_i, n_i] in {+1,-1}.

The port offset is (3u_i+v_i)/16 from its unit-face center. The unequal
magnitudes 3 and 1 determine the two ordered axes from the position.
For an opposed, registered unit-face contact with proper relative rotation R,
coincident port sites therefore imply

    u_i = R u_j,    v_i = R v_j,    n_i = -R n_j.

Thus chi_i = -det(R) chi_j = -chi_j. This is independent of the heights.
The common face center and the unique signed 3/1 decomposition justify
recovering both tangent axes here; this statement is about aligned grid
contacts, not arbitrary real placements of unregistered surfaces.

Consequently every contact equation x_i+x_j=0 joins opposite colors. Every
closed walk has even length. This is a structural obstruction to odd cycles,
not a fortunate result of choosing the twelve depth values.

The same determinant identity appeared in the earlier
[handedness argument](FOLLOWUP_REFLECTIONS.md#1-reflections-a-local-invariant-gives-a-global-reduction).
Here it is used in the other direction: proper rotations are fixed first,
then chirality colors the graph of potential equations. For an improper R,
chi_i=chi_j instead, so the unrestricted reflected-contact graph is not
covered by this bipartiteness conclusion.

## 2. The change of variables that explains the freedom

Set y_i=chi_i x_i. On an edge, chi_j=-chi_i, hence

    x_i+x_j = chi_i (y_i-y_j).

The complete system is therefore equivalent to y_i=y_j on each edge.
On a connected component C its general real solution is

    y_i=a_C, or x_i=chi_i a_C, for i in C.

A spanning tree on n vertices supplies n-1 independent equations. Each
remaining edge closes a cycle and contributes a dependent equation.
For c connected components and m distinct edges, the rank is n-c, the
solution dimension is c, and the number of independent row dependencies
is m-n+c. These counts refer to scalar equations, not geometric contacts
between whole chairs.

For the successful profile, each of its twelve components has 16 vertices
and 31 distinct edges. The first 15 spanning-tree edges leave one freedom;
the remaining 16 equations are redundant. There are 372 equations in total,
rank 180, nullity 12, and 192 independent equation dependencies.

For example, on a four-cycle the equations have the identity

    (x1+x2) - (x2+x3) + (x3+x4) - (x4+x1) = 0.

An odd cycle would instead imply x=-x, forcing that entire connected
component to zero. Since the system is homogeneous, zero is still a
solution; it becomes impossible only when a nonzero port depth is required.
The checker adds a hypothetical same-chirality chord as a negative control
and finds nullity zero for the affected component. That edge is disallowed
by the actual geometric coloring and is not a newly discovered contact.

## 3. Symmetry, transport and a precise conservation statement

The transformed constraints are invariant under y_i -> y_i+b_C throughout
one component. In x-coordinates this is x_i -> x_i+chi_i b_C. It is a
continuous freedom of the required-equation system, not a spatial symmetry
of the already decorated solid. Changes can cross zero or identify two
previously distinct depths, altering other, formerly forbidden contacts.
Therefore this invariance alone does not preserve the whole matching rule.

Equivalently, transport along an edge multiplies x by -1. The product along
every closed path is +1: transport is path-independent. In signed-graph
language the all-negative edge signature is **balanced**, and multiplication
by chi is a **switching** to an all-positive signature. It can also be
viewed as a trivializable Z2 connection with trivial loop holonomy. These
are standard interpretations, not a new signed-graph theorem. See
Zaslavsky, [*Signed Graphs and Geometry*](https://people.math.binghamton.edu/zaslav/Tpapers/mananthavady-lecture-notes.20110729.pdf),
Sections 2.1–2.2 and Theorem 3.6.

A quadratic diagnostic gives the same picture:

    E(x) = sum_edges (x_i+x_j)^2 = sum_edges (y_i-y_j)^2.

This is the ordinary graph Laplacian energy after switching. Its zero modes
are the constants on components. It is an algebraic diagnostic here, not a
measured physical energy or a specified dynamical model. No time evolution
or Noether conservation law is asserted.

There is also literal volume neutrality. The successful profile has eight
positive and eight negative signs in each component. This equal-part-size
property is additional to bipartiteness; it does not hold for every
bipartite graph. Thus every solution has sum_i x_i=0, independently for each
family. For the frozen cap shape, the signed volume contributed by one port
is

    w^2 delta x_i * integral[-1,1]^2
      (1-u^2)(1-v^2)(1+u/5+v/7) du dv
    = (16/9) w^2 delta x_i = x_i / 9437184.

The odd terms integrate to zero. While the caps remain separated and the
solid remains in the regime of the construction, varying family amplitudes
therefore preserves total volume 7. This volume cancellation is not the
reason odd cycles are excluded, and does not imply recursive aperiodicity.

## 4. Coordinate audit and the limits of the explanation

`audit/check_constraint_balance.py` imports no project implementation. It
reads frozen rational coordinates, independently enumerates all 24 proper
frames and nonoverlapping integer offsets, and reconstructs 1,194 contact
types. The frozen tangent frames match at every paired port. Every pair
reverses chi, including pairs outside all three selected substitution
languages. The union has 7,740 distinct undirected port-pair edges, forms
one connected bipartite graph on 192 ports, and retains one freedom.

In particular, assigning x_i=chi_i satisfies even **all** these potential
contact equations. This explains why the synthesis never needs to collapse
the entire pattern to zero, independently of which subset a stationary
substitution generates. It also shows why the plateau alone cannot explain
the successful deflation rule: excessive identification can allow every
proper geometric contact.

| Equation system | Components | Vertices per component | Edges per component | Total rank | Total free scalars |
|---|---:|---:|---:|---:|---:|
| Profile 0 | 4 | 48 | 153 | 188 | 4 |
| Profile 1, successful recurrence | 12 | 16 | 31 | 180 | 12 |
| Profile 2 | 12 | 16 | 27 | 180 | 12 |
| All geometric contacts together | 1 | 192 | 7,740 | 191 | 1 |

The checker reproduces the three selected graphs from the preserved
synthesis contact IDs, cross-checks the interactive export's contact poses
and graph edges, verifies spanning trees, fundamental-cycle parity and
equal sign counts, and records the artificial odd-cycle control.
It does not rerun the 6,561-template synthesis. Rank follows from the
explicit trees and sign solutions, not a floating-point rank estimate.

## 5. A further finite symmetry of the equation graph

There is an eight-element action on port sites: replace the ordered pair
(u,v) by any signed permutation of (u,v), then place the port at its new
offset (3u'+v')/16 on the same face. These operations form D4. They commute
with the frame identifications at each proper contact, so act as graph
automorphisms for every selected contact language. The audit verifies all
eight permutations, without referring to assigned depth equality.

They act transitively on profile 0's four components. Profile 1's twelve
components form orbits of sizes eight and four, and profile 2's form orbits
of sizes four and eight. This is an additional symmetry of the constraint
problem; the fixed signed depth assignment generally breaks it. It is not
an eight-element rigid symmetry group of the physical block, nor an
explanation of uniqueness of the successful recurrence profile.

## Reproduce

From the repository root:

```sh
uv run --locked python strong/audit/check_constraint_balance.py
```

[Recorded exact results](audit/constraint_balance.json).
The frozen candidate, research witnesses and current interactive UI are
unchanged by this investigation. The remaining deeper question is how the
substitution retains enough separate families to recover exactly the
original contact relation after grouping. Cycle balance explains why the
equations stay soluble, not why that stronger fixed-point condition holds.

**Subsequent investigation:** [Which distinctions survive grouping?](INFORMATION_TRANSFER.md)
answers this for the fixed twelve-component family. Five forbidden equality
patterns exactly characterize preservation of both complete contact sets;
the aligned scale operator reaches a symbolic fixed point after one grouping.
A two-depth witness separates collective phase information from the additional
distinctions needed to prevent odd parent offsets.

---
title: "A one-chair 3D matching system: request for assessment"
date: "16 September 2026"
lang: en
---

**Research proposal, not an established theorem.** Developed with substantial
AI assistance, including computation and proof drafting. No external
mathematical review or novelty determination has occurred.

## Question and proposed distinction

Can one compact solid with connected interior tile $\mathbb{R}^3$ while
every tiling by congruent copies has a **finite symmetry group**, even when
reflections are allowed? This explicitly excludes translations and
infinite-order screws; it does not require a trivial symmetry group.

The candidate uses Goodman-Strauss's familiar seven-cube chair and
eight-child hierarchy. Those are not new. The proposed distinction is to
encode the hierarchy using the chair's three distinguishable internal
rotational poses, without a second prototile. Whether this rule system
is already known is one of the questions for review.

## The finite matching system

Each of the chair's 24 exposed unit faces carries one oriented pattern
A, B, or C, occurring eight times each. Write $U$ for its arrow, $n$ for
the outward normal, and $V=n\times U$. Opposing faces allow exactly:

| Patterns | Required second arrow |
|---|---|
| A / A | $U_2=V_1$ |
| B / C or C / B | $U_2=-U_1$ |

These patterns are shorthand for physical surface profiles, not extra
assembly conditions. The complete face layout and local proof are supplied
in the [grouping note](../MOTIF_GROUPING.md).

There are 1,194 nonoverlapping geometric directed contacts in the proper
cubic frame; 44 fit. Fourteen leave a nearby face impossible to cover.
The remaining 30 equal the contact set closed under substitution.

A local recognition rule groups any valid grid tiling: six specified
mixed-sign diagonal contacts mark a central chair; otherwise the chair
occupying its notch is its parent. The one same-orientation notch case is
resolved by a forced axial neighbor. Every outer child selects the same
center, so the groups partition the tiling uniquely. A separate enumeration
reproduces the earlier 33 complete neighborhoods.

Among 6,801 possible group contacts, including odd fine-grid offsets,
exactly 44 fit. Their offsets are even, and deflation recovers exactly
the original contact rules. The grouped physical boundary need not be a
scaled copy of the small boundary; it is the matching language that recurs.

## Exact solid and the geometric step

Begin with unit cubes whose lower corners are in
$\{-1,0\}^3\setminus\{(0,0,0)\}$. On each exposed face, eight disjoint
small squares are replaced by graph patches

$$
p+\frac{u}{64}e_u+\frac{v}{64}e_v+
\frac{k}{4096}(1-u^2)(1-v^2)
\left(1+\frac{u}{5}+\frac{v}{7}\right)n,
\qquad -1\leq u,v\leq1,
$$

where $p=f+(3e_u+e_v)/16$, $f$ is the unit-face center, and the signed
depth key satisfies $1\leq |k|\leq12$. Each signed key occurs eight times.
The tile occupies the inward side of each graph. The signed volume
corrections cancel; the volume is 7 and the cube cores remain connected.
The exact [coordinate file](../audit/frozen_v1/candidate.json) specifies
all 192 ports and eight child placements. The STL is not the defining solid.

The proposed geometric argument is:

1. Local finiteness and boundary coverage force an open cap coincidence
   somewhere on each cap.
2. Polynomial continuation turns open coincidence into equality of whole
   algebraic graphs. Their five straight lines identify the base square
   and ordered tangent axes, fixing an integral relative placement.
3. Each signed key has a fixed local frame determinant; opposite keys
   have opposite determinants. A matching pair therefore has a proper
   relative orientation. A cap-contact component has one handedness.
4. Every exposed coarse face supplies a matched neighbor owning the
   adjacent grid cube. Such a component owns the entire lattice. Disjoint
   feature boxes and complementary graph sides make it fill space physically,
   excluding a second component on a different grid.

These are written geometric arguments supported by symbolic and finite
checks, not automatically verified statements about every Euclidean tiling.
The detailed [dependency audit](DEPENDENCY_AUDIT.md) and
[cap proof](../audit/README.md) expose the assumptions.

## Consequence, if those steps hold

Substituted patches contain balls of unbounded radius; compactness gives a
tiling. Unique grouping and exact recurrence force a translation period
into $\bigcap_{m\geq0}2^m\mathbb{Z}^3=\{0\}$. Open planar boundary patches
restrict symmetry linear parts to the finite cubic group, so the full
tile-preserving symmetry group is finite. Globally mirrored tilings give
the same conclusion.

## What would be most useful to assess

1. **Prior art:** is this oriented one-chair system equivalent to a known
   construction, particularly the markings in the aperiodic-pair work?
2. **Geometry:** does the open-cap/component argument actually exclude
   non-grid tilings, or does it assume the alignment it needs to prove?

The primary comparison is Goodman-Strauss, *An Aperiodic Pair of Tiles in
$E^n$ for All $n\geq3$*, European Journal of Combinatorics 20 (1999), 385–395
([author preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf)).
The brief asks for an initial assessment or reference, not a full referee report.

## Evidence and reproduction

The source archive includes the [review note](../REVIEW_NOTE.md), exact
data, independent implementations of several finite checks, certificates,
and controls. In particular, the plain chair tiles periodically, and a
specified modified decoration also has a periodic tiling; neither is a
periodic tiling of the reference decorated solid.

From the extracted archive root:

```sh
uv run --locked python strong/review/verify_package.py
```

Candidate SHA-256:
`95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54`.
The reference remains the original twelve-depth solid; an exploratory
six-depth reduction is not substituted for it.

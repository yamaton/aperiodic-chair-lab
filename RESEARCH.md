# Constructing a block that fills 3D space aperiodically

## 1. The result and its scope

An explicit SCD biprism works for **translation aperiodicity**: filling space
with one physical handedness admits no nonzero translational symmetry.
The underlying construction is known. Baake and Frettlöh describe the SCD
family and its layered structure in §1, and discuss mirror images and screw
symmetry in §3 of [their paper](https://www.math.uni-bielefeld.de/~frettloe/papers/scdart.pdf).

The calculations below establish the geometry and nonperiodicity of our
specified infinite arrangement directly. Extending the claim to **every**
possible arrangement uses the published SCD classification, rather than a new
classification proved by these scripts.

There are three different targets:

| Target | Status here |
|---|---|
| Identical connected solids fill all of R³ | Explicit construction and proof below |
| No nonzero translation can preserve the tiling | Proved for the construction; established SCD result for all allowed tilings |
| Shape forces every tiling to have no infinite-order symmetry, including screws | **Not achieved** |

The CAD files contain one handedness. A mirror-image solid is generally a
different physical part; turning the part over in 3D is a proper rotation and
is allowed. If both handednesses are available, the convex SCD block has
periodic counterexamples. This qualification belongs to the model itself.

## 2. The eight vertices

Work in units where the underlying rhombus has side length one. Set

```text
a = (1, 0, 0)
b = (1/3, 2√2/3, 0)
h = 2/5
λ = 1/3
c = λb + (0,0,h)
d = λa - (0,0,h).
```

Take the convex hull

```text
T = conv{0, a, b, a+b, c, a+c, d, b+d}.
```

Explicitly, the vertices are

```text
(0,       0,       0)
(1,       0,       0)
(1/3,     2√2/3,   0)
(4/3,     2√2/3,   0)
(1/9,     2√2/9,   2/5)
(10/9,    2√2/9,   2/5)
(1/3,     0,      -2/5)
(2/3,     2√2/3,  -2/5).
```

It is two triangular prisms joined on the rhombus with corners
`0,a,b,a+b`. The upper ridge is parallel to `a`; the lower ridge is parallel
to `b`. There are four triangular and four quadrilateral boundary faces.
It is convex, solid, and topologically a ball.

The rhombus area is `2√2/3`. Each triangular prism has half that area times
height `h`, so

```text
volume(T) = (2√2/3)(2/5) = 4√2/15.
```

The 30 mm export multiplies every coordinate by 30 and translates the lowest
point onto `z=0`. Its volume is about 10,182.34 mm³.

## 3. A complete space-filling rule

Let `Γ = Za + Zb`. Let `R` be a **clockwise** rotation around the vertical
axis by

```text
θ = arccos(1/3) ≈ 70.52877936550931 degrees.

R = [  1/3      2√2/3    0 ]
    [ -2√2/3    1/3      0 ]
    [   0        0       1 ].
```

In particular `Rb=a`. For every integer triple `(m,i,j)`, place a block at

```text
T(m,i,j) = R^m (T + i a + j b - c) + (0,0,mh).
```

All copies are related by rotations and translations. There is no scaling,
deformation, reflection, second block type, adhesive, or empty internal region.

### Direct proof that interfaces match

Use oblique horizontal coordinates `(u,v)` meaning `x = ua + vb`.
Define the period-one triangular wave

```text
f(t) = min(t/λ, (1-t)/(1-λ)),  0 ≤ t ≤ 1,
f(t+n) = f(t),                n integer.
```

Within the rhombus `0≤u,v≤1`, the solid is exactly

```text
-h f(u) ≤ z ≤ h f(v).
```

The bottom is convex and the top is concave, confirming that this is the
specified convex hull. Translating over Γ partitions the horizontal plane
into rhombi. Above each interior point of a rhombus, one tile supplies precisely
the vertical interval between these surfaces. Tile boundaries may be shared.

For the translated layer `L₀ = (T+Γ)-c`, the surfaces become

```text
bottom = -h - h f(u)
top    = -h + h f(v+λ).
```

Two simple identities do all the work:

```text
f(v+λ) + f(-v) = 1,
u-coordinate of R⁻¹x = -v-coordinate of x.
```

The bottom of `h e_z + R L₀` is therefore `-h f(-v)`, which equals the top
of `L₀` at every horizontal point. Rotation and translation give the same
identity at every successive interface. Every layer has nonnegative
thickness. Interface heights tend to plus/minus infinity with `m`, because
they differ from `mh` by a uniformly bounded amount. Thus the vertical
intervals cover each vertical line without interior overlap, proving coverage
of all R³.

**Coordinate caution:** the introductory angle formula and ridge-direction
sentence in the cited PDF do not agree with its displayed vectors. Its later
rotation calculation uses `b₁=cos φ, b₂=sin φ`. We define R explicitly,
derive `Rb=a`, and verify the seam identities independently, avoiding that
convention mismatch.

## 4. Why no translation can repeat the infinite stack

### No orientation return

If `θ/π` were rational, `ζ = exp(iθ)` would be a root of unity.
Consequently `ζ+ζ⁻¹` would be an algebraic integer. But

```text
ζ + ζ⁻¹ = 2 cos θ = 2/3,
```

and a rational algebraic integer must be an integer. Contradiction.
Thus `θ/π` is irrational.

A vertical component of a translation would move a tile to a different layer
while preserving its orientation. That would require `R^k` to be a symmetry
of the block for some nonzero integer `k`. A bounded polyhedron has a finite
rotation symmetry group, whereas `R^k` has infinite order. Impossible.

For our actual block one can identify its layer even more directly: its
upper and lower ridge directions are distinguished by the nonsymmetric
placement `λ=1/3`. A pure translation cannot change them.

### No common horizontal lattice period

A horizontal period `t` must preserve every layer's rhombus lattice, so

```text
t ∈ ⋂(m∈Z) R^m Γ.
```

Suppose such a `t` were nonzero. All `R⁻ᵐt` would be lattice points of Γ
on the circle of radius `|t|`. Irrational rotation makes these infinitely
many distinct points. A discrete lattice has only finitely many points
in any bounded set. Contradiction. Hence `t=0`.

This is an infinite proof. Searching a large patch for repeating patterns
cannot replace it.

### A subtle finite-patch trap

In the basis `(a,b)`, rotation is the exact rational matrix

```text
M = B⁻¹ R B = [[2/3, 1], [-1, 0]].
```

Any **finite** intersection of these rationally related lattices has a
nonzero sublattice. So a finite number of full layers still has horizontal
periods, even though the infinite stack has none. The bounded search in
`verification.json` illustrates their decreasing availability. It does not
claim to rule out all periods in a finite slab.

## 5. Attempts at something stronger

These are deductions and experiments from this investigation, not claims of
a new established monotile.

### Attempt A: extrude a planar hat or Spectre

For any planar tile P that tiles the plane, `P×[0,h]` admits a tiling made by
repeating the same planar layer at every integer height. That tiling has
vertical period `(0,0,h)`. Aperiodicity inside each plane is insufficient.

### Attempt B: shear or lean the extrusion

Replacing the product with

```text
{(x + z v, z): x∈P, 0≤z≤h}
```

still permits a period `(hv,h)`. Tilting a repeat direction does not
eliminate it.

### Attempt C: alternate a finite sequence of layer types

If the entire geometric stack repeats after k layers, it has a translation
or screw symmetry. Merely specifying a finite cycle of rotations therefore
does not solve strong aperiodicity.

### Attempt D: use the SCD block's sliding freedom

For this convention the interface between layers m and m+1 is invariant
along `R^m a`. Consequently one can add horizontal offsets `v_m` satisfying

```text
v_(m+1) - v_m = s_m R^m a
```

for arbitrary real `s_m`, without opening a seam.

The explorer's experimental mode sets `v_m=0` for `m≤0` and
`v_m=(√2/10)a` for `m≥1`. The changed interface still matches numerically
and by the ridge identity. This disrupts the displayed canonical screw
step, but the same block still allows `s_m=0` everywhere. Choosing a more
complicated sequence of shifts is not a proof that the **shape forces** it.
We make no all-symmetries classification of the single-fault arrangement.

### Attempt E: finite keyed registers between whole layers — an obstruction

Suppose a proposed modification only gives each layer a choice from a finite
set of registers, with translation-invariant constraints spanning a fixed
number of consecutive layers in the rotating frame. Suppose further that
every allowed register sequence has the stated geometric realization.

Such a system can be represented by a finite directed graph: a vertex
records the last few registers, and an edge records an allowed extension.
If it has a bi-infinite path, it has a directed cycle. Repeating that cycle
gives an allowed periodic register sequence.

For example, if the displacements above have `s_(m+p)=s_m`, then

```text
v_(m+p) - R^p v_m = w
```

is independent of m: subtract consecutive expressions and use the
periodicity of s. The resulting stack has the symmetry

```text
x ↦ R^p x + w + ph e_z.
```

Its nonzero vertical advance makes this an infinite-order screw motion.
Thus **finite-state, finite-range whole-layer registers alone cannot force
strong aperiodicity under these assumptions**. This does not rule out
spatially varying registers inside a layer, unbounded memory, or a coupled
two-dimensional hierarchy. It rules out a tempting but insufficient shortcut.

### The remaining research direction

A plausible stronger construction would couple a planar aperiodic hierarchy
to the interface registrations, and make that hierarchy geometrically
recoverable from every tiling. The [Spectre work](https://cs.uwaterloo.ca/~csk/spectre/)
provides a known planar shape with forced aperiodicity, but combining it with
these crossed-ridge layers is not automatic: adjacent planes rotate through
θ and their planar patterns generally fail to match.

To turn this into a new monotile would require an actual boundary geometry
and proofs of all three facts:

1. The local features admit at least one complete 3D tiling.
2. Every tiling reconstructs the intended coupled hierarchy.
3. Any translational or screw symmetry contradicts that hierarchy.

No such boundary construction or proof was obtained here. The deliverable is
the working SCD block plus the explicit calculations and rejected shortcuts,
not an asserted solution to the stronger problem.

## 6. What the computations establish

`uv run python verify.py` checks:

- The triangle mesh closes, each edge occurs twice, and outward signed
  volume agrees with the analytic value.
- Exact symbolic `B⁻¹RB`, `RᵀR=I`, `det R=1`, and `Rb=a`.
- Matching surfaces at 20,000 points on each of 17 interfaces, including
  negative-index layers; a separate fault-interface check.
- Convex intersection via linear programming for every pair in a 175-block
  patch whose axis-aligned boxes could have a positive-volume intersection.
  The optimization maximizes the radius of a ball lying inside both solids.
- Coverage of 12,000 interior points using independent convex-hull
  halfspace membership, requiring exactly one covering tile each.
- A deliberately wrong turn breaks the surface fit.
- Changing the block to `cos θ=1/2` produces a six-layer vertical period.

Tolerance is used only in numerical verification and export. The arguments
in §§3–4 use the exact irrational coordinates. The tests do not establish
absence of arbitrary alternative tilings, manufacturing tolerances, or
strong aperiodicity.

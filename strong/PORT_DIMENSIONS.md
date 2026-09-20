# Port dimensions with movable anchors

*19 September 2026. Exact design-family analysis and a reproducible larger
candidate. Neither frozen snapshot nor the tutorial/cover has been replaced.*

Subsequent presentation updates incorporate the study into the tutorial and
provide a [Blender cover at the larger witness's actual proportions](../docs/figures/aperiodic-chair-cover-relocated.md).
The two frozen mathematical snapshots remain unchanged.

**Result.** The original anchor coordinates are not part of the matching
information. Moving the eight ports coherently permits a strictly separated
candidate with **12 times the recorded width and 256 times its depth**, while
preserving the contact rules. In the common eightfold face-orbit family, with
the same 1:2 right-triangle shape and orientation convention, the supremum
width is **1/4**, sixteen times the recorded 1/64. Strictly positive clearances
are possible at every width below that supremum.

The earlier 1/16 width bound applies only to the old anchors. It is not a
design-wide limit. The depth bounds below are **sufficient conditions** for
separated curved modifications and the existing registration proof; they
are not necessary limits on all possible solids. This distinction matters
even after the anchors are allowed to move.

![Actual face layouts and sufficient width/depth regions](artifacts/port-dimensions.svg)

## 1. Which parameters carry information?

Let a carrier cube have side length 1, and write a port as

    f + a U + b V + w u U + w v V + k delta psi(u,v) N.

Here f is the unit face center, U,V are the existing ordered signed tangent
axes, and N is outward. The triangle is still
`(-1,-1), (1,-1), (-1,0)`, with
`psi = -27(u+1)(v+1)(u+2v+1)/4`. The recorded values are
`a=3/16, b=1/16, w=1/64, delta=1/4096`.

- **w** is the short leg, not the total footprint width. The long leg is
  `2w`, the hypotenuse is `sqrt(5)w`, and the area is `w²`.
- **delta** is the lower depth magnitude; with keys ±1,±2 the maximum depth
  is `h=2 delta`. The plotted vertical axis is h.
- **a,b** place the old frame anchor relative to f. The physical centroid is
  `f+(a-w/3)U+(b-2w/3)V`. The anchor can lie outside the triangle; its sign
  and its distance from f have no independent matching-rule significance.

The three-line algebraic rigidity argument in
[PORT_SIMPLIFICATION.md](PORT_SIMPLIFICATION.md) works for every `w>0` and
every nonzero height. For a matching pair it recovers
`R U_B=U_A`, `R V_B=V_A`, `R N_B=-N_A`, and opposite signed depths.
Consequently, with the **same a,b on every port**,

    t = p_A - R p_B
      = f_A - R f_B + a(U_A-R U_B) + b(V_A-R V_B)
      = f_A - R f_B.

Both placement parameters cancel exactly. There is no requirement that a,b
equal the recorded fractions, or even be rational, in this identity.
Uniform w also cancels when corresponding triangle vertices are matched.

Thus every full-frame neighbor pose is unchanged by these parameter moves.
Disjoint supports inside their unit faces still identify the same eight
ordered port slots. Their signed-key comparisons, and therefore the fine
and full macro contact predicates, are unchanged. The two positive depth
magnitudes need only remain distinct; the ratio 1:2 is convenient, not forced.
Collapsing the levels or making either zero would change these premises.

There is more freedom than a common a,b. Since only opposite keys of the
**same magnitude** can match, the low and high levels may have separate
offsets `(a_low,b_low)` and `(a_high,b_high)`. Each offset still cancels within
a matching pair. As an explicit check, moving only high ports in the larger
witness from `a=-1/4` to `a=-31/128` leaves all 13,312 frame maps unchanged
and all 672 actual same-face triangle pairs strictly separated. Their
nearest-edge distances increase by 1/128, so the depth certificate remains
valid. This exhibits four position parameters, not just two. Fully independent
per-port placement would need further compatibility conditions; the
common-offset restriction is not being treated as a universal necessity.

This is a transfer of the existing contact-language result, not an assertion
that the geometric outline of a parent is a scaled copy of the child.

## 2. Optimizing width includes moving the ports

Keep eight supports per face, related by the full square symmetry group D4,
with the existing ordered-axis convention. Allow arbitrary common a,b.

There is a short packing argument that makes this optimization exact.
A convex triangle that straddles a reflection axis overlaps the interior of
its reflected image: an interior point on the axis belongs to both interiors.
Therefore eight disjoint orbit triangles must each lie inside one of the
eight 45-degree wedges bounded by the four face reflection axes.

Map that wedge to `0 <= y <= x <= 1/2`. There are eight possible relative
orientations of the triangle. For any such orientation, let its normalized
vertices be `(dx_i,dy_i)`, and its anchor be `(A,B)`. Containment requires

    B >= -w min(dy_i),
    A >= B - w min(dx_i-dy_i),
    A + w max(dx_i) <= 1/2.

The first two inequalities give the least possible A and B; substitution
into the third gives an exact upper bound for that orientation, attained
by the corresponding closed triangle. The eight bounds are six occurrences
of 1/6 and two of 1/4. The checker records every case using rational arithmetic.

Hence `w <= 1/4` in this family. At the maximum, some zero-height triangle
edges touch other supports or cube edges. We use a **strictly separated
family** instead:

    0 < w < 1/4,
    a = -1/4,
    b = 1/8 + w/2.

Its reference triangle lies in the wedge `x <= -y <= 0`. Put
`epsilon=1/8-w/2 > 0`. Throughout that triangle,

    y >= epsilon,
    x+y <= -epsilon,
    distance to the nearest outer face edge = 1/4+w u >= 1/4-w > 0.

The eight images therefore have strict separation from each other and the
outer face edges. This attains widths arbitrarily close to 1/4 without
relying on touching seams. The anchor sites are also distinct for w<1/4.

For comparison, the old `a=3/16,b=1/16` makes a pair of triangles meet along
their bases at `w=1/16` and overlap immediately above it. Shrinking a square
support to a triangle did not remove that particular bottleneck. Relocation
does. Neither 1/16 nor 1/4 is claimed as an upper bound for independently
oriented/positioned ports, a different aspect ratio, fewer ports, or a
different matching construction.

Even allowing separate offsets for the two depth levels does not remove
this particular width supremum when both levels keep a common w. Sixteen
actual faces have seven low ports and one high port; the other eight have
six low and two high. On a seven-low face, if the hypothetical full low-port
orbit straddled a reflection axis, a triangle and its reflection would
overlap. Rotating that pair by 180 degrees gives a second pair with disjoint
port indices (the scalene triangle has no symmetry identifying these frames).
Removing one low slot cannot remove both offending pairs. Hence the low
triangle must still fit a reflection wedge, and w<=1/4 follows. This does
not extend the bound to arbitrary independent per-port placements.

## 3. Depth is controlled by the curved profile, not just its box

At tangent point q on a port, let d(q) be the distance to the nearest outer
edge of its unit face. Enclose the actual modification in the curved zone

    |s| <= h psi(q).

This deliberately encloses both signs and both depth levels. The conditions

    h < 1/2,                 h psi(q) < d(q) at every support point

are sufficient to separate zones on different grid faces:

- Different coplanar unit faces have disjoint interior footprints.
- Parallel grid planes are at least 1 apart; the combined reach is at most 2h.
- For perpendicular planes, a hypothetical common point has distances
  `|s_A|,|s_B|` from the two planes. The tangent distance to the other integer
  plane is at least the distance to the nearest edge of the first unit face.
  The two zone inequalities would give both `|s_A|<|s_B|` and
  `|s_B|<|s_A|`, a contradiction.

Same-face separation comes from Section 2. This covers the infinite periodic
family geometrically; it does not extrapolate from a finite sample of caps.
The zones need not be replaced by mutually disjoint rectangular boxes.

For each fixed u, completing a square gives

    P(u) = max_v psi(u,v) = 27(u+1)(1-u)^2/32,
    P(u)-psi(u,v) = 27(u+1)(u+4v+3)^2/32 >= 0.

The maximum occurs at `v=-(u+3)/4`, inside the triangle. In our relocated
family `d(q)=1/4+w u`, so the sufficient depth envelope is

    h < D(w) = min_{-1<u<1} (1/4+w u)/P(u).

This is an algebraic one-variable minimization, not a sampling rule. Its
interior stationary point solves

    2w u² + (w+3/4)u + (w+1/4) = 0.

At `w=3/16` the minimum is

    D(3/16) = 59/672 + 19 sqrt(57)/2016
            = 0.158951812634...

As width approaches 1/4, D(w) approaches **2/27 ≈ 0.074074**.
In particular, a shrinking clearance at a triangle vertex or edge does not
force depth to zero: the bubble height vanishes there as well. A constant
height box misses this fact.

With the original anchors and `0<w<=1/16`, the analogous nearest-edge formula
is `5/16-w u`, giving the sufficient envelope
`min (5/16-w u)/P(u)`. At the recorded w=1/64 it is approximately **0.317594**,
compared with the recorded h=1/2048 ≈ 0.000488281. Even with fixed anchors the
recorded depth is far below this geometric sufficient bound.

These envelopes do **not** optimize a,b for depth at each width. They also
ignore the actual handedness and low/high assignment by enclosing all ports
in two-sided maximum-depth zones. Overlap of those enclosing zones would
not itself prove collision of actual surfaces. Exact necessary depth bounds,
and a globally optimal width/depth tradeoff with movable anchors, remain open.

## 4. A simultaneous large-width, large-depth witness

Use `a=-1/4, b=7/32, w=3/16, delta=1/16`, keeping all existing signed keys.

| Quantity, in carrier-cube side units | Recorded candidate | Relocated witness |
|---|---:|---:|
| Short triangle leg w | 1/64 | 3/16 (12×) |
| Long triangle leg 2w | 1/32 | 3/8 (12×) |
| Lower depth delta | 1/4096 | 1/16 (256×) |
| Higher depth h | 1/2048 | 1/8 (256×) |
| Total support area on one face, 8w² | 1/512 | 9/32 (144×) |
| Minimum distance to an outer face edge | 19/64 | 1/16 |

For this witness,

    d-h psi >= 1/4 + 3u/16 - P(u)/8 >= 5/256 > 0.

The second inequality has an exact certificate: divide [-1,1] into four
equal intervals and express the cubic in the degree-three Bernstein basis
on each. All sixteen coefficients are positive, and the smallest is 5/256.
The basis functions are nonnegative and sum to one, so this proves the bound
on **every** point of the intervals. All coefficients are in the evidence JSON.

The old symmetric boxes cannot certify this witness: h=1/8 exceeds the
minimum tangential edge margin 1/16. The curved zones do certify it.

The normal reach is below 1/4, so the middle-half core of every carrier cube
remains intact, including a radius-1/4 open ball. Caps lie on actual exposed
faces and their disjoint zones remain in the two adjacent cubes; they remain
genuine boundary graphs with two sides. Connected interior can also be
checked without guessing paths around pockets. Thicken each enclosing zone
from h=1/8 to H=9/64: since psi<=1, the clearance bound remains at least
`5/256-(H-h)=1/256 > 0`. Inside each such zone, use an increasing piecewise
linear map of the normal coordinate fixing `-H psi` and `H psi` and sending
0 to the actual signed cap height. Outside the zones use the identity.
The maps glue continuously where psi vanishes, and the zones are disjoint.
They define an ambient homeomorphism taking the coarse chair to the new
solid, so its interior stays connected.

For component exhaustion, the earlier fixed inset 1/64 was merely a choice.
Use **rho=1/7** for this witness:

    h=1/8 < rho=1/7,
    3 rho²=3/49 < 1/16=(1/4)².

Thus the same retained-ball clamping argument excludes additional grid
components. This is the adapted argument attributed in
[the geometric scrutiny, Section 8a](review/GEOMETRIC_GRID_SCRUTINY.md#8a-shorter-component-exhaustion-route-from-the-chair44-comparison),
with new constants. The original literal condition h<1/64 is not essential.
For the broader plotted family, the separated-zone physical-coverage route
in Sections 7–8 of that report remains available when this particular
clamping estimate does not apply.

The signed volume changes still cancel because the signed keys sum to zero
and every support has the same integral `9w²/20`. The volume remains 7.
The finite hierarchy and its 44 fine / 44 full macro contact language
transfer through the unchanged frame poses and disjoint local interfaces.
The all-isometries and global-solid deductions are written mathematics;
this study is not a new Lean theorem or an externally reviewed proof.

## 5. Reproduction, evidence, and what was not adopted

```sh
uv run --locked python strong/audit/investigate_port_dimensions.py
```

The script checks all eight packing orientations, all 28 same-face triangle
pairs of the larger witness, 13,312 opposite-key frame maps (1,410 distinct
poses), actual corresponding triangle vertices, 9,216 signed-frame layout
memberships, and the exact polynomial clearance certificate. Each relocated
frame map has **exactly the same translation** as in the recorded candidate.
Its result is [audit/port_dimensions.json](audit/port_dimensions.json).
The figure's smooth curves evaluate the algebraic stationary roots; the
universal inequalities and the witness certificate are separate from that
floating-point display.

The existing standalone checker `node strong/audit/crosscheck_triangular_ports.cjs`
replays the reference triangular fine/full-macro atlases. The new script does
not rerun those atlases with a center-only representation: the parameter-free
frame-map identity is what transfers their predicates. This matters at some
limiting packings, where different frames can have the same anchor even though
their triangle interiors differ. The strict witness here has distinct anchors.

The source hash is preserved in the evidence. `frozen_v1/` and `triangular_v1/`
retain their recorded designs. The dimension study initially left presentation
artifacts unchanged; subsequent updates teach the larger witness and render
it with a separate wedge-based face triangulation. Mesh code that cuts out
one enclosing square per port is insufficient at these dimensions: disjoint
triangular supports do not imply disjoint enclosing squares. The earlier
cover images and their receipts remain available.
These dimensions describe an exact mathematical candidate, not printer
tolerances, clearance fits, assembly paths, or a certified manufactured block.

---
title: "How one shape can enforce order without repetition"
subtitle: "An undergraduate guide to aperiodic chairs, local rules, and physical realization"
date: "16 September 2026"
lang: en
---

# Before we begin

Imagine a box of identical blocks. You can translate and rotate them, and
you want to fill three-dimensional space without gaps or overlapping interiors.
Could their shape make a repeating arrangement impossible?

This tutorial explains the mechanism behind one approach: a seven-cube chair
with carefully designed surface features. Its central idea is that local
contacts can force a hierarchy extending to every length scale.

The route is simple to state: surface features restrict neighboring blocks;
those restrictions force groups of eight; the groups obey the same rules
again. A repeating arrangement would have to repeat consistently through
every level of this hierarchy. We will see why that is impossible.

**Audience.** Undergraduate students familiar with vectors, matrices, and
elementary calculus. No previous tiling theory or abstract algebra is needed.
The physics sections use basic energy, entropy, and Fourier analysis.

**Reading route.** Sections 1–7 explain the mathematical mechanism;
Sections 8–10 connect it to physics and printing. Section 11 gives the
verification status and further reading. Exercises with answers follow.

**Status matters.** For our curved chair, the proof is most complete in a
model that restricts blocks to a cubic grid. Showing that freely moving
blocks must obey that model is a separate argument still requiring review.
A related construction, Chair44, uses different surface features and has a
more complete computer-checked proof. Section 11 explains that comparison.
The printable replacement interfaces described here remain proposals.

# 1. Aperiodic means more than an irregular-looking arrangement

A **tiling** covers all of space with copies of a shape, allowing their
boundaries to touch but forbidding interior overlap. A **packing** only
requires no interior overlap; it may leave gaps.

For a tiling $T$, a vector $v$ is a **translation period** if shifting every
tile by $v$ leaves exactly the same collection of tiles:

$$T+v=T.$$

The zero vector always works. A tiling is translation-nonperiodic if no
nonzero vector works. Here “no period” excludes even repetition in just one
direction, not merely a full three-dimensional crystal lattice.

An **aperiodic tile** must satisfy two different requirements:

1. At least one infinite tiling exists.
2. Every allowed infinite tiling has no nonzero translation period.

Even constructing one infinite nonrepeating tiling would not establish the
second requirement: the same shape might also allow a repeating arrangement.
Ordinary cubes, for example, admit the familiar periodic cubic tiling and
therefore cannot be an aperiodic tile, regardless of their other arrangements.

In three dimensions there is another issue. A **screw motion** rotates around
an axis and translates along it. Repeating the motion can generate an
infinite symmetry even when a pure translation is unavailable. Our earlier
Schmitt–Conway–Danzer construction illustrates this distinction; see the
[SCD research note](../RESEARCH.md).

Our stronger target is explicit:

> One solid tiles space, and every tiling by that solid has a finite symmetry
> group, even when reflected copies are allowed.

A symmetry group is simply the collection of rigid motions preserving the
tiling. A finite group permits a few rotations, but excludes nonzero
translations and infinite-order screws. Terminology for “strongly aperiodic”
varies, so this explicit property is more useful than the label alone.

We will first tackle translations, then return to screw motions in Section 6.

# 2. Meet the chair

Start with a $2\times2\times2$ cube assembled from eight unit cubes. Remove
one corner cube. The remaining seven cubes form the **three-dimensional
chair**. We call this coarse shape the **carrier**; later we modify its surface.

The carrier has volume 7. Its boundary has 24 unit-square panels, including
the three panels facing the missing corner, or **notch**.

Eight suitably oriented chairs fit together to form a chair with twice the
linear dimensions. The volume check is

$$8\times7=7\times2^3=56.$$

This is a useful consistency check, but equal volume alone does not prove
that the pieces fit. Their positions and orientations must also be checked.

![The modified chair, an exploded eight-chair group, and matching versus mismatching surface sections.](../strong/artifacts/recut-chair-placements.png)

*Figure 1. Existing project illustration. Body colors distinguish identical
copies. Surface features are enlarged by factors of 3 in width and 12 in
depth; the cross-sections also exaggerate the vertical scale. The image is
an approximate rendering, not a certificate for the exact curved solid.*

Repeating the eight-child construction gives patches containing
$8,64,512,\ldots$ chairs. This is called a **substitution**: replace a larger
chair by eight smaller ones. Equivalently, enlarge a chair by a factor of
two and fill it with eight chairs of the original size. A **level-one group**
contains eight original chairs; a level-two group contains eight such
groups, or 64 original chairs.

However, the undecorated chair also admits periodic tilings. Its ability
to participate in a hierarchy does not force every arrangement to have one.
The surface features must supply that missing constraint.

# 3. Surfaces can carry local information

Think of a jigsaw puzzle. A tab and a matching pocket allow one contact;
incompatible profiles obstruct another. Our chair uses small surface features,
called **ports**, to encode allowed neighbors. A **matching rule** specifies
which contacts are allowed.

For Sections 3–5, imagine placing the chairs on three-dimensional graph
paper: their carrier cubes occupy cells of one common cubic lattice. This
is the **grid model**. A **legal tiling** in this model covers every cell
exactly once and satisfies every matching rule. We temporarily assume this
alignment so that we can understand the hierarchy; Section 7 explains why
justifying the alignment for freely moving solids is a separate challenge.

The current curved design has eight ports on each of its 24 panels: 192 ports
in total. Signed labels $\pm1,\ldots,\pm12$ specify complementary protrusions
and recesses, with the magnitude controlling depth. Each port is asymmetric,
so its shape also encodes an orientation within the panel.

The complete arrangement can be summarized by three panel patterns, A, B,
and C, together with an arrow on each panel. These are descriptions of one
block's geometry, not three different tile species.

In words, A meets A with a specified quarter-turn between their arrows;
B meets C with their arrows pointing oppositely. The arrow records a
direction along the face, much as an arrow printed on a square card does.

To make “quarter-turn” precise, let $n$ point straight out of the first
panel and let $U$ be its unit arrow. The cross product $V=n\times U$ gives
a perpendicular arrow lying in the same panel. For example, if $n$ points
along positive $z$ and $U$ along positive $x$, then $V$ points along positive
$y$. Compare both panels' arrows in the same three-dimensional coordinate
system, even though their outward normals point oppositely.

With subscripts 1 and 2 identifying the two panels, the rules are:

| First pattern | Second pattern | Required arrow on the second panel |
|---|---|---|
| A | A | $U_2=V_1$ |
| B | C | $U_2=-U_1$ |
| C | B | $U_2=-U_1$ |

All other pattern pairings are forbidden. In particular, C cannot meet C.
The arrows are essential: forgetting them changes the rules.

![The chair's 24 unit-face patterns and their arrows.](../strong/artifacts/motif-face-layout.png)

*Figure 2. The complete face layout. You do not need to memorize it. Its role
is to specify the finite input from which contacts and grouping are checked.*

We can now hold one chair fixed and list every grid-aligned way a second
chair could touch it across a panel without overlapping it. Using rotations
that preserve the cubic grid, there are 1,194 such candidate placements.
Only 44 satisfy all interface rules. Fourteen of those leave a nearby face
with no possible compatible neighbor, so they cannot occur in a complete
legal tiling. That leaves 30 contacts supporting the hierarchy.

The exact counts are useful for checking the calculation; the next argument
does not require memorizing them. They count relative placements, not
different shapes or infinite tilings. See the
[local grouping report](../strong/MOTIF_GROUPING.md) for the full enumeration.

**Lesson:** pairwise compatibility need not imply compatibility with a whole
neighborhood. A contact can fit in isolation and still prevent space from
being filled around it.

# 4. The crucial step: every chair has a unique parent

To force a hierarchy, we need to recover the eight-chair groups from an
arbitrary legal tiling. We cannot assume that someone assembled it using
our preferred substitution.

Imagine receiving a finished tiling with all assembly instructions lost.
Our task is to identify its groups using only the neighbors we can see.
Each group is named by one distinguished member, its **central child**.
The rule assigns every chair to one such member, which we call its parent.

The local recognition rule has two cases:

1. If a chair has one of six particular oriented diagonal neighbors, it
   identifies itself as the central child of an eight-chair group.
2. Otherwise, it selects the chair occupying its notch as that central child.

The six special contacts are **triggers**. Each triggers a chain of forced
neighbors: an uncovered face has only one possible compatible occupant,
which exposes another forced choice, and so on.

Most of the notch cases are reciprocal: viewed from the notch owner's
coordinates, the original chair is a trigger, identifying that owner as a
center. One exceptional orientation takes an additional local check.

> **Optional detail: the exceptional case.** Suppose the original chair has
> no trigger, and its notch owner has the same orientation. One neighboring
> face has three candidate occupants. One would give the original chair a
> trigger, contradicting our assumption. Another would create a forbidden
> C/C contact with the notch owner. The remaining occupant gives the notch
> owner a trigger. Thus the notch owner is a center in this case too.

The decisive check is that all eight children select the same central chair.
Consequently every chair belongs to exactly one group. Here “parent” names
the central child used to identify a group; it is not an additional ninth tile.

This is **recognizability**: the larger structure can be read from the smaller
one. The chair-recognition mechanism has a predecessor in Goodman-Strauss's
1999 construction; our [markings comparison](../strong/review/GOODMAN_STRAUSS_COMPARISON.md)
records the attribution and differences in the matching systems.

Treat each group as a single effective chair, then shrink distances by a
factor of two so that these chairs have the original size. This operation
is **deflation**. A separate result, called contact recurrence, says that
the effective chairs obey the same matching rules as the original ones.
We may therefore group and deflate again.

There is a geometric subtlety: the **coarse carrier** of a group is a doubled
chair. Its finely patterned outer surface need not be an enlarged copy of
the original curved surface. It is the effective matching rules that recur.

At this point we have two essential ingredients: the groups are uniquely
recognizable, and grouping produces another legal tiling. These let us
test what would happen to a repeating pattern under deflation.

# 5. A short proof that translation periods are impossible

We can now see the central argument without a large coordinate table.
Work in the legal integer-grid model, with lengths measured in unit-cube
edges. The notation $\mathbb Z^3$ means triples of integers, such as
$(12,4,0)$. Use the inward corner of a chair's notch as its reference point;
a group's origin is that point on its central child. Because each chair's
reference point lies on the grid, a period
that carries chairs to chairs must also have integer coordinates.
Suppose $v\in\mathbb Z^3$ is such a period.

**Step 1: translation preserves the recognized groups.** The parent rule
depends only on relative positions and orientations. Translating the tiling
translates its parents. Uniqueness prevents the translation from choosing
a different grouping.

**Step 2: the period has even coordinates.** First picture a row of unit
intervals grouped into pairs. Once the pair starts are at $0,2,4,\ldots$,
any shift preserving those pairs has even length. A shift by one unit
would send a pair start to its midpoint.

The three-dimensional argument uses a separately proved alignment result:
all group origins have the same coordinate remainders modulo 2. This result
comes from the contact rules and coverage; it does not follow from group
size alone. For example, origins with remainders $(1,0,1)$ have odd $x$ and
$z$ coordinates and even $y$ coordinates. Any difference between two such
origins has three even coordinates.

If $o$ is one group origin, we write this common **parity class** as

$$o+2\mathbb Z^3.$$

Here $2\mathbb Z^3$ means all integer vectors with even coordinates. Every
group origin lies in this class, though some points in the class need not
be group origins. If $c$ is an actual group origin, Step 1 says that $c+v$
is another. Their difference $v$ therefore equals $2w$ for an integer vector $w$.

**Step 3: deflation halves the period.** After shrinking the grouped tiling,
$w=v/2$ is a period of another legal tiling.

**Step 4: repeat.** Every deflated tiling is legal, so

$$v\in2^m\mathbb Z^3\qquad\text{for every integer }m\geq0.$$

In words, each coordinate of the original period must be divisible by 2,
then by 4, then by 8, and so on without end. Any nonzero integer eventually
fails this test. Therefore $v=0$.

For a concrete example, an alleged period $(12,4,0)$ would give $(6,2,0)$
after one deflation and $(3,1,0)$ after two. The latter has odd coordinates,
contradicting Step 2 for that legal tiling.

Notice what we did **not** assume: the original tiling need not reproduce
itself under scaling. Each deflation may give a different tiling. Closure
of the class of legal tilings under deflation is sufficient.

This argument has been checked using **Lean**, a proof assistant: software
that checks each inference against precise definitions and logical rules.
The checked statement concerns the integer-grid model. See
[translation exclusion](../formal/TRANSLATION_EXCLUSION.md).

# 6. Why this can also rule out screw symmetries

To return to the screw-motion question, separate a rigid motion into an
orientation change followed by a shift:

$$g(x)=Rx+t,$$

The matrix $R$ describes a rotation or reflection; mathematically, it is
an **orthogonal matrix**, which preserves lengths and angles. The vector
$t$ describes the shift.

Suppose the geometry forces all symmetries to permute three common
perpendicular grid axes. There are six ways to permute $x,y,z$, and two
choices of direction for each axis. This gives $6\times2^3=48$ matrices.
Half are rotations; the other half reverse handedness, as a mirror does.
The project's handedness argument excludes the latter as symmetries of
a tiling, leaving 24 possibilities. Even the bound of 48 would suffice
to establish that the symmetry group is finite.

If two symmetries have the same matrix $R$, composing one with the inverse
of the other gives a pure translation: doing the first motion and then
undoing the second cancels their orientation changes. A composition of
symmetries still preserves the tiling. Since a nonzero translation cannot
do so, the two motions must have been identical. Thus there is at most
one symmetry per matrix, giving the bound of 24 when reflections are excluded.

For a concrete screw-motion example, rotate by $90^\circ$ and move one unit
along the rotation axis. Four repetitions restore the original orientation
but move four units along the axis: a forbidden translation. The same
argument works whenever some finite number of repetitions cancels the rotation.

Both premises matter: we need translation exclusion **and** geometric
control of the possible orientation changes. Translation exclusion alone does not rule
out an irrational-angle screw. For our curved chair, this full physical
conclusion still depends on the geometric argument discussed next; it is
not part of our completed Lean grid theorem.

# 7. Two obligations that the short proof does not settle

The previous sections showed what follows **if** we have a legal grid
tiling. To finish a theorem about freely placed physical blocks, we must
justify that assumption and show that tilings exist in the first place.

## 7.1 Why should real blocks respect an integer grid?

An arbitrary block in space can slide, tilt, or touch only part of another
block. A proof that starts by placing everything on a cubic grid has already
assumed something substantial.

Our proposed bridge uses the exact asymmetric curved ports:

1. Space-filling coverage forces an open patch of a port to coincide with
   another tile's boundary. An open patch means a small two-dimensional
   region of surface, rather than just an edge or point.
2. The polynomial surface is designed so that such coincidence determines
   its center, its two tangent directions, and its signed depth.
3. Those constraints fix a discrete relative placement of the two chairs.
4. Contact propagation and coverage then force a common grid for the entire
   tiling, including ruling out independently shifted components.

Why use a carefully chosen curved surface? A flat patch can slide against
another flat patch without fixing an in-plane position. Our asymmetric
curved patch is intended to identify a much more specific position and
orientation, like a three-dimensional key fitting its lock.

The detailed rigidity argument uses polynomial equations. Its guiding fact
is that two polynomial expressions which agree throughout an open region
must be identical. Applying that fact to moved surface patches takes
additional geometric work; it is not a general claim about arbitrary curves.
Approximate agreement between printed or triangulated surfaces does not
give the exact identity required by this argument.

The proof details and remaining review scope are in the
[geometric scrutiny](../strong/review/GEOMETRIC_GRID_SCRUTINY.md).

Tsiokos's Chair44 realization uses square pyramids instead. Its proof must
handle their extra symmetries and exclude additional off-grid placements.
Our [comparison](../strong/review/CHAIR44_PROOF_COMPARISON.md) explains the
different routes to the same discrete contact system.

## 7.2 Does even one infinite tiling exist?

If no tiling existed, the statement “every tiling has no period” would be
vacuously true. We need an independent existence argument.

Repeated substitution produces legal finite patches with larger and larger
interior regions. Recenter those regions around the origin and imagine
looking through a small fixed window. Only finitely many grid patterns
can appear in that window. Among infinitely many patches, at least one
of those patterns must occur infinitely often. Keep just those patches.

Now enlarge the window and select an infinite subcollection again. The
patches retained at this step still agree on the first window. Repeating
the procedure gives consistent patterns on successively larger windows.

This limiting selection defines an infinite tiling: each fixed window is
eventually covered consistently, and the local matching rules survive.
Mathematicians call this a **compactness argument**.

The expanding interior is essential. A growing collection confined to a
thin slab would not establish a tiling of all three-dimensional space.
The written estimates are in the [existence audit](../strong/review/DEPENDENCY_AUDIT.md#d-existence-explicit-expanding-balls-and-a-compactness-argument).
Existence is not yet formalized in our own Lean development.

# 8. What a physicist can learn from the hierarchy

We now change the question. So far a contact has been either exactly legal
or illegal. Real objects have manufacturing errors, may deform under force,
and need some process to put them together. Which aspects of the ideal
hierarchy remain useful under those conditions?

## 8.1 A concrete example of coarse-graining

**Coarse-graining** means replacing a group of small objects by one effective
object, keeping information relevant at a larger scale. Here eight chairs
become one effective chair with twice the linear size and eight times the
volume, and the same contact rules reappear.

In statistical physics, repeatedly coarse-graining and then rescaling to
the original size is part of **real-space renormalization**. Our hierarchy
provides a concrete geometric example of that procedure.

It is not yet a renormalization calculation for a material. We have not
specified an energy for configurations or shown how temperature and
interaction strengths transform. The proved recurrence concerns legal
configurations. An energy model is the next ingredient.

## 8.2 Allowed configurations, equilibrium, and assembly are different

Imagine softening the rules: a wrong contact is possible, but costs an
energy $\epsilon>0$. Two wrong contacts cost $2\epsilon$, three cost
$3\epsilon$, and so on. For this simple model, the total energy is

$$H=\epsilon\sum_\alpha m_\alpha,\qquad m_\alpha\in\{0,1\}.$$

Here $H$ denotes energy, $\alpha$ labels a tested local constraint, and
$m_\alpha$ is 1 when that constraint is violated and 0 otherwise. The sum
counts violations.
This is a proposed soft-constraint model, not a measured interaction between
our chairs. A continuous model of physical blocks would additionally need
excluded volume, positional and orientational interactions, and a dynamics.

The tiling question concerns zero violations. At nonzero temperature the
equilibrium question concerns free energy, $F=E-TS$, where $E$ is internal
energy, $T$ is temperature, and $S$ is entropy. (Here $T$ denotes temperature,
not the tiling used in Section 1.) Entropy accounts for the number of
accessible arrangements: many defective states can compete with fewer
perfectly ordered ones. The assembly question asks whether a physical
process can reach the ordered states within the available time.

There are related models in which directional bonding produces one-component
icosahedral quasicrystals in simulations. They illustrate the physical program,
but do not establish self-assembly for our chair. [Noya and Doye](https://arxiv.org/abs/2407.17212)

## 8.3 Nearly legal periodic states can have a small energy cost

Does excluding every perfectly legal periodic arrangement mean that periodic
arrangements must cost a substantial energy per particle? In a model with
soft penalties, the answer can be no.

Continue with discrete states on a lattice. Assume each constraint involves
only nearby sites and each violation has a bounded cost. Take a large legal
region of side $L$, measured in lattice spacings, and repeat its state
pattern periodically, like repeating a picture on wallpaper.
The repeated configuration may violate rules near the seams. The number
of affected constraints grows like $L^2$, while the number of sites grows
like $L^3$. Hence an upper bound on excess energy per site scales as

$$\frac{\Delta E}{N}\leq\frac{C}{L}\quad\text{for sufficiently large }L.$$

Here $N$ is the number of sites per repeated cell, $\Delta E$ is its extra
energy from violations, and $C$ is independent of $L$. Doubling the cell
size multiplies its boundary area by four and its volume by eight, so the
estimated cost per site halves. This is a boundary-to-volume argument.

Thus periodic approximations can have arbitrarily small violation density
without any periodic state being perfectly legal. This construction applies
to the soft discrete model; it does not produce a nonoverlapping periodic
packing of rigid chairs with hard geometric constraints.

This distinction suggests a physical question worth measuring: how much
ordering survives at a specified defect density?

## 8.4 Defects can be studied at successive scales

Introduce a wrong local contact and apply parent recognition wherever it
remains unambiguous. Repeat at the next level. Record the fraction of a
sample that can still be assigned consistent parents at each level.

If recognition remains reliable through $m$ levels, the corresponding
linear scale is proportional to $2^m a$, where $a$ is the unit-cube edge.
This provides an operational measure of hierarchical order. Whether errors
remain localized or spread across levels is a research question, not a
consequence of the ideal aperiodicity proof.

# 9. Diffraction: what would we actually observe?

One way to probe order is to scatter waves from a sample. Waves scattered
from different positions arrive with different phases. At some scattering
directions they reinforce one another, producing peaks in intensity;
at others they largely cancel. This is the basic idea of diffraction.

Nonperiodic does not mean random. Chair substitution point patterns have
established connections to sharp **Bragg peaks**, rather than only a diffuse
pattern. In the infinite ideal limit a spectrum consisting entirely of
such sharp peaks is called **pure point diffraction**.
[Lee and Moody](https://arxiv.org/abs/math/0002019)

For a sample with $N$ idealized point scatterers at positions $r_j$, we can
sum the scattered waves and take the squared magnitude. Dividing by $N$
gives a convenient intensity per scatterer, often written as a structure
factor:

$$S(q)=\frac1N\left|\sum_{j=1}^N b_j e^{i q\cdot r_j}\right|^2,$$

Here $q$ is the change in wavevector between incoming and outgoing waves,
and $b_j$ is the scattering amplitude of marker $j$. The factor
$e^{i q\cdot r_j}$ records its phase. If all amplitudes equal 1 and all
phases agree, the sum is $N$, so $S(q)=N$: a strong peak. If phases differ,
the waves can cancel. A finite sample broadens peaks; it cannot show
infinitely sharp peaks or certify an infinite aperiodicity property.

There is a crucial experimental detail. If homogeneous blocks of identical
density fill space perfectly, with no density change at their interfaces,
their combined bulk density is constant. A density-sensitive probe cannot
see the abstract partition into chairs. A finite sample still scatters from
its outer boundary, but that does not reveal the internal tiling.

To observe the order, use physical contrast: for example, an identical
embedded marker at a fixed position in each chair, an interface coating, or
an orientation-dependent material response. Then calculate the structure
factor for that actual observable. The intensity pattern depends on the
chosen decoration; some peaks may vanish.

The chair's repeated factor of two points toward **limit-periodic** order:
roughly, an arrangement described through periodic patterns on successively
larger scales, without one period common to the entire limiting pattern.
For the chair hierarchy, the relevant scales double repeatedly. It should not
be identified automatically with the familiar fivefold or icosahedral
quasicrystals. Aperiodicity alone determines neither a diffraction pattern
nor a photonic or acoustic band gap.

# 10. Bringing the rules to a 3D printer

To build a sample, we must return to the features that enforce its contacts.
The exact surfaces were chosen to make a geometric proof possible. A printer
introduces a different requirement: contacts must remain distinguishable
despite finite resolution and dimensional errors.

## 10.1 Why scaling the existing model is insufficient

The curved bumps and recesses used as ports are called **caps** in the
construction. Let $a$ be the physical unit-cube edge. Each exact cap has
width $a/32$;
consecutive depth keys differ at the cap center by $a/4096$. At $a=25$ mm:

| Quantity | Size |
|---|---:|
| Overall chair span along each carrier axis | 50 mm |
| Cap width | 0.78125 mm |
| Consecutive depth difference at the center | 0.00610 mm |
| Upper bound on any cap's normal displacement | 0.09836 mm |

The depth distinction is about six micrometers. Preserving it reliably is
not a suitable target for ordinary filament printing. Increasing that
difference to 0.2 mm by uniform scaling would require $a=819.2$ mm and a
chair over 1.6 m across.

## 10.2 Encode identity with separated features

A candidate replacement is a shallow array of broad tabs and pockets with
chamfered entrances, meaning beveled edges that help guide the parts together.
Instead of twelve finely separated depths, use distinct spatial patterns
at one or a few easily resolved heights.

For example, one binary symbol could occupy two positions:

```text
symbol 0:   tab      pocket
symbol 1:   pocket   tab
```

Its intended partner has the complementary relief in the aligned contact
coordinates. A wrong symbol then creates tab–tab interference at one
position. Four bits provide 16 possible labels, enough to encode twelve
identities before imposing additional geometric restrictions.

This is only a coding idea. A useful design must also distinguish rotations
and reflections, prevent lateral bypass, leave enough retained material,
and avoid accidental partial engagement. We should compare whole-panel
encodings of A/B/C against replacing every existing port separately.

Correctly reproducing the aligned contact table would reuse much of the
discrete reasoning. Establishing an exact physical monotile would additionally
require a new argument about arbitrary Euclidean placements.

## 10.3 Tolerance and assembly are part of the design

**Clearance** is a small intentional gap between mating surfaces. It helps
real parts fit, but also admits motion and can weaken contact
discrimination. The useful test is whether intended pairs seat reproducibly
while unintended pairs remain distinguishable over a stated range of errors
and applied forces. Printer tolerances depend on material, orientation,
geometry, settings, and calibration. [Prusa's design guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)

A collision-free final arrangement need not have an accessible assembly
path. A piece may be blocked by neighbors before reaching its final position.
Check insertion paths and disassembly as well as static fit.

A practical progression is:

1. Print **contact coupons**: small samples of correct and incorrect interfaces,
   including wrong orientations, at several clearances.
2. Measure seating gaps, assembly force, repeatability, and wear.
3. Print eight identical chairs and assemble one parent group.
4. Build a 64-chair patch to display two hierarchy levels.
5. Introduce controlled defects and measure recognition at each level.

Record printer settings and failed fits as carefully as successful ones.
This first object would be an experimental matching-rule demonstrator. Its
value does not depend on claiming that a finite, imperfect assembly proves
an infinite-space theorem.

# 11. What has been established, and where to read more

The chair hierarchy has substantial prior history. Goodman-Strauss used
chair recognition in [*A Pair of Aperiodic Tiles in Eⁿ*](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).
The recent [Chair44 preprint](https://zenodo.org/records/22792358) by Ioannis
Tsiokos uses the same discrete decorated system as ours after coordinate
conversion and key relabelling. Its square-pyramid solid differs from our
curved solid. Our comparison does not settle private discovery chronology
or establish independent invention.

| Layer | Status in this project |
|---|---|
| Finite contacts and substitution data | Exact computational checks with preserved witnesses |
| Universal grouping, legal deflation, and translation exclusion | Lean proofs for our defined proper integer-grid tiling model |
| Existence and arbitrary-placement bridge for our curved solid | Written arguments; outside the completed Lean development and awaiting mathematical review |
| Chair44 square-pyramid solid | Pinned Lean build and fresh axiom audit reproduced; theorem includes existence and finite symmetry for arbitrary physical tilings |
| Printable replacement interfaces | Proposed direction; no validated replacement or printing experiment yet |

It helps to separate three kinds of evidence. A finite calculation checks
the configurations it actually enumerates. A proof shows why its conclusion
holds for every object satisfying specified assumptions. A formal proof
expresses those steps in a language a proof assistant can check.

## Optional detail: what must we trust in a computer-checked proof?

Lean checks a precisely stated formal theorem. We must still inspect whether
its definitions describe the intended geometric object and whether the
assumptions match the claim being communicated. Our grid audit reports the
standard logical axioms and no native-evaluation hooks. A **native-evaluation
hook** allows a finite calculation executed by compiled code to supply a
result to the proof; this requires trusting that execution as well as the
proof checker. The reproduced Chair44 endpoint uses 21 disclosed hooks.
Its release control suite also has a packaging failure: a historical comparison archive is
missing. That is distinct from the successful proof compilation. See the
[build record](../strong/review/CHAIR44_BUILD_REPRODUCTION.md).

Neither this tutorial nor the internal AI reviews constitute independent
human mathematical review.

## Further reading and a reproducible calculation

For a next reading step:

- **Inspect the object:** open the [offline chair viewer](../strong/artifacts/recut-chair.html)
  directly in a browser. Its mesh approximates the exact surfaces.
- **Follow the local argument:** [three-pattern grouping](../strong/MOTIF_GROUPING.md).
- **Follow the formal proof:** [Lean project guide](../formal/README.md) and
  [translation exclusion](../formal/TRANSLATION_EXCLUSION.md).
- **Compare physical realizations:** [Chair44 proof comparison](../strong/review/CHAIR44_PROOF_COMPARISON.md).
- **Explore physics:** the Lee–Moody diffraction paper and Noya–Doye assembly
  paper linked above address different aspects of order without periodicity.

To reproduce the finite grouping check, run from the repository root:

```sh
uv sync --locked
uv run --locked python strong/audit/motif_grouping.py
```

This command regenerates its research evidence. It checks the stated finite
grouping certificates; it does not test a printed object or establish the
continuous geometric bridge. Full Lean reproduction additionally requires
the pinned toolchain described in the Lean project guide.

# 12. Exercises

1. **Count the boundary.** Explain why the seven-cube chair has 24 exposed
   unit-square panels, the same count as the original $2\times2\times2$ cube.
2. **Count a hierarchy.** How many elementary chairs are in a level-three
   group? What are its carrier volume and linear scale in unit-cube units?
3. **Exclude a period.** An alleged grid period is $(24,-8,0)$. Apply the
   deflation argument until you obtain a contradiction.
4. **Identify the missing premise.** Why is “this patch has an eight-chair
   decomposition” insufficient to show that every tiling is aperiodic?
5. **Estimate printable scale.** What unit-cube edge would make consecutive
   center heights differ by 0.1 mm without changing the cap design?
6. **Interpret scattering.** Two assemblies have the same outer boundary and
   uniform density, but different invisible internal tile partitions. Does
   their continuum density scattering distinguish the partitions?
7. **Energy versus legality.** If a periodically repeated discrete patch has
   seam energy $6\epsilon L^2$ and $L^3$ sites, what happens to its energy per
   site as $L$ grows? Does this make it a legal exact tiling?

## Answers and hints

1. The original cube has six sides with four panels each. Removing a corner
   loses three exterior panels but exposes three previously internal ones:
   $24-3+3=24$.
2. $8^3=512$ chairs; carrier volume $7\times512=3584$; linear scale factor
   $2^3=8$ relative to one chair. Its bounding cube therefore has edge 16.
3. The successive periods are $(12,-4,0)$, $(6,-2,0)$, and $(3,-1,0)$.
   The last vector is not even, but every legal tiling's period must be even.
4. We need every legal infinite tiling to have an intrinsic, unique grouping,
   and its deflation to remain legal, so that periods preserve the grouping
   and the argument can be repeated. Existence is a separate obligation.
5. $a/4096=0.1$ mm gives $a=409.6$ mm, with overall span $819.2$ mm.
6. No, under these idealized assumptions the density fields coincide.
   Introduce a physically observable contrast to distinguish them.
7. It is $6\epsilon/L$, which tends to zero. The seams may still violate
   constraints for every finite $L$. Small energy density is not exact legality.

# The lessons to keep

- Local geometry can encode information that controls organization at every scale.
- The ability to build a hierarchy is weaker than forcing every tiling to have one.
- Recognizable grouping turns a global symmetry question into an integer-divisibility argument.
- The geometric bridge from freely moving solids to a discrete model deserves its own proof.
- Exact constraints, thermal stability, and assembly kinetics answer different questions.
- A physical measurement must couple to a real feature of the arrangement.
- A printable realization requires a tolerance and assembly study, not just an STL export.

The central experimental opportunity is to ask how much of that hierarchy
survives when exact local rules become imperfect physical contacts.

# Further scrutiny: rigidity, addresses, and a synchronization witness

*16 September 2026. Working addendum; not part of the frozen v1 review package.*

## What changed in this pass

The candidate geometry is unchanged. This pass found a **three-subdivision
synchronization witness** for its full orientation-sensitive substitution,
and gives additional written consequences of the existing hierarchy.
It did not identify a counterexample to the proposed physical-solid theorem.
Neither that observation nor the new finite calculation replaces review of
the analytic grid-enforcement argument.

The useful separation is:

1. **Geometric claim under review:** every physical tiling is an exact grid
   tiling obeying our finite rules.
2. **Checked finite statements:** local grouping, macrocontact recurrence,
   and now the cube-substitution synchronization witness.
3. **Written deductions:** a dyadic address factor, a sharper symmetry bound,
   and almost-everywhere uniqueness of a tiling with a prescribed address.
4. **Unresolved:** novelty, possible exceptional symmetric tilings, and the
   precise relation between all matching-rule tilings and the substitution hull.

The PDF, inquiry, and ZIP already being reviewed have not been replaced.

**Subsequent literature update:** the [follow-up search](LITERATURE_FOLLOWUP.md)
found direct precedents for several mechanisms below, notably the
Frettlöh–Sing coincidence graph, self-simulation proofs, and curved-boundary
enforcement of handedness. The new contribution within this project is
the explicit witness and its application, not those general methods.

**Deeper comparison:** [the direct prior-art audit](DIRECT_PRIOR_ART_AUDIT.md)
now gives an exact projection of all 168 cube labels onto Ben-Abraham–Flom's
published eight-color chair substitution: all 1,344 transitions agree.
It also identifies Fletcher's 2010/2011 orientation encoding of 21 Wang
cubes into one labeled cube with an external neighborhood atlas. The
substitution coding and general orientation-encoding idea have established
predecessors; the complete physical forcing claim still requires comparison
and correctness review.

## 1. Sharpening the geometric bridge

The cap argument is best read as a rigidity lemma followed by an ownership
lemma. This exposes the place where a symbolic result becomes a statement
about arbitrary Euclidean tilings.

### Rigidity lemma

For the uniformly normalized graph

\[
 z=H(1-u^2)(1-v^2)(1+u/5+v/7),\qquad H\ne0,
\]

an open coincidence under an ambient isometry determines its base center
and ordered tangent axes. The only remaining freedom is normal reversal;
the height coefficients then differ by the same sign.

**Reason.** The equation is monic in z. Substituting one graph into a moved
copy of the other equation gives a polynomial vanishing on an open subset
of the u,v plane. Polynomial division and equal total degree extend the
coincidence to the full algebraic surfaces. Their only straight lines are
the four lines bounding the unit square and `1+u/5+v/7=0`, all at z=0.
The parallel pairs determine the square; the fifth line eliminates its
nonidentity symmetries. This also identifies the entire bounded cap domain.
The fifth line need not lie on the physical cap.

### Ownership lemma

For this candidate, the rigidity lemma converts every open cap match into
an integral relative placement, an identical unit face, and opposite coarse
cube ownership. These implications require the actual port offsets, not
just opposite keys or a matching normal.

Here is a noncircular order for the global argument:

1. Compact congruent tiles have a uniform interior ball. Disjoint such
   balls in a bounded enlargement give local finiteness, before any grid
   has been assumed.
2. Every cap is covered by finitely many other tile boundaries. A finite
   closed cover of an open surface patch has a member with relative
   interior. Planes and seams cannot supply that interior, so a cap does.
3. Rigidity fixes the relative frame and integral translation. The key
   chirality table makes this relative frame proper.
4. A connected component of cap matches therefore has a common grid.
   Unchanged cube cores forbid duplicate ownership. An exposed face has
   a cap match, so ownership is closed under adjacency in that grid.
   One occupied cube consequently forces ownership of every grid cube.
5. **This last sentence alone is insufficient.** Use the disjoint feature
   boxes: outside them the coarse partition is unchanged, and inside each
   box its two opposite owners occupy complementary graph sides. Only
   this step proves physical coverage by the component.
6. Another component would have an interior ball overlapping the first
   component's tile interiors. Thus the component is the whole tiling.

This rules out independently shifted grid components without presupposing
face-to-face matching. The exact estimates and line calculation remain in
the [analytic audit](../audit/README.md). No new general theorem about all
tabbed polycubes is asserted: the exposed-face coverage and feature-box
hypotheses are essential.

This distinction connects to Hellouin de Menibus, Lutfalla, and Vanier's
[work on geometric tilings and finite local complexity](https://lutfalla.fr/documents/.preprints/geomino.pdf):
their setting explicitly separates geometric placement from symbolic
grid constraints. Their results do not prove our three-dimensional lemma.

## 2. The hierarchy gives an onto 2-adic address map

Work first with **X, the space of all valid grid tilings in one handedness**,
with origins in Z³ and the 24 proper orientations. This is the full local-rule
space, not merely tilings whose patches occur inside substitution supertiles.
The geometric bridge is needed to apply these conclusions to arbitrary
physical tilings.

X is a nonempty compact subshift of finite type. For example, put occupancy
bits for the 24 possible tile orientations at each integer origin. Requiring
each unit cube to have exactly one owner, and each shared face to match,
imposes finitely many bounded-range conditions. Nonemptiness is the separate
[expanding-ball compactness argument](DEPENDENCY_AUDIT.md#d-existence-explicit-expanding-balls-and-a-compactness-argument).

The local parent rule and macrocontact recurrence give, for every m, one
coset containing all level-m parent origins:

\[
 a_m(T)+2^m\mathbb Z^3.
\]

These are containing cosets, not a claim that every point of a coset is a
parent origin. They are nested: the central child has zero displacement,
so a level-(m+1) origin is also a level-m origin. Hence

\[
 a_{m+1}(T)\equiv a_m(T)\pmod {2^m}.
\]

The compatible residues define

\[
 \pi:X\longrightarrow\mathbb Z_2^3
       =\varprojlim_m(\mathbb Z/2^m\mathbb Z)^3.
\]

A 2-adic address is simply the infinite compatible list of these residues.
For the convention `T+v` translating all placements by v,

\[
 \pi(T+v)=\pi(T)+v.
\]

**Continuity.** At a fixed m, follow the locally recognized parents of a
tile owning a specified unit cube. Only a finite neighborhood is inspected
at each of finitely many levels. This finds a level-m origin and therefore
its residue. Thus each coordinate a_m is locally constant.

**Surjectivity.** The image is nonempty and compact, and contains
`π(T)+Z³` for any T. Integer translations are dense in Z₂³. Its closed
image is therefore all of Z₂³. This uses no assumption of minimality.

**Aperiodicity.** A translation symmetry v first has to be integral, since
it takes tile origins to tile origins. It must satisfy
`a_m+v=a_m mod 2^m` for every m, hence v=0. This repackages the existing
period-divisibility proof; it is not a second independent proof of the
parent rule.

The terminology is **recognizability** or **unique composition**.
[Solomyak's notes, Theorem 3.8](https://u.math.biu.ac.il/~solomyb/RESEARCH/notes6.pdf)
explain its relation to aperiodicity for self-affine tiling hulls. We prove
recognizability from local rules here; invoking a theorem that assumes
aperiodicity to obtain recognizability would be circular.

This is a Z³ action on grid-normalized tilings. The continuous R³ tiling
space is a different space; its corresponding factor is a dyadic solenoid,
not simply Z₂³.

## 3. A concrete link to substitution automata and model sets

Lee and Moody's [Lattice Substitution Systems and Model Sets](https://arxiv.org/abs/math/0002019)
studies n-dimensional chairs using 2-adic internal spaces. Their modular
coincidence criterion motivates the following test. The extra orientations
in our candidate mean their chair result cannot simply be imported.

The subset-to-singleton search is the established coincidence-graph method
of [Frettlöh and Sing, Theorem 4.4](https://www.math.uni-bielefeld.de/~frettloe/papers/mfs.pdf).
This direct methodological precedent was located in the subsequent search.

### Turn chairs into a finite alphabet

Label each unit cube by `(R,q)`, where R is its owner's proper orientation
and q is its cube in the original seven-cube chair. There are `24×7=168`
labels. The cube's position and its label recover the chair's origin and
orientation, so this loses no placement information.

Inflate one such cube by 2. Its eight unit subcubes obtain their labels
from the frozen eight-chair subdivision. This gives eight functions
`F_d` on the 168 labels, one for each binary digit vector `d∈{0,1}³`.

### The exact witness

Read successive digits from the outermost subdivision to the innermost:

\[
 (0,0,0),\quad(0,0,1),\quad(0,0,0).
\]

The images of the full alphabet shrink as follows:

```text
168 labels → 42 labels → 6 labels → 1 label.
```

Equivalently, after three substitutions the cube at position `(0,0,2)` in
the `8×8×8` expansion has the same label for every possible starting label:

```text
R(x,y,z) = (x,z,-y),    q = (-1,0,-1).
```

The six possibilities immediately before the last digit are small enough
to display. Applying `F_(0,0,0)` to each gives the single label above:

| Orientation `(x,y,z) ↦` | Local cube q |
|---|---|
| `(-x,-z,-y)` | `(0,-1,0)` |
| `(-y,-x,-z)` | `(0,0,-1)` |
| `(-z,-y,-x)` | `(-1,0,0)` |
| `(z,x,y)` | `(-1,0,-1)` |
| `(y,z,x)` | `(0,-1,-1)` |
| `(x,y,z)` | `(-1,-1,0)` |

This is a **synchronizing word** in finite-automaton language: observing
this digit sequence erases uncertainty about the starting state. In the
lattice-substitution language it is a modular coincidence at level three.

The new [standalone calculation](../audit/explore_cube_substitution.py)
reads only the frozen coordinates and uses exact integer arithmetic. It
also expands the actual chairs directly through depths one, two, and three,
and compares **98,112 cube labels** against the digit-map calculation.
These are two calculation paths in one program, not two independent reviewers.

Additional finite results:

- Every orientation occurs in the second iterate of every orientation:
  the 24-state orientation substitution has primitivity exponent 2.
- Every cube label occurs in the third iterate of every cube label:
  the 168-state cube substitution has primitivity exponent 3.
- Forgetting the three internal poses about a chair's notch diagonal gives
  56 coarse cube labels. All their digit maps are well-defined: zero
  conflicts among the three representatives of each coarse state.

The last point concerns forgetting information in an already hierarchical
tiling. Physically removing orientation keys allows additional tilings, as
the [periodic ablation](../FOLLOWUP_REFLECTIONS.md) showed. These operations
must not be confused.

## 4. What synchronization adds: almost every address determines a tiling

Here is a written deduction from the finite witness and the hierarchy,
including the step from generated patches to the full space X.

Fix a fine-grid cube at x∈Z³ and an address a=π(T). At level m, its position
inside its level-m grid cube is

\[
 r_m=x-a_m\pmod {2^m},\qquad 0\le(r_m)_i<2^m.
\]

The 168-label state of that ancestor cube may be unknown. Its fine label
is nevertheless obtained by applying the digit maps of r_m from most
significant to least significant digit. This holds in **every T∈X**, since
its uniquely recognized groups have exactly the frozen subdivision.

If any three consecutive digit vectors form the synchronizing word, the
fine label is independent of every more distant ancestor: apply that word,
then the remaining less significant digits.

For Haar probability on Z₂³ (uniform independent binary digits in its three
coordinates), x−a also has uniform independent digits. Each disjoint block
of three digit vectors has probability `1/8³=1/512` of being the word.
The probability of avoiding it in k disjoint blocks is

\[
 (511/512)^k\longrightarrow0.
\]

Thus the label at x is forced by a for almost every address. There are only
countably many x. Outside a Haar-null set, **every cube label is forced**.
Since cube labels reconstruct the tiling and π is onto, the fiber π⁻¹(a)
then consists of exactly one tiling.

Consequences, conditional on the stated hierarchy:

1. **Unique invariant probability measure on X.** An invariant measure
   exists by averaging translations over larger integer boxes and taking
   a weak limit. Every such measure pushes forward to Haar probability:
   invariance under dense integer translations implies invariance under
   all translations of Z₂³. The singleton fibers on a full-measure set
   then determine its unique lift.
2. **Pure point measurable dynamical spectrum.** Under that measure, π is
   an isomorphism modulo null sets with the 2-adic translation action.
   The pulled-back characters
   `exp(2πi k·a_m/2^m)` are eigenfunctions and span L². This is a statement
   about the grid translation action, with frequencies in
   `(Z[1/2]/Z)³`.

These are mathematical deductions, not properties the Python program
itself verifies. They explain precisely why the model-set literature is
relevant. A complete model-set/diffraction presentation would still need
to specify its point sets and check the relevant theorem's hypotheses.
The unmarked union of the solid tiles is all of R³, so its uniform density
alone would not encode the interesting diffraction information.

**Limits:** singleton fibers almost everywhere do not show that every fiber
is singleton, that X is minimal, or that every locally legal patch occurs
inside one substituted chair. Exceptional boundaries and addresses remain
to be classified. The synchronization calculation therefore does not
license importing every theorem about a primitive substitution hull.

## 5. Sharper symmetry statements

### Every symmetry group has at most 24 elements

The earlier proof gave the conservative bound 48 from cubic frames. The
handedness result improves this to **24**. In a one-handed tiling write
tiles as `c+RP`, with every R proper and P the keyed solid. If an improper
symmetry carried one tile to another, composing its placement maps would
give an improper self-isometry of P. The checked full stabilizer of P is
the identity, so this is impossible. The mirrored case is equivalent by
global reflection.

All symmetry linear parts consequently lie in the proper cubic group of
order 24. Two symmetries with the same linear part differ by a translation,
already excluded. This gives the bound, without claiming that it is attained.

### Almost every tiling has no nonidentity symmetry at all

Write a possible symmetry in grid coordinates as `x↦Rx+t`. Its translation
part t is integral, since it maps a tile origin to a tile origin. Equivariance
of the hierarchy gives the necessary address condition

\[
 (I-R)a=t\quad\hbox{in }\mathbb Z_2^3.
\]

For each R≠I and each integer t, this solution set has Haar measure zero:
one nonzero row of I−R supplies a nonzero integer linear equation; fixing
the other coordinates permits at most one value of a coordinate with a
nonzero coefficient. Haar measure on Z₂ has no atoms. There are only
countably many such pairs (R,t).

Therefore Haar-almost every address admits **no possible nontrivial
symmetry**, and the invariant measure above gives full weight to tilings
with trivial stabilizer. This argument only needs the address factor;
synchronization is not needed for the null-set exclusion itself.

This does **not** upgrade the all-tilings theorem to trivial stabilizers.
It narrows the remaining question to exceptional address fibers. Satisfying
the displayed equation is necessary, not sufficient, for a symmetry.

## 6. Attribution and the next useful questions

Goodman-Strauss's [Addressing in substitution tilings](https://strauss.hosted.uark.edu/papers/Addresses_5_97.pdf)
is particularly relevant: it describes parent addresses and automata for
neighbor relations. The available manuscript says **DRAFT: May 6, 2004**
despite its older-looking filename. It motivates a finite-state analysis
of exceptional boundaries; it is not an external verification of this work.

The chair hierarchy, recognizability framework, 2-adic addresses, and
coincidence method are established ideas. The new items **within this
project** are the explicit 168-state encoding, its short synchronization
witness, and the deductions above for the proposed full local-rule space.
No priority claim for these deductions is made.

The candidate's potential contribution remains narrowly stated: its
orientation patterns might enforce the known hierarchy using one
congruence class of connected solid. The dynamical connections clarify
the mechanism; they do not establish that this enforcement is new.

Priority follow-ups:

1. Obtain an outside assessment of the analytic ownership/grid bridge and
   of the one-congruence-class enforcement claim.
2. Turn the synchronization witness into a short, human-readable table,
   or a synthetic proof, rather than making a reviewer inspect all 168 states.
3. Study exceptional fibers and rotation constraints using a finite-state
   boundary analysis. This can address actual finite symmetries and whether
   the full local-rule space equals the substitution hull.
4. Only then seek a full model-set or diffraction description. Do not
   inflate the initial inquiry with every secondary connection.

## Reproduction and record

```sh
uv run --locked python strong/audit/explore_cube_substitution.py
```

- [Exact transition tables and result](../audit/cube_substitution_exploration.json).
- Input candidate SHA-256:
  `95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54`.
- The program imports no project implementation and uses no floating point.
- The three-subdivision witness was found by subset exploration, then
  checked against direct coordinate expansions, including all starting labels.
- Frozen geometry, v1 review artifacts, and the unsent inquiry are unchanged.
- No external review or outreach occurred in this pass.

# Earlier studies and the recut-chair proposal

*15 September 2026. Targeted primary-source review by subagent
`/root/literature_review`, summarized by the primary agent.*

**Substantial parts of the construction have close precedents.** The review
did not identify the exact one-chair matching system in those sources.
This is neither a novelty claim nor an exhaustive priority search.

**Scope update, 16 September:** this review compared the original proper-copy
proposal. The subsequent [handedness argument](../FOLLOWUP_REFLECTIONS.md)
extends the proposed theorem to reflected copies without changing the
frozen solid. That extension does not settle the priority question.

## 1. The closest predecessor: Goodman-Strauss's aperiodic pair

*An Aperiodic Pair of Tiles in Eⁿ for All n ≥ 3*, European Journal of
Combinatorics **20 (1999), 385–395**, has an author preprint dated
17 February 1998. [Published paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Goodman2.pdf),
[searchable preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).

The published paper already supplies:

- The seven-cube chair and scale-two, eight-child substitution (§2,
  pp.386–387).
- A recut chair together with an auxiliary I piece; geometric fittings can
  implement the markings (§3, p.389).
- Transmission along I chains and preservation of the hierarchy under
  grouping (Lemma 4.3 and Proposition 4.6, pp.392–393).
- A connected-interior **two-tile** variant `{X₂,L}` in 3D (§5, p.394).
  An additional X₁ is required only in the stated higher-dimensional variant.

Its introduction gives eight L-tile orientation states in 3D, and its
markings preserve coordinate-permutation symmetry. Our frozen candidate
distinguishes three proper poses per missing-corner direction, giving 24
states. This is a concrete difference, not proof of inequivalence under
every possible recoding. The paper's difficulty replacing its I pieces by
one marked cross is specific to that design, not an impossibility theorem
for all chair decorations.

### What the auxiliary pieces do

The author's [construction poster](https://strauss.hosted.uark.edu/distribution/tilings/enap.pdf)
explains that the obelisks carry markings between supertiles at successive
levels: central-tile information reaches the boundary through those pieces.
They cannot simply be discarded as irrelevant fillers.

**Our interpretation:** the candidate's crucial proposed contribution is
carrying enough information through differently oriented copies of one
decorated chair. The old coarse substitution is already known. The new
finite claim to compare is the exact 44-contact rule system recurring after
unique grouping. The separate geometric claim is that the exact caps force
every physical tiling to realize that system.

## 2. Marked chairs and general hierarchy enforcement are older still

Goodman-Strauss's [Threelobites retrospective](https://chaimgoodmanstrauss.com/threelobites/)
dates drawings of marked higher-dimensional chairs to **fall 1994**.
The date refers to the drawings, not publication of a one-solid theorem.
The page does not give the candidate's local rules.

His *Matching Rules and Substitution Tilings*, Annals of Mathematics
**147 (1998), 181–223**, gives broad matching-rule constructions under its
hypotheses. These may introduce multiple decorated tile types; the theorem
does not promise that they are rotations of one physical tile.
[Journal abstract](https://annals.math.princeton.edu/articles/12903),
[author manuscript](https://strauss.hosted.uark.edu/papers/MRandST.pdf).

Thus a hierarchical marked chair, or a general theorem enforcing a
substitution with markings, is insufficient on its own to establish this
one-solid claim.

## 3. Orientation rules need not be realizable by a shape

Walton and Whittaker's *An Aperiodic Tile with Edge-to-Edge Orientational
Matching Rules*, first published online **18 October 2021**, gives a marked
hexagon with orientation and charge conditions. Its introduction explicitly
distinguishes these conditions from rules enforceable by shape alone.
[Primary article, introduction and R1/R2](https://doi.org/10.1017/S1474748021000517).

The broad use of orientation as information is therefore established.
Our geometry still requires its own compatibility and grid-enforcement
proof; that earlier example cannot supply the conversion automatically.

## 4. Other 3D monotiles and definitions

- **Socolar–Taylor, 2010/2011:** the connected 3D realization in §7 permits
  periodic stacking transverse to corrugated slabs. It does not meet our
  finite-symmetry target. [Primary preprint, p.31](https://arxiv.org/pdf/1003.4279).
- **Goucher, 26 August 2013:** the author's construction explicitly retains
  screw symmetry. [Construction account](https://cp4space.hatsya.com/2013/08/26/a-more-aperiodic-monotile/).
- **Kaplan, September 2025:** the closing 3D discussion distinguishes the
  stronger target from SCD's remaining screw symmetry. This is dated context,
  not a priority certificate. [Survey](https://arxiv.org/html/2509.12216v1).
- **Coulbois–Gajardo–Guillon–Lutfalla, 2026:** “strongly aperiodic” means
  trivial stabilizers in their terminology; “mildly aperiodic” means finite
  stabilizers. Their open-problem statements must be translated before
  comparison with our target. [Primary paper, §§2, 5.3, 6](https://doi.org/10.1016/j.tcs.2025.115555).

## 5. What remains unresolved

The examined sources establish the ancestry of the chair hierarchy and
several methods used here. They do **not**, as far as this review found,
identify the exact single asymmetric chair, its recursive 44-contact system,
or the specified polynomial-cap proof. An equivalent construction could
still exist in another presentation, older notes, or unpublished work.

The appropriate description remains:

> A proposed single-solid realization using an orientation-sensitive chair
> matching system, built on known chair-hierarchy methods.

An expert comparison should start with the 1999 paper's marking definition,
Lemma 4.3, Proposition 4.6, and §5, and explicitly account for our extra
orientation states. Sharing the same unmarked substitution does not by
itself establish equivalence of the two spaces of allowed tilings.

No external researcher was contacted, and the literature review does not
change the [mathematical reviews'](SUBAGENT_REVIEWS.md) scope: exact curved
solid, proper rotations of one handedness, and tile-preserving symmetries.

## 6. Figure 2 and the ordinary chair's periodic tilings

Figure 2 on p.3 of the linked **author preprint** concerns the same coarse
chair used here. The surrounding text defines the chair and its subdivision.
That known geometry alone does not force aperiodicity. Nor does displaying
one hierarchical arrangement exclude other, periodic arrangements.

In fact the plain chair tiles periodically by translations in

```text
Λ = {(x,y,z) in Z³ : x+2y+4z = 0 mod 7}.
```

Its seven cube lower corners have all seven distinct residues, so their
translates by Λ partition the integer cubes. A basis for Λ is
`(7,0,0), (-2,1,0), (-4,0,1)`.

We tested this particular periodic arrangement directly against the frozen
candidate. Chairs separated by `(-2,1,0)` share 16 ports, and all 16 mismatch
for every one of the nine combinations of their three shape-preserving
proper poses. Thus even arbitrary choices of these poses cannot rescue this
coarse periodic arrangement.

For two identity poses, a common port center is `(-1,5/16,-9/16)`. The keys
are `-7` and `+9`: the tab exceeds the opposite pocket's depth. At its tangent
center the boundary x coordinates are `-4089/4096` and `-4087/4096`.
The point `(-511/512,5/16,-9/16)` lies strictly inside both physical solids.

[Exact result](periodic_chair_check.json), reproduced using:

```sh
uv run --locked python strong/audit/check_periodic_chair.py
```

This check excludes **one** periodic arrangement. Exclusion of all periodic
tilings rests on the proposed forced-hierarchy proof, not this test, the
appearance of Figure 2, or the number of available orientation states.

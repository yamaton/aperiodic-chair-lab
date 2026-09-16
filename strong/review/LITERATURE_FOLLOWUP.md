# Further literature search: close analogues and useful distinctions

*16 September 2026. Primary-source search following the scrutiny addendum.*

## Assessment

Several mechanisms we independently arrived at have **direct predecessors**:
the subset-to-singleton algorithm, self-simulation by uniquely recognized
macrotiles, encoding tile types by orientations of one shape, and enforcing
homochirality with curved boundaries. The new references substantially
improve attribution and suggest concrete checks. They do not themselves
validate our solid or identify it with an earlier construction.

The narrow unresolved comparison remains: can this particular local rule
system and exact geometry enforce the chair hierarchy with **one congruence
class of connected solid**, covering all of R³ under unrestricted isometries?
The existing [Goodman-Strauss comparison](../audit/LITERATURE_REVIEW.md) remains
the closest geometric starting point.

This record supplements the [scrutiny addendum](SCRUTINY_ADDENDUM.md).
It does not change the frozen geometry or the v1 review packet.

## 1. The subset computation is an established coincidence-graph method

**Dirk Frettlöh and Bernd Sing, _Computing modular coincidences for
substitution tilings and point sets_, Discrete & Computational Geometry
37 (2007), 381–401.** Preprint title: _Computing modular coincidences_ (2006).
[Author PDF](https://www.math.uni-bielefeld.de/~frettloe/papers/mfs.pdf),
[bibliographic record](https://arxiv.org/abs/math/0601067),
[DOI](https://doi.org/10.1007/s00454-006-1280-9).

**Read:** §4, especially Theorems 4.4–4.5, and the pair-graph discussion.
Their coincidence graph has subsets of labels as vertices. Reaching a
singleton detects a modular coincidence; exhaustion without a singleton
can certify its absence under the stated lattice-substitution hypotheses.

**Our connection:** `168 → 42 → 6 → 1` is an instance of this established
algorithmic idea. The particular word is a certificate for our encoding,
not a new general method. The paper's return-lattice conventions must be
checked before transferring a theorem verbatim; our all-label singleton
witness is a concrete sufficient coincidence.

**Use next:** cite this method, export a readable coincidence graph, and
check lattice-substitution hypotheses explicitly before claiming model sets.

## 2. Exceptional addresses have an automata literature

**Gandhar Joshi and Reem Yassawi, _Semicocycle discontinuities for
substitutions and reverse-reading automata_.** Preprint 2022;
[primary PDF](https://arxiv.org/pdf/2211.01843),
[publication DOI](https://doi.org/10.1016/j.indag.2023.05.003).

**Read:** §§2–3, Definitions 18 and 21, Theorem 22. They construct a
substitution-semigroup automaton and remove constant-output states to study
the unresolved part of a Toeplitz sequence. Theorem 22 relates its reduced
graph to semicocycle discontinuities under precise one-dimensional hypotheses.

**Our connection:** addresses where orientation information never becomes
forced are the natural analogue of these discontinuities.

**Limit:** our digits are vectors and our action is Z³. Their theorem is
not a ready-made classification of our exceptional fibers. Also, a word
avoiding our one known reset word can still synchronize by another word;
word avoidance alone does not identify the exceptional set. Reading digits
in the opposite order generally requires a different automaton.

**Use next:** adapt a transformation-semigroup or reverse-reading construction,
and separately enforce which ambiguous ancestors are globally realizable.

## 3. Robinson tilings demonstrate the full-space versus hull distinction

**Franz Gähler, Antoine Julien, Jean Savinien, _Combinatorics and topology
of the Robinson tiling_, C. R. Mathématique 350 (2012), 627–631.**
[Primary article](https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.1016/j.crma.2012.06.007/),
[PDF](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/j.crma.2012.06.007.pdf).

**Read:** Proposition 1.1, Theorem 2.1, and the local-derivation discussion.
The full Robinson local-rule space is not minimal but contains a unique
minimal subsystem. Their substitution description concerns that subsystem.
They distinguish configurations with one infinite-order supertile from
those with several; additional decorations recover information lost by
a simpler factor.

**Our connection:** this is a concrete precedent for the distinction we
left open. Forced hierarchy does not automatically imply that every finite
patch appears inside one substituted chair.

**Use next:** test complete vertex neighborhoods, including edge/corner
contacts. Agreement of the 30 surviving face-contact types with the
substitution language is insufficient to establish equality of tiling spaces.

## 4. Self-simulation already gives our period-divisibility proof pattern

**Bruno Durand, Andrei Romashchenko, Alexander Shen, _Fixed point theorem
and aperiodic tilings_ (2010 preprint).**
[Primary PDF](https://arxiv.org/pdf/1003.2801).
Their larger development is
[_Fixed-point tile sets and their applications_](https://arxiv.org/abs/0910.2415).

**Read:** §3 of the short paper. A tile set implements a macrotile system
when every valid tiling has a unique decomposition into those macrotiles.
Self-simulation requires the matching relation to recur. The resulting
period-divisibility argument and separate compactness existence argument
closely parallel ours.

**Our connection:** the 44 fine contacts recurring as 44 deflated macrocontacts,
plus the local parent rule, form a geometric version of self-simulation.

**Limit:** their symbolic Wang-tile construction does not deliver one connected
physical solid. We should attribute the proof architecture while isolating
the compression into one shape and the geometric placement argument.

## 5. A general higher-dimensional hierarchy-enforcement framework

**Thomas Fernique and Nicolas Ollinger, _Combinatorial substitutions and
sofic tilings_ (2010 preprint; revised 2011).**
[Primary PDF](https://arxiv.org/pdf/1009.5167).

**Read:** Definitions 3.1–3.4, Theorem 1.1, and the self-simulation setup.
They define a limit set using arbitrarily deep preimages and show that
good combinatorial substitutions have sofic limit sets: finite decorations
and local rules enforce the hierarchy. Their definitions cover polytopes
in Rᵈ, with connecting and consistency assumptions.

**Our connection:** their separation of parent structure, matching macrofacets,
and channels carrying information is a useful language for the chair rules.

**Limit:** the decorations need not be orientations of one congruent object.
Nor may their face-to-face hypotheses be assumed for arbitrary curved-solid
placements. They address the symbolic stage after the geometric bridge.

## 6. A recent preprint targets exactly the hierarchy/hull distinction

**Nikolay Vereshchagin, _Matching Rules for Substitution and Hierarchical
Tilings for any Substitution with Finite Local Complexity_.**
Submitted 23 June 2026; inspected v2 dated 10 August 2026.
[Primary PDF](https://arxiv.org/pdf/2606.25005v2),
[version record](https://arxiv.org/abs/2606.25005).

**Read:** §§1–2, Lemmas 2–3, and the statement of Theorem 1. The paper
distinguishes substitution tilings from tilings that can be composed
indefinitely. Lemma 2 supplies a sufficient condition for the converse:
allowed vertex crowns at every composition level, with FLC. A crown is
the collection of tiles incident to a vertex.

**Our connection:** a promising additional certificate is that every crown
permitted by our rules occurs in a substitution supertile, and this property
survives composition.

**Limits:** the inspected development uses planar polygons; the analogous
3D covering argument needs proof. This is a recent preprint, not a theorem
we have independently verified. Its decorations also do not establish a
one-congruence-class realization.

## 7. One shape encoding many tile types by rotation is older

**Erik D. Demaine, Martin L. Demaine, Sándor P. Fekete, Matthew J. Patitz,
Robert T. Schweller, Andrew Winslow, Damien Woods, _One Tile to Rule Them
All_.** Extended preprint 2012; related ICALP 2014 publication.
[Extended primary PDF](https://arxiv.org/pdf/1212.4756),
[authors' publication page](https://erikdemaine.org/papers/OneTile_ICALP2014/).

**Read:** introduction and §7, especially Theorem 7.1 and its construction.
Their many-sided tile uses rotations and small geometric features to encode
different tile types. The plane-tiling simulation explicitly uses a
prescribed lattice and permits small gaps: it is a nearly-plane tiling.
Their self-assembly model is separately defined and has different rules.

**Our connection:** orientation as a substitute for multiple prototile types
is a direct precedent, not merely a loose analogy.

**Critical difference:** we require full coverage and must derive the grid
from the solid's geometry. The cited result supplies neither for our candidate.
The remaining work is exactly where a casual appeal to a universal tile
would be misleading.

## 8. Curved boundaries enforcing common handedness: the Spectre

**David Smith, Joseph Samuel Myers, Craig S. Kaplan, Chaim Goodman-Strauss,
_A chiral aperiodic monotile_, Combinatorial Theory 4(2) (2024), #13.**
[Primary article](https://escholarship.org/uc/item/4xn41982),
[PDF](https://escholarship.org/content/qt4xn41982/qt4xn41982.pdf).

**Read:** Lemma 2.1 and §2.1. Their curved-edge construction enforces whole-edge
alignment and excludes neighboring opposite handednesses. It establishes
a correspondence with homochiral tilings of the underlying polygon.

**Our connection:** the strategy “geometric interfaces force consistent
handedness, then transfer a hierarchy argument” has a direct published
precedent. Our signed-key determinant identity is a specific 3D implementation.

**Limit:** their planar boundary argument does not prove rigidity of our
surface caps. The five-line algebraic characterization and the component
coverage argument still require their own justification. We should not
claim a new general principle of chiral enforcement.

## 9. Chair symmetries and exceptional fibers have been studied together

**Michael Baake, John A. G. Roberts, Reem Yassawi, _Reversing and extended
symmetries of shift spaces_, DCDS A 38 (2018), 835–866.**
[Primary PDF](https://arxiv.org/pdf/1611.05756),
[journal article](https://doi.org/10.3934/dcds.2018036).

**Read:** Theorem 6 and its proof. For the planar chair shift they determine
the extended symmetry group using its 2-adic factor, including exceptional
fibers of cardinalities 2 and 5.

**Our connection:** analyzing fibers and the action induced on the dyadic
address space is an established route to symmetry restrictions.

**Essential distinction:** their symmetry group consists of transformations
of the entire shift space. Our finite group is the Euclidean stabilizer of
one particular tiling. Translations act on the whole tiling space even
when no nonzero translation fixes an individual tiling. The group formulas
cannot be substituted for our stabilizer calculation.

## 10. Boundary defects can restrict extended symmetries

**Álvaro Bustos, _Extended symmetry groups of multidimensional subshifts
with hierarchical structure_, inspected 2019 revision.**
[Primary PDF](https://arxiv.org/pdf/1810.02838).

**Read:** §5, including Proposition 22 and Corollary 23. The paper uses
fracture directions in Robinson configurations to constrain symmetries,
and treats both full and minimal spaces.

**Our connection:** if exceptional chair configurations have boundary planes
that persist through all levels, their directions could constrain possible
rotations and the structure of address fibers.

**Limit:** the paper also studies bijective substitutions. Our cube
substitution is synchronizing and is not bijective in that sense. Those
results do not apply wholesale. Its extended-symmetry groups likewise
are not individual geometric stabilizers.

## 11. The correct multidimensional odometer framework

**María Isabel Cortez and Samuel Petite, _G-odometers and their almost
one-to-one extensions_, Journal of the London Mathematical Society 78
(2008), 1–20.**
[Primary publication](https://doi.org/10.1112/jlms/jdn002).

**Checked:** publication abstract and author-preprint introduction; a full
hypothesis audit remains to be done. The paper treats finitely generated
group actions, minimal almost-one-to-one extensions, and G-Toeplitz systems.
This is more appropriate to Z³ than importing a one-dimensional theorem
by replacing a scalar digit with a vector digit.

**Use next:** apply its framework to the appropriate minimal subsystem
once that subsystem has been identified. Our almost-everywhere singleton
result does not by itself establish minimality of the full rule space.

## 12. Older foundations and further leads

- **Dekking, _The spectrum of dynamical systems arising from substitutions
  of constant length_.** The
  [archived seminar version](https://www.numdam.org/item/PSMIR_1976___2_A6_0/)
  is catalogued 1976; its scan says submitted March 1977. It is a foundation
  for the later coincidence literature. Do not conflate the archive date
  with the 1978 journal citation used by later authors.
- **Mozes, _Tilings, substitution systems and dynamical systems generated
  by them_, J. Analyse Math. 53 (1989), 139–186.**
  [Author-institution record](https://cris.huji.ac.il/en/publications/tilings-substitution-systems-and-dynamical-systems-generated-by-t/),
  [DOI](https://doi.org/10.1007/BF02793412).
  Bibliography and abstract checked here; the exact applicability of its
  construction has not been audited. Fernique–Ollinger gives a directly
  accessible later formulation.
- **Baake, Gähler, Mazáč, Sadun, _On the long-range order of the Spectre
  tilings_**, [2024 preprint](https://arxiv.org/abs/2411.15503).
  Abstract checked: it links Spectre dynamics to regular cut-and-project
  descriptions. Useful for a later diffraction study; not evidence about
  our 3D geometry or an immediate priority conflict.

These are leads or context at the stated reading depth, not fully audited
applications of their theorems.

## What this changes in our writeup

1. Attribute the subset algorithm explicitly to the coincidence-graph
   literature. Describe our reset word as a newly checked instance.
2. Present the hierarchy proof as an explicit self-simulation certificate
   with a separate geometric realization. Its overall logic is established.
3. Cite the Spectre and one-tile simulation papers when discussing
   handedness and information carried by orientation.
4. Maintain separate notation for the full local-rule space X and the
   substitution hull Y. Neither a measure-theoretic identification nor
   agreement of pair-contact lists proves X=Y.
5. Keep individual tiling stabilizers separate from automorphisms or
   extended symmetries of a tiling space.

## Concrete next investigations suggested by the sources

### A. Compare complete crown languages

In the 168-label cube representation, a vertex crown is a labeled 2×2×2
block. Enumerate the blocks generated by substitution to a certified
closure. Separately obtain the blocks that the chair matching rules can
permit, preserving owner consistency between cube labels. A local search
may overestimate globally extendible blocks; mark that distinction.

If the latter set is contained in the former, and the same holds after
composition, prove the 3D analogue of the small-neighborhood covering
argument. That would address X=Y rather than merely comparing face pairs.
If extra blocks appear, first determine whether they extend; their presence
in a finite local search alone proves neither a new infinite tiling nor a gap.

### B. Classify unresolved addresses with the correct reading direction

Retain all digit maps, not just the one reset word. Build an automaton that
tracks the transformations induced when increasingly significant ancestor
digits are supplied. Distinguish a subset graph useful for finding reset
words from a reverse-reading construction useful for fixed low-order
digits. Only globally realizable ambiguity should count as a non-singleton
fiber. This follows the questions raised by Joshi–Yassawi, not an automatic
application of their one-dimensional theorem.

### C. Test rotations only after imposing address and label compatibility

The necessary equation `(I-R)a=t` is a first filter. Study how R acts on
the admissible labels and choices in the remaining fibers. This can decide
whether some exceptional addresses actually support nontrivial finite
stabilizers. A solution of the address equation alone is insufficient.

## Search scope and limits

Searched for 3D monotiles/chairs, one-tile simulations, geometric matching
and chirality, modular coincidence algorithms, substitution automata,
Toeplitz/odometer extensions, Robinson boundary defects, and symmetry
groups. Followed references from the newly found papers, including the
2026 preprint's citation to Fernique–Ollinger.

Technical comparisons above use primary papers or author/institution
records. Search hits on “3D aperiodic metamaterials” or near-tilings do not
by their titles establish a solid whose every full-space tiling meets our
symmetry condition. General search did not locate an exact duplicate of
our frozen matching system; that is a limited search result, not priority
evidence. No researcher was contacted.

No new geometry computation was needed for this bibliographic pass.
Preserved the exact candidate, inquiry, PDF, HTML, and v1 ZIP. Further
calculation should continue using `uv` and the existing locked environment.

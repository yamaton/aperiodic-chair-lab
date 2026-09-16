# Direct prior-art audit: chairs, orientation coding, and physical enforcement

*16 September 2026. Separate from the frozen v1 packet. No outreach.*

## Assessment

This deeper search found **an exact published substitution factor** and
**a direct precedent for encoding 3D tile types as orientations of one tile**.
It also found an author's chair-based attempt at reducing to identical shapes
whose proposed rules admit periodic arrangements. These are substantive
additions to our comparison, not evidence that the full candidate is new.

The outstanding claim is narrowly stated: one connected solid, with arbitrary
Euclidean placements (including reflected copies), fills all of R³ and forces
every tiling to have finite symmetry group, using its boundary alone. The
candidate's correctness remains under review. Neither the chair hierarchy,
orientation encoding in general, nor dyadic chair dynamics should be presented
as our discovery.

Read this together with [the previous literature pass](LITERATURE_FOLLOWUP.md)
and [the scrutiny addendum](SCRUTINY_ADDENDUM.md).

## 1. Published chair coding: an exact match after projection

**Shelomo Izhaq Ben-Abraham and Dvir Flom, “Multidimensional color codes
for chair tilings,” Acta Cryst. A78 (2022), 359–363.**
[Full primary article](https://journals.iucr.org/a/issues/2022/04/00/ae5109/index.html),
[DOI](https://doi.org/10.1107/S2053273322004065).

Read: full article, especially §§2–4. It gives inward body-diagonal labels
for unit cubes, an eight-color 3D substitution, and a construction covering
the whole space. In each substituted block, the basic cube's color opposite
the parent color is replaced by the parent color. The article studies coding
substitution tilings; it does not give a boundary-only monotile forcing theorem.
It explicitly builds on Robinson's planar coding and Lee–Moody's
n-dimensional chairs.

### Our exact comparison (new calculation, not a claim in that paper)

Our cube labels are `(R,q)`, with 24 proper cubic rotations R and seven
local cube lower corners `q ∈ {-1,0}³ \ {(0,0,0)}`. Put `1=(1,1,1)` and define

```
π(R,q) = -R(2q+1) ∈ {-1,+1}³.
```

This is the doubled arrow from the cube center to its enclosing chair's
notch. For a subdivision digit `d∈{0,1}³`, let `s(d)=1-2d`. The published
rule in these coordinates is

```
F_d(c) = c       if s(d) = -c,
         s(d)   otherwise.
```

For **all 168×8 = 1,344 transitions**, the saved exact table satisfies

```
π(S_d(R,q)) = F_d(π(R,q)).
```

There are zero mismatches; each of the eight arrows has 21 input labels.
No fitted permutation, tolerance, or coordinate search was needed.
Thus our 168-label substitution projects exactly onto this published
eight-label substitution. Equality at one step implies equality of projected
iterates by induction.

Reproduce:

```sh
uv run --locked python strong/audit/compare_published_chair_code.py
```

[Comparison program](../audit/compare_published_chair_code.py) and
[full projection and eight-color table](../audit/published_chair_code_comparison.json).
The program pins both its input-table hash and the frozen candidate hash.
Its input is the earlier coordinate-derived table, cross-checked through
depth three in `explore_cube_substitution.py`. This new check does not
independently regenerate those coordinates.

**Limit:** a many-to-one map of substitution alphabets is not a proof that
the full tiling spaces are mutually locally derivable. It neither recovers
our internal poses from eight colors nor compares the physical matching
rules. In particular, it does not imply that an unmodified chair is aperiodic.

## 2. Fletcher: one labeled cube with orientation-encoded states

**David Fletcher, “Aperiodic Tilings with One Prototile and Low Complexity
Atlas Matching Rules,” DCG 46 (2011), 394–403; online 2010.**
[Publisher](https://doi.org/10.1007/s00454-010-9278-8),
[primary preprint](https://arxiv.org/pdf/1003.4909).

Read: preprint definitions, Theorem 1/construction, and §3 Example 2;
publisher metadata. Example 2 replaces the 21 Culik–Kari Wang cubes by
21 orientations of an asymmetrically labeled cube. It uses the cube's
48 isometries. The required configurations are specified by an atlas of
one-coronas: a tile together with all tiles touching it. The paper explicitly
notes that face matching has been replaced by this atlas; the atlas patches
have a fixed frame and cannot themselves be arbitrarily rotated/reflected.

**Relevance:** storing tile types in orientations of one 3D object has a direct
predecessor. **Difference:** removing the external neighborhood constraint
and enforcing it by one solid's boundary is an additional task. The cube's
asymmetric interior label does not itself forbid periodic cube placements.

This is a closer orientation-coding reference than the planar simulation
papers in our first search. It deserves explicit mention in any revised
account. The preprint says the work forms part of a PhD thesis; that thesis
was not retrieved in this pass.

## 3. Goodman-Strauss: exact ancestry and older variants

**“A Pair of Aperiodic Tiles in Eⁿ,” EJC 20 (1999), 385–395.**
[Author preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf),
[published version](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Goodman2.pdf).

Re-read: introduction, substitution definition, boundary markings in §2,
and connected-interior variants in §4. This already forces the chair
hierarchy, with the no-infinite-cyclic-symmetry target. In 3D its connected
variant uses two tiles, `L` and marked `X₂`. The paper explicitly permits
replacing markings by bumps/nicks. Therefore boundary recutting, by itself,
is not our distinguishing idea.

The introduction identifies two circulated predecessors: “An aperiodic
tiling in Eⁿ for each n≥2” (1995) and “An aperiodic set of n tiles in Eⁿ
for all n≥2” (1997). These were superseded; the introduction describes
multiple tiles, not a proved monotile. Exact-title searches and the author's
paper/notes indexes did not retrieve those versions. Their detailed
constructions remain unchecked.

Also read: [“Open Questions in Tiling”](https://strauss.hosted.uark.edu/papers/survey.pdf),
§3.1.3, Theorem 3.6. The survey already explains simulation by a single
rectangle with an external patch atlas. Its 2000 conjectures are historical
statements, not reliable descriptions of the current frontier.

**Required comparison:** translate the old markings and auxiliary-tile
information into our three face motifs. We have not established whether our
local rules are a known recoding, a strict extension, or a different forcing
system. The eight-color computation above does not resolve this.

## 4. Hibma: an explicit chair-to-identical-shapes exploration

**Tjipke Hibma, “3D Chair Tiles,” author's research website, undated.**
[Primary account](https://www.aperiodictiling.org/wpaperiodictiling/index.php/3d-chair-tiles/).

Read: whole page. After describing the chair hierarchy and Goodman-Strauss,
Hibma deforms the pieces toward identically shaped cross blocks and asks for
rules forcing the inherited hierarchy. The last paragraphs explicitly state
that the proposed rules are insufficient and describe periodic placements.
A supplementary hierarchy-building prescription is then given.

This is direct evidence that the chair-to-one-shape route has been explored.
It is not a proof of the target theorem. The page's existence was checked
on the date above; its original posting date and revision history were not
established. Do not infer a publication date from search-engine crawl times.
Nor should this informal page replace the original paper for statements
about Goodman-Strauss's construction.

The neighboring [polycube account](https://www.aperiodictiling.org/wpaperiodictiling/index.php/aperiodic-polycube-tilings/)
describes another substitution using tri- and tetra-cubes, then distinguishes
two tri-cubes and three tetra-cubes with pegs/slots. It does not supply the
one-solid result either. Both pages were inspected, without independently
verifying their constructions.

## 5. Older three-dimensional simulation branch

**Culik II–Kari, “An Aperiodic Set of Wang Cubes,” JUCS 1(10) (1995),
675–686.** [Primary PDF](https://www.jucs.org/jucs_1_10/an_aperiodic_set_of/Culik_II_K.pdf).

Read: introduction, Theorem 3, and final motion convention. This supplies
the 21 colored cube types used by Fletcher. Rotations are explicitly
prohibited. It is relevant finite face-rule ancestry, not 21 rotated copies
of one boundary-enforced solid under arbitrary motions.

**Peter Schmitt, “Triples of Prototiles (With Prescribed Properties) in
Space (A quasiperiodic triple in space),” Periodica Math. Hung. 34 (1997),
143–152.** [Publisher abstract and references](https://doi.org/10.1023/A:1004236910492).

Read: abstract and bibliography only; full text not retrieved. The abstract
states a conversion of arbitrary cubic domino sets to three prototiles with
a one-to-one correspondence of tilings. Its references lead to **“An
Aperiodic Triple of Prototiles” (1990), pp. 627–633**, and an in-preparation
work on versatility. These are retrieval targets, not fully audited sources.
Use the publisher's 1997 date; one discovery index incorrectly suggested
1999. This is distinct from Schmitt's screw-symmetric single-tile example.

## 6. Recent encoding results that change the comparison landscape

### Stade: local constraints versus geometric realization

**Jack Stade, “Two Tiling is Undecidable,” arXiv:2506.11628 (2025).**
[Primary preprint](https://arxiv.org/pdf/2506.11628).

Read: introduction/Theorems 1–3 and §3's construction. The paper states
undecidability for one planar prototile with edge-to-edge rules; its geometric
realization introduces a second, staple tile. Bump/bump conflicts exclude
forbidden pairings, while staples fill dent/dent gaps. This is a concrete
example of why realizing an arbitrary allowed-pair relation by geometry
can increase the number of shapes. Full reduction not independently audited.
It is not a three-dimensional monotile theorem.

### Kim: connecting disconnected tiles without increasing their number

**Yoonhu Kim, “Undecidability of Translational Tiling with 2 Polycubes,”
arXiv:2508.11725v2, revised 10 August 2026.**
[Primary text](https://arxiv.org/html/2508.11725v2).

Read: abstract, Theorem 4.1 and its concluding construction, Theorem 5.1,
and conclusion. The paper gives two connected polycubes for translational
tiling of Z³ and a conversion preserving tile count from disconnected to
connected tiles in dimension ≥3. The latter is worth auditing for alternative
constructions. Its ambient model fixes integer translations: it does not
automatically exclude additional rotated or off-grid Euclidean tilings.
We have not checked the complete connectivity/simulation proof or applied
it to our solid. Undecidability also must not be silently substituted for
the stronger assertion that every tiling has finite stabilizer.

### Greenfeld–Tao: a nonabelian monotile is not automatically a 3D solid

**“Undecidable Translational Tilings with Only Two Tiles, or One Nonabelian
Tile,” DCG 70 (2023), 1652–1706.**
[Primary preprint](https://arxiv.org/pdf/2108.07902).

Read: introduction and §11's group and Theorem 11.2. The one-tile theorem
uses a product involving Z², powers of the permutation group S₁₆, and a
finite abelian factor, tiling a specified periodic subset. This is not a
construction in the Euclidean cubic motion group. Our oriented grid
placements compose in `Z³ ⋊ O`, where O is the proper cubic rotation group;
the translation part rotates under composition. No conversion from their
particular group tile to our 3D solid has been established.

## 7. Other checked branches and unresolved retrievals

- **Mampusti–Whittaker (2020), dendrite monotile:**
  [primary text](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.12375).
  Read rules R1/R2 and the aperiodicity statement. R2 imposes red-tree
  connectivity through the permitted assembly process; the discussion uses
  magnetic interaction to represent it. It is not merely boundary fitting
  of a 3D solid. This supplements our prior Walton–Whittaker comparison.
- **Ben-Abraham–Flom's 2017 reference:** following the 2022 article's
  reference to J. Phys. Conf. Ser. 809, 012025 leads to *Color coding for
  the brick tiling*, DOI `10.1088/1742-6596/809/1/012025`. Publisher PDF
  retrieval failed. A discovery result exposed the paper text, describing
  48 labeled cubes for the brick/table generalization. Do not label this
  as an independently verified earlier version of the eight-color chair
  rule merely because the 2022 introduction calls it a preliminary report.
- **Lee–Flom–Ben-Abraham (2016):** the authors' institution identifies
  the cited paper as *Multidimensional period doubling structures*,
  [DOI](https://doi.org/10.1107/S2053273316004897).
  Metadata/abstract checked; not a full forcing-rule audit.
- The exact-title searches for Goodman-Strauss's old versions, Schmitt's
  full paper, and Fletcher's thesis remain incomplete retrieval branches.
  No private documents, correspondence, or subscription database coverage
  was available. There has been no comprehensive forward-citation census.

## 8. What follows for this project

The available evidence supports a **known-substitution, proposed-new-forcing
construction** description, with “new” still unestablished. A full duplicate
was not identified among the sources inspected. That absence is not a
probability estimate and does not justify claiming that direct prior work
is unlikely.

**Subsequent focused comparison:**
[Goodman-Strauss markings versus our face patterns](GOODMAN_STRAUSS_COMPARISON.md)
establishes exact equality of the 26 coarse pair projections, with only
90 of 234 pose assignments surviving our local exclusions. It also
identifies the parent-recognition mechanism as already present in the
old proof. The full auxiliary-piece encoding remains unclassified.

The most useful next steps are now concrete:

1. Extend the finite markings comparison to an explicit local map for the
   information transmitted by the auxiliary `I`/`X` pieces, with an inverse
   or a demonstrated obstruction. Pair projection alone does not identify
   the full sets of legal tilings.
2. Audit whether our proposed solid supplies all the enforcement missing
   from an orientation/atlas encoding. Keep the unrestricted-placement
   argument separate from the finite grid computation.
3. Continue the named retrieval branches above; an expert can help identify
   unpublished chair variants more efficiently than broad keyword searches.
4. Retain the complete-crown and exceptional-fiber problems from the earlier
   addendum. The eight-color factor neither settles nor removes them.

The v1 brief, HTML, ZIP, inquiry, and frozen geometry were preserved. The
comparison ran using `uv`; no dependencies were added. Any subsequent
revision of the review material should include these closer predecessors.

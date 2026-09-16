# Goodman-Strauss markings versus our three face patterns

*16 September 2026. Exact finite comparison and written analysis; no geometry
change or external review. Separate from the frozen v1 packet.*

**Subsequent result:** the [reconstruction follow-up](AUXILIARY_RECONSTRUCTION.md)
gives a written obstruction to any fixed-radius forward conversion that
retains the coarse chair placements. It also gives a symmetry obstruction
to a rotation-equivariant inverse on the full old `L/I` space. The earlier
open comparison below is therefore not simply awaiting a larger lookup
table. A separate discrepancy in the connected `X₂` transcription remains
to be reconciled with the source.

## Result

The correspondence extends beyond substitution pictures:

1. Our contacts project onto **exactly the 26 coarse contacts** in the old
   three contact families, when all three internal poses of the reference
   chair are included.
2. Our local parent proof uses the **same central-recognition mechanism**
   as the earlier proof. This mechanism should be attributed accordingly.
3. Our rules retain additional pose constraints: **90 of 234 possible
   pose assignments** survive the local exclusions. Equality of coarse
   pair projections does not remove these constraints.
4. We have **not** proved a local conversion between our complete tilings
   and the full old marked `L/I` or `L/X₂` tilings. In particular, we have
   not established that the auxiliary pieces' information is exactly the
   information carried by our poses.

## Source and notation

Source: Chaim Goodman-Strauss, *A Pair of Aperiodic Tiles in Eⁿ*, EJC 20
(1999), 385–395:
[published scan](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Goodman2.pdf),
[author preprint](https://strauss.hosted.uark.edu/papers/NDimPair.pdf).
The relevant published pages 388–394 were visually inspected; the scan has
no usable embedded text. Published/preprint numbering differs:

| Subject | Published | Preprint |
|---|---|---|
| Three coarse contact families | Lemma 2.2 | Lemma 1.2 |
| Markings and local contacts | §3, Lemmas 3.2–3.4 | §2, Lemmas 2.2–2.4 |
| Auxiliary chains | Lemma 4.3 | Lemma 3.3 |
| Unique grouping | Proposition 4.6 | Theorem 3.6 |
| Connected pair | §5 | §4 |

The old diagonal markings match on coincident boundary patches. Auxiliary
`I` pieces transmit markings along straight chains; the connected 3D
variant uses `L` and `X₂`. Proposition 4.6 recognizes centers from mixed-sign
outside corners, then handles an identically oriented notch neighbor as an
exception. These are the source facts used below.

Use `L` here for the **coarse** seven-cube chair and `L_GS` for its old recut
version. A coarse placement is described by an origin `t` and missing-octant
direction `s∈{±1}³`. A placement `(t,R)` of our decorated chair projects to
`(t,R1)`, with `1=(1,1,1)`. For each s there are three proper cubic matrices
R with `R1=s`. Those are the internal poses being compared.

## 1. Translating the old arrow into coordinates

Our coordinate interpretation of the old marking at endpoint `c+n` is

```
A(s,n) = (n·s) [s - (n·s)n],
```

where n is a signed coordinate unit vector and s is the chair's notch
direction. A is the diagonal arrow in the transverse square, not its
black-region outline. For the normalized chair, it is the positive
transverse diagonal at a positive endpoint and the negative diagonal at
a negative endpoint. The expression transforms equivariantly under cubic
isometries and ignores the three internal poses.

At an axial separation `2n`, matching arrows gives

```
A(1,n) = A(s,-n).
```

Solving this equation leaves exactly two notch directions: flip the
coordinate along n, or flip both transverse coordinates. The checker
verifies this for all six n and eight s: **48 tests, no discrepancies**.
Thus the old axial marking test has an explicit projection from our pose
description; it is not a rule equating our motif arrows U directly.

## 2. Exact pair correspondence

Transcribing the old coarse formulas into `(t,s)` gives this finite set G:

| Family | Origin t | Notch s | Directed coarse pairs |
|---|---|---|---:|
| (i) | `±2e_a` | `1-2e_a` | 6 |
| (ii) | `±2e_a` | `2e_a-1` | 6 |
| (iii) | `1` | any `s≠-1` | 7 |
| (iii), reversed | `-s` | the same `s≠-1` | 7 |

Here a ranges over x,y,z. The axial offsets follow published Lemma 2.2;
the later printed Lemma 3.2(i) has an inconsistent offset of 1 while
identifying the same reflection. The comparison uses the former formula,
whose reflection plane and coarse geometry agree.

The new [standalone checker](../audit/compare_goodman_strauss.py) imports no
project implementation. From our existing A/B/C descriptors it reconstructs
all 1,194 geometric contacts, the 44 fitting contacts, and the 14
impossible-face exclusions. These agree with the saved certificate.
It then compares every old coarse pair with all nine choices of the two
internal poses.

| Quantity | Exact result |
|---|---:|
| Coarse pairs G | 26 |
| Potential decorated assignments, `26×3×3` | 234 |
| Assignments fitting the immediate face rules | 132 |
| Assignments remaining after the local exclusions | 90 |
| Coarse pairs with at least one remaining assignment | 26 |
| Projected fitting contacts outside G | 0 |

Of the 26 coarse pairs, 23 have three surviving assignments and three
have seven. The 90 count is `3×30`: three root poses, each with the earlier
30 surviving neighbors. For an identity-pose root alone, the 30 contacts
project to only 20 coarse pairs. Allowing the other root poses matters.

These are finite pair statements. “Surviving” means not eliminated by the
checked local obstruction, not an independent assertion that each assignment
extends to an infinite tiling.

### A/B/C are not names for (i)/(ii)/(iii)

The checker finds that **every surviving contact in each family involves
all three motif names on the reference chair's touching unit faces**.
Consequently, all three handshake kinds participate. There is no proposed
dictionary `A↔(i), B↔(ii), C↔(iii)`; that interpretation would be wrong.
The relevant dictionary is between *whole oriented chair contacts*.

### Why pair projection is weaker than simultaneous lifting

A small computed example makes the distinction explicit. Take a normalized
coarse root with notch `+++`, and two neighbors:

| Neighbor origin | Notch direction | Family | Required root pose after exclusions |
|---|---|---|---|
| `(0,0,2)` | `--+` | (ii) | `(x,y,z) ↦ (z,x,y)` |
| `(0,2,0)` | `-+-` | (ii) | identity |

These three coarse chairs do not overlap, and every positive-area contact
in this patch belongs to G. Each root-neighbor pair separately lifts, but
there is no common root pose making both pairs survive our exclusions.

This is **not a counterexample to the full old system**: extension of the
patch using its recut pieces and markings has not been shown. It does
prove that independently existentially choosing poses for each pair loses
a compatibility condition at the shared chair.

## 3. What our three poses actually encode

For a fixed coarse root with notch `+++`, the seven decorated notch-owner
options do not mean seven distinct coarse orientations at a fixed root
pose. They project onto only three coarse directions:

| Root's internal pose R | Allowed notch-owner directions | Distinguished axis |
|---|---|---|
| `(z,x,y)` | `+++`, `--+`, `++-` | z |
| `(y,z,x)` | `+++`, `-++`, `+--` | x |
| `(x,y,z)` | `+++`, `-+-`, `+-+` | y |

For a nonidentical owner direction, the distinguished coordinate is the
one with the exceptional sign. This gives a geometric meaning to the
three-valued state. When the owner has direction `+++`, the surviving
matrix instead requires identical internal poses: the state is copied.

The checker also rotates the frozen eight-child group through all three
root poses while holding its coarse shape fixed. It finds:

- The child at the origin and the child at `(-1,-1,-1)` copy the parent's
  matrix.
- At each of the six mixed-sign child positions, the world matrix is
  independent of the parent's internal pose.

Thus, at this level, two children transmit the pose and six reset it.
This is a precise additional interpretation of our stored substitution,
not a proof that this state is identical to an old `X₂` marking.

## 4. Attribution of the parent mechanism

Compare our [local proof](../MOTIF_GROUPING.md) with the published
Proposition 4.6 (p.393). Under the projection above, our six triggers are
exactly the mixed-sign outside-corner incidences. Our use of the notch
owner, including the same-orientation exception, follows the same
recognition structure.

The work done in our note is a **verification and explicit implementation
of this mechanism for our different face rules**: 14 excluded contacts,
six finite propagation certificates, the particular C/C obstruction, and
a deterministic parent map. It should not be presented as a new conceptual
parent-recognition idea. This attribution does not invalidate those checks.

## 5. The auxiliary-piece comparison: what is and is not established

Our interpretation is that the new pose constraints provide information
needed beyond the old coarse pair projection. The multi-scale recurrence
certificate demonstrates that our information survives grouping. The old
construction uses auxiliary chains at this stage. This is a functional
comparison; an exact local translation of the two encodings is still missing.

There is also a useful count distinction. In a fixed cubic frame, the old
coarse/marked chair has eight orientations. An `X₂` marking has an axis
(three choices) and a transverse diagonal (four choices), giving twelve
orientations. Our one handedness has 24 oriented states. Reducing two
congruence classes to one therefore need not reduce the total number of
translation states: here the comparison is **8+12 versus 24**.

Our proposal is not explained by simply gluing the same integral number
of whole auxiliary pieces to each old chair. From the symmetric recutting
geometry, if v is the volume of X, then

```
volume(L_GS) = 7 + v/8 - 7v/8 = 7 - 3v/4.
```

One eighth of X is added in the missing central octant and one eighth is
removed at each of seven occupied outside corners. Recovering volume 7
would require three quarters of a whole X per chair. Equivalently, the
bulk X-to-chair ratio for the recut hierarchy is 3:4. This rules out only
that simple one-chair-plus-whole-crosses explanation. Cutting and
redistributing pieces, or grouping several chairs, remains possible.

**Unproved correspondences:**

1. A bounded-radius rule taking our decorated tiling to every nearby old
   `X₂` position and its exact marking, including exceptional infinite
   chains. A relation between pose and axis alone does not supply this.
2. A consistent inverse pose assignment for arbitrary valid old marked
   tilings. The small patch above explains why independent pair choices
   do not establish one.
3. Equality of the full tiling spaces, or mutual local derivability.
   The earlier unresolved substitution-hull versus full-rule-space issue
   must also be handled before claiming such equality.

## 6. Reproduction and research record

```sh
uv run --locked python strong/audit/compare_goodman_strauss.py
```

- [Complete matrices and conventions](../audit/goodman_strauss_comparison.json)
- [Readable 26-row table](../audit/goodman_strauss_comparison_tables.md)
- [Earlier direct prior-art audit](DIRECT_PRIOR_ART_AUDIT.md)

Inputs are the unchanged frozen candidate, A/B/C descriptors, and previous
grouping certificate; hashes are recorded in the output. The checker
recomputes the motif contacts and exclusions, but relies on the earlier
cap-to-motif validation and does not test arbitrary Euclidean placements.

During exploration the existing phase-erased periodic control was also
checked against G: 72 of its 192 directed unit-face incidences fall outside
G. Therefore that control cannot be used as a periodic counterexample to
the old coarse family constraints. No such counterexample is claimed.

The corrected assessment is **a proposed geometric realization with extra
pose constraints of an already known chair-forcing mechanism**. Neither a
complete duplicate nor full equivalence of the encodings has been established.
The next meaningful comparison is an explicit local rule for the auxiliary
cross markings, with its inverse or a demonstrated obstruction. Repeating
the substitution-picture comparison would not answer that question.

No new dependencies, frozen-coordinate edits, package rebuild, or outreach.

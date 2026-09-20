# Which distinctions survive grouping?

*19 September 2026. A symbolic analysis and a two-depth recoding witness.
The frozen reference, interactive UI and existing research witnesses are unchanged.*

**Findings.** For the fixed successful eight-child substitution, twelve
independent port amplitudes do not need twelve distinct depths. The exact
region preserving both the 44 fine contacts and the 44 full parent contacts
is the complement of **five forbidden equality patterns**. A concrete
assignment with just **two positive depth magnitudes** lies in that region.
An independent coordinate replay confirms its complete contact sets and
excludes odd parent offsets.

For aligned parent contacts, the entire dependence on the twelve amplitudes
reduces to **two collective phase tests**. Applying the aligned scale
operator again gives exactly the same symbolic predicates, for every
amplitude assignment. This explains a stable information reduction rather
than literal transport of twelve numerical depth values.

These are statements about a specified port model and recoding family, not
a new classification of monotiles or a new proof for arbitrary physical
placements. The underlying matching system remains the one compared with
Chair44; no novelty or discovery-priority claim is made.

## 1. Coordinates on the remaining freedom

The [cycle-balance analysis](CONSTRAINT_BALANCE.md) gives a geometric sign
chi_i=det[u_i,v_i,n_i] at each port. Every solution of the required substitution
contact equations can be written

    x_i = chi_i a_{c(i)},

where c(i) is one of twelve connected components and x_i is the signed
physical depth key. Number components by the absolute frozen key, 1..12.
The amplitudes a_1,...,a_12 are therefore **chirality-corrected amplitudes**;
they are not simply the frozen positive key names.

For positive old keys, the chi signs are

    (-,+,+,-,-,+,+,-,+,-,+,-).

On a proper grid contact between components r and s, the depth equation is
just a_r=a_s. Thus a complete interface is described by a partition of the
twelve components: every block must have a common amplitude. Numerical
spacing, order and ratios of distinct amplitudes are irrelevant here.
Zero values are allowed by the homogeneous algebra, but excluded when
using these equations to describe nonzero physical caps.

## 2. Exactly five ways to accidentally admit a forbidden contact

Write the following five propositions; the equalities in each row must
hold **simultaneously** for that proposition to be true.

| Proposition | Simultaneous equalities |
|---|---|
| E1 | a1=a6, a2=a4, a3=a8, a5=a7 |
| E2 | a1=a8, a2=a7, a3=a6, a4=a5 |
| E3 | a1=a2, a3=a4, a5=a6, a7=a8 |
| E4 | a1=a3, a2=a5, a4=a7, a6=a8 |
| E5 | a9=a12, a10=a11 |

For this fixed substitution and port layout, the following are equivalent:

1. None of E1,...,E5 holds.
2. The fine allowed-contact set is exactly the original 44.
3. The **full** integer-offset parent contact set is exactly the original 44
   doubled placements, with no odd-offset contacts.

This is a finite symbolic classification valid for all real amplitude
assignments, not just the sampled two-depth assignments.

**How the classification is obtained.** Reconstruct all 1,194 fine and 6,801
macro geometric contacts from the frozen faces. Merge the component variables
that each interface requires to be equal. The fine contacts yield 19 distinct
predicates, including the unconditional one; the full macro contacts yield
21. A stronger equality pattern contains all equalities of some weaker one.
Remove those redundant forbidden patterns. Both catalogues have exactly the
five minimal patterns above. Each minimal pattern has an actual contact
witness; their poses are saved in the JSON. The empty predicate accounts for
44 contacts in both catalogues. Thus avoiding those five patterns is both
necessary and sufficient, with equality of sets, not merely equality of counts.

A single collision a_r=a_s usually does not admit an unwanted whole-chair
contact. An entire row of coincidences is needed. The bad sets are four
linear subspaces of codimension four and one of codimension two in R^12.
Their complement is open and dense. Highly compressed assignments can also
lie in this complement: it is not necessary to keep every pair distinct.

Each row can alternatively be read as invariance of the amplitude coloring
under an explicit involution exchanging its listed pairs. Breaking all five
of these particular identification patterns is sufficient. This is a
statement about constraint patterns, not five rigid symmetries of the solid.

## 3. What an aligned parent actually reads

Use the phase families already identified in
[FOLLOWUP_REFLECTIONS](FOLLOWUP_REFLECTIONS.md#3-where-the-three-state-information-lives),
and form three four-component words:

    v0 = (a1, a2, a4, a6)
    v1 = (a3, a5, a7, a8)
    v2 = (a9, a10, a11, a12).

These are the three phase columns after correcting chirality. They are a
bookkeeping of the existing phase families; they do not assert that a single
uniform cyclic permutation of key names describes rotating the chair.
The earlier investigation explicitly found that uniform-permutation shortcut
fails at individual port occurrences.

The aligned parent reads only

    P: v0 = v1                (the proposition E4)
    Q: v0 = v1 = v2.

The 1,194 coarse relative placements split into three disjoint classes:

| Relative placements | Predicate for the parent to fit |
|---:|---|
| 44 | Always true within the required-equation solution space |
| 67 | P |
| 1,083 | Q |

Since Q implies P, the resulting contact counts are:

- 44 when v0 differs from v1;
- 111 when v0=v1 but v2 differs;
- 1,194 when all three words coincide.

Thus it is a **collective phase distinction** that an aligned parent carries:
one surviving difference anywhere between v0 and v1 already blocks the two
classes of additional aligned contacts. Requiring every row to preserve all
three phase values is stronger than necessary.

The loss of the other tests from this aligned census does not make them
irrelevant. The full parent census includes 5,607 odd-offset placements.
Its minimal forbidden patterns recover precisely E1,...,E5. Information that
is not visible in the aligned-contact count also protects registration of
the parent grid. Checking only 44 aligned contacts would miss this role.
For example, among binary amplitude partitions 1,920 give 44 aligned parent
contacts, but only 1,224 preserve the fine and full macro contact sets.

## 4. A symbolic fixed point after one grouping

Let F_0(t,R;a) be the fine interface predicate for relative placement (t,R),
as a function of the twelve amplitudes. For an array F of such predicates,
define T(F) by substituting the fixed eight children on each side and taking
the conjunction of every cross-boundary child contact predicate.

Direct macro-face reconstruction and this child-contact computation agree:

    F_1 = T(F_0).

A second symbolic induction gives the stronger identity

    T(F_1) = F_1,

as equality of required partitions for **each of the 1,194 relative poses**.
It holds before choosing amplitudes. By induction, F_n=F_1 for every n>=1,
for aligned successive supertiles of the fixed template.

The independent JavaScript replay also constructs the actual 64-child
supertiles (448 cubes and 3,072 exposed ports) and checks every aligned
second-level predicate directly against F_1.

The aligned rule transformation therefore reaches a stable reduced
description after one step. Depending on the amplitudes, its contact
language has 44, 111 or 1,194 placements. This does **not** establish unique
recognizability, common parity or tilability for the 111-contact rule or for
arbitrary edited assignments. The operator substitutes a prescribed template;
it does not prove that every legal assembly must group that way.

## 5. Two depths suffice in this recoding family

Take

    (a1,...,a12) = (1,2,1,1,1,1,1,1,2,1,1,1).

In other words, make components **2 and 9** high, and the other ten low.
Then E1–E4 each fail at the pair containing component 2, and E5 fails at the
pair containing component 9. This proves symbolically that the assignment
preserves both complete contact sets.

The phase words in this particular example are

| Phase column | Four-component word |
|---|---|
| v0 | (1,2,1,1) |
| v1 | (1,1,1,1) |
| v2 | (2,1,1,1) |

Two symbols encode three distinct words. Here the location of the high
entry distinguishes the columns; a third numerical depth is unnecessary.
Pairwise distinct phase words are illustrative of this witness, not claimed
as a necessary condition for every admissible recoding.

There is a simple family of **32** such witnesses: choose one high component
among 1..8 and one among 9..12. The first choice breaks all four perfect
matchings E1–E4 on the first eight components. The second breaks E5 on the
last four. Every other component is low.

Exhaustively checking all 2^11=2,048 binary partitions, with component 1 fixed
to the first symbol to remove global color renaming, gives **1,224** preserving
assignments. Only one monochromatic partition is included. These numbers count
amplitude partitions, not tile placements or distinct physical congruence
classes.

For the displayed witness, positive old keys map to new signed keys as

    (-1, +2, +1, -1, -1, +1, +1, -1, +2, -1, +1, -1).

Extend the map oddly to negative old keys. The complete 192-key assignment
is saved in the report. Many bumps and recesses change polarity, so this is
not obtained by replacing every old positive key by an arbitrary positive
number. Its maximum absolute depth key is 2.

The switched amplitudes are positive, so the sign of each new physical key
is its local chirality. All 13,312 opposite-key cap-frame correspondences
are proper and have integer translations. This retains the earlier local
handedness mechanism. The signed key sum is zero; total cap volume cancels,
and the maximum cap height is below the frozen candidate's bound.

One switched amplitude value would allow every proper geometric contact,
so two values are minimal for preserving the reference atlas **within this
positive, chirality-aligned recoding family**. This is not a minimum-depth
theorem for arbitrary solids or for recodings using one physical magnitude
with both signs of switched amplitude.

## 6. Evidence, implications and remaining scope

Primary analysis:

```sh
uv run --locked python strong/audit/analyze_information_transfer.py
```

It uses the frozen-coordinate audit's geometry helpers, reconstructs all
predicates from complete faces, derives the five-pattern antichain, checks
the symbolic scale identity by child contacts, and enumerates the binary
partitions. It does not depend on the UI's compressed condition table or
rerun the original 6,561-template synthesis.

Independent implementation replay:

```sh
node strong/audit/crosscheck_information_transfer.cjs
```

It imports no project geometry implementation. Starting from raw integer
port coordinates, cube centers and independently generated signed rotations,
it checks all 1,194 fine and 6,801 macro symbolic predicates, plus the 1,194
aligned second-level predicates. Original keys and the two-depth witness
allow exactly the same contact poses. It also checks the constant-amplitude
control and all opposite-key cap maps of the new witness.

- [Symbolic results and full predicate catalogues](audit/information_transfer.json)
- [Independent replay results](audit/information_transfer_crosscheck.json)

Matching the complete proper-grid contact atlas transfers the existing
abstract grid-rule consequences to this recoding by the evident identification
of placements. No new Lean theorem has been built for the changed port keys.
The two-depth geometry has not replaced the frozen reference, and the full
arbitrary-Euclidean analytic argument has not been independently re-audited
for it. The finite results are not a certification of a printed object.
The 111-contact regime remains unclassified as a tiling system.

The answer to the motivating question is therefore concrete: the hierarchy
carries **relations among spatially distributed phase words**, while the
complete boundary also retains enough distinctions to prevent misregistration.
Twelve distinct numerical labels were a convenient maximal encoding of this
information; they are not its minimum physical alphabet.

**Subsequent shape investigation:** [a scalene triangular cubic port](PORT_SIMPLIFICATION.md)
realizes the displayed two-depth assignment with a lower-degree surface,
an explicit open-patch rigidity argument and a separate candidate snapshot.

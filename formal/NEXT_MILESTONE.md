# Next internal milestone: universal grouping and legal deflation

*16 September 2026. Steps A, B and C completed; subsequent translation exclusion also verified.*

## Assessment

The completed [recurrence milestone](README.md) settles normalized pairwise
contacts: all integral offsets are covered, and macro contacts are exactly
doubled fine contacts with the same orientation. The independent review found
no material defect within that scope. The next priority is to connect those
pairwise results to **every legal infinite grid tiling**.

| Dependency | Current evidence |
|---|---|
| Arbitrary physical placements imply a grid | Written geometric proof, exact checks, internal reviews |
| Normalized macrocontact recurrence | Lean theorem, kernel-checked certificates, independent agent review |
| Arbitrary grid-tiling semantics, covariance and actual neighbors | Lean theorems; [completed step A](GRID_TILING_BRIDGE.md) |
| Unique grouping of all legal grid tilings | [Lean universal grouping](UNIVERSAL_GROUPING.md), linked to the actual frozen ports |
| Global parity and repeated legal deflation | [Lean deflation theorem and finite-depth iteration](LEGAL_DEFLATION.md) |
| Exclusion of nonzero integer translation periods | [Lean halving and descent](TRANSLATION_EXCLUSION.md) |
| Existence and finite symmetry | Separate written arguments; not the completed Lean milestone |

This review identifies formalization priorities. It does not identify a new
counterexample or establish a defect in the existing written grouping proof.

## Target statement

> Every legal grid tiling has a unique partition into the specified
> eight-child groups. All parent origins have one common residue modulo two.
> After choosing that common origin and halving parent coordinates, the
> parent placements form another legal tiling of the same oriented rule system.

The starting tiling must be arbitrary. Do not restrict it to patches generated
by the substitution, assume a parent partition, or require every pair of tiles
to touch. Existence of a legal infinite tiling remains a separate obligation.

## A. First bounded step: placements and arbitrary legal tilings

**Completed:** see [the result record](GRID_TILING_BRIDGE.md), including exact
scope, source map, verification and the next contact-exclusion step.

Define `LegalTiling` through actual placements, with one owner per lattice
cube and matching on every shared exposed face. Distant placements are
permitted. Preserve the 24 decorated orientations and consistency between
each tile's placement and all of its owned cubes.

Prove that common translations and proper cubic rotations preserve these
conditions. This requires composition and inversion of frames and their
actions on cube lower corners, face centers, normals, ports and ordered axes.
It lets us apply the existing normalized contact theorem to any neighboring
pair in a tiling. Prove that every exposed face has an actual neighboring
owner from coverage, rather than taking a supplied neighborhood as complete.

**Acceptance criterion:** normalized contact results apply to arbitrary
placed neighbors of a precisely defined legal grid tiling, with no hierarchy
or parity premise in that definition.

## B. Universal unique parent partition

**Completed:** see [the proof record](UNIVERSAL_GROUPING.md). The Lean
development follows the local exclusions and forcing chains without relying
on complete-star enumeration or assuming motif-rule equivalence.

Use the existing [local parent argument](../strong/MOTIF_GROUPING.md) and
[certificate](../strong/audit/motif_grouping_certificate.json):

1. Start with all 44 immediately compatible contacts. Derive the 14
   impossible-face exclusions using coverage and pairwise incompatibility.
2. Check the six trigger propagation chains and the exceptional identical-
   orientation notch case as consequences for an arbitrary legal tiling.
3. Define the parent of a tile from its actual neighbors: itself when a
   trigger occurs, otherwise its notch owner.
4. Prove that each parent is a group center, the preimage of each center
   consists of its eight specified children, and those preimages partition
   the tiling uniquely. Prove compatibility with translating the tiling.

Reuse the frozen-port contact semantics already in Lean. The A/B/C motif
description currently has its own Python-checked correspondence with those
ports. Either formally prove that correspondence before using motif rules,
or verify the grouping witnesses directly against the existing port model.
Do not silently introduce a second assumed matching system.

**Acceptance criterion:** a theorem about a unique partition of every legal
tiling, with finite certificates proved applicable to those tilings. The 33
enumerated stars may serve as a cross-check; they need not replace the shorter
local parent proof.

## C. Common parity and legal deflation

**Completed:** see [the proof record](LEGAL_DEFLATION.md). Coverage and unit
cube paths establish common parent parity; exact support and contact
recurrence prove legality after halving. The result is iterated at every
finite depth, conditional on the initial legal tiling.

Show that the groups cover the lattice without overlap and their adjacency
graph is connected. Apply normalized recurrence through the frame-change
lemmas. Neighboring parent origins differ by even vectors; connectivity gives
one common residue class in `Z³ / 2Z³`.

After removing that residue and dividing coordinates by two, prove coverage,
unique cube ownership, and all required matching conditions anew. Thus the
output meets the same `LegalTiling` definition as the input. This closes the
step needed to iterate grouping without additional alignment assumptions.

**Acceptance criterion:** the target statement above, with an axiom audit and
an explicit distinction between checked local certificates and universal
tiling arguments. Preserve the first milestone's frozen construction.

## Subsequent priorities

1. Iterate the intrinsic grouping to exclude translation periods in the
   grid model. Carry symmetry preservation through the actual parent map.
   **Completed for translations:** periods inherit center invariance and
   halve under legal deflation; well-founded descent proves they are zero.
2. Establish nonemptiness through legal expanding substitution patches and
   a compactness argument, so the universal conclusion is nonvacuous.
3. Complete the finite-symmetry deduction and connect the grid theorem to the
   exact physical solid through the geometric bridge.

Existence can be developed alongside grouping because it is a separate proof
branch. Full classification of the tiling space, further dynamical deductions,
geometry simplification and additional visualizations are not prerequisites
for this milestone. Prior-art assessment remains separate from correctness.

## Review provenance

The coordinating agent reviewed the current Lean definitions, dependency
audit, local grouping note and certificate structure. The fresh milestone
reviewer was consulted again and independently recommended the same order:
precise arbitrary-tiling semantics and frame covariance first, then universal
grouping, followed by parity and deflation. No proof source or frozen artifact
was changed during the original planning review. The subsequent step-A
implementation is recorded separately in `GRID_TILING_BRIDGE.md`.

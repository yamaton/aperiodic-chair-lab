# At most 24 proper grid symmetries

*16 September 2026. Verified with the pinned Lean 4.34.0 toolchain.*

For every `LegalTiling T`, its complete set of proper grid symmetries has
at most 24 elements. The starting tiling has the unchanged coverage,
unique-ownership and frozen-port matching definition; no hierarchy,
finite-symmetry or existence premise was added.

## Exact statements

In [Symmetry.lean](Chair/Symmetry.lean),

```lean
def GridSymmetry (T : GridTiling) (g : GridMotion) : Prop := moveTiling g T = T
```

`GridMotion` already means an integer shift and a proper cubic frame.
The action is on the full set of decorated placements. Identity, composition
and inverse preserve `GridSymmetry`; the ambient group laws are those proved
in [Frames.lean](Chair/Frames.lean). No additional group library is required.

The two final formulations are:

```text
LegalTiling.symmetry_list_bound:
  any duplicate-free list of grid symmetries has length ≤ 24

LegalTiling.symmetries_finite:
  ∃ gs : List GridMotion, gs.length ≤ 24 ∧
    ∀ g, g ∈ gs ↔ GridSymmetry T g
```

The second statement establishes an exhaustive finite list, including both
directions of membership. It does not assume that the symmetries were already
enumerated or finite. The list is obtained by classical choice, not by a
decision procedure for an arbitrary infinite tiling. The first statement
independently expresses the bound on distinct elements. Together these give
the ordinary group-order conclusion without introducing Mathlib cardinality
types. They do not say that the bound is attained or that every group is trivial.

## Proof

If `g` and `h` have the same frame, their composition `g ∘ h⁻¹` is exactly
the translation by `g.shift - h.shift`. If both are symmetries, so is that
translation. The existing `LegalTiling.translation_period_zero` forces its
vector to vanish; hence `g = h`.

Thus the frame map is injective on all symmetries. Mapping a duplicate-free
list through this map gives a list of distinct entries from the 24 listed
rotations, so its length is at most 24; their order is irrelevant. For an
exhaustive list, choose one symmetry for each rotation that occurs and omit
rotations that do not occur. Frame injectivity proves that this list contains
every symmetry. Its length is bounded by the length of the rotation list.

## Scope and validation

The full verifier passed deterministic regeneration, the incremental build,
the independent contact-table comparison and **62 theorem axiom audits**.
All audited dependencies lie in `propext`, `Classical.choice`, `Quot.sound`.
There are **41 Lean source files** in the updated
[verification manifest](verification.json). No finite geometric certificate,
new axiom, native-evaluation hook or dependency was introduced.

```sh
uv run --locked python formal/verify.py --lake /path/to/lean/bin/lake --write-report
```

This addition was implemented by the coordinating AI assistant. A subsequent
[fresh independent agent review](../strong/review/FOLLOWUP_INDEPENDENT_REVIEW.md)
found no material defect, reproduced direct Lean checks and the axiom audit,
and checked all manifest hashes. Earlier compiled modules were reused.
This is not human review. The frozen construction is unchanged.

Initial tiling existence remains outside this Lean development. Arbitrary
Euclidean placement, reflections, and symmetries of the unlabelled physical
tile family still require the geometric and representation bridge. In
particular, the present theorem is not yet a formal finite-symmetry theorem
for the curved solid. See the [current dependency table](../docs/PROOF_STATUS.md)
and the [short registration manuscript](../strong/review/CURVED_GRID_NOTE.md).

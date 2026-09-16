# Common parent parity and legal deflation

*16 September 2026. Completed and verified with Lean 4.34.0.*

## Result

For every `LegalTiling T`, Lean proves that all recognized parent origins
lie in one residue class modulo two. Subtracting a representative of that
class and halving the parent translations gives another `LegalTiling` of
the same decorated fine chair, with the same proper frames.

The main theorem is `Chair.LegalTiling.grouping_deflation` in
[Hierarchy.lean](Chair/Hierarchy.lean):

```text
LegalTiling T →
  ∃ origin,
    (∀ c, groupCenters T c → SameParity origin c.shift) ∧
    LegalTiling (deflated (groupCenters T) origin).
```

Here `SameParity a b` means `b = a + 2k` for some integer vector `k`.
`deflated P origin` contains precisely those placements whose translation
`t` becomes `origin + 2t` in `P`, retaining their frame. The theorem assumes
only the original `LegalTiling`; it derives both the parent macro tiling and
its alignment.

The noncomputable `iteratedDeflation` chooses an allowed origin at each level.
`iteratedDeflation_legal` proves legality at every natural-number depth, and
`iteratedDeflation_step` identifies each successor as the actual grouping
and deflation of its predecessor. All these statements are conditional on
an initial legal tiling. They do not prove that one exists.

## Proof chain

1. **Assemble the groups.** Their occupied cubes are exactly the union of
   their eight fine children. Universal unique grouping gives coverage and
   unique ownership for the assembled macro tiling. Every macro boundary
   face, including its complete port record, is an uncancelled child face,
   so interface matching is inherited from the original tiling.
2. **Propagate parity.** Choose the owner of the origin cube. Walk along
   unit coordinate steps to any other cube; explicit integer induction
   proves that all cubes are reachable. At each step, distinct owners have
   opposed exposed faces and hence a true macro contact. Recurrence makes
   their relative translation even. Frame covariance turns that into equal
   ambient origin parity. Coverage supplies all owners along the path.
3. **Preserve coverage and uniqueness after halving.** The support of an
   inflated coarse placement is exactly its occupied cubes expanded into
   two-by-two-by-two blocks. The equality is checked for all 24 orientations
   and transported to arbitrary translations. Sampling `origin + 2q`
   transfers coverage and unique ownership to every coarse cube `q`.
4. **Preserve matching.** Opposed coarse faces supply adjacent occupied
   coarse cubes. Suitable subcubes in their doubled blocks are adjacent
   macro cubes, giving an actual macro contact. Exact contact recurrence
   then supplies a complete fine contact, including the required port match.

Two details matter for future work. Rotating a cube changes its lower corner
by a sign-dependent offset; the scaling check includes this offset. Also,
matching is obtained from the contact recurrence: the proof does not assume
that simply scaling individual port positions turns the macro decoration
into the fine decoration.

## Sources

| File | Role |
|---|---|
| [SolidTiling](Chair/SolidTiling.lean) | Legal tilings of a fixed discrete solid and the predicate of actual group centers |
| [SolidContacts](Chair/SolidContacts.lean) | Adjacent owners give contact; opposed faces give adjacent occupied cubes |
| [MacroAssembly](Chair/MacroAssembly.lean) | Universal grouping yields a legal tiling by the actual macro solid |
| [MacroBoundary](Chair/MacroBoundary.lean) | Exact exposed macro boundary in every proper placement |
| [MacroParity](Chair/MacroParity.lean) | Integer-grid connectivity and common macro-origin parity |
| [Scaling](Chair/Scaling.lean) | Exact doubled support, block ownership, adjacency and relative-motion identities |
| [Deflation](Chair/Deflation.lean) | An aligned legal macro tiling deflates to a legal fine tiling |
| [Hierarchy](Chair/Hierarchy.lean) | Discharges alignment, combines the result and iterates it |

## Verification and review

The full `formal/verify.py --write-report` run passed through `uv`: three
deterministic regeneration checks, the complete project build, comparison
with the independent contact table, and 44 theorem axiom audits. The updated
manifest at this step contained 36 Lean source hashes; later additions extend
it. All audited dependencies are among
`propext`, `Classical.choice`, and `Quot.sound`. No admitted proof, custom axiom
or native-evaluation dependency was added. Frozen geometry and the preceding
finite contact/grouping certificates are unchanged.

Three agents implemented assembly, boundary/parity, and scaling separately;
the coordinating agent implemented generic solid contacts, deflation and
iteration, and reviewed the integration. The scaling and parity contributors
reviewed the deflation argument. The assembly contributor reviewed deflation,
iteration and the parity proof. No material issue was reported. This is
internal cross-review, not a fresh independent review of the complete proof
or external mathematical validation.

The macro-boundary kernel check took approximately 109 seconds; the other
new structural modules compiled quickly. Earlier finite proof batches were
reused, so this was not a cold whole-project rebuild. Avoid launching two
builds that both need to compile `MacroBoundary`: its finite check is
memory-intensive. Reproduce from the repository root:

```sh
uv run --locked python formal/verify.py --lake /path/to/lean/bin/lake --write-report
```

This session used `/tmp/lean-4.34.0-linux/bin/lake`. The completed grouping and
deflation work was subsequently committed together locally at the user's
request. No push or outreach was performed.

## Next obligations

**Subsequent progress:** period halving and nonzero integer-period exclusion
are now proved in [TRANSLATION_EXCLUSION.md](TRANSLATION_EXCLUSION.md). The
following paragraph records the next step identified at this milestone.

Next, carry a translation period through the intrinsic grouping and legal
deflation: common parity should force that period to be even, and deflation
should give the half-period in the next legal tiling. Iterating this deduction,
or using descent on a nonzero period's integer norm, would exclude all nonzero
grid translation periods. That deduction is not yet formalized here.

Nonemptiness still needs a separate construction/compactness proof. Finite
symmetry, arbitrary Euclidean grid enforcement, and the connection to the
exact curved physical solid also remain separate formal obligations. This
milestone does not certify a mesh or manufactured approximation, or resolve
the prior-art assessment.

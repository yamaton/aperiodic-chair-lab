# Universal grouping of legal grid tilings

*16 September 2026. Completed and verified with Lean 4.34.0.*

## Target and attribution

**Proved:** one level of intrinsic grouping. Every legal tiling of the
integer cube grid partitions uniquely into the specified eight-chair groups.
The input has no parent assignment, substitution history or parity premise.
This implements the local recognition argument in
[`strong/MOTIF_GROUPING.md`](../strong/MOTIF_GROUPING.md), whose conceptual
mechanism is attributed there to Goodman-Strauss's chair construction.
Formal verification of this particular decorated rule system is a correctness
result, not a claim of a new grouping mechanism or an assessment of novelty.

## Proof architecture

1. **Actual neighbors.** The completed grid-tiling bridge supplies an owner
   across each exposed face and normalizes its exact placement into the
   certified 44-contact language.
2. **Finite occurrences.** `Occurrences.valid_occurrences` establishes that
   every required face has an occurring option, and that no pair with a
   checked incompatibility witness can occur together. It holds around every
   actual tile of any `LegalTiling`.
3. **Fourteen exclusions.** Each excluded contact obstructs one exposed face:
   every possible owner of that face conflicts with the assumed contact.
4. **Six forcing chains.** Starting from any mixed-sign diagonal trigger,
   seven singleton-coverage steps force the same eight-neighbor star. Seven
   neighbors join the central tile to form its eight-child group; the eighth
   neighbor is an external notch owner. Every other contact is excluded from
   a central star.
5. **Notch recognition.** A noncentral tile has one notch owner. Six notch
   orientations immediately give a reciprocal trigger at that owner. In
   the same-orientation case, one exposed outer face forces an axial neighbor,
   which supplies the owner's trigger.
6. **Parent consistency.** Every outer child of a group is noncentral and
   recognizes that group's center as its notch owner. This gives a unique
   containing group and hence a partition of all actual tiles.

The universal implications concern arbitrary predicates of occurrence, with
coverage and incompatibility supplied by a legal tiling. They are not an
enumeration of finite patches followed by an assumption of extendibility.
No enumeration of the 33 complete stars is used by this proof.

The main statements in namespace `Chair.ChairGrouping` are:

- `universal_grouping`: each actual tile belongs to a unique center's group.
- `parent_fiber`: membership in a center's group is exactly equality of
  the intrinsic parent to that center.
- `group_has_eight_distinct_tiles`: the group has exactly eight distinct
  decorated placements after any proper grid motion.
- `center_iff_group_occurs`: a full occurrence of the specified pattern is
  exactly a recognized center. The trigger condition does not restrict the
  class of candidate groups.
- `group_partition_unique`: any covering by occurrences of that pattern
  uses exactly the recognized centers; disjointness follows from unique
  membership. A preselected partition is not a premise.
- `parent_map_unique` and `parent_covariant`: the parent assignment is unique
  and commutes with every proper grid rotation and integral translation.

## Finite data and trust boundary

[`generate_grouping.py`](generate_grouping.py) reads the old motif certificate
for stable IDs, proposed face options, exclusions and forcing traces. The
generated Lean module checks the data against the already defined frozen
cube/port geometry:

- Every face used in the argument belongs to the actual fine solid.
- Face-option membership is equivalent to actual opposing-face contact.
- All accepted normalized contacts are represented by the 44 motions.
- Every claimed conflict has an actual overlapping-cube or mismatched-port
  witness. Completeness of the conflict table is not assumed or needed.
- The derived group has eight distinct placements and is a permutation of
  the eight frozen substitution children, including their decorated frames.
- Every inverse or relative-motion identity used in parent recognition is
  kernel checked.

The motif descriptions are therefore proposals for certificates, not an
additional assumed matching system. The original frozen JSON-to-Lean export
remains checked by deterministic Python regeneration, outside Lean itself.

## Sources

| File | Role |
|---|---|
| [GroupingData](Chair/GroupingData.lean) | Generated finite tables and kernel-checked geometric witnesses |
| [Neighborhood](Chair/Neighborhood.lean) | Normalized tilings and generic catalogue/compatibility bridge |
| [Occurrences](Chair/Occurrences.lean) | Actual legal tilings satisfy finite propagation premises |
| [LocalRules](Chair/LocalRules.lean) | Generic exclusion and forcing-chain soundness |
| [LocalGrouping](Chair/LocalGrouping.lean) | Concrete exclusions, central stars, notch uniqueness and exceptional case |
| [Partition](Chair/Partition.lean) | Abstract parent-fiber and unique-partition deductions |
| [Grouping](Chair/Grouping.lean) | Concrete universal grouping and parent theorem |

## Validation and review

At this step the full verification driver passed: three deterministic regeneration checks,
the Lean build, comparison with the independent 44-contact table, and an
expanded audit of 31 theorem declarations. All dependencies remain among
`propext`, `Classical.choice`, and `Quot.sound`; no admitted proof, custom axiom
or native-evaluation dependency was added. The manifest now records 28 Lean
source hashes (later additions extend the manifest). Existing recurrence certificates and frozen geometry are
unchanged. This run reused earlier compiled proof batches and was not a cold
rebuild of the entire project.

Three agents contributed finite certificates, local propagation and partition
proofs; the coordinating agent implemented the arbitrary-tiling bridge and
reviewed the integration. The finite-data contributor cross-reviewed that
bridge, the propagation contributor reviewed the concrete partition proof,
and the partition contributor reviewed the bridge and propagation. None
reported a material issue. This is internal cross-review, not fresh independent
review of the entire proof or external mathematical validation.

Reproduce from the repository root using the pinned Lean 4.34.0 toolchain:

```sh
uv run --locked python formal/verify.py --lake /path/to/lean/bin/lake --write-report
```

This session used `/tmp/lean-4.34.0-linux/bin/lake`. The preceding grid-tiling
bridge was committed locally as `ff440f1` before this work began. The grouping
addition was subsequently committed locally with the deflation development
at the user's request; no push or outreach was performed.

## Remaining obligations

**Subsequent progress:** common parity and legal deflation are now proved;
see [LEGAL_DEFLATION.md](LEGAL_DEFLATION.md). The following paragraph records
the obligations identified when grouping was completed.

Grouping is one step toward repeated deflation. The next step is to show
that all group origins have common parity and that removing this parity
and halving coordinates yields another `LegalTiling`. Iteration, existence
of a legal infinite tiling, finite symmetry, and the connection to the exact
curved physical solid remain separate formal obligations. The grouping result
alone cannot establish that the tiling space is nonempty.

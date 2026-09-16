# Chair44: exact overlap and proof-scope comparison

*16 September 2026. Initial assessment, not a validation of the full physical
theorem. No author or reviewer contacted.*

## Conclusion

**Follow-up completed:** the [proof comparison](CHAIR44_PROOF_COMPARISON.md)
independently reconstructs Chair44's atlas from its pyramid geometry, checks
Lean literal/solid correspondence, proves a written grid-model bijection,
and adapts its retained-core lemma to shorten our registration argument.
It includes a [deeper formal-source audit](CHAIR44_FORMAL_SOURCE_AUDIT.md).
The subsequent [pinned build and fresh axiom audit](CHAIR44_BUILD_REPRODUCTION.md)
also passed without proof-source edits: 169 reproduced axiom lines match the
published log. The [off-grid companion replay](CHAIR44_COMPANION_REPLAY.md)
passed independently. The complete release control script has one packaging
failure from a missing historical archive; its four logical negative controls
and positive scope check passed. These results supersede the initial
source-only status described below.

Ioannis Tsiokos's **A Strongly Aperiodic Monotile in Three Dimensions** is a
directly overlapping construction. Exact rational comparison identifies the
same decorated-chair substitution and contact system after a coordinate
change, a panel-local change of feature offsets, and a signed key relabelling.
This is substantially stronger evidence than coincident counts or pictures.
The physical solids differ: Chair44 uses square pyramids; ours uses asymmetric
polynomial caps.

The release also supplies Lean source whose endpoint genuinely states a
stronger theorem than our current formal result: physical tiling existence,
arbitrary Euclidean placements including reflections, and a full symmetry
group of order at most 24. We inspected definitions and proof endpoints and
subsequently reproduced the pinned development's build and axiom report.
This verifies the formal proof under its disclosed native-evaluation trust
boundary. We have not independently audited every geometric definition and
proof against the manuscript, and this is not independent human review.

Our current findings should therefore be presented as a comparison and
verification effort. The matching system is not a defensible differentiator
from this published construction. A different physical realization or a
smaller proof may be useful, but does not by itself establish a new monotile
discovery of comparable significance.

## Sources and versions

- [Version 1, Zenodo 22734468](https://zenodo.org/records/22734468), publication
  date 15 September 2026; API creation time
  `2026-09-15T23:30:43.260897+00:00`.
- [Version 2, Zenodo 22792358](https://zenodo.org/records/22792358), publication
  date 16 September 2026; API creation time
  `2026-09-16T09:36:26.413556+00:00`. Its downloaded PDF has MD5
  `9275314e2442cab134dcb31719dd75fc`, matching the API, and SHA-256
  `47c12cd2fee428d7a6ef6c43ac3f0997bb4f977395364b1d37336c76d7493120`.
- [Pinned public source release](https://github.com/ioannist/six-birds-tiles/tree/137e46b15d36266c37879478cfc62af6e4469147),
  commit `137e46b15d36266c37879478cfc62af6e4469147`. Both Zenodo descriptions
  identify this release checkpoint. The paper separately describes its
  mathematical baseline as `d90313a717`; these identifiers are not interchangeable.
- Version 2 PDF, API metadata, comparison script and exact output are listed
  below. Source inspection refers to the pinned release, not a moving branch.

The user-supplied repository-root PDF was initially zero bytes, then became
complete during this comparison. Its MD5 is
`e9d5e2e9622d2a5228aa86392b787b26`, matching the version 1 API and our separate
download. We left that file untouched. Version 2 updates exposition and
cross-references, including the solid's panel recipe; our exact-data checks
remain pinned to the source commit above. The X post itself was not
accessible; no conclusion relies on its contents.

On the user's follow-up, both repository-root PDFs were checked: version 1
is 989,630 bytes and version 2 is 999,058 bytes. Each matches the size and
MD5 in its respective saved Zenodo API record. Root version 2 is byte-for-byte
identical to `sources/tsiokos-chair44-v2.pdf`, already used for this assessment.
Both user-supplied files remain untouched; this confirmation does not change
the mathematical comparison.

## Exact correspondence

Let `e=(1,1,1)` and `P(x,y,z)=(y,z,x)`. The point-coordinate conversion is
`x_ours=P(x_theirs-e)`. This cyclic permutation is a proper rotation.
For a fine contact with rotation `R` and translation `t`, the converted pose is

```text
R_ours = P R P^-1
t_ours = P(t + R e - e).
```

For child placements the translation is `P(t+R e-2e)`, because the parent
carrier is doubled. For macro contacts it is `P(t+2R e-2e)`.

The comparison checks the following finite data exactly:

| Object | Result |
|---|---|
| Seven carrier cubes | Equal after recentering |
| Eight decorated child poses | Equal after the proper coordinate change |
| Fine contact atlas | All 44 poses agree |
| Closed substitution contacts | All 30 poses agree |
| Macro contact atlas | All 44 poses agree |
| Feature roles | All 192 correspond, with matching normals and ordered panel axes |
| Signed contact equations | All 372 distinct equations agree under the role map |
| Face motifs | The 24 panels correspond to A, B, C, eight of each |

Feature correspondence uses the panel-local substitution of offset magnitudes
`1/8 -> 1/16` and `1/4 -> 3/16`, preserving the signed short and long axes.
This is **not** a rigid congruence of the physical solids. Their positive key
labels map to our signed keys by

```text
1:-1  2:-7  3:-2  4:-8  5:-3  6:-5
7:-4  8:-6  9:-12  10:10  11:-11  12:9
```

Extend this map oddly to negative keys. Absolute labels are permuted
bijectively, preserving the opposite-key matching relation.

| Physical parameter | Our frozen proposal | Chair44 |
|---|---|---|
| Feature surface | Polynomial cap | Square pyramid |
| Half-width | `1/64` | `1/100` |
| Height unit | `1/4096` | `1/10000` |
| Panel offset magnitudes | `1/16, 3/16` | `1/8, 1/4` |

These differences matter to the arbitrary-placement proof. Discrete contact
equivalence does not transfer a physical grid-enforcement theorem automatically.

## Actual formal scope

An independent subagent inspected the released Lean statements and their
underlying definitions without executing the downloaded code. In the pinned
source, `lean/R44/R44/LogicalSpineFoundation.lean` defines:

- `E3` as real Euclidean three-space and `RigidMotion` as all affine isometry
  equivalences (lines 21–22).
- A concrete tent-modified solid `Q` (line 465).
- `Packing` and `Tiling` using disjoint interiors and coverage, without a grid,
  hierarchy or matching-rule premise (lines 475–483).
- Symmetries of the unlabelled family of closed geometric tiles, rather than
  only symmetries of decorated placement records (lines 563–572).

`LogicalSpine.lean:7231` states:

```lean
theorem r44_einstein : Nonempty (Tiling Q) ∧ ∀ T : Tiling Q,
    Per T = {0} ∧ (Set.univ : Set (Sym T)).encard ≤ 24 :=
  r44_einstein_of_hypotheses ⟨⟩
```

The `Hypotheses` structure at line 2058 is empty in this release. Older
descriptions of undischarged hypotheses do not describe its final endpoint.
`registration_of_tiling` at line 6261 invokes geometric endpoints with proof
bodies, including `Proved/UnrestrictedAlignment.lean`.

| Obligation | Our present Lean result | Released Chair44 claim |
|---|---|---|
| Contact recurrence | Proved in grid semantics | Proved |
| Forced grouping and legal deflation | Proved for any `LegalTiling` | Proved |
| Translation exclusion | Proved for any `LegalTiling` | Proved for physical tilings |
| Initial infinite tiling existence | Not yet formalized | Included |
| Arbitrary physical placements force a grid | Written proposal only | Included |
| Reflections and full finite symmetry | Not yet formalized | Included; bound 24 |

The release's `AXIOMS.md` reports 21 named `native_decide` hooks for the final
theorem, besides the standard logical axioms. These trust compiled evaluation
for finite decisions. Our finite certificates use kernel reduction and our
final audited declarations require only the standard logical axioms. This is
a real trust-boundary difference, **not** evidence of a mathematical defect
in Chair44. The subsequent build reproduced their complete axiom output exactly.

## The geometric contribution to scrutinize

Version 2, Sections 4–5, proposes a concrete way to make polyhedral features
force complete partners without assuming face-to-face placement:

1. At generic feature-edge points, dihedral-angle budgets force exactly one
   complementary feature edge of the same magnitude and type.
2. At every point of a feature's connected edge graph, a solid-angle lower
   bound rules out three feature-bearing tiles. Local finiteness then gives
   a finite, disjoint, closed cover of the graph by possible partner tiles.
   Connectedness forces a single partner for the entire graph.
3. Containment rigidity recovers equality of the full feature graphs and
   restricts the relative placement to a finite signed-grid list.
4. The companion census rejects nonregistered placements using forced third
   partners and explicit collision boxes. Registered components cover the
   carrier lattice; a material-coverage argument excludes other components.

This is a substantive alternative to our analytic cap-rigidity route. The
connected-graph argument, its generic-to-everywhere passage, and the bridge
from exact solid to the formal feature definitions deserve an independent
audit. This outline is a reading of the proposed proof, not certification.

## Chronology and provenance limits

Our frozen manifest and proposal are dated **15 September 2026**, without an
intraday time in those records. Our first local Git commit is **16 September
2026, 08:20:50 -04:00**, later than the first Zenodo deposit. That does not
date the beginning of our work. Conversely, a day-only research note does
not establish that our finding preceded the deposit within that day.

Their `provenance/HASH_CHAIN.md` describes a construction packet chain
verified on 6 September, and the paper describes a mathematical baseline on
10 September. These are the author's provenance statements; we did not
validate historical timestamps or the external cryptographic attestations.
A content hash alone does not prove when a file existed.

We can establish overlap and the public deposit dates. We cannot establish
relative private discovery priority, independent discovery, or borrowing
from the materials examined. The user's statement that publication followed
our finding remains distinct from what this audit can independently date.

The paper explicitly discloses extensive AI-assisted discovery, coding,
writing and review. Its named external adversarial reviews were performed
by agents. They should not be described as independent human expert review.
The same limitation applies to our own subagent reviews.

## Revised next work

**Progress update:** items 1 and the off-grid finite replay are complete; see
the [build result](CHAIR44_BUILD_REPRODUCTION.md). The list below preserves
the initial comparison's plan. Remaining work concerns semantic review and
presentation, not repeating the successful build.

1. Reproduce the pinned Chair44 build in an isolated environment after
   inspecting its build commands; retain compiler versions, axiom output and
   source hashes. The present comparison ran only our own JSON reader.
2. Audit the physical-solid definitions and companion theorem before investing
   in a competing full formalization. Check that the exact object in the
   final theorem is the one described by the geometry and exports.
3. Use our smaller grid proof as a cross-check. The coordinate equivalence
   gives a concrete route to relating the two formal models, but that bridge
   has not itself been proved in Lean.
4. Reframe any Goodman-Strauss inquiry around this disclosed overlap and a
   precise remaining question. The old frozen brief predates this finding;
   retain it as historical evidence, not as an up-to-date novelty assessment.

Finishing our grid symmetry bound remains a small useful milestone. It is
no longer the highest-value step for deciding whether we have a distinct
research contribution.

## Reproduction and evidence

Run from our repository root, with an extracted copy of the pinned public
release. The comparison imports no downloaded implementation and uses exact
integer/fraction arithmetic:

```sh
uv run --locked python strong/audit/compare_chair44.py \
  --release-root /path/to/six-birds-tiles-137e46b15d36266c37879478cfc62af6e4469147 \
  --output strong/audit/chair44_comparison.json
```

- [Comparison script](../audit/compare_chair44.py).
- [Exact results and input hashes](../audit/chair44_comparison.json).
- [Version 2 PDF](sources/tsiokos-chair44-v2.pdf), Ioannis Tsiokos, CC BY 4.0,
  downloaded unchanged from Zenodo.
- [Version 1 metadata](sources/zenodo-22734468.json) and
  [version 2 metadata](sources/zenodo-22792358.json), retrieved 16 September.

Two separate subagents handled finite-data correspondence and formal-scope
inspection. The coordinator read the manuscript's geometry and mechanization
sections and examined chronology. These were bounded AI-assisted reviews;
no full external proof verification or human expert assessment is claimed.

Validation: the comparator passed under `uv` on the pinned data. A negative
control changing one frozen port's signed key to 100 was rejected with no
successful output written. Assertions must remain enabled; the script rejects
execution under Python's `-O` option.

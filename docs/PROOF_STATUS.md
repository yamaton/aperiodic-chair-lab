# Current claims and proof dependencies

*Updated 19 September 2026. Grid proof status and separate triangular variant.*

This is the current dependency table, rather than a development chronology.
Older reports retain their historical results and plans. The exact object is
the [frozen curved-cap chair](../strong/audit/frozen_v1/candidate.json), SHA-256
`95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54`.
Chair44's square-pyramid solid is a different geometric object with the same
discrete matching system under the [recorded correspondence](../strong/review/TSIOKOS_CHAIR44_COMPARISON.md).

The tutorial now uses a separate [triangular cubic candidate](../strong/PORT_SIMPLIFICATION.md)
as its geometric main example. Its full fine/macro contact sets and A/B/C
panel rules match the reference; a written three-line rigidity proof
transfers the registration argument. The main dependency table below still
specifies the frozen square-cap object and its Lean inputs. The triangular
variant has no new real-geometry Lean endpoint; its separate evidence is
listed in the comparison table.

**Evidence classes:** “Lean” means a checked theorem in the stated formal
model; “exact checks” means finite arithmetic or symbolic identities;
“written” means a mathematical argument outside the completed Lean project.
A written argument is not merely a finite observation, but its correctness
does not follow from a successful checker run. AI review is not human review.

| ID / claim | Required inputs | Current evidence and source | Remaining boundary |
|---|---|---|---|
| D0. Exact solid and faithful input data | Seven cubes, 192 signed ports, polynomial surface prescription | [Frozen data/audit](../strong/audit/README.md); deterministic JSON → Lean export; exact width, height and separation checks | Lean models cells and ports, not the real solid; regular-closedness and interior-ball interpretation are written |
| G1. Local finiteness and an open cap mate | D0, arbitrary congruent closed tiles, disjoint interiors and full coverage | Written Lemma 1 of the [short geometric note](../strong/review/CURVED_GRID_NOTE.md) | No grid or face-to-face premise; finite computations do not prove this topological implication |
| G2. Cap rigidity and adjacent ownership | G1; asymmetric polynomial, actual face offsets and key handedness | Written Lemmas 2–3; symbolic line identities and 1,536 opposite-key frame checks | Analytic continuation is written; 86 single-cap poses are necessities, not the 44 whole-chair contacts |
| G3. One global proper grid and all interface rules | G2, retained cube interiors, lattice adjacency | Written Lemmas 4–5 and theorem; [geometric scrutiny](../strong/review/GEOMETRIC_GRID_SCRUTINY.md) | Applies conditionally to physical tilings; not yet connected in Lean to real Euclidean sets |
| L1. Exact fine/macro contact language and recurrence | Frozen cells, ports and eight children | Lean [recurrence](../formal/README.md): all integer offsets, 24 proper orientations, 44 contacts at each scale | Source-file correspondence is checked by Python; physical surface semantics are outside Lean |
| L2. Legal grid tilings have actual face neighbors | Coverage, unique cube ownership and port compatibility | Lean [tiling bridge](../formal/GRID_TILING_BRIDGE.md), using L1 | No grouping, parity or substitution-origin assumption in `LegalTiling` |
| L3. Unique eight-child grouping | L1–L2, checked local exclusion/forcing witnesses | Lean [universal grouping](../formal/UNIVERSAL_GROUPING.md) | Parent mechanism has Goodman–Strauss precedents; no new existence assertion |
| L4. Common parent parity and legal deflation | L1–L3, exact macro support/boundary and lattice connectivity | Lean [legal deflation](../formal/LEGAL_DEFLATION.md), repeatable to every finite depth | Conditional on an initial `LegalTiling`; does not construct one |
| L5. Every integer translation period is zero | L4; intrinsic centers preserve periods; integer descent | Lean [translation exclusion](../formal/TRANSLATION_EXCLUSION.md) | Period means invariance of the whole decorated placement set |
| L6. At most 24 proper grid symmetries | L5 and proper grid motion algebra | Lean [grid symmetry theorem](../formal/GRID_SYMMETRY.md): frame injectivity and an exhaustive list of length ≤24 | Completed here; no assertion of trivial stabilizer, arbitrary Euclidean symmetries or reflected grid states |
| E1. A legal infinite grid tiling exists | Eight-child partition, legal substitution-contact closure, expanding interior balls | Exact checks plus written [compactness proof](../strong/review/DEPENDENCY_AUDIT.md#d-existence-explicit-expanding-balls-and-a-compactness-argument) | Not yet formalized; logically separate from L2–L6 |
| E2. An exact physical tiling exists | E1, separated feature boxes and complementary matching graphs | Written material-filling argument in the [geometric scrutiny](../strong/review/GEOMETRIC_GRID_SCRUTINY.md#7-physical-coverage-all-ports-have-the-same-opposite-owner) | G3 is a physical → grid implication and cannot replace this converse construction |
| P1. Physical symmetries act faithfully on grid placements | G3, recovery of carrier axes/origin and trivial self-isometry of the decorated solid | Written [representation argument](../strong/review/DEPENDENCY_AUDIT.md#e-grouping-recurrence-and-representation-of-physical-orientations), finite stabilizer check | Requires the geometric interpretation; checking 48 frames alone does not exclude arbitrary self-isometries |
| P2. The curved solid tiles and every physical tiling has finite symmetry | E2; G3 + P1 + L5–L6 | Written synthesis, with a proposed bound of 24; [symmetry discussion](../strong/review/SCRUTINY_ADDENDUM.md#5-sharper-symmetry-statements) | Not an end-to-end Lean theorem; geometric/semantic review remains; no mesh or printed-object conclusion |

The universal argument follows `D0 → G1 → G2 → G3 → L2–L6`, with L1
supplying the discrete contact facts and P1 needed to transport physical
symmetries. The existence branch is `D0 + substitution closure → E1 → E2`.
Neither branch substitutes for the other. G3 and L1 are independent results
until the real-solid interpretation is connected to the formal cell/port model.

## Separate comparison and experimental claims

| Claim | Evidence | Limit |
|---|---|---|
| Same discrete system as Chair44 | Exact coordinate/key bijection, including all contact sets and children | Does not make the two physical solids congruent or transfer their geometric proofs |
| Two-depth triangular cubic candidate | [Written rigidity and registration transfer](../strong/PORT_SIMPLIFICATION.md), [exact snapshot](../strong/audit/triangular_v1/README.md), [independent replay](../strong/audit/triangular_ports_crosscheck.json): same full contact sets, all 2,304 aligned panel comparisons, trivial stabilizer among 48 signed frames | The all-isometries reduction and geometric interpretation remain written; this is not a new Lean build, independent human review or fabrication result |
| Movable-anchor width/depth family | [Packing and curved-zone argument](../strong/PORT_DIMENSIONS.md), [rational frame/clearance evidence](../strong/audit/port_dimensions.json): 12× width / 256× depth witness, w supremum 1/4 in the stated family | Written geometric transfer, no new Lean theorem; depth conditions are sufficient, not a global optimum or tolerance specification; snapshots unchanged |
| Chair44 physical theorem reproduced | [Pinned build and axiom audit](../strong/review/CHAIR44_BUILD_REPRODUCTION.md), 169 matching axiom lines | Final endpoint has 21 disclosed native-evaluation hooks; not a full independent semantic review; release controls retain the missing-archive failure |
| Dyadic address/synchronization deductions | [168-state calculation and written deductions](../strong/review/SCRUTINY_ADDENDUM.md) | Not part of our Lean endpoint; exceptional fibers and equality with the substitution hull remain open |
| Printable interfaces and defect response | [Experimental proposal](APERIODIC_CHAIR_TUTORIAL.md#10-bringing-the-rules-to-a-3d-printer) | No validated replacement geometry, tolerance study or physical theorem |

## Verification and next obligations

The current Lean manifest has **62 audited declarations and 41 Lean source
hashes**, with only the standard three logical axioms. The new symmetry
module was built and the full driver rerun; earlier proof artifacts were
reused.

A subsequent [independent agent review](../strong/review/FOLLOWUP_INDEPENDENT_REVIEW.md)
found no material defect in the new grid-symmetry module or short geometric
manuscript. It reproduced the Lean audit and supplied a new finite/symbolic
geometry probe. Its scope does not include a complete re-audit of the earlier
formal development, initial existence or physical-symmetry transport.

Reproduce from the repository root:

```sh
uv run --locked python formal/verify.py
uv run --locked python strong/review/verify_package.py
uv run --locked python strong/audit/scrutinize_grid_bridge.py
uv run --locked python strong/audit/grid_bridge_crosscheck.py
```

The package verifier runs its six checks in a temporary copy. The last two
commands rewrite deterministic result JSONs; inspect their diffs. The
registration manuscript cites these checks but makes its analytic steps
explicit rather than treating the outputs as an all-tilings proof.

The next formal branch is E1, initial existence. The next geometric work is
review of G1–G3 and P1 with the exact solid fixed. Neither requires rerunning
the completed Chair44 cold build. Frozen artifacts and old publication
snapshots remain historical; no new outreach or publication is implied.

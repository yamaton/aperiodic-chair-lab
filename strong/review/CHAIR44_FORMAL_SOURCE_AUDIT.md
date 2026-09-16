# Chair44 physical definition and companion-chain source audit

**Subsequent verification:** the [pinned build and axiom audit](CHAIR44_BUILD_REPRODUCTION.md)
have now been reproduced, and the [independent companion replay](CHAIR44_COMPANION_REPLAY.md)
passed. This memo preserves the narrower source-inspection stage that preceded
those checks; its statements about an outstanding build are historical.

Scope: bounded read-only inspection of release
`137e46b15d36266c37879478cfc62af6e4469147`, plus an independently written
`uv` data-correspondence check. No downloaded program was executed; Lean was
not built. This is an AI source review, not independent human validation.

## Verdict

**No concrete defect or hidden restriction was found in the inspected
physical-solid/companion chain.** The formal solid is the actual signed
square-pyramid chair described by the released JSON. The inspected chain
addresses arbitrary isometric placements through real geometry, rather
than defining physical legality to mean membership in the 44-contact table.
This finding is narrower than validation of the whole proof.

## Exact data correspondence

`uv run --locked python strong/audit/check_chair44_lean_literals.py --release-root RELEASE --output REPORT`
parses the Lean `Generated/CoreData.lean` literals and compares them with
`solid/native_panels.csv` and `solid/r44_solid.json`. Its reconstruction uses
formulas manually inspected in `FiniteModel.lean:145-174` and
`LogicalSpineFoundation.lean:191-230`. All comparisons passed:

- 24 panels and all 192 profile coefficients;
- all 192 feature base-corner sets and signed apices, with role/face identity;
- all 2,138 vertex coordinates and all 4,272 ordered triangle index triples;
- base half-width `1/100` and height unit `1/10000`.

The report records source and probe SHA-256 hashes. The formula is manually
transcribed, not a general Lean interpreter; the hashes bind it to this
inspected release. This is a finite source/data correspondence test, not
proof checking or a new theorem about arbitrary placements.

## Inspected semantic chain

Paths below are relative to `lean/R44/R44/` in that release.

1. **Explicit physical set.** `LogicalSpineFoundation.lean:432-472` defines
   the signed tent height and `Q` as the seven-cube carrier with negative
   tents cut out and positive tents added. Centers/normals/coefficients
   derive from the same generated panel table through `nativeFeatures`.
   `Tiling`, at lines 475-485, asks only for pairwise-disjoint interiors and
   full Euclidean coverage by arbitrary affine isometries. Its definition
   does not impose grid, homochirality, or contact-table membership.

2. **Actual local geometric quantities.** `LogicalSpineFoundation.lean:1104`
   defines a radial tangent cone by sufficiently short positive ray
   segments staying in the set. `solidAngle`, at line 1151, is three times
   the cone's volume inside the Euclidean unit ball. These are geometric
   quantities, not labels defined to make the desired angle equation true.

3. **Generic companion without face-to-face premise.**
   `Proved/NativeBoundaryStrata.lean:71` classifies actual nonvertex boundary
   points using local tent/carrier charts. `Proved/GenericBoundaryLabels.lean:74`
   removes the finitely many placed mesh vertices meeting the compact root
   graph; the surviving set is dense. Its conversion at line 162 obtains
   the angle sum from incident cone-volume additivity. No common transverse
   plane or pre-existing collinearity is assumed in this inspected layer.
   `Proved/GenericFeaturePartner.lean:23,67` extracts the unique opposite
   coefficient partner from that packet and the dihedral arithmetic.

4. **Whole companion.** `Proved/ConnectedFeatureCompanion.lean:87,106`
   excludes three feature-bearing tiles at a point via large open circular
   cones, then applies a finite disjoint closed-cover argument to the
   connected feature graph. Endpoints are included. A second connectedness
   argument selects one role of the companion tile.

5. **Rigid feature and census.**
   `Proved/FeatureContainmentRigidity.lean:24,121` uses a generic partner to
   infer opposite coefficients, then compact congruent graph containment
   to get equality. The distinct-placement premise is explicitly present.
   `Proved/CompanionPoseDiscrete.lean:19` links actual complete feature mates
   to the center/normal/frame equations and the eighth-grid census.

6. **The finite table is linked back to physical packing.**
   `Proved/CompanionCollisionSemantics.lean:78` connects a physical mate
   formula to a literal role/pose pair; lines 198 and 223 interpret the
   unpruned companion-option list and its rejection witnesses.
   `Proved/RetainedBoxGeometry.lean:277` turns positive baseline overlap
   into actual interior overlap of `Q` copies. Then
   `Proved/OnlyRegisteredMates.lean:24` excludes every non-atlas pose by
   compulsory companions and packing disjointness, treating both owner
   normalizations. `Proved/ConcreteCompanions.lean:156-192` assembles these
   results and derives ownership of the far-side shell cell.

## What remains unverified

- The release has not been cold-built here, and its generated axiom audit
  has not been independently reproduced. `Theorems.lean:56,94` uses
  `native_decide` for the mate census and mesh check, among other finite
  facts. A successful build therefore still has compiler-backed finite
  hooks; it is not the same trust boundary as our kernel-reduced checks.
- This inspection followed selected semantic interfaces and their proof
  bodies. It did not independently validate every leaf in the chart,
  tangent-cone, angle-measure, compact-containment, or global registration
  developments, or the subsequent existence and symmetry proofs.
- No result here transfers automatically to our curved-cap solid. Our
  analytic matching argument is geometrically different even though the
  discrete matching system agrees.

Recommended next audit: cold build the pinned release in an isolated
location; reproduce the endpoint axiom list; then scrutinize the generic
boundary/sector arithmetic and global component-to-grid bridge with those
compiled definitions fixed. The independently checked literal connection
removes one possible mismatch, but does not replace those steps.

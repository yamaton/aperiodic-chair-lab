# Arbitrary grid tilings: placement and neighbor bridge

*16 September 2026. Completed first bounded step of [the next milestone](NEXT_MILESTONE.md).*

## Result

Lean now connects the frozen chair's normalized finite contact certificates
to actual neighbors in any legal tiling of the integer cube grid. The input
is an arbitrary set of proper placements, not a substitution-generated patch.

`LegalTiling T` has exactly three requirements:

1. Every lattice cube has an owner in `T`.
2. Two placements owning the same cube are equal.
3. Every pair of distinct placements matches on all coincident opposing faces.

The third condition allows distant placements: it does not require every
pair to touch. All 24 decorated orientations are retained. There is no parent
assignment, finite neighborhood completeness, parity or hierarchy premise.
These conditions concern the discrete occupied-cube and port model; they do
not themselves define the curved physical solid.

## Proved statements

| Source | What is established |
|---|---|
| [Frames](Chair/Frames.lean) | Proper frame and integral motion composition/inversion; correct actions on points, cube lower corners and scaled coordinates |
| [Covariance](Chair/Covariance.lean) | Action on complete face/port records agrees with `moveSolid`; matching and contact survive a common motion, with relative offsets rotated |
| [Boundary](Chair/Boundary.lean) | The listed faces are exactly the exposed cube boundary of every placed frozen chair |
| [Tiling](Chair/Tiling.lean) | Common motions preserve legality; coverage supplies face neighbors; those neighbors belong to the certified contact language |

The principal combined theorem is
`LegalTiling.exposed_face_neighbor_accepted`. Given an actual tile and any
of its exposed faces, it provides a different tile of the same tiling, a
matching opposite face, and an orientation index whose accepted list contains
the relative placement's translation. Across these lists there are exactly
the 44 contacts proved in the previous milestone. This does **not** assert
that every accepted contact occurs in some infinite legal tiling.

`placed_macro_contact_recurrence` also transports the earlier recurrence
to any pair of properly placed macro objects. It does not say that an
arbitrary fine tiling is already partitioned into such objects.

## Two details worth retaining

**Cube lower corners do not transform like points.** For a signed coordinate
permutation `R`, a cube at `q` has transformed lower corner `Rq + c(R)`, where
each negative entry contributes a minus one to its row of `c(R)`. For example,
the proper rotation `diag(-1,-1,1)` sends the origin cube's lower corner to
`(-1,-1,0)`. Composition requires
`c(RS) = R c(S) + c(R)`. Lean checks this identity over the finite frames,
then proves the action laws for arbitrary integer coordinates. Face centers
and ports instead use linear actions with translations scaled by two and
sixteen. The covariance proofs keep these distinct actions consistent.

**Coverage supplies the missing neighboring witness.** A face belongs to a
cube `q` with outward normal `n`; boundary correctness says `q+n` is outside
that tile. Coverage supplies its owner. Unique ownership prevents this new
tile from also owning `q`, so its face in direction `-n` is exposed. Boundary
completeness supplies that opposite face, and legality gives its port match.
Subsequent local exclusions can therefore demand actual tiling neighbors
without assuming a supplied finite neighborhood was exhaustive.

For two placements `g,h`, normalization uses the full motion `g⁻¹h`.
Its shift is `R_g⁻¹(t_h-t_g)`. Merely subtracting the two shifts would lose
the first tile's frame. The normalization lemma transfers this precise shift
into the old contact predicate before invoking the finite certificate.

## Validation and provenance

The full verification driver passed through `uv`: deterministic source
regeneration checks, the Lean build, comparison with the independent
44-contact table, and an expanded audit of 16 theorem declarations. Every
audited dependency is among `propext`, `Classical.choice`, and `Quot.sound`.
No admitted proof, custom axiom or native-evaluation dependency was added.
[verification.json](verification.json) records the current 21 Lean source
hashes. Existing construction and finite-contact proof modules are unchanged.

Three subagents implemented frame algebra, contact covariance and boundary
ownership separately. The boundary contributor then reviewed the coordinator's
tiling definitions and proofs without editing them; it found no material
issue. This was an internal cross-review, not a fresh independent review of
the entire addition or external mathematical validation.

From the repository root:

```sh
uv run --locked python formal/verify.py --lake /path/to/lean/bin/lake --write-report
```

This run used `/tmp/lean-4.34.0-linux/bin/lake`, Lean 4.34.0 and bundled Std.
The full driver reused the prior milestone's compiled proof batches while
building the new modules; it was not a cold rebuild of the whole project.

## Next boundary

Next, formalize the 14 impossible-contact exclusions in
`strong/MOTIF_GROUPING.md` as consequences of `LegalTiling`. Use the new
face-neighbor theorem to demand an owner of each obstructed face and the
existing port semantics to rule out every possible owner. Then implement
the six forcing chains, exceptional notch case and unique eight-child
partition. Common parity and legal deflation follow as later obligations.

No existence, universal grouping, deflation, arbitrary Euclidean grid
enforcement or finite-symmetry theorem has been added by this step. The
tiling statements remain conditional until nonemptiness is proved separately.
Frozen geometry, outreach materials and published work were not changed.

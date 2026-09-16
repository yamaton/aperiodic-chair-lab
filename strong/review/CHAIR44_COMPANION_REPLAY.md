# Independent finite companion replay

*16 September 2026. Independent arithmetic verification of the off-grid
collision stage; the continuous companion theorem remains a separate premise.*

A new standard-library Python checker, run through `uv`, read only the pinned
Chair44 release data. It did not import or execute the released implementations.
The release root was commit `137e46b15d36266c37879478cfc62af6e4469147`.

The complete replay passed in 2.58 seconds. It independently reconstructed the
192 pyramid fans as connected components of sloping mesh triangles, checked
their square bases, centered apices, outward orientation and signed heights,
and only then associated the certificate's role numbers with those features.
It regenerated all 48 signed cubic frames and all complete-feature mates.

| Stage | Independently checked count |
|---|---:|
| Complete-feature mate poses | 6,862 |
| Direct retained-core collisions | 1,545 |
| Isolated surviving poses | 5,317 |
| Integer isolated survivors | 83 |
| Fractional isolated survivors | 5,234 |
| Forced-companion rejected poses | 5,273 |
| Explicit partner collision boxes | 299,975 |
| Remaining poses, exactly the registered atlas | 44 |

Every surviving atlas pose is proper and integral. Both direct collisions and
partner collisions have minimum certified retained-core width `42/400`; each
such open box contains an open Euclidean ball of radius `21/400`.

## Completeness of this finite check

Every ordered pair of native features with complementary coefficients and
opposite transformed normals is considered in every signed cubic frame. Their
center difference determines the sole possible translation. Square bases are
preserved by these frames, so this enumerates the complete-feature mate poses
conditional on the separate geometric theorem that any full feature mate has
such a frame.

For each native feature `u`, the checker constructs `Partners(u)` from **every**
pose in the 5,317-member set that matches `u`. Only direct carrier overlaps with
the root have been removed. No flat-panel check, recursive deletion, registered
atlas restriction, or earlier forced-companion rejection filters this set.

For every rejected pose `V`, the checker verifies that the indicated feature's
partner list is nonempty and does not contain the other already placed tile's
pose. It verifies that the exported partner list equals this entire reconstructed
set, with no missing or duplicated entries. Each listed partner has an actual
intersection of native carrier cubes with the other placed tile. The exact
intersection and the eroded physical core box are checked from the cube poses,
not taken on trust from the certificate.

The exclusion of the other tile from `Partners(u)` is essential: the compulsory
companion must be a third tile for its overlap with the other placed tile to
contradict a packing. The root itself cannot belong to a partner list because
it has a direct carrier/interior overlap with itself. For the other tile, its
actual chosen pose would belong to `Partners(u)` if that physical tile supplied
the indicated feature mate: enumeration considered all its native features.
Thus this use does not silently assume a third tile before checking it.

**Every one of the 5,273 supplied rejection witnesses uses a feature of the
root tile (owner 0).** The script handles either owner, but no inversion is
actually needed by this certificate.

The complement of the rejected-pose set in the 5,317 isolated survivors agrees
exactly, pose by pose, with the released 44-entry registered contact atlas.
Packet solid and candidate/companion certificates are checked byte-for-byte
against the canonical `solid/` and `certificates/` copies. All source hashes
are included in the JSON result.

## Corruption controls

Three fresh copies of the compressed collision stream were deliberately
altered. The checker rejected all three with the intended errors:

1. Remove one partner: `export omitted an unpruned partner`.
2. Alter one claimed intersection endpoint: `claimed carrier intersection incorrect`.
3. Duplicate one partner: `invalid/duplicate listed partner`.

The release files were left untouched. The control driver accepts
`--release-root`, `--checker`, and `--output`.

## Scope limits

This is an independent finite certificate check, not a Lean proof. It does not
prove the continuous assertion that every physical feature has one complete
companion, the geometry-to-mesh equivalence, retained-core inclusion, tiling
existence, hierarchy, or aperiodicity. It verifies the finite exclusion bridge
once the complete-companion and retained-core theorems are available. The mesh
checks cover feature geometry and local fan structure; they are not a complete
embedded-manifold or solid-equivalence audit.

## Deliverables and commands

Files preserved in `strong/audit/` after coordinator review:

- `replay_chair44_companions.py`: checker; `--release-root` and `--output`.
- `chair44_companion_replay.json`: exact checks, counts, source/script hashes.
- `check_chair44_replay_mutations.py`: corruption-control driver.
- `chair44_companion_mutation_controls.json`: three detected corruptions.

```sh
uv run --locked python strong/audit/replay_chair44_companions.py \
  --release-root RELEASE \
  --output strong/audit/chair44_companion_replay.json
uv run --locked python strong/audit/check_chair44_replay_mutations.py \
  --release-root RELEASE \
  --checker strong/audit/replay_chair44_companions.py \
  --output strong/audit/chair44_companion_mutation_controls.json
```

Replace `RELEASE` with the extracted pinned source directory. A separate
agent with no authorship role reviewed completeness, units, unpruned partner
sets and third-tile logic and reran the checker under `uv` in 2.49 seconds.
It found no material defect. The coordinator separately reran the positive
check and all three controls. These are AI reviews of this finite step.

This strengthens the earlier [proof comparison](CHAIR44_PROOF_COMPARISON.md)
beyond its registered-grid atlas reconstruction. In particular, its prior
statement that the off-grid census had not been replayed is now superseded.

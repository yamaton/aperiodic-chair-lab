# Exploration with unrestricted cluster boundaries

**Subsequent work:** the [eight-chair search](EIGHT_CHAIRS.md) now exhausts
the face-connected eight-chair arrangements left open in this report.

**There is substantial room left to explore.** The earlier search classified
specific connector families and cluster arrangements. It did not classify
3D shapes in general. This pass tests one previously open gap and derives a
structural obstruction for another candidate architecture.

No strongly aperiodic monotile is claimed here.

## 1. Four-chair clusters can now cross the boundary

Previously, a cluster had to fit inside the chosen supertile. That restriction
could falsely reject a useful fusion. The new experiment requires coverage
only of an interior core and allows clusters to extend into a surrounding
halo. Coverage of the halo itself is optional.

We use a fourth-level chair substitution patch with 4,096 chairs. Its core
contains 764 chairs at least three face-adjacency steps from the boundary.
A connected four-chair cluster has graph diameter at most three. Any chair
outside the patch is at least four steps from the core. Therefore **every
possible face-connected four-chair cluster touching the core is represented**;
the surrounding patch imposes no artificial cut on those clusters.

Any partition into one cluster shape must cover a chosen interior anchor.
It has 587 possible connected four-chair clusters, representing 206 shapes
under proper rotations and translations. For each shape, we generate all
its occurrences and solve an exact-cover problem:

- Every core chair belongs to exactly one cluster.
- Every halo chair belongs to at most one cluster.
- Clusters may cross the core boundary.

Of the 206 shapes, 203 leave at least one core chair with no possible
placement. The remaining three have mutually incompatible coverage
requirements. All three are unsatisfiable in both Z3 and an independent
backtracking solver.

This gives a finite obstruction to partitioning this hierarchical patch
into congruent face-connected groups of four whole chairs. Because the halo
is sufficient, allowing clusters to cross the outer boundary cannot repair
the obstruction at the core. Every tiling built from this chair substitution
contains a fourth-level supertile, so the same obstruction applies to a
fixed four-chair grouping of those hierarchical tilings.

**Scope:** the grouping must preserve the whole coarse-chair decomposition
and use face-connected chair groups. This does not exclude chairs connected
only through fillers, larger groups, different decompositions, or recutting.

Independent verification exhausts all anchor-containing four-subsets of
the 84-chair radius-three neighborhood, rather than using the search's
incremental growth method. It recovers the same 587 clusters and 206 shapes.

## 2. Eight chairs: a positive starting point, then an obstruction

Eight chairs already form a substitution supertile. Grouping them that way
is valid throughout the infinite hierarchy. Volume balance requires six
whole cross-shaped fillers per such group, as derived in
[the previous pass](SECOND_PASS.md#3-can-an-existing-hierarchical-pair-be-fused-into-one-block).

We tested a concrete fusion: the eight-chair group plus one fixed selection
of six fillers. The large group has three proper rotations preserving its
missing-octant direction. An asymmetric filler pattern can exploit those
three orientations to place its fillers differently at different occurrences.

The SAT model jointly chooses the six sites and the orientation of every
macrochair. It checks 1,685 interior lattice vertices in a 512-macrochair
patch, with sufficient geometric padding. The first experiment uses the
25 adjacent candidate sites and is unsatisfiable.

### Why extending the attachment range cannot rescue this design

The following argument is independent of the 25-site bound.

Use integer coordinates for the macrochair tiling and let `C` be its chair
centres. The substitution gives

```text
C = O ∪ 2C′,
O = {(odd, odd, odd)},
E = {(even, even, even)},
```

where `C′` is the centre set of the parent chair tiling. Thus:

1. Every site in `O` is a chair centre.
2. All remaining chair centres lie in `E`.
3. Some sites in `E` are centres and others are filler holes.

In the eight-chair fusion, the crosses already inside the chairs occupy
the sites in `C`. The additional crosses must fill the other lattice sites.

Let `F` be any fixed set of integer attachment offsets. A block centred at
`c` places its attached crosses at `c + Rf`, for `f ∈ F`, where `R` is a
signed coordinate permutation. Such a rotation preserves whether a vector
has all-even, all-odd, or mixed coordinate parity.

- An **all-even** offset is forbidden: at any odd chair centre it places
  an extra cross on an odd site already occupied by a chair.
- An **all-odd** offset is forbidden: at any even chair centre it likewise
  places an extra cross on an occupied odd site.
- Every remaining offset has **mixed parity**. Added to either an all-even
  or all-odd centre, it reaches only mixed-parity sites.

Consequently no allowed offset can fill the unoccupied all-even sites.
Contradiction.

**Conditional conclusion:** a fixed eight-chair substitution group cannot
be turned into a monotile merely by attaching a fixed pattern of whole
cross fillers. This holds at arbitrary attachment distances and also if
reflections are allowed. It does not assert an obstruction for a different
arrangement of eight chairs or a new dissection of the pieces.

The verified finite patch has 2,232 occupied odd interior sites, 511 occupied
even sites, and 2,352 unoccupied even sites. The exact centre recursion and
parity invariance under all 48 signed coordinate permutations were checked.
Those checks support the implementation; the contradiction above supplies
the argument beyond the finite patch.

The underlying hierarchy and marked filler pieces are from
[Goodman-Strauss's aperiodic pair](https://doi.org/10.1006/eujc.1998.0282).
The fusion experiments and parity argument here analyze possible modifications
of that construction; they are not a monotile theorem from that paper.

## 3. Substantial search space remains

The new results distinguish the following possibilities:

| Architecture | What is established here |
|---|---|
| One of the 65,216 previously analyzed connector designs | Classified within its stated grid model |
| Fixed, face-connected groups of four whole hierarchical chairs | Excluded by the padded-core test |
| One standard eight-chair supertile plus whole cross fillers | Excluded by the parity argument |
| Eight-chair groups with a different internal arrangement | Not exhaustively searched |
| Larger groups, such as 12 chairs and 9 crosses | Not exhaustively searched |
| Coarse chair groups connected through fillers | Not exhaustively searched |
| Recutting and redistributing material between the original pieces | Not covered by these fusion obstructions |
| Different hierarchical or noncubic block architectures | Not classified by these experiments |

The next productive search should change one of the assumptions responsible
for an obstruction. Simply enlarging the attachment range of the failed
eight-chair design would repeat a problem the parity argument already rules
out. A different eight-chair arrangement or a dissection that changes the
ownership of the original pieces remains a concrete direction.

For a successful candidate, an infinite construction and an all-tilings
recognition argument are still necessary. A valid sample packing alone would
not establish that the block forces strong aperiodicity.

## Reproduce

```sh
uv run --locked python strong/open_chair_clusters.py
uv run --locked python strong/fused_chair.py --seconds 40
uv run --locked python strong/verify_open_chairs.py
uv run --locked python strong/summarize.py
```

Artifacts: [open-core search](artifacts/open_chair_clusters_4_level4.json),
[attachment synthesis](artifacts/fused_chair_level3.json),
[independent verification](artifacts/open_chair_verification.json).

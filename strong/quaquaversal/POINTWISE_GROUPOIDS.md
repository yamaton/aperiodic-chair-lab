# Pointwise panel maps under all stationary handedness words

Q010 rejects all 256 stationary child-handedness words for two families:
arbitrary pointwise equality markings and real scalar opposite-sign markings.
The result uses actual affine identifications on entire panel domains, not
a polynomial degree bound or constant values on panels.

For each word, repeat the corresponding eight-child assembly twice. Every
positive-area contact of the resulting 64-copy patch imposes identifications
between whole panels in the audited 60-panel partition. There are no partial
panel generators in these runs. A candidate decoration admitting the intended
infinite assembly must satisfy these necessary level-2 identities.

An affine map between bounded polygons is determined by its action on their
noncollinear corners. Consequently composable whole-panel maps form a finite
groupoid, represented exactly by source/target panel IDs and corner
permutations. Every generator edge and its inverse changes sign in the
opposite-sign model. Equality accepts either path parity. Signed matching
requires odd parity; an odd identity loop additionally forces a real scalar
function to vanish throughout that panel. Two such zero panels satisfy any
required opposite-sign relation. This last step does not generalize to an
arbitrary involution with multiple fixed symbols.

For 254 equality words and all 256 signed words, the derived identities admit
a two-prism periodic cell. The remaining equality words, 111 and 144, admit
the four-prism alternating-handedness cell from Q005. Thus every decoration
in each stated family admits the corresponding periodic filling, not merely
the particular numerical markings previously tested.

`audit_pointwise_groupoid.py` does not rerun the groupoid search. It verifies
1,112 affine map records on spanning corner sets, rebuilds the geometric
contact generators for all 256 words, replays 243,360 path/zero-cycle
derivations, checks complete periodic face coverage, and replays all 5,140
directed contacts of the 512 periodic witnesses. Polygon corner extraction
and basic geometry routines are shared with the producer; this is an exact
certificate replay, not a wholly independent implementation or formal proof.

The scope is one decoration, a stationary reflected-child word, and the
stated pointwise face-matching conventions. It does not exclude independent
edge/vertex constraints, multibody neighborhood rules, multiple decorated
types, nonstationary choices of child words, or arbitrary geometric recuts.

```sh
uv run --locked python strong/quaquaversal/pointwise_groupoid.py
uv run --locked python strong/quaquaversal/pointwise_groupoid.py --all --output strong/quaquaversal/artifacts/pointwise_groupoid_all.json
uv run --locked python strong/quaquaversal/audit_pointwise_groupoid.py
```

The pilot preserves words 0, 111 and 144. The full JSON preserves each
generator list, every accepted periodic contact's derivation and every
periodic assignment. No external review or geometric fabrication claim.

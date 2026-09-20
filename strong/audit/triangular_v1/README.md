# Triangular cubic port: research snapshot v1

This is a separate proposed design, not a replacement for `../frozen_v1`.
It uses a cubic bubble on a scalene triangular footprint and two signed-depth
magnitudes. The exact surface, original frame anchors, new keys and eight
child placements are specified in `candidate.json`; its hash is in
`manifest.json`. The field `center` remains the old port frame anchor and
is not the triangular support's centroid.

See [the report](../../PORT_SIMPLIFICATION.md) for the written rigidity and
registration arguments, finite checks, attribution and limitations.

Run from the repository root:

```sh
uv run --locked python strong/audit/simplify_ports.py
node strong/audit/crosscheck_triangular_ports.cjs
```

The generator checks this snapshot byte for byte and refuses to overwrite
different data. Changed designs require a new version. No real-geometry
Lean verification, independent human review or manufactured-object
certification is claimed for this snapshot.

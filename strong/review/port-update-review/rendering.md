# Read-only rendering review

No actionable correctness findings in the reviewed rendering changes.

Reviewed complete `docs/relocated_cover_mesh.py`, `docs/triangular_cover_mesh.py`, `docs/render_chair_cover.py`, `docs/blender_chair_cover.py`; related diffs, cover notes/receipts, README caption, current and earlier triangular images. No repository source, research data, receipt or published image was changed; no Blender render was run.

## Checks actually run

`uv run --locked python /tmp/review-rendering.py` from repository root, using temporary meshes in `/tmp/aperiodic-rendering-review`. The initial independent script needed a NumPy API correction (2D cross product was removed); this correction touched only `/tmp`. The completed run passed.

- Ran `prepare_relocated` with its actual witness assertions, rational contact checks, 56-cell assembly check, welded-edge orientation checks, Euler and volume checks. Result: 470,592 triangles, 235,298 vertices, volume 7.000000000000007.
- Independently derived all 24 actual carrier boundary faces from the seven cubes; the exporter uses exactly those faces, not merely an abstract spherical topology.
- Examined the exported triangles in each of the 192 wedges. Each projects inside its intended reflection wedge; eight distinct wedges occur per face; projected area is 1/8 per wedge and 1 per face. Independently clipped every flat triangle against the cap support and found no positive overlap. Every triangle points outward relative to its carrier-face normal.
- Independently evaluated exported curved vertices against the intended a=-1/4, b=7/32, w=3/16, delta=1/16 profile. Maximum error after coordinate rounding: 5.00158942040585e-13. Minimum vertex clearance between normal displacement and every outer face edge: 0.02734375, exceeding 5/256. These are checks of actual intended geometry, additional to the exporter's topology checks.
- Reconstructed the eight placements and all contact occurrences independently; exactly 384 internal pairs occur, with shared ordered axes, opposite normals and opposite keys. Every pair's transformed exported cap vertex sets coincide.
- Inverted each detail mesh's display transformation, checked the actual cubic cap and padded top rim, and confirmed both transformation matrices are orthogonal with determinant +1. The 9/8 rims lie inside the actual port wedges. Artificial backing extends below the pocket as intended and is disclosed.
- Independently projected all single-chair, eight-child, and detail vertices with the worker's orthographic camera. All are strictly inside their 800x800 panels. Single/assembly bounds are approximately [93.15,61.34] to [706.85,738.66]; detail bounds [117.55,252.39] to [763.66,481.94]. Visually inspected final relocated PNG: whole silhouettes, detail surfaces and labels are visible without clipping.
- Verified all eight current receipt hashes against inputs/sources/image. All four cover PNG hashes match their adjacent receipts. `git diff --exit-code` confirms old square PNG/JSON paths and frozen_v1 unchanged.
- Ran earlier triangular preparation at the documented 3x width / 64x depth settings: 116,208 mesh triangles and 384 internal matches; all its assertions passed. Visually inspected that earlier PNG too.

Relevant implementation locations: witness and area checks at `docs/relocated_cover_mesh.py:98`; wedge construction at :129; internal correspondences at :160; detail crop at :75 and display setup at :188. Worker scales/camera are `docs/blender_chair_cover.py:113`, :127, :198 and :209. README's proportions statement agrees with the current mesh and adjacent notes.

## Scope and limitations

No new arbitrary-Euclidean-tiling theorem, exact-solid certification or manufacturing tolerance claim is established by this review. I inspected current PNGs and rebuilt numerical geometry, but did not rerun Blender or claim pixel-identical reproduction. Mesh contacts were independently compared as vertex sets; equality of their triangle connectivity follows from the common parameter-lattice implementation, not an additional independent face-connectivity comparison. The historical triangular receipt retains its original driver hash; that historical hash is not expected to match a driver subsequently extended for the relocated variant.

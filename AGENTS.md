# Aperiodic Chair Lab: project guidance

- On resuming, read `HANDOFF.md` for current results, outstanding work,
  and outreach status. `strong/review/` holds the outside-review preparation.
- `README.md` introduces the project; `docs/INDEX.md` maps reports, scripts,
  evidence, and commands. Package name: `aperiodic-chair-lab`. Preserve
  research JSON, search logs, and frozen artifacts in version control;
  ignore local environments and caches. Keep changes and commits local
  unless the user authorizes publishing.
- Use **`uv` for all Python work**: `uv sync --locked` to install and
  `uv run --locked python <script>` to run. Use `uv add` for dependencies;
  keep `pyproject.toml` and `uv.lock` consistent. Python 3.13+ is required.
- Run commands from the repository root. Some chair searches compile a
  C++17 helper and require `g++`; browser-control checks use Node.js.
- The objective is one space-filling 3D block whose every tiling has finite
  symmetry group: no nonzero translations or infinite-order screws.
  The recut-chair proposal in `strong/RECUT_CHAIR.md` has checked grid-hierarchy
  certificates and a proposed analytic grid-enforcement argument; it needs
  mathematical review. `strong/FOLLOWUP_REFLECTIONS.md` records the proposed
  extension to reflected copies via a local handedness invariant, face
  motifs, and periodic controls; `strong/REVIEW_NOTE.md` summarizes the claim.
  `strong/MOTIF_GROUPING.md` gives the simpler local parent proof; verify it
  with `uv run --locked python strong/audit/motif_grouping.py`.
  The older SCD construction permits screw symmetry.
- Read `FINDINGS.md` for insights and open directions, `RESEARCH.md` for SCD,
  and `strong/README.md` plus its linked reports for the stronger search.
  Geometry/build scripts live at the root; search scripts in `strong/`;
  generated evidence in `artifacts/` and `strong/artifacts/`.
- Check relevant changes with `uv run --locked python verify.py` for SCD,
  or the affected search's verification script documented in its report.
  Rebuild SCD exports with `uv run --locked python build.py`.
  Use `node verify_viewer.cjs` after viewer changes. Both `viewer.html` and
  `artifacts/explorer.html` must remain standalone and work offline.
- Preserve reproducible witnesses and distinguish proofs, finite checks,
  and conjectures. A finite successful patch does not prove infinite
  tilability or forced aperiodicity. Grid-model exclusions do not exclude
  arbitrary Euclidean tilings. Record timeouts as unknown, never impossible.
- Attribute known constructions and keep design counts separate from rooted
  cluster-placement counts. Update the relevant report when results change.
- For recut-chair work, follow the reproduction commands in its report.
  `strong/audit/README.md` documents the frozen-coordinate audit; preserve
  `strong/audit/frozen_v1/` and use a new snapshot version for changed designs.
  Exact curved surfaces and their approximate meshes have different claims;
  do not present the STL or a printed version as certified aperiodic.

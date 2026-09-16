# Repository record

## Initial organization — 16 September 2026

The user requested a Git repository, clearer organization, a better project
name, and a local initial commit.

**Name:** Aperiodic Chair Lab; package and directory slug
`aperiodic-chair-lab`. The former name was `aperiodic-3d-monotile`.
The name reflects the active chair research without asserting that the
monotile theorem or novelty has been established.

The root README and [project index](INDEX.md) organize the current arguments,
reproduction commands, prior experiments, and review materials. Existing
internal paths are retained: scripts and reports cite them, and the frozen
review package uses the same layout.

The workspace directory is renamed to `aperiodic-chair-lab`; a compatibility
symlink at `aperiodic-3d-monotile` keeps existing local links and environment
paths usable. In a fresh checkout, use the new name and run `uv sync --locked`.

## What belongs in Git

- Source code, research notes, agent handoff, and the locked environment.
- Exact candidate data, certificates, negative controls, and search results.
- Search logs that record completed experiments, including the larger JSON
  enumerations; these are evidence, not disposable caches.
- Figures, standalone viewers, meshes, and the frozen v1 review packet.

Local virtual environments, caches, browser dependencies, and machine-local
agent settings are ignored. `.gitattributes` preserves recorded artifact
and frozen-input bytes across platforms. There is no remote publication in this task.
The initial commit records the accumulated workspace; it does not recreate
the historical sequence of research as separate commits.

## Preservation and future work

The project/package rename changes live metadata only. The files in
`strong/audit/frozen_v1/` and the existing v1 PDF, HTML, and ZIP are preserved
byte for byte. Their old metadata and historical absolute paths remain part
of the original record. A revised review packet should receive a new version.

Use `uv` for Python, run the checks appropriate to a change, and record
mathematical progress in the relevant report and `HANDOFF.md`. The
[review record](../strong/review/RECORD.md) tracks literature and expert-review
preparation. Keep finite computations, written arguments, and externally
validated conclusions distinct.

## Initial validation

The renamed package runs with `uv run --locked --offline`; project and
lockfile names agree. The frozen-snapshot verifier passes, all 69 local
links checked in the root navigation and new index resolve, and the
candidate/PDF/HTML/ZIP hashes match the previously recorded v1 values.
No mathematical algorithms or viewer code changed in this organization pass.

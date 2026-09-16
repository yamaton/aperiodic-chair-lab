# Licensing and reuse

These terms cover material distributed with this notice, to the extent the
project contributors hold the applicable rights. They do not assert rights
over mathematical facts or material in the public domain. Substantial AI
assistance is disclosed in [Provenance](docs/PROVENANCE.md).

## Project material

| Material | License |
|---|---|
| Original Python, Lean, C++, JavaScript, shell, CSS and OpenSCAD source; configuration and dependency manifests; original machine-readable research data and certificates | [MIT](LICENSE) |
| Project prose, tutorials, research notes, figures, and geometric model exports such as STL and OBJ | [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt) (CC BY 4.0) |
| HTML documents and viewers | Embedded program code is MIT; project prose, figures and model content are CC BY 4.0 |
| Archives and frozen snapshots | Each contained file follows the corresponding rule above, subject to third-party exceptions below |

Code blocks in project documentation can also be reused under MIT. Merely
packaging third-party material in an archive or HTML file does not change
its license. Existing notices on a particular file or component take
precedence over the defaults above.

Credit project writing and figures to **Aperiodic Chair Lab contributors**,
link to [the repository](https://github.com/yamaton/aperiodic-chair-lab), identify
the version or commit when practical, link to CC BY 4.0, and indicate changes.
For code, retain the MIT copyright and permission notice. The
[CC BY summary](https://creativecommons.org/licenses/by/4.0/) explains its
attribution requirements; the linked local legal text contains the full terms.

## Third-party exceptions

The [third-party notices](THIRD_PARTY_NOTICES.md) identify the copied Chair44
papers, source-derived extracts and data, and original source licenses.
Those materials are not relicensed as our MIT code. In particular:

- The three retained Tsiokos PDF files are unchanged CC BY 4.0 works by
  Ioannis Tsiokos.
- Chair44 release excerpts, source-derived portions of comparison data,
  and release-generated build/axiom logs retain the release's CC BY 4.0
  terms and attribution. Our additions to those mixed evidence files are
  also offered under CC BY 4.0 to make their reuse straightforward.
- External dependencies remain under their respective licenses. The local
  environments and downloaded Lean/Mathlib/Chair44 installations are not
  included in this repository.

The MIT license applies to our independently implemented comparison and
replay programs; embedded third-party excerpts, if any, remain subject to
their identified original terms. Preserve the notices when redistributing
source-derived evidence.

Frozen artifacts are retained byte-for-byte, including old packets that
predate these notices. Distribute this licensing document and the third-party
notices alongside them; their historical contents are not updated claims.
See the [historical-material guide](docs/HISTORICAL_MATERIAL.md).

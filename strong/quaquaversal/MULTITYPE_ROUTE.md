# Q003: a finite boundary structure for general hierarchy enforcement

This is an **applicability audit for an existing theorem**, not a new monotile
and not yet a list of decorated prism types. The main one-decoration target
remains open outside the families already rejected.

The Goodman–Strauss theorem cited in [LITERATURE.md](LITERATURE.md) provides
finite matching-rule decorations once hereditary boundary panels and the
specified sibling incidences have been supplied. Its “edges” are 2D panels
in this setting. A prism's five unsplit faces are inadequate: an internal
contact can cover only part of a face.

## Failed first refinement

Starting from the full carrier faces, transport face-boundary lines through
all sibling contact maps and through parent-to-boundary-child maps. Extend
each transported segment to a supporting chord of the relevant face. This
is an intentional overrefinement, not a minimality search.

Line closure stabilizes with 51 panels: 12,12,24,1,2 on the bottom, top,
long rectangle, square, hypotenuse rectangle. Area matching passes, but
there are **10 missing sibling-vertex incidences**, and the later segment
audit also finds **28 sibling-edge mismatches**. Thus area agreement alone
does not establish the hypotheses. Both the failed partition and audit are
preserved in `artifacts/panel_refinement.json` and `panel_audit.json`.

## Second refinement

Seed additional horizontal/vertical face-chart lines at those missing
vertices, then repeat closure. The result has **60 panels**, distributed
12,12,24,4,8. There are 38 distinct boundary vertices and 96 distinct
boundary segments across the panels.

The exact audit checks:

- 240 positive-area sibling panel overlaps are whole-panel identifications;
- 240 positive-area parent/child overlaps place a whole child panel inside
  a parent panel;
- 346 sibling vertex incidences land on listed vertices, and parent
  vertices are inherited by every incident child;
- 536 positive-length sibling edge incidences identify complete segments;
- every one of the 96 parent segments is covered by collinear child
  segments, with no child segment crossing a parent segment endpoint.

Together with the already checked solid partition and face coverage, these
are finite certificates for the hereditary-panel and sibling-incidence
conditions used here. They support the standard **multiple-decoration**
route. They do not specify the skeleton packets, vertex wires, decorated
tile inventory or physical jigsaw geometry of that construction.

The substitution must retain its canonical frame (or a corresponding
orientation mark) when interpreted as a marked prototile system; the bare
carrier has an improper self-symmetry which need not preserve its subdivision.
Do not silently identify these two framed states.

## Reproduce

```sh
uv run --locked python strong/quaquaversal/refine_panels.py
uv run --locked python strong/quaquaversal/audit_panels.py
uv run --locked python strong/quaquaversal/refine_panels.py \
  --seed-audit strong/quaquaversal/artifacts/panel_audit.json \
  --output strong/quaquaversal/artifacts/panel_refinement_v2.json
uv run --locked python strong/quaquaversal/audit_panels.py \
  --input strong/quaquaversal/artifacts/panel_refinement_v2.json \
  --output strong/quaquaversal/artifacts/panel_audit_v2.json
```

## Next constructive work

Choose a connected network of the refined internal panels, determine the
substitution power needed to link child networks to parent networks, and
make the transmitted finite labels explicit. Prove grouping and legal
deflation with those labels before claiming a successful matching-rule set.
Then address whether a recut/fusion can reduce the independently marked
types to congruent copies of one solid. The one-decoration obstruction
prevents simply erasing that extra information on the current proper prism.

[The symmetry lemma](SYMMETRY_LEMMA.md) supplies a direct finite-group
argument once symmetry-preserving supertile partitions at all scales have
actually been forced. It does not assume a finite orientation set.

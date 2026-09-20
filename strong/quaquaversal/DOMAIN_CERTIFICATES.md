# Choice contradictions through multiple propagation layers

Q026 supplies a finite proof format for a necessary forbidden conjunction
of center-star choices. It does not prove hierarchy enforcement or infinite
tilability. The rule being studied is still the 6,840-type closed-star rule.

## Assertions and sound operations

Fix the shared geometric pose table and the audited compatibility sets
`C(s,q)`: the allowed stars at a neighbor in relative pose `q`, conditional
on star `s` at the source. A certificate node is either **unknown**, making
no assertion about tile presence, or asserts that a tile is present at pose
`p` and its complete star belongs to a set `D`. A present tile with `D` empty
is a contradiction. Unknown must never be confused with an empty domain.

Four node operations suffice for the current propagation chain:

- **Choice.** A retained hypothesis `(p,s)` asserts presence at `p` with
  domain `{s}`. A deleted hypothesis produces unknown. Even when a center
  was known present in the original search, deleting its whole assertion
  is conservative and simplifies the conditional proof.
- **Forced neighbor.** From present `(p,D)`, a relative pose `q` forces a
  neighbor only if `q` occurs in every star in `D`. The neighbor is at
  `p ◦ q` and its domain is the **union** of `C(s,q)` over `s` in `D`.
  If presence or universal occurrence is not established, the result is
  unknown. If a present source already has an empty domain, the contradiction
  has already been established; propagating that empty set cannot invalidate
  the argument.
- **Intersection.** Assertions about the same pose combine by intersecting
  all known domains. Unknown inputs contribute nothing. If every input is
  unknown, the output is unknown too.
- **Arc restriction.** Given present `(p,D)` and present `(p ◦ q,E)`, retain
  exactly those `s` in `D` for which `q` occurs and `C(s,q)` meets `E`.
  An unknown right input makes no restriction. An unknown left input stays
  unknown; this operation does not itself assert its presence.

Every asserted geometric relation is checked with rational coordinates.
All node references point backward, so induction proves soundness: in any
admitted tiling satisfying the retained choice hypotheses, every known
node gives a necessary presence/domain assertion. Consequently a known
empty root domain proves that the conjunction of retained choices is
impossible. It says nothing against other choices for the same parent.

## Extracted two-layer certificate

The source is the formerly surviving Q021 assignment, model 5, parent key
`(boundary_index=515, cover_index=0)`. Its first forced layer and 2,440-step
arc run survive. A second forced layer survives, but its following arc run
fails after 38 reductions. The source records are
`neighbor_star_cut_seed.json`, `neighbor_star_cut_layer_1.json`,
`neighbor_star_cut_arcs.json`, `neighbor_star_cut_layer_2.json`, and
`neighbor_star_cut_arcs_2.json`.

`layered_choice_certificate.py` constructs lazy dependencies through both
forced layers and both arc traces. Only the ancestors of the failed domain
enter the certificate. It then deletes choice premises whenever replay still
has a known empty root, recomputing presence after every deletion.

The retained certificate has 1,070 nodes: 158 choice nodes, 742 forced-neighbor
nodes, 92 intersections, and 78 arc restrictions. Greedy deletion reduces
the required hypotheses from 158 to **eight**. This is not a claim of minimum
cut size. Nodes descended from deleted hypotheses remain in the stored graph
and may evaluate to unknown; the eight retained choices suffice nonetheless.

`verify_layered_choice_certificate.py` checks the graph independently of
extraction, using explicit sets and 820 exact geometric compositions. It
also checks membership of the retained choices in the original parent
problem. Not all hypotheses were fixed there, so the certificate gives
**zero direct parent exclusions**.

## Effect on the ongoing search

`extend_choice_cut_catalog.py` checks the audit hashes and appends this cut
to the previous 162 in `choice_cut_catalog_163.json`. The eight-choice cut
rejects Q023 finite SAT model 5, although that model passed its immediate
neighbor-star and arc test. The two-layer proof establishes a deeper
obstruction for it without assuming that its optional tiles were present.

On the Q024 full frontier (`choice_cut_frontier_seed.json`), the conjunction
is still possible in parent keys `(515,0)`, `(635,0)`, `(645,0)`, `(655,0)`,
and `(715,0)`. Six of the eight hypotheses are unfixed in each case, so this
cut alone is neither a direct contradiction nor a unit removal there.
These are finite-domain observations, not five actual tilings.

The next SAT refinement can use this same proof language for deeper
counterexamples. Its important requirement is to recompute presence when
removing hypotheses: a failure involving an optional position is not a valid
cut if the remaining hypotheses no longer force that position.

## Reproduction

Run the three commands after their inputs in `reproduce.py`:

```sh
uv run --locked python strong/quaquaversal/layered_choice_certificate.py
uv run --locked python strong/quaquaversal/verify_layered_choice_certificate.py
uv run --locked python strong/quaquaversal/extend_choice_cut_catalog.py
```

The certificate, independent audit, and catalog all bind their input hashes.
No new Lean theorem, external review, solid realization, or full aperiodicity
claim is made.

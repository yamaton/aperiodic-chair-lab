# Independent review of the undergraduate tutorial

*16–17 September 2026. AI review requested by the user; no human student
trial or independent human mathematical review is claimed.*

## Review question and method

The user asked reviewers to check correctness **and** whether a reader with
undergraduate vectors, matrices and elementary calculus, but no prior tiling
theory, could follow the exposition without abrupt increases in prerequisite
knowledge. Three separately assigned agents read the same working-tree draft:

| Reviewer | Assignment and checks |
|---|---|
| `tutorial_math_review` | Mathematical implications and claim scope; compared the grouping tables, geometric manuscript and symmetry audit; independently checked the 56-cube partition and two overlap witnesses |
| `tutorial_beginner_review` | Sequential first reading from the promised prerequisites before consulting research notes; notation, motivation, transitions, and manageable worked steps |
| `review_grid_symmetry` | New tutorial-specific assignment to an agent previously used for an unrelated Lean review; inspected figures, exercises, physics prerequisites and mobile Firefox rendering |

The reviewers did not edit the tutorial. The coordinator compared their
findings, reread the relevant passages, implemented revisions, and requested
bounded follow-up reviews. Mathematical and pedagogical reviewers separately
checked the revised prose. The presentation reviewer was also asked to
inspect the new enlargement controls; interaction checks are recorded in
the [presentation verification](tutorial_verification.json).

The initial reviewed files had SHA-256 hashes:

```text
Markdown f4d9234a5d1111e2f45776931394eaca2e906178920ebb2536d65983ce914fae
HTML     0f69fffee43dbc7f26280dfe7bf0ce656766b7363632cedb5c56ccff60af95c4
```

The verification JSON contains the current post-revision artifact hashes.
No proof source or frozen construction data changed in this review.

## Findings and changes

No reviewer reported a major mathematical error in the checked arguments.
That finding is limited to the review performed; it is not a new formal
verification of the real geometry or the entire research project. The main
problems were insufficient teaching steps and mobile diagram legibility.
Line references in the table refer to the **initial** reviewed Markdown.

| Priority / location | Finding | Revision |
|---|---|---|
| High, §7.1 Step B, lines 701–740 | Polynomial division with polynomial coefficients, total degree, and continued surfaces arrived together after an elementary zero-count argument | Replaced the division terminology with the elementary identity `F(z) − F(a) = (z − a)G`, starting from difference of squares; defined total degree and explained the equal-degree conclusion; displayed the cubic/quartic coefficients; added Exercise 19 to show why divisibility alone is insufficient |
| Medium, §4.1, lines 304–324 | The first forced-neighbor step was still only a result in a table | Listed its two candidates and the exact overlapping cube that excludes one; remaining steps explicitly repeat that procedure |
| Medium, §§4.2–4.3, lines 342–389 | Inverse coordinates lacked a worked example, and `D+--` denoted different neighbors in two frames | Computed one nonidentity notch-owner inverse in full; distinguished actual sibling S from hypothetical neighbor J and named their shared cube in the child's frame |
| Medium, §7.1 opening, lines 606–660 | Many constants and derivatives appeared before the purpose of the five steps became visible | Added a five-question roadmap, introduced the roles of width/depth/reach, defined the partial derivatives used, and clarified closedness and surface interior |
| Medium, §9, lines 1095–1114 | Phase, wavevector and complex conjugation were undeclared prerequisites | Introduced phase as a planar arrow, complex notation and squared magnitude, wavelength and wavevector; linked Figure 10's arrow example to its point on the intensity curve |
| Medium, §12, lines 1309 onward | Exercises returned to Section 3 only after printing and physics; no timely invitations to test understanding | Added an ordered reading route, checkpoints in the prose, a short face-alignment Exercise 18 and the factor Exercise 19, with answers |
| Medium, all figures on mobile | At viewport 390 px, every original figure shrank to 358 px; important labels were roughly 4–7 px, despite no page overflow | Added visible whole-figure enlargement buttons and an offline full-size view with pan/scroll, keyboard opening, Escape/Close and focus restoration; kept the overview in the prose |
| Low, Figure 4 | Four horizontal layers required an unprompted reconstruction of a three-dimensional child | Added a guided trace of child 0 through its four negative-z and three positive-z cubes |
| Low, §7.1 surface definition | The port box's normal extent was not specified in the tutorial itself | Stated `|u|, |v| ≤ 1, |s| ≤ h` and the precise local material replacement |
| Low, §7.1 symmetry transport | The formula connecting physical and placement symmetries skipped the role of trivial tile self-symmetry | Inserted the self-map `j⁻¹ ∘ g ∘ f` and the resulting equations `AR = S`, `At + b = s` |
| Low, first use of parity class | The term preceded its odd/even explanation | Added the coordinatewise odd/even meaning at first use |

The coordinator corrected one proposed reviewer example before adopting it:
the reference child's layer counts are **four below zero and three above**,
not the reverse. The reviewer confirmed the correction. The diagram itself
was already correct. Review suggestions were checked against the object,
not incorporated automatically.

## Follow-up assessment and verification

The mathematical reviewer rechecked the new overlap witnesses, inverse
coordinate example, factor argument, affine degree reasoning, line
coefficients, port-box definition, self-isometry composition, and Exercises
18–19. All five of that reviewer's original findings were considered
addressed, with no new mathematical or scope issue found.

The beginner reviewer found the main prerequisite jumps substantially
addressed. In particular, Step B now advances by elementary factorization,
total degree and a worked coefficient comparison. It remains the most
demanding passage, but its difficulty now comes from following a detailed
argument rather than encountering unexplained prerequisite machinery.
The final small first-use parity clarification was also incorporated.

The presentation reviewer independently confirmed readable enlarged mobile
flowchart labels, keyboard opening, panning, Escape/Close, and focus return,
as well as the revised wave primer, exercise route, layer walkthrough, and
interference marker. Both that reviewer and the coordinator noticed that
opening at the left edge hid the flowchart's entry node. The coordinator
then centered the initial horizontal scroll and added a check of this
initial position to the automated verification. The reviewer's independent
UI check precedes this final small adjustment.

The coordinator rebuilt the figures and offline HTML. The figure generator
checked the exact 56-cube partition. Firefox checks cover both 1200 px and
390 px widths, all ten embedded figures, 635 MathML expressions, 29 display
formulas, 49 local links, and zero external network requests/page errors.
All ten figures at both viewport widths were opened from the keyboard,
matched to their overview image, and closed by Escape or Close with focus
restored. All mobile enlarged images support horizontal panning at a width
of at least 1000 px; the PNGs retain their larger source resolutions.
The original ten figures and all formulas also remain available with
JavaScript disabled. See the current JSON for exact hashes and checks.

No Lean rebuild was needed: formal source and theorem scope were unchanged.
The mathematical follow-up was a bounded review of the changed explanations,
not a repeat of every historical audit.

## What this review cannot establish

Three AI readings do not measure comprehension by actual students. The
next useful teaching test is to have a reader work the first forced contact,
explain the two coordinate frames, and solve the factor exercise without
consulting its answer. Section 7.1 is an appropriate place to pause for a
separate session; it need not be treated as a single uninterrupted reading.

The [current tutorial](APERIODIC_CHAIR_TUTORIAL.md) still delegates complete
finite contact tables to the generated appendix and distinguishes written
geometry from Lean grid theorems. This review does not turn the exact-solid
argument into a theorem about an STL or manufactured object. Changes remain
local; the user subsequently requested a commit. No publication or reviewer
outreach was performed.

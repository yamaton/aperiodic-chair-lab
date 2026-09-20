# Primary-source notes

Accessed 20 September 2026 UTC. This is a targeted review, not a priority audit.
Downloaded third-party papers are kept in `/tmp`, not redistributed here.

## Conway and Radin: the substitution

J. H. Conway and C. Radin, *Quaquaversal tilings and rotations*,
Inventiones Mathematicae 132 (1998), 179–188.
[Author-hosted paper](https://web.ma.utexas.edu/users/radin/papers/quaquaversal.pdf),
[author-hosted diagrams](https://web.ma.utexas.edu/users/radin/federation/quaqua.html).

Section II, pp.180–181 and Figures 1–2 specify two half-height slabs. In A,
the rectangular union of children 2 and 3 is turned through a quarter turn
about its long axis. In B, the equilateral-prism union of children 3 and 4
is turned through a third turn about its prism axis. Section II also supplies
an interior three-step child address (2B,2B,4A) used for an expanding tiling.
Our coordinate convention and sign choices must be checked against these
figures, not inferred from an orientation list alone.

## Radin's retrospective

C. Radin, *Conway and aperiodic tilings*, Mathematical Intelligencer 43
(2021), 15–20, [author PDF](https://web.ma.utexas.edu/users/radin/papers/conway.pdf).

The discussion accompanying Figure 8 says the author expected an extension
of the pinwheel matching-rule technique to work, but did not pursue it.
This is motivation, **not** an explicit quaquaversal matching-rule construction
or a current nonexistence/open-problem certificate.

## Goodman–Strauss: general enforcement

C. Goodman–Strauss, *Matching rules and substitution tilings*, Annals of
Mathematics 147 (1998), 181–223.
[Journal](https://annals.math.princeton.edu/articles/12903),
[author manuscript](https://strauss.hosted.uark.edu/papers/MRandST.pdf).

The theorem allows arbitrary Euclidean isometries and finite decoration
types. It requires hereditary boundary subdivisions and sibling-edge-to-edge
compatibility (Section 1.4); its technical “edges” have dimension d−1, so
in three dimensions these are boundary **panels**, not just line segments.
Checking these hypotheses for this non-face-to-face prism substitution is
an actual task. The original five unsplit faces cannot simply be assumed to
satisfy them. Its Lemma 4.3 addresses infinite cyclic isometry groups, which
is relevant to screw exclusion, not merely translational aperiodicity.
The theorem does not promise a single decoration or one congruent solid.

## Vereshchagin: a recent theorem variant

N. Vereshchagin, *Goodman-Strauss theorem revisited*, arXiv:2510.02842v1
(2025), [versioned text](https://arxiv.org/html/2510.02842v1).

The inspected version formulates its construction for planar polygons with
translations only. It discusses subtleties in earlier general constructions.
It cannot be applied to a three-dimensional dense-orientation tiling just
by quoting its abstract. Keep this route separate from the 1998 theorem.

# From curved chair contacts to a single cubic grid

*16 September 2026. Short mathematical manuscript; exact frozen design.*

**Abstract.** We give a registration argument for the specified curved-cap
chair. Any covering of Euclidean three-space by congruent copies with
disjoint interiors has one common cubic frame and handedness, and obeys
the prescribed discrete port rules. The proof uses local finiteness,
polynomial rigidity, adjacent-cell ownership and retained interior material.
Its finite coordinate hypotheses are checked separately. This manuscript
does not prove existence or formalize real geometry in Lean.

## 1. Solid, data and theorem

Let $L$ be the union of the seven closed unit cubes with lower corners
in $\{-1,0\}^3\setminus\{(0,0,0)\}$. Each of its 24 exposed unit faces
has eight ports. A port record is $(p,U,V,N,k)$: center, ordered base-plane
axes, outward normal, and nonzero signed key. Use the accompanying
[192-record data file](../audit/frozen_v1/candidate.json), SHA-256
`95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54`.
The data file is part of the specification, not a presumed contact census.

Set $w=1/64$, $\delta=1/4096$, and

$$
 \phi(u,v)=(1-u^2)(1-v^2)(1+u/5+v/7).
$$

In the port box, points are $p+wuU+wvV+sN$, with
$|u|,|v|\le1$ and $|s|\le h=141/35840$. Replace the carrier's local
condition $s\le0$ by $s\le k\delta\phi(u,v)$; elsewhere leave $L$
unchanged. This defines the closed solid $Q$, including the seams.
The graph is zero along its square boundary. Its nonnegative factor obeys
$0\le\phi\le47/35$, and $1\le|k|\le12$, giving the stated reach $h$.

The following coordinate facts are verified from the data (see §4):

- $U,V,N$ are signed coordinate axes and form an orthonormal frame.
  The actual exposed face center is $f=p-(3U+V)/16$. Its inside cube
  has center $f-N/2$; the cube centered at $f+N/2$ is absent from $L$.
- Each face has exactly eight distinct ports. Their squares are at least
  $19/64$ from face edges; different port boxes in a tile are disjoint.
- Writing $\chi=\det[U,V,N]$, all occurrences of a signed key have the
  same $\chi(k)$, and $\chi(-k)=-\chi(k)$.

The prescriptions therefore give genuine boundary graphs with two local
sides in their interiors. The solid is regular closed: locally it is a
closed graph subregion or the unchanged polycube, and the prescriptions
agree on the seams. Each carrier cube retains its middle half, hence an
open ball of radius $1/4$. Also $Q\subset[-1-h,1+h]^3$, so its diameter
is less than 4. More generally the inset cube of margin
$\rho=1/64>h$ has a neighborhood contained in the tile interior.

**Registration theorem.** Let $\mathcal T$ be a family of distinct
congruent copies of $Q$, covering $\mathbb R^3$ with pairwise-disjoint
interiors. Placements may initially be arbitrary affine isometries,
including reflections. After a common Euclidean change of coordinates,
their chosen placements have integer origins and proper cubic frames.
Every unit cube has exactly one carrier owner, and every common exposed
unit face has equal port centers and ordered axes, opposite normals and
opposite signed keys.

The conclusion is the geometric interpretation of the proper grid matching
model. It assumes neither a hierarchy nor any pre-existing common grid.

## 2. Local contact and rigidity

**Lemma 1 (an open cap mate).** Every cap has an open patch coinciding
with a cap of another tile.

*Proof.* Choose one radius-$1/4$ interior ball per tile. The balls are
pairwise interior-disjoint. A tile meeting a radius-$R$ ball has its
chosen ball inside the concentric radius-$(R+17/4)$ ball. A volume bound
on any finite subfamily gives at most $(4R+17)^3$ such tiles. Thus the
family is locally finite, before any registration has been established.

At an interior cap point $x$, approach from the tile's exterior.
Coverage and local finiteness give another tile containing a subsequence;
closedness puts $x$ in that tile. It cannot contain $x$ in its interior,
since interior points of the first tile approach $x$. Thus finitely many
other boundaries cover the cap. Each is a finite union of closed planar
and polynomial pieces. A finite relatively closed cover of an open surface
patch has a member with nonempty relative interior. A plane cannot contain
an open part of this polynomial graph, and finitely many seams cannot
contain a surface-open set. Shrinking the coincidence gives two cap
interiors with an open common patch. ∎

**Lemma 2 (full frame rigidity).** An open coincidence of two caps under
an ambient isometry identifies their entire base squares, centers and
ordered base axes. Only reversal of the normal is possible, with the
corresponding change in the sign of the key.

*Proof.* Uniformly scale all three ambient coordinates by $1/w$, obtaining
$z=H\phi(u,v)$, where $H=k/64\ne0$. This uniform scaling preserves the
isometry question. Write $P_H=z-H\phi$. Substitute this graph into the
moved second defining polynomial. The resulting polynomial in $u,v$
vanishes on an open set and hence identically. Division by the monic
polynomial $P_H$ proves divisibility. Both defining polynomials have
total degree five, so they differ by a nonzero constant. Consequently the
isometry identifies their entire algebraic graphs.

The full graph contains exactly five straight lines, all at $z=0$:

$$
 u=1,\quad u=-1,\quad v=1,\quad v=-1,\quad 1+u/5+v/7=0.
$$

Indeed, substituting $(u,v,z)=(x+dt,y+et,c+ft)$ gives leading coefficient
$H d^2e^2(d/5+e/7)$. If $d=0,e\ne0$, the cubic coefficient forces
$x=\pm1$; if $e=0,d\ne0$, it forces $y=\pm1$. If both $d,e$ are nonzero,
$e=-7d/5$, and the quartic coefficient forces $1+x/5+y/7=0$.
In these cases the polynomial vanishes along the line, so $z=0$.
A vertical nonconstant line is impossible on a graph.

The two parallel pairs recover the square and its center. The remaining
line distinguishes the ordered axes: among square symmetries, its unequal
positive coefficients and nonzero constant term permit only the identity.
The five lines also recover the base plane. Thus the isometry fixes the
ordered base frame, with normal reversal as its sole remaining option;
the graph equation then gives $H_1=\pm H_2$. The recovered square is
precisely the bounded cap domain. The fifth line is used only on the
algebraic continuation, not as extra physical material. ∎

**Lemma 3 (registered adjacent owner).** An open cap mate gives a proper
cubic relative frame, an integer relative shift and ownership of the
opposite unit cube.

*Proof.* Normalize the first tile to the identity and write the other as
$x\mapsto t+Rx$. Lemma 2 gives

$$
 RU_B=U_A,\quad RV_B=V_A,\quad RN_B=\sigma N_A,\quad k_A=\sigma k_B.
$$

If $\sigma=1$, the two local interiors occupy the same side of the
coincident graph, contradicting disjointness. Hence $\sigma=-1$, and

$$
 R=U_AU_B^{\mathsf T}+V_AV_B^{\mathsf T}-N_AN_B^{\mathsf T},\qquad
 t=p_A-Rp_B=f_A-Rf_B.
$$

The frame is a signed coordinate permutation. The corresponding face
centers have integral normal coordinates and half-integral tangential
coordinates, so $t\in\mathbb Z^3$. Moreover

$$
 t+R(f_B-N_B/2)=f_A+N_A/2,
$$

which identifies the outward adjacent cube as a cube owned by the second
tile. Finally $\det R=-\chi(k_A)\chi(k_B)=1$. Properness has been
derived even though arbitrary reflected placements were allowed. ∎

## 3. Global registration

**Lemma 4 (carrier coverage).** Any component of the graph of open cap
matches owns every unit cube of its reference grid, exactly once.

*Proof.* Choose one member as reference. By Lemma 3 all placements in its
component are integral and proper in that frame. Two distinct members
cannot own the same cube: both would contain its retained open core.
For an owned cube and any face-adjacent cube, either the same chair owns
both or the intervening face is exposed. In the latter case, Lemmas 1
and 3 supply a cap mate in the component owning the adjacent cube.
The nonempty set of owned cubes is therefore closed under all lattice
adjacency steps and equals the whole connected cubic lattice. ∎

**Lemma 5 (component exhaustion).** Every actual tile belongs to that
component.

*Proof.* Take any tile $A$ and the center $c$ of its retained open
radius-$1/4$ ball. Lemma 4 supplies a component cube containing $c$,
owned by a tile $B$. Clamp each coordinate of $c$ into that cube's
inset of margin $\rho=1/64$, obtaining $y$. Since $h<\rho$, the
point $y$ lies in the interior of $B$. Also

$$
 \|y-c\|^2\le3\rho^2=3/4096<1/16,
$$

so it lies in the interior of $A$. Disjoint interiors force $A=B$.
This argument uses carrier coverage, not an unproved assertion that the
component's curved material already fills space. ∎

*Completion of the theorem.* Lemmas 4–5 give a single registered component,
unique carrier ownership and common handedness. Across an exposed face,
each of its eight caps has a mate. Lemma 3 puts all these mates in the
same outward cube, so unique ownership makes them the same neighboring
tile. Lemma 2 identifies each full bounded cap. Distinct centers give an
injective correspondence to the eight ports on the opposite face, hence
a bijection, with the frames and keys specified in Lemma 3. This proves
all interface rules. ∎

## 4. Evidence, attribution and scope

The local polynomial identities and coordinate hypotheses are reproduced
from the repository root by:

```sh
uv run --locked python strong/audit/verify_caps.py
uv run --locked python strong/audit/check_reflections.py
uv run --locked python strong/audit/scrutinize_grid_bridge.py
uv run --locked python strong/audit/grid_bridge_crosscheck.py
```

The last two checks reconstruct exposed-face ownership, verify all 1,536
opposite-key matches and recover 86 distinct necessary single-cap poses.
They also check a periodic family of separated feature boxes, useful for
the separate grid-to-physical existence argument. Their finite outputs do
not establish the analytic and topological implications above. The exact
interface rules, rather than these 86 necessities, yield 44 fitting
whole-chair contacts in the separate discrete census.

Lemma 5 adapts Tsiokos's retained-core argument in the pinned Chair44 source,
`Proved/CarrierCoreCover.lean`; see the [proof comparison](CHAIR44_PROOF_COMPARISON.md#5-an-attributed-simplification-of-our-geometric-argument).
Chair44 uses square pyramids and a different contact-rigidity argument.
The shared discrete system and the Goodman–Strauss chair/recognition
precedents are recorded in the [exact comparison](TSIOKOS_CHAIR44_COMPARISON.md)
and [local parent note](../MOTIF_GROUPING.md). No new matching-system
discovery or priority is claimed here.

This note consolidates the [longer geometric scrutiny](GEOMETRIC_GRID_SCRUTINY.md)
without changing the solid. It was prepared by the coordinating AI assistant.
A subsequent [fresh independent agent review](FOLLOWUP_INDEPENDENT_REVIEW.md)
found no substantive defect and supplied an independent arithmetic probe;
no external human review is claimed. The [dependency table](../../docs/PROOF_STATUS.md)
separates this written registration theorem from the Lean grid theorems,
initial existence and faithful transport of physical symmetries. Analytic
continuation is essential to this proof; triangulated meshes and
manufactured approximations do not inherit its conclusion.

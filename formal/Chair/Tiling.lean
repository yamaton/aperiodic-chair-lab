import Chair.Boundary
import Chair.Recurrence

namespace Chair

/-- An arbitrary set of decorated proper grid placements. -/
abbrev GridTiling := GridMotion → Prop

def placed (g : GridMotion) : Solid := g.solid fine
def Owns (g : GridMotion) (q : V3) : Prop := q ∈ (placed g).cells

/-- Exact coverage and matching only: no parent, parity or hierarchy premise. -/
structure LegalTiling (T : GridTiling) : Prop where
  cover : ∀ q, ∃ g, T g ∧ Owns g q
  unique_owner : ∀ {g h q}, T g → T h → Owns g q → Owns h q → g = h
  compatible : ∀ {g h}, T g → T h → g ≠ h →
    interfacesFit (placed g) (placed h) zero = true

def moveTiling (g : GridMotion) (T : GridTiling) : GridTiling :=
  fun h => ∃ p, T p ∧ h = g.comp p

theorem owns_covariant (g p : GridMotion) (q : V3) :
    Owns (g.comp p) (g.cell q) ↔ Owns p q := by
  unfold Owns placed
  rw [GridMotion.solid_comp]
  change g.cell q ∈ ((p.solid fine).cells.map g.cell) ↔ q ∈ (p.solid fine).cells
  rw [List.mem_map]
  constructor
  · rintro ⟨a, ha, heq⟩
    exact g.cell_injective heq ▸ ha
  · intro hq
    exact ⟨q, hq, rfl⟩

theorem LegalTiling.move {T : GridTiling} (hT : LegalTiling T) (g : GridMotion) :
    LegalTiling (moveTiling g T) := by
  constructor
  · intro q
    obtain ⟨p, hp, hq⟩ := hT.cover (g.inv.cell q)
    refine ⟨g.comp p, ⟨p, hp, rfl⟩, ?_⟩
    simpa only [GridMotion.cell_inv_cell] using
      (owns_covariant g p (g.inv.cell q)).mpr hq
  · rintro _ _ q ⟨p, hp, rfl⟩ ⟨r, hr, rfl⟩ hqp hqr
    have hp' : Owns p (g.inv.cell q) :=
      (owns_covariant g p _).mp (by simpa using hqp)
    have hr' : Owns r (g.inv.cell q) :=
      (owns_covariant g r _).mp (by simpa using hqr)
    exact congrArg g.comp (hT.unique_owner hp hr hp' hr')
  · rintro _ _ ⟨p, hp, rfl⟩ ⟨r, hr, rfl⟩ hne
    have hpr : p ≠ r := fun heq => hne (congrArg g.comp heq)
    simpa only [zero, placed, GridMotion.solid_comp] using
      (GridMotion.interfacesFit_covariant_zero g (placed p) (placed r)).mpr
        (hT.compatible hp hr hpr)

theorem LegalTiling.contact_of_touching {T : GridTiling} (hT : LegalTiling T)
    {g h : GridMotion} (hg : T g) (hh : T h) (hne : g ≠ h)
    (htouch : ∃ f ∈ (placed g).faces, ∃ f' ∈ (placed h).faces, Opposed f f' zero) :
    Contact (placed g) (placed h) zero := by
  refine ⟨?_, htouch, (interfacesFit_eq_true_iff _ _ _).mp (hT.compatible hg hh hne)⟩
  intro a ha b hb heq
  have hab : a = b := by simpa [zero, V3.add] using heq
  exact hne (hT.unique_owner hg hh ha (hab.symm ▸ hb))

/-- The neighboring placement is obtained from cube coverage, not supplied
as a completeness assumption on a finite neighborhood. -/
theorem LegalTiling.exposed_face_has_neighbor {T : GridTiling} (hT : LegalTiling T)
    {g : GridMotion} (hg : T g) {f : Face} (hf : f ∈ (placed g).faces) :
    ∃ h, T h ∧ h ≠ g ∧ ∃ f' ∈ (placed h).faces,
      Opposed f f' zero ∧ FaceFit f f' zero := by
  obtain ⟨hn, q, hq, hc, hout⟩ := (placed_fine_boundary g).1 f hf
  obtain ⟨h, hh, hnext⟩ := hT.cover (q.add f.normal)
  have hne : h ≠ g := by
    intro heq
    exact hout (heq ▸ hnext)
  have hprev : q ∉ (placed h).cells := by
    intro hi
    exact hne (hT.unique_owner hh hg hi hq)
  have hout' : (q.add f.normal).add (f.normal.scale (-1)) ∉ (placed h).cells := by
    simpa only [V3.add_assoc, V3.add_neg, V3.add_zero] using hprev
  obtain ⟨f', hf', hc', hn'⟩ := (placed_fine_boundary h).2 _ hnext _
    (normal_neg_mem f.normal hn) hout'
  have hopp : Opposed f f' zero := by
    constructor
    · rw [hc', faceCenter2_opposite]
      simpa [zero, V3.scale, V3.add] using hc
    · rw [hn']
      simp only [V3.scale_scale]
      exact (V3.scale_one f.normal).symm
  exact ⟨h, hh, hne, f', hf', hopp,
    (interfacesFit_eq_true_iff _ _ _).mp (hT.compatible hg hh (Ne.symm hne)) f hf f' hf' hopp⟩

theorem contact_normalized (s : Solid) (g h : GridMotion) :
    ∃ r : Fin 24, rotation r = (g.inv.comp h).frame.mat ∧
      (Contact (g.solid s) (h.solid s) zero ↔
        Contact s (moveSolid ⟨zero, rotation r⟩ s) (g.inv.comp h).shift) := by
  obtain ⟨r, hr⟩ := (g.inv.comp h).frame.exists_rotation
  refine ⟨r, hr, ?_⟩
  rw [zero, GridMotion.contact_relative, GridMotion.solid_eq_moveSolid, GridMotion.toPlacement,
    ← hr, contact_moveSolid_shift]

/-- Every actual touching pair has one of the previously certified 44
normalized contacts; no bound on the original placements is needed. -/
theorem LegalTiling.touching_contact_accepted {T : GridTiling} (hT : LegalTiling T)
    {g h : GridMotion} (hg : T g) (hh : T h) (hne : g ≠ h)
    (htouch : ∃ f ∈ (placed g).faces, ∃ f' ∈ (placed h).faces, Opposed f f' zero) :
    ∃ r : Fin 24, rotation r = (g.inv.comp h).frame.mat ∧
      (g.inv.comp h).shift ∈ fineAccepted r := by
  obtain ⟨r, hr, hnorm⟩ := contact_normalized fine g h
  exact ⟨r, hr, (fineContact_iff_accepted r _).mp
    (hnorm.mp (hT.contact_of_touching hg hh hne htouch))⟩

/-- The face-neighbor and finite-contact bridges combined. -/
theorem LegalTiling.exposed_face_neighbor_accepted {T : GridTiling} (hT : LegalTiling T)
    {g : GridMotion} (hg : T g) {f : Face} (hf : f ∈ (placed g).faces) :
    ∃ h, T h ∧ h ≠ g ∧
      (∃ f' ∈ (placed h).faces, Opposed f f' zero ∧ FaceFit f f' zero) ∧
      ∃ r : Fin 24, rotation r = (g.inv.comp h).frame.mat ∧
        (g.inv.comp h).shift ∈ fineAccepted r := by
  obtain ⟨h, hh, hne, f', hf', ho, hm⟩ := hT.exposed_face_has_neighbor hg hf
  exact ⟨h, hh, hne, ⟨f', hf', ho, hm⟩,
    hT.touching_contact_accepted hg hh (Ne.symm hne) ⟨f, hf, f', hf', ho⟩⟩

/-- Recurrence for arbitrarily placed macro objects. This does not assume
or prove that an arbitrary tiling has already been partitioned into macros. -/
theorem placed_macro_contact_recurrence (g h : GridMotion) :
    ∃ r : Fin 24, rotation r = (g.inv.comp h).frame.mat ∧
      (Contact (g.solid macroSolid) (h.solid macroSolid) zero ↔
        ∃ s : V3, (g.inv.comp h).shift = s.scale 2 ∧ fineContact r s) := by
  obtain ⟨r, hr, hnorm⟩ := contact_normalized macroSolid g h
  exact ⟨r, hr, hnorm.trans (macro_contact_recurrence r _)⟩

end Chair

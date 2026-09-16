import Chair.Tiling

namespace Chair

/-- View the tiling in the coordinate frame of a selected placement. -/
def normalizeTiling (T : GridTiling) (g : GridMotion) : GridTiling :=
  moveTiling g.inv T

theorem normalizeTiling_mem (T : GridTiling) (g h : GridMotion) :
    normalizeTiling T g h ↔ T (g.comp h) := by
  constructor
  · rintro ⟨p, hp, rfl⟩
    simpa only [← GridMotion.comp_assoc, GridMotion.comp_inv,
      GridMotion.identity_comp] using hp
  · intro hp
    refine ⟨g.comp h, hp, ?_⟩
    simp only [← GridMotion.comp_assoc, GridMotion.inv_comp, GridMotion.identity_comp]

theorem LegalTiling.normalize {T : GridTiling} (hT : LegalTiling T) (g : GridMotion) :
    LegalTiling (normalizeTiling T g) := hT.move g.inv

theorem normalizeTiling_identity {T : GridTiling} {g : GridMotion} (hg : T g) :
    normalizeTiling T g GridMotion.identity := by
  apply (normalizeTiling_mem T g _).mpr
  simpa using hg

theorem LegalTiling.pair_allowed {T : GridTiling} (hT : LegalTiling T)
    {g h : GridMotion} (hg : T g) (hh : T h) :
    g = h ∨ (disjoint (placed g) (placed h) zero = true ∧
      interfacesFit (placed g) (placed h) zero = true) := by
  by_cases heq : g = h
  · exact Or.inl heq
  · refine Or.inr ⟨?_, hT.compatible hg hh heq⟩
    simp only [disjoint, List.all_eq_true, Bool.not_eq_true', decide_eq_false_iff_not]
    intro a ha b hb heq'
    have hab : a = b := by simpa [zero, V3.add] using heq'
    exact heq (hT.unique_owner hg hh ha (hab.symm ▸ hb))

theorem GridMotion.comp_left_injective (g : GridMotion) {h k : GridMotion}
    (heq : g.comp h = g.comp k) : h = k := by
  have h := congrArg g.inv.comp heq
  simpa only [← comp_assoc, inv_comp, identity_comp] using h

theorem GridMotion.inv_comp_eq_iff (g h k : GridMotion) :
    g.inv.comp h = k ↔ h = g.comp k := by
  constructor
  · intro heq
    have h := congrArg g.comp heq
    simpa only [← comp_assoc, comp_inv, identity_comp] using h
  · rintro rfl
    simp only [← comp_assoc, inv_comp, identity_comp]

/-- Transfer coverage into a finite contact catalogue. Completeness is a
theorem about contacts, not a hypothesis about the given tiling's neighbors. -/
theorem LegalTiling.catalogue_covers {T : GridTiling} (hT : LegalTiling T)
    (hidentity : T GridMotion.identity)
    {ι κ : Type} (motion : ι → GridMotion) (face : κ → Face)
    (covers : ι → κ → Bool)
    (complete : ∀ h, Contact fine (placed h) zero → ∃ i, motion i = h)
    (face_mem : ∀ f, face f ∈ fine.faces)
    (covers_spec : ∀ i f, covers i f = true ↔
      ∃ b ∈ (placed (motion i)).faces, Opposed (face f) b zero) :
    ∀ f, ∃ i, T (motion i) ∧ covers i f = true := by
  intro f
  have hf : face f ∈ (placed GridMotion.identity).faces := by
    simpa only [placed, GridMotion.solid_identity] using face_mem f
  obtain ⟨h, hh, hne, b, hb, ho, _⟩ := hT.exposed_face_has_neighbor hidentity hf
  have hc : Contact fine (placed h) zero := by
    simpa only [placed, GridMotion.solid_identity] using
      hT.contact_of_touching hidentity hh (Ne.symm hne) ⟨face f, hf, b, hb, ho⟩
  obtain ⟨i, rfl⟩ := complete h hc
  exact ⟨i, hh, (covers_spec i f).mpr ⟨b, hb, ho⟩⟩

theorem LegalTiling.catalogue_pairs {T : GridTiling} (hT : LegalTiling T)
    {ι : Type} (motion : ι → GridMotion) (allowed : ι → ι → Bool)
    (allowed_spec : ∀ i j, allowed i j = true ↔
      motion i = motion j ∨
        (disjoint (placed (motion i)) (placed (motion j)) zero = true ∧
         interfacesFit (placed (motion i)) (placed (motion j)) zero = true)) :
    ∀ i j, T (motion i) → T (motion j) → allowed i j = true := by
  intro i j hi hj
  exact (allowed_spec i j).mpr (hT.pair_allowed hi hj)

/-- The same finite rejection witnesses also rule out coexistence when the
two tiles are not required to touch. -/
theorem rejectCheck_incompatible {s u : Solid} {t : V3} {w : RejectWitness}
    (hw : rejectCheck s u t w = true)
    (hd : disjoint s u t = true) (hf : interfacesFit s u t = true) : False := by
  cases w with
  | overlap i j =>
    simp only [rejectCheck] at hw
    split at hw
    next a b ha hb =>
      simp only [disjoint, List.all_eq_true, Bool.not_eq_true', decide_eq_false_iff_not] at hd
      exact hd a (List.mem_of_getElem? ha) b (List.mem_of_getElem? hb)
        (of_decide_eq_true hw)
    next => contradiction
  | mismatch i j =>
    simp only [rejectCheck] at hw
    split at hw
    next a b ha hb =>
      have hm := (interfacesFit_eq_true_iff _ _ _).mp hf a (List.mem_of_getElem? ha)
        b (List.mem_of_getElem? hb)
      simp only [Bool.and_eq_true, opposed_eq_true, Bool.not_eq_true'] at hw
      have fit := (faceFits_eq_true a b t).mpr (hm hw.1)
      rw [fit] at hw
      exact Bool.noConfusion hw.2
    next => contradiction

end Chair

import Chair.TranslationExclusion

namespace Chair

/-- Symmetry of the entire decorated placement set under a proper grid motion. -/
def GridSymmetry (T : GridTiling) (g : GridMotion) : Prop := moveTiling g T = T

@[simp] theorem moveTiling_identity (T : GridTiling) :
    moveTiling GridMotion.identity T = T := by
  funext p
  apply propext
  simp [moveTiling]

theorem moveTiling_comp (g h : GridMotion) (T : GridTiling) :
    moveTiling (g.comp h) T = moveTiling g (moveTiling h T) := by
  funext p
  apply propext
  constructor
  · rintro ⟨q, hq, rfl⟩
    exact ⟨h.comp q, ⟨q, hq, rfl⟩, GridMotion.comp_assoc g h q⟩
  · rintro ⟨q, ⟨r, hr, rfl⟩, rfl⟩
    exact ⟨r, hr, (GridMotion.comp_assoc g h r).symm⟩

theorem GridSymmetry.identity (T : GridTiling) : GridSymmetry T GridMotion.identity :=
  moveTiling_identity T

theorem GridSymmetry.comp {T : GridTiling} {g h : GridMotion}
    (hg : GridSymmetry T g) (hh : GridSymmetry T h) : GridSymmetry T (g.comp h) := by
  change moveTiling (g.comp h) T = T
  rw [moveTiling_comp, hh, hg]

theorem GridSymmetry.inv {T : GridTiling} {g : GridMotion}
    (hg : GridSymmetry T g) : GridSymmetry T g.inv := by
  change moveTiling g.inv T = T
  calc
    moveTiling g.inv T = moveTiling g.inv (moveTiling g T) := congrArg _ hg.symm
    _ = T := by rw [← moveTiling_comp, GridMotion.inv_comp, moveTiling_identity]

/-- Equal frames cancel, leaving exactly the difference of the two shifts. -/
theorem GridMotion.same_frame_difference {g h : GridMotion} (hf : g.frame = h.frame) :
    g.comp h.inv = translationMotion (g.shift.sub h.shift) := by
  apply GridMotion.ext
  · simp [GridMotion.comp, GridMotion.inv, translationMotion, hf,
      V3.sub_eq_add_neg, V3.add_comm]
  · simp [GridMotion.comp, GridMotion.inv, translationMotion, hf]

theorem GridSymmetry.same_frame_period {T : GridTiling} {g h : GridMotion}
    (hg : GridSymmetry T g) (hh : GridSymmetry T h) (hf : g.frame = h.frame) :
    TranslationPeriod T (g.shift.sub h.shift) := by
  apply (translationPeriod_iff_moveTiling _ _).mpr
  have hs := hg.comp hh.inv
  rwa [GridMotion.same_frame_difference hf] at hs

/-- Translation exclusion makes the frame map injective on all grid symmetries. -/
theorem LegalTiling.symmetry_frame_injective {T : GridTiling} (hT : LegalTiling T)
    {g h : GridMotion} (hg : GridSymmetry T g) (hh : GridSymmetry T h)
    (hf : g.frame = h.frame) : g = h := by
  have hz := hT.translation_period_zero (hg.same_frame_period hh hf)
  apply GridMotion.ext _ hf
  have hx := congrArg V3.x hz
  have hy := congrArg V3.y hz
  have hz' := congrArg V3.z hz
  apply V3.ext <;> simp only [V3.sub, zero] at * <;> omega

/-- Cardinality bound stated without a Mathlib cardinality interface. -/
theorem LegalTiling.symmetry_list_bound {T : GridTiling} (hT : LegalTiling T)
    (gs : List GridMotion) (hn : gs.Nodup)
    (hs : ∀ g ∈ gs, GridSymmetry T g) : gs.length ≤ 24 := by
  have hinj : ∀ g ∈ gs, ∀ h ∈ gs, g.frame.mat = h.frame.mat → g = h := by
    intro g hg h hh heq
    exact hT.symmetry_frame_injective (hs g hg) (hs h hh) (Frame.ext heq)
  have hn' : (gs.map fun g => g.frame.mat).Nodup := by
    apply List.pairwise_map.mpr
    exact hn.imp_of_mem (fun hg hh hne heq => hne (hinj _ hg _ hh heq))
  have hsub : gs.map (fun g => g.frame.mat) ⊆ rotations := by
    intro r hr
    obtain ⟨g, _, rfl⟩ := List.mem_map.mp hr
    exact g.frame.proper
  simpa only [List.length_map, rotations_length] using hn'.length_le_of_subset hsub

/-- All grid symmetries, not merely a supplied finite sample, have an exhaustive
list with at most 24 entries. Choice here is not an algorithm for deciding
whether a given frame occurs as a symmetry of an arbitrary infinite tiling. -/
theorem LegalTiling.symmetries_finite {T : GridTiling} (hT : LegalTiling T) :
    ∃ gs : List GridMotion, gs.length ≤ 24 ∧ ∀ g, g ∈ gs ↔ GridSymmetry T g := by
  classical
  let pick : Mat → Option GridMotion := fun r =>
    if h : ∃ g, GridSymmetry T g ∧ g.frame.mat = r then
      some (Classical.choose h)
    else none
  refine ⟨rotations.filterMap pick, ?_, ?_⟩
  · simpa only [rotations_length] using List.length_filterMap_le pick rotations
  · intro g
    rw [List.mem_filterMap]
    constructor
    · rintro ⟨r, _, hp⟩
      dsimp [pick] at hp
      split at hp
      next he =>
        have heq : Classical.choose he = g := Option.some.inj hp
        exact heq ▸ (Classical.choose_spec he).1
      next he => contradiction
    · intro hg
      refine ⟨g.frame.mat, g.frame.proper, ?_⟩
      have he : ∃ h, GridSymmetry T h ∧ h.frame.mat = g.frame.mat := ⟨g, hg, rfl⟩
      have heq : Classical.choose he = g :=
        hT.symmetry_frame_injective (Classical.choose_spec he).1 hg
          (Frame.ext (Classical.choose_spec he).2)
      simp only [pick, dite_eq_left he, heq]

end Chair

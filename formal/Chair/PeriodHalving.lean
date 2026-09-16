import Chair.Translations

namespace Chair

/-- Two origins in the same residue class can differ only by an even vector. -/
theorem even_difference_of_parity {o a v : V3}
    (ha : SameParity o a) (hav : SameParity o (a.add v)) :
    ∃ w : V3, v = w.scale 2 := by
  obtain ⟨k, hk⟩ := ha
  obtain ⟨l, hl⟩ := hav
  refine ⟨l.sub k, ?_⟩
  cases o; cases a; cases v
  simp only [V3.add, V3.scale, V3.mk.injEq] at hk hl
  apply V3.ext <;> simp only [V3.sub, V3.scale] <;> omega

/-- A period preserves a nonempty set of parent origins in one parity class,
so the period itself is an even integer vector. -/
theorem LegalTiling.period_even {T : GridTiling} (hT : LegalTiling T)
    {v : V3} (hp : TranslationPeriod T v) : ∃ w : V3, v = w.scale 2 := by
  obtain ⟨o, ho⟩ := hT.parent_common_parity
  obtain ⟨c, hc, _⟩ := hT.assemble.cover zero
  have hc' := (hp.groupCenters c).mpr hc
  exact even_difference_of_parity (ho c hc) (ho (translatePlacement v c) hc')

/-- Every period halves to a period of the actual legally deflated tiling.
The origin used here is the already defined deflation choice. -/
theorem LegalTiling.period_halves {T : GridTiling} (hT : LegalTiling T)
    {v : V3} (hp : TranslationPeriod T v) :
    ∃ w : V3, v = w.scale 2 ∧ TranslationPeriod (deflateTiling hT) w := by
  obtain ⟨w, rfl⟩ := hT.period_even hp
  exact ⟨w, rfl, hp.groupCenters.deflated (deflationOrigin hT)⟩

end Chair

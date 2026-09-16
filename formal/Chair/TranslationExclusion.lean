import Chair.PeriodHalving
import Chair.IntegerDescent

namespace Chair

/-- A translation period of any legal decorated grid tiling is zero.
Descent ranges over the class of legal tilings: deflation changes the tiling
while halving its period. No initial tiling existence is assumed or proved. -/
theorem LegalTiling.translation_period_zero {T : GridTiling} (hT : LegalTiling T)
    {v : V3} (hp : TranslationPeriod T v) : v = zero := by
  let P : V3 → Prop := fun w => ∃ U : GridTiling, LegalTiling U ∧ TranslationPeriod U w
  have halve : ∀ w, P w → ∃ u, w = u.scale 2 ∧ P u := by
    rintro w ⟨U, hU, hw⟩
    obtain ⟨u, heq, hu⟩ := hU.period_halves hw
    exact ⟨u, heq, deflateTiling hU, deflateTiling_legal hU, hu⟩
  exact doubling_descent P halve v ⟨T, hT, hp⟩

/-- Equivalent set-invariance formulation for the common translation action. -/
theorem LegalTiling.translation_stabilizer_trivial {T : GridTiling}
    (hT : LegalTiling T) {v : V3}
    (hp : moveTiling (translationMotion v) T = T) : v = zero :=
  hT.translation_period_zero ((translationPeriod_iff_moveTiling T v).mpr hp)

end Chair

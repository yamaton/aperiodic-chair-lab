import Chair.Frames

namespace Chair

namespace V3

/-- An integer vector's coordinate-sum norm, used only for well-founded descent. -/
def norm (v : V3) : Nat := v.x.natAbs + v.y.natAbs + v.z.natAbs

@[simp] theorem norm_eq_zero (v : V3) : v.norm = 0 ↔ v = zero := by
  cases v
  simp [norm, zero, V3.mk.injEq, Nat.add_eq_zero_iff, and_assoc]

@[simp] theorem norm_double (v : V3) : (v.scale 2).norm = 2 * v.norm := by
  simp [norm, scale, Int.natAbs_mul, Nat.mul_add]

theorem norm_lt_double {v : V3} (h : v ≠ zero) : v.norm < (v.scale 2).norm := by
  have hn : v.norm ≠ 0 := fun hz => h ((norm_eq_zero v).mp hz)
  rw [norm_double]
  omega

end V3

/-- If every vector satisfying a predicate has an integer half satisfying the
same predicate, only zero can satisfy it. The witnesses behind the predicate
may change at each step; no fixed tiling or chosen infinite sequence is needed. -/
theorem doubling_descent (P : V3 → Prop)
    (h : ∀ v, P v → ∃ w, v = w.scale 2 ∧ P w) :
    ∀ v, P v → v = V3.zero := by
  have descent : ∀ n, ∀ v, v.norm = n → P v → v = V3.zero := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v hv hp
      obtain ⟨w, hw, hpw⟩ := h v hp
      by_cases hz : w = V3.zero
      · simpa [hz] using hw
      · have hlt : w.norm < n := by
          rw [← hv, hw]
          exact V3.norm_lt_double hz
        have hwz := ih w.norm hlt w rfl hpw
        exact (hz hwz).elim
  intro v hp
  exact descent v.norm v rfl hp

end Chair

import Chair.MacroBoundary
import Chair.SolidContacts

namespace Chair

/-- Integral origins differ by an even vector. -/
def SameParity (a b : V3) : Prop := ∃ k : V3, b = a.add (k.scale 2)

namespace SameParity

theorem refl (a : V3) : SameParity a a := by
  exact ⟨V3.zero, by simp⟩

theorem trans {a b c : V3} (hab : SameParity a b) (hbc : SameParity b c) :
    SameParity a c := by
  obtain ⟨u, rfl⟩ := hab
  obtain ⟨v, rfl⟩ := hbc
  exact ⟨u.add v, by simp [V3.add_assoc]⟩

end SameParity

/-- Macro recurrence forces contacting macro origins to have the same parity
in the ambient frame, irrespective of their two orientations. -/
theorem macro_contact_sameParity (g h : GridMotion)
    (hc : Contact (g.solid macroSolid) (h.solid macroSolid) zero) :
    SameParity g.shift h.shift := by
  obtain ⟨r, _, hrec⟩ := placed_macro_contact_recurrence g h
  obtain ⟨k, hk, _⟩ := hrec.mp hc
  refine ⟨g.frame.apply k, ?_⟩
  have hrecover : h = g.comp (g.inv.comp h) := by
    simp only [← GridMotion.comp_assoc, GridMotion.comp_inv, GridMotion.identity_comp]
  have hs := congrArg GridMotion.shift hrecover
  change h.shift = (g.frame.apply (g.inv.comp h).shift).add g.shift at hs
  simpa only [hk, Frame.apply_scale, V3.add_comm] using hs

private theorem int_walk (P : Int → Prop) (hz : P 0)
    (hp : ∀ z, P z → P (z + 1)) (hm : ∀ z, P z → P (z - 1)) : ∀ z, P z := by
  intro z
  cases z with
  | ofNat n =>
    induction n with
    | zero => exact hz
    | succ n ih => simpa using hp (Int.ofNat n) ih
  | negSucc n =>
    induction n with
    | zero => simpa using hm 0 hz
    | succ n ih => simpa using hm (Int.negSucc n) ih

/-- Every integer cube is connected to the origin by unit axis steps. -/
theorem integer_grid_connected (P : V3 → Prop) (hz : P zero)
    (step : ∀ q n, n ∈ normals → P q → P (q.add n)) : ∀ q, P q := by
  have hx : ∀ x : Int, P ⟨x, 0, 0⟩ := by
    apply int_walk
    · exact hz
    · intro x h
      simpa [V3.add] using step ⟨x,0,0⟩ ⟨1,0,0⟩ (by decide +kernel) h
    · intro x h
      simpa [V3.add, Int.sub_eq_add_neg] using
        step ⟨x,0,0⟩ ⟨-1,0,0⟩ (by decide +kernel) h
  have hy : ∀ x y : Int, P ⟨x,y,0⟩ := by
    intro x
    apply int_walk
    · exact hx x
    · intro y h
      simpa [V3.add] using step ⟨x,y,0⟩ ⟨0,1,0⟩ (by decide +kernel) h
    · intro y h
      simpa [V3.add, Int.sub_eq_add_neg] using
        step ⟨x,y,0⟩ ⟨0,-1,0⟩ (by decide +kernel) h
  rintro ⟨x,y,z⟩
  apply int_walk (fun z => P ⟨x,y,z⟩) (hy x y) _ _ z
  · intro z h
    simpa [V3.add] using step ⟨x,y,z⟩ ⟨0,0,1⟩ (by decide +kernel) h
  · intro z h
    simpa [V3.add, Int.sub_eq_add_neg] using
      step ⟨x,y,z⟩ ⟨0,0,-1⟩ (by decide +kernel) h

/-- All origins of any legal tiling by the actual macro have a common residue
modulo two. The result uses infinite coverage, rather than patch connectivity. -/
theorem LegalSolidTiling.macro_common_parity {T : GridTiling}
    (hT : LegalSolidTiling macroSolid T) :
    ∃ origin : V3, ∀ g, T g → SameParity origin g.shift := by
  obtain ⟨g₀, hg₀, hzero⟩ := hT.cover zero
  refine ⟨g₀.shift, ?_⟩
  have all_cubes : ∀ q, ∀ g, T g → q ∈ (g.solid macroSolid).cells →
      SameParity g₀.shift g.shift := by
    apply integer_grid_connected
    · intro g hg hq
      have heq := hT.unique_owner hg₀ hg hzero hq
      rw [← heq]
      exact SameParity.refl _
    · intro q n hn ih g hg hnext
      obtain ⟨p, hp, hq⟩ := hT.cover q
      have hpar := ih p hp hq
      by_cases heq : p = g
      · simpa only [heq] using hpar
      · exact hpar.trans (macro_contact_sameParity p g
          (hT.contact_of_adjacent hp hg heq (placed_macro_boundary p)
            (placed_macro_boundary g) hn hq hnext))
  intro g hg
  have hcell : (⟨-2,-2,-2⟩ : V3) ∈ macroSolid.cells := by
    rw [macro_eq_cached]
    decide +kernel
  exact all_cubes (g.cell ⟨-2,-2,-2⟩) g hg
    (List.mem_map.mpr ⟨_, hcell, rfl⟩)

end Chair

import Chair.MacroAssembly
import Chair.MacroParity
import Chair.Deflation

namespace Chair

/-- The common residue is derived for every actual parent placement. -/
theorem LegalTiling.parent_common_parity {T : GridTiling} (hT : LegalTiling T) :
    ∃ origin : V3, ∀ c, groupCenters T c → SameParity origin c.shift :=
  hT.assemble.macro_common_parity

/-- Universal grouping followed by alignment and halving yields another
legal tiling of exactly the same decorated fine chair. -/
theorem LegalTiling.grouping_deflation {T : GridTiling} (hT : LegalTiling T) :
    ∃ origin : V3,
      (∀ c, groupCenters T c → SameParity origin c.shift) ∧
      LegalTiling (deflated (groupCenters T) origin) := by
  obtain ⟨o, ho⟩ := hT.parent_common_parity
  exact ⟨o, ho, hT.assemble.deflate o ho⟩

/-- Choose an origin from the proved common parity class. Its absolute
position is a coordinate choice, not additional hierarchy information. -/
noncomputable def deflationOrigin {T : GridTiling} (hT : LegalTiling T) : V3 :=
  Classical.choose hT.grouping_deflation

noncomputable def deflateTiling {T : GridTiling} (hT : LegalTiling T) : GridTiling :=
  deflated (groupCenters T) (deflationOrigin hT)

theorem deflateTiling_legal {T : GridTiling} (hT : LegalTiling T) :
    LegalTiling (deflateTiling hT) :=
  (Classical.choose_spec hT.grouping_deflation).2

/-- Iteration stays in the same legal tiling class at every finite depth.
This construction is conditional on the supplied initial legal tiling. -/
noncomputable def iteratedDeflation {T : GridTiling} (hT : LegalTiling T) :
    Nat → {U : GridTiling // LegalTiling U}
  | 0 => ⟨T, hT⟩
  | n + 1 =>
    let previous := iteratedDeflation hT n
    ⟨deflateTiling previous.property, deflateTiling_legal previous.property⟩

theorem iteratedDeflation_legal {T : GridTiling} (hT : LegalTiling T) (n : Nat) :
    LegalTiling (iteratedDeflation hT n).val :=
  (iteratedDeflation hT n).property

theorem iteratedDeflation_step {T : GridTiling} (hT : LegalTiling T) (n : Nat) :
    ∃ origin : V3,
      (∀ c, groupCenters (iteratedDeflation hT n).val c → SameParity origin c.shift) ∧
      (iteratedDeflation hT (n + 1)).val =
        deflated (groupCenters (iteratedDeflation hT n).val) origin := by
  refine ⟨deflationOrigin (iteratedDeflation hT n).property,
    (Classical.choose_spec (iteratedDeflation hT n).property.grouping_deflation).1, rfl⟩

end Chair

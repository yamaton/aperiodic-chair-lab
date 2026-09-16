import Chair.Grouping

namespace Chair

/-- Coverage, unique cube ownership and interface matching for an arbitrary
fixed discrete solid. Used for the assembled macro tiling. -/
structure LegalSolidTiling (s : Solid) (T : GridTiling) : Prop where
  cover : ∀ q, ∃ g, T g ∧ q ∈ (g.solid s).cells
  unique_owner : ∀ {g h q}, T g → T h →
    q ∈ (g.solid s).cells → q ∈ (h.solid s).cells → g = h
  compatible : ∀ {g h}, T g → T h → g ≠ h →
    interfacesFit (g.solid s) (h.solid s) zero = true

def groupCenters (T : GridTiling) : GridTiling :=
  fun c => T c ∧ ChairGrouping.Center T c

theorem legalFine_iff (T : GridTiling) : LegalSolidTiling fine T ↔ LegalTiling T := by
  constructor
  · intro h
    exact ⟨h.cover, h.unique_owner, h.compatible⟩
  · intro h
    exact ⟨h.cover, h.unique_owner, h.compatible⟩

end Chair

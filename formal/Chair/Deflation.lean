import Chair.Scaling
import Chair.SolidContacts
import Chair.MacroBoundary

namespace Chair

/-- The coarse placement belongs precisely when its inflated macro does. -/
def deflated (T : GridTiling) (origin : V3) : GridTiling :=
  fun g => T (inflate origin g)

/-- Contact recurrence applies to the exact relative motion of two aligned
macro placements; their coarse copies retain the same decorated frames. -/
theorem contact_deflate (o : V3) (g h : GridMotion)
    (hc : Contact ((inflate o g).solid macroSolid) ((inflate o h).solid macroSolid) zero) :
    Contact (g.solid fine) (h.solid fine) zero := by
  obtain ⟨r, hr⟩ := (g.inv.comp h).frame.exists_rotation
  have hr' : rotation r = ((inflate o g).inv.comp (inflate o h)).frame.mat := hr
  have hm := (contact_normalized_as macroSolid (inflate o g) (inflate o h) r hr').mp hc
  change macroContact r _ at hm
  obtain ⟨s, hs, hf⟩ := (macro_contact_recurrence r _).mp hm
  rw [inflate_relative_shift] at hs
  have heq := V3.double_injective hs
  apply (contact_normalized_as fine g h r hr).mpr
  exact heq.symm ▸ hf

/-- Coverage and compatibility survive halving an aligned macro tiling.
The alignment premise is later derived from coverage and recurrence. -/
theorem LegalSolidTiling.deflate {T : GridTiling}
    (hT : LegalSolidTiling macroSolid T) (o : V3)
    (haligned : ∀ g, T g → ∃ k : V3, g.shift = o.add (k.scale 2)) :
    LegalTiling (deflated T o) := by
  constructor
  · intro q
    obtain ⟨p, hp, hq⟩ := hT.cover (o.add (q.scale 2))
    obtain ⟨k, hk⟩ := haligned p hp
    let g : GridMotion := ⟨k, p.frame⟩
    have heq : inflate o g = p := GridMotion.ext hk.symm rfl
    refine ⟨g, ?_, ?_⟩
    · change T (inflate o g)
      exact heq.symm ▸ hp
    · change q ∈ (g.solid fine).cells
      apply (sample_owned_iff o g q).mp
      exact heq.symm ▸ hq
  · intro g h q hg hh hq hq'
    apply inflate_injective o
    exact hT.unique_owner hg hh ((sample_owned_iff o g q).mpr hq)
      ((sample_owned_iff o h q).mpr hq')
  · intro g h hg hh hne
    apply (interfacesFit_eq_true_iff _ _ _).mpr
    intro f hf f' hf' ho
    obtain ⟨hn, q, hq, hnext⟩ := opposed_owned_cubes
      (placed_fine_boundary g) (placed_fine_boundary h) hf hf' ho
    obtain ⟨b, hb, b', hb', hadj⟩ := block_adjacency o q f.normal hn
    have hmacroq : blockCell o q b ∈ ((inflate o g).solid macroSolid).cells :=
      (placed_macro_support o g _).mpr ⟨q, hq, b, hb, rfl⟩
    have hmacroq' : (blockCell o q b).add f.normal ∈
        ((inflate o h).solid macroSolid).cells := by
      rw [hadj]
      exact (placed_macro_support o h _).mpr ⟨q.add f.normal, hnext, b', hb', rfl⟩
    have hcontact := hT.contact_of_adjacent hg hh
      (fun heq => hne (inflate_injective o heq))
      (placed_macro_boundary _) (placed_macro_boundary _) hn hmacroq hmacroq'
    exact (contact_deflate o g h hcontact).2.2 f hf f' hf' ho

end Chair

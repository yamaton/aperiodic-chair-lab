import Chair.Neighborhood
import Chair.GroupingData
import Chair.LocalRules

namespace Chair.Occurrences

open GroupingData

def occurs (T : GridTiling) (g : GridMotion) (i : ContactId) : Prop :=
  T (g.comp (contactMotion i))

theorem catalogue_complete (h : GridMotion) (hc : Contact fine (placed h) zero) :
    ∃ i : ContactId, contactMotion i = h := by
  obtain ⟨r, hr, hn⟩ := contact_normalized fine GridMotion.identity h
  simp only [show GridMotion.identity.inv = GridMotion.identity from rfl,
    GridMotion.identity_comp, GridMotion.solid_identity] at hr hn
  have hn' : fineContact r h.shift := by
    apply hn.mp
    simpa only [placed, GridMotion.solid_identity] using hc
  obtain ⟨i, hs, hm⟩ := accepted_motion r h.shift ((fineContact_iff_accepted r _).mp hn')
  refine ⟨i, GridMotion.ext hs (Frame.ext ?_)⟩
  exact hm.trans hr

theorem normalized_valid {T : GridTiling} (hT : LegalTiling T)
    (hidentity : T GridMotion.identity) :
    LocalRules.Valid faceOptions incompatible (fun i => T (contactMotion i)) := by
  constructor
  · intro f
    obtain ⟨i, hi, hcover⟩ := hT.catalogue_covers hidentity contactMotion contactFace covers
      catalogue_complete contactFace_mem covers_iff f
    exact ⟨i, List.contains_iff_mem.mp hcover, hi⟩
  · intro i j hbad hi hj
    have hne : i ≠ j := by
      intro heq
      subst j
      rw [incompatible_self] at hbad
      contradiction
    have hmotions : contactMotion i ≠ contactMotion j :=
      fun heq => hne (contactMotion_injective i j heq)
    obtain ⟨w, hw⟩ := incompatible_checked i j hbad
    rcases hT.pair_allowed hi hj with heq | ⟨hd, hf⟩
    · exact hmotions heq
    · exact rejectCheck_incompatible hw hd hf

/-- Finite local propagation is valid around every actual tile of every
legal tiling, with the original frozen-port contact semantics. -/
theorem valid_occurrences {T : GridTiling} (hT : LegalTiling T)
    {g : GridMotion} (hg : T g) :
    LocalRules.Valid faceOptions incompatible (occurs T g) := by
  have h := normalized_valid (hT.normalize g) (normalizeTiling_identity hg)
  change LocalRules.Valid faceOptions incompatible (fun i => T (g.comp (contactMotion i)))
  simpa only [normalizeTiling_mem] using h

end Chair.Occurrences

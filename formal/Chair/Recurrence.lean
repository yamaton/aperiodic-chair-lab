import Chair.Checked
import Chair.Integrity

namespace Chair

set_option maxHeartbeats 0
set_option maxRecDepth 100000

theorem fineContact_iff_accepted (r : Fin 24) (t : V3) :
    fineContact r t ↔ t ∈ fineAccepted r :=
  certificate_contact_iff_mem _ _ _ _ (fine_certificates r) t

theorem macroContact_iff_accepted (r : Fin 24) (t : V3) :
    macroContact r t ↔ t ∈ macroAccepted r :=
  certificate_contact_iff_mem _ _ _ _ (macro_certificates r) t

/-- This final finite comparison contains just the accepted offsets. The
certificates, not an assumption about a search window, justify its scope. -/
theorem accepted_recurrence : ∀ r : Fin 24,
    ((macroAccepted r).all (fun t =>
      t == t.half.scale 2 && (fineAccepted r).contains t.half) &&
    (fineAccepted r).all (fun s => (macroAccepted r).contains (s.scale 2))) = true := by
  decide +kernel

/-- Main milestone. The first chair/group is normalized to the identity frame
at the origin; the other uses any of the 24 enumerated proper cubic frames.
The translation is an arbitrary integer vector, with no boundedness premise. -/
theorem macro_contact_recurrence (r : Fin 24) (t : V3) :
    macroContact r t ↔ ∃ s : V3, t = s.scale 2 ∧ fineContact r s := by
  have h := accepted_recurrence r
  simp only [Bool.and_eq_true, List.all_eq_true, beq_iff_eq,
    List.contains_iff_mem] at h
  constructor
  · intro ht
    obtain ⟨heven, hfine⟩ := h.1 t ((macroContact_iff_accepted r t).mp ht)
    exact ⟨t.half, heven, (fineContact_iff_accepted r t.half).mpr hfine⟩
  · rintro ⟨s, rfl, hs⟩
    exact (macroContact_iff_accepted r (s.scale 2)).mpr
      (h.2 s ((fineContact_iff_accepted r s).mp hs))

theorem macro_contact_even (r : Fin 24) (t : V3) (h : macroContact r t) :
    t.x % 2 = 0 ∧ t.y % 2 = 0 ∧ t.z % 2 = 0 := by
  obtain ⟨s, rfl, _⟩ := (macro_contact_recurrence r t).mp h
  simp [V3.scale]

theorem fine_accepted_count :
    ((List.finRange 24).map fun r => (fineAccepted r).length).sum = 44 := by
  decide +kernel

theorem macro_accepted_count :
    ((List.finRange 24).map fun r => (macroAccepted r).length).sum = 44 := by
  decide +kernel

theorem accepted_lists_distinct : ∀ r : Fin 24,
    (fineAccepted r).Nodup ∧ (macroAccepted r).Nodup := by
  decide +kernel

#print axioms macro_contact_recurrence
#print axioms macro_contact_even
#print axioms fine_accepted_count
#print axioms macro_accepted_count

end Chair

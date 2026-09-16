import Chair.Model

namespace Chair

/-- A local, indexed reason that an integral translation is not a contact. -/
inductive RejectWitness where
  | overlap (i j : Nat)
  | mismatch (i j : Nat)
  deriving Repr

/-- Out-of-bounds indices fail the check. A mismatch must be on opposed faces. -/
def rejectCheck (s u : Solid) (t : V3) : RejectWitness → Bool
  | .overlap i j =>
    match s.cells[i]?, u.cells[j]? with
    | some a, some b => decide (a = b.add t)
    | _, _ => false
  | .mismatch i j =>
    match s.faces[i]?, u.faces[j]? with
    | some a, some b => opposed a b t && !(faceFits a b t)
    | _, _ => false

theorem rejectCheck_sound {s u : Solid} {t : V3} {w : RejectWitness}
    (h : rejectCheck s u t w = true) : ¬Contact s u t := by
  intro hc
  cases w with
  | overlap i j =>
    simp only [rejectCheck] at h
    split at h
    next a b ha hb =>
      exact hc.1 a (List.mem_of_getElem? ha) b (List.mem_of_getElem? hb)
        (of_decide_eq_true h)
    next => contradiction
  | mismatch i j =>
    simp only [rejectCheck] at h
    split at h
    next a b ha hb =>
      have hm := hc.2.2 a (List.mem_of_getElem? ha) b (List.mem_of_getElem? hb)
      simp only [Bool.and_eq_true, opposed_eq_true, Bool.not_eq_true'] at h
      have hf := (faceFits_eq_true a b t).mpr (hm h.1)
      rw [hf] at h
      exact Bool.noConfusion h.2
    next => contradiction

/-- Enumerate only offsets with an actual opposed face pair. Offsets arise
from face centers, so no arbitrary search radius is assumed. -/
def touchingCandidates (s u : Solid) : List V3 :=
  s.faces.flatMap fun a => u.faces.flatMap fun b =>
    let t := (a.center2.sub b.center2).half
    if opposed a b t then [t] else []

theorem contact_mem_touchingCandidates {s u : Solid} {t : V3}
    (h : Contact s u t) : t ∈ touchingCandidates s u := by
  obtain ⟨a, ha, b, hb, hop⟩ := h.2.1
  have ht : (a.center2.sub b.center2).half = t :=
    V3.half_sub_of_eq_add_double hop.1
  apply List.mem_flatMap.mpr
  refine ⟨a, ha, List.mem_flatMap.mpr ⟨b, hb, ?_⟩⟩
  simp [ht, (opposed_eq_true a b t).mpr hop]

/-- Check positive offsets in full, negative offsets using local witnesses,
and coverage of every touching offset. Duplicate rows are harmless. -/
def certificateCheck (s u : Solid) (accepted : List V3)
    (rejected : List (V3 × RejectWitness)) : Bool :=
  accepted.all (contact s u) &&
  rejected.all (fun row => rejectCheck s u row.1 row.2) &&
  (touchingCandidates s u).eraseDups.all
    (fun t => (accepted ++ rejected.map Prod.fst).contains t)

/-- A successful certificate gives the entire contact language on the
infinite integral grid, not just contacts within a preselected finite box. -/
theorem certificate_contact_iff_mem (s u : Solid) (accepted : List V3)
    (rejected : List (V3 × RejectWitness))
    (h : certificateCheck s u accepted rejected = true) (t : V3) :
    Contact s u t ↔ t ∈ accepted := by
  simp only [certificateCheck, Bool.and_eq_true, List.all_eq_true,
    List.contains_iff_mem] at h
  constructor
  · intro hc
    have hm := h.2 t (List.mem_eraseDups.mpr (contact_mem_touchingCandidates hc))
    rcases List.mem_append.mp hm with ha | hr
    · exact ha
    · obtain ⟨row, hrow, heq⟩ := List.mem_map.mp hr
      have hn := rejectCheck_sound (h.1.2 row hrow)
      exact False.elim (hn (heq ▸ hc))
  · intro ht
    exact (contact_eq_true_iff s u t).mp (h.1.1 t ht)

end Chair

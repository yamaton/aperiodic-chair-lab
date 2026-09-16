import Chair.SolidTiling

namespace Chair

theorem LegalSolidTiling.contact_of_touching {s : Solid} {T : GridTiling}
    (hT : LegalSolidTiling s T) {g h : GridMotion}
    (hg : T g) (hh : T h) (hne : g ≠ h)
    (ht : ∃ f ∈ (g.solid s).faces, ∃ f' ∈ (h.solid s).faces, Opposed f f' zero) :
    Contact (g.solid s) (h.solid s) zero := by
  refine ⟨?_, ht, (interfacesFit_eq_true_iff _ _ _).mp (hT.compatible hg hh hne)⟩
  intro a ha b hb heq
  have hab : a = b := by simpa [zero, V3.add] using heq
  exact hne (hT.unique_owner hg hh ha (hab.symm ▸ hb))

/-- Adjacent cubes owned by different tiles supply an actual contact. -/
theorem LegalSolidTiling.contact_of_adjacent {s : Solid} {T : GridTiling}
    (hT : LegalSolidTiling s T) {g h : GridMotion}
    (hg : T g) (hh : T h) (hne : g ≠ h)
    (bg : BoundaryCorrect (g.solid s)) (bh : BoundaryCorrect (h.solid s))
    {q n : V3} (hn : n ∈ normals)
    (hq : q ∈ (g.solid s).cells) (hnext : q.add n ∈ (h.solid s).cells) :
    Contact (g.solid s) (h.solid s) zero := by
  have hout : q.add n ∉ (g.solid s).cells :=
    fun hi => hne (hT.unique_owner hg hh hi hnext)
  have hprev : q ∉ (h.solid s).cells :=
    fun hi => hne (hT.unique_owner hg hh hq hi)
  have hout' : (q.add n).add (n.scale (-1)) ∉ (h.solid s).cells := by
    simpa only [V3.add_assoc, V3.add_neg, V3.add_zero] using hprev
  obtain ⟨f, hf, hc, hfn⟩ := bg.2 q hq n hn hout
  obtain ⟨f', hf', hc', hfn'⟩ := bh.2 _ hnext _ (normal_neg_mem n hn) hout'
  apply hT.contact_of_touching hg hh hne
  refine ⟨f, hf, f', hf', ?_, ?_⟩
  · rw [hc, hc', faceCenter2_opposite]
    simp [zero, V3.scale, V3.add]
  · rw [hfn, hfn']
    simp only [V3.scale_scale]
    exact (V3.scale_one n).symm

private theorem face_centers_adjacent (q u n m : V3)
    (hc : faceCenter2 q n = faceCenter2 u m) (hn : n = m.scale (-1)) :
    u = q.add n := by
  cases q; cases u; cases n; cases m
  simp only [faceCenter2, V3.add, V3.scale, V3.mk.injEq] at hc hn ⊢
  omega

/-- Opposed exposed faces have occupied cubes on the two adjacent sides. -/
theorem opposed_owned_cubes {s u : Solid} (bs : BoundaryCorrect s)
    (bu : BoundaryCorrect u) {f f' : Face} (hf : f ∈ s.faces)
    (hf' : f' ∈ u.faces) (ho : Opposed f f' zero) :
    f.normal ∈ normals ∧ ∃ q ∈ s.cells, q.add f.normal ∈ u.cells := by
  obtain ⟨hn, q, hq, hc, _⟩ := bs.1 f hf
  obtain ⟨_, p, hp, hc', _⟩ := bu.1 f' hf'
  have hcenter : faceCenter2 q f.normal = faceCenter2 p f'.normal := by
    simpa only [← hc, ← hc', zero, V3.scale, V3.add, Int.mul_zero, Int.add_zero] using ho.1
  have hpq := face_centers_adjacent q p f.normal f'.normal hcenter ho.2
  exact ⟨hn, q, hq, hpq ▸ hp⟩

theorem contact_normalized_as (s : Solid) (g h : GridMotion) (r : Fin 24)
    (hr : rotation r = (g.inv.comp h).frame.mat) :
    Contact (g.solid s) (h.solid s) zero ↔
      Contact s (moveSolid ⟨zero, rotation r⟩ s) (g.inv.comp h).shift := by
  rw [zero, GridMotion.contact_relative, GridMotion.solid_eq_moveSolid,
    GridMotion.toPlacement, ← hr, contact_moveSolid_shift]

theorem V3.double_injective {a b : V3} (h : a.scale 2 = b.scale 2) : a = b := by
  cases a; cases b
  simp only [V3.scale, V3.mk.injEq] at h ⊢
  omega

end Chair

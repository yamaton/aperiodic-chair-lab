import Chair.Boundary

namespace Chair

set_option maxHeartbeats 0
set_option maxRecDepth 100000

/-- Actual listed macro faces, in every cubic orientation, are exactly the exposed boundary. -/
theorem rotated_macro_boundary :
    ∀ r ∈ rotations, BoundaryCorrect (moveSolid ⟨zero, r⟩ macroSolid) := by
  simp only [macro_eq_cached, BoundaryCorrect]
  decide +kernel

private def translateFace (t : V3) (f : Face) : Face :=
  ⟨f.center2.add (t.scale 2), f.normal,
   f.ports.map fun p => ⟨p.pos16.add (t.scale 16), p.key, p.u, p.v⟩⟩

private def translateSolid (t : V3) (s : Solid) : Solid :=
  ⟨s.cells.map (fun q => q.add t), s.faces.map (translateFace t)⟩

private theorem add_cancel (a b t : V3) : a.add t = b.add t ↔ a = b := by
  cases a; cases b; cases t
  simp only [V3.add, V3.mk.injEq]
  omega

private theorem add_swap (q t n : V3) : (q.add t).add n = (q.add n).add t := by
  cases q; cases t; cases n
  simp only [V3.add, V3.mk.injEq]
  omega

private theorem faceCenter2_translate (q n t : V3) :
    (faceCenter2 q n).add (t.scale 2) = faceCenter2 (q.add t) n := by
  cases q; cases n; cases t
  simp only [faceCenter2, V3.add, V3.scale, V3.mk.injEq]
  omega

private theorem mem_translated_cells (q t : V3) (s : Solid) :
    q.add t ∈ (translateSolid t s).cells ↔ q ∈ s.cells := by
  simp only [translateSolid, List.mem_map]
  constructor
  · rintro ⟨a, ha, heq⟩
    exact (add_cancel a q t).mp heq ▸ ha
  · intro hq
    exact ⟨q, hq, rfl⟩

private theorem translate_boundary (s : Solid) (t : V3) (h : BoundaryCorrect s) :
    BoundaryCorrect (translateSolid t s) := by
  constructor
  · intro f hf
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hf
    obtain ⟨hn, q, hq, hc, hout⟩ := h.1 a ha
    refine ⟨hn, q.add t, (mem_translated_cells q t s).mpr hq, ?_, ?_⟩
    · change a.center2.add (t.scale 2) = faceCenter2 (q.add t) a.normal
      rw [hc, faceCenter2_translate]
    · change (q.add t).add a.normal ∉ (translateSolid t s).cells
      rw [add_swap, mem_translated_cells]
      exact hout
  · intro q hq n hn hout
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hq
    have hout' : a.add n ∉ s.cells := by
      intro hi
      apply hout
      rw [add_swap]
      exact (mem_translated_cells (a.add n) t s).mpr hi
    obtain ⟨f, hf, hc, hfn⟩ := h.2 a ha n hn hout'
    refine ⟨translateFace t f, List.mem_map.mpr ⟨f, hf, rfl⟩, ?_, hfn⟩
    change f.center2.add (t.scale 2) = faceCenter2 (a.add t) n
    rw [hc, faceCenter2_translate]

private theorem translated_moveSolid (s : Solid) (t : V3) (r : Mat) :
    translateSolid t (moveSolid ⟨zero, r⟩ s) = moveSolid ⟨t, r⟩ s := by
  simp [translateSolid, translateFace, moveSolid, List.map_map, Function.comp_def,
    zero, V3.add, V3.scale]

/-- Every integral translate in every listed proper orientation has exactly
its occupancy boundary, with the complete frozen face records retained. -/
theorem move_macro_boundary (t : V3) (r : Mat) (hr : r ∈ rotations) :
    BoundaryCorrect (moveSolid ⟨t, r⟩ macroSolid) := by
  rw [← translated_moveSolid macroSolid t r]
  exact translate_boundary _ t (rotated_macro_boundary r hr)

/-- Boundary ownership is a theorem of the frozen geometry for every
proper grid placement. -/
theorem placed_macro_boundary (g : GridMotion) : BoundaryCorrect (g.solid macroSolid) := by
  rw [GridMotion.solid_eq_moveSolid]
  exact move_macro_boundary g.shift g.frame.mat g.frame.proper

end Chair

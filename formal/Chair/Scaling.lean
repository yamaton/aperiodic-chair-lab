import Chair.SolidTiling

namespace Chair

/-- Inflate the placement translation around a chosen common parity origin. -/
def inflate (origin : V3) (g : GridMotion) : GridMotion :=
  ⟨origin.add (g.shift.scale 2), g.frame⟩

def blockCell (origin q b : V3) : V3 := origin.add ((q.scale 2).add b)

def doubledCells (qs : List V3) : List V3 :=
  qs.flatMap fun q => binaryCorners.map fun b => (q.scale 2).add b

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
private theorem oriented_support : ∀ r : Fin 24,
    (∀ q ∈ (orientedMacro r).cells, q ∈ doubledCells (orientedFine r).cells) ∧
    (∀ q ∈ doubledCells (orientedFine r).cells, q ∈ (orientedMacro r).cells) := by
  decide +kernel

theorem inflate_injective (o : V3) {g h : GridMotion} (heq : inflate o g = inflate o h) :
    g = h := by
  have hs := congrArg GridMotion.shift heq
  have hf := congrArg GridMotion.frame heq
  apply GridMotion.ext
  · apply V3.ext
    all_goals simp only [inflate, V3.add, V3.scale, V3.mk.injEq] at hs
    all_goals omega
  · exact hf

private theorem cells_by_shift (s : Solid) (g : GridMotion) :
    (g.solid s).cells = (s.cells.map g.frame.mat.cube).map (fun q => q.add g.shift) := by
  simp [GridMotion.solid, GridMotion.cell, List.map_map]

private theorem frame_support (r : Frame) :
    ∀ q, q ∈ macroSolid.cells.map r.mat.cube ↔
      q ∈ doubledCells (fine.cells.map r.mat.cube) := by
  obtain ⟨i, hi⟩ := r.exists_rotation
  have h := oriented_support i
  simp only [orientedMacro, orientedFine, moveSolid, zero, V3.add, Int.add_zero] at h
  rw [hi] at h
  intro q
  exact ⟨h.1 q, h.2 q⟩

theorem placed_macro_support (o : V3) (g : GridMotion) (q : V3) :
    q ∈ ((inflate o g).solid macroSolid).cells ↔
      ∃ a ∈ (g.solid fine).cells, ∃ b ∈ binaryCorners, q = blockCell o a b := by
  rw [cells_by_shift, List.mem_map]
  constructor
  · rintro ⟨c, hc, rfl⟩
    have hc' := (frame_support g.frame c).mp hc
    obtain ⟨a, ha, hmem⟩ := List.mem_flatMap.mp hc'
    obtain ⟨b, hb, heq⟩ := List.mem_map.mp hmem
    refine ⟨a.add g.shift, ?_, b, hb, ?_⟩
    · rw [cells_by_shift]
      exact List.mem_map.mpr ⟨a, ha, rfl⟩
    · rw [← heq]
      apply V3.ext <;> simp [inflate, blockCell, V3.add, V3.scale] <;> omega
  · rintro ⟨a, ha, b, hb, rfl⟩
    rw [cells_by_shift] at ha
    obtain ⟨c, hc, rfl⟩ := List.mem_map.mp ha
    refine ⟨(c.scale 2).add b, (frame_support g.frame _).mpr ?_, ?_⟩
    · exact List.mem_flatMap.mpr ⟨c, hc, List.mem_map.mpr ⟨b, hb, rfl⟩⟩
    · apply V3.ext <;> simp [inflate, blockCell, V3.add, V3.scale] <;> omega

theorem binary_corner_bounds {b : V3} (hb : b ∈ binaryCorners) :
    0 ≤ b.x ∧ b.x ≤ 1 ∧ 0 ≤ b.y ∧ b.y ≤ 1 ∧ 0 ≤ b.z ∧ b.z ≤ 1 := by
  have h : ∀ b ∈ binaryCorners,
      0 ≤ b.x ∧ b.x ≤ 1 ∧ 0 ≤ b.y ∧ b.y ≤ 1 ∧ 0 ≤ b.z ∧ b.z ≤ 1 := by
    decide +kernel
  exact h b hb

theorem blockCell_unique {o q p b c : V3} (hb : b ∈ binaryCorners)
    (hc : c ∈ binaryCorners) (heq : blockCell o q b = blockCell o p c) : q = p := by
  have hbb := binary_corner_bounds hb
  have hcc := binary_corner_bounds hc
  simp only [blockCell, V3.add, V3.scale, V3.mk.injEq] at heq
  apply V3.ext <;> omega

theorem sample_owned_iff (o : V3) (h : GridMotion) (q : V3) :
    o.add (q.scale 2) ∈ ((inflate o h).solid macroSolid).cells ↔
      q ∈ (h.solid fine).cells := by
  rw [placed_macro_support]
  have hz : V3.zero ∈ binaryCorners := by decide +kernel
  constructor
  · rintro ⟨p, hp, b, hb, heq⟩
    have hpq : q = p := blockCell_unique (o := o) hz hb (by simpa [blockCell] using heq)
    exact hpq ▸ hp
  · intro hq
    exact ⟨q, hq, V3.zero, hz, by simp [blockCell]⟩

theorem block_adjacency (o q n : V3) (hn : n ∈ normals) :
    ∃ b ∈ binaryCorners, ∃ b' ∈ binaryCorners,
      (blockCell o q b).add n = blockCell o (q.add n) b' := by
  have h : ∀ n ∈ normals, ∃ b ∈ binaryCorners, ∃ b' ∈ binaryCorners,
      b.add n = (n.scale 2).add b' := by decide +kernel
  obtain ⟨b, hb, c, hc, heq⟩ := h n hn
  refine ⟨b, hb, c, hc, ?_⟩
  simp only [V3.add, V3.scale, V3.mk.injEq] at heq
  apply V3.ext <;> simp [blockCell, V3.add, V3.scale] <;> omega

theorem inflate_relative_shift (o : V3) (g h : GridMotion) :
    ((inflate o g).inv.comp (inflate o h)).shift =
      ((g.inv.comp h).shift).scale 2 := by
  simp only [GridMotion.comp, GridMotion.inv, inflate, Frame.apply_add,
    Frame.apply_scale, V3.scale_add, V3.scale_scale]
  apply V3.ext <;> simp [V3.add, V3.scale] <;> omega

theorem inflate_relative_frame (o : V3) (g h : GridMotion) :
    ((inflate o g).inv.comp (inflate o h)).frame = (g.inv.comp h).frame := rfl

end Chair

import Chair.SolidTiling

namespace Chair

open GroupingData ChairGrouping

/-- The frozen children and the intrinsic group have exactly the same placements. -/
theorem frozen_child_iff (p : Placement) :
    p ∈ Input.children ↔ ∃ d ∈ group, d.toPlacement = p := by
  rw [← group_matches_frozen.mem_iff]
  exact List.mem_map

/-- The macro support is the union of its eight fine children. -/
theorem macro_cell_iff (q : V3) :
    q ∈ macroSolid.cells ↔ ∃ d ∈ group, q ∈ (d.solid fine).cells := by
  change q ∈ Input.children.flatMap (fun p => (childSolid p).cells) ↔ _
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨p, hp, hq⟩
    obtain ⟨d, hd, rfl⟩ := (frozen_child_iff p).mp hp
    exact ⟨d, hd, hq⟩
  · rintro ⟨d, hd, hq⟩
    exact ⟨d.toPlacement, (frozen_child_iff _).mpr ⟨d, hd, rfl⟩, hq⟩

/-- Every complete macro face, including all ports, is an uncancelled child face. -/
theorem macro_face_child {f : Face} (hf : f ∈ macroSolid.faces) :
    ∃ d ∈ group, f ∈ (d.solid fine).faces := by
  have hf' := (List.mem_filter.mp (macro_boundary_exact.1 f hf)).1
  obtain ⟨p, hp, hf''⟩ := List.mem_flatMap.mp hf'
  obtain ⟨d, hd, rfl⟩ := (frozen_child_iff p).mp hp
  exact ⟨d, hd, hf''⟩

/-- The union identity holds at every proper grid placement. -/
theorem placed_macro_cell_iff (c : GridMotion) (q : V3) :
    q ∈ (c.solid macroSolid).cells ↔
      ∃ d ∈ group, q ∈ ((c.comp d).solid fine).cells := by
  change q ∈ macroSolid.cells.map c.cell ↔ _
  rw [List.mem_map]
  constructor
  · rintro ⟨a, ha, rfl⟩
    obtain ⟨d, hd, ha⟩ := (macro_cell_iff a).mp ha
    refine ⟨d, hd, ?_⟩
    rw [GridMotion.solid_comp]
    exact List.mem_map.mpr ⟨a, ha, rfl⟩
  · rintro ⟨d, hd, hq⟩
    rw [GridMotion.solid_comp] at hq
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hq
    exact ⟨a, (macro_cell_iff a).mpr ⟨d, hd, ha⟩, rfl⟩

theorem placed_macro_face_child (c : GridMotion) {f : Face}
    (hf : f ∈ (c.solid macroSolid).faces) :
    ∃ d ∈ group, f ∈ ((c.comp d).solid fine).faces := by
  obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hf
  obtain ⟨d, hd, ha⟩ := macro_face_child ha
  refine ⟨d, hd, ?_⟩
  rw [GridMotion.solid_comp]
  exact List.mem_map.mpr ⟨a, ha, rfl⟩

/-- Two recognized groups containing the same fine placement have equal centers. -/
theorem group_centers_eq_of_shared_child {T : GridTiling} (hT : LegalTiling T)
    {c e d k : GridMotion} (hc : groupCenters T c) (he : groupCenters T e)
    (hd : d ∈ group) (hk : k ∈ group) (heq : c.comp d = e.comp k) : c = e := by
  have hq := (center_iff_group_occurs hT hc.1).mp hc.2 d hd
  have hcm : Member c (c.comp d) :=
    (member_iff_in_group _ _).mpr (List.mem_map.mpr ⟨d, hd, rfl⟩)
  have hem : Member e (c.comp d) :=
    (member_iff_in_group _ _).mpr (List.mem_map.mpr ⟨k, hk, heq.symm⟩)
  have hpc := child_selects_center hT ⟨c, hc.1⟩ ⟨c.comp d, hq⟩ hc.2 hcm
  have hpe := child_selects_center hT ⟨e, he.1⟩ ⟨c.comp d, hq⟩ he.2 hem
  exact congrArg Subtype.val (hpc.symm.trans hpe)

/-- Universal grouping assembles an arbitrary legal fine tiling into a legal
macro tiling. Its hypotheses contain neither parity nor a parent tiling. -/
theorem LegalTiling.assemble {T : GridTiling} (hT : LegalTiling T) :
    LegalSolidTiling macroSolid (groupCenters T) := by
  constructor
  · intro q
    obtain ⟨g, hg, hq⟩ := hT.cover q
    obtain ⟨c, ⟨hc, hm⟩, _⟩ := universal_grouping hT ⟨g, hg⟩
    obtain ⟨d, hd, heq⟩ := List.mem_map.mp ((member_iff_in_group _ _).mp hm)
    exact ⟨c.val, ⟨c.property, hc⟩,
      (placed_macro_cell_iff c.val q).mpr ⟨d, hd, heq.symm ▸ hq⟩⟩
  · intro c e q hc he hqc hqe
    obtain ⟨d, hd, hqd⟩ := (placed_macro_cell_iff c q).mp hqc
    obtain ⟨k, hk, hqk⟩ := (placed_macro_cell_iff e q).mp hqe
    have htd := (center_iff_group_occurs hT hc.1).mp hc.2 d hd
    have htk := (center_iff_group_occurs hT he.1).mp he.2 k hk
    exact group_centers_eq_of_shared_child hT hc he hd hk
      (hT.unique_owner htd htk hqd hqk)
  · intro c e hc he hne
    apply (interfacesFit_eq_true_iff _ _ _).mpr
    intro f hf f' hf' ho
    obtain ⟨d, hd, hfd⟩ := placed_macro_face_child c hf
    obtain ⟨k, hk, hfk⟩ := placed_macro_face_child e hf'
    have htd := (center_iff_group_occurs hT hc.1).mp hc.2 d hd
    have htk := (center_iff_group_occurs hT he.1).mp he.2 k hk
    have hchild_ne : c.comp d ≠ e.comp k := fun heq =>
      hne (group_centers_eq_of_shared_child hT hc he hd hk heq)
    exact (interfacesFit_eq_true_iff _ _ _).mp
      (hT.compatible htd htk hchild_ne) f hfd f' hfk ho

end Chair

import Chair.Occurrences
import Chair.LocalGrouping
import Chair.Partition

namespace Chair.ChairGrouping

open GroupingData Occurrences

/-- An actual trigger among the six specified oriented neighbors. -/
def Center (T : GridTiling) (g : GridMotion) : Prop :=
  LocalGrouping.HasTrigger (occurs T g)

/-- The specified eight-child pattern, with its center retained as a
distinguished actual tile. No tiling or occurrence is built into this relation. -/
def Member (c q : GridMotion) : Prop :=
  q = c ∨ ∃ i ∈ outer, q = c.comp (contactMotion i)

private theorem trigger_outer : ∀ i ∈ triggers, i ∈ outer := by decide +kernel
private theorem outer_central : ∀ i ∈ outer, i ∈ central := by decide +kernel
private theorem notch_central : ∀ i ∈ notch, i ∈ central → i = 37 := by decide +kernel
private theorem axial_not_central : (39 : ContactId) ∉ central := by decide +kernel

variable {T : GridTiling} (hT : LegalTiling T)

include hT in
theorem center_children {c : GridMotion} (hc : T c) (hcenter : Center T c) :
    ∀ i ∈ outer, T (c.comp (contactMotion i)) := by
  obtain ⟨j, hj, hp⟩ := hcenter
  intro i hi
  exact LocalGrouping.trigger_forces_central (valid_occurrences hT hc) hj hp i
    (outer_central i hi)

theorem reciprocal_occurs {g : GridMotion} (hg : T g) {i j : ContactId}
    (hinv : (contactMotion i).inv = contactMotion j) :
    occurs T (g.comp (contactMotion i)) j := by
  unfold occurs
  rw [← hinv, GridMotion.comp_assoc, GridMotion.comp_inv, GridMotion.comp_identity]
  exact hg

include hT in
theorem notch_center {g : GridMotion} (hg : T g) (hnoc : ¬ Center T g)
    {i : ContactId} (hi : i ∈ notch) (hp : occurs T g i) :
    Center T (g.comp (contactMotion i)) := by
  by_cases heq : i = 37
  · subst i
    have ha := LocalGrouping.exceptional_axial (valid_occurrences hT hg) hp hnoc
    refine ⟨28, by decide +kernel, ?_⟩
    unfold occurs at ha ⊢
    have heq : (contactMotion 37).comp (contactMotion 28) = contactMotion 39 := by
      rw [← exceptional_relative, ← GridMotion.comp_assoc, GridMotion.comp_inv,
        GridMotion.identity_comp]
    simpa only [GridMotion.comp_assoc, heq] using ha
  · obtain ⟨j, hj, hinv⟩ := ordinary_notch_inverse_trigger i hi heq
    exact ⟨j, hj, reciprocal_occurs hg hinv⟩

theorem notch_member {g : GridMotion} {i : ContactId} (hi : i ∈ notch) :
    Member (g.comp (contactMotion i)) g := by
  by_cases heq : i = 37
  · subst i
    refine Or.inr ⟨4, by decide +kernel, ?_⟩
    rw [← same_notch_inverse, GridMotion.comp_assoc, GridMotion.comp_inv,
      GridMotion.comp_identity]
  · obtain ⟨j, hj, hinv⟩ := ordinary_notch_inverse_trigger i hi heq
    refine Or.inr ⟨j, trigger_outer j hj, ?_⟩
    rw [← hinv, GridMotion.comp_assoc, GridMotion.comp_inv, GridMotion.comp_identity]

include hT in
/-- An outer child of an actual center cannot itself have a trigger. -/
theorem outer_not_center {c : GridMotion} (hc : T c) (hcenter : Center T c)
    {i : ContactId} (hi : i ∈ outer) :
    ¬ Center T (c.comp (contactMotion i)) := by
  intro hchild
  have hq := center_children hT hc hcenter i hi
  have hvalid := valid_occurrences hT hq
  by_cases heq : i = 4
  · subst i
    have hs := center_children hT hc hcenter 28 (by decide +kernel)
    have haxial : occurs T (c.comp (contactMotion 4)) 39 := by
      unfold occurs
      have heq : (contactMotion 4).comp (contactMotion 39) = contactMotion 28 := by
        rw [← exceptional_sibling, ← GridMotion.comp_assoc, GridMotion.comp_inv,
          GridMotion.identity_comp]
      simpa only [GridMotion.comp_assoc, heq] using hs
    exact axial_not_central (LocalGrouping.central_exact hvalid hchild haxial)
  · obtain ⟨j, hj, hjne, hinv⟩ := outer_inverse_notch_nonidentity i hi heq
    have hp := reciprocal_occurs hc hinv
    exact hjne (notch_central j hj (LocalGrouping.central_exact hvalid hchild hp))

abbrev Tile (T : GridTiling) := {g : GridMotion // T g}

noncomputable def notchIndex (q : Tile T) : ContactId :=
  Classical.choose (LocalGrouping.notch_present (valid_occurrences hT q.property))

theorem notchIndex_spec (q : Tile T) :
    notchIndex hT q ∈ notch ∧ occurs T q.val (notchIndex hT q) :=
  Classical.choose_spec (LocalGrouping.notch_present (valid_occurrences hT q.property))

noncomputable def notchTile (q : Tile T) : Tile T :=
  ⟨q.val.comp (contactMotion (notchIndex hT q)), (notchIndex_spec hT q).2⟩

/-- The intrinsic rule: a triggered tile selects itself; every other tile
selects the owner of its notch. Choice is harmless because `notch_unique`
proves that the selected notch index is unique. -/
noncomputable def parent (q : Tile T) : Tile T := by
  classical
  exact if Center T q.val then q else notchTile hT q

theorem selected_center (q : Tile T) : Center T (parent hT q).val := by
  classical
  by_cases hc : Center T q.val
  · simpa only [parent, ite_eq_left hc] using hc
  · simp only [parent, ite_eq_right hc, notchTile]
    exact notch_center hT q.property hc (notchIndex_spec hT q).1
      (notchIndex_spec hT q).2

theorem selected_member (q : Tile T) : Member (parent hT q).val q.val := by
  classical
  by_cases hc : Center T q.val
  · simp only [parent, ite_eq_left hc]
    exact Or.inl rfl
  · simp only [parent, ite_eq_right hc, notchTile]
    exact notch_member (notchIndex_spec hT q).1

theorem child_selects_center (c q : Tile T) (hc : Center T c.val)
    (hm : Member c.val q.val) : parent hT q = c := by
  classical
  rcases hm with heq | ⟨i, hi, heq⟩
  · have hqc : q = c := Subtype.ext heq
    subst q
    simp only [parent, ite_eq_left hc]
  · have hn : ¬ Center T q.val := by
      rw [heq]
      exact outer_not_center hT c.property hc hi
    simp only [parent, ite_eq_right hn]
    apply Subtype.ext
    change q.val.comp (contactMotion (notchIndex hT q)) = c.val
    obtain ⟨j, hj, hinv⟩ := outer_inverse_notch i hi
    have hp : occurs T q.val j := by
      rw [heq]
      exact reciprocal_occurs c.property hinv
    have hchoice : notchIndex hT q = j :=
      LocalGrouping.notch_unique (valid_occurrences hT q.property)
        (notchIndex_spec hT q).1 hj (notchIndex_spec hT q).2 hp
    rw [hchoice, heq, ← hinv, GridMotion.comp_assoc, GridMotion.comp_inv,
      GridMotion.comp_identity]

noncomputable def recognition : Grouping.Recognition (Tile T) where
  center q := Center T q.val
  member c q := Member c.val q.val
  parent := parent hT
  self_member _ _ := Or.inl rfl
  selected_center := selected_center hT
  selected_member := selected_member hT
  child_selects_center := child_selects_center hT

/-- Every tile in an arbitrary legal tiling belongs to exactly one of the
 specified groups. The hypotheses contain no parent partition or hierarchy. -/
theorem universal_grouping (hT : LegalTiling T) (q : Tile T) :
    ∃ c : Tile T, (Center T c.val ∧ Member c.val q.val) ∧
      ∀ d : Tile T, Center T d.val ∧ Member d.val q.val → d = c :=
  (recognition hT).unique_center q

theorem parent_fiber (c q : Tile T) (hc : Center T c.val) :
    Member c.val q.val ↔ parent hT q = c :=
  (recognition hT).fiber_iff c q hc

theorem parent_map_unique (p : Tile T → Tile T)
    (hp : ∀ q, Center T (p q).val ∧ Member (p q).val q.val) :
    p = parent hT :=
  (recognition hT).parent_unique p hp

include hT in
theorem partition_unique (chosen : Tile T → Prop)
    (hvalid : ∀ c, chosen c → Center T c.val)
    (hcover : ∀ q : Tile T, ∃ c, chosen c ∧ Member c.val q.val) :
    chosen = fun c => Center T c.val :=
  (recognition hT).covering_centers_unique chosen hvalid hcover

/-- The member relation is exactly the finite frozen eight-child pattern. -/
theorem member_iff_in_group (c q : GridMotion) :
    Member c q ↔ q ∈ group.map c.comp := by
  simp only [Member, group, List.map_cons, GridMotion.comp_identity,
    List.mem_cons, List.mem_map]
  constructor
  · rintro (h | ⟨i, hi, h⟩)
    · exact Or.inl h
    · exact Or.inr ⟨contactMotion i, ⟨i, hi, rfl⟩, h.symm⟩
  · rintro (h | ⟨_, ⟨i, hi, rfl⟩, h⟩)
    · exact Or.inl h
    · exact Or.inr ⟨i, hi, h.symm⟩

theorem group_has_eight_distinct_tiles (c : GridMotion) :
    (group.map c.comp).length = 8 ∧ (group.map c.comp).Nodup := by
  constructor
  · simpa only [List.length_map] using group_length
  · apply List.pairwise_map.mpr
    exact group_nodup.imp fun hne heq => hne (c.comp_left_injective heq)

/-- An occurrence of the specified eight-child pattern automatically has
a trigger. Thus `Center` is not an extra restriction on allowed groups. -/
theorem center_iff_group_occurs (hT : LegalTiling T) {c : GridMotion} (hc : T c) :
    Center T c ↔ ∀ d ∈ group, T (c.comp d) := by
  constructor
  · intro hcenter d hd
    rcases List.mem_cons.mp hd with heq | hm
    · simpa only [heq, GridMotion.comp_identity] using hc
    · obtain ⟨i, hi, rfl⟩ := List.mem_map.mp hm
      exact center_children hT hc hcenter i hi
  · intro hgroup
    exact ⟨5, by decide +kernel,
      hgroup (contactMotion 5) (by decide +kernel)⟩

/-- Any covering of the tiling by occurrences of the frozen group gives
the same partition. There is no assumed trigger condition on that covering. -/
theorem group_partition_unique (hT : LegalTiling T) (chosen : Tile T → Prop)
    (hgroups : ∀ c, chosen c → ∀ d ∈ group, T (c.val.comp d))
    (hcover : ∀ q : Tile T, ∃ c, chosen c ∧ Member c.val q.val) :
    chosen = fun c => Center T c.val :=
  partition_unique hT chosen
    (fun c hc => (center_iff_group_occurs hT c.property).mpr (hgroups c hc)) hcover

theorem moved_mem (g p : GridMotion) : moveTiling g T (g.comp p) ↔ T p := by
  constructor
  · rintro ⟨q, hq, heq⟩
    exact g.comp_left_injective heq ▸ hq
  · intro hp
    exact ⟨p, hp, rfl⟩

theorem center_covariant (g c : GridMotion) :
    Center (moveTiling g T) (g.comp c) ↔ Center T c := by
  unfold Center LocalGrouping.HasTrigger occurs
  simp only [GridMotion.comp_assoc, moved_mem]

theorem member_covariant (g c q : GridMotion) :
    Member (g.comp c) (g.comp q) ↔ Member c q := by
  unfold Member
  constructor
  · rintro (heq | ⟨i, hi, heq⟩)
    · exact Or.inl (g.comp_left_injective heq)
    · exact Or.inr ⟨i, hi, g.comp_left_injective
        (by simpa only [GridMotion.comp_assoc] using heq)⟩
  · rintro (heq | ⟨i, hi, heq⟩)
    · exact Or.inl (congrArg g.comp heq)
    · exact Or.inr ⟨i, hi,
        by simpa only [GridMotion.comp_assoc] using congrArg g.comp heq⟩

def moveTile (g : GridMotion) (q : Tile T) : Tile (moveTiling g T) :=
  ⟨g.comp q.val, ⟨q.val, q.property, rfl⟩⟩

/-- The intrinsic parent map commutes with every proper grid motion,
including translations. This is a consequence of local recognition,
independent of which witness was selected for the notch. -/
theorem parent_covariant (g : GridMotion) (q : Tile T) :
    parent (hT.move g) (moveTile g q) = moveTile g (parent hT q) := by
  exact (recognition hT).parent_covariant (recognition (hT.move g)) (moveTile g)
    (fun c hc => (center_covariant g c.val).mpr hc)
    (fun c q _ hm => (member_covariant g c.val q.val).mpr hm) q

end Chair.ChairGrouping

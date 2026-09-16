import Std

namespace Chair.LocalRules

/-- An option occurs in the actual (possibly infinite) configuration. -/
def AllPresent {α : Type} (present : α → Prop) (items : List α) : Prop :=
  ∀ a ∈ items, present a

/-- Every option in this finite list is absent from the configuration. -/
def AllAbsent {α : Type} (present : α → Prop) (items : List α) : Prop :=
  ∀ a ∈ items, ¬ present a

/-- The finite face list is complete for the actual configuration. -/
def Covered {α : Type} (present : α → Prop) (options : List α) : Prop :=
  ∃ a ∈ options, present a

/-- A checked incompatible pair cannot occur together. No converse is needed. -/
def ConflictSound {α : Type} (present : α → Prop) (conflict : α → α → Bool) : Prop :=
  ∀ a b, conflict a b = true → present a → present b → False

/-- The only hypotheses consumed by finite local propagation. In the chair
application both follow from an unrestricted legal infinite tiling. -/
structure Valid {α β : Type} (options : β → List α)
    (conflict : α → α → Bool) (present : α → Prop) : Prop where
  covered : ∀ face, Covered present (options face)
  conflict_sound : ConflictSound present conflict

/-- A candidate blocks every possible owner of one exposed face. -/
def exclusionCheck {α : Type} (conflict : α → α → Bool)
    (options : List α) (candidate : α) : Bool :=
  options.all (conflict candidate)

theorem exclusion_sound {α : Type} {present : α → Prop}
    {conflict : α → α → Bool} (sound : ConflictSound present conflict)
    {options : List α} (covered : Covered present options) {candidate : α}
    (checked : exclusionCheck conflict options candidate = true) :
    ¬ present candidate := by
  intro occurs
  obtain ⟨other, hm, ho⟩ := covered
  have incompatible := (List.all_eq_true.mp checked) other hm
  exact sound candidate other incompatible occurs ho

/-- An option is the target, was already excluded, or conflicts with an
already present option. This is a sufficient, not necessary, forcing test. -/
def forceCheck {α : Type} [BEq α] (conflict : α → α → Bool)
    (options known excluded : List α) (target : α) : Bool :=
  options.all fun option => option == target || excluded.contains option ||
    known.any (fun k => conflict k option)

theorem force_sound {α : Type} [BEq α] [LawfulBEq α]
    {present : α → Prop} {conflict : α → α → Bool}
    (sound : ConflictSound present conflict)
    {options known excluded : List α} {target : α}
    (covered : Covered present options)
    (known_present : AllPresent present known)
    (excluded_absent : AllAbsent present excluded)
    (checked : forceCheck conflict options known excluded target = true) :
    present target := by
  obtain ⟨other, hm, ho⟩ := covered
  have h := (List.all_eq_true.mp checked) other hm
  simp only [Bool.or_eq_true, beq_iff_eq, List.contains_iff_mem,
    List.any_eq_true] at h
  rcases h with (heq | he) | ⟨k, hk, hbad⟩
  · exact heq ▸ ho
  · exact False.elim (excluded_absent other he ho)
  · exact False.elim (sound k other hbad (known_present k hk) ho)

/-- A forcing step identifies a face and its forced owner. -/
structure ForceStep (α β : Type) where
  face : β
  target : α

/-- Check a sequence in which each newly forced option becomes available
as a premise for subsequent steps. -/
def chainCheck {α β : Type} [BEq α] (options : β → List α)
    (conflict : α → α → Bool) (excluded known : List α) :
    List (ForceStep α β) → Bool
  | [] => true
  | step :: rest =>
    forceCheck conflict (options step.face) known excluded step.target &&
      chainCheck options conflict excluded (step.target :: known) rest

theorem chain_sound {α β : Type} [BEq α] [LawfulBEq α]
    {present : α → Prop} {options : β → List α}
    {conflict : α → α → Bool}
    (sound : ConflictSound present conflict)
    (covered : ∀ face, Covered present (options face))
    {excluded : List α} (excluded_absent : AllAbsent present excluded)
    (steps : List (ForceStep α β)) (known : List α)
    (known_present : AllPresent present known)
    (checked : chainCheck options conflict excluded known steps = true) :
    AllPresent present (steps.map ForceStep.target ++ known) := by
  induction steps generalizing known with
  | nil => simpa using known_present
  | cons step rest ih =>
    have checked' := checked
    simp only [chainCheck, Bool.and_eq_true] at checked'
    obtain ⟨hfirst, hrest⟩ := checked'
    have htarget := force_sound sound (covered step.face) known_present
      excluded_absent hfirst
    have hknown : AllPresent present (step.target :: known) := by
      intro a ha
      rcases List.mem_cons.mp ha with heq | hm
      · exact heq ▸ htarget
      · exact known_present a hm
    have hind := ih (step.target :: known) hknown hrest
    intro a ha
    simp only [List.map_cons, List.cons_append, List.mem_cons] at ha
    rcases ha with heq | hm
    · exact heq ▸ htarget
    · apply hind a
      rw [List.mem_append] at hm ⊢
      rcases hm with hleft | hright
      · exact Or.inl hleft
      · exact Or.inr (List.mem_cons_of_mem _ hright)

end Chair.LocalRules

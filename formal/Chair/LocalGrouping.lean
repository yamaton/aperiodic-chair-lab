import Chair.LocalRules
import Chair.GroupingData

namespace Chair.LocalGrouping

open LocalRules GroupingData

set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev Valid (present : ContactId → Prop) :=
  LocalRules.Valid faceOptions incompatible present

/-- Occurrence of any one of the six orientation-sensitive center triggers. -/
def HasTrigger (present : ContactId → Prop) : Prop :=
  ∃ i ∈ triggers, present i

/-- The fourteen impossible contacts are absent in every configuration with
complete face ownership and sound pair compatibility. -/
theorem excluded_absent {present : ContactId → Prop} (valid : Valid present) :
    AllAbsent present excluded := by
  intro i hi
  exact exclusion_sound valid.conflict_sound (valid.covered (exclusionFace i))
    (exclusion_checked i hi)

def trace (i : ContactId) : List (ForceStep ContactId FaceId) :=
  (forcingTrace i).map fun step => ⟨step.1, step.2⟩

private theorem traces_checked : ∀ i ∈ triggers,
    chainCheck faceOptions incompatible excluded [i] (trace i) = true := by
  decide +kernel

private theorem traces_complete : ∀ i ∈ triggers, ∀ j ∈ central,
    j ∈ (trace i).map ForceStep.target ++ [i] := by
  decide +kernel

/-- A trigger forces all eight neighboring placements of the central star.
The eighth is the external notch owner, not an eighth outer child. -/
theorem trigger_forces_central {present : ContactId → Prop} (valid : Valid present)
    {i : ContactId} (hi : i ∈ triggers) (occurs : present i) :
    AllPresent present central := by
  have initial : AllPresent present [i] := by
    intro j hj
    simpa using (List.mem_singleton.mp hj) ▸ occurs
  have forced := chain_sound valid.conflict_sound valid.covered
    (excluded_absent valid) (trace i) [i] initial (traces_checked i hi)
  intro j hj
  exact forced j (traces_complete i hi j hj)

private theorem central_exact_checked : ∀ i : ContactId,
    i ∈ central ∨ i ∈ excluded ∨ ∃ j ∈ central, incompatible j i = true := by
  decide +kernel

/-- The forced central star excludes every other contact ID. -/
theorem central_exact {present : ContactId → Prop} (valid : Valid present)
    (center : HasTrigger present) {i : ContactId} (occurs : present i) :
    i ∈ central := by
  obtain ⟨trigger, htrigger, hoccurs⟩ := center
  have all := trigger_forces_central valid htrigger hoccurs
  rcases central_exact_checked i with hc | he | ⟨j, hj, hbad⟩
  · exact hc
  · exact False.elim (excluded_absent valid i he occurs)
  · exact False.elim (valid.conflict_sound j i hbad (all j hj) occurs)

/-- Covering any notch face supplies one of the same seven notch owners. -/
theorem notch_present {present : ContactId → Prop} (valid : Valid present) :
    ∃ i ∈ notch, present i := by
  exact valid.covered 12

private theorem notch_unique_checked : ∀ i ∈ notch, ∀ j ∈ notch,
    i = j ∨ incompatible i j = true := by
  decide +kernel

theorem notch_unique {present : ContactId → Prop} (valid : Valid present)
    {i j : ContactId} (hi : i ∈ notch) (hj : j ∈ notch)
    (pi : present i) (pj : present j) : i = j := by
  rcases notch_unique_checked i hi j hj with heq | hbad
  · exact heq
  · exact False.elim (valid.conflict_sound i j hbad pi pj)

private theorem exceptional_checked :
    forceCheck incompatible (faceOptions 21) [37] (excluded ++ triggers) 39 = true := by
  decide +kernel

/-- If the same-oriented notch owner occurs and no central trigger occurs,
the exceptional axial contact is forced by coverage of one outer face. -/
theorem exceptional_axial {present : ContactId → Prop} (valid : Valid present)
    (notch_occurs : present 37) (noncentral : ¬ HasTrigger present) :
    present 39 := by
  apply force_sound valid.conflict_sound (valid.covered 21)
    (known := [37]) (excluded := excluded ++ triggers)
  · intro j hj
    simpa using (List.mem_singleton.mp hj) ▸ notch_occurs
  · intro j hj occurs
    rcases List.mem_append.mp hj with he | ht
    · exact excluded_absent valid j he occurs
    · exact noncentral ⟨j, ht, occurs⟩
  · exact exceptional_checked

end Chair.LocalGrouping

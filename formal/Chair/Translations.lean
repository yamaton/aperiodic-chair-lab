import Chair.Hierarchy

namespace Chair

/-- Translate a decorated placement, retaining its complete proper frame. -/
def translatePlacement (v : V3) (g : GridMotion) : GridMotion :=
  ⟨g.shift.add v, g.frame⟩

def translationMotion (v : V3) : GridMotion := ⟨v, Frame.identity⟩

/-- A genuine period of the entire placement set, in both directions. -/
def TranslationPeriod (T : GridTiling) (v : V3) : Prop :=
  ∀ g, T (translatePlacement v g) ↔ T g

theorem translatePlacement_eq_comp (v : V3) (g : GridMotion) :
    translatePlacement v g = (translationMotion v).comp g := by
  apply GridMotion.ext <;> simp [translatePlacement, translationMotion, GridMotion.comp]

@[simp] theorem translatePlacement_comp (v : V3) (g h : GridMotion) :
    (translatePlacement v g).comp h = translatePlacement v (g.comp h) := by
  simp only [translatePlacement_eq_comp, GridMotion.comp_assoc]

theorem translationPeriod_iff_moveTiling (T : GridTiling) (v : V3) :
    TranslationPeriod T v ↔ moveTiling (translationMotion v) T = T := by
  constructor
  · intro hp
    funext g
    apply propext
    constructor
    · rintro ⟨p, ht, rfl⟩
      simpa only [translatePlacement_eq_comp] using (hp p).mpr ht
    · intro ht
      let p := (translationMotion v).inv.comp g
      have heq : (translationMotion v).comp p = g := by
        simp [p, ← GridMotion.comp_assoc]
      refine ⟨p, ?_, heq.symm⟩
      apply (hp p).mp
      simpa only [translatePlacement_eq_comp, heq] using ht
  · intro heq g
    have hm := ChairGrouping.moved_mem (T := T) (translationMotion v) g
    simpa only [heq, ← translatePlacement_eq_comp] using hm

/-- Intrinsically recognized centers inherit every period. This uses only
the local trigger definition, even for placement sets that are not legal. -/
theorem TranslationPeriod.groupCenters {T : GridTiling} {v : V3}
    (hp : TranslationPeriod T v) : TranslationPeriod (groupCenters T) v := by
  intro g
  change ∀ p, T (translatePlacement v p) ↔ T p at hp
  unfold Chair.groupCenters ChairGrouping.Center LocalGrouping.HasTrigger Occurrences.occurs
  simp only [translatePlacement_comp, hp]

theorem inflate_translatePlacement (o w : V3) (g : GridMotion) :
    inflate o (translatePlacement w g) = translatePlacement (w.scale 2) (inflate o g) := by
  apply GridMotion.ext
  · simp only [inflate, translatePlacement, V3.scale_add, V3.add_assoc]
  · rfl

/-- Halving an even translation period is independent of the chosen
alignment origin and needs no extra hierarchy premise. -/
theorem TranslationPeriod.deflated {P : GridTiling} {w : V3}
    (hp : TranslationPeriod P (w.scale 2)) (o : V3) :
    TranslationPeriod (deflated P o) w := by
  intro g
  simpa only [Chair.deflated, inflate_translatePlacement] using hp (inflate o g)

end Chair

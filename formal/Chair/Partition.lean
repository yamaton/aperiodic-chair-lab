import Std

namespace Chair.Grouping

/-- The two local recognition obligations, together with the fact that a
center is a member of its own group.  In the chair application `α` is the
type of actual tiles, not the ambient space of all possible placements.

This structure does not assert that any chair geometry satisfies the
obligations: that is the separate finite-certificate and tiling argument. -/
structure Recognition (α : Type u) where
  center : α → Prop
  member : α → α → Prop
  parent : α → α
  self_member : ∀ c, center c → member c c
  selected_center : ∀ q, center (parent q)
  selected_member : ∀ q, member (parent q) q
  child_selects_center : ∀ c q, center c → member c q → parent q = c

namespace Recognition

variable {α : Type u} (R : Recognition α)

/-- The fibers of the intrinsic selector are exactly the occurring groups. -/
theorem fiber_iff (c q : α) (hc : R.center c) :
    R.member c q ↔ R.parent q = c := by
  constructor
  · exact R.child_selects_center c q hc
  · intro h
    exact h ▸ R.selected_member q

theorem parent_fixed (c : α) (hc : R.center c) : R.parent c = c :=
  R.child_selects_center c c hc (R.self_member c hc)

theorem center_iff_fixed (c : α) : R.center c ↔ R.parent c = c := by
  constructor
  · exact R.parent_fixed c
  · intro h
    exact h ▸ R.selected_center c

theorem parent_idempotent (q : α) : R.parent (R.parent q) = R.parent q :=
  R.parent_fixed _ (R.selected_center q)

/-- This is a partition of all actual tiles, rather than merely a claim
about the groups that happen to have already been exhibited. -/
theorem unique_center (q : α) :
    ∃ c, (R.center c ∧ R.member c q) ∧
      ∀ d, R.center d ∧ R.member d q → d = c := by
  refine ⟨R.parent q, ⟨R.selected_center q, R.selected_member q⟩, ?_⟩
  intro c hc
  exact (R.child_selects_center c q hc.1 hc.2).symm

theorem groups_disjoint {c d q : α} (hc : R.center c) (hd : R.center d)
    (hcq : R.member c q) (hdq : R.member d q) : c = d :=
  (R.child_selects_center c q hc hcq).symm.trans
    (R.child_selects_center d q hd hdq)

/-- Any assignment that puts every tile in an occurring group is forced
to equal the intrinsic parent map. -/
theorem parent_unique (p : α → α)
    (hp : ∀ q, R.center (p q) ∧ R.member (p q) q) : p = R.parent := by
  funext q
  exact (R.child_selects_center (p q) q (hp q).1 (hp q).2).symm

/-- Even without assuming disjointness of a proposed covering, a covering
by the specified occurring groups must use exactly all group centers.
Together with `groups_disjoint`, this is uniqueness of the partition. -/
theorem covering_centers_unique (chosen : α → Prop)
    (hvalid : ∀ c, chosen c → R.center c)
    (hcover : ∀ q, ∃ c, chosen c ∧ R.member c q) :
    chosen = R.center := by
  funext c
  apply propext
  constructor
  · exact hvalid c
  · intro hc
    obtain ⟨d, hd, hdc⟩ := hcover c
    have heq : d = c := R.groups_disjoint (hvalid d hd) hc hdc
      (R.self_member c hc)
    exact heq ▸ hd

/-- Once a geometric transformation carries centers and their members
to centers and their members, the recognized parent map commutes with it.
This applies in particular to translations after their local geometric
covariance has been proved. -/
theorem parent_covariant {β : Type v} (S : Recognition β) (f : α → β)
    (hcenter : ∀ c, R.center c → S.center (f c))
    (hmember : ∀ c q, R.center c → R.member c q → S.member (f c) (f q))
    (q : α) : S.parent (f q) = f (R.parent q) :=
  S.child_selects_center _ _ (hcenter _ (R.selected_center q))
    (hmember _ _ (R.selected_center q) (R.selected_member q))

end Recognition
end Chair.Grouping

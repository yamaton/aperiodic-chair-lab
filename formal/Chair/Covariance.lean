import Chair.Frames

namespace Chair

private theorem exists_mem_map_iff {α β : Type} (f : α → β) (l : List α)
    (P : β → Prop) : (∃ b ∈ l.map f, P b) ↔ ∃ a ∈ l, P (f a) := by
  constructor
  · rintro ⟨b, hb, hp⟩
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hb
    exact ⟨a, ha, hp⟩
  · rintro ⟨a, ha, hp⟩
    exact ⟨f a, List.mem_map.mpr ⟨a, ha, rfl⟩, hp⟩

theorem interfacesFit_eq_true_iff (s u : Solid) (t : V3) :
    interfacesFit s u t = true ↔
      ∀ a ∈ s.faces, ∀ b ∈ u.faces, Opposed a b t → FaceFit a b t := by
  simp [interfacesFit]
  grind

/-- Move the second placement's translation into the contact offset.
This arithmetic identity does not require the matrix to be a cubic frame. -/
theorem contact_moveSolid_shift (s u : Solid) (r : Mat) (t : V3) :
    Contact s (moveSolid ⟨t,r⟩ u) ⟨0,0,0⟩ ↔
      Contact s (moveSolid ⟨⟨0,0,0⟩,r⟩ u) t := by
  simp only [Contact, moveSolid, Opposed, FaceFit, PortMatch,
    List.forall_mem_map, exists_mem_map_iff]
  simp [V3.add, V3.scale]

namespace GridMotion

/-- Exact action on the port data, retaining the signed key. -/
def port (g : GridMotion) (p : Port) : Port :=
  ⟨g.scaledPoint 16 p.pos16, p.key, g.frame.apply p.u, g.frame.apply p.v⟩

/-- Exact action on a face and all its ports. -/
def face (g : GridMotion) (f : Face) : Face :=
  ⟨g.scaledPoint 2 f.center2, g.frame.apply f.normal, f.ports.map g.port⟩

/-- Simultaneously move occupied cubes and exposed face records. -/
def solid (g : GridMotion) (s : Solid) : Solid :=
  ⟨s.cells.map g.cell, s.faces.map g.face⟩

theorem solid_eq_moveSolid (g : GridMotion) (s : Solid) :
    g.solid s = moveSolid g.toPlacement s := rfl

@[simp] theorem port_identity (p : Port) : identity.port p = p := by
  simp only [port, scaledPoint_identity]
  change (⟨p.pos16, p.key, Frame.identity.apply p.u, Frame.identity.apply p.v⟩ : Port) = p
  simp only [Frame.apply_identity]

@[simp] theorem face_identity (f : Face) : identity.face f = f := by
  simp only [face, scaledPoint_identity,
    show identity.port = id from funext port_identity, List.map_id]
  change (⟨f.center2, Frame.identity.apply f.normal, f.ports⟩ : Face) = f
  simp only [Frame.apply_identity]

@[simp] theorem solid_identity (s : Solid) : identity.solid s = s := by
  simp only [solid, show identity.cell = id from funext cell_identity,
    show identity.face = id from funext face_identity, List.map_id]

@[simp] theorem port_comp (g h : GridMotion) (p : Port) :
    (g.comp h).port p = g.port (h.port p) := by
  simp only [port, scaledPoint_comp]
  simp only [comp, Frame.apply_comp]

@[simp] theorem face_comp (g h : GridMotion) (f : Face) :
    (g.comp h).face f = g.face (h.face f) := by
  simp only [face, scaledPoint_comp, List.map_map, Function.comp_def, ← port_comp]
  simp only [comp, Frame.apply_comp]

@[simp] theorem solid_comp (g h : GridMotion) (s : Solid) :
    (g.comp h).solid s = g.solid (h.solid s) := by
  simp [solid, cell_comp, List.map_map, Function.comp_def]

theorem moveSolid_comp (g h : GridMotion) (s : Solid) :
    moveSolid g.toPlacement (moveSolid h.toPlacement s) =
      moveSolid (g.comp h).toPlacement s := by
  simpa only [← solid_eq_moveSolid] using (solid_comp g h s).symm

theorem cell_offset_eq_iff (g : GridMotion) (a b t : V3) :
    g.cell a = (g.cell b).add (g.frame.apply t) ↔ a = b.add t := by
  rw [← cell_add]
  exact ⟨g.cell_injective, congrArg g.cell⟩

theorem scaledPoint_offset_eq_iff (g : GridMotion) (n : Int) (a b t : V3) :
    g.scaledPoint n a = (g.scaledPoint n b).add ((g.frame.apply t).scale n) ↔
      a = b.add (t.scale n) := by
  rw [← Frame.apply_scale, ← scaledPoint_add]
  exact ⟨g.scaledPoint_injective n, congrArg (g.scaledPoint n)⟩

theorem opposed_covariant (g : GridMotion) (a b : Face) (t : V3) :
    Opposed (g.face a) (g.face b) (g.frame.apply t) ↔ Opposed a b t := by
  change (_ = _ ∧ _ = _) ↔ (_ = _ ∧ _ = _)
  apply and_congr (scaledPoint_offset_eq_iff g 2 _ _ t)
  change g.frame.apply a.normal = (g.frame.apply b.normal).scale (-1) ↔ _
  rw [← Frame.apply_scale]
  exact g.frame.apply_inj _ _

theorem portMatch_covariant (g : GridMotion) (a b : Port) (t : V3) :
    PortMatch (g.port a) (g.port b) (g.frame.apply t) ↔ PortMatch a b t := by
  simp only [PortMatch, port, scaledPoint_offset_eq_iff]
  have cancel (a b : V3) : g.frame.apply a = g.frame.apply b ↔ a = b :=
    ⟨g.frame.apply_injective, congrArg g.frame.apply⟩
  simp only [cancel]

theorem faceFit_covariant (g : GridMotion) (a b : Face) (t : V3) :
    FaceFit (g.face a) (g.face b) (g.frame.apply t) ↔ FaceFit a b t := by
  simp only [FaceFit, face, List.forall_mem_map, exists_mem_map_iff,
    portMatch_covariant]

/-- Contact covariance includes the correctly rotated relative offset. -/
theorem contact_covariant (g : GridMotion) (s u : Solid) (t : V3) :
    Contact (g.solid s) (g.solid u) (g.frame.apply t) ↔ Contact s u t := by
  simp only [Contact, solid, List.forall_mem_map, exists_mem_map_iff, ne_eq, cell_offset_eq_iff,
    opposed_covariant, faceFit_covariant]

theorem interfacesFit_covariant (g : GridMotion) (s u : Solid) (t : V3) :
    interfacesFit (g.solid s) (g.solid u) (g.frame.apply t) = true ↔
      interfacesFit s u t = true := by
  simp [interfacesFit_eq_true_iff, solid, List.mem_map,
    opposed_covariant, faceFit_covariant]

theorem contact_covariant_zero (g : GridMotion) (s u : Solid) :
    Contact (g.solid s) (g.solid u) ⟨0,0,0⟩ ↔ Contact s u ⟨0,0,0⟩ := by
  have h := contact_covariant g s u V3.zero
  rw [Frame.apply_zero] at h
  exact h

theorem interfacesFit_covariant_zero (g : GridMotion) (s u : Solid) :
    interfacesFit (g.solid s) (g.solid u) ⟨0,0,0⟩ = true ↔
      interfacesFit s u ⟨0,0,0⟩ = true := by
  have h := interfacesFit_covariant g s u V3.zero
  rw [Frame.apply_zero] at h
  exact h

/-- Normalize the first solid without imposing a condition on either placement. -/
theorem contact_relative (g h : GridMotion) (s u : Solid) :
    Contact (g.solid s) (h.solid u) ⟨0,0,0⟩ ↔
      Contact s ((g.inv.comp h).solid u) ⟨0,0,0⟩ := by
  have hc := contact_covariant_zero g.inv (g.solid s) (h.solid u)
  rw [← solid_comp, ← solid_comp, inv_comp, solid_identity] at hc
  exact hc.symm

end GridMotion
end Chair

import Chair.Geometry

namespace Chair
deriving instance ReflBEq, LawfulBEq for Mat


namespace V3

def zero : V3 := ⟨0, 0, 0⟩
@[ext] theorem ext {a b : V3} (hx : a.x = b.x) (hy : a.y = b.y)
    (hz : a.z = b.z) : a = b := by cases a; cases b; simp_all
@[simp] theorem add_zero (a : V3) : a.add zero = a := by cases a; simp [add, zero]
@[simp] theorem zero_add (a : V3) : zero.add a = a := by cases a; simp [add, zero]
theorem add_assoc (a b c : V3) : (a.add b).add c = a.add (b.add c) := by
  simp [add, Int.add_assoc]
theorem add_comm (a b : V3) : a.add b = b.add a := by simp [add, Int.add_comm]
@[simp] theorem scale_zero (k : Int) : zero.scale k = zero := by simp [scale, zero]
@[simp] theorem scale_one (a : V3) : a.scale 1 = a := by cases a; simp [scale]
@[simp] theorem scale_add (a b : V3) (k : Int) :
    (a.add b).scale k = (a.scale k).add (b.scale k) := by simp [add, scale, Int.mul_add]
@[simp] theorem scale_scale (a : V3) (j k : Int) :
    (a.scale j).scale k = a.scale (k*j) := by simp [scale, Int.mul_assoc]
@[simp] theorem add_neg (a : V3) : a.add (a.scale (-1)) = zero := by
  simp [add, scale, zero] <;> omega
@[simp] theorem neg_add (a : V3) : (a.scale (-1)).add a = zero := by
  simp [add, scale, zero] <;> omega
@[simp] theorem sub_self (a : V3) : a.sub a = zero := by simp [sub, zero]
theorem sub_eq_add_neg (a b : V3) : a.sub b = a.add (b.scale (-1)) := by
  simp [sub, add, scale, Int.sub_eq_add_neg]
@[simp] theorem add_left_cancel_iff (a b c : V3) : a.add b = a.add c ↔ b = c := by
  cases b; cases c; simp [add, V3.mk.injEq]
@[simp] theorem add_right_cancel_iff (a b c : V3) : a.add c = b.add c ↔ a = b := by
  cases a; cases b; simp [add, V3.mk.injEq]
end V3

namespace Mat

def identity : Mat := ⟨⟨1,0,0⟩, ⟨0,1,0⟩, ⟨0,0,1⟩⟩
def transpose (r : Mat) : Mat := ofColumns r.x r.y r.z
def comp (r s : Mat) : Mat :=
  ofColumns (r.apply ⟨s.x.x,s.y.x,s.z.x⟩)
    (r.apply ⟨s.x.y,s.y.y,s.z.y⟩) (r.apply ⟨s.x.z,s.y.z,s.z.z⟩)
def cubeOffset (r : Mat) : V3 :=
  ⟨min r.x.x 0 + min r.x.y 0 + min r.x.z 0,
   min r.y.x 0 + min r.y.y 0 + min r.y.z 0,
   min r.z.x 0 + min r.z.y 0 + min r.z.z 0⟩
@[simp] theorem apply_identity (q : V3) : identity.apply q = q := by
  cases q; simp [identity, apply, V3.dot]
@[simp] theorem apply_zero (r : Mat) : r.apply V3.zero = V3.zero := by
  simp [apply, V3.dot, V3.zero]
@[simp] theorem apply_add (r : Mat) (a b : V3) :
    r.apply (a.add b) = (r.apply a).add (r.apply b) := by
  apply V3.ext <;> simp [apply, V3.dot, V3.add] <;> grind
@[simp] theorem apply_scale (r : Mat) (a : V3) (k : Int) :
    r.apply (a.scale k) = (r.apply a).scale k := by
  apply V3.ext <;> simp [apply, V3.dot, V3.scale] <;> grind
@[simp] theorem apply_comp (r s : Mat) (q : V3) :
    (r.comp s).apply q = r.apply (s.apply q) := by
  apply V3.ext <;> simp [comp, apply, ofColumns, V3.dot] <;> grind
@[ext] theorem ext {r s : Mat} (hx : r.x = s.x) (hy : r.y = s.y)
    (hz : r.z = s.z) : r = s := by cases r; cases s; simp_all

theorem ext_apply {r s : Mat} (h : ∀ q, r.apply q = s.apply q) : r = s := by
  have h₁ := h ⟨1,0,0⟩; have h₂ := h ⟨0,1,0⟩; have h₃ := h ⟨0,0,1⟩
  simp [apply, V3.dot, V3.mk.injEq] at h₁ h₂ h₃
  apply Mat.ext <;> apply V3.ext <;> simp_all
@[simp] theorem comp_identity (r : Mat) : r.comp identity = r := by
  apply ext_apply; intro q; simp
@[simp] theorem identity_comp (r : Mat) : identity.comp r = r := by
  apply ext_apply; intro q; simp
theorem comp_assoc (r s t : Mat) : (r.comp s).comp t = r.comp (s.comp t) := by
  apply ext_apply; intro q; simp

theorem cube_eq (r : Mat) (q : V3) : r.cube q = (r.apply q).add r.cubeOffset := rfl
@[simp] theorem cube_add (r : Mat) (q t : V3) :
    r.cube (q.add t) = (r.cube q).add (r.apply t) := by
  simp only [cube_eq, apply_add]
  simp [V3.add, Int.add_assoc, Int.add_comm, Int.add_left_comm]
end Mat

/-- One of the 24 proper cubic frames, with no quotient by chair symmetries. -/
structure Frame where
  mat : Mat
  proper : mat ∈ rotations
  deriving DecidableEq

namespace Frame

/-- Every abstract proper frame is represented by a normalized orientation index. -/
theorem exists_rotation (f : Frame) : ∃ r : Fin 24, rotation r = f.mat := by
  obtain ⟨i, hi, heq⟩ := List.mem_iff_getElem.mp f.proper
  refine ⟨⟨i, by simpa only [rotations_length] using hi⟩, ?_⟩
  exact heq

private theorem identity_proper : Mat.identity ∈ rotations := by decide_cbv
private theorem closed : ∀ r ∈ rotations, ∀ s ∈ rotations, r.comp s ∈ rotations := by
  have h : rotations.all (fun r => rotations.all (fun s => decide (r.comp s ∈ rotations))) = true := by
    decide_cbv
  simpa only [List.all_eq_true, decide_eq_true_eq] using h
private theorem inverse_facts : ∀ r ∈ rotations,
    r.transpose ∈ rotations ∧ r.transpose.comp r = Mat.identity ∧
    r.comp r.transpose = Mat.identity := by
  have h : rotations.all (fun r => decide (r.transpose ∈ rotations ∧
      r.transpose.comp r = Mat.identity ∧ r.comp r.transpose = Mat.identity)) = true := by
    decide_cbv
  simpa only [List.all_eq_true, decide_eq_true_eq] using h
private theorem cube_cocycle : ∀ r ∈ rotations, ∀ s ∈ rotations,
    (r.comp s).cubeOffset = (r.apply s.cubeOffset).add r.cubeOffset := by
  have h : rotations.all (fun r => rotations.all (fun s => decide
      ((r.comp s).cubeOffset = (r.apply s.cubeOffset).add r.cubeOffset))) = true := by
    decide_cbv
  simpa only [List.all_eq_true, decide_eq_true_eq] using h

def identity : Frame := ⟨Mat.identity, identity_proper⟩
def comp (r s : Frame) : Frame := ⟨r.mat.comp s.mat, closed _ r.proper _ s.proper⟩
def inv (r : Frame) : Frame := ⟨r.mat.transpose, (inverse_facts _ r.proper).1⟩
def apply (r : Frame) (q : V3) : V3 := r.mat.apply q
@[ext] theorem ext {r s : Frame} (h : r.mat = s.mat) : r = s := by cases r; cases s; simp_all
@[simp] theorem apply_identity (q : V3) : identity.apply q = q := Mat.apply_identity q
@[simp] theorem apply_comp (r s : Frame) (q : V3) :
    (r.comp s).apply q = r.apply (s.apply q) := Mat.apply_comp _ _ _
@[simp] theorem apply_add (r : Frame) (a b : V3) :
    r.apply (a.add b) = (r.apply a).add (r.apply b) := Mat.apply_add _ _ _
@[simp] theorem apply_scale (r : Frame) (a : V3) (k : Int) :
    r.apply (a.scale k) = (r.apply a).scale k := Mat.apply_scale _ _ _
@[simp] theorem apply_zero (r : Frame) : r.apply V3.zero = V3.zero := Mat.apply_zero _
theorem apply_sub (r : Frame) (a b : V3) :
    r.apply (a.sub b) = (r.apply a).sub (r.apply b) := by
  simp [V3.sub_eq_add_neg]
@[simp] theorem comp_identity (r : Frame) : r.comp identity = r := by apply ext; exact Mat.comp_identity _
@[simp] theorem identity_comp (r : Frame) : identity.comp r = r := by apply ext; exact Mat.identity_comp _
theorem comp_assoc (r s t : Frame) : (r.comp s).comp t = r.comp (s.comp t) := by
  apply ext; exact Mat.comp_assoc _ _ _
@[simp] theorem inv_comp (r : Frame) : r.inv.comp r = identity := by
  apply ext; exact (inverse_facts _ r.proper).2.1
@[simp] theorem comp_inv (r : Frame) : r.comp r.inv = identity := by
  apply ext; exact (inverse_facts _ r.proper).2.2
@[simp] theorem inv_inv (r : Frame) : r.inv.inv = r := by
  apply ext; rfl
@[simp] theorem inv_apply_apply (r : Frame) (q : V3) : r.inv.apply (r.apply q) = q := by
  rw [← apply_comp, inv_comp, apply_identity]
@[simp] theorem apply_inv_apply (r : Frame) (q : V3) : r.apply (r.inv.apply q) = q := by
  rw [← apply_comp, comp_inv, apply_identity]
theorem apply_injective (r : Frame) {a b : V3} (h : r.apply a = r.apply b) : a = b := by
  have := congrArg r.inv.apply h; simpa using this
@[simp] theorem apply_inj (r : Frame) (a b : V3) : r.apply a = r.apply b ↔ a = b :=
  ⟨apply_injective r, congrArg r.apply⟩
theorem cube_comp (r s : Frame) (q : V3) :
    (r.comp s).mat.cube q = r.mat.cube (s.mat.cube q) := by
  simp only [Mat.cube_eq, comp, Mat.apply_comp, Mat.apply_add]
  rw [cube_cocycle _ r.proper _ s.proper, V3.add_assoc]
@[simp] theorem cube_identity (q : V3) : identity.mat.cube q = q := by
  simp [identity, Mat.cube_eq, Mat.identity, Mat.cubeOffset, Mat.apply, V3.dot,
    V3.add, Int.min_def]
end Frame

/-- A proper cubic frame and an integral translation. Composition acts right to left. -/
structure GridMotion where
  shift : V3
  frame : Frame
  deriving DecidableEq

namespace GridMotion

def identity : GridMotion := ⟨V3.zero, Frame.identity⟩
def comp (g h : GridMotion) : GridMotion :=
  ⟨(g.frame.apply h.shift).add g.shift, g.frame.comp h.frame⟩
def inv (g : GridMotion) : GridMotion :=
  ⟨(g.frame.inv.apply g.shift).scale (-1), g.frame.inv⟩
def point (g : GridMotion) (q : V3) : V3 := (g.frame.apply q).add g.shift
def cell (g : GridMotion) (q : V3) : V3 := (g.frame.mat.cube q).add g.shift
def scaledPoint (g : GridMotion) (k : Int) (q : V3) : V3 :=
  (g.frame.apply q).add (g.shift.scale k)
def toPlacement (g : GridMotion) : Placement := ⟨g.shift, g.frame.mat⟩

theorem point_add (g : GridMotion) (q t : V3) :
    g.point (q.add t) = (g.point q).add (g.frame.apply t) := by
  simp only [point, Frame.apply_add]
  simp [V3.add, Int.add_assoc, Int.add_comm]
theorem cell_add (g : GridMotion) (q t : V3) :
    g.cell (q.add t) = (g.cell q).add (g.frame.apply t) := by
  simp only [cell, Mat.cube_add, Frame.apply]
  simp [V3.add, Int.add_comm, Int.add_left_comm]
theorem scaledPoint_add (g : GridMotion) (k : Int) (q t : V3) :
    g.scaledPoint k (q.add t) = (g.scaledPoint k q).add (g.frame.apply t) := by
  simp only [scaledPoint, Frame.apply_add]
  simp [V3.add, Int.add_assoc, Int.add_comm, Int.add_left_comm]

@[ext] theorem ext {g h : GridMotion} (hs : g.shift = h.shift) (hf : g.frame = h.frame) :
    g = h := by cases g; cases h; simp_all
@[simp] theorem point_identity (q : V3) : identity.point q = q := by simp [point, identity]
@[simp] theorem point_comp (g h : GridMotion) (q : V3) :
    (g.comp h).point q = g.point (h.point q) := by simp [point, comp, V3.add_assoc]
@[simp] theorem cell_identity (q : V3) : identity.cell q = q := by simp [cell, identity]
@[simp] theorem cell_comp (g h : GridMotion) (q : V3) :
    (g.comp h).cell q = g.cell (h.cell q) := by
  simp [cell, comp, Frame.cube_comp, Mat.cube_add, Frame.apply, V3.add_assoc]
@[simp] theorem scaledPoint_identity (k : Int) (q : V3) : identity.scaledPoint k q = q := by
  simp [scaledPoint, identity]
@[simp] theorem scaledPoint_comp (g h : GridMotion) (k : Int) (q : V3) :
    (g.comp h).scaledPoint k q = g.scaledPoint k (h.scaledPoint k q) := by
  simp [scaledPoint, comp, V3.add_assoc]
@[simp] theorem comp_identity (g : GridMotion) : g.comp identity = g := by
  apply ext <;> simp [comp, identity]
@[simp] theorem identity_comp (g : GridMotion) : identity.comp g = g := by
  apply ext <;> simp [comp, identity]
theorem comp_assoc (g h k : GridMotion) : (g.comp h).comp k = g.comp (h.comp k) := by
  apply ext <;> simp [comp, Frame.comp_assoc, V3.add_assoc]
@[simp] theorem inv_comp (g : GridMotion) : g.inv.comp g = identity := by
  apply ext <;> simp [comp, inv, identity]
@[simp] theorem comp_inv (g : GridMotion) : g.comp g.inv = identity := by
  apply ext <;> simp [comp, inv, identity]
@[simp] theorem inv_inv (g : GridMotion) : g.inv.inv = g := by
  apply ext <;> simp [inv]
@[simp] theorem inv_point_point (g : GridMotion) (q : V3) : g.inv.point (g.point q) = q := by
  rw [← point_comp, inv_comp, point_identity]
@[simp] theorem point_inv_point (g : GridMotion) (q : V3) : g.point (g.inv.point q) = q := by
  rw [← point_comp, comp_inv, point_identity]
@[simp] theorem inv_cell_cell (g : GridMotion) (q : V3) : g.inv.cell (g.cell q) = q := by
  rw [← cell_comp, inv_comp, cell_identity]
@[simp] theorem cell_inv_cell (g : GridMotion) (q : V3) : g.cell (g.inv.cell q) = q := by
  rw [← cell_comp, comp_inv, cell_identity]
@[simp] theorem inv_scaledPoint_scaledPoint (g : GridMotion) (k : Int) (q : V3) :
    g.inv.scaledPoint k (g.scaledPoint k q) = q := by
  rw [← scaledPoint_comp, inv_comp, scaledPoint_identity]
@[simp] theorem scaledPoint_inv_scaledPoint (g : GridMotion) (k : Int) (q : V3) :
    g.scaledPoint k (g.inv.scaledPoint k q) = q := by
  rw [← scaledPoint_comp, comp_inv, scaledPoint_identity]
@[simp] theorem point_inj (g : GridMotion) (a b : V3) : g.point a = g.point b ↔ a = b := by
  constructor
  · intro h; have := congrArg g.inv.point h; simpa using this
  · exact congrArg g.point
@[simp] theorem cell_inj (g : GridMotion) (a b : V3) : g.cell a = g.cell b ↔ a = b := by
  constructor
  · intro h; have := congrArg g.inv.cell h; simpa using this
  · exact congrArg g.cell
@[simp] theorem scaledPoint_inj (g : GridMotion) (k : Int) (a b : V3) :
    g.scaledPoint k a = g.scaledPoint k b ↔ a = b := by
  constructor
  · intro h; have := congrArg (g.inv.scaledPoint k) h; simpa using this
  · exact congrArg (g.scaledPoint k)
theorem point_injective (g : GridMotion) {a b : V3} (h : g.point a = g.point b) :
    a = b := (point_inj g a b).mp h
theorem cell_injective (g : GridMotion) {a b : V3} (h : g.cell a = g.cell b) :
    a = b := (cell_inj g a b).mp h
theorem scaledPoint_injective (g : GridMotion) (k : Int) {a b : V3}
    (h : g.scaledPoint k a = g.scaledPoint k b) : a = b := (scaledPoint_inj g k a b).mp h
end GridMotion
end Chair

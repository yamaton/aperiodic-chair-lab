import Std

namespace Chair

structure V3 where
  x : Int
  y : Int
  z : Int
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr

namespace V3

def add (a b : V3) : V3 := ⟨a.x + b.x, a.y + b.y, a.z + b.z⟩
def sub (a b : V3) : V3 := ⟨a.x - b.x, a.y - b.y, a.z - b.z⟩
def scale (n : Int) (a : V3) : V3 := ⟨n * a.x, n * a.y, n * a.z⟩
def half (a : V3) : V3 := ⟨a.x / 2, a.y / 2, a.z / 2⟩

theorem half_sub_of_eq_add_double {a b t : V3}
    (h : a = b.add (t.scale 2)) : (a.sub b).half = t := by
  cases a; cases b; cases t
  simp only [add, scale, V3.mk.injEq] at h
  simp only [sub, half, V3.mk.injEq]
  omega

end V3

structure Port where
  /-- Absolute port center, measured in sixteenths of a unit. -/
  pos16 : V3
  key : Int
  u : V3
  v : V3
  deriving DecidableEq, BEq, Repr

structure Face where
  /-- Absolute face center, measured in halves of a unit. -/
  center2 : V3
  normal : V3
  ports : List Port
  deriving DecidableEq, BEq, Repr

structure Solid where
  /-- Lower corners of occupied unit cubes. -/
  cells : List V3
  faces : List Face
  deriving DecidableEq, BEq, Repr

/-- The second face is translated by the integral vector `t`. -/
def Opposed (a b : Face) (t : V3) : Prop :=
  a.center2 = b.center2.add (t.scale 2) ∧ a.normal = b.normal.scale (-1)

def opposed (a b : Face) (t : V3) : Bool :=
  decide (a.center2 = b.center2.add (t.scale 2)) &&
  decide (a.normal = b.normal.scale (-1))

def PortMatch (a b : Port) (t : V3) : Prop :=
  a.pos16 = b.pos16.add (t.scale 16) ∧ a.key = -b.key ∧ a.u = b.u ∧ a.v = b.v

def portMatches (a b : Port) (t : V3) : Bool :=
  decide (a.pos16 = b.pos16.add (t.scale 16)) && decide (a.key = -b.key) &&
  decide (a.u = b.u) && decide (a.v = b.v)

/-- Both directions are required: no port may disappear on either side. -/
def FaceFit (a b : Face) (t : V3) : Prop :=
  (∀ p ∈ a.ports, ∃ q ∈ b.ports, PortMatch p q t) ∧
  (∀ q ∈ b.ports, ∃ p ∈ a.ports, PortMatch p q t)

def faceFits (a b : Face) (t : V3) : Bool :=
  a.ports.all (fun p => b.ports.any (fun q => portMatches p q t)) &&
  b.ports.all (fun q => a.ports.any (fun p => portMatches p q t))

def disjoint (s u : Solid) (t : V3) : Bool :=
  s.cells.all (fun a => u.cells.all (fun b => !(decide (a = b.add t))))

def touching (s u : Solid) (t : V3) : Bool :=
  s.faces.any (fun a => u.faces.any (fun b => opposed a b t))

def interfacesFit (s u : Solid) (t : V3) : Bool :=
  s.faces.all (fun a => u.faces.all (fun b =>
    if opposed a b t then faceFits a b t else true))

/-- Integral-grid contact; `u` has already been oriented. -/
def contact (s u : Solid) (t : V3) : Bool :=
  disjoint s u t && touching s u t && interfacesFit s u t

def Contact (s u : Solid) (t : V3) : Prop :=
  (∀ a ∈ s.cells, ∀ b ∈ u.cells, a ≠ b.add t) ∧
  (∃ a ∈ s.faces, ∃ b ∈ u.faces, Opposed a b t) ∧
  (∀ a ∈ s.faces, ∀ b ∈ u.faces, Opposed a b t → FaceFit a b t)

@[simp] theorem opposed_eq_true (a b : Face) (t : V3) :
    opposed a b t = true ↔ Opposed a b t := by
  simp [opposed, Opposed]

@[simp] theorem opposed_eq_false (a b : Face) (t : V3) :
    opposed a b t = false ↔ ¬Opposed a b t := by
  rw [Bool.eq_false_iff]
  exact not_congr (opposed_eq_true a b t)

@[simp] theorem portMatches_eq_true (a b : Port) (t : V3) :
    portMatches a b t = true ↔ PortMatch a b t := by
  simp [portMatches, PortMatch, and_assoc]

@[simp] theorem faceFits_eq_true (a b : Face) (t : V3) :
    faceFits a b t = true ↔ FaceFit a b t := by
  simp [faceFits, FaceFit]

theorem contact_eq_true_iff (s u : Solid) (t : V3) :
    contact s u t = true ↔ Contact s u t := by
  simp [contact, Contact, disjoint, touching, interfacesFit, and_assoc]
  grind

/-- Every face-pair supplies a candidate, including harmless extraneous ones.
No bounding-box assumption or finite search radius is needed. -/
def candidates (s u : Solid) : List V3 :=
  s.faces.flatMap (fun a => u.faces.map (fun b => (a.center2.sub b.center2).half))

theorem contact_complete {s u : Solid} {t : V3}
    (h : contact s u t = true) : t ∈ candidates s u := by
  obtain ⟨_, ⟨a, ha, b, hb, hcenter, _⟩, _⟩ := (contact_eq_true_iff s u t).mp h
  apply List.mem_flatMap.mpr
  refine ⟨a, ha, List.mem_map.mpr ⟨b, hb, ?_⟩⟩
  exact V3.half_sub_of_eq_add_double hcenter

def legalCandidates (s u : Solid) : List V3 :=
  (candidates s u).filter (contact s u)

theorem contact_iff_mem_legalCandidates (s u : Solid) (t : V3) :
    contact s u t = true ↔ t ∈ legalCandidates s u := by
  simp only [legalCandidates, List.mem_filter]
  exact ⟨fun h => ⟨contact_complete h, h⟩, fun h => h.2⟩

/-- Optional deduplication does not change the exhaustive contact language. -/
def uniqueCandidates (s u : Solid) : List V3 := (candidates s u).eraseDups

theorem contact_mem_uniqueCandidates {s u : Solid} {t : V3}
    (h : contact s u t = true) : t ∈ uniqueCandidates s u := by
  simpa only [uniqueCandidates, List.mem_eraseDups] using contact_complete h

def uniqueLegalCandidates (s u : Solid) : List V3 :=
  (uniqueCandidates s u).filter (contact s u)

theorem contact_iff_mem_uniqueLegalCandidates (s u : Solid) (t : V3) :
    contact s u t = true ↔ t ∈ uniqueLegalCandidates s u := by
  simp only [uniqueLegalCandidates, List.mem_filter]
  exact ⟨fun h => ⟨contact_mem_uniqueCandidates h, h⟩, fun h => h.2⟩

end Chair

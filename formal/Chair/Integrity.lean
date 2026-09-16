import Chair.Cache

namespace Chair

set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false

deriving instance ReflBEq, LawfulBEq for Mat
deriving instance ReflBEq, LawfulBEq for RawPort
deriving instance ReflBEq, LawfulBEq for Port
deriving instance ReflBEq, LawfulBEq for Face

/-- Reattach the outward normal to recover the complete raw port record. -/
def assignedPorts (s : Solid) : List RawPort :=
  s.faces.flatMap fun f => f.ports.map fun p =>
    ⟨p.pos16, p.key, p.u, p.v, f.normal⟩

theorem fine_cell_count : fine.cells.length = 7 := by decide +kernel
theorem fine_cells_distinct : fine.cells.Nodup := by decide +kernel
theorem fine_face_count : fine.faces.length = 24 := by decide +kernel
theorem fine_faces_distinct : fine.faces.Nodup := by decide +kernel
theorem fine_ports_per_face : ∀ f ∈ fine.faces, f.ports.length = 8 := by decide +kernel
theorem frozen_port_count : Input.ports.length = 192 := by decide +kernel
theorem frozen_ports_distinct : Input.ports.Nodup := by decide +kernel
theorem fine_assigned_port_count : (assignedPorts fine).length = 192 := by decide +kernel
theorem fine_assigned_ports_distinct : (assignedPorts fine).Nodup := by decide +kernel

/-- Together with `fine_assigned_ports_distinct`, this gives exactly one
assignment for each frozen port, and no invented boundary ports. -/
theorem fine_assignment_exact :
    (∀ p ∈ Input.ports, p ∈ assignedPorts fine) ∧
    (∀ p ∈ assignedPorts fine, p ∈ Input.ports) := by decide +kernel

theorem macro_cell_count : macroSolid.cells.length = 56 := by decide +kernel
theorem macro_cells_distinct : macroSolid.cells.Nodup := by decide +kernel
theorem macro_face_count : macroSolid.faces.length = 96 := by decide +kernel
theorem macro_faces_distinct : macroSolid.faces.Nodup := by decide +kernel
theorem macro_ports_per_face : ∀ f ∈ macroSolid.faces, f.ports.length = 8 := by decide +kernel

def binaryCorners : List V3 :=
  [⟨0,0,0⟩, ⟨0,0,1⟩, ⟨0,1,0⟩, ⟨0,1,1⟩,
   ⟨1,0,0⟩, ⟨1,0,1⟩, ⟨1,1,0⟩, ⟨1,1,1⟩]

def doubledChairCells : List V3 :=
  fine.cells.flatMap fun q => binaryCorners.map fun b => (q.scale 2).add b

theorem macro_cells_exactly_doubled :
    (∀ q ∈ macroSolid.cells, q ∈ doubledChairCells) ∧
    (∀ q ∈ doubledChairCells, q ∈ macroSolid.cells) := by decide +kernel

theorem child_count : Input.children.length = 8 := by decide +kernel
theorem children_distinct : Input.children.Nodup := by decide +kernel
theorem child_frames_are_rotations :
    ∀ g ∈ Input.children, g.frame ∈ rotations := by decide +kernel

/-- Row vectors are perpendicular signed coordinate vectors and have positive
orientation. Thus every listed matrix is a proper signed permutation. -/
theorem rotation_frames_proper :
    ∀ r ∈ rotations,
      r.x ∈ normals ∧ r.y ∈ normals ∧ r.z ∈ normals ∧
      r.x.dot r.y = 0 ∧ r.x.dot r.z = 0 ∧ r.y.dot r.z = 0 ∧
      r.x.cross r.y = r.z := by decide +kernel

/-- No face-contact assumption is imposed on a pair of children. Disjointness
and matching of every actual interface are checked for every distinct pair. -/
theorem child_pairs_compatible :
    ∀ a ∈ Input.children, ∀ b ∈ Input.children, a ≠ b →
      disjoint (childSolid a) (childSolid b) zero = true ∧
      interfacesFit (childSolid a) (childSolid b) zero = true := by decide +kernel

/-- Every ordered pair of perpendicular signed coordinate axes occurs, with
its unique positively oriented third column. -/
theorem completed_coordinate_frame_mem_rotations {u v : V3}
    (hu : u ∈ normals) (hv : v ∈ normals) (horth : u.dot v = 0) :
    Mat.ofColumns u v (u.cross v) ∈ rotations := by
  unfold rotations
  apply List.mem_flatMap.mpr
  refine ⟨u, hu, List.mem_map.mpr ⟨v, ?_, rfl⟩⟩
  exact List.mem_filter.mpr ⟨hv, by simpa only [beq_iff_eq] using horth⟩

/-- Boundary patches of the eight independently placed children, before any
internal interfaces are cancelled. -/
def allChildFaces : List Face :=
  Input.children.flatMap fun g => (childSolid g).faces

/-- Cancel exactly the patches having an opposed patch from the assembly.
This definition does not consult `makeSolid` or the macro occupancy boundary. -/
def uncancelledChildFaces : List Face :=
  allChildFaces.filter fun f => !(allChildFaces.any fun other => opposed f other zero)

/-- The occupancy-based macro reconstruction has precisely the uncancelled
child boundary, including every port position, key, and ordered frame. -/
theorem macro_boundary_exact :
    (∀ f ∈ macroSolid.faces, f ∈ uncancelledChildFaces) ∧
    (∀ f ∈ uncancelledChildFaces, f ∈ macroSolid.faces) := by
  simp only [uncancelledChildFaces, allChildFaces, childSolid,
    fine_eq_cached, macro_eq_cached]
  decide +kernel

end Chair

import Chair.Certificate

namespace Chair.Controls

/-- Tiny test records with one matching interface after translation by e₁.
They exercise certificate semantics, independently of the chair search. -/
def left : Solid := ⟨[⟨0,0,0⟩],
  [⟨⟨2,1,1⟩, ⟨1,0,0⟩, [⟨⟨16,8,8⟩, 1, ⟨0,1,0⟩, ⟨0,0,1⟩⟩]⟩]⟩
def right : Solid := ⟨[⟨0,0,0⟩],
  [⟨⟨0,1,1⟩, ⟨-1,0,0⟩, [⟨⟨0,8,8⟩, -1, ⟨0,1,0⟩, ⟨0,0,1⟩⟩]⟩]⟩
def offset : V3 := ⟨1,0,0⟩

theorem valid_certificate : certificateCheck left right [offset] [] = true := by
  decide +kernel
theorem missing_contact_rejected : certificateCheck left right [] [] = false := by
  decide +kernel
theorem nonexistent_contact_rejected :
    certificateCheck left right [⟨3,0,0⟩] [] = false := by
  decide +kernel
theorem nonexistent_cell_index_rejected :
    rejectCheck left right offset (.overlap 999 0) = false := by
  decide +kernel
theorem nonexistent_face_index_rejected :
    rejectCheck left right offset (.mismatch 0 999) = false := by
  decide +kernel
theorem false_overlap_rejected :
    rejectCheck left right offset (.overlap 0 0) = false := by
  decide +kernel
theorem nonopposed_mismatch_rejected :
    rejectCheck left right ⟨3,0,0⟩ (.mismatch 0 0) = false := by
  decide +kernel
theorem false_mismatch_rejected :
    rejectCheck left right offset (.mismatch 0 0) = false := by
  decide +kernel

end Chair.Controls

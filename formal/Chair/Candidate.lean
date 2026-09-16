import Chair.Input

namespace Chair

def zero : V3 := ⟨0,0,0⟩
def fine : Solid := makeSolid Input.cells Input.ports
def childSolid (g : Placement) : Solid := moveSolid g fine
def macroCells : List V3 := Input.children.flatMap fun g =>
  Input.cells.map fun q => (g.frame.cube q).add g.shift
def macroPorts : List RawPort := Input.children.flatMap fun g =>
  Input.ports.map (RawPort.move g)
def macroSolid : Solid := makeSolid macroCells macroPorts

def orientedFine (r : Fin 24) : Solid := moveSolid ⟨zero, rotation r⟩ fine
def orientedMacro (r : Fin 24) : Solid := moveSolid ⟨zero, rotation r⟩ macroSolid

def fineContacts (r : Fin 24) : List V3 := uniqueLegalCandidates fine (orientedFine r)
def macroContacts (r : Fin 24) : List V3 := uniqueLegalCandidates macroSolid (orientedMacro r)

def fineContact (r : Fin 24) (t : V3) : Prop := Contact fine (orientedFine r) t
def macroContact (r : Fin 24) (t : V3) : Prop := Contact macroSolid (orientedMacro r) t

theorem fineContact_iff_mem (r : Fin 24) (t : V3) :
    fineContact r t ↔ t ∈ fineContacts r := by
  rw [fineContact, ← contact_eq_true_iff]
  exact contact_iff_mem_uniqueLegalCandidates _ _ _

theorem macroContact_iff_mem (r : Fin 24) (t : V3) :
    macroContact r t ↔ t ∈ macroContacts r := by
  rw [macroContact, ← contact_eq_true_iff]
  exact contact_iff_mem_uniqueLegalCandidates _ _ _

end Chair

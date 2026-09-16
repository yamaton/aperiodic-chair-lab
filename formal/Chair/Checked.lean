import Chair.Batches.Batch0
import Chair.Batches.Batch1
import Chair.Batches.Batch2
import Chair.Batches.Batch3

namespace Chair
open Witnesses

set_option maxRecDepth 100000

def fineAccepted (r : Fin 24) : List V3 := match r.val with
  | 0 => fineAccepted0
  | 1 => fineAccepted1
  | 2 => fineAccepted2
  | 3 => fineAccepted3
  | 4 => fineAccepted4
  | 5 => fineAccepted5
  | 6 => fineAccepted6
  | 7 => fineAccepted7
  | 8 => fineAccepted8
  | 9 => fineAccepted9
  | 10 => fineAccepted10
  | 11 => fineAccepted11
  | 12 => fineAccepted12
  | 13 => fineAccepted13
  | 14 => fineAccepted14
  | 15 => fineAccepted15
  | 16 => fineAccepted16
  | 17 => fineAccepted17
  | 18 => fineAccepted18
  | 19 => fineAccepted19
  | 20 => fineAccepted20
  | 21 => fineAccepted21
  | 22 => fineAccepted22
  | 23 => fineAccepted23
  | _ => []

def fineRejected (r : Fin 24) : List (V3 × RejectWitness) := match r.val with
  | 0 => fineRejected0
  | 1 => fineRejected1
  | 2 => fineRejected2
  | 3 => fineRejected3
  | 4 => fineRejected4
  | 5 => fineRejected5
  | 6 => fineRejected6
  | 7 => fineRejected7
  | 8 => fineRejected8
  | 9 => fineRejected9
  | 10 => fineRejected10
  | 11 => fineRejected11
  | 12 => fineRejected12
  | 13 => fineRejected13
  | 14 => fineRejected14
  | 15 => fineRejected15
  | 16 => fineRejected16
  | 17 => fineRejected17
  | 18 => fineRejected18
  | 19 => fineRejected19
  | 20 => fineRejected20
  | 21 => fineRejected21
  | 22 => fineRejected22
  | 23 => fineRejected23
  | _ => []

theorem fine_certificates (r : Fin 24) :
    certificateCheck fine (orientedFine r) (fineAccepted r) (fineRejected r) = true := by
  revert r
  exact (Fin.cases fine_certificate_0 (Fin.cases fine_certificate_1 (Fin.cases fine_certificate_2 (Fin.cases fine_certificate_3 (Fin.cases fine_certificate_4 (Fin.cases fine_certificate_5 (Fin.cases fine_certificate_6 (Fin.cases fine_certificate_7 (Fin.cases fine_certificate_8 (Fin.cases fine_certificate_9 (Fin.cases fine_certificate_10 (Fin.cases fine_certificate_11 (Fin.cases fine_certificate_12 (Fin.cases fine_certificate_13 (Fin.cases fine_certificate_14 (Fin.cases fine_certificate_15 (Fin.cases fine_certificate_16 (Fin.cases fine_certificate_17 (Fin.cases fine_certificate_18 (Fin.cases fine_certificate_19 (Fin.cases fine_certificate_20 (Fin.cases fine_certificate_21 (Fin.cases fine_certificate_22 (Fin.cases fine_certificate_23 (fun r => Fin.elim0 r)))))))))))))))))))))))))

def macroAccepted (r : Fin 24) : List V3 := match r.val with
  | 0 => macroAccepted0
  | 1 => macroAccepted1
  | 2 => macroAccepted2
  | 3 => macroAccepted3
  | 4 => macroAccepted4
  | 5 => macroAccepted5
  | 6 => macroAccepted6
  | 7 => macroAccepted7
  | 8 => macroAccepted8
  | 9 => macroAccepted9
  | 10 => macroAccepted10
  | 11 => macroAccepted11
  | 12 => macroAccepted12
  | 13 => macroAccepted13
  | 14 => macroAccepted14
  | 15 => macroAccepted15
  | 16 => macroAccepted16
  | 17 => macroAccepted17
  | 18 => macroAccepted18
  | 19 => macroAccepted19
  | 20 => macroAccepted20
  | 21 => macroAccepted21
  | 22 => macroAccepted22
  | 23 => macroAccepted23
  | _ => []

def macroRejected (r : Fin 24) : List (V3 × RejectWitness) := match r.val with
  | 0 => macroRejected0
  | 1 => macroRejected1
  | 2 => macroRejected2
  | 3 => macroRejected3
  | 4 => macroRejected4
  | 5 => macroRejected5
  | 6 => macroRejected6
  | 7 => macroRejected7
  | 8 => macroRejected8
  | 9 => macroRejected9
  | 10 => macroRejected10
  | 11 => macroRejected11
  | 12 => macroRejected12
  | 13 => macroRejected13
  | 14 => macroRejected14
  | 15 => macroRejected15
  | 16 => macroRejected16
  | 17 => macroRejected17
  | 18 => macroRejected18
  | 19 => macroRejected19
  | 20 => macroRejected20
  | 21 => macroRejected21
  | 22 => macroRejected22
  | 23 => macroRejected23
  | _ => []

theorem macro_certificates (r : Fin 24) :
    certificateCheck macroSolid (orientedMacro r) (macroAccepted r) (macroRejected r) = true := by
  revert r
  exact (Fin.cases macro_certificate_0 (Fin.cases macro_certificate_1 (Fin.cases macro_certificate_2 (Fin.cases macro_certificate_3 (Fin.cases macro_certificate_4 (Fin.cases macro_certificate_5 (Fin.cases macro_certificate_6 (Fin.cases macro_certificate_7 (Fin.cases macro_certificate_8 (Fin.cases macro_certificate_9 (Fin.cases macro_certificate_10 (Fin.cases macro_certificate_11 (Fin.cases macro_certificate_12 (Fin.cases macro_certificate_13 (Fin.cases macro_certificate_14 (Fin.cases macro_certificate_15 (Fin.cases macro_certificate_16 (Fin.cases macro_certificate_17 (Fin.cases macro_certificate_18 (Fin.cases macro_certificate_19 (Fin.cases macro_certificate_20 (Fin.cases macro_certificate_21 (Fin.cases macro_certificate_22 (Fin.cases macro_certificate_23 (fun r => Fin.elim0 r)))))))))))))))))))))))))

end Chair

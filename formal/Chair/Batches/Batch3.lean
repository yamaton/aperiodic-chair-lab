import Chair.Witnesses
import Chair.Cache

namespace Chair
open Witnesses

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option Elab.async false

theorem fine_certificate_18 :
    certificateCheck fine (orientedFine 18) fineAccepted18 fineRejected18 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_18 :
    certificateCheck macroSolid (orientedMacro 18) macroAccepted18 macroRejected18 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_19 :
    certificateCheck fine (orientedFine 19) fineAccepted19 fineRejected19 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_19 :
    certificateCheck macroSolid (orientedMacro 19) macroAccepted19 macroRejected19 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_20 :
    certificateCheck fine (orientedFine 20) fineAccepted20 fineRejected20 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_20 :
    certificateCheck macroSolid (orientedMacro 20) macroAccepted20 macroRejected20 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_21 :
    certificateCheck fine (orientedFine 21) fineAccepted21 fineRejected21 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_21 :
    certificateCheck macroSolid (orientedMacro 21) macroAccepted21 macroRejected21 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_22 :
    certificateCheck fine (orientedFine 22) fineAccepted22 fineRejected22 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_22 :
    certificateCheck macroSolid (orientedMacro 22) macroAccepted22 macroRejected22 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_23 :
    certificateCheck fine (orientedFine 23) fineAccepted23 fineRejected23 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_23 :
    certificateCheck macroSolid (orientedMacro 23) macroAccepted23 macroRejected23 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

end Chair

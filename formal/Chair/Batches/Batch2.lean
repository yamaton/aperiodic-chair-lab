import Chair.Witnesses
import Chair.Cache

namespace Chair
open Witnesses

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option Elab.async false

theorem fine_certificate_12 :
    certificateCheck fine (orientedFine 12) fineAccepted12 fineRejected12 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_12 :
    certificateCheck macroSolid (orientedMacro 12) macroAccepted12 macroRejected12 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_13 :
    certificateCheck fine (orientedFine 13) fineAccepted13 fineRejected13 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_13 :
    certificateCheck macroSolid (orientedMacro 13) macroAccepted13 macroRejected13 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_14 :
    certificateCheck fine (orientedFine 14) fineAccepted14 fineRejected14 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_14 :
    certificateCheck macroSolid (orientedMacro 14) macroAccepted14 macroRejected14 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_15 :
    certificateCheck fine (orientedFine 15) fineAccepted15 fineRejected15 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_15 :
    certificateCheck macroSolid (orientedMacro 15) macroAccepted15 macroRejected15 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_16 :
    certificateCheck fine (orientedFine 16) fineAccepted16 fineRejected16 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_16 :
    certificateCheck macroSolid (orientedMacro 16) macroAccepted16 macroRejected16 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_17 :
    certificateCheck fine (orientedFine 17) fineAccepted17 fineRejected17 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_17 :
    certificateCheck macroSolid (orientedMacro 17) macroAccepted17 macroRejected17 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

end Chair

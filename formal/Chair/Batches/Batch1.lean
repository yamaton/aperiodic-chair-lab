import Chair.Witnesses
import Chair.Cache

namespace Chair
open Witnesses

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option Elab.async false

theorem fine_certificate_6 :
    certificateCheck fine (orientedFine 6) fineAccepted6 fineRejected6 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_6 :
    certificateCheck macroSolid (orientedMacro 6) macroAccepted6 macroRejected6 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_7 :
    certificateCheck fine (orientedFine 7) fineAccepted7 fineRejected7 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_7 :
    certificateCheck macroSolid (orientedMacro 7) macroAccepted7 macroRejected7 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_8 :
    certificateCheck fine (orientedFine 8) fineAccepted8 fineRejected8 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_8 :
    certificateCheck macroSolid (orientedMacro 8) macroAccepted8 macroRejected8 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_9 :
    certificateCheck fine (orientedFine 9) fineAccepted9 fineRejected9 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_9 :
    certificateCheck macroSolid (orientedMacro 9) macroAccepted9 macroRejected9 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_10 :
    certificateCheck fine (orientedFine 10) fineAccepted10 fineRejected10 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_10 :
    certificateCheck macroSolid (orientedMacro 10) macroAccepted10 macroRejected10 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_11 :
    certificateCheck fine (orientedFine 11) fineAccepted11 fineRejected11 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_11 :
    certificateCheck macroSolid (orientedMacro 11) macroAccepted11 macroRejected11 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

end Chair

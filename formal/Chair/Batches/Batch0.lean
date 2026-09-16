import Chair.Witnesses
import Chair.Cache

namespace Chair
open Witnesses

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option Elab.async false

theorem fine_certificate_0 :
    certificateCheck fine (orientedFine 0) fineAccepted0 fineRejected0 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_0 :
    certificateCheck macroSolid (orientedMacro 0) macroAccepted0 macroRejected0 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_1 :
    certificateCheck fine (orientedFine 1) fineAccepted1 fineRejected1 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_1 :
    certificateCheck macroSolid (orientedMacro 1) macroAccepted1 macroRejected1 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_2 :
    certificateCheck fine (orientedFine 2) fineAccepted2 fineRejected2 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_2 :
    certificateCheck macroSolid (orientedMacro 2) macroAccepted2 macroRejected2 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_3 :
    certificateCheck fine (orientedFine 3) fineAccepted3 fineRejected3 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_3 :
    certificateCheck macroSolid (orientedMacro 3) macroAccepted3 macroRejected3 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_4 :
    certificateCheck fine (orientedFine 4) fineAccepted4 fineRejected4 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_4 :
    certificateCheck macroSolid (orientedMacro 4) macroAccepted4 macroRejected4 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

theorem fine_certificate_5 :
    certificateCheck fine (orientedFine 5) fineAccepted5 fineRejected5 = true := by
  simp only [orientedFine, fine_eq_cached]
  decide +kernel

theorem macro_certificate_5 :
    certificateCheck macroSolid (orientedMacro 5) macroAccepted5 macroRejected5 = true := by
  simp only [orientedMacro, macro_eq_cached]
  decide +kernel

end Chair

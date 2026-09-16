"""Merge the staged searches, keeping timeouts distinct from disproofs."""

from collections import Counter
import json
from pathlib import Path


def run():
    out = Path(__file__).parent / "artifacts"
    refinements = {}
    for filename in ("dipole_refinement.json", "sat_refinement.json"):
        for case in json.loads((out / filename).read_text()):
            if case["outcome"] != "unresolved":
                refinements[tuple(case["tile"])] = case["outcome"]
    families = []
    totals = Counter()
    for filename in ("port_search.json", "keyed_search.json", "dipole_search.json"):
        report = json.loads((out / filename).read_text())
        final = Counter()
        for case in report["catalog"]:
            outcome = case["outcome"]
            if filename == "dipole_search.json" and outcome == "unresolved":
                outcome = refinements.get(tuple(case["tile"]), "unresolved")
            final[outcome] += 1
        totals.update(final)
        families.append({"source": filename, "tested": len(report["catalog"]), "final_classification": dict(final)})
    assert totals["unresolved"] == 0
    assert sum(totals.values()) == 54144
    summary = {"achievement": "No strongly aperiodic monotile found.",
               "scope": "Three explicit keyed-cube matching models on a common cubic grid, 24 proper rotations.",
               "important_limit": "No-open-patch verdicts do not rule out unaligned Euclidean tilings of a physical solid.",
               "families": families, "total_tested": sum(totals.values()),
               "periodic_counterexamples": sum(n for k, n in totals.items() if k.startswith("periodic_")),
               "no_aligned_tiling": sum(n for k, n in totals.items() if k.startswith("no_open_")),
               "unresolved": totals["unresolved"],
               "positive_theoretical_result": "A synchronized crossed-plane construction is strongly aperiodic as a 121-state matching-rule system, not as a monotile."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    offset_path = out / "offset_verification.json"
    if offset_path.exists():
        offset = json.loads(offset_path.read_text())
        counts = offset["final_classifications"]
        assert offset["status"] == "passed"
        assert counts.get("unresolved", 0) == 0
        combined = {
            "achievement": "No strongly aperiodic monotile found.",
            "first_pass": "summary.json",
            "second_pass": "offset_verification.json",
            "designs_analyzed": summary["total_tested"] + offset["new_family_total"],
            "new_designs_excluded_by_coarse_model": counts["inherited_no_open_3"],
            "periodic_counterexamples": summary["periodic_counterexamples"] + sum(
                n for k, n in counts.items() if k.startswith("periodic_")),
            "no_aligned_tiling": summary["no_aligned_tiling"] + sum(
                n for k, n in counts.items() if "no_open_" in k),
            "unresolved_in_tested_grid_families": 0,
            "important_limit": summary["important_limit"],
            "fusion_experiments": ["chair_fusion.json", "chair_clusters.json"],
        }
        assert combined["designs_analyzed"] == combined["periodic_counterexamples"] + combined["no_aligned_tiling"]
        if (out / "open_chair_verification.json").exists():
            checked = json.loads((out / "open_chair_verification.json").read_text())
            assert checked["status"] == "passed"
            combined["further_fusion_experiments"] = [
                "open_chair_clusters_4_level4.json", "fused_chair_level3.json",
                "open_chair_verification.json"]
            combined["further_fusion_scope"] = (
                "Whole-chair cluster groupings and fixed whole-cross attachments; "
                "these exclusions do not classify general monotiles.")
        if (out / "eight_chair_verification.json").exists():
            checked = json.loads((out / "eight_chair_verification.json").read_text())
            assert checked["status"] == "passed"
            combined["eight_chair_rooted_placements"] = checked["rooted_eight_clusters"]
            combined["eight_chair_occurrence_survivors"] = checked["surviving_occurrence_classes"]
            combined["eight_chair_new_cover_shapes"] = 0
            combined["eight_chair_report"] = "eight_chair_verification.json"
        if (out / "chair_recut_hierarchy_verification.json").exists():
            recut = json.loads((out / "chair_recut_hierarchy_verification.json").read_text())
            assert recut["status"] == "passed"
            combined["achievement"] = (
                "Curved recut-chair research proposal: verified grid hierarchy and a proposed "
                "analytic grid-enforcement argument; the full construction requires mathematical review.")
            combined["recut_chair_proposal"] = {
                "report": "../RECUT_CHAIR.md",
                "hierarchy_verification": "chair_recut_hierarchy_verification.json",
                "exact_geometry": "recut_chair_exact.json",
                "viewer": "recut-chair.html",
                "pose_templates_enumerated": 6561,
                "matching_profile_classes": 3,
                "rejected_by_periodic_witness": 2,
                "candidate_profile_index": 1,
                "convention": "Proper rotations of one physical handedness",
                "limit": "No external mathematical review; approximate meshes are not certified aperiodic."}
            reflection_path = out.parent / "audit/reflection_verification.json"
            if reflection_path.exists():
                reflected = json.loads(reflection_path.read_text())
                assert reflected["status"] == "passed"
                assert reflected["single_cap_frame_correspondences_by_determinant"]["-1"] == 0
                manifest = json.loads((out.parent / "audit/frozen_v1/manifest.json").read_text())
                assert reflected["candidate_sha256"] == manifest["candidate_sha256"]
                combined["recut_chair_proposal"].update(
                    convention="Arbitrary Euclidean congruent copies; proposed cap argument forces one handedness throughout each tiling",
                    reflection_verification="../audit/reflection_verification.json",
                    followup_record="../FOLLOWUP_REFLECTIONS.md",
                    review_note="../REVIEW_NOTE.md")
        (out / "research_summary.json").write_text(json.dumps(combined, indent=2) + "\n")
        print(json.dumps(combined, indent=2))


if __name__ == "__main__":
    run()

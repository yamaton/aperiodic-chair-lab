"""Reproduce the Lean milestone; run with uv from the repository root.

Requires the pinned Lean toolchain (via elan, or --lake /path/to/lake).
Python checks the source bridge and an existing independent contact table.
Lean checks all proof obligations; its final axiom dependencies are audited.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from generate_input import SHA256

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(args, cwd=HERE):
    output = []
    with subprocess.Popen(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line, end="", flush=True)
            output.append(line)
        returncode = process.wait()
    if returncode:
        raise subprocess.CalledProcessError(returncode, args, output="".join(output))
    return "".join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lake", default="lake")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    lake = shutil.which(args.lake)
    if lake is None:
        parser.error("lake not found; install the pinned toolchain or pass --lake")
    run([sys.executable, str(HERE / "generate_input.py"), "--check"])
    run([sys.executable, str(HERE / "generate_certificates.py"), "--check"])
    run([sys.executable, str(HERE / "generate_grouping.py"), "--check"])
    version = run([lake, "env", "lean", "--version"]).strip()
    assert "version 4.34.0," in version, f"Unexpected Lean version: {version}"
    run([lake, "build"])
    audit = run([lake, "env", "lean", "Audit.lean"])
    standard_axioms = {"propext", "Classical.choice", "Quot.sound"}
    dependencies = {}
    for name, names in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit):
        dependencies[name] = [name.strip() for name in names.split(",") if name.strip()]
        assert set(dependencies[name]) <= standard_axioms, (name, dependencies[name])
    for name in re.findall(r"'([^']+)' does not depend on any axioms", audit):
        dependencies[name] = []
    expected_theorems = {
        "Chair.macro_contact_recurrence", "Chair.macro_contact_even",
        "Chair.macro_boundary_exact", "Chair.fine_assignment_exact",
        "Chair.child_pairs_compatible", "Chair.fine_accepted_count",
        "Chair.macro_accepted_count", "Chair.accepted_lists_distinct",
        "Chair.GridMotion.cell_comp", "Chair.GridMotion.contact_covariant",
        "Chair.placed_fine_boundary", "Chair.LegalTiling.move",
        "Chair.LegalTiling.exposed_face_has_neighbor",
        "Chair.LegalTiling.touching_contact_accepted",
        "Chair.LegalTiling.exposed_face_neighbor_accepted",
        "Chair.placed_macro_contact_recurrence",
        "Chair.Occurrences.valid_occurrences",
        "Chair.LocalGrouping.excluded_absent",
        "Chair.LocalGrouping.trigger_forces_central",
        "Chair.LocalGrouping.exceptional_axial",
        "Chair.GroupingData.group_matches_frozen",
        "Chair.GroupingData.group_nodup",
        "Chair.GroupingData.group_length",
        "Chair.ChairGrouping.universal_grouping",
        "Chair.ChairGrouping.parent_fiber",
        "Chair.ChairGrouping.partition_unique",
        "Chair.ChairGrouping.group_partition_unique",
        "Chair.ChairGrouping.group_has_eight_distinct_tiles",
        "Chair.ChairGrouping.center_iff_group_occurs",
        "Chair.ChairGrouping.parent_map_unique",
        "Chair.ChairGrouping.parent_covariant",
        "Chair.LegalTiling.assemble", "Chair.placed_macro_boundary",
        "Chair.integer_grid_connected", "Chair.LegalSolidTiling.macro_common_parity",
        "Chair.placed_macro_support", "Chair.sample_owned_iff",
        "Chair.contact_deflate", "Chair.LegalSolidTiling.deflate",
        "Chair.LegalTiling.parent_common_parity", "Chair.LegalTiling.grouping_deflation",
        "Chair.deflateTiling_legal", "Chair.iteratedDeflation_legal",
        "Chair.iteratedDeflation_step",
        "Chair.translationPeriod_iff_moveTiling",
        "Chair.TranslationPeriod.groupCenters", "Chair.TranslationPeriod.deflated",
        "Chair.LegalTiling.period_even", "Chair.LegalTiling.period_halves",
        "Chair.doubling_descent", "Chair.LegalTiling.translation_period_zero",
        "Chair.LegalTiling.translation_stabilizer_trivial",
    }
    assert set(dependencies) == expected_theorems, dependencies

    summary = json.loads((HERE / "certificate_summary.json").read_text())
    exported = {(tuple(t), tuple(v for row in entry["matrix"] for v in row))
                for entry in summary["orientations"] for t in entry["fine_accepted"]}
    independent = json.loads((ROOT / "strong/audit/coordinate_certificate.json").read_text())
    expected = {(tuple(t), tuple(r)) for t, r in independent["legal_contacts"]}
    assert exported == expected and len(exported) == 44
    report = {
        "status": "passed", "lean": version, "candidate_sha256": SHA256,
        "finite_evaluation": "Lean kernel reduction; no native_decide",
        "source_bridge": "Exact rational export, pinned JSON SHA, deterministic regeneration",
        "orientations": 24, "fine_contacts": 44, "macro_contacts": 44,
        "independent_python_contact_table": "all 44 oriented contacts agree",
        "axiom_dependencies": dependencies,
        "lean_source_sha256": {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(HERE.rglob("*.lean")) if ".lake" not in p.parts},
        "scope": "Integral-grid recurrence, unique grouping, legal deflation and exclusion of every nonzero integral translation period of any LegalTiling; not initial tiling existence, full finite symmetry or the physical-solid theorem",
    }
    if args.write_report:
        (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Lean recurrence, grouping, deflation and translation exclusion: all checks passed", flush=True)


if __name__ == "__main__":
    main()

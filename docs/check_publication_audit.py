"""Exercise publication scanning in a disposable Git repository through uv."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    project = Path(__file__).resolve().parents[1]
    scanner = project / "docs/audit_publication.py"
    with tempfile.TemporaryDirectory(prefix="chair-publication-controls-") as tmp:
        root = Path(tmp)

        def git(*args):
            subprocess.run(
                ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
                 "-c", "user.name=Publication audit control",
                 "-c", "user.email=audit@example.invalid", *args],
                cwd=root, check=True, capture_output=True)

        git("init", "--quiet")
        # Deliberately synthetic, never an actual service credential.
        token = "ghp_" + "A" * 40
        (root / "removed.txt").write_text(token + "\n")
        git("add", "removed.txt")
        git("commit", "--quiet", "-m", "Synthetic historical fixture")
        (root / "removed.txt").unlink()
        git("add", "-u")
        git("commit", "--quiet", "-m", "Remove fixture from current tree")
        with zipfile.ZipFile(root / "fixture.zip", "w") as archive:
            archive.writestr("nested.txt", token)
        output = root / "report.json"
        reports = []
        # Run again with an existing absolute output path to check that the
        # scanner excludes its own report from both the scan and digest.
        for _ in range(2):
            subprocess.run(
                ["uv", "run", "--project", str(project), "--locked", "--offline",
                 "python", str(scanner), "--output", str(output)],
                cwd=root, check=True, capture_output=True)
            reports.append(json.loads(output.read_text()))
        report = reports[-1]
        findings = report["suspected_credentials"]
        checks = {
            "removed_historical_token_detected": any(
                f["source"].startswith("git:") and f["source"].endswith(":removed.txt")
                for f in findings),
            "zip_member_token_detected": any(
                f["source"] == "working:fixture.zip!nested.txt" for f in findings),
            "only_expected_rule": len(findings) == 2 and all(
                f["rule"] == "github_token" for f in findings),
            "secret_values_not_reported": token not in output.read_text(),
            "report_excluded_from_inventory": reports[0] == reports[1],
            "no_extraction_failures": not report["extraction_failures_or_limits"],
        }
        if not all(checks.values()):
            raise RuntimeError(f"Publication audit control failure: {checks}")
    evidence = {"status": "passed", "checks": checks,
                "scanner_sha256": hashlib.sha256(scanner.read_bytes()).hexdigest(),
                "control_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (project / "docs/publication_controls.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print("PASS: publication scanner history, archive, redaction and repeatability controls.")


if __name__ == "__main__":
    main()

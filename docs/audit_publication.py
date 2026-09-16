"""Read-only publication inventory; heuristic scanning, not a security guarantee.

Run from the repository root through uv. Git objects, working files, ZIP
members and extracted PDF text are inspected without executing their contents.
Potential secret values and email addresses are never included in the report.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile


RULES = {
    "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "github_token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b",
    "cloud_access_key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "service_token": rb"\b(?:sk-(?:proj-)?[A-Za-z0-9_-]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})\b",
    "credential_in_url": rb"https?://[^\s/:@]{2,}:[^\s/@]{4,}@",
    "credential_assignment": rb'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*["']([^"'\s]{8,})["']''',
}
EXPOSURES = {
    "email_address": rb"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "home_directory": rb"/(?:home|Users)/[^/\s\"<>]+/",
    "temporary_path": rb"/(?:tmp|dev/shm)/",
    "wsl_path": rb"(?:wsl\.localhost|\\\\wsl)",
}
SECRET_RULES = {name: re.compile(pattern) for name, pattern in RULES.items()}
EXPOSURE_RULES = {name: re.compile(pattern) for name, pattern in EXPOSURES.items()}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("docs/publication_audit.json"))
    args = parser.parse_args()
    if Path.cwd().resolve() != Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve():
        parser.error("Run from the repository root.")

    counts: Counter[str] = Counter()
    findings: list[dict] = []
    exposures: dict[str, set[str]] = {name: set() for name in EXPOSURES}
    skipped: list[dict] = []

    def text_scan(data: bytes, source: str) -> None:
        counts["text_payloads_scanned"] += 1
        for name, pattern in SECRET_RULES.items():
            for match in pattern.finditer(data):
                findings.append({"source": source, "rule": name,
                                 "line": data.count(b"\n", 0, match.start()) + 1})
        for name, pattern in EXPOSURE_RULES.items():
            if pattern.search(data):
                exposures[name].add(source)

    def scan(data: bytes, source: str, depth: int = 0) -> None:
        if data.startswith(b"PK\x03\x04"):
            if depth >= 4:
                skipped.append({"source": source, "reason": "archive_depth_limit"})
                return
            counts["zip_payloads_scanned"] += 1
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for item in archive.infolist():
                    if not item.is_dir():
                        scan(archive.read(item), f"{source}!{item.filename}", depth + 1)
            return
        if data.startswith(b"%PDF-"):
            counts["pdf_payloads_scanned"] += 1
            text_scan(data, source + " [raw PDF]")
            result = subprocess.run(["pdftotext", "-", "-"], input=data, capture_output=True)
            if result.returncode:
                skipped.append({"source": source, "reason": "pdf_text_extraction_failed"})
            else:
                text_scan(result.stdout, source + " [PDF text]")
            return
        if b"\0" in data:
            counts["binary_payloads_raw_scanned"] += 1
            text_scan(data, source + " [raw binary]")
        else:
            text_scan(data, source)

    objects: dict[str, str] = {}
    for line in git("rev-list", "--objects", "--all").decode().splitlines():
        oid, _, name = line.partition(" ")
        objects[oid] = name
    checked = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        input="\n".join(objects) + "\n", text=True, capture_output=True, check=True)
    for line in checked.stdout.splitlines():
        oid, kind, size = line.split()
        if kind == "blob":
            counts["reachable_blob_versions"] += 1
            counts["reachable_blob_bytes"] += int(size)
            scan(git("cat-file", "blob", oid), f"git:{oid}:{objects[oid]}")
    commits = git("log", "--all", "--format=%H%n%an <%ae>%n%cn <%ce>%n%B").decode()
    text_scan(commits.encode(), "git:commit_metadata_and_messages")
    identities = git("log", "--all", "--format=%ae%n%ce").decode().splitlines()

    # Include pending publication edits. The report itself is excluded to avoid
    # a self-referential hash and repeated matches from its inventory strings.
    files = git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")
    inventory: list[tuple[str, str]] = []
    for raw in sorted(set(files)):
        if not raw:
            continue
        p = Path(raw.decode())
        if p.resolve() == args.output.resolve() or not p.is_file():
            continue
        data = p.read_bytes()
        counts["working_files_scanned"] += 1
        inventory.append((str(p), hashlib.sha256(data).hexdigest()))
        scan(data, f"working:{p}")

    report = {
        "scope": "all locally reachable Git blob versions and commit metadata; tracked and unignored working files; ZIP members; PDF text",
        "head": git("rev-parse", "HEAD").decode().strip(),
        "refs": git("for-each-ref", "--format=%(refname) %(objectname)").decode().splitlines(),
        "reachable_commits": int(git("rev-list", "--count", "--all")),
        "counts": dict(counts),
        "suspected_credentials": findings,
        "exposure_sources": {name: sorted(paths) for name, paths in exposures.items()},
        "commit_email_domains": sorted({s.rsplit("@", 1)[-1] for s in identities if "@" in s}),
        "unique_commit_email_count": len(set(identities)),
        "extraction_failures_or_limits": skipped,
        "working_inventory_sha256": hashlib.sha256(json.dumps(inventory).encode()).hexdigest(),
        "scanner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "limitations": [
            "Heuristic token patterns cannot prove absence of secrets or sensitive information.",
            "No OCR, steganography detection, or decoding of embedded base64 image contents.",
            "Unreachable Git objects, reflogs, ignored files and external GitHub state are outside this scan.",
            "An object's displayed path is a representative path from git rev-list, not its complete path history.",
            "Local paths and public scholarly contact addresses require contextual review, not automatic deletion.",
        ],
    }
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"report": str(args.output), "counts": dict(counts),
                      "suspected_credentials": len(findings), "extraction_failures_or_limits": len(skipped)}))


if __name__ == "__main__":
    main()

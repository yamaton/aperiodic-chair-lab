# Publication preparation review

*16 September 2026. Prepared locally. Repository visibility remains private.*

## Result

The public-facing documentation and license notices are prepared. The current
presentation acknowledges the exact Chair44 overlap, distinguishes the scope
of each proof, discloses substantial AI assistance, and leads with comparison,
reproduction, teaching and physical experiments. The frozen evidence and Git
history have not been rewritten.

**One personal-information decision remains before publication:** all ten
existing commits use a personal Gmail author/committer address. The address
is not repeated in this report. Making the current history public would
expose it; changing the current Git configuration alone would not alter old
commits. The maintainer should choose whether to retain that identity or
authorize replacing it with a GitHub no-reply identity before publication.
A rewrite would change commit IDs and require reconciling the remote history
and documents that cite those IDs. No such rewrite has been performed.

## Changes prepared

- Rewrote the README around current scope, Chair44 attribution, completed
  grid formalization, reproducibility, the tutorial, and future physical work.
- Added [provenance](PROVENANCE.md), including AI involvement, the meaning
  of independent agent checks, and limits of discovery chronology.
- Added [licensing scope](../LICENSING.md): MIT for project code and original
  machine-readable data; CC BY 4.0 for project prose, figures and model exports.
- Added [third-party notices](../THIRD_PARTY_NOTICES.md), retaining Tsiokos's
  CC BY 4.0 terms on papers and source-derived evidence and the applicable
  BSD notice for Pandoc templates. Dependencies retain their own licenses.
- Added a [historical-material guide](HISTORICAL_MATERIAL.md) and current
  context notices on proposal entry points. The unsent draft now points
  to the intended recipient's public profile instead of repeating an address.
- Added a repeatable, read-only [inventory scanner](audit_publication.py).

The old inquiry has been clearly retired from the current presentation.
It has not been rewritten into a new outreach request: no outreach is part
of this publication preparation.

## Reviewed history and files

The local scan covers all ten locally reachable commits through
`3984e42c612f20808ff65598aa42b226463aa083`, including **331 unique Git blob
versions** (119,860,188 bytes), commit messages and author/committer metadata.
It also scans the working files, including this preparation, and recursively
examines ZIP members and extracted PDF text. The saved
[audit result](publication_audit.json) lists counts and exposure locations
without copying potential secret values or contact addresses into the report.

The targeted credential patterns found **no suspected credentials**. Patterns
cover private-key markers, common GitHub/service/cloud tokens, credentials in
URLs, and quoted credential assignments. Synthetic controls detected a token
present only in an earlier commit and a token inside a ZIP; neither token
value appeared in the generated report. The controls also verify that an
existing report is excluded from its own scan and digest. Their
[script](check_publication_audit.py) and [results](publication_controls.json)
are preserved.

This is a bounded heuristic review, not a guarantee that every possible
secret format or sensitive item has been found. It does not inspect
unreachable objects, reflogs, ignored local environments, image text via
OCR, or hidden data encoded in media. Historical image contents are project
geometry and plots, not a substitute for such a scan.

## Exposure findings and disposition

| Finding | Disposition |
|---|---|
| Personal Gmail address in all ten commits | Maintainer decision before publication; history preserved |
| Publicly sourced Goodman-Strauss contact address in the old draft and record | Current draft/navigation use the public profile; historical record and old revisions retain the public address; no contact or endorsement implied |
| Local username and old workspace path in `strong/artifacts/review_brief_firefox.json` | Retained as exact historical verification evidence; it discloses a machine username and folder layout |
| Temporary paths in handoff, proof reports, receipts and logs | Retained as reproduction context; portable commands explain temporary checkout/toolchain paths |
| Old proposal claims and “no duplicate identified” assessments | Superseded by current-context notices and the historical guide; frozen packets remain unchanged |
| Third-party PDFs and source-derived release output | Preserved with source/version attribution, license terms and existing checksums |

Removing a line from a current file does not remove it from Git history.
The changes here are editorial context and current-page cleanup, not a claim
that historical personal information has been erased.

## GitHub state reviewed

Read-only API checks found the repository **private**, with one branch,
`main`, pointing to the same audited tutorial commit, no tags, no Actions
runs and no Actions artifacts. The [snapshot](publication_github.json)
records that observation. Unlike older handoff entries, the remote now
contains the tutorial commit; this preparation did not push it.

GitHub notes that public repositories can be forked and that making the
original private again does not make existing public forks private.
Actions history and logs also become visible on publication; none existed
at this check. [GitHub visibility documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)

## Reproduce this review

From the repository root:

```sh
uv run --locked python docs/audit_publication.py
uv run --locked python docs/check_publication_audit.py
uv run --locked python strong/review/verify_package.py --hashes-only
```

The scanner requires Git and `pdftotext`. It reads repository material but
does not execute downloaded source. The JSON is a snapshot: rerun it if
files or reachable history change. Its working-file digest excludes the
report itself. Review its findings rather than treating an empty list of
matched token patterns as authorization to publish.

Only the current documentation, notices and audit tool are being changed.
Our Lean sources, frozen candidate, old PDF/HTML/ZIP packet, numerical
witnesses and build logs remain intact. No new mathematical test result is
claimed. Publication preparation does not change repository visibility,
send messages, or claim external review.

Validation checked 269 local links in changed/new Markdown and compared
128 frozen, evidence and formal-development files byte-for-byte with HEAD.
The frozen candidate/proposal hash verifier passed. Existing proof builds
were not repeated for these documentation and audit-tool changes.

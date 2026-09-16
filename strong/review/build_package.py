"""Build a bounded, linked review archive and PDF/HTML brief; send nothing."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'strong/artifacts'
LINK = re.compile(r'(\]\()([^)]+)(\))')
CSS = '''
body {max-width: 850px; margin: 3rem auto; padding: 0 1.4rem; color: #172737;
font: 17px/1.6 Georgia, serif; background: #fcfcfa;}
h1,h2,h3 {font-family: system-ui,sans-serif; line-height: 1.25;}
h1 {font-size: 2rem;} h2 {margin-top: 2rem; font-size: 1.4rem;}
a {color: #075984;} table {border-collapse: collapse; width:100%;}
th,td {border-bottom:1px solid #ccd4da; padding:.5rem; text-align:left;}
pre {padding:1rem; background:#edf1f3; overflow:auto;}
code {font-size:.85em; overflow-wrap:anywhere;} img {max-width:100%;}
.equation {overflow-x:auto; max-width:100%; padding:1rem 0;}
math[display="block"] {min-width:max-content;}
@media print {body {max-width:none; margin:0; font-size:11pt;} h2 {break-after:avoid;}}
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_target(source, link):
    if '://' in link or link.startswith(('#', 'mailto:', 'data:')):
        return None
    clean = link.split('#')[0]
    # Archived proposal's documented historical relative-link base.
    base = ROOT / 'strong' if source == ROOT / 'strong/audit/frozen_v1/proposal.md' else source.parent
    target = (base / clean).resolve()
    assert target.is_relative_to(ROOT), (source, link)
    return target


def source_files():
    seeds = [HERE / 'BRIEF.md', HERE / 'DEPENDENCY_AUDIT.md', ROOT / 'strong/REVIEW_NOTE.md',
             HERE / 'verify_package.py', ROOT / 'pyproject.toml', ROOT / 'uv.lock',
             OUT / 'review_reproduction.json']
    seeds += list((ROOT / 'strong/audit').glob('*.py'))
    seeds += list((ROOT / 'strong/audit/frozen_v1').glob('*'))
    seeds += [ROOT / 'strong/audit/orientation_information.json', ROOT / 'strong/audit/face_motifs.json',
              ROOT / 'strong/audit/periodic_ablation_verification.json',
              ROOT / 'strong/audit/motif_grouping_verification.json']
    included = set()
    while seeds:
        source = seeds.pop().resolve()
        if source in included:
            continue
        assert source.is_file(), source
        included.add(source)
        if source.suffix == '.md':
            for _, link, _ in LINK.findall(source.read_text()):
                target = local_target(source, link)
                if target:
                    assert target.exists(), (source, link)
                    seeds.append(target)
    return included


def rewrite_brief(output_base):
    source = HERE / 'BRIEF.md'
    def replace(match):
        prefix, link, suffix = match.groups()
        target = local_target(source, link)
        if target is None:
            return match.group(0)
        anchor = '#'+link.split('#', 1)[1] if '#' in link else ''
        return prefix+Path(os.path.relpath(target, output_base)).as_posix()+anchor+suffix
    return LINK.sub(replace, source.read_text())


def contain_equations(path):
    # Firefox's native MathML needs an HTML overflow container for wide
    # display equations. Keep the formula readable by horizontal scrolling.
    text = path.read_text()
    text, count = re.subn(r'<p>(<math display="block".*?</math>)</p>',
                         r'<div class="equation">\1</div>', text, flags=re.DOTALL)
    assert count > 0
    path.write_text(text)


def run():
    assert shutil.which('pandoc') and shutil.which('pdflatex'), 'Building requires pandoc and pdflatex.'
    candidate_hash = digest(ROOT / 'strong/audit/frozen_v1/candidate.json')
    assert candidate_hash == json.loads((ROOT / 'strong/audit/frozen_v1/manifest.json').read_text())['candidate_sha256']
    reproduced = json.loads((OUT / 'review_reproduction.json').read_text())
    assert reproduced['status'] == 'passed' and reproduced['candidate_sha256'] == candidate_hash
    assert len(reproduced['checks']) == 6
    assert all(item['exit_code'] == 0 and digest(ROOT / item['script']) == item['script_sha256']
               for item in reproduced['checks'])
    included = source_files()
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='chair-package-') as temporary:
        work = Path(temporary)
        stage = work / 'review'
        stage.mkdir()
        for source in included:
            target = stage / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        css = work / 'review.css'
        css.write_text(CSS)
        brief = stage / 'START_HERE.md'
        brief.write_text(rewrite_brief(ROOT))
        subprocess.run(['pandoc', str(brief), '--standalone', '--embed-resources', '--math-method=mathml',
                        '--css', str(css), '-o', str(stage / 'START_HERE.html')], cwd=stage, check=True)
        contain_equations(stage / 'START_HERE.html')
        subprocess.run(['pandoc', str(brief), '--standalone', '--pdf-engine=pdflatex',
                        '-V', 'geometry:margin=22mm', '-V', 'fontsize=10pt',
                        '-o', str(stage / 'review-brief.pdf')], cwd=stage, check=True)
        # Workspace preview needs paths relative to strong/artifacts instead.
        preview = work / 'preview.md'
        preview.write_text(rewrite_brief(OUT))
        subprocess.run(['pandoc', str(preview), '--standalone', '--embed-resources', '--math-method=mathml',
                        '--css', str(css), '-o', str(OUT / 'review-brief.html')], cwd=ROOT, check=True)
        contain_equations(OUT / 'review-brief.html')
        shutil.copyfile(stage / 'review-brief.pdf', OUT / 'review-brief.pdf')
        (stage / 'README.md').write_text('''# Recut-chair review package

Open START_HERE.html or review-brief.pdf. The HTML uses native MathML and
has no external assets. Original source paths are preserved.

To reproduce the four primary checks and two periodic controls:

```sh
uv run --locked python strong/review/verify_package.py
```

Python 3.13+ and uv are needed; dependencies may download on first use.
The runner checks the file manifest, then works in a temporary copy.
Use --hashes-only to verify the archive without running calculations.

The defining solid is strong/audit/frozen_v1/candidate.json. The viewer and
STL are illustrations. The archived proposal preserves its original bytes
and historical proper-copy scope; its relative links use strong/ as base.
Current scope and reflection/grouping extensions are stated in the brief.

The preparation run is recorded in strong/artifacts/review_reproduction.json.
It reports six successful checks; it does not establish the written global
geometry arguments. The source archive contains a checksum manifest for
every supplied file except the manifest itself.

This is an AI-assisted research proposal requiring mathematical review.
No external endorsement or novelty determination is claimed.
''')
        manifest = {'format': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
                    'candidate_sha256': candidate_hash,
                    'scope': 'Original twelve-depth candidate; exact geometry only; finite-group property proposed, external review pending.',
                    'files': {p.relative_to(stage).as_posix(): digest(p) for p in sorted(stage.rglob('*')) if p.is_file()}}
        (stage / 'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
        archive = OUT / 'review-goodman-strauss-v1.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            for p in sorted(stage.rglob('*')):
                if p.is_file():
                    zip_file.write(p, p.relative_to(stage).as_posix())
        assert zipfile.ZipFile(archive).testzip() is None
        result = {'status': 'built', 'candidate_sha256': candidate_hash,
                  'archive': archive.relative_to(ROOT).as_posix(), 'archive_sha256': digest(archive),
                  'archive_bytes': archive.stat().st_size, 'manifest_files': len(manifest['files']),
                  'brief_pdf_sha256': digest(OUT / 'review-brief.pdf'),
                  'brief_html_sha256': digest(OUT / 'review-brief.html'),
                  'limit': 'Build success only; reproduce and inspect before treating package as checked.'}
        (OUT / 'review_package_build.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()

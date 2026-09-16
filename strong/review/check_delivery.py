"""Extract the prepared archive and check its actual recipient workflow."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'strong/artifacts'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src'):
                self.links.append(value)


def run():
    build = json.loads((OUT / 'review_package_build.json').read_text())
    archive = ROOT / build['archive']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == build['archive_sha256']
    with tempfile.TemporaryDirectory(prefix='chair-delivery-') as temporary:
        extracted = Path(temporary)
        with zipfile.ZipFile(archive) as source:
            assert source.testzip() is None
            assert all((extracted / name).resolve().is_relative_to(extracted) for name in source.namelist())
            source.extractall(extracted)
        manifest = json.loads((extracted / 'PACKAGE_MANIFEST.json').read_text())
        checked_links = 0
        for name in manifest['files']:
            file = extracted / name
            if file.suffix == '.md':
                links = re.findall(r'\]\(([^)]+)\)', file.read_text())
            elif file.suffix == '.html' and name == 'START_HERE.html':
                parser = Links(); parser.feed(file.read_text()); links = parser.links
            else:
                continue
            base = extracted / 'strong' if name == 'strong/audit/frozen_v1/proposal.md' else file.parent
            for link in links:
                if '://' in link or link.startswith(('#', 'data:', 'mailto:')):
                    continue
                target = (base / link.split('#')[0]).resolve()
                assert target.is_relative_to(extracted) and target.exists(), (name, link)
                checked_links += 1
        reproduced = extracted / 'recipient-run.json'
        completed = subprocess.run([sys.executable, str(extracted / 'strong/review/verify_package.py'),
                                    '--report', str(reproduced)], cwd=extracted, text=True,
                                   capture_output=True, timeout=300)
        assert completed.returncode == 0, completed.stdout+'\n'+completed.stderr
        result = json.loads(reproduced.read_text())
        assert result['status'] == 'passed' and result['archive_integrity']['present']
        assert len(result['checks']) == 6
        (OUT / 'review_recipient_reproduction.json').write_text(json.dumps(result, indent=2)+'\n')
        subprocess.run(['node', str(ROOT / 'strong/review/verify_brief_firefox.cjs'),
                        str(OUT / 'review-brief.html'), str(extracted / 'START_HERE.html')],
                       cwd=ROOT, check=True, timeout=90)
        # The supplied files remain unchanged after the temporary-copy runner.
        for name, expected in manifest['files'].items():
            assert hashlib.sha256((extracted / name).read_bytes()).hexdigest() == expected
        pdf_info = subprocess.check_output(['pdfinfo', str(OUT / 'review-brief.pdf')], text=True)
        pages = int(re.search(r'^Pages:\s+(\d+)', pdf_info, re.MULTILINE).group(1))
        text = subprocess.check_output(['pdftotext', str(OUT / 'review-brief.pdf'), '-'], text=True)
        assert 'not an established theorem' in text and 'AI assistance' in text
        report = {'status': 'passed', 'archive_sha256': build['archive_sha256'],
                  'candidate_sha256': build['candidate_sha256'], 'manifest_files_verified': len(manifest['files']),
                  'local_document_links_checked': checked_links, 'recipient_checks_passed': len(result['checks']),
                  'supplied_files_unchanged': True, 'brief_pdf_pages': pages,
                  'pdf_text_extraction': 'passed', 'offline_firefox': 'passed',
                  'external_review_received': False, 'outreach_sent': False}
        (OUT / 'review_delivery_verification.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run()

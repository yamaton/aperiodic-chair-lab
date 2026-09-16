"""Reproduce the primary audit in a temporary copy, preserving supplied files.

Run from a repository or extracted review archive with uv. No project helper
is imported here. This runner checks execution and specified finite outputs;
it is not another mathematical implementation of the underlying lemmas.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
CHECKS = [
    ('coordinates and hierarchy', 'verify_from_coordinates.py', 'coordinate_verification.json'),
    ('local cap identities', 'verify_caps.py', 'cap_verification.json'),
    ('reflections', 'check_reflections.py', 'reflection_verification.json'),
    ('local parent rule', 'motif_grouping.py', 'motif_grouping_verification.json'),
    ('plain-chair periodic control', 'check_periodic_chair.py', 'periodic_chair_check.json'),
    ('altered-solid periodic control', 'verify_periodic_ablation.py', 'periodic_ablation_verification.json'),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest():
    path = ROOT / 'PACKAGE_MANIFEST.json'
    if not path.exists():
        return {'present': False, 'scope': 'Working repository; frozen inputs checked separately.'}
    manifest = json.loads(path.read_text())
    for name, expected in manifest['files'].items():
        file = (ROOT / name).resolve()
        assert file.is_relative_to(ROOT) and file.is_file(), name
        assert digest(file) == expected, f'Package file differs: {name}'
    return {'present': True, 'files_checked': len(manifest['files']), 'status': 'passed'}


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--hashes-only', action='store_true')
    args = parser.parse_args()
    if sys.flags.optimize:
        raise SystemExit('Assertions must be enabled; do not use Python -O or PYTHONOPTIMIZE.')
    frozen = ROOT / 'strong/audit/frozen_v1'
    manifest = json.loads((frozen / 'manifest.json').read_text())
    candidate_hash = digest(frozen / 'candidate.json')
    assert candidate_hash == manifest['candidate_sha256']
    assert digest(frozen / 'proposal.md') == manifest['archived_proposal_sha256']
    report = {'status': 'passed', 'utc': datetime.now(timezone.utc).isoformat(),
              'candidate_sha256': candidate_hash, 'python': sys.version,
              'archive_integrity': check_manifest(), 'checks': [],
              'limit': 'Reproduction of finite and symbolic checks. Global geometric arguments and novelty still require mathematical review.'}
    if not args.hashes_only:
        # Programs write their normal result files only in this disposable copy.
        with tempfile.TemporaryDirectory(prefix='chair-review-') as temporary:
            work = Path(temporary)
            audit = work / 'strong/audit'
            shutil.copytree(ROOT / 'strong/audit', audit, ignore=shutil.ignore_patterns('__pycache__'))
            for label, script, output in CHECKS:
                started = time.monotonic()
                completed = subprocess.run([sys.executable, str(audit / script)], cwd=work,
                                           text=True, capture_output=True, timeout=180)
                entry = {'check': label, 'script': 'strong/audit/'+script,
                         'script_sha256': digest(audit / script), 'exit_code': completed.returncode,
                         'elapsed_seconds': round(time.monotonic()-started, 3),
                         'stdout': completed.stdout, 'stderr': completed.stderr}
                report['checks'].append(entry)
                if completed.returncode:
                    report['status'] = 'failed'
                    break
                result = json.loads((audit / output).read_text())
                assert result['status'] == 'passed' and result['candidate_sha256'] == candidate_hash
                entry['result'] = result
                print(f'Passed: {label}', flush=True)
            if report['status'] == 'passed':
                coordinate, caps, mirrors, parent, periodic, altered = [x['result'] for x in report['checks']]
                assert (coordinate['geometric_contacts'], coordinate['legal_contacts'], coordinate['complete_stars']) == (1194, 44, 33)
                assert (coordinate['macro_geometric_contacts'], coordinate['macro_legal_contacts']) == (6801, 44)
                assert coordinate['deflation_preserves_grid_and_rules']
                assert caps['volume'] == '7' and caps['matching_frame_correspondences'] == 1536
                assert mirrors['single_cap_frame_correspondences_by_determinant'] == {'1': 1536, '-1': 0}
                assert parent['remaining_contacts'] == 30 and parent['outer_children_select_same_parent'] == 7
                assert parent['remaining_contacts_equal_substitution_closure']
                assert parent['derived_group_coarse_union_is_double_chair']
                assert len(periodic['all_nine_pose_pairs']) == 9
                assert altered['phase_erased_solid']['mismatched_port_incidences'] == 0
                assert altered['original_solid_on_same_placements']['mismatched_port_incidences'] == 480
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, indent=2))
    if report['status'] != 'passed':
        print(report['checks'][-1]['stderr'], file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    run()

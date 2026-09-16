#!/usr/bin/env python3
"""Build an inspected Chair44 checkout using its already installed dependencies.

Run via uv from our repository. This executes the supplied Lean sources; unlike
the finite JSON replays, it is not a data-only check. It does not fetch dependencies
or modify proof sources. Use a disposable copy of the pinned release.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-root', type=Path, required=True)
    parser.add_argument('--lake', type=Path, required=True)
    parser.add_argument('--logs-root', type=Path, required=True)
    args = parser.parse_args()
    project = args.release_root.resolve() / 'lean/R44'
    logs = args.logs_root.resolve()
    logs.mkdir(parents=True, exist_ok=True)
    lake = args.lake.resolve()
    env = dict(os.environ)
    env['PATH'] = str(lake.parent) + os.pathsep + env.get('PATH', '')
    env['MATHLIB_NO_CACHE_ON_UPDATE'] = '1'
    source_paths = sorted(project.glob('R44/**/*.lean')) + [project / 'R44.lean', project / 'lakefile.lean', project / 'lean-toolchain', project / 'lake-manifest.json']
    before = {str(p.relative_to(project)): digest(p) for p in source_paths}
    record = {
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'release_root': str(args.release_root.resolve()),
        'scope': 'Reproduction of supplied Lean sources using installed pinned dependencies, not an independent proof or compiler audit.',
        'source_hashes_before': before,
        'lean_version': subprocess.check_output([str(lake.parent / 'lean'), '--version'], text=True).strip(),
        'dependency_commits': {},
        'phases': [], 'status': 'running',
    }
    for package in json.loads((project / 'lake-manifest.json').read_text())['packages']:
        checkout = project / '.lake/packages' / package['name']
        actual = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != package['rev']:
            raise RuntimeError(f'Dependency revision mismatch: {package["name"]}')
        record['dependency_commits'][package['name']] = actual
    axiom_file = project / 'build_axioms.log'
    if axiom_file.exists():
        record['previous_axiom_log_sha256'] = digest(axiom_file)
        previous = logs / 'axioms-before-build.log'
        if previous.exists():
            raise RuntimeError('Use a fresh logs directory; previous build receipt exists.')
        axiom_file.rename(previous)

    def save():
        record['source_hashes_unchanged'] = all(p.exists() and digest(p) == before[str(p.relative_to(project))] for p in source_paths)
        (logs / 'build_receipt.json').write_text(json.dumps(record, indent=2) + '\n')

    save()
    commands = [('default-build', ['build']), ('discharge-build', ['build', 'R44Discharge']),
                ('fresh-axiom-audit', ['env', 'lean', '-j', '4', 'R44/Axioms.lean'])]
    for name, command in commands:
        started = time.monotonic()
        print('Starting', name, flush=True)
        output = logs / (name + '.log')
        with output.open('w') as stream:
            result = subprocess.run([str(lake), *command], cwd=project, env=env,
                                    stdout=stream, stderr=subprocess.STDOUT)
        record['phases'].append({'name': name, 'command': [str(lake), *command],
                                 'exit_code': result.returncode, 'seconds': time.monotonic() - started,
                                 'log': output.name, 'sha256': digest(output)})
        if result.returncode:
            record['status'] = 'failed'
            save()
            print('Failed', name, 'exit', result.returncode, flush=True)
            raise SystemExit(result.returncode if result.returncode > 0 else 1)
        save()
    if not axiom_file.exists():
        raise RuntimeError('Successful commands did not produce a fresh axiom log.')
    text = axiom_file.read_text()
    lines = [line for line in text.splitlines() if line.startswith("'R44.r44_einstein' ")]
    if len(lines) != 1 or 'sorryAx' in text:
        raise RuntimeError('Missing final theorem audit or sorryAx dependency.')
    (logs / 'axioms-reproduced.log').write_text(text)
    record['final_theorem_axiom_line'] = lines[0]
    record['axiom_log_sha256'] = digest(axiom_file)
    record['status'] = 'passed'
    record['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    if not record['source_hashes_unchanged']:
        raise RuntimeError('Proof sources changed during reproduction.')
    print('Build and fresh axiom audit passed.', flush=True)


if __name__ == '__main__':
    main()

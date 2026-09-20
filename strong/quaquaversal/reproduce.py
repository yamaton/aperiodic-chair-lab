"""Replay the current research checkpoint, including its expected failures.

Run: uv run --locked python strong/quaquaversal/reproduce.py
This is a finite reproduction command, not an unattended discovery loop.
"""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
PREFIX = 'strong/quaquaversal/'
ARTIFACTS = PREFIX+'artifacts/'

COMMANDS = [
    ['verify_geometry.py'],
    ['polynomial_rules.py'],
    ['periodic_obstruction.py'],
    ['reflected_search.py'],
    ['reflected_controls.py'],
    ['reflected_second_level.py'],
    ['refine_vertices.py'],
    ['refine_panels.py'],
    ['audit_panels.py'],
    ['refine_panels.py','--seed-audit',ARTIFACTS+'panel_audit.json','--output',ARTIFACTS+'panel_refinement_v2.json'],
    ['audit_panels.py','--input',ARTIFACTS+'panel_refinement_v2.json','--output',ARTIFACTS+'panel_audit_v2.json'],
    ['piecewise_search.py'],
    ['piecewise_deeper.py'],
    ['piecewise_periodic_grid.py'],
    ['contact_atlas.py'],
    ['atlas_periodic_reflections.py'],
    ['atlas_stars.py'],
    ['star_language.py'],
    ['closed_stars.py','--sample-level','3','--periodic-level','1'],
    ['closed_stars.py','--sample-level','4','--periodic-level','2'],
    ['closed_contact_atlas.py'],
    ['audit_closed_atlas.py'],
    ['closed_star_language.py'],
    ['audit_star_language.py'],
    ['pointwise_groupoid.py'],
    ['pointwise_groupoid.py','--all','--output',ARTIFACTS+'pointwise_groupoid_all.json'],
    ['audit_pointwise_groupoid.py'],
    ['star_parent_consistency.py'],
    ['parent_star_join.py'],
    ['parent_join_filter.py'],
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit-only',action='store_true',help='Check retained artifacts and hashes without rerunning searches')
    options = parser.parse_args()
    runs = ROOT/'artifacts'/'runs'
    runs.mkdir(exist_ok=True)
    records = []
    for i,args in enumerate([] if options.audit_only else COMMANDS,1):
        command = ['uv','run','--locked','python',PREFIX+args[0],*args[1:]]
        print(f'[{i}/{len(COMMANDS)}] '+ ' '.join(command),flush=True)
        result = subprocess.run(command,cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log = runs/f'{i:02d}_{Path(args[0]).stem}.txt'
        log.write_text(result.stdout)
        records.append(dict(command=command,exit_code=result.returncode,log=str(log.relative_to(ROOT))))
        if result.returncode:
            print(result.stdout,flush=True)
            raise SystemExit(result.returncode)
    checks = 0
    for p in sorted((ROOT/'artifacts').glob('*.json')):
        if p.name in ('reproduction.json','reproduction_hash_audit.json'):
            continue
        data = json.loads(p.read_text())
        for name,expected in data.get('sources',{}).items():
            source = ROOT/name if (ROOT/name).exists() else ROOT/'artifacts'/name
            assert hashlib.sha256(source.read_bytes()).hexdigest() == expected,(p.name,name)
            checks += 1
    def read(name):
        return json.loads((ROOT/'artifacts'/name).read_text())
    assert read('panel_audit.json')['failures']  # Retain the failed first refinement.
    assert not read('panel_audit_v2.json')['failures']
    assert read('reflected_second_level.json')['not_rejected_by_control'] == 0
    assert all(r['witness'] is not None for r in read('piecewise_periodic_grid.json')['results'])
    assert read('contact_atlas.json')['status'] == 'closed'
    assert read('atlas_periodic_reflections.json')['volume_ratio'] == '1'
    assert read('star_language_3_1.json')['periodic_control_uses_only_observed_stars']
    assert read('closed_contact_atlas.json')['status'] == 'closed'
    assert read('closed_contact_audit.json')['dimensions'] == {'0':953,'1':247,'2':91}
    assert read('closed_star_language.json')['status'] == 'closed'
    assert read('closed_star_audit.json')['role_multiplicities'] == {'1':6840}
    assert read('closed_star_audit.json')['periodic_bad_cycle']
    assert read('star_parent_consistency.json')['all_sibling_roles_agree']
    assert read('pointwise_groupoid_audit.json')['families'] == 512
    assert len(read('parent_join_filter.json')['extra_tuples']) == 52485
    receipt = dict(scope='Reproduction of finite research results, including counterexamples; objective remains open',
                   commands=records,input_hash_checks=checks,
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    filename = 'reproduction.json' if records else 'reproduction_hash_audit.json'
    (ROOT/'artifacts'/filename).write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'PASS: {len(records)} commands and {checks} input hashes; expected failures preserved.',flush=True)


if __name__ == '__main__':
    main()

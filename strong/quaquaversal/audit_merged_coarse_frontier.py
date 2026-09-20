"""Verify complete coverage and every unchanged fine domain in a merge."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_arc_frontier_1.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_arc_frontier_1_audit.json')
    args = parser.parse_args()
    raw = json.loads(args.input.read_text())
    arguments = raw['arguments']
    paths = [ROOT/'artifacts'/'coarse_parent_language.json']+[Path(arguments[n]) for n in
             ('fine','fine_audit','poses_source','filter','filter_audit')]
    loaded = {p:json.loads(p.read_text()) for p in dict.fromkeys(paths)}
    coarse,fine,fine_audit,pose_source,filtered,filter_audit = [loaded[p] for p in paths]
    for p in paths:
        assert raw['sources'][p.name] == hashlib.sha256(p.read_bytes()).hexdigest()
    assert fine_audit['sources'][paths[1].name] == hashlib.sha256(paths[1].read_bytes()).hexdigest()
    assert filter_audit['sources'][paths[4].name] == hashlib.sha256(paths[4].read_bytes()).hexdigest()
    assert raw['poses'] == pose_source['poses'] and raw['domain_pool'] == fine['domain_pool']
    by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    active = set(filtered['final_active_stars'])
    seen = set()
    counts = dict(survivor=0,fine_rejection=0,coarse_rejection=0)
    domain_records = 0
    for row in raw['results']:
        i = row['source_index']
        assert i not in seen
        seen.add(i)
        old = fine['results'][i]
        key = row['boundary_index'],row['cover_index']
        assert key == (old['boundary_index'],old['cover_index'])
        if 'domains' not in old:
            assert row['rejection'] == dict(kind='inherited_fine_exclusion',result_index=i)
            counts['fine_rejection'] += 1
        elif by_key[key] not in active:
            assert row['rejection'] == dict(kind='conditional_coarse_star',star=by_key[key])
            counts['coarse_rejection'] += 1
        else:
            assert row['domains'] == old['domains']
            domain_records += len(row['domains'])
            counts['survivor'] += 1
    assert seen == set(range(len(fine['results']))) and counts == raw['status_counts']
    output = dict(scope='Full fine-case coverage and equality of all retained domains after coarse intersection',
                  **counts,domain_records=domain_records,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,args.input,Path(__file__))})
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

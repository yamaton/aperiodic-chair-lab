"""Replay a later unit-cut pass, including fixed-pose prefix validation."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=ROOT/'artifacts'/'coarse_refined_frontier.json')
    parser.add_argument('--catalog',type=Path,default=ROOT/'artifacts'/'choice_cut_catalog_163.json')
    parser.add_argument('--basis',type=Path,default=ROOT/'artifacts'/'expanded_arcs_2_seed.json')
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'choice_cut_pass_2.json')
    parser.add_argument('--changed',type=Path,default=ROOT/'artifacts'/'choice_cut_pass_2_changed.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'choice_cut_pass_2_audit.json')
    args = parser.parse_args()
    paths = [args.source,args.catalog,args.input,args.changed,args.basis]
    source,cuts_data,raw,subset,basis = [json.loads(p.read_text()) for p in paths]
    assert cuts_data['sources'][args.basis.name] == hashlib.sha256(args.basis.read_bytes()).hexdigest()
    assert source['poses'][:len(basis['poses'])] == basis['poses']
    assert raw['poses'] == subset['poses'] == source['poses']
    assert raw['domain_pool'] == subset['domain_pool']
    cuts = [c['antecedents'] for c in cuts_data['cuts']]
    assert all(0 <= t < len(basis['poses']) for cut in cuts for t,s in cut)
    pool = [sum(1<<s for s in ss) for ss in source['domain_pool']]
    out_pool = [sum(1<<s for s in ss) for ss in raw['domain_pool']]
    seen = set()
    removals = changed = rejected = 0
    for ri,row in enumerate(raw['results']):
        si = row['source_index']
        assert si not in seen
        seen.add(si)
        original = source['results'][si]
        assert (row['boundary_index'],row['cover_index']) == (original['boundary_index'],original['cover_index'])
        ds = {t:pool[di] for t,di in original['domains']}
        for ci,t,s in row['choice_reductions']:
            cut = cuts[ci]
            assert (t,s) in [tuple(a) for a in cut]
            assert len({tile for tile,star in cut}) == len(cut)
            assert ds[t] & (1<<s) and ds[t].bit_count() > 1
            assert all(tile in ds and (tile == t or ds[tile] == 1<<star) for tile,star in cut)
            ds[t] ^= 1<<s
            removals += 1
        if 'rejection' in row:
            assert all(ds[t] == 1<<s for t,s in cuts[row['rejection']['cut']])
            rejected += 1
        else:
            assert ds == {t:out_pool[di] for t,di in row['domains']}
            for cut in cuts:
                if all(t in ds and ds[t] & (1<<s) for t,s in cut):
                    assert sum(ds[t].bit_count()>1 for t,s in cut) >= 2
        changed += bool(row['choice_reductions']) or 'rejection' in row
    assert seen == {i for i,r in enumerate(source['results']) if 'domains' in r}
    expected = [dict(r,full_result_index=i) for i,r in enumerate(raw['results'])
                if r['choice_reductions'] or 'rejection' in r]
    assert subset['results'] == expected
    assert subset['status_counts'] == dict(survivor=sum('domains' in r for r in expected),
                                         rejected=sum('rejection' in r for r in expected))
    counts = raw['status_counts']
    assert counts.get('rejected',0) == rejected and counts['survivor'] == len(seen)-rejected
    assert counts['star_removals'] == removals and counts['changed_cases'] == changed
    output = dict(scope='Independent replay of unit-choice reductions and all retained frontier domains',
                  parent_cases=len(seen),parent_rejections=rejected,changed_cases=changed,star_removals=removals,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

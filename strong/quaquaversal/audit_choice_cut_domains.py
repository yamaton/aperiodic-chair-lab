"""Replay every Q024 unit consequence, including all retained domains."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/n for n in ('expanded_arcs_2_seed.json','neighbor_arc_cut_sat.json',
                                         'choice_cut_domains.json','choice_cut_changed_seed.json')]
    source,cuts_data,raw,subset = [json.loads(p.read_text()) for p in paths]
    assert raw['poses'] == subset['poses'] == source['poses']
    assert raw['domain_pool'] == subset['domain_pool']
    cuts = [c['antecedents'] for c in cuts_data['cuts']]
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
    (ROOT/'artifacts'/'choice_cut_domain_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

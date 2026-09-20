"""Losslessly merge audited changed-case arcs into the full parent frontier."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    names = ('choice_cut_domains.json','choice_cut_changed_seed.json','choice_cut_arcs.json',
             'choice_cut_domain_audit.json','choice_cut_arcs_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    full,subset,arcs,unit_audit,arc_audit = [json.loads(p.read_text()) for p in paths]
    assert unit_audit['sources'][paths[0].name] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    assert arc_audit['sources'][paths[2].name] == hashlib.sha256(paths[2].read_bytes()).hexdigest()
    changes = {subset['results'][r['source_index']]['full_result_index']:r for r in arcs['results']}
    pool,ids,results = [],{},[]
    survivors = rejected = changed_domains = 0
    for fi,original in enumerate(full['results']):
        row = changes.get(fi,original)
        assert (row['boundary_index'],row['cover_index']) == (original['boundary_index'],original['cover_index'])
        result = dict(source_index=fi,original_source_index=original['source_index'],
                      boundary_index=row['boundary_index'],cover_index=row['cover_index'])
        if 'domains' not in row:
            result['rejection'] = dict(kind='choice_arc_trace' if fi in changes else 'choice_unit_conflict',result_index=fi)
            rejected += 1
        else:
            original_domains = {t:set(full['domain_pool'][di]) for t,di in original['domains']}
            source_pool = arcs['domain_pool'] if fi in changes else full['domain_pool']
            domains = []
            assert {t for t,di in row['domains']} == set(original_domains)
            for tile,di in row['domains']:
                key = tuple(source_pool[di])
                assert set(key) <= original_domains[tile]
                changed_domains += set(key) != original_domains[tile]
                if key not in ids:
                    ids[key] = len(pool)
                    pool.append(key)
                domains.append((tile,ids[key]))
            result['domains'] = domains
            survivors += 1
        results.append(result)
    output = dict(scope='Full unresolved parent frontier after audited choice-unit and changed-case arc consequences',
                  poses=full['poses'],domain_pool=pool,results=results,
                  status_counts=dict(survivor=survivors,rejected=rejected),arc_narrowed_domains=changed_domains,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'choice_cut_frontier_seed.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(survivors=survivors,rejected=rejected,arc_narrowed_domains=changed_domains)),flush=True)


if __name__ == '__main__':
    main()

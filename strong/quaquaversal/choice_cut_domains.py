"""Apply audited fixed-pose choice cuts to every unresolved parent domain.

Unit propagation removes a star only when every other cut premise is fixed.
Unknown centers never become implicitly present. Record each removal for
independent replay, and provide a changed-only seed for further arc checks.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/n for n in ('expanded_arcs_2_seed.json','neighbor_arc_cut_sat.json',
                                         'neighbor_arc_sat_audit.json')]
    source,cut_data,audit = [json.loads(p.read_text()) for p in paths]
    assert audit['sources'][paths[1].name] == hashlib.sha256(paths[1].read_bytes()).hexdigest()
    assert cut_data['sources'][paths[0].name] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    cuts = [c['antecedents'] for c in cut_data['cuts']]
    pool,ids = [],{}
    results,counts = [],Counter()
    for si,row in enumerate(source['results']):
        if 'domains' not in row:
            continue
        ds = {t:set(source['domain_pool'][di]) for t,di in row['domains']}
        applicable = [k for k,cut in enumerate(cuts) if all(t in ds for t,s in cut)]
        trace,conflict = [],None
        while True:
            changed = False
            for k in applicable:
                cut = cuts[k]
                if any(s not in ds[t] for t,s in cut):
                    continue
                unfixed = [(t,s) for t,s in cut if len(ds[t]) > 1]
                if not unfixed:
                    conflict = k
                    break
                if len(unfixed) == 1:
                    t,s = unfixed[0]
                    ds[t].remove(s)
                    trace.append((k,t,s))
                    changed = True
            if conflict is not None or not changed:
                break
        result = dict(source_index=si,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                      choice_reductions=trace)
        if conflict is not None:
            result['rejection'] = dict(cut=conflict)
            counts['rejected'] += 1
        else:
            rows = []
            for tile,ss in sorted(ds.items()):
                key = tuple(sorted(ss))
                if key not in ids:
                    ids[key] = len(pool)
                    pool.append(key)
                rows.append((tile,ids[key]))
            result['domains'] = rows
            counts['survivor'] += 1
        counts['changed_cases'] += bool(trace) or conflict is not None
        counts['star_removals'] += len(trace)
        results.append(result)
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))}
    output = dict(scope='Necessary unit consequences of audited fixed-center choice cuts over the full unresolved frontier',
                  poses=source['poses'],domain_pool=pool,results=results,status_counts=dict(counts),sources=sources)
    (ROOT/'artifacts'/'choice_cut_domains.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    changed = [dict(r,full_result_index=i) for i,r in enumerate(results) if r['choice_reductions'] or 'rejection' in r]
    subset = dict(output,scope='Changed cases only; other frontier domains are unchanged',results=changed,
                  status_counts=dict(survivor=sum('domains' in r for r in changed),
                                     rejected=sum('rejection' in r for r in changed)))
    (ROOT/'artifacts'/'choice_cut_changed_seed.json').write_text(json.dumps(subset,separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),**counts)),flush=True)


if __name__ == '__main__':
    main()

"""Intersect the full fine frontier with necessary coarse-star support.

This fixed snapshot consumes the full Q025 frontier, not SAT assignments or
a selected pilot. Its surviving coarse vocabulary bounds the parent stars
of every original-rule tiling. Only that global coverage licenses pruning.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    names = ('choice_cut_forced_1.json','choice_cut_forced_1_audit.json',
             'choice_cut_expanded_arcs_1.json','choice_cut_expanded_arcs_1_audit.json',
             'coarse_parent_language.json','coarse_parent_language_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    source,forced_audit,fine,fine_audit,coarse,coarse_audit = [json.loads(p.read_text()) for p in paths]
    for data,path in ((forced_audit,paths[0]),(fine_audit,paths[2]),(coarse_audit,paths[4])):
        assert data['sources'][path.name] == hashlib.sha256(path.read_bytes()).hexdigest()
    star_by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    n = coarse['original_stars']
    active = set(range(n))|{star_by_key[r['boundary_index'],r['cover_index']]
                          for r in fine['results'] if 'domains' in r}
    initial = sorted(active)
    rounds = []
    while True:
        removed = []
        for s in sorted(active):
            for q,di in coarse['cases'][s]:
                if not active.intersection(coarse['domain_pool'][di]):
                    removed.append((s,q,di))
                    break
        if not removed:
            break
        assert all(s >= n for s,q,di in removed)
        rounds.append(removed)
        active.difference_update(s for s,q,di in removed)
    results = []
    counts = dict(survivor=0,fine_rejection=0,coarse_rejection=0)
    for i,row in enumerate(fine['results']):
        key = row['boundary_index'],row['cover_index']
        result = dict(source_index=i,forced_source_index=row['source_index'],boundary_index=key[0],cover_index=key[1])
        star = star_by_key[key]
        if 'domains' not in row:
            result['rejection'] = dict(kind='fine_arc_trace',result_index=i)
            counts['fine_rejection'] += 1
        elif star not in active:
            result['rejection'] = dict(kind='coarse_star_support',star=star)
            counts['coarse_rejection'] += 1
        else:
            result['domains'] = row['domains']
            counts['survivor'] += 1
        results.append(result)
    output = dict(scope='Full frontier after audited fine propagation and necessary parent-star support pruning',
                  poses=source['poses'],domain_pool=fine['domain_pool'],results=results,status_counts=counts,
                  initial_active_stars=initial,coarse_removal_rounds=rounds,final_active_stars=sorted(active),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'coarse_refined_frontier.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(**counts,rounds=[len(r) for r in rounds])),flush=True)


if __name__ == '__main__':
    main()

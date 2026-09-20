"""Q011: join the eight child-star domains using common-neighbor constraints.

This is an overapproximation of globally realizable clusters. Extra tuples
are unresolved candidates, not tilings. A cap is explicitly unknown.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=100000)
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/name for name in ('closed_star_audit.json','star_parent_consistency.json')]
    audit,raw = [json.loads(p.read_text()) for p in paths]
    assert raw['all_sibling_roles_agree']
    roles = [r[0] for r in audit['child_roles']]
    domains = [{s for s,r in enumerate(roles) if r == i} for i in range(8)]
    table = {(c['star'],c['sibling_role']):set(c['compatible_stars']) for c in raw['cases']}
    expected = {tuple(t) for t in audit['transitions']}
    results = []
    nodes = 0
    capped = False
    def search(current,assignment):
        nonlocal nodes,capped
        nodes += 1
        if len(assignment) == 8:
            result = tuple(assignment[i] for i in range(8))
            results.append(result)
            if len(results) >= args.limit:
                capped = True
            return
        role = min((i for i in range(8) if i not in assignment),key=lambda i:len(current[i]))
        for star in sorted(current[role]):
            next_domains = list(current)
            good = True
            for target in range(8):
                if target in assignment or target == role or (star,target) not in table:
                    continue
                next_domains[target] = current[target] & table[star,target]
                if not next_domains[target]:
                    good = False
                    break
            if good:
                search(next_domains,assignment|{role:star})
            if capped:
                return
    search(domains,{})
    extra = [t for t in results if t not in expected]
    found = set(results)
    if not capped:
        assert expected <= found
    output = dict(scope='Necessary overlap join for the eight recognized siblings; global extendibility not tested',
                  status='unknown_at_model_limit' if capped else 'enumeration_complete',
                  arguments=vars(args),search_nodes=nodes,tuples=results,
                  genuine_tuples=len(expected),extra_tuples=extra,
                  genuine_tuples_not_enumerated=len(expected-found),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_star_join.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('tuples','extra_tuples','sources')}|
                     dict(tuples=len(results),extra_tuples=len(extra))),flush=True)


if __name__ == '__main__':
    main()

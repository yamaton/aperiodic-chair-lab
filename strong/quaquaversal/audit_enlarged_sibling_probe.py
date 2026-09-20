"""Check every retained eight-star witness of the Q031 finite relaxation."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    names = ('coarse_parent_language.json','coarse_support_domain_audit.json','coarse_star_arc_filter.json',
             'enlarged_sibling_roles.json','enlarged_sibling_probe.json')
    paths = [ROOT/'artifacts'/n for n in names]
    coarse,support_audit,filtered,recognizer,raw = [json.loads(p.read_text()) for p in paths]
    assert support_audit['sources'][paths[0].name] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    roles = dict(recognizer['roles'])
    active = set(filtered['final_active_stars'])
    cases = [dict(row) for row in coarse['cases']]
    seen = set()
    incidences = 0
    for row in raw['results']:
        root = row['star']
        assert root not in seen and root in active and root >= coarse['original_stars']
        seen.add(root)
        assert row['status'] == 'sat'  # This snapshot has no UNSAT/capped case.
        witness = row['witness']
        assert len(witness) == 8 and witness[roles[root]] == root
        for i,s in enumerate(witness):
            assert s in active and roles[s] == i
            for j,q in recognizer['sibling_edges'][i]:
                assert q in cases[s] and witness[j] in coarse['domain_pool'][cases[s][q]]
                incidences += 1
    assert seen == active-set(range(coarse['original_stars']))
    output = dict(scope='Witness audit for the eight-sibling compatibility CSP, not a geometric/global extension certificate',
                  witnesses=len(seen),checked_directed_incidences=incidences,additional_parent_exclusions=0,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'enlarged_sibling_probe_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

"""Q030: check recognizable sibling grouping for the enlarged parent rule.

Exact child geometry and complete audited support domains are used. This
establishes the local hypotheses for ONE grouping step of the enlarged rule;
it does not establish that its own parent tiling obeys the enlarged rule.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import child_maps,compose
from contact_atlas import relative
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_star_language.json','coarse_parent_language.json','coarse_support_domain_audit.json',
             'coarse_star_arc_filter.json','coarse_star_arc_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    language,coarse,support_audit,filtered,filter_audit = [json.loads(p.read_text()) for p in paths]
    assert support_audit['sources'][paths[1].name] == hashlib.sha256(paths[1].read_bytes()).hexdigest()
    assert filter_audit['sources'][paths[3].name] == hashlib.sha256(paths[3].read_bytes()).hexdigest()
    poses = [raw_pose(p) for p in coarse['poses']]
    index = {p:i for i,p in enumerate(poses)}
    children = [p for name,p in child_maps()]
    edges = []
    for i,p in enumerate(children):
        row = []
        for j,q in enumerate(children):
            if i == j:
                continue
            rel = relative(p,q)
            assert compose(p,rel) == q
            if edge_points(rel,first_only=True):
                row.append((j,index[rel]))
        edges.append(row)
    siblings = [set(q for j,q in row) for row in edges]
    assert siblings == [set(row) for row in language['sibling_neighbors']]
    reached = {0}
    while True:
        more = reached|{j for i in reached for j,q in edges[i]}
        if more == reached:
            break
        reached = more
    assert reached == set(range(8))
    stars = [set(star) for star in coarse['stars']]
    active = set(filtered['final_active_stars'])
    roles = {s:[i for i,ss in enumerate(siblings) if ss <= stars[s]] for s in active}
    assert all(len(rs) == 1 for rs in roles.values())
    roles = {s:rs[0] for s,rs in roles.items()}
    cases = [dict(row) for row in coarse['cases']]
    unresolved = []
    checked = alternatives = 0
    for s in sorted(active):
        for expected,q in edges[roles[s]]:
            assert q in stars[s]
            options = set(coarse['domain_pool'][cases[s][q]]) & active
            assert options
            wrong = sorted(t for t in options if roles[t] != expected)
            if wrong:
                unresolved.append(dict(star=s,pair=q,expected_role=expected,wrong_role_stars=wrong))
            checked += 1
            alternatives += len(options)
    output = dict(scope='Exact local role and sibling-consistency hypotheses for one recognizable grouping of the enlarged rule',
                  active_stars=len(active),extra_stars=len(active)-coarse['original_stars'],sibling_edges=edges,
                  roles=sorted(roles.items()),role_counts=dict(Counter(roles.values())),
                  checked_incidences=checked,checked_target_alternatives=alternatives,
                  unresolved=unresolved,all_sibling_roles_agree=not unresolved,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',ROOT/'audit_closed_atlas.py',
                            *paths,Path(__file__))})
    (ROOT/'artifacts'/'enlarged_sibling_roles.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('sources','roles','sibling_edges','unresolved')},
                     separators=(',',':')),flush=True)


if __name__ == '__main__':
    main()

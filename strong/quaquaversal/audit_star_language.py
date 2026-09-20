"""Audit closed-star closure and recover child roles without using its BFS.

Uses edge clipping for the geometric lift table, and direct patch geometry
for the seed. The result is a finite language/recognizability certificate,
not yet a hierarchy theorem for arbitrary locally admitted tilings.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import I,ZERO,F,child_maps,compose,vertices,inside,encode
from contact_atlas import relative
from closed_stars import bounds,disjoint,TouchChecker
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT/'artifacts'/'closed_star_language.json'
    raw = json.loads(path.read_text())
    assert raw['status'] == 'closed' and not raw['pending_star_indices']
    atlas_path = ROOT/'artifacts'/'closed_contact_atlas.json'
    atlas_raw = json.loads(atlas_path.read_text())
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    indices = {p:i for i,p in enumerate(atlas)}
    children = [p for _,p in child_maps()]
    cb = [bounds(p) for p in children]
    siblings = []
    for i,p in enumerate(children):
        siblings.append(sorted(indices[relative(p,q)] for j,q in enumerate(children)
                               if i != j and edge_points(relative(p,q),first_only=True)))
    assert siblings == raw['sibling_neighbors']
    lifts = []
    for pi,parent in enumerate(atlas):
        right = [compose(parent,q) for q in children]
        rb = [bounds(q) for q in right]
        lift = [[] for _ in children]
        for i,p in enumerate(children):
            for j,q in enumerate(right):
                if not disjoint(cb[i],rb[j]) and edge_points(relative(p,q),first_only=True):
                    lift[i].append([j,indices[relative(p,q)]])
        assert lift == raw['closed_pair_lifts'][pi],pi
        lifts.append(lift)
        if (pi+1)%300 == 0:
            print(f'lifts audited: {pi+1}/{len(atlas)}',flush=True)
    stars = [tuple(s['neighbors']) for s in raw['stars']]
    index = {s:i for i,s in enumerate(stars)}
    assert len(index) == len(stars)
    def descendants(s):
        result = [set(sib) for sib in siblings]
        for q in s:
            for i,neighbors in enumerate(lifts[q]):
                result[i].update(k for j,k in neighbors)
        return [tuple(sorted(t)) for t in result]
    transitions = [[index[t] for t in descendants(s)] for s in stars]
    roles = [set() for s in stars]
    for row in transitions:
        for i,t in enumerate(row):
            roles[t].add(i)
    for si,entry in enumerate(raw['stars'][1:],start=1):
        o = entry['origin']
        assert o['kind'] == 'descendant' and o['parent'] < si
        assert transitions[o['parent']][o['role']] == si
    # Locate the seed in a real level-3 patch, then verify every possible
    # neighbor with edge clipping. Bounding boxes are exact necessary tests.
    patch = [(I,ZERO,F(1))]
    for _ in range(3):
        patch = [compose(p,q) for p in patch for q in children]
    bs = [bounds(p) for p in patch]
    checker = TouchChecker()
    seed_tile = None
    for i,p in enumerate(patch):
        if not all(inside(v,strict=True) for v in vertices(p)):
            continue
        candidates = [j for j,q in enumerate(patch) if j != i and not disjoint(bs[i],bs[j])]
        found = tuple(sorted(indices[relative(p,patch[j])] for j in candidates if checker.touches(p,patch[j])))
        if found == stars[0]:
            independent = tuple(sorted(indices[relative(p,patch[j])] for j in candidates
                                       if edge_points(relative(p,patch[j]),first_only=True)))
            assert independent == stars[0]
            seed_tile = i
            break
    assert seed_tile is not None
    # Bad periodic stars form a separate finite descendant graph. Closure
    # of the legal graph means discarded legal descendants cannot reenter it.
    sample_path = ROOT/'artifacts'/'closed_stars_4_2.json'
    sample = json.loads(sample_path.read_text())
    ids = [indices[raw_pose(p)] for p in sample['relative_poses']]
    bad = []
    bad_index = {}
    origins = []
    def insert(s,origin):
        if s not in bad_index:
            bad_index[s] = len(bad)
            bad.append(s)
            origins.append(origin)
        return bad_index[s]
    for k,entry in enumerate(sample['periodic']):
        s = tuple(sorted(ids[q] for q in entry['star']))
        if s not in index:
            insert(s,dict(kind='periodic_seed',index=k))
    bad_transitions = []
    cursor = 0
    while cursor < len(bad):
        row = []
        for role,s in enumerate(descendants(bad[cursor])):
            row.append(dict(legal=index[s]) if s in index else
                       dict(bad=insert(s,dict(kind='descendant',parent=cursor,role=role))))
        bad_transitions.append(row)
        cursor += 1
        assert len(bad) < 100000,'bad-star closure exceeds audit budget'
    # Exhibit a reachable cycle by following a bad descendant. If a chosen
    # branch ends, this search alone reports none; it does not prove acyclicity.
    cycle = None
    for start in range(len(bad)):
        visited = {}
        walk = []
        current = start
        while current not in visited:
            visited[current] = len(walk)
            options = [(i,e['bad']) for i,e in enumerate(bad_transitions[current]) if 'bad' in e]
            if not options:
                break
            role,target = options[0]
            walk.append(dict(star=current,role=role,target=target))
            current = target
        else:
            cycle = walk[visited[current]:]
            break
    output = dict(scope='Independent geometric lift and seed audit; finite closed-star language and child-role recognition',
                  legal_star_count=len(stars),seed_patch_level=3,seed_patch_tile=seed_tile,
                  transitions=transitions,child_roles=[sorted(r) for r in roles],
                  role_multiplicities=dict(Counter(len(r) for r in roles)),
                  periodic_bad_stars=[dict(neighbors=s,origin=o,descendants=row)
                                      for s,o,row in zip(bad,origins,bad_transitions)],
                  periodic_bad_cycle=cycle,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'closed_stars.py',
                            ROOT/'reflected_controls.py',ROOT/'audit_closed_atlas.py',path,atlas_path,sample_path,Path(__file__))})
    (ROOT/'artifacts'/'closed_star_audit.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps(dict(stars=len(stars),role_multiplicities=output['role_multiplicities'],
                          bad_stars=len(bad),bad_cycle_length=len(cycle) if cycle else None)),flush=True)


if __name__ == '__main__':
    main()

"""Q012: each exterior neighbor must extend all touching child stars at once.

Intersect complete-star domains from every child center seeing that neighbor.
An empty intersection rejects a candidate tuple. Survivors still require
simultaneous compatibility among their exterior neighbors and parent legality.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import child_maps,compose,encode
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_audit.json','closed_star_compatibility.json','parent_join_filter.json')]
    atlas_raw,audit,compat,joined = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    children = [p for _,p in child_maps()]
    poses = list(children)
    index = {p:i for i,p in enumerate(poses)}
    global_ids = {}
    for si,row in enumerate(compat['cases']):
        role, = audit['child_roles'][si]
        for q,domain in row:
            if (role,q) not in global_ids:
                p = compose(children[role],atlas[q])
                if p not in index:
                    index[p] = len(poses)
                    poses.append(p)
                global_ids[role,q] = index[p]
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    requirements = [[(global_ids[audit['child_roles'][si][0],q],domain) for q,domain in row]
                    for si,row in enumerate(compat['cases'])]
    genuine = {tuple(t) for t in audit['transitions']}
    survivors = []
    rejections = []
    stats = Counter()
    # Retain domain ID intersections as compact, replayable provenance.
    for ti,t in enumerate(joined['survivors']):
        domains = {i:1<<s for i,s in enumerate(t)}
        traces = {i:[] for i in range(8)}
        failure = None
        for i,s in enumerate(t):
            for tile,di in requirements[s]:
                domains[tile] = domains.get(tile,bits[di]) & bits[di]
                traces.setdefault(tile,[]).append(di)
                if not domains[tile]:
                    failure = dict(tile=tile,domains=traces[tile],last_child=i)
                    break
            if failure:
                break
        if failure:
            assert tuple(t) not in genuine
            rejections.append(dict(tuple_index=ti,conflict=failure))
        else:
            survivors.append(dict(tuple_index=ti,external_domains=[dict(tile=k,domains=traces[k])
                                                                  for k in sorted(domains) if k >= 8]))
            stats[len(domains)] += 1
        if (ti+1)%10000 == 0:
            print(f'checked {ti+1}/{len(joined["survivors"])}; survivors {len(survivors)}',flush=True)
    surviving_tuples = {tuple(joined['survivors'][s['tuple_index']]) for s in survivors}
    assert genuine <= surviving_tuples
    extra = len(surviving_tuples-genuine)
    output = dict(scope='Necessary simultaneous closed-star extension domains for neighbors of eight recognized children',
                  poses=poses,requirements=requirements,survivors=survivors,rejections=rejections,
                  extra_survivors=extra,union_tile_counts=dict(stats),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'parent_external_domains.json').write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(global_positions=len(poses),input=len(joined['survivors']),
                          rejected=len(rejections),survivors=len(survivors),extra=extra)),flush=True)


if __name__ == '__main__':
    main()

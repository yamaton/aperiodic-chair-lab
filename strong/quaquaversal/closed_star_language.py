"""Q009: exact closure of complete closed stars under subdivision.

All children touching a root child belong to the root's closed parent star.
This makes the eight descendant stars a deterministic finite operation. A
nonempty seed star from a real supertile generates the entire proper-copy
closed-star language if this closure stabilizes: every legal finite patch
occurs in an iterate of the one prototile, which is part of the seed star.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import child_maps,compose,encode
from contact_atlas import relative
from closed_stars import bounds,disjoint
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=16)
    parser.add_argument('--limit',type=int,default=200000)
    parser.add_argument('--periodic-levels',type=int,default=10)
    args = parser.parse_args()
    atlas_path = ROOT/'artifacts'/'closed_contact_atlas.json'
    atlas_raw = json.loads(atlas_path.read_text())
    assert atlas_raw['status'] == 'closed'
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    indices = {p:i for i,p in enumerate(atlas)}
    children = [p for _,p in child_maps()]
    cb = [bounds(p) for p in children]
    siblings = [{indices[relative(p,q)] for j,q in enumerate(children) if i != j and relative(p,q) in indices}
                for i,p in enumerate(children)]
    lifts = []
    for parent in atlas:
        right = [compose(parent,q) for q in children]
        rb = [bounds(q) for q in right]
        lift = [[] for _ in children]
        for i,p in enumerate(children):
            for j,q in enumerate(right):
                if not disjoint(cb[i],rb[j]):
                    r = relative(p,q)
                    if r in indices:
                        lift[i].append((j,indices[r]))
        lifts.append(lift)
    def descendants(star):
        result = [set(s) for s in siblings]
        for parent in star:
            for i,neighbors in enumerate(lifts[parent]):
                result[i].update(k for j,k in neighbors)
        return tuple(tuple(sorted(s)) for s in result)
    paths = [ROOT/'artifacts'/'closed_stars_3_1.json',ROOT/'artifacts'/'closed_stars_4_2.json']
    samples = []
    for path in paths:
        raw = json.loads(path.read_text())
        ids = [indices[raw_pose(p)] for p in raw['relative_poses']]
        samples.append(dict(observed=[tuple(sorted(ids[k] for k in s['star'])) for s in raw['observed']],
                            periodic=Counter({tuple(sorted(ids[k] for k in s['star'])):s['count'] for s in raw['periodic']})))
    seed = samples[0]['observed'][0]
    stars,origins,index = [seed],[dict(kind='observed_seed',file=paths[0].name,index=0)],{seed:0}
    frontier = [0]
    rounds = []
    for step in range(args.rounds):
        old_count = len(stars)
        for si in frontier:
            for role,star in enumerate(descendants(stars[si])):
                if star not in index:
                    index[star] = len(stars)
                    stars.append(star)
                    origins.append(dict(kind='descendant',parent=si,role=role))
        frontier = list(range(old_count,len(stars)))
        row = dict(round=step+1,added=len(frontier),total=len(stars))
        rounds.append(row)
        print(json.dumps(row),flush=True)
        if not frontier or len(stars) >= args.limit:
            break
    closed = not frontier
    sample_missing = [len(set(s['observed'])-set(index)) for s in samples]
    if closed:
        assert sample_missing == [0,0],sample_missing
    periodic = []
    current = samples[1]['periodic']
    for level in range(2,args.periodic_levels+1):
        missing = {s:n for s,n in current.items() if s not in index}
        periodic.append(dict(level=level,tile_count=sum(current.values()),distinct_stars=len(current),
                             outside_language_stars=len(missing),outside_language_tile_count=sum(missing.values()),
                             all_legal=closed and not missing))
        print('periodic',json.dumps(periodic[-1]),flush=True)
        if closed and not missing:
            break
        newer = Counter()
        for star,n in current.items():
            for descendant in descendants(star):
                newer[descendant] += n
        current = newer
    output = dict(scope='Complete closed-star substitution closure from a genuinely observed seed',
                  status='closed' if closed else 'unknown_after_finite_prefix',rounds=rounds,
                  sibling_neighbors=[sorted(s) for s in siblings],closed_pair_lifts=lifts,
                  stars=[dict(neighbors=s,origin=o) for s,o in zip(stars,origins)],
                  pending_star_indices=frontier,sample_stars_outside=sample_missing,
                  periodic_controls=periodic,arguments=vars(args),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'closed_stars.py',
                                     ROOT/'reflected_controls.py',atlas_path,*paths,Path(__file__))})
    (ROOT/'artifacts'/'closed_star_language.json').write_text(json.dumps(encode(output),indent=2)+'\n')


if __name__ == '__main__':
    main()

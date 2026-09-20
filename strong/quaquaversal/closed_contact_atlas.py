"""Q009: substitution closure of all nonempty closed tile intersections.

Unlike contact_atlas.py, this includes edge-only and point-only intersections.
An exhausted frontier proves closure. Hitting a bound is recorded as unknown.
Each new pose retains a finite substitution witness back to sibling contacts.
"""

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

from geometry import F,I,ZERO,child_maps,compose,encode
from contact_atlas import relative
from closed_stars import TouchChecker,bounds,disjoint
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=12)
    parser.add_argument('--limit',type=int,default=10000)
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'closed_contact_atlas.json')
    args = parser.parse_args()
    children = [p for _,p in child_maps()]
    child_bounds = [bounds(p) for p in children]
    checker = TouchChecker()
    poses,origins,index = [],[],{}
    def insert(p,origin):
        if p in index:
            return False
        index[p] = len(poses)
        poses.append(p)
        origins.append(origin)
        return True
    for i,j in combinations(range(8),2):
        if not disjoint(child_bounds[i],child_bounds[j]) and checker.touches(children[i],children[j]):
            insert(relative(children[i],children[j]),dict(kind='sibling',i=i,j=j))
            insert(relative(children[j],children[i]),dict(kind='sibling',i=j,j=i))
    seed_count = len(poses)
    frontier = list(range(seed_count))
    rounds = []
    inputs = (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'closed_stars.py',ROOT/'reflected_controls.py',Path(__file__))
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    print(f'seeds: {seed_count}',flush=True)
    def save(status,pending):
        controls = []
        for name in ('closed_stars_3_1.json','closed_stars_4_2.json'):
            path = ROOT/'artifacts'/name
            raw = json.loads(path.read_text())
            table = [raw_pose(p) for p in raw['relative_poses']]
            selected = {table[k] for star in raw['periodic'] for k in star['star']}
            unknown = sorted(selected-set(index))
            controls.append(dict(source=name,total_distinct_pairs=len(selected),
                                 outside_current_atlas=len(unknown),outside_poses=unknown))
            sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        report = dict(scope='All closed pair intersections in finite proper quaquaversal supertiles',
                      status=status,seed_count=seed_count,rounds=rounds,
                      poses=[dict(pose=p,origin=o) for p,o in zip(poses,origins)],
                      pending_pose_indices=pending,closed_intersection_tests=checker.calls,
                      periodic_controls=controls,
                      arguments={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},sources=sources)
        args.output.write_text(json.dumps(encode(report),indent=2)+'\n')
    for step in range(args.rounds):
        old_count = len(poses)
        for fi,pi in enumerate(frontier):
            p = poses[pi]
            right = [compose(p,q) for q in children]
            rb = [bounds(q) for q in right]
            for i,a in enumerate(children):
                for j,b in enumerate(right):
                    if not disjoint(child_bounds[i],rb[j]) and checker.touches(a,b):
                        insert(relative(a,b),dict(kind='subdivision',parent=pi,i=i,j=j,reverse=False))
                        insert(relative(b,a),dict(kind='subdivision',parent=pi,i=i,j=j,reverse=True))
            if (fi+1)%100 == 0:
                print(f'round {step+1}: processed {fi+1}/{len(frontier)}, poses {len(poses)}',flush=True)
        fresh = list(range(old_count,len(poses)))
        row = dict(round=step+1,processed=len(frontier),added=len(fresh),total=len(poses))
        rounds.append(row)
        print(json.dumps(row),flush=True)
        frontier = fresh
        status = 'closed' if not fresh else 'unknown_after_finite_prefix'
        save(status,frontier)
        if not fresh or len(poses) >= args.limit:
            break
    if not rounds:
        save('unknown_after_finite_prefix',frontier)
    print(f'{status}: {len(poses)} closed-contact poses',flush=True)


if __name__ == '__main__':
    main()

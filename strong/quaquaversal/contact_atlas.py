"""Q006: exact relative-pose rules, stronger than pointwise face colors.

Close the sibling contact atlas under subdivision of both contacting tiles.
Finite stabilization certifies the pair language in finite supertiles; it
does not prove that this pair language forces a hierarchy in arbitrary tilings.
"""

import argparse
import hashlib
import json
from pathlib import Path

from geometry import (F,I,ZERO,child_maps,compose,contacts,contacts_fast,
                      inverse_rotation,mm,mul,mv,sub,encode)
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def relative(p,q):
    r = inverse_rotation(p[0])
    return mm(r,q[0]),mul(1/p[2],mv(r,sub(q[1],p[1]))),q[2]/p[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=8)
    parser.add_argument('--limit',type=int,default=2000)
    args = parser.parse_args()
    children = [p for _,p in child_maps()]
    known = {}
    for c in contacts(children):
        for i,j in ((c['i'],c['j']),(c['j'],c['i'])):
            known.setdefault(relative(children[i],children[j]),dict(kind='sibling',i=i,j=j))
    frontier = list(known)
    rounds = []
    for step in range(args.rounds):
        fresh = {}
        for p in frontier:
            poses = children+[compose(p,q) for q in children]
            for c in contacts_fast(poses):
                if c['i'] >= 8 or c['j'] < 8:
                    continue
                for i,j in ((c['i'],c['j']),(c['j'],c['i'])):
                    q = relative(poses[i],poses[j])
                    if q not in known and q not in fresh:
                        fresh[q] = dict(kind='subdivided_contact',parent=p,i=i,j=j)
        known.update(fresh)
        frontier = list(fresh)
        row = dict(round=step+1,added=len(fresh),total=len(known))
        rounds.append(row)
        print(json.dumps(row),flush=True)
        if not fresh or len(known) >= args.limit:
            break
    raw = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    cell = [raw_pose(p) for p in raw['periodic_control']['cell']]
    periodic = []
    for c in raw['periodic_control']['contacts']:
        p,q = cell[c['tile']],cell[c['neighbor']]
        q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
        rel = relative(p,q)
        periodic.append(dict(tile=c['tile'],neighbor=c['neighbor'],offset=c['offset'],
                             allowed=rel in known,relative_pose=rel))
    output = dict(scope='All observed positive-area relative poses; substitution closure, not hierarchy enforcement',
                  status='closed' if not frontier else 'unknown_after_finite_prefix',rounds=rounds,
                  poses=[dict(pose=p,origin=o) for p,o in known.items()],
                  periodic_control_contacts=periodic,
                  two_prism_periodic_control_accepted=all(c['allowed'] for c in periodic),
                  arguments=vars(args),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'reflected_controls.py',
                                     ROOT/'artifacts'/'geometry_and_constant_rules.json',Path(__file__))})
    (ROOT/'artifacts'/'contact_atlas.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print('periodic control accepted:',output['two_prism_periodic_control_accepted'],flush=True)


if __name__ == '__main__':
    main()

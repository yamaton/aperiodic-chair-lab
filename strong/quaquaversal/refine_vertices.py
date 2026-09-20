"""Q003 necessary vertex closure for hereditary sibling-compatible panels.

This checks a necessary condition, not the full Goodman–Strauss hypotheses.
A finite prefix which keeps growing proves no nonexistence result.
"""

import argparse
import hashlib
import json
from pathlib import Path

from geometry import (F,I,ZERO,VERTICES,child_maps,compose,encode,inside,
                      inverse_rotation,mm,mul,mv,sub,transform,inverse_point)

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=5)
    parser.add_argument('--limit',type=int,default=10000)
    args = parser.parse_args()
    named = child_maps()
    # Unscaled affine maps from one canonical copy to another.
    transfers = []
    for i,(_,p) in enumerate(named):
        for j,(_,q) in enumerate(named):
            if i == j:
                continue
            r = mm(inverse_rotation(q[0]),p[0])
            t = mul(1/q[2],mv(inverse_rotation(q[0]),sub(p[1],q[1])))
            transfers.append((f'sibling:{i}:{j}',(r,t,F(1))))
    for j,(_,q) in enumerate(named):
        r = inverse_rotation(q[0])
        t = mul(-1/q[2],mv(r,q[1]))
        transfers.append((f'hereditary:{j}',(r,t,1/q[2])))
    known = {v:dict(kind='carrier_vertex',index=i) for i,v in enumerate(VERTICES)}
    frontier = list(known)
    rounds = []
    for step in range(args.rounds):
        fresh = {}
        for v in frontier:
            for label,pose in transfers:
                w = transform(pose,v)
                if inside(w) and not inside(w,strict=True) and w not in known and w not in fresh:
                    fresh[w] = dict(kind=label,source=encode(v))
        known.update(fresh)
        frontier = list(fresh)
        item = dict(round=step+1,added=len(fresh),total=len(known),
                    maximum_denominator=max(x.denominator for p in known for x in p))
        rounds.append(item)
        print(json.dumps(item),flush=True)
        if not fresh or len(known) >= args.limit:
            break
    status = 'vertex_closure_stabilized' if not frontier else 'unknown_after_finite_prefix'
    output = dict(scope='Necessary finite vertex closure only; no full panel theorem certificate',
                  status=status,rounds=rounds,
                  vertices=[dict(point=encode(p),origin=origin) for p,origin in known.items()],
                  arguments=vars(args),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',Path(__file__))})
    (ROOT/'artifacts'/'vertex_refinement.json').write_text(json.dumps(output,indent=2)+'\n')
    print(status,flush=True)


if __name__ == '__main__':
    main()

"""Q004: change the handedness assigned to child occurrences, not the carrier.

The scalene prism has one improper self-symmetry, z -> 1-z. Decorating it
breaks that symmetry, so the 256 child words are meaningful new candidates.
This is an exhaustive finite family, not an arbitrary matching-rule search.
"""

import hashlib
import json
from pathlib import Path
import sympy as sp

from geometry import F,vec,child_maps,compose,contacts
from polynomial_rules import system

ROOT = Path(__file__).resolve().parent
MIRROR = ((vec(1,0,0),vec(0,1,0),vec(0,0,-1)),vec(0,0,1),F(1))


def mirrored_case(mask,base,cs):
    poses = [compose(p,MIRROR) if (mask >> i)&1 else p for i,p in enumerate(base)]
    mapped = []
    for c in cs:
        q = dict(c)
        for side in ('i','j'):
            f = 'f'+side
            if (mask >> c[side])&1 and c[f] in (0,1):
                q[f] = 1-c[f]
        mapped.append(q)
    return poses,mapped


def main():
    base = [p for _,p in child_maps()]
    cs = contacts(base)
    results = []
    for mask in range(256):
        poses,mapped = mirrored_case(mask,base,cs)
        entry = dict(mask=mask,reflected_children=[name for i,(name,_) in enumerate(child_maps()) if (mask>>i)&1])
        for degree in (0,1,2):
            for sign in (-1,1):
                matrix,monomials,nmaps = system(poses,mapped,degree,sign)
                basis = matrix.nullspace()
                key = ('equal' if sign == -1 else 'opposite')+f'_degree_{degree}'
                entry[key] = len(basis)
        results.append(entry)
        if mask % 32 == 31:
            print(f'Completed masks 0..{mask}',flush=True)
    summary = {key:sorted({r[key] for r in results}) for key in results[0] if 'degree_' in key}
    out = dict(scope='256 reflected child words; scalar polynomial markings degree <=2; sibling compatibility only',
               summary=summary,results=results,
               sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',Path(__file__))})
    (ROOT/'artifacts'/'reflected_polynomial_search.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()

"""Q004 follow-up: challenge every degree-two family with periodic cells."""

import hashlib
import json
from pathlib import Path
import sympy as sp

from geometry import F,child_maps,compose,contacts,encode
from polynomial_rules import system,A,B
from reflected_search import MIRROR,mirrored_case

ROOT = Path(__file__).resolve().parent


def raw_pose(raw):
    return tuple(tuple(F(x) for x in row) for row in raw[0]),tuple(F(x) for x in raw[1]),F(raw[2])


def control_matrix(original,mask,degree,sign):
    cell = [raw_pose(p) for p in original['periodic_control']['cell']]
    cell = [compose(p,MIRROR) if (mask>>i)&1 else p for i,p in enumerate(cell)]
    rows = []
    for c in original['periodic_control']['contacts']:
        p,q = cell[c['tile']],cell[c['neighbor']]
        q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
        fi,fj = c['fi'],c['fj']
        if (mask>>c['tile'])&1 and fi < 2:
            fi = 1-fi
        if (mask>>c['neighbor'])&1 and fj < 2:
            fj = 1-fj
        m,monomials,_ = system([p,q],[dict(i=0,j=1,fi=fi,fj=fj)],degree,sign)
        rows.extend(m.tolist())
    return sp.Matrix(rows),monomials


def main():
    original = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    base = [p for _,p in child_maps()]
    cs = contacts(base)
    results = []
    for sign in (-1,1):
        controls = [control_matrix(original,mask,2,sign)[0] for mask in range(4)]
        for mask in range(256):
            poses,mapped = mirrored_case(mask,base,cs)
            m,monomials,_ = system(poses,mapped,2,sign)
            basis = m.nullspace()
            accepted = [i for i,c in enumerate(controls) if all(c*v == sp.zeros(c.rows,1) for v in basis)]
            record = dict(mask=mask,condition='equal' if sign == -1 else 'opposite',
                          dimension=len(basis),universally_accepted_cell_masks=accepted)
            if not accepted or (sign == 1 and basis):
                record['basis'] = [[str(sp.expand(sum(v[f*len(monomials)+k]*A**i*B**j
                                                     for k,(i,j) in enumerate(monomials))))
                                    for f in range(5)] for v in basis]
            results.append(record)
        print(f'Completed {"equal" if sign == -1 else "opposite"} families',flush=True)
    unresolved = [r for r in results if not r['universally_accepted_cell_masks']]
    output = dict(scope='All 256 child words; scalar face polynomials total degree <=2; two-prism periodic cells',
                  families=len(results),not_rejected_by_control=len(unresolved),results=results,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'reflected_search.py',
                                     ROOT/'artifacts'/'geometry_and_constant_rules.json',Path(__file__))})
    (ROOT/'artifacts'/'reflected_periodic_controls.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(families=len(results),not_rejected_by_control=len(unresolved)),indent=2))


if __name__ == '__main__':
    main()

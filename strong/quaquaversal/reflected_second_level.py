"""Continue Q004 past the misleading first-generation free outer faces."""

import hashlib
import json
from pathlib import Path
import sympy as sp

from geometry import child_maps,compose,contacts,contacts_fast,encode
from polynomial_rules import system,A,B
from reflected_search import mirrored_case
from reflected_controls import control_matrix

ROOT = Path(__file__).resolve().parent


def main():
    original = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    previous = json.loads((ROOT/'artifacts'/'reflected_periodic_controls.json').read_text())
    survivors = [r for r in previous['results'] if not r['universally_accepted_cell_masks']]
    base = [p for _,p in child_maps()]
    first_contacts = contacts(base)
    controls = {sign:[control_matrix(original,mask,2,sign)[0] for mask in range(4)] for sign in (-1,1)}
    cache = {}
    results = []
    for record in survivors:
        mask = record['mask']
        sign = -1 if record['condition'] == 'equal' else 1
        if mask not in cache:
            first,_ = mirrored_case(mask,base,first_contacts)
            second = [compose(p,q) for p in first for q in first]
            cache[mask] = second,contacts_fast(second)
        poses,cs = cache[mask]
        m,monomials,_ = system(poses,cs,2,sign)
        basis = m.nullspace()
        accepted = [i for i,c in enumerate(controls[sign]) if all(c*v == sp.zeros(c.rows,1) for v in basis)]
        result = dict(mask=mask,condition=record['condition'],contacts=len(cs),
                      first_level_dimension=record['dimension'],second_level_dimension=len(basis),
                      universally_accepted_cell_masks=accepted,
                      basis=[[str(sp.expand(sum(v[f*len(monomials)+k]*A**i*B**j
                                                  for k,(i,j) in enumerate(monomials))))
                              for f in range(5)] for v in basis])
        results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k != 'basis'}),flush=True)
    output = dict(scope='Second-level sibling constraints for the 40 degree-two families not yet rejected',
                  results=results,not_rejected_by_control=sum(not r['universally_accepted_cell_masks'] for r in results),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'reflected_search.py',
                                     ROOT/'reflected_controls.py',ROOT/'artifacts'/'geometry_and_constant_rules.json',
                                     ROOT/'artifacts'/'reflected_periodic_controls.json',Path(__file__))})
    (ROOT/'artifacts'/'reflected_second_level.json').write_text(json.dumps(output,indent=2)+'\n')
    print('Remaining families:',output['not_rejected_by_control'])


if __name__ == '__main__':
    main()

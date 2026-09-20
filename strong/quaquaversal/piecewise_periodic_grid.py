"""Q005: larger periodic controls for the two surviving panel-color families."""

import hashlib
import json
from itertools import product
from pathlib import Path
import z3

from geometry import compose,encode
from reflected_search import MIRROR
from reflected_controls import raw_pose
from piecewise_search import PanelRules

ROOT = Path(__file__).resolve().parent


def main():
    original = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    candidates = json.loads((ROOT/'artifacts'/'piecewise_level_3.json').read_text())['results']
    panel_path = ROOT/'artifacts'/'panel_refinement_v2.json'
    rules = PanelRules(json.loads(panel_path.read_text()))
    cell = [raw_pose(p) for p in original['periodic_control']['cell']]
    tables = []
    for c in original['periodic_control']['contacts']:
        possibilities = []
        for ha,hb in product((0,1),repeat=2):
            p,q = cell[c['tile']],cell[c['neighbor']]
            if ha:
                p = compose(p,MIRROR)
            if hb:
                q = compose(q,MIRROR)
            q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
            fi,fj = c['fi'],c['fj']
            if ha and fi < 2:
                fi = 1-fi
            if hb and fj < 2:
                fj = 1-fj
            possibilities.append(dict(source_handedness=ha,target_handedness=hb,
                                      equations=rules.equations([p,q],dict(i=0,j=1,fi=fi,fj=fj))))
        tables.append(dict(tile=c['tile'],neighbor=c['neighbor'],offset=c['offset'],possibilities=possibilities))
    results = []
    for candidate in candidates:
        colors = sum(candidate['canonical_panel_colors'],[])
        allowed = [[(p['source_handedness'],p['target_handedness']) for p in t['possibilities']
                    if all(colors[a] == colors[b] for a,b in p['equations'])] for t in tables]
        attempts = []
        witness = None
        for size in ((1,1,1),(2,1,1),(1,2,1),(1,1,2),(2,2,1),(2,2,2)):
            boxes = list(product(*(range(n) for n in size)))
            keys = [box+(tile,) for box in boxes for tile in range(2)]
            variables = {k:z3.Bool('h_'+'_'.join(map(str,k))) for k in keys}
            solver = z3.Solver()
            solver.set(timeout=10000)
            constraints = []
            for box in boxes:
                for i,t in enumerate(tables):
                    source = box+(t['tile'],)
                    target = tuple((x+d)%n for x,d,n in zip(box,t['offset'],size))+(t['neighbor'],)
                    solver.add(z3.Or([z3.And(variables[source] == bool(a),variables[target] == bool(b)) for a,b in allowed[i]]))
                    constraints.append((source,target,i))
            status = solver.check()
            attempts.append(dict(box_dimensions=size,status=str(status)))
            if status == z3.sat:
                model = solver.model()
                values = {k:int(z3.is_true(model.eval(v,model_completion=True))) for k,v in variables.items()}
                # Recheck every contact truth-table requirement without solver operations.
                assert all((values[a],values[b]) in allowed[i] for a,b,i in constraints)
                witness = dict(box_dimensions=size,tile_count=len(keys),
                               assignments=[dict(box=k[:3],tile=k[3],reflected=values[k]) for k in keys],
                               directed_contact_checks=len(constraints))
                break
        result = dict(candidate_mask=candidate['mask'],attempts=attempts,allowed_handedness_pairs=allowed,witness=witness)
        results.append(result)
        print(json.dumps(result),flush=True)
    output = dict(scope='Periodic box grids using either handedness; 60-panel constant-color families from Q005',
                  results=results,contact_tables=tables,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'periodic_obstruction.py',
                                     ROOT/'piecewise_search.py',ROOT/'reflected_search.py',ROOT/'reflected_controls.py',
                                     ROOT/'artifacts'/'piecewise_level_3.json',
                                     ROOT/'artifacts'/'geometry_and_constant_rules.json',panel_path,Path(__file__))})
    (ROOT/'artifacts'/'piecewise_periodic_grid.json').write_text(json.dumps(encode(output),indent=2)+'\n')


if __name__ == '__main__':
    main()

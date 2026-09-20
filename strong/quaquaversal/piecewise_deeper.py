"""Q005 continuation: preserve higher-generation tests as separate files."""

import argparse
import hashlib
import json
from pathlib import Path

from geometry import child_maps,compose,contacts,contacts_fast,encode
from reflected_search import mirrored_case
from piecewise_search import PanelRules,control_edges

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',type=int,default=3)
    parser.add_argument('--mask',type=int,nargs='+',default=[111,144])
    args = parser.parse_args()
    rules = PanelRules(json.loads((ROOT/'artifacts'/'panel_refinement_v2.json').read_text()))
    original = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    controls = [control_edges(rules,original,mask) for mask in range(4)]
    base = [p for _,p in child_maps()]
    cs = contacts(base)
    results = []
    for mask in args.mask:
        first,_ = mirrored_case(mask,base,cs)
        poses = first
        for _ in range(1,args.level):
            poses = [compose(p,q) for p in poses for q in first]
        print(f'mask {mask}: {len(poses)} tiles; extracting exact contacts',flush=True)
        current = contacts_fast(poses)
        constraints = rules.constrain(poses,current,False)
        accepted = [i for i,edges in enumerate(controls) if all(constraints.implies(a,b) for a,b in edges)]
        roots = sorted({constraints.find(i)[0] for i in range(rules.count)})
        colors = [[roots.index(constraints.find(rules.offsets[f]+i)[0])
                   for i in range(len(face))] for f,face in enumerate(rules.panels)]
        record = dict(mask=mask,level=args.level,tiles=len(poses),contacts=len(current),
                      dimension=constraints.dimension(),accepted_cells=accepted,canonical_panel_colors=colors)
        results.append(record)
        print(json.dumps(record),flush=True)
    out = dict(scope='Finite higher-level 60-panel equality candidates; no all-level enforcement claim',
               results=results,
               sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'periodic_obstruction.py',
                                  ROOT/'piecewise_search.py',ROOT/'reflected_search.py',ROOT/'reflected_controls.py',
                                  ROOT/'artifacts'/'geometry_and_constant_rules.json',
                                  ROOT/'artifacts'/'panel_refinement_v2.json',Path(__file__))})
    (ROOT/'artifacts'/f'piecewise_level_{args.level}.json').write_text(json.dumps(encode(out),indent=2)+'\n')


if __name__ == '__main__':
    main()

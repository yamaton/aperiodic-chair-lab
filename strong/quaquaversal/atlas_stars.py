"""Q007: finite root-face covers for the Q006 exact relative-pose rule.

These are an overapproximation of local stars, not infinite tilings. Only
root/neighbor contacts obey the atlas; neighbor/neighbor atlas compatibility
and coverage beyond the root's faces are not imposed.
"""

import hashlib
import json
from itertools import combinations
from pathlib import Path
import z3

from geometry import (F,I,ZERO,contacts,face_polygons,inverse_point,vertices,
                      separating_axis,area2,clip2,encode)
from polynomial_rules import COORDS
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    raw = json.loads((ROOT/'artifacts'/'contact_atlas.json').read_text())
    poses = [raw_pose(r['pose']) for r in raw['poses']]
    panelraw = json.loads((ROOT/'artifacts'/'panel_refinement_v2.json').read_text())
    panels = [[[tuple(F(x) for x in p) for p in poly] for poly in face] for face in panelraw['panels']]
    offsets = [sum(map(len,panels[:f])) for f in range(5)]
    footprints = []
    for i,pose in enumerate(poses):
        covered = set()
        for c in contacts([(I,ZERO,F(1)),pose]):
            f = c['fi']
            domain = [tuple(p[k] for k in COORDS[f]) for p in c['polygon']]
            for j,panel in enumerate(panels[f]):
                area = abs(area2(clip2(panel,domain)))
                if area:
                    assert area == abs(area2(panel)),(i,f,j)
                    covered.add(offsets[f]+j)
        assert covered
        footprints.append(sorted(covered))
    vs = [vertices(p) for p in poses]
    bounds = [tuple((min(p[k] for p in v),max(p[k] for p in v)) for k in range(3)) for v in vs]
    conflicts = []
    separation_checks = 0
    for i,j in combinations(range(len(poses)),2):
        if any(ahi <= blo or bhi <= alo for (alo,ahi),(blo,bhi) in zip(bounds[i],bounds[j])):
            continue
        separation_checks += 1
        if separating_axis(poses[i],poses[j]) is None:
            conflicts.append((i,j))
    print(f'{len(poses)} neighbors; {len(conflicts)} overlap conflicts; building root stars',flush=True)
    selected = [z3.Bool(f'n_{i}') for i in range(len(poses))]
    solver = z3.Solver()
    solver.set(timeout=10000)
    for k in range(sum(map(len,panels))):
        solver.add(z3.PbEq([(selected[i],1) for i,f in enumerate(footprints) if k in f],1))
    for i,j in conflicts:
        solver.add(z3.Or(z3.Not(selected[i]),z3.Not(selected[j])))
    stars = []
    max_models = 10000
    while len(stars) < max_models:
        status = solver.check()
        if status != z3.sat:
            break
        model = solver.model()
        indices = [i for i,v in enumerate(selected) if z3.is_true(model.eval(v,model_completion=True))]
        assert all(sum(k in footprints[i] for i in indices) == 1 for k in range(sum(map(len,panels))))
        assert not any(i in indices and j in indices for i,j in conflicts)
        stars.append(indices)
        solver.add(z3.Or([v != z3.is_true(model.eval(v,model_completion=True)) for v in selected]))
        if len(stars) % 1000 == 0:
            print('stars',len(stars),flush=True)
    complete = status == z3.unsat
    report = dict(scope='Overapproximation: root/neighbor atlas contacts and nonoverlap only; neighbor/neighbor atlas legality not imposed',
                  exact_cover_panels=sum(map(len,panels)),neighbors=len(poses),
                  footprints=footprints,overlap_conflicts=conflicts,separation_checks=separation_checks,
                  stars=stars,enumeration_complete=complete,
                  termination=str(status) if len(stars)<max_models else 'model_limit_unknown',
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'reflected_controls.py',
                                     ROOT/'artifacts'/'contact_atlas.json',ROOT/'artifacts'/'panel_refinement_v2.json',Path(__file__))})
    (ROOT/'artifacts'/'atlas_stars.json').write_text(json.dumps(encode(report),indent=2)+'\n')
    print(json.dumps(dict(stars=len(stars),enumeration_complete=complete,termination=report['termination'])),flush=True)


if __name__ == '__main__':
    main()

"""Small checker for Q022 cut certificates, without the extraction search."""

import hashlib
import json
from pathlib import Path

from geometry import compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'neighbor_star_cut_layer_1.json','neighbor_arc_cuts.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,layer,raw = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    used = {t for cut in raw['cuts'] for t,rs in cut['requirements']}
    used.update(r['tile'] for cut in raw['cuts'] for t,rs in cut['requirements'] for r in rs)
    poses = {t:raw_pose(layer['poses'][t]) for t in used}
    cases = [dict(row) for row in compat['cases']]
    options = [set(row['stars']) for row in compat['domains']]
    placements = steps = 0
    for cut in raw['cuts']:
        hypotheses = {tuple(a) for a in cut['antecedents']}
        assert len(hypotheses) == len(cut['antecedents'])
        ds = {}
        referenced = set()
        for target,reasons in cut['requirements']:
            assert target not in ds and reasons  # Each used tile is forced present.
            sets = []
            for r in reasons:
                tile,star = r['tile'],r['star']
                assert (tile,star) in hypotheses
                referenced.add((tile,star))
                if r['kind'] == 'selected_center':
                    assert poses[tile] == poses[target]
                    sets.append({star})
                else:
                    assert r['kind'] == 'neighbor'
                    q = r['pair']
                    assert q in language['stars'][star]['neighbors']
                    assert compose(poses[tile],atlas[q]) == poses[target]
                    placements += 1
                    sets.append(options[cases[star][q]])
            ds[target] = set.intersection(*sets)
        assert hypotheses == referenced
        for x,y,q in cut['reduction_trace']:
            assert x in ds and y in ds and compose(poses[x],atlas[q]) == poses[y]
            ds[x] = {s for s in ds[x] if q in cases[s] and options[cases[s][q]] & ds[y]}
            placements += 1
            steps += 1
        assert not ds[cut['target']]
    output = dict(scope='Standalone exact replay of Q022 necessary forbidden-conjunction certificates',
                  verified_cuts=len(raw['cuts']),exact_placements=placements,arc_steps=steps,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'neighbor_arc_cut_certificate_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

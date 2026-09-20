"""Compare Q023 oracle fixed domains with the independently replayed run."""

import hashlib
import json
from pathlib import Path

from geometry import F
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('neighbor_arc_cut_sat.json','neighbor_arc_sat_layer_1.json','neighbor_arc_sat_arcs.json',
             'neighbor_arc_sat_arcs_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    sat,layer,arcs,audit = [json.loads(p.read_text()) for p in paths]
    assert audit['sources'][paths[2].name] == hashlib.sha256(paths[2].read_bytes()).hexdigest()
    denom,scale = sat['pose_key_denominator'],F(sat['tile_scale'])
    lookup = {}
    for i,encoded in enumerate(layer['poses']):
        r,t,s = raw_pose(encoded)
        assert s == scale
        key = tuple(v*denom for row in r for v in row)+tuple(v*denom/scale for v in t)
        if all(v.denominator == 1 for v in key):
            lookup[tuple(map(int,key))] = i
    checked = 0
    for result in arcs['results']:
        model = sat['results'][result['source_index']]
        assert model['status'] == 'sat_passes_neighbor_arc_test'
        reported = {lookup[tuple(sat['normalized_pose_keys'][p])]:ss
                    for p,ss in model['rounds'][-1]['arc']['retained_domains']}
        replayed = {p:arcs['domain_pool'][di] for p,di in result['domains']}
        assert reported == replayed
        checked += len(replayed)
    output = dict(scope='Equality of every Q023 reported final arc domain with the independently audited generic run',
                  assignments=len(arcs['results']),domain_records=checked,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'arc_oracle_comparison.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

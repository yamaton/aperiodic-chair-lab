"""Combine audited narrowing with earlier geometric rejections for continuation.

This is a lossless view of surviving domains and their original pose table,
not a new search. Earlier geometric contradictions apply to the same fixed
parent-cover key even after further necessary domains were propagated.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'expanded_arc_consistency.json')
    parser.add_argument('--poses-source',type=Path,default=ROOT/'artifacts'/'forced_outer_layer_4.json')
    parser.add_argument('--geometry',type=Path,default=ROOT/'artifacts'/'forced_patch_geometry.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'expanded_arc_seed.json')
    args = parser.parse_args()
    paths = [args.poses_source,args.input,args.geometry]
    source,arcs,geometry = [json.loads(p.read_text()) for p in paths]
    bad = {(r['boundary_index'],r['cover_index']):i for i,r in enumerate(geometry['results'])
           if 'forbidden_pair_witness' in r}
    results = []
    counts = Counter()
    for ai,row in enumerate(arcs['results']):
        key = row['boundary_index'],row['cover_index']
        origin = source['results'][row['source_index']]
        assert key == (origin['boundary_index'],origin['cover_index'])
        record = dict(source_index=ai,boundary_index=key[0],cover_index=key[1])
        if 'domains' not in row:
            record['rejection'] = dict(kind='expanded_arc_trace',arc_result=ai)
            counts['arc_rejection'] += 1
        elif key in bad:
            record['rejection'] = dict(kind='earlier_geometric_witness',geometry_result=bad[key])
            counts['additional_geometry_rejection'] += 1
        else:
            assert {i for i,d in row['domains']} == {i for i,d in origin['domains']}
            record['domains'] = row['domains']
            counts['survivor'] += 1
        results.append(record)
    output = dict(scope='Continuation view combining earlier necessary exclusions, with unchanged retained pose/domain data',
                  poses=source['poses'],domain_pool=arcs['domain_pool'],results=results,status_counts=dict(counts),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),statuses=dict(counts))),flush=True)


if __name__ == '__main__':
    main()

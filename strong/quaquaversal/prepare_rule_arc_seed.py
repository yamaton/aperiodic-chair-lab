"""Lossless continuation view of an audited explicit-rule arc run."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'coarse_expanded_arcs_1.json')
    parser.add_argument('--source',type=Path,default=ROOT/'artifacts'/'coarse_forced_1.json')
    parser.add_argument('--audit',type=Path,default=ROOT/'artifacts'/'coarse_expanded_arcs_1_audit.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_arc_seed_1.json')
    args = parser.parse_args()
    paths = [args.source,args.input,args.audit]
    source,arcs,audit = [json.loads(p.read_text()) for p in paths]
    assert arcs['coordinate_level'] == source['coordinate_level']
    assert arcs['sources'][args.source.name] == hashlib.sha256(args.source.read_bytes()).hexdigest()
    assert audit['sources'][args.input.name] == hashlib.sha256(args.input.read_bytes()).hexdigest()
    seen = set()
    results,counts = [],Counter()
    for i,row in enumerate(arcs['results']):
        si = row['source_index']
        assert si not in seen
        seen.add(si)
        old = source['results'][si]
        assert (row['boundary_index'],row['cover_index']) == (old['boundary_index'],old['cover_index'])
        result = dict(source_index=i,boundary_index=row['boundary_index'],cover_index=row['cover_index'])
        if 'domains' in row:
            assert {t for t,di in row['domains']} == {t for t,di in old['domains']}
            result['domains'] = row['domains']
            counts['survivor'] += 1
        else:
            result['rejection'] = dict(kind='audited_arc_trace',result_index=i)
            counts['rejected'] += 1
        results.append(result)
    assert seen == {i for i,r in enumerate(source['results']) if 'domains' in r}
    output = dict(scope='Lossless view of an audited explicit-rule arc frontier',coordinate_level=source['coordinate_level'],
                  poses=source['poses'],domain_pool=arcs['domain_pool'],results=results,status_counts=dict(counts),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cases=len(results),**counts)),flush=True)


if __name__ == '__main__':
    main()

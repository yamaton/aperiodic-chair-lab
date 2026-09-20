"""Intersect two audited complete necessary frontiers, preserving fine domains."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fine',type=Path,default=ROOT/'artifacts'/'choice_cut_expanded_arcs_2.json')
    parser.add_argument('--fine-audit',type=Path,default=ROOT/'artifacts'/'choice_cut_expanded_arcs_2_audit.json')
    parser.add_argument('--poses-source',type=Path,default=ROOT/'artifacts'/'choice_cut_forced_2.json')
    parser.add_argument('--filter',type=Path,default=ROOT/'artifacts'/'coarse_star_arc_filter.json')
    parser.add_argument('--filter-audit',type=Path,default=ROOT/'artifacts'/'coarse_star_arc_audit.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'coarse_arc_frontier_1.json')
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/'coarse_parent_language.json',args.fine,args.fine_audit,args.poses_source,
             args.filter,args.filter_audit]
    loaded = {p:json.loads(p.read_text()) for p in dict.fromkeys(paths)}
    coarse,fine,fine_audit,pose_source,filtered,filter_audit = [loaded[p] for p in paths]
    assert fine_audit['sources'][args.fine.name] == hashlib.sha256(args.fine.read_bytes()).hexdigest()
    assert filter_audit['sources'][args.filter.name] == hashlib.sha256(args.filter.read_bytes()).hexdigest()
    if 'poses' in fine:
        assert fine['poses'] == pose_source['poses']
    else:
        assert fine['sources'][args.poses_source.name] == hashlib.sha256(args.poses_source.read_bytes()).hexdigest()
    by_key = {(r['boundary_index'],r['cover_index']):r['star'] for r in coarse['cover_stars']}
    active = set(filtered['final_active_stars'])
    results = []
    counts = dict(survivor=0,fine_rejection=0,coarse_rejection=0)
    for i,row in enumerate(fine['results']):
        key = row['boundary_index'],row['cover_index']
        star = by_key[key]
        result = dict(source_index=i,boundary_index=key[0],cover_index=key[1])
        if 'domains' not in row:
            result['rejection'] = dict(kind='inherited_fine_exclusion',result_index=i)
            counts['fine_rejection'] += 1
        elif star not in active:
            result['rejection'] = dict(kind='conditional_coarse_star',star=star)
            counts['coarse_rejection'] += 1
        else:
            result['domains'] = row['domains']
            counts['survivor'] += 1
        results.append(result)
    output = dict(scope='Intersection of audited full fine and conditional coarse frontiers; retained fine domains unchanged',
                  arguments={k:str(v) for k,v in vars(args).items()},poses=pose_source['poses'],
                  domain_pool=fine['domain_pool'],results=results,status_counts=counts,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(counts),flush=True)


if __name__ == '__main__':
    main()

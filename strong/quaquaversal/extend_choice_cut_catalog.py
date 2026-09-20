"""Combine audited cuts and record the new layered cut's finite effects."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    names = ('expanded_arcs_2_seed.json','choice_cut_frontier_seed.json','neighbor_arc_cut_sat.json',
             'neighbor_arc_sat_audit.json','layered_choice_certificate.json','layered_choice_certificate_audit.json')
    paths = [ROOT/'artifacts'/n for n in names]
    baseline,frontier,sat,sat_audit,proof,proof_audit = [json.loads(p.read_text()) for p in paths]
    assert sat_audit['sources'][paths[2].name] == hashlib.sha256(paths[2].read_bytes()).hexdigest()
    assert proof_audit['sources'][paths[4].name] == hashlib.sha256(paths[4].read_bytes()).hexdigest()
    assert frontier['poses'] == baseline['poses']
    assert sat['sources'][paths[0].name] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    cuts = [dict(antecedents=c['antecedents'],origin=dict(file=paths[2].name,index=i)) for i,c in enumerate(sat['cuts'])]
    new = proof['antecedents']
    assert new not in [c['antecedents'] for c in cuts]
    cuts.append(dict(antecedents=new,origin=dict(file=paths[4].name,root=proof['root'])))
    rejected_models = [i for i,r in enumerate(sat['results']) if
                       'selected_stars' in r and all(dict(r['selected_stars']).get(t) == s for t,s in new)]
    applications = []
    for i,row in enumerate(frontier['results']):
        if 'domains' not in row:
            continue
        ds = {t:frontier['domain_pool'][di] for t,di in row['domains']}
        if all(t in ds and s in ds[t] for t,s in new):
            applications.append(dict(source_index=i,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                                     unfixed_hypotheses=sum(len(ds[t]) > 1 for t,s in new)))
    output = dict(scope='Audited fixed-pose cut catalog; recorded model rejections are not parent exclusions',
                  cuts=cuts,rejected_q023_models=rejected_models,new_cut_frontier_applications=applications,
                  direct_parent_exclusions=sum(r['unfixed_hypotheses'] == 0 for r in applications),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'choice_cut_catalog_163.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(cuts=len(cuts),rejected_q023_models=rejected_models,
                          frontier_applications=applications)),flush=True)


if __name__ == '__main__':
    main()

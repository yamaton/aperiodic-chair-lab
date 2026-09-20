"""Q020 pilot: request complete stars around neighbors selected by SAT.

Freeze each finite SAT assignment's chosen stars at the existing centers.
One forced-neighbor step can then refute the assignment if an optional
neighbor has no compatible complete star. Parent cases are not preselected.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    paths = [ROOT/'artifacts'/name for name in ('expanded_arcs_2_seed.json','neighbor_incidence_geometry_sat.json')]
    source,sat = [json.loads(p.read_text()) for p in paths]
    pool,indices = [],{}
    results = []
    for mi,model in enumerate(sat['results']):
        if model['status'] != 'sat':
            continue
        origin = source['results'][model['source_index']]
        allowed = dict(origin['domains'])
        domains = []
        seen = set()
        for tile,star in model['selected_stars']:
            assert tile not in seen and star in source['domain_pool'][allowed[tile]]
            seen.add(tile)
            if star not in indices:
                indices[star] = len(pool)
                pool.append([star])
            domains.append((tile,indices[star]))
        assert seen == set(allowed)
        results.append(dict(source_index=mi,model_index=mi,boundary_index=model['boundary_index'],
                            cover_index=model['cover_index'],domains=domains))
    output = dict(scope='Selected finite SAT star assignments as hypotheses for complete-neighbor-star extension tests',
                  poses=source['poses'],domain_pool=pool,results=results,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (*paths,Path(__file__))})
    (ROOT/'artifacts'/'incidence_model_star_seed.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(assignments=len(results),singleton_star_domains=len(pool))),flush=True)


if __name__ == '__main__':
    main()

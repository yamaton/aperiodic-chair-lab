"""Q008: observed complete face-stars and periodic controls after subdivision.

Observed stars are a lower bound on the intended language. A periodic tiling
using only observed stars is a rigorous rejection of any rule that accepts
all those stars; a missing star is NOT a proof of aperiodicity.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import F,I,ZERO,child_maps,compose,contacts_fast,encode
from contact_atlas import relative
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample-level',type=int,default=3)
    parser.add_argument('--periodic-level',type=int,default=1)
    args = parser.parse_args()
    atlas_raw = json.loads((ROOT/'artifacts'/'contact_atlas.json').read_text())
    atlas = [raw_pose(r['pose']) for r in atlas_raw['poses']]
    atlas_id = {p:i for i,p in enumerate(atlas)}
    footprints = json.loads((ROOT/'artifacts'/'atlas_stars.json').read_text())['footprints']
    children = [p for _,p in child_maps()]
    patch = [(I,ZERO,F(1))]
    for _ in range(args.sample_level):
        patch = [compose(p,q) for p in patch for q in children]
    print(f'extracting sample contacts on {len(patch)} tiles',flush=True)
    neighbor_lists = [[] for _ in patch]
    for c in contacts_fast(patch):
        for i,j in ((c['i'],c['j']),(c['j'],c['i'])):
            k = atlas_id[relative(patch[i],patch[j])]
            neighbor_lists[i].append(k)
    observed = {}
    for i,star in enumerate(neighbor_lists):
        coverage = Counter(k for j in star for k in footprints[j])
        if len(coverage) == 60 and all(v == 1 for v in coverage.values()):
            observed.setdefault(tuple(sorted(star)),[]).append(i)
    periodic_raw = json.loads((ROOT/'artifacts'/'atlas_periodic_reflections.json').read_text())
    periods = tuple(F(x) for x in periodic_raw['periods'])
    def normalize(p):
        return p[0],tuple(x%d for x,d in zip(p[1],periods)),p[2]
    periodic = {normalize(raw_pose(p)) for p in periodic_raw['poses']}
    for _ in range(args.periodic_level):
        periodic = {normalize(compose(p,q)) for p in periodic for q in children}
    print(f'checking {len(periodic)} periodic tiles against {len(observed)} observed stars',flush=True)
    stars = []
    for i,p in enumerate(sorted(periodic)):
        star = tuple(j for j,q in enumerate(atlas) if normalize(compose(p,q)) in periodic)
        coverage = Counter(k for j in star for k in footprints[j])
        assert len(coverage) == 60 and all(v == 1 for v in coverage.values()),i
        stars.append(star)
    missing = sorted(set(stars)-set(observed))
    output = dict(scope='Observed complete face-stars only; sample incompleteness never proves exclusion',
                  arguments=vars(args),sample_tile_count=len(patch),observed_distinct_stars=len(observed),
                  observed=[dict(star=k,sample_tile_indices=v) for k,v in sorted(observed.items())],
                  periodic_tile_count=len(periodic),periodic_distinct_stars=len(set(stars)),
                  periodic_stars=[dict(star=k,count=v) for k,v in sorted(Counter(stars).items())],
                  not_observed=missing,periodic_control_uses_only_observed_stars=not missing,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',
                                     ROOT/'artifacts'/'contact_atlas.json',ROOT/'artifacts'/'atlas_stars.json',
                                     ROOT/'artifacts'/'atlas_periodic_reflections.json',Path(__file__))})
    out = ROOT/'artifacts'/f'star_language_{args.sample_level}_{args.periodic_level}.json'
    out.write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps(dict(observed=len(observed),periodic_stars=len(set(stars)),
                          not_observed=len(missing),counterexample=not missing)),flush=True)


if __name__ == '__main__':
    main()

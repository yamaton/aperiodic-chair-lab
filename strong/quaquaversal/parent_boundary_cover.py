"""Q012: recover neighboring parents as a finite boundary exact-cover problem.

The already proved one-level grouping supplies necessary role/parent support
constraints. Every child of a neighboring parent touching the root parent
must be present in the eight-child neighborhood, with the correct role.
We enumerate covers of these external children, excluding intersecting
parent interiors. A finite cap remains unknown, never a rejection.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import I,ZERO,F,child_maps,compose,encode
from contact_atlas import relative
from reflected_controls import raw_pose
from audit_closed_atlas import edge_points,dimension
from closed_stars import bounds,disjoint

ROOT = Path(__file__).resolve().parent
IDENTITY = I,ZERO,F(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=10000,help='Maximum covers per neighborhood; hitting it is unknown')
    parser.add_argument('--arcs',action='store_true',help='Use the stronger exterior arc-consistency domains')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'parent_boundary_cover.json')
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/name for name in
             ('closed_contact_atlas.json','closed_star_language.json','closed_star_audit.json',
              'closed_star_compatibility.json','parent_external_domains.json','parent_join_filter.json')]
    atlas_raw,language,audit,compat,external,joined = [json.loads(p.read_text()) for p in paths]
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    atlas_index = {p:i for i,p in enumerate(atlas)}
    legal = {tuple(s['neighbors']):i for i,s in enumerate(language['stars'])}
    children = [p for _,p in child_maps()]
    inverse = [relative(p,IDENTITY) for p in children]
    world = [raw_pose(p) for p in external['poses']]
    world_index = {p:i for i,p in enumerate(world)}
    role_bits = [sum(1<<s for s,r in enumerate(audit['child_roles']) if r == [i]) for i in range(8)]
    bits = [sum(1<<s for s in d['stars']) for d in compat['domains']]
    arc_by_external = None
    if args.arcs:
        arc_path = ROOT/'artifacts'/'parent_star_arc_consistency.json'
        paths.append(arc_path)
        arcs = json.loads(arc_path.read_text())
        arc_by_external = {r['external_index']:r for r in arcs['results'] if 'domains' in r}
        arc_bits = [sum(1<<s for s in ss) for ss in arcs['domain_pool']]
    sources = [(i,row) for i,row in enumerate(external['survivors'])
               if arc_by_external is None or i in arc_by_external]
    domains = []
    proposals = set()
    for external_index,row in sources:
        roles = {}
        if arc_by_external is None:
            values = {}
            for d in row['external_domains']:
                value = bits[d['domains'][0]]
                for di in d['domains'][1:]:
                    value &= bits[di]
                values[d['tile']] = value
        else:
            values = {tile:arc_bits[di] for tile,di in arc_by_external[external_index]['domains'] if tile >= 8}
        for tile,value in values.items():
            possible = tuple(i for i,rs in enumerate(role_bits) if value & rs)
            assert possible
            roles[tile] = possible
            proposals.update((tile,i) for i in possible)
        domains.append(roles)
    parents = []
    parent_index = {}
    proposal_parent = {}
    for tile,role in sorted(proposals):
        p = compose(world[tile],inverse[role])
        if p not in parent_index:
            parent_index[p] = len(parents)
            parents.append(p)
        proposal_parent[tile,role] = parent_index[p]
    root_bounds = bounds(IDENTITY)
    requirements = []
    unusable = []
    for pi,p in enumerate(parents):
        d = dimension(edge_points(p))
        if d not in (0,1,2):
            requirements.append(None)
            unusable.append(dict(parent=pi,reason='root_intersection_dimension',dimension=d))
            continue
        needed = []
        missing = []
        for role,c in enumerate(children):
            q = compose(p,c)
            if not disjoint(root_bounds,bounds(q)) and edge_points(q,first_only=True):
                if q in world_index:
                    needed.append((world_index[q],role))
                else:
                    missing.append(role)
        if missing:
            requirements.append(None)
            unusable.append(dict(parent=pi,reason='child_outside_global_catalog',roles=missing))
        else:
            assert needed
            requirements.append(needed)
        if (pi+1)%250 == 0:
            print(f'parent supports: {pi+1}/{len(parents)}',flush=True)
    p_bounds = [bounds(p) for p in parents]
    overlap_cache = {}
    def overlaps(i,j):
        key = tuple(sorted((i,j)))
        if key not in overlap_cache:
            overlap_cache[key] = (False if disjoint(p_bounds[i],p_bounds[j]) else
                                  dimension(edge_points(relative(parents[i],parents[j]))) == 3)
        return overlap_cache[key]
    results = []
    statuses = Counter()
    genuine_seen = set()
    for si,((external_index,source),roles) in enumerate(zip(sources,domains)):
        potential = {proposal_parent[tile,role] for tile,rs in roles.items() for role in rs}
        admissible = {pi for pi in potential if requirements[pi] is not None and
                      all(role in roles.get(tile,()) for tile,role in requirements[pi])}
        masks = {pi:frozenset(tile for tile,role in requirements[pi]) for pi in admissible}
        incident = {tile:sorted(pi for pi in admissible if tile in masks[pi]) for tile in roles}
        covers = []
        capped = False
        nodes = 0
        def search(uncovered,chosen):
            nonlocal capped,nodes
            nodes += 1
            if not uncovered:
                ids = [atlas_index.get(parents[pi]) for pi in chosen]
                star = tuple(sorted(ids)) if all(i is not None for i in ids) else None
                legal_id = legal.get(star)
                covers.append(dict(parents=sorted(chosen),legal_star=legal_id))
                if legal_id is not None:
                    genuine_seen.add(legal_id)
                if len(covers) >= args.limit:
                    capped = True
                return
            choices = {}
            for tile in uncovered:
                choices[tile] = [pi for pi in incident[tile] if masks[pi] <= uncovered and
                                 not any(overlaps(pi,q) for q in chosen)]
            tile = min(uncovered,key=lambda t:(len(choices[t]),t))
            for pi in choices[tile]:
                search(uncovered-masks[pi],chosen+[pi])
                if capped:
                    return
        search(frozenset(roles),[])
        status = 'unknown_at_cover_limit' if capped else ('no_cover' if not covers else
                 'all_covers_legal' if all(c['legal_star'] is not None for c in covers) else 'nonlanguage_covers_remain')
        statuses[status] += 1
        results.append(dict(external_index=external_index,tuple_index=source['tuple_index'],status=status,
                            role_domains=sorted(roles.items()),admissible_parents=sorted(admissible),
                            search_nodes=nodes,covers=covers))
        if (si+1)%1000 == 0:
            print(f'boundary covers: {si+1}/{len(domains)}; {dict(statuses)}',flush=True)
    # A capped enumeration must not be mistaken for failed genuine coverage.
    # Independently insert/check every known legal parent-star witness, even
    # if the search stopped before reaching it in that case.
    result_by_tuple = {tuple(joined['survivors'][r['tuple_index']]):r for r in results}
    genuine_witnesses = []
    for li,(star,child_tuple) in enumerate(zip(language['stars'],audit['transitions'],strict=True)):
        result = result_by_tuple[tuple(child_tuple)]
        chosen = [parent_index[atlas[q]] for q in star['neighbors']]
        assert set(chosen) <= set(result['admissible_parents'])
        covered = [tile for pi in chosen for tile,role in requirements[pi]]
        expected = {tile for tile,roles in result['role_domains']}
        assert len(covered) == len(set(covered)) and set(covered) == expected
        if li not in genuine_seen:
            assert result['status'] == 'unknown_at_cover_limit'
        genuine_witnesses.append(dict(legal_star=li,tuple_index=result['tuple_index'],parents=chosen))
    output = dict(scope='Necessary parent-boundary covers from recognized external child roles; nonlanguage survivors are unresolved',
                  arguments={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
                  parents=parents,requirements=requirements,unusable_parents=unusable,
                  overlapping_parent_pairs=[k for k,v in sorted(overlap_cache.items()) if v],
                  results=results,status_counts=dict(statuses),genuine_parent_stars_enumerated=len(genuine_seen),
                  genuine_parent_witnesses=genuine_witnesses,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'contact_atlas.py',ROOT/'reflected_controls.py',
                            ROOT/'audit_closed_atlas.py',ROOT/'closed_stars.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(encode(output),separators=(',',':'))+'\n')
    print(json.dumps(dict(parents=len(parents),unusable=len(unusable),statuses=dict(statuses),
                          recovered_legal_stars=len(genuine_seen))),flush=True)


if __name__ == '__main__':
    main()

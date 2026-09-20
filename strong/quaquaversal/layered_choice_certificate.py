"""Q026: extract a choice proof through forced and arc propagation layers.

Nodes certify necessary domains at positions whose presence is also tracked.
An omitted hypothesis is unknown, not a tile with an asserted empty domain.
Forced-neighbor nodes require their pair in EVERY source star; their target
domain is a UNION of compatible-star sets. Intersections and arc restrictions
then combine independently necessary consequences.
"""

import hashlib
import json
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

from geometry import compose
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    names = ('closed_contact_atlas.json','closed_star_language.json','closed_star_compatibility.json',
             'neighbor_star_cut_seed.json','neighbor_star_cut_layer_1.json','neighbor_star_cut_arcs.json',
             'neighbor_star_cut_layer_2.json','neighbor_star_cut_arcs_2.json')
    paths = [ROOT/'artifacts'/n for n in names]
    atlas_raw,language,compat,seed,layer1,arcs1,layer2,arcs2 = [json.loads(p.read_text()) for p in paths]
    assert layer2['poses'][:len(layer1['poses'])] == layer1['poses']
    assert layer1['poses'][:len(seed['poses'])] == seed['poses']
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    poses = [raw_pose(p) for p in layer2['poses']]
    lookup = {p:i for i,p in enumerate(poses)}
    cases = [dict(row) for row in compat['cases']]
    options = [frozenset(row['stars']) for row in compat['domains']]
    selected = {t:seed['domain_pool'][di][0] for t,di in seed['results'][5]['domains']}
    assert all(len(seed['domain_pool'][di]) == 1 for t,di in seed['results'][5]['domains'])
    a1 = arcs1['results'][5]
    a2 = arcs2['results'][0]
    assert (a1['boundary_index'],a1['cover_index']) == (515,0) == (a2['boundary_index'],a2['cover_index'])
    input_domains = {
        1:{t:frozenset([s]) for t,s in selected.items()},
        2:{t:frozenset(arcs1['domain_pool'][di]) for t,di in a1['domains']},
    }
    output_domains = {
        1:{t:frozenset(layer1['domain_pool'][di]) for t,di in layer1['results'][5]['domains']},
        2:{t:frozenset(layer2['domain_pool'][di]) for t,di in layer2['results'][0]['domains']},
    }
    initial_refs = {t:('selected',t) for t in selected}
    source_refs = {1:initial_refs}
    arc_dependencies = {}
    final_refs = {}
    for stage,raw in ((1,a1),(2,a2)):
        refs = {t:('forced',stage,t) for t in output_domains[stage]}
        for step,(x,y,q) in enumerate(raw['reduction_trace']):
            ref = ('arc',stage,step)
            arc_dependencies[ref] = refs[x],refs[y],q,x
            refs[x] = ref
        final_refs[stage] = refs
        if stage == 1:
            source_refs[2] = refs
    forcing = {}
    for stage,ds in input_domains.items():
        requirements = defaultdict(list)
        for tile,ss in ds.items():
            for q in sorted(set.intersection(*(set(cases[s]) for s in ss))):
                target = lookup[compose(poses[tile],atlas[q])]
                requirements[target].append((tile,q))
        forcing[stage] = requirements
        print(json.dumps(dict(stage=stage,forced_requirements=sum(map(len,requirements.values())))),flush=True)
    nodes,values = [],[]

    def add(node,value):
        i = len(nodes)
        nodes.append(node)
        values.append(value)
        return i

    @cache
    def visit(ref):
        if ref[0] == 'selected':
            tile = ref[1]
            return add(dict(op='choice',pose=tile,tile=tile,star=selected[tile]),frozenset([selected[tile]]))
        if ref[0] == 'arc':
            left,right,q,tile = arc_dependencies[ref]
            x,y = visit(left),visit(right)
            assert compose(poses[nodes[x]['pose']],atlas[q]) == poses[nodes[y]['pose']]
            value = frozenset(s for s in values[x] if q in cases[s] and options[cases[s][q]] & values[y])
            return add(dict(op='arc',pose=tile,left=x,right=y,pair=q),value)
        _,stage,tile = ref
        inputs = []
        if tile in source_refs[stage]:
            inputs.append(visit(source_refs[stage][tile]))
        for source,q in forcing[stage][tile]:
            parent = visit(source_refs[stage][source])
            assert values[parent] == input_domains[stage][source]
            assert all(q in cases[s] for s in values[parent])
            value = frozenset(t for s in values[parent] for t in options[cases[s][q]])
            inputs.append(add(dict(op='neighbor',pose=tile,source=parent,pair=q),value))
        assert inputs
        value = frozenset.intersection(*(values[i] for i in inputs))
        assert value == output_domains[stage][tile]
        return add(dict(op='meet',pose=tile,inputs=inputs),value)

    root = visit(final_refs[2][a2['rejection']['tiles'][0]])
    assert not values[root]
    hypotheses = {(n['tile'],n['star']) for n in nodes if n['op'] == 'choice'}

    def replay(kept):
        # None means no certified tile presence. Every set, including the
        # empty set, means present with that necessary domain restriction.
        ds = []
        for n in nodes:
            op = n['op']
            if op == 'choice':
                value = frozenset([n['star']]) if (n['tile'],n['star']) in kept else None
            elif op == 'neighbor':
                src,q = ds[n['source']],n['pair']
                value = (frozenset(t for s in src for t in options[cases[s][q]])
                         if src is not None and all(q in cases[s] for s in src) else None)
            elif op == 'meet':
                known = [ds[i] for i in n['inputs'] if ds[i] is not None]
                value = frozenset.intersection(*known) if known else None
            else:
                left,right,q = ds[n['left']],ds[n['right']],n['pair']
                value = (left if left is None or right is None else
                         frozenset(s for s in left if q in cases[s] and options[cases[s][q]] & right))
            ds.append(value)
        return ds[root] is not None and not ds[root]

    before = len(hypotheses)
    assert replay(hypotheses)
    for choice in sorted(hypotheses):
        if replay(hypotheses-{choice}):
            hypotheses.remove(choice)
    assert replay(hypotheses)
    output = dict(scope='Necessary choice contradiction through two forced layers and two arc traces; not a parent exclusion',
                  boundary_index=515,cover_index=0,model_index=5,antecedents=sorted(hypotheses),
                  unminimized_choices=before,nodes=nodes,root=root,
                  node_counts=dict(Counter(n['op'] for n in nodes)),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    (ROOT/'artifacts'/'layered_choice_certificate.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps(dict(nodes=len(nodes),initial_choices=before,cut_choices=len(hypotheses),
                          node_counts=output['node_counts'])),flush=True)


if __name__ == '__main__':
    main()

"""Audit chirality, cycle balance and freedoms from frozen port geometry.

No project implementation imports. The synthesis table selects contact subsets;
positions, rotations, frames and all geometric contact pairs are rebuilt here.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import permutations, product, combinations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def act(r, p):
    return tuple(dot(r[i:i+3], p) for i in (0, 3, 6))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(k, p):
    return tuple(k*x for x in p)


def path(tree, start, end):
    queue = deque([start])
    previous = {start: None}
    while queue:
        a = queue.popleft()
        if a == end:
            result = [end]
            while previous[result[-1]] is not None:
                result.append(previous[result[-1]])
            return result[::-1]
        for b in sorted(tree[a]):
            if b not in previous:
                previous[b] = a
                queue.append(b)
    raise AssertionError('Disconnected path')


def graph(vertices, edges):
    adjacency = {i: set() for i in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen = set(vertices)
    components = []
    while unseen:
        root = min(unseen)
        signs = {root: 1}
        queue = [root]
        tree = {i: set() for i in vertices}
        balanced = True
        for a in queue:
            for b in sorted(adjacency[a]):
                if b not in signs:
                    signs[b] = -signs[a]
                    tree[a].add(b)
                    tree[b].add(a)
                    queue.append(b)
                elif signs[b] != -signs[a]:
                    balanced = False
        unseen.difference_update(queue)
        es = [e for e in edges if e[0] in signs]
        tree_edges = {tuple(sorted((a, b))) for a in queue for b in tree[a]}
        cycles = [path(tree, a, b) for a, b in es if (a, b) not in tree_edges]
        # Each path plus its omitted edge is a fundamental cycle.
        assert balanced == all(len(c) % 2 == 0 for c in cycles)
        components.append(dict(nodes=sorted(queue), edges=len(es), balanced=balanced,
                               rank=len(queue)-(1 if balanced else 0),
                               nullity=1 if balanced else 0,
                               cycle_dimension=len(es)-len(queue)+1,
                               fundamental_cycle_lengths=dict(sorted(Counter(map(len, cycles)).items())),
                               positive=sum(s == 1 for s in signs.values()),
                               negative=sum(s == -1 for s in signs.values()),
                               first_cycle=cycles[0] if cycles else []))
    return components


def main():
    raw = (HERE/'frozen_v1/candidate.json').read_bytes()
    d = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((HERE/'frozen_v1/manifest.json').read_text())['candidate_sha256']
    ports = [dict(c=tuple(int(16*Fraction(x)) for x in p['center']),
                  n=tuple(p['outward_normal']), u=tuple(p['u_axis']), v=tuple(p['v_axis']))
             for p in d['ports']]
    lookup = {(p['c'], p['n']): i for i, p in enumerate(ports)}
    chi = [dot(cross(p['u'], p['v']), p['n']) for p in ports]
    assert set(chi) == {-1, 1}
    rotations = []
    for axes in permutations(range(3)):
        parity = (-1)**sum(axes[i] > axes[j] for i in range(3) for j in range(i+1, 3))
        for signs in product((-1, 1), repeat=3):
            if parity*signs[0]*signs[1]*signs[2] == 1:
                rotations.append(tuple(signs[i] if j == axes[i] else 0 for i in range(3) for j in range(3)))
    cubes = {tuple(2*x+1 for x in c) for c in d['coarse_cubes']}
    types = []
    for shift in product(range(-2, 3), repeat=3):
        for r in rotations:
            if cubes & {add(scale(2, shift), act(r, q)) for q in cubes}:
                continue
            pairs = []
            for j, p in enumerate(ports):
                i = lookup.get((add(scale(16, shift), act(r, p['c'])), scale(-1, act(r, p['n']))))
                if i is not None:
                    assert ports[i]['u'] == act(r, p['u'])
                    assert ports[i]['v'] == act(r, p['v'])
                    assert chi[i] == -chi[j]
                    pairs.append((i, j))
            if pairs:
                types.append((shift, r, pairs))
    assert len(types) == 1194
    lab = json.loads((ROOT/'docs/assembly/rule-data.json').read_text())
    assert [(list(t), list(r)) for t, r, _ in types] == [(p['shift'], p['rotation']) for p in lab['poses']]
    all_edges = sorted({tuple(sorted(e)) for _, _, pairs in types for e in pairs})
    universal = graph(range(192), all_edges)
    assert len(universal) == 1 and universal[0]['nullity'] == 1
    assert len(all_edges) == 7740

    # Intrinsic permutations of the eight port sites on every face, not rigid
    # symmetries of the decorated solid. Signed permutations of (u,v) form D4.
    site_permutations = []
    for swap, su, sv in product((False, True), (-1, 1), (-1, 1)):
        perm = []
        for p in ports:
            f = tuple(x if p['n'][i] else 16*(x//16)+8 for i, x in enumerate(p['c']))
            u, v = (p['v'], p['u']) if swap else (p['u'], p['v'])
            q = add(f, add(scale(3*su, u), scale(sv, v)))
            perm.append(lookup[q, p['n']])
        assert len(set(perm)) == 192
        site_permutations.append(perm)

    synth = json.loads((ROOT/'strong/artifacts/chair_recut_synthesis.json').read_text())
    profiles = []
    for index, p in enumerate(synth['profiles']):
        edges = sorted({tuple(sorted(e)) for t in p['closed_contact_types'] for e in types[t][2]})
        assert edges == [tuple(e) for e in lab['profiles'][index]['edges']]
        components = graph(range(192), edges)
        edge_set = set(edges)
        for c in components:
            assert c['balanced'] and c['positive'] == c['negative']
            assert len({abs(p['labels'][n]) for n in c['nodes']}) == 1
            assert len({chi[n]*(1 if p['labels'][n] > 0 else -1) for n in c['nodes']}) == 1
        component_id = {v: i for i, c in enumerate(components) for v in c['nodes']}
        actions = []
        for perm in site_permutations:
            assert {tuple(sorted((perm[a], perm[b]))) for a, b in edges} == edge_set
            actions.append([component_id[perm[c['nodes'][0]]] for c in components])
        orbits = []
        unseen = set(range(len(components)))
        while unseen:
            orbit = sorted({a[min(unseen)] for a in actions})
            unseen.difference_update(orbit)
            orbits.append(orbit)
        profiles.append(dict(index=index, components=components, edges=len(edges),
                             rank=sum(c['rank'] for c in components), nullity=len(components),
                             dependencies=sum(c['cycle_dimension'] for c in components),
                             site_D4_automorphisms=8, component_orbits=orbits))

    # Negative control: an abstract same-chirality chord, forbidden by the
    # geometry, makes an odd cycle. Homogeneous solutions then vanish on it.
    comp = profiles[1]['components'][0]
    edges = [tuple(e) for e in lab['profiles'][1]['edges'] if e[0] in comp['nodes']]
    a, b = next((a, b) for a, b in combinations(comp['nodes'], 2) if chi[a] == chi[b])
    bad = graph(comp['nodes'], sorted(edges+[(a, b)]))
    assert len(bad) == 1 and not bad[0]['balanced'] and bad[0]['nullity'] == 0
    volume_coefficient = Fraction(d['half_width'])**2 * Fraction(d['height_unit']) * Fraction(16, 9)
    # All equations are homogeneous: the odd cycle forces zero, not literal
    # inconsistency unless a nonzero port amplitude is required.
    report = dict(status='passed', candidate_sha256=digest,
                  implementation='Standalone standard-library coordinate reconstruction; no project implementation imports.',
                  geometric_contacts=len(types), all_pair_edges=len(all_edges),
                  frame_mismatches=0, chirality_violations=0, universal_graph=universal,
                  profiles=profiles,
                  cap_signed_volume_per_unit_key=str(volume_coefficient),
                  every_profile_component_has_equal_positive_negative_counts=True,
                  odd_chord_control=dict(added_edge=[a,b],same_chirality=chi[a],
                                         geometric_edge=False, result=bad[0]),
                  scope='Proper grid port constraints, cycle ranks, intrinsic port permutations and balanced signs. Not a deflation, recognizability or physical-solid proof.')
    target = HERE/'constraint_balance.json'
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status','geometric_contacts','all_pair_edges','frame_mismatches','chirality_violations')}))
    print(json.dumps([dict(profile=p['index'],rank=p['rank'],nullity=p['nullity'],dependencies=p['dependencies'],D4_orbit_sizes=list(map(len,p['component_orbits']))) for p in profiles]))
    print('Odd-chord control: 1 freedom -> 0; only the all-zero solution remains in that component.')


if __name__ == '__main__':
    main()

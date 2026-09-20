"""Replay pointwise periodic certificates without the groupoid search.

Checks affine maps on spanning corner sets, every word in actual contact
generators, odd zero cycles, full periodic face coverage, and periodic
handedness assignments. Generator provenance is rebuilt geometrically.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from geometry import F,child_maps,compose,contacts,contacts_fast,area2,encode
from reflected_search import MIRROR,mirrored_case
from reflected_controls import raw_pose
from polynomial_rules import contact_map
from periodic_obstruction import affine,act

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT/'artifacts'/'pointwise_groupoid_all.json'
    raw = json.loads(path.read_text())
    panel_path = ROOT/'artifacts'/'panel_refinement_v2.json'
    geometry_path = ROOT/'artifacts'/'geometry_and_constant_rules.json'
    panel_raw = json.loads(panel_path.read_text())
    face_of = [f for f,panels in enumerate(panel_raw['panels']) for p in panels]
    areas = [abs(area2([tuple(F(x) for x in p) for p in panel]))
             for panels in panel_raw['panels'] for panel in panels]
    corners = [[tuple(F(x) for x in p) for p in ps] for ps in raw['panel_corners']]
    maps = raw['maps']
    for g in maps:
        g['affine'] = tuple(tuple(F(x) for x in row) for row in g['affine'])
        a,b = g['source'],g['target']
        assert sorted(g['permutation']) == list(range(len(corners[b])))
        assert len(corners[a]) == len(corners[b]) >= 3
        for i,p in enumerate(corners[a]):
            assert act(g['affine'],p) == corners[b][g['permutation'][i]]
        assert any((q[0]-corners[a][0][0])*(r[1]-corners[a][0][1]) !=
                   (q[1]-corners[a][0][1])*(r[0]-corners[a][0][0])
                   for q in corners[a] for r in corners[a])
        # Certificate corners must span exactly their original panel domain.
        f = face_of[a]
        local = a-sum(len(ps) for ps in panel_raw['panels'][:f])
        poly = [tuple(F(x) for x in p) for p in panel_raw['panels'][f][local]]
        assert set(corners[a]) <= set(poly)
        from pointwise_groupoid import corners as extreme_corners
        assert tuple(corners[a]) == extreme_corners(poly)
    def signature(g):
        return face_of[g['source']],face_of[g['target']],g['affine']
    geo = json.loads(geometry_path.read_text())
    cell = [raw_pose(p) for p in geo['periodic_control']['cell']]
    for t,c in zip(raw['periodic_tables'],geo['periodic_control']['contacts'],strict=True):
        assert (t['tile'],t['neighbor'],t['offset']) == (c['tile'],c['neighbor'],c['offset'])
        for option in t['options']:
            ha,hb = option['handedness']
            p,q = cell[c['tile']],cell[c['neighbor']]
            if ha:
                p = compose(p,MIRROR)
            if hb:
                q = compose(q,MIRROR)
            q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
            fi = 1-c['fi'] if ha and c['fi'] < 2 else c['fi']
            fj = 1-c['fj'] if hb and c['fj'] < 2 else c['fj']
            actual = fi,fj,affine(contact_map([p,q],dict(i=0,j=1,fi=fi,fj=fj)))
            assert not option['partial_panels']
            assert all(signature(maps[k]) == actual for k in option['maps'])
            covered = [maps[k]['source'] for k in option['maps']]
            assert len(covered) == len(set(covered))
            assert set(covered) == {i for i,f in enumerate(face_of) if f == fi}
    def walk(start,word,allowed):
        current = start
        perm = list(range(len(corners[start])))
        for edge in word:
            k = abs(edge)-1
            assert k in allowed
            g = maps[k]
            a,b,q = g['source'],g['target'],g['permutation']
            if edge < 0:
                a,b,q = b,a,[q.index(i) for i in range(len(q))]
            assert a == current
            perm = [q[j] for j in perm]
            current = b
        return current,perm,len(word)%2
    base = [p for _,p in child_maps()]
    cs = contacts(base)
    checked_masks = {}
    derivations = 0
    periodic_contacts = 0
    for entry in raw['results']:
        allowed = set(entry['generators'])
        if entry['mask'] not in checked_masks:
            first,_ = mirrored_case(entry['mask'],base,cs)
            poses = first
            for _ in range(1,entry['level']):
                poses = [compose(p,q) for p in poses for q in first]
            actual = {(c['fi'],c['fj'],affine(contact_map(poses,c))) for c in contacts_fast(poses)}
            assert all(signature(maps[k]) in actual for k in allowed)
            checked_masks[entry['mask']] = (entry['level'],allowed)
            if len(checked_masks)%32 == 0:
                print(f'generator words audited: {len(checked_masks)}/256',flush=True)
        else:
            assert checked_masks[entry['mask']] == (entry['level'],allowed)
        signed = entry['condition'] == 'opposite'
        proof_options = set()
        for proof in entry['proofs']:
            ti = proof['table']
            hands = tuple(proof['handedness'])
            option = next(o for o in raw['periodic_tables'][ti]['options'] if tuple(o['handedness']) == hands)
            assert [d['map'] for d in proof['derivations']] == option['maps']
            for d in proof['derivations']:
                g = maps[d['map']]
                a,b = g['source'],g['target']
                if 'path' in d:
                    target,perm,parity = walk(a,d['path'],allowed)
                    assert (target,perm) == (b,g['permutation']) and (not signed or parity == 1)
                else:
                    assert signed
                    for s,name in ((a,'source_zero_cycle'),(b,'target_zero_cycle')):
                        assert walk(s,d[name],allowed) == (s,list(range(len(corners[s]))),1)
                derivations += 1
            proof_options.add((ti,hands))
        expected = {(i,tuple(h)) for i,hs in enumerate(entry['allowed_handedness_pairs']) for h in hs}
        assert proof_options == expected
        witness = entry['witness']
        assert witness is not None
        size = witness['size']
        values = {tuple(a['site']):a['handedness'] for a in witness['assignments']}
        from itertools import product
        boxes = list(product(*(range(n) for n in size)))
        assert set(values) == {b+(i,) for b in boxes for i in (0,1)}
        for box in boxes:
            for ti,t in enumerate(raw['periodic_tables']):
                a = box+(t['tile'],)
                b = tuple((x+d)%n for x,d,n in zip(box,t['offset'],size))+(t['neighbor'],)
                assert (ti,(values[a],values[b])) in proof_options
                periodic_contacts += 1
    assert len(checked_masks) == 256 and len(raw['results']) == 512
    output = dict(scope='Exact replay of all 512 arbitrary-scalar-function periodic obstructions',
                  masks=len(checked_masks),families=len(raw['results']),maps=len(maps),
                  checked_derivations=derivations,checked_periodic_contacts=periodic_contacts,
                  witness_sizes=[dict(condition=c,size=s,count=n) for (c,s),n in
                                 Counter((e['condition'],tuple(e['witness']['size'])) for e in raw['results']).items()],
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_search.py',ROOT/'reflected_controls.py',
                            ROOT/'polynomial_rules.py',ROOT/'periodic_obstruction.py',ROOT/'pointwise_groupoid.py',
                            path,panel_path,geometry_path,Path(__file__))})
    (ROOT/'artifacts'/'pointwise_groupoid_audit.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'sources'}),flush=True)


if __name__ == '__main__':
    main()

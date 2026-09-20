"""Q002b: piecewise exact certificate for arbitrary pointwise face markings.

Every contact in a two-prism periodic filling follows from an odd-length
chain of sibling identifications. This covers equality colors and any fixed
involutive complement (including signed normal height), without a polynomial
or continuity assumption. It does not classify recuts lacking this carrier.
"""

import hashlib
import json
from pathlib import Path

from geometry import (F,FACE_NAMES,child_maps,contacts,encode,inverse_point,
                      area2,clip2,vec,vertices)
from polynomial_rules import COORDS,contact_map,A,B

ROOT = Path(__file__).resolve().parent


def rational(x):
    return F(int(x.p),int(x.q))


def affine(expr):
    return tuple((rational(p.coeff(A)),rational(p.coeff(B)),rational(p.subs({A:0,B:0})))
                 for p in expr)


def act(mapping,p):
    return tuple(a*p[0]+b*p[1]+c for a,b,c in mapping)


def in_polygon(p,poly):
    orientation = 1 if area2(poly) > 0 else -1
    return all(orientation*((q[0]-r[0])*(p[1]-r[1])-(q[1]-r[1])*(p[0]-r[0])) >= 0
               for r,q in zip(poly,poly[1:]+poly[:1]))


def main():
    named = child_maps()
    poses = [p for _,p in named]
    cs = contacts(poses)
    edges = {}
    for c in cs:
        name = named[c['i']][0]+'-'+named[c['j']][0]
        for reverse in (False,True):
            cc = dict(c)
            if reverse:
                cc.update(i=c['j'],j=c['i'],fi=c['fj'],fj=c['fi'])
            poly = [tuple(inverse_point(poses[cc['i']],p)[k] for k in COORDS[cc['fi']])
                    for p in c['polygon']]
            edges[name+('-reverse' if reverse else '')] = dict(
                source=cc['fi'],target=cc['fj'],domain=poly,
                map=affine(contact_map(poses,cc)))
    square = [vec(0,0),vec(1,0),vec(1,1),vec(0,1)]
    triangle = [vec(0,0),vec(1,0),vec(0,1)]
    lower = [vec(0,0),vec(1,0),vec(1,1)]
    upper = [vec(0,0),vec(1,1),vec(0,1)]
    candidates = [
        (1,0,triangle,['1A-1B']),
        (0,1,triangle,['1A-1B-reverse']),
        (4,4,square,['2A-3A']),
        (3,3,square,['1A-2A','1B-2B','1A-2A']),
        (2,2,lower,['2A-4A-reverse','3A-4A','3B-4B']),
        (2,2,upper,['3A-4A-reverse','2A-4A','3B-4B']),
    ]
    proofs = []
    for source,target,domain,path in candidates:
        current_face = source
        poly = list(domain)
        probes = [vec(0,0),vec(1,0),vec(0,1)]
        for name in path:
            e = edges[name]
            assert current_face == e['source']
            assert all(in_polygon(p,e['domain']) for p in poly)
            poly = [act(e['map'],p) for p in poly]
            probes = [act(e['map'],p) for p in probes]
            current_face = e['target']
        assert current_face == target
        expected = (lambda p:p) if source in (0,1) else (lambda p:(1-p[0],p[1]))
        assert probes == [expected(p) for p in (vec(0,0),vec(1,0),vec(0,1))]
        assert len(path) % 2 == 1
        proofs.append(dict(source=source,target=target,domain=domain,path=path,
                           map='identity' if source in (0,1) else '(1-a,b)',
                           odd_length=True))
    assert area2(lower)+area2(upper) == area2(square)
    assert area2(clip2(lower,upper)) == 0

    # Compare the derived maps with every actual periodic contact, using raw poses.
    original = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    def pose(raw):
        return tuple(tuple(F(v) for v in row) for row in raw[0]),tuple(F(v) for v in raw[1]),F(raw[2])
    cell = [pose(p) for p in original['periodic_control']['cell']]
    controls = []
    for c in original['periodic_control']['contacts']:
        p = cell[c['tile']]
        q = cell[c['neighbor']]
        q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
        cc = dict(i=0,j=1,fi=c['fi'],fj=c['fj'])
        mapping = affine(contact_map([p,q],cc))
        relevant = [r for r in proofs if (r['source'],r['target']) == (c['fi'],c['fj'])]
        assert relevant
        for r in relevant:
            expected = (lambda x:x) if r['map'] == 'identity' else (lambda x:(1-x[0],x[1]))
            assert all(act(mapping,v) == expected(v) for v in (vec(0,0),vec(1,0),vec(0,1)))
        controls.append(dict(tile=c['tile'],neighbor=c['neighbor'],offset=c['offset'],
                             fi=c['fi'],fj=c['fj'],map=mapping,
                             proof_indices=[proofs.index(r) for r in relevant]))
    output = dict(scope='One identical face marking; fixed proper child poses; pointwise equality or involutive complement',
                  result='Every first-level-compatible marking accepts the two-prism periodic control',
                  directed_sibling_maps=edges,proofs=proofs,periodic_contacts=controls,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',Path(__file__),
                                     ROOT/'artifacts'/'geometry_and_constant_rules.json')})
    (ROOT/'artifacts'/'periodic_obstruction.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print('PASS: six exact region/path certificates imply all ten periodic contacts; all paths odd.')


if __name__ == '__main__':
    main()

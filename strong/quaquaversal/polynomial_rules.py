"""Q002: exact linear constraints for one polynomial marking on each face.

Polynomial equality on an open contact extends to its supporting plane.
This test does not cover discontinuous colors, piecewise polynomials,
vector/tensor transformation laws, or arbitrary geometric recuts.
"""

import hashlib
import json
from pathlib import Path
import sympy as sp

from geometry import (F,child_maps,contacts,compose,inverse_rotation,inverse_point,
                      mm,mul,mv,sub,vec,encode)

ROOT = Path(__file__).resolve().parent
A,B = sp.symbols('a b')
COORDS = ((0,1),(0,1),(0,2),(1,2),(0,2))


def embed(face,a,b):
    return ((a,b,0),(a,b,1),(a,0,b),(0,a,b),(a,1-a,b))[face]


def sym(x):
    return sp.Rational(x.numerator,x.denominator) if isinstance(x,F) else x


def contact_map(poses,c):
    pi,pj = poses[c['i']],poses[c['j']]
    r = mm(inverse_rotation(pj[0]),pi[0])
    t = mul(1/pj[2],mv(inverse_rotation(pj[0]),sub(pi[1],pj[1])))
    p = embed(c['fi'],A,B)
    q = [sym(pi[2]/pj[2])*sum(sym(r[i][j])*p[j] for j in range(3))+sym(t[i]) for i in range(3)]
    return tuple(sp.expand(q[j]) for j in COORDS[c['fj']])


def system(poses,cs,degree,sign):
    monomials = [(i,n-i) for n in range(degree+1) for i in range(n+1)]
    index = {p:i for i,p in enumerate(monomials)}
    width = len(monomials)
    rows = []
    maps = {}
    for c in cs:
        q = contact_map(poses,c)
        maps[(c['fi'],c['fj'],q)] = None
    for fi,fj,q in maps:
        block = [[sp.S.Zero]*(5*width) for _ in monomials]
        for k,(i,j) in enumerate(monomials):
            block[k][fi*width+k] += 1
            for power,coef in sp.Poly(sp.expand(q[0]**i*q[1]**j),A,B).terms():
                block[index[power]][fj*width+k] += sign*coef
        rows.extend(row for row in block if any(row))
    return sp.Matrix(rows),monomials,len(maps)


def main():
    poses = [p for _,p in child_maps()]
    cs = contacts(poses)
    results = []
    for degree in range(7):
        for sign in (-1,1):
            m,monomials,nmaps = system(poses,cs,degree,sign)
            basis = m.nullspace()
            polynomials = []
            for v in basis:
                polynomials.append([str(sp.expand(sum(v[f*len(monomials)+k]*A**i*B**j
                                                       for k,(i,j) in enumerate(monomials))))
                                    for f in range(5)])
            entry = dict(degree=degree,condition='equal' if sign == -1 else 'opposite',
                         variables=m.cols,equations=m.rows,distinct_maps=nmaps,
                         kernel_dimension=len(basis),basis=polynomials)
            results.append(entry)
            print(json.dumps(entry),flush=True)
    out = dict(scope="Exact total-degree <=6 scalar face-polynomial families; first-level sibling compatibility",
               results=results,
               sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (ROOT/'geometry.py',Path(__file__))})
    (ROOT/'artifacts'/'polynomial_rules.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__ == '__main__':
    main()

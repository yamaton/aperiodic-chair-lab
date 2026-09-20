"""Q018: simultaneous possible-neighbor incidence choices in finite patches.

Each forced center chooses one allowed star. Centers predicting the same
neighbor pose must agree whether it exists, even if the centers do not touch.
This is a necessary relaxation: optional tiles need no complete stars yet,
and geometric conflicts between optional tiles are not encoded. SAT is not
an extension certificate. Timeouts are unknown. Unsat inputs/proofs are kept.
"""

import argparse
import hashlib
import json
from collections import defaultdict
from math import lcm
from pathlib import Path

import z3

from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=ROOT/'artifacts'/'expanded_arcs_2_seed.json')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'neighbor_incidence_sat.json')
    parser.add_argument('--case-count',type=int,default=6)
    parser.add_argument('--timeout-ms',type=int,default=10000)
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/'closed_contact_atlas.json',ROOT/'artifacts'/'closed_star_language.json',args.input]
    atlas_raw,language,source = [json.loads(p.read_text()) for p in paths]
    chosen_rows = [(i,r) for i,r in enumerate(source['results']) if 'domains' in r][:args.case_count]
    used = sorted({tile for i,row in chosen_rows for tile,di in row['domains']})
    poses = {i:raw_pose(source['poses'][i]) for i in used}
    atlas = [raw_pose(p['pose']) for p in atlas_raw['poses']]
    scale = next(iter(poses.values()))[2]
    assert all(p[2] == scale for p in poses.values())
    rotations = list(dict.fromkeys(p[0] for p in poses.values()))
    ri = {r:i for i,r in enumerate(rotations)}
    ts = {i:tuple(x/scale for x in p[1]) for i,p in poses.items()}
    d = lcm(*(v.denominator for r in rotations+[p[0] for p in atlas] for row in r for v in row),
            *(v.denominator for t in list(ts.values())+[p[1] for p in atlas] for v in t))
    def integer(v):
        assert (v*d).denominator == 1
        return int(v*d)
    rs = [tuple(tuple(integer(v) for v in row) for row in r) for r in rotations]
    ts = {i:tuple(integer(v) for v in t) for i,t in ts.items()}
    ars = [tuple(tuple(integer(v) for v in row) for row in p[0]) for p in atlas]
    ats = [tuple(integer(v) for v in p[1]) for p in atlas]
    product_cache = {}
    position_cache = {}
    position_ids = {}
    positions = []
    def identifier(key):
        if key not in position_ids:
            position_ids[key] = len(positions)
            positions.append(key)
        return position_ids[key]
    centers = {i:identifier(tuple(v*d for row in rs[ri[p[0]]] for v in row)+tuple(v*d for v in ts[i]))
               for i,p in poses.items()}
    def neighbor(tile,q):
        key = tile,q
        if key not in position_cache:
            rid = ri[poses[tile][0]]
            rotation_key = rid,atlas[q][0]
            if rotation_key not in product_cache:
                a,b = rs[rid],ars[q]
                product_cache[rotation_key] = tuple(sum(a[i][k]*b[k][j] for k in range(3)) for i in range(3) for j in range(3))
            translation = tuple(ts[tile][i]*d+sum(rs[rid][i][j]*ats[q][j] for j in range(3)) for i in range(3))
            position_cache[key] = identifier(product_cache[rotation_key]+translation)
        return position_cache[key]
    results = []
    proof_dir = ROOT/'artifacts'/'incidence_proofs'
    for ci,(si,row) in enumerate(chosen_rows):
        ctx = z3.Context(proof=True)
        solver = z3.Solver(ctx=ctx)
        solver.set(timeout=args.timeout_ms)
        selectors = {}
        definitions = defaultdict(list)
        for tile,di in row['domains']:
            ss = source['domain_pool'][di]
            choices = [z3.BoolVal(True,ctx=ctx)] if len(ss) == 1 else [z3.Bool(f't{tile}_s{s}',ctx=ctx) for s in ss]
            selectors[tile] = ss,choices
            if len(ss) > 1:
                solver.add(z3.PbEq([(v,1) for v in choices],1))
            local = defaultdict(list)
            for k,s in enumerate(ss):
                for q in language['stars'][s]['neighbors']:
                    local[neighbor(tile,q)].append(k)
            for pos,ks in local.items():
                definitions[pos].append((tile,tuple(ks)))
        present = {centers[tile] for tile,di in row['domains']}
        constraints = 0
        for pos,defs in definitions.items():
            expressions = [z3.Or([selectors[tile][1][k] for k in ks]) for tile,ks in defs]
            anchor = z3.BoolVal(True,ctx=ctx) if pos in present else expressions[0]
            for expression in (expressions if pos in present else expressions[1:]):
                solver.add(expression == anchor)
                constraints += 1
        status = solver.check()
        result = dict(source_index=si,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                      status=str(status),forced_centers=len(selectors),possible_positions=len(definitions),
                      incidence_equalities=constraints,ambiguous_centers=sum(len(ss)>1 for ss,vs in selectors.values()))
        if status == z3.sat:
            model = solver.model()
            selected = {}
            for tile,(ss,vs) in selectors.items():
                indices = [k for k,v in enumerate(vs) if z3.is_true(model.eval(v,model_completion=True))]
                assert len(indices) == 1
                selected[tile] = indices[0]
            for pos,defs in definitions.items():
                values = [selected[tile] in ks for tile,ks in defs]
                assert len(set(values)) == 1 and (pos not in present or values[0])
            result['selected_stars'] = [(tile,selectors[tile][0][k]) for tile,k in sorted(selected.items())]
        elif status == z3.unsat:
            proof_dir.mkdir(exist_ok=True)
            stem = args.output.stem+f'_{ci}'
            smt_path = proof_dir/(stem+'.smt2')
            smt_path.write_text(solver.to_smt2())
            result['smt2'] = str(smt_path.relative_to(ROOT))
            try:
                proof_path = proof_dir/(stem+'.proof')
                proof_path.write_text(solver.proof().sexpr()+'\n')
                result['proof'] = str(proof_path.relative_to(ROOT))
            except z3.Z3Exception as exc:
                result['proof_unavailable'] = str(exc)
        else:
            result['reason_unknown'] = solver.reason_unknown()
        results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k != 'selected_stars'}),flush=True)
    output = dict(scope='Finite necessary incidence constraints; satisfiable assignments are not geometric tilings',
                  arguments={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
                  z3_version=z3.get_version_string(),pose_key_denominator=d*d,tile_scale=str(scale),
                  normalized_pose_keys=positions,results=results,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')


if __name__ == '__main__':
    main()

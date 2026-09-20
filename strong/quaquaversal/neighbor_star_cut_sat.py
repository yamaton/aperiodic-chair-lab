"""Q021: bounded lazy complete-neighbor-star cuts in the finite SAT pilot.

Each forced center chooses one allowed star. Centers predicting the same
neighbor pose must agree whether it exists, even if the centers do not touch.
Each model is checked for a possible complete star at every required neighbor.
Empty domains yield logged necessary choice cuts. Passing this check is still
not infinite extension. Round limits and timeouts are unknown. Solver UNSAT
results keep formulas/proofs and remain pending independent proof audit.
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
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'neighbor_star_cut_sat.json')
    parser.add_argument('--cuts',type=Path,default=ROOT/'artifacts'/'incidence_star_cuts.json')
    parser.add_argument('--rounds',type=int,default=16)
    parser.add_argument('--baseline',type=Path,default=ROOT/'artifacts'/'neighbor_incidence_sat.json')
    parser.add_argument('--forbidden',type=Path,default=ROOT/'artifacts'/'incidence_sample_exclusions.json')
    parser.add_argument('--case-count',type=int,default=6)
    parser.add_argument('--timeout-ms',type=int,default=10000)
    args = parser.parse_args()
    paths = [ROOT/'artifacts'/'closed_contact_atlas.json',ROOT/'artifacts'/'closed_star_language.json',args.input]
    atlas_raw,language,source = [json.loads(p.read_text()) for p in paths]
    baseline = json.loads(args.baseline.read_text())
    exclusions = json.loads(args.forbidden.read_text())
    initial_cuts = json.loads(args.cuts.read_text())
    compat_path = ROOT/'artifacts'/'closed_star_compatibility.json'
    compat = json.loads(compat_path.read_text())
    paths.extend((args.baseline,args.forbidden,args.cuts,compat_path))
    assert initial_cuts['sources'][args.input.name] == hashlib.sha256(args.input.read_bytes()).hexdigest()
    assert args.rounds > 0
    case_maps = [dict(row) for row in compat['cases']]
    domain_bits = [sum(1<<s for s in dom['stars']) for dom in compat['domains']]
    all_stars = (1<<len(language['stars']))-1
    cuts = [dict(antecedents=c['antecedents'],origin=dict(kind='audited_initial',index=i)) for i,c in enumerate(initial_cuts['cuts'])]
    cut_keys = {tuple(tuple(a) for a in c['antecedents']) for c in cuts}
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
        occupancy = {pos:z3.BoolVal(True,ctx=ctx) for pos in present}
        for pos,defs in definitions.items():
            expressions = [z3.Or([selectors[tile][1][k] for k in ks]) for tile,ks in defs]
            anchor = z3.BoolVal(True,ctx=ctx) if pos in present else expressions[0]
            occupancy[pos] = anchor
            for expression in (expressions if pos in present else expressions[1:]):
                solver.add(expression == anchor)
                constraints += 1
        assert d*d == baseline['pose_key_denominator'] == exclusions['normalized_pose_denominator']
        assert positions == [tuple(p) for p in baseline['normalized_pose_keys'][:len(positions)]]
        overlap_constraints = 0
        forced_collisions = []
        for ei,exclusion in enumerate(exclusions['exclusions']):
            a,b = exclusion['positions']
            if a in occupancy and b in occupancy:
                solver.add(z3.Or(z3.Not(occupancy[a]),z3.Not(occupancy[b])))
                overlap_constraints += 1
                if a in present and b in present:
                    forced_collisions.append(ei)
        installed = set()
        def install_cuts():
            for ki,cut in enumerate(cuts):
                if ki in installed:
                    continue
                antecedents = cut['antecedents']
                if all(tile in selectors and star in selectors[tile][0] for tile,star in antecedents):
                    solver.add(z3.Not(z3.And([selectors[tile][1][selectors[tile][0].index(star)] for tile,star in antecedents])))
                    installed.add(ki)
        install_cuts()
        rounds = []
        status = None
        passed = False
        selected_stars = None
        center_tiles = {centers[tile]:tile for tile in selectors}
        for step in range(args.rounds):
            installed_keys = {tuple(tuple(a) for a in cuts[i]['antecedents']) for i in installed}
            status = solver.check()
            if status != z3.sat:
                rounds.append(dict(round=step+1,solver_status=str(status),new_cuts=0,installed_cuts=len(installed)))
                break
            model = solver.model()
            chosen = {}
            for tile,(ss,vs) in selectors.items():
                options = [k for k,v in enumerate(vs) if z3.is_true(model.eval(v,model_completion=True))]
                assert len(options) == 1
                chosen[tile] = options[0]
            selected_stars = {tile:selectors[tile][0][k] for tile,k in chosen.items()}
            for pos,defs in definitions.items():
                values = [chosen[tile] in ks for tile,ks in defs]
                assert len(set(values)) == 1 and (pos not in present or values[0])
            active = present|{pos for pos,defs in definitions.items() if chosen[defs[0][0]] in defs[0][1]}
            assert all(not set(e['positions']) <= active for e in exclusions['exclusions'])
            requirements = defaultdict(list)
            for pos,tile in center_tiles.items():
                star = selected_stars[tile]
                requirements[pos].append(dict(tile=tile,star=star,kind='selected_center'))
            for tile,star in selected_stars.items():
                for q in language['stars'][star]['neighbors']:
                    requirements[neighbor(tile,q)].append(dict(tile=tile,star=star,kind='neighbor',pair=q,
                                                              domain=case_maps[star][q]))
            def intersection(rs):
                value = all_stars
                for reason in rs:
                    value &= (1<<reason['star']) if reason['kind'] == 'selected_center' else domain_bits[reason['domain']]
                return value
            failures = []
            for pos,reasons in requirements.items():
                if intersection(reasons):
                    continue
                minimal = list(reasons)
                cursor = 0
                while cursor < len(minimal) and len(minimal) > 1:
                    smaller = minimal[:cursor]+minimal[cursor+1:]
                    if not intersection(smaller):
                        minimal = smaller
                    else:
                        cursor += 1
                antecedents = tuple(sorted({(r['tile'],r['star']) for r in minimal}))
                assert antecedents not in installed_keys,'Installed necessary cut violated by solver model'
                if antecedents in cut_keys:
                    # The same conjunction may empty several neighbors in
                    # this one model, before newly discovered cuts are installed.
                    continue
                cut_keys.add(antecedents)
                failures.append(len(cuts))
                cuts.append(dict(antecedents=antecedents,origin=dict(kind='empty_neighbor_domain',case=ci,round=step+1,
                                                                    position=pos,requirements=minimal)))
            rounds.append(dict(round=step+1,solver_status='sat',new_cuts=len(failures),cut_indices=failures,
                               installed_cuts=len(installed),neighbor_positions=len(requirements)))
            print(json.dumps(dict(case=ci,round=step+1,new_cuts=len(failures),total_cuts=len(cuts))),flush=True)
            if not failures:
                passed = True
                break
            install_cuts()
        result = dict(source_index=si,boundary_index=row['boundary_index'],cover_index=row['cover_index'],
                      status=('sat_passes_neighbor_star_test' if passed else 'unknown_at_cut_round_limit') if status == z3.sat else
                             ('unsat_pending_independent_audit' if status == z3.unsat else 'unknown_solver'),
                      rounds=rounds,installed_cut_indices=sorted(installed),
                      forced_centers=len(selectors),possible_positions=len(definitions),
                      incidence_equalities=constraints,ambiguous_centers=sum(len(ss)>1 for ss,vs in selectors.values()),
                      sampled_overlap_clauses=overlap_constraints,forced_collision_witnesses=forced_collisions)
        if status == z3.sat:
            result['selected_stars'] = sorted(selected_stars.items())
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
    output = dict(scope='Bounded lazy complete-neighbor-star cuts; UNSAT solver results await independent proof audit',
                  arguments={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
                  z3_version=z3.get_version_string(),pose_key_denominator=d*d,tile_scale=str(scale),
                  normalized_pose_keys=positions,cuts=cuts,results=results,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (ROOT/'geometry.py',ROOT/'reflected_controls.py',*paths,Path(__file__))})
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')


if __name__ == '__main__':
    main()

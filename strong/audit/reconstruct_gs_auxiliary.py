"""Witnesses and finite checks for the Goodman-Strauss reconstruction question.

Reads frozen coordinates and motif descriptors; no project implementation imports.
The all-radius obstruction and the infinite symmetry construction are written
arguments in ../review/AUXILIARY_RECONSTRUCTION.md, not finite-test conclusions.
Run: uv run --locked python strong/audit/reconstruct_gs_auxiliary.py
"""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = '95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54'
ONE = (1, 1, 1)
ZERO = (0, 0, 0)
ID = (1, 0, 0, 0, 1, 0, 0, 0, 1)
CYCLE = (0, 0, 1, 1, 0, 0, 0, 1, 0)
SIGNS = tuple(product((-1, 1), repeat=3))
OCTANTS = tuple(product((-1, 0), repeat=3))


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def scale(k, a): return tuple(k*x for x in a)
def mv(r, v): return tuple(sum(r[3*i+j]*v[j] for j in range(3)) for i in range(3))
def mm(r, s): return tuple(sum(r[3*i+k]*s[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def lower(r, q): return tuple((v-1)//2 for v in mv(r, tuple(2*x+1 for x in q)))
def arrow(s, n):
    d = sum(a*b for a, b in zip(s, n))
    return tuple(d*(a-d*b) for a, b in zip(s, n))


def expand(patch, children):
    out = {}
    for c, r in patch.items():
        for t, s in children:
            v = add(scale(2, c), mv(r, t))
            assert v not in out
            out[v] = mm(r, s)
    return out


def expand_old(coarse):
    # Directly transcribe the signed-diagonal substitution, without the
    # candidate's choice of proper orientations for its outer children.
    out = {}
    for c, s in coarse.items():
        out[scale(2, c)] = s
        for t in SIGNS:
            if t == ONE:
                continue
            v = add(scale(2, c), tuple(a*b for a, b in zip(s, t)))
            assert v not in out
            out[v] = tuple(-a*b for a, b in zip(s, t))
    return out


def geometry(patch, base):
    cells = {}
    for c, r in patch.items():
        for q in base:
            v = add(c, lower(r, q))
            assert v not in cells
            cells[v] = c
    outside = {add(c, mv(r, s)) for c, r in patch.items() for s in SIGNS if s != ONE}
    holes = outside - patch.keys()
    complete = {v for v in holes if all(add(v, q) in cells for q in OCTANTS)}
    # Every interior slot really has eight outside-corner octants, not a
    # chair face cutting across the proposed cross.
    for v in complete:
        for q in OCTANTS:
            assert sub(v, cells[add(v, q)]) in SIGNS
    return cells, holes, complete


def trace(patch, holes, v, axis, sign):
    step = tuple(2*sign*int(i == axis) for i in range(3))
    w, path = add(v, step), []
    while w in holes:
        path.append(w)
        w = add(w, step)
    if w not in patch:
        return None
    n = tuple(-sign*int(i == axis) for i in range(3))
    return {'endpoint': w, 'notch': mv(patch[w], ONE),
            'arrow': arrow(mv(patch[w], ONE), n), 'intermediate_crosses': path}


def all_forced(patch, holes, complete):
    forced, records, free = {}, {}, Counter()
    for v in sorted(complete):
        marks = []
        for axis in range(3):
            ends = [e for sign in (-1, 1) if (e := trace(patch, holes, v, axis, sign))]
            if ends:
                assert len({e['arrow'] for e in ends}) == 1
                marks.append((axis, ends[0]['arrow']))
                records[v, axis] = ends
        assert len(marks) <= 1
        free[len(marks)] += 1
        if marks:
            forced[v] = marks[0]
    return forced, records, dict(free)


def check_face_rules(patch, motifs):
    exposed = {}
    count = 0
    for c, r in patch.items():
        for f in motifs['face_descriptors']:
            pos = add(scale(2, c), mv(r, f['center_times_2']))
            n, u = mv(r, f['normal']), mv(r, f['arrow'])
            opposite = pos, scale(-1, n)
            if opposite in exposed:
                other, v = exposed[opposite]
                name = f['motif']
                assert ((name == other == 'A' and v == cross(n, u)) or
                        ((name, other) in (('B', 'C'), ('C', 'B')) and v == scale(-1, u)))
                count += 1
            exposed[pos, n] = f['motif'], u
    return count


def voxel_check(patch, witnesses):
    # X is exactly the union of three axis bars. A 1/4-grid is exact for
    # X and the old recut chair (not an approximation of our curved tile).
    xv = {q for q in product(range(-4, 4), repeat=3) if sum(-1 <= a < 1 for a in q) >= 2}
    lv = {q for q in product(range(-4, 4), repeat=3) if any(a < 0 for a in q)}
    recut = (lv | xv) - {add(scale(4, s), q) for s in SIGNS for q in xv}
    assert (len(xv), len(recut)) == (80, 388)
    occupied = set()
    for c, r in patch.items():
        placed = {add(scale(4, c), lower(r, q)) for q in recut}
        assert not occupied & placed
        occupied.update(placed)
    for v in witnesses:
        slot = {add(scale(4, v), q) for q in xv}
        box = {add(scale(4, v), q) for q in product(range(-4, 4), repeat=3)}
        assert box - occupied == slot
    return {'quarter_voxels_in_X': len(xv), 'quarter_voxels_in_recut_L': len(recut),
            'nonoverlapping_recut_chairs': len(patch), 'exact_cavities_checked': sorted(witnesses)}


def main():
    raw = (HERE / 'frozen_v1/candidate.json').read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED
    data = json.loads(raw)
    motif_raw = (HERE / 'face_motifs.json').read_bytes()
    motifs = json.loads(motif_raw)
    assert motifs['candidate_sha256'] == EXPECTED
    children = [(tuple(c['center']), tuple(v for row in c['matrix'] for v in row)) for c in data['children']]
    base = tuple(map(tuple, data['coarse_cubes']))
    patch, coarse = {ZERO: ID}, {ZERO: ONE}
    for _ in range(3):
        patch, coarse = expand(patch, children), expand_old(coarse)
        assert {c: mv(r, ONE) for c, r in patch.items()} == coarse
    legal_faces = check_face_rules(patch, motifs)
    cells, holes, complete = geometry(patch, base)
    forced, records, free = all_forced(patch, holes, complete)
    a, b = (-4, 0, -4), (-4, 0, 4)
    local = []
    for v in (a, b):
        owners = {cells[add(v, q)] for q in OCTANTS}
        local.append({sub(c, v): patch[c] for c in owners})
    assert local[0] == local[1] and len(local[0]) == 8
    assert forced[a] == (1, (1, 0, 1)) and forced[b] == (1, (1, 0, -1))
    for v in (a, b):
        assert len(records[v, 1]) == 2
        assert all(w in complete for end in records[v, 1] for w in end['intermediate_crosses'])
    forward = {'crosses': [a, b], 'forced_axis': 'y',
               'forced_arrows': [forced[a][1], forced[b][1]],
               'endpoint_certificates': [records[a, 1], records[b, 1]],
               'identical_relative_chairs': [{'origin': t, 'rotation': r} for t, r in sorted(local[0].items())]}

    # The connected-X2 question is kept distinct from the main L/I model.
    target = (-4, -2, 0)
    blockers = [(0, (-2, -2, 0), 2), (1, (-4, -4, 0), 2), (2, (-4, -2, -2), 0)]
    assert target in complete and target not in forced
    x2 = []
    for axis, w, forced_axis in blockers:
        assert w in complete and forced[w][0] == forced_axis != axis
        delta = sub(w, target)
        assert abs(delta[axis]) == 2 and sum(abs(x) for x in delta) == 2
        ends = records[w, forced_axis]
        assert any(all(q in complete for q in e['intermediate_crosses']) for e in ends)
        x2.append({'rejected_axis': axis, 'neighbor_cross': w, 'neighbor_forced_axis': forced_axis,
                   'forcing_chair_chains': ends})
    voxels = voxel_check(patch, {a, b, target} | {w for _, w, _ in blockers})

    # Finite checks behind the reverse-direction symmetry argument.
    assert {mv(CYCLE, c): mv(CYCLE, s) for c, s in coarse.items()} == coarse
    rotated = {mv(CYCLE, c): mm(CYCLE, r) for c, r in patch.items()}
    changed = sorted(c for c in patch if rotated[c] != patch[c])
    assert changed == sorted(scale(-j, ONE) for j in range(8))
    old_marks = {}
    for v in complete:
        for axis in range(3):
            ends = [e for sign in (-1, 1) if (e := trace(patch, holes, v, axis, sign))]
            old_marks[v, axis] = ends[0]['arrow'] if ends else tuple(int(i != axis) for i in range(3))
    for (v, axis), mark in old_marks.items():
        direction = mv(CYCLE, tuple(int(i == axis) for i in range(3)))
        new_axis = direction.index(1)
        assert old_marks[mv(CYCLE, v), new_axis] == mv(CYCLE, mark)
    face_set = {(tuple(f['center_times_2']), tuple(f['normal']), f['motif'], tuple(f['arrow']))
                for f in motifs['face_descriptors']}
    assert {(mv(CYCLE, p), mv(CYCLE, n), name, mv(CYCLE, u)) for p, n, name, u in face_set} != face_set
    nested, seed, nesting_checks = {ZERO: ID}, {ZERO: ID}, []
    for n in range(1, 3):
        seed = expand(expand(seed, children), children)
        shift = scale((4**n-1)//3, ONE)
        enlarged = {add(c, shift): r for c, r in seed.items()}
        assert all(enlarged.get(c) == r for c, r in nested.items())
        assert enlarged[ZERO] == ID
        nesting_checks.append({'n': n, 'shift': shift, 'included_chairs': len(nested),
                               'larger_chairs': len(enlarged)})
        nested = enlarged

    scaled_checks = []
    common = local[0]
    for m in range(3):
        if m:
            patch, coarse = expand(patch, children), expand_old(coarse)
            common = expand(common, children)
            assert {c: mv(r, ONE) for c, r in patch.items()} == coarse
            cells, holes, complete = geometry(patch, base)
        factor = 2**m
        common_cells = {add(t, lower(r, q)) for t, r in common.items() for q in base}
        assert set(product(range(-factor, factor), repeat=3)) <= common_cells
        endpoints = []
        for v0 in (a, b):
            v = scale(factor, v0)
            assert v in complete
            for t, r in common.items():
                assert patch[add(v, t)] == r
            ends = [trace(patch, holes, v, 1, sign) for sign in (-1, 1)]
            assert all(ends)
            assert {e['arrow'] for e in ends} == {forced[v0][1]}
            assert all(w in complete for e in ends for w in e['intermediate_crosses'])
            assert {e['endpoint'] for e in ends} == {scale(factor, e['endpoint']) for e in records[v0, 1]}
            endpoints.append(ends)
        scaled_checks.append({'substitution_depth': 3+m, 'chairs': len(patch),
                              'common_chairs': len(common), 'covered_cube_half_side': factor,
                              'crosses': [scale(factor, a), scale(factor, b)], 'chains': endpoints})
    report = {'status': 'passed', 'candidate_sha256': EXPECTED,
              'face_motifs_sha256': sha256(motif_raw).hexdigest(),
              'scope': 'Finite witnesses; all-radius and infinite symmetry arguments are in the report.',
              'depth_three_matching_unit_face_pairs': legal_faces,
              'depth_three_complete_crosses_by_number_of_endpoint_forced_axes': free,
              'forward_obstruction': forward, 'inflation_checks': scaled_checks,
              'old_recut_geometry_check': voxels,
              'connected_X2_model_discrepancy': {'target': target, 'blockers': x2,
                  'scope': 'No X2 orientation fits this cavity in the transcribed fixed-chair model; source interpretation needs review.'},
              'reverse_symmetry_checks': {'cyclic_rotation': CYCLE, 'coarse_patch_invariant': True,
                  'original_I_marked_patch_invariant': True, 'our_root_motif_not_invariant': True,
                  'changed_decorated_chair_origins': changed,
                  'finite_nested_patch_checks': nesting_checks,
                  'infinite_nested_patch_shifts': [(4**n-1)//3 for n in range(6)]}}
    (HERE / 'auxiliary_reconstruction.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'matching_face_pairs': legal_faces,
                      'forward_crosses': [a, b], 'arrows': forward['forced_arrows'],
                      'inflation_cube_half_sides': [x['covered_cube_half_side'] for x in scaled_checks],
                      'connected_X2_model': 'three axes excluded at '+str(target),
                      'reverse_symmetry': 'finite checks passed; infinite argument is written separately'}, indent=2))


if __name__ == '__main__':
    main()

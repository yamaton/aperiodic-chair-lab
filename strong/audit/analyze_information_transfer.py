"""Symbolic classification of recodings of the twelve frozen port families.

Uses the frozen-coordinate audit geometry; equations are reconstructed from
complete faces, not the interactive export. No search or frozen input changes.
"""
from collections import Counter
from itertools import product
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import verify_from_coordinates as a

HERE = Path(__file__).resolve().parent
N = 12
IDENTITY = tuple(range(N))
PAIRS = tuple((i, j) for i in range(N) for j in range(i+1, N))


def partition(pairs):
    parent = list(range(N))
    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for i, j in pairs:
        parent[find(j)] = find(i)
    names, result = {}, []
    for i in range(N):
        root = find(i)
        if root not in names:
            names[root] = len(names)
        result.append(names[root])
    return tuple(result)


def equalities(p):
    return tuple((i, j) for i, j in PAIRS if p[i] == p[j])


def mask(p):
    return sum(1 << k for k, (i, j) in enumerate(PAIRS) if p[i] == p[j])


def blocks(p):
    return [b for v in sorted(set(p)) if len(b := [i+1 for i, x in enumerate(p) if x == v]) > 1]


def minimal(rows):
    ps = set(rows)-{IDENTITY}
    masks = {p: mask(p) for p in ps}
    return sorted(p for p in ps if not any(q != p and masks[q] & masks[p] == masks[q] for q in ps))


def catalogue(solid, rotations, chirality):
    records = {}
    for r in rotations:
        other = a.rotate_solid(solid, r)
        ranges = [range(min(q[k] for q in solid.cubes)-max(q[k]+1 for q in other.cubes),
                        max(q[k]+1 for q in solid.cubes)-min(q[k] for q in other.cubes)+1)
                  for k in range(3)]
        for t in product(*ranges):
            if any(a.add(q, t) in solid.cubes for q in other.cubes):
                continue
            pairs = []
            for (f, n), ports in other.faces.items():
                opposite = (a.add(f, a.scale(2, t)), a.scale(-1, n))
                if opposite not in solid.faces:
                    continue
                target = solid.faces[opposite]
                for p, (k, u, v) in ports.items():
                    j, uu, vv = target[a.add(p, a.scale(16, t))]
                    assert (u, v) == (uu, vv)
                    assert chirality[k] == -chirality[j]
                    pairs.append((abs(k)-1, abs(j)-1))
            if pairs:
                records[t, r] = partition(pairs)
    return records


def main():
    raw = (HERE/'frozen_v1/candidate.json').read_bytes()
    data = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((HERE/'frozen_v1/manifest.json').read_text())['candidate_sha256']
    chirality = {}
    for p in data['ports']:
        key = p['signed_key']
        c = a.determinant(tuple(p['u_axis'])+tuple(p['v_axis'])+tuple(p['outward_normal']))
        if key in chirality:
            assert chirality[key] == c
        chirality[key] = c
    assert all(chirality[-k] == -chirality[k] for k in range(1, N+1))
    solid = a.from_data(data)
    rotations = a.rotation_group()
    oriented = {r: a.rotate_solid(solid, r) for r in rotations}
    children = [(tuple(c['center']), tuple(x for row in c['matrix'] for x in row)) for c in data['children']]
    macro = a.assemble(children, solid, oriented)
    fine = catalogue(solid, rotations, chirality)
    full = catalogue(macro, rotations, chirality)
    assert len(fine) == 1194 and len(full) == 6801
    aligned = {(tuple(x//2 for x in t), r): p for (t, r), p in full.items() if all(x % 2 == 0 for x in t)}
    assert set(aligned) == set(fine)
    assert {q for q, p in fine.items() if p == IDENTITY} == {q for q, p in aligned.items() if p == IDENTITY}
    assert sum(p == IDENTITY for p in fine.values()) == 44
    assert sum(p == IDENTITY for p in full.values()) == 44

    # Independent child-to-child construction of the scale operator, compared
    # with directly assembled macro boundary predicates, then iterated again.
    dependencies = {}
    for t, r in fine:
        moved = [a.move_placement(c, a.scale(2, t), r) for c in children]
        dependencies[t, r] = sorted({q for x in children for y in moved if (q := a.relative(x, y)) in fine})
    def induce(rows):
        return {q: partition(e for child in ds for e in equalities(rows[child])) for q, ds in dependencies.items()}
    assert induce(fine) == aligned
    assert induce(aligned) == aligned

    P = partition([(0,2), (1,4), (3,6), (5,7)])
    Q = partition([(0,2), (2,8), (1,4), (4,9), (3,6), (6,10), (5,7), (7,11)])
    assert Counter(aligned.values()) == {IDENTITY:44, P:67, Q:1083}
    low = minimal(fine.values())
    high = minimal(full.values())
    assert len(low) == 5 and low == high
    expected = [partition([(i-1,j-1) for i,j in pairs]) for pairs in [
        [(1,6),(2,4),(3,8),(5,7)], [(1,8),(2,7),(3,6),(4,5)],
        [(1,2),(3,4),(5,6),(7,8)], [(1,3),(2,5),(4,7),(6,8)], [(9,12),(10,11)]]]
    assert set(low) == set(expected)

    def permitted(rows, colors):
        cm = mask(tuple(colors))
        return {q for q, p in rows.items() if mask(p) & cm == mask(p)}
    good, counts = [], Counter()
    fine_patterns, macro_patterns = Counter(fine.values()), Counter(full.values())
    for code in range(1 << 11):
        colors = [1] + [1+((code >> i)&1) for i in range(11)]
        cm = mask(tuple(colors))
        fits = lambda p: mask(p) & cm == mask(p)
        fc = sum(n for p, n in fine_patterns.items() if fits(p))
        mc = sum(n for p, n in macro_patterns.items() if fits(p))
        ac = 44 + 67*fits(P) + 1083*fits(Q)
        counts[fc, ac, mc] += 1
        valid = not any(fits(p) for p in low)
        assert valid == (fc == 44) == (mc == 44)
        if valid:
            assert ac == 44
            good.append(code)
    assert len(good) == 1224
    colors = [1,2,1,1,1,1,1,1,2,1,1,1]
    keys = [chirality[p['signed_key']]*colors[abs(p['signed_key'])-1] for p in data['ports']]
    assert sum(keys) == 0 and set(keys) == {-2,-1,1,2}
    assert permitted(fine, colors) == {q for q, p in fine.items() if p == IDENTITY}
    assert permitted(full, colors) == {q for q, p in full.items() if p == IDENTITY}
    # The small constructive family: choose one high variable among 1..8
    # and one among 9..12. It breaks every one of the five forbidden patterns.
    for i, j in product(range(8), range(8,12)):
        test = [1]*12
        test[i] = test[j] = 2
        assert all(mask(p)&mask(tuple(test)) != mask(p) for p in low)

    patterns = sorted(set(fine.values()) | set(full.values()))
    pattern_id = {p:i for i,p in enumerate(patterns)}
    rotation_id = {r:i for i,r in enumerate(rotations)}
    compact = lambda rows: [[list(t),rotation_id[r],pattern_id[p]] for (t,r),p in sorted(rows.items())]
    report = dict(status='passed',candidate_sha256=digest,
        implementation='Symbolic predicates rebuilt from frozen faces using verify_from_coordinates; scale identity cross-checked by child contacts. Binary partitions exhaustively evaluated.',
        scope='All assignments constant in each of the twelve chirality-switched components; proper integer-grid fine contacts and all integer-offset parent contacts. Aligned higher-level induction only. No new arbitrary-Euclidean solid theorem.',
        counts=dict(fine=1194,full_macro=6801,odd_macro=5607,fine_predicates=len(set(fine.values())),aligned_macro_predicates=3,full_macro_predicates=len(set(full.values()))),
        positive_key_chirality=[chirality[k] for k in range(1,13)],
        predicates=[dict(partition=p,blocks=blocks(p),fine_contacts=fine_patterns[p],full_macro_contacts=macro_patterns[p]) for p in patterns],
        minimal_forbidden_patterns=[dict(blocks=blocks(p),predicate_id=pattern_id[p],
            fine_witness=next([list(t),rotation_id[r]] for (t,r),q in sorted(fine.items()) if q==p),
            macro_witness=next([list(t),rotation_id[r]] for (t,r),q in sorted(full.items()) if q==p)) for p in expected],
        aligned_recurrence=dict(P=blocks(P),Q=blocks(Q),counts={'unconditional':44,'P':67,'Q':1083},
            outcomes=[44,111,1194],second_symbolic_induction_identical=True),
        binary=dict(partitions_checked=2048,reference_preserving=1224,reference_preserving_codes=good,
            joint_counts=[dict(fine=f,aligned_macro=m,full_macro=b,count=n) for (f,m,b),n in sorted(counts.items())],
            simple_two_high_choices=32),
        two_depth_witness=dict(chirality_corrected_amplitudes=colors,signed_port_keys=keys,
            positive_old_key_to_new=[chirality[k]*colors[k-1] for k in range(1,13)],
            fine_contacts=44,full_macro_contacts=44,odd_macro_contacts=0,volume_key_sum=0,
            chirality_equals_new_key_sign=True),
        rotations=rotations,fine_contact_predicates=compact(fine),macro_contact_predicates=compact(full))
    path=HERE/'information_transfer.json'
    path.write_text(json.dumps(report,separators=(',',':'))+'\n')
    print(json.dumps({k:report[k] for k in ('status','counts','aligned_recurrence')}))
    print('Five minimal forbidden equality patterns agree for fine and full macro contacts.')
    print('Two gauge values: 1224 / 2048 partitions preserve both 44-contact sets; 32 simple witnesses.')
    print(f'Wrote {path.name} ({path.stat().st_size:,} bytes).')


if __name__=='__main__':
    main()

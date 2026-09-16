"""Independent finite paths used by the grid-audit subagent, made portable.

Brute-force all 48 frames, transform all eight cube corners, and derive
periodic box templates from ports. Does not import the primary checker.
Run: uv run --locked python strong/audit/grid_bridge_crosscheck.py
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = '95284fd672945936a383b046f67f5d4b11ab34d05909d0548f4ac95a565b3e54'


def vec(v): return tuple(map(F, v))
def add(a, b): return tuple(x+y for x, y in zip(a, b))
def neg(a): return tuple(-x for x in a)
def rot(p, s, v): return tuple(s[i]*v[p[i]] for i in range(3))
def determinant(p, s):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))
    return (-1)**inversions*s[0]*s[1]*s[2]


def main():
    raw = (HERE/'frozen_v1/candidate.json').read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED
    d = json.loads(raw)
    ports, cells = d['ports'], set(map(tuple, d['coarse_cubes']))
    frames = list(product(permutations(range(3)), product((-1, 1), repeat=3)))
    matches, determinants = [], Counter()
    owner_checks = 0
    for a, b in product(ports, repeat=2):
        if a['signed_key'] != -b['signed_key']: continue
        matches_here = 0
        for p, s in frames:
            if rot(p, s, b['u_axis']) != tuple(a['u_axis']): continue
            if rot(p, s, b['v_axis']) != tuple(a['v_axis']): continue
            if rot(p, s, b['outward_normal']) != neg(a['outward_normal']): continue
            t = add(vec(a['center']), neg(rot(p, s, vec(b['center']))))
            assert all(x.denominator == 1 for x in t)
            owners = []
            for port in (a, b):
                f = tuple(F(port['center'][i])-(3*port['u_axis'][i]+port['v_axis'][i])/F(16) for i in range(3))
                q = tuple(f[i]-F(1, 2)-F(port['outward_normal'][i], 2) for i in range(3))
                assert q in cells and add(q, port['outward_normal']) not in cells
                owners.append(q)
            vertices = [add(t, rot(p, s, add(owners[1], e))) for e in product((0, 1), repeat=3)]
            image_lower = tuple(min(v[i] for v in vertices) for i in range(3))
            assert image_lower == add(owners[0], a['outward_normal'])
            matches.append((p, s, t)); owner_checks += 1; matches_here += 1
            determinants[determinant(p, s)] += 1
        assert matches_here == 1
    assert len(matches) == owner_checks == 1536 and len(set(matches)) == 86
    assert determinants == {1: 1536}

    # Derive the periodic family from actual ports, not a prescribed orbit.
    w = F(d['half_width'])
    h = max(abs(p['signed_key']) for p in ports)*F(d['height_unit'])*(1+F(d['cap_polynomial']['a'])+F(d['cap_polynomial']['b']))
    boxes = set()
    for port, (p, s) in product(ports, frames):
        center = tuple(x % 1 for x in rot(p, s, vec(port['center'])))
        n = rot(p, s, port['outward_normal'])
        radius = tuple(h if n[i] else w for i in range(3))
        boxes.add((center, radius))
    assert len(boxes) == 24
    count, smallest = 0, None
    for (a, ar), (b, br), shift in product(boxes, boxes, product(range(-2, 3), repeat=3)):
        bb = add(b, shift)
        if a == bb and ar == br: continue
        gaps = [abs(a[i]-bb[i])-ar[i]-br[i] for i in range(3)]
        assert not all(g <= 0 for g in gaps)
        count += 1
        smallest = max(gaps) if smallest is None else min(smallest, max(gaps))
    assert count == 71976 and smallest == F(3, 32)

    # Independently find the altered equal-coefficient cap's swapped frame.
    a = ports[0]
    b = next(b for b in ports if b['signed_key'] == -a['signed_key'])
    swapped = [(p, s) for p, s in frames if rot(p, s, b['u_axis']) == tuple(a['v_axis'])
               and rot(p, s, b['v_axis']) == tuple(a['u_axis'])
               and rot(p, s, b['outward_normal']) == neg(a['outward_normal'])]
    assert len(swapped) == 1
    p, s = swapped[0]
    control_t = add(vec(a['center']), neg(rot(p, s, vec(b['center']))))
    assert determinant(p, s) == -1 and any(x.denominator != 1 for x in control_t)
    result = {'status': 'passed', 'candidate_sha256': EXPECTED,
              'scope': 'Alternate finite arithmetic; no analytic or all-tilings proof is performed.',
              'opposite_key_frame_matches': len(matches), 'relative_determinants': dict(determinants),
              'distinct_poses': len(set(matches)), 'cube_corner_owner_checks': owner_checks,
              'derived_periodic_box_types': len(boxes), 'periodic_checks_shifts_up_to_two': count,
              'minimum_separating_gap': str(smallest),
              'equal_coefficient_control': {'determinant': determinant(p, s),
                  'translation': list(map(str, control_t)), 'reflections_allowed': True}}
    (HERE/'grid_bridge_crosscheck.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

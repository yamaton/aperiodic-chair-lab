"""Check Chair44's Lean literals against its exact solid data, without executing it.

This independently written finite check parses the released Generated/CoreData
literals and reconstructs feature geometry from the inspected definitions in
FiniteModel and LogicalSpineFoundation. It does not elaborate Lean or establish
that the surrounding geometric proof compiles or is mathematically correct.
Run from our repository using uv run --locked python <this-script> --release-root
<extracted-pinned-release> --output <report.json>.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import re
from fractions import Fraction as F


def check(root):
    source_paths = [
        'lean/R44/R44/Generated/CoreData.lean',
        'lean/R44/R44/FiniteModel.lean',
        'lean/R44/R44/LogicalSpineFoundation.lean',
        'solid/native_panels.csv',
        'solid/r44_solid.json',
    ]
    hashes = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in source_paths}
    src = (root / source_paths[0]).read_text()
    solid = json.loads((root / 'solid/r44_solid.json').read_text())
    block = src.split('def panels : List Panel := [', 1)[1].split('\ndef ', 1)[0]
    pattern = r'\{ axis := (\d+), outward := (\(?-?\d+\)?), center2 := v ([^,]+), coefficients := \[([^\]]*)\] \}'
    panels = []
    for axis, sign, center, coefficients in re.findall(pattern, block, re.S):
        panels.append((int(axis), int(sign.strip('()')),
                       list(map(int, re.findall(r'-?\d+', center))),
                       list(map(int, re.findall(r'-?\d+', coefficients)))))
    with (root / 'solid/native_panels.csv').open() as stream:
        csv_rows = list(csv.DictReader(stream))
    assert len(panels) == len(csv_rows) == 24, 'panel count'
    for panel_id, (panel, row) in enumerate(zip(panels, csv_rows)):
        assert int(row['panel']) == panel_id
        expected = (int(row['normal_axis']), int(row['outward_sign']),
                    [2 * F(row['center_' + k]) for k in 'xyz'],
                    [int(row['a_' + str(i)]) for i in range(8)])
        assert panel == expected, ('CSV/Lean panel mismatch', panel_id)
    assert [a for p in panels for a in p[3]] == solid['profile'], 'profile mismatch'
    # Literal offset pattern in FiniteModel.lean:145; manually inspected formulas
    # at FiniteModel:155-174 and LogicalSpineFoundation:191-230.
    offsets = [(-1, -2), (-1, 2), (1, -2), (1, 2),
               (-2, -1), (-2, 1), (2, -1), (2, 1)]
    patches = {p['role']: p for p in solid['patches']}
    assert len(solid['patches']) == len(patches) == 192
    assert set(patches) == set(range(192))
    for panel_id, (axis, sign, center2, coefficients) in enumerate(panels):
        tangents = [j for j in range(3) if j != axis]
        for slot, (u, v) in enumerate(offsets):
            role = 8 * panel_id + slot
            patch = patches[role]
            center = [F(x, 2) for x in center2]
            center[tangents[0]] += F(u, 8)
            center[tangents[1]] += F(v, 8)
            apex = center.copy()
            apex[axis] += F(sign * coefficients[slot], 10000)
            base = []
            for s, t in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                corner = center.copy()
                corner[tangents[0]] += F(s, 100)
                corner[tangents[1]] += F(t, 100)
                base.append(tuple(corner))
            assert patch['face'] == panel_id, ('face', role)
            assert patch['coefficient'] == coefficients[slot], ('coefficient', role)
            assert list(map(F, patch['apex'])) == apex, ('apex', role)
            assert set(base) == {tuple(map(F, b)) for b in patch['base']}, ('base', role)
    for name, key, scale in [('solidVertices10000', 'vertices', 10000),
                             ('solidTriangles', 'triangles', 1)]:
        match = re.search(r'def ' + name + r'[^\n]* := decode\w+ "([^"\n]*)"', src)
        assert match, ('missing literal', name)
        values = [list(map(int, row.split(',')))
                  for row in match.group(1).split('\\n') if row]
        expected = [[F(value) * scale for value in row] for row in solid[key]]
        assert values == expected, ('array mismatch', name)
    assert F(solid['base_halfwidth']) == F(1, 100)
    assert F(solid['height_unit']) == F(1, 10000)
    return {
        'status': 'passed',
        'scope': 'Exact data correspondence only; no Lean compilation or proof validation.',
        'formula_scope': 'Feature formulas transcribed from manually inspected pinned Lean source; the source hashes bind that inspection.',
        'release_root': str(root.resolve()),
        'source_sha256': hashes,
        'probe_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'panels_equal': 24,
        'features_exact_Lean_formula_vs_JSON': 192,
        'vertices_equal': len(solid['vertices']),
        'triangles_equal': len(solid['triangles']),
        'base_halfwidth': '1/100',
        'height_unit': '1/10000',
    }


def main():
    if not __debug__:
        raise SystemExit('Run without -O: this audit requires assertions.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-root', required=True, type=pathlib.Path)
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    result = check(args.release_root)
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()

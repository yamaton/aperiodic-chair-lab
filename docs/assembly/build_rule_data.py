"""Export exact signed equations for an offline teaching experiment.

Does not rerun synthesis or modify research evidence. Parent contacts here
are the 1,194 aligned coarse poses, not the full odd-offset macro census.
"""
import hashlib
import json
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'strong'))
from chair_recut import build_tables, contact_types, rotate, oriented_patch  # noqa: E402


def build(check=False):
    source = ROOT / 'strong/artifacts/chair_recut_synthesis.json'
    synthesis = json.loads(source.read_text())
    types = contact_types()
    _, transitions, _ = build_tables(types)
    profiles = []
    def matrix(r):
        columns = [rotate(e, r) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
        return [columns[j][i] for i in range(3) for j in range(3)]
    for profile in synthesis['profiles']:
        labels = profile['labels']
        equations, ids = [], {}

        def encode(pairs):
            result = set()
            for i, j in pairs:
                a, b = labels[i], labels[j]
                if a == -b:
                    continue
                pair = min(tuple(sorted((a, b))), tuple(sorted((-a, -b))))
                if pair not in ids:
                    ids[pair] = len(equations)
                    equations.append(pair)
                result.add(ids[pair])
            return sorted(result)

        fine = [encode(pairs) for _, _, pairs in types]
        selected = [3*j+q for j, q in enumerate(profile['template'])]
        parent = [sorted({e for j in selected for k in selected
                          if matrix[j][k] >= 0 for e in fine[matrix[j][k]]})
                  for matrix in transitions]
        edges = sorted({tuple(sorted((a, b))) for t in profile['closed_contact_types']
                        for a, b in types[t][2]})
        assert all(labels[a] == -labels[b] for a, b in edges)
        children = [dict(t=t, r=matrix(r)) for t, r in oriented_patch(profile['template'], 1)]
        profiles.append(dict(labels=labels, edges=edges, equations=equations, children=children,
                             fine=fine, parent=parent, templates=profile['template_count']))
    recoding = json.loads((ROOT / 'strong/audit/key_reduction.json').read_text())
    six = recoding['results']['six_depths']['signed_key_mapping']
    result = dict(schema=1, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  sixDepths=[six[str(i)] for i in range(1, 13)],
                  poses=[dict(shift=t, rotation=matrix(r)) for t, r, _ in types], profiles=profiles,
                  scope='Signed-depth equations; proper integer-grid contacts with aligned parent origins. Not a new synthesis or an infinite-tiling proof.')
    destination = ROOT / 'docs/assembly/rule-data.json'
    rendered = json.dumps(result, separators=(',', ':')) + '\n'
    if check:
        if destination.read_text() != rendered:
            raise SystemExit('rule-data.json differs; regenerate with build_rule_data.py')
        print('rule-data.json matches the preserved contact equations.')
    else:
        destination.write_text(rendered)
        print(f'Wrote {destination.relative_to(ROOT)} ({destination.stat().st_size:,} bytes)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)

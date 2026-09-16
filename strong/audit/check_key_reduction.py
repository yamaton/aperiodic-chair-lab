"""Bounded recoding experiment; does not modify the frozen candidate.

Uses the coordinate audit implementation, not an independent verifier.
"""

import hashlib
import json
from pathlib import Path

import verify_from_coordinates as a
from orientation_information import signed_quotient


def allowed(catalogue):
    return {pose for pose, (_, fits) in catalogue.items() if fits}


def run():
    here = Path(__file__).resolve().parent
    raw = (here / 'frozen_v1/candidate.json').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == json.loads((here / 'frozen_v1/manifest.json').read_text())['candidate_sha256']
    data = json.loads(raw)
    solid = a.from_data(data)
    rotations = a.rotation_group()
    original, oriented = a.contact_catalogue(solid, rotations)
    children = [(tuple(c['center']), tuple(x for row in c['matrix'] for x in row)) for c in data['children']]
    macro = a.assemble(children, solid, oriented)
    macrocat, _ = a.contact_catalogue(macro, rotations)
    families, _ = signed_quotient(solid)
    codes = {s*k: (g, q, s) for g, keys in enumerate(families, 1)
             for q, k in enumerate(keys) for s in (-1, 1)}
    results = {}
    for name, depth_count in [('six_depths', 6), ('three_depths', 3)]:
        mapping = {k: (-1)**g*s*(q+1+(3*((g-1)//2) if depth_count == 6 else 0))
                   for k, (g, q, s) in codes.items()}
        keys = [mapping[p['signed_key']] for p in data['ports']]
        assert sum(keys) == 0
        for p, key in zip(data['ports'], keys):
            chirality = a.determinant(tuple(p['u_axis'])+tuple(p['v_axis'])+tuple(p['outward_normal']))
            assert chirality == (-1 if key < 0 else 1)
        recoded = a.from_data(data, keys)
        cat, recoded_orientations = a.contact_catalogue(recoded, rotations)
        result = {'signed_key_mapping': mapping, 'port_keys': keys,
                  'legal_contacts': len(allowed(cat)),
                  'extra_contacts': len(allowed(cat)-allowed(original)),
                  'lost_contacts': len(allowed(original)-allowed(cat)),
                  'signed_key_sum': sum(keys), 'forces_single_handedness': True}
        if depth_count == 6:
            assert allowed(cat) == allowed(original)
            recoded_macro = a.assemble(children, recoded, recoded_orientations)
            mcat, _ = a.contact_catalogue(recoded_macro, rotations)
            assert allowed(mcat) == allowed(macrocat)
            result.update(legal_macrocontacts=len(allowed(mcat)),
                          macrocontacts_identical_to_original=True)
        results[name] = result
    report = {'status': 'passed', 'candidate_sha256': digest,
              'implementation': 'Uses the existing coordinate audit helpers',
              'scope': 'Alternate exact depth assignments, not a replacement frozen design. Six-depth contact and macrocontact languages agree with the reference; the three-depth tiling question is unclassified.',
              'results': results}
    (here / 'key_reduction.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({name: {k: v for k, v in result.items() if k not in ('signed_key_mapping', 'port_keys')}
                      for name, result in results.items()}, indent=2))


if __name__ == '__main__':
    run()

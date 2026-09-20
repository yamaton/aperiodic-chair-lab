"""Q005: one constant value per panel; all 256 stationary handedness words.

Only positive-area pointwise constraints are modeled. Additional independent
edge/vertex labels are not included. Signed values are unconstrained reals.
"""

import hashlib
import json
from pathlib import Path

from geometry import F,child_maps,compose,contacts,contacts_fast,area2,clip2,encode
from polynomial_rules import contact_map
from periodic_obstruction import affine,act
from reflected_search import MIRROR,mirrored_case
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


class Equalities:
    def __init__(self,n,opposite):
        self.parent = list(range(n))
        self.parity = [0]*n
        self.zero = [False]*n
        self.opposite = int(opposite)

    def find(self,x):
        if self.parent[x] != x:
            root,p = self.find(self.parent[x])
            self.parity[x] ^= p
            self.parent[x] = root
        return self.parent[x],self.parity[x]

    def join(self,a,b):
        ra,pa = self.find(a)
        rb,pb = self.find(b)
        if ra == rb:
            if (pa^pb) != self.opposite:
                self.zero[ra] = True
        else:
            self.parent[ra] = rb
            self.parity[ra] = pa^pb^self.opposite
            self.zero[rb] |= self.zero[ra]

    def implies(self,a,b):
        ra,pa = self.find(a)
        rb,pb = self.find(b)
        return (self.zero[ra] and self.zero[rb]) or (ra == rb and (pa^pb) == self.opposite)

    def dimension(self):
        return sum(not self.zero[r] for r in {self.find(i)[0] for i in range(len(self.parent))})


class PanelRules:
    def __init__(self,raw):
        self.panels = [[[tuple(F(v) for v in p) for p in poly] for poly in face] for face in raw['panels']]
        self.offsets = [sum(map(len,self.panels[:f])) for f in range(5)]
        self.count = sum(map(len,self.panels))
        self.cache = {}

    def equations(self,poses,c):
        mapping = affine(contact_map(poses,c))
        key = c['fi'],c['fj'],mapping
        if key not in self.cache:
            edges = []
            for si,poly in enumerate(self.panels[c['fi']]):
                image = [act(mapping,p) for p in poly]
                low = [min(p[k] for p in image) for k in range(2)]
                high = [max(p[k] for p in image) for k in range(2)]
                for ti,target in enumerate(self.panels[c['fj']]):
                    if any(max(p[k] for p in target) <= low[k] or min(p[k] for p in target) >= high[k]
                           for k in range(2)):
                        continue
                    if area2(clip2(image,target)):
                        edges.append((self.offsets[c['fi']]+si,self.offsets[c['fj']]+ti))
            self.cache[key] = edges
        return self.cache[key]

    def constrain(self,poses,cs,opposite):
        result = Equalities(self.count,opposite)
        for c in cs:
            for a,b in self.equations(poses,c):
                result.join(a,b)
        return result


def control_edges(rules,original,mask):
    cell = [raw_pose(p) for p in original['periodic_control']['cell']]
    cell = [compose(p,MIRROR) if (mask>>i)&1 else p for i,p in enumerate(cell)]
    out = []
    for c in original['periodic_control']['contacts']:
        p,q = cell[c['tile']],cell[c['neighbor']]
        q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
        fi,fj = c['fi'],c['fj']
        if (mask>>c['tile'])&1 and fi < 2:
            fi = 1-fi
        if (mask>>c['neighbor'])&1 and fj < 2:
            fj = 1-fj
        out.extend(rules.equations([p,q],dict(i=0,j=1,fi=fi,fj=fj)))
    return sorted(set(out))


def main():
    panel_path = ROOT/'artifacts'/'panel_refinement_v2.json'
    rules = PanelRules(json.loads(panel_path.read_text()))
    original = json.loads((ROOT/'artifacts'/'geometry_and_constant_rules.json').read_text())
    controls = [control_edges(rules,original,mask) for mask in range(4)]
    base = [p for _,p in child_maps()]
    cs = contacts(base)
    results = []
    for mask in range(256):
        poses,mapped = mirrored_case(mask,base,cs)
        current = []
        for opposite in (False,True):
            constraints = rules.constrain(poses,mapped,opposite)
            accepted = [i for i,edges in enumerate(controls) if all(constraints.implies(a,b) for a,b in edges)]
            current.append(dict(mask=mask,condition='opposite' if opposite else 'equal',
                                first_dimension=constraints.dimension(),first_accepted_cells=accepted))
        if any(not r['first_accepted_cells'] for r in current):
            second = [compose(p,q) for p in poses for q in poses]
            second_cs = contacts_fast(second)
            for r in current:
                if not r['first_accepted_cells']:
                    constraints = rules.constrain(second,second_cs,r['condition'] == 'opposite')
                    r['second_dimension'] = constraints.dimension()
                    r['second_accepted_cells'] = [i for i,edges in enumerate(controls)
                                                  if all(constraints.implies(a,b) for a,b in edges)]
                    r['second_contacts'] = len(second_cs)
        results.extend(current)
        if mask % 16 == 15:
            print(f'Finished masks 0..{mask}; cached contact maps {len(rules.cache)}',flush=True)
    unresolved = [r for r in results if not r.get('second_accepted_cells',r['first_accepted_cells'])]
    output = dict(scope='60-panel constant equality/signed values; all 256 stationary handedness words; positive-area contacts',
                  panel_count=rules.count,results=results,not_rejected_by_control=len(unresolved),
                  cached_maps=len(rules.cache),
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'periodic_obstruction.py',
                                     ROOT/'reflected_search.py',ROOT/'reflected_controls.py',panel_path,
                                     ROOT/'artifacts'/'geometry_and_constant_rules.json',Path(__file__))})
    (ROOT/'artifacts'/'piecewise_search.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print('Not rejected:',len(unresolved),flush=True)


if __name__ == '__main__':
    main()

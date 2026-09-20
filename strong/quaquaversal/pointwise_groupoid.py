"""Q010: retain exact panel-frame maps for arbitrary pointwise functions.

Whole-panel identifications are encoded by corner permutations. Composition
is finite because the panels are bounded polygons. Unlike Q005, no function
is assumed constant on a panel. Partial-panel contacts are explicitly ignored
as generators, weakening the premise and hence preserving any derived
periodic obstruction. A control with unhandled partial panels is not accepted.
"""

import argparse
import hashlib
import json
from collections import deque
from itertools import product
from pathlib import Path
import z3

from geometry import F,child_maps,compose,contacts,contacts_fast,area2,clip2,encode
from polynomial_rules import contact_map
from periodic_obstruction import affine,act
from reflected_search import MIRROR,mirrored_case
from reflected_controls import raw_pose

ROOT = Path(__file__).resolve().parent


def corners(poly):
    out = list(poly)
    while True:
        clean = []
        for i,p in enumerate(out):
            a,b = out[i-1],out[(i+1)%len(out)]
            if (p[0]-a[0])*(b[1]-p[1]) != (p[1]-a[1])*(b[0]-p[0]):
                clean.append(p)
        if len(clean) == len(out):
            return tuple(sorted(clean))
        out = clean


class PanelMaps:
    def __init__(self,raw):
        self.faces = [[[tuple(F(x) for x in p) for p in poly] for poly in f] for f in raw['panels']]
        self.offsets = [sum(map(len,self.faces[:f])) for f in range(5)]
        self.corners = [corners(p) for face in self.faces for p in face]
        self.cache = {}
        self.maps = []
        self.index = {}

    def contact(self,poses,c):
        mapping = affine(contact_map(poses,c))
        key = c['fi'],c['fj'],mapping
        if key in self.cache:
            return self.cache[key]
        maps,partials = [],[]
        for si,poly in enumerate(self.faces[c['fi']]):
            image = [act(mapping,p) for p in poly]
            low = [min(p[k] for p in image) for k in range(2)]
            high = [max(p[k] for p in image) for k in range(2)]
            for ti,target in enumerate(self.faces[c['fj']]):
                if any(max(p[k] for p in target) <= low[k] or min(p[k] for p in target) >= high[k] for k in range(2)):
                    continue
                overlap = abs(area2(clip2(image,target)))
                if not overlap:
                    continue
                a,b = self.offsets[c['fi']]+si,self.offsets[c['fj']]+ti
                if overlap != abs(area2(image)) or overlap != abs(area2(target)):
                    partials.append((a,b))
                    continue
                image_corners = tuple(act(mapping,p) for p in self.corners[a])
                assert set(image_corners) == set(self.corners[b])
                permutation = tuple(self.corners[b].index(p) for p in image_corners)
                signature = a,b,permutation
                if signature not in self.index:
                    self.index[signature] = len(self.maps)
                    self.maps.append(dict(source=a,target=b,permutation=permutation,affine=mapping))
                maps.append(self.index[signature])
        self.cache[key] = tuple(maps),tuple(partials)
        return self.cache[key]


class Groupoid:
    def __init__(self,panels,generators):
        self.panels = panels
        self.adjacency = [[] for _ in panels.corners]
        self.cache = {}
        for i in generators:
            g = panels.maps[i]
            a,b,perm = g['source'],g['target'],g['permutation']
            inverse = tuple(perm.index(j) for j in range(len(perm)))
            self.adjacency[a].append((b,perm,i+1))
            self.adjacency[b].append((a,inverse,-i-1))

    def reachable(self,source):
        if source not in self.cache:
            identity = tuple(range(len(self.panels.corners[source])))
            initial = source,identity,0
            seen = {initial:None}
            queue = deque([initial])
            while queue:
                state = queue.popleft()
                a,perm,parity = state
                for b,q,edge in self.adjacency[a]:
                    new = b,tuple(q[j] for j in perm),1-parity
                    if new not in seen:
                        seen[new] = state,edge
                        queue.append(new)
            self.cache[source] = seen
        return self.cache[source]

    def path(self,source,state):
        seen = self.reachable(source)
        out = []
        while seen[state] is not None:
            state,edge = seen[state]
            out.append(edge)
        return list(reversed(out))

    def zero_cycle(self,source):
        target = source,tuple(range(len(self.panels.corners[source]))),1
        return self.path(source,target) if target in self.reachable(source) else None

    def derive(self,identifier,opposite):
        g = self.panels.maps[identifier]
        a,b,perm = g['source'],g['target'],g['permutation']
        for parity in ((1,) if opposite else (0,1)):
            state = b,perm,parity
            if state in self.reachable(a):
                return dict(map=identifier,path=self.path(a,state))
        if opposite:
            za,zb = self.zero_cycle(a),self.zero_cycle(b)
            if za is not None and zb is not None:
                return dict(map=identifier,source_zero_cycle=za,target_zero_cycle=zb)
        return None


def periodic_tables(panels,raw):
    cell = [raw_pose(p) for p in raw['periodic_control']['cell']]
    result = []
    for c in raw['periodic_control']['contacts']:
        options = []
        for ha,hb in product((0,1),repeat=2):
            p,q = cell[c['tile']],cell[c['neighbor']]
            if ha:
                p = compose(p,MIRROR)
            if hb:
                q = compose(q,MIRROR)
            q = q[0],tuple(x+y for x,y in zip(q[1],c['offset'])),q[2]
            fi,fj = c['fi'],c['fj']
            if ha and fi < 2:
                fi = 1-fi
            if hb and fj < 2:
                fj = 1-fj
            maps,partial = panels.contact([p,q],dict(i=0,j=1,fi=fi,fj=fj))
            options.append(dict(handedness=(ha,hb),maps=maps,partial_panels=partial))
        result.append(dict(tile=c['tile'],neighbor=c['neighbor'],offset=c['offset'],options=options))
    return result


def find_periodic(tables,allowed):
    attempts = []
    for size in ((1,1,1),(2,1,1),(1,2,1),(1,1,2),(2,2,1),(2,2,2)):
        boxes = list(product(*(range(n) for n in size)))
        keys = [b+(i,) for b in boxes for i in range(2)]
        variables = {k:z3.Bool('h_'+'_'.join(map(str,k))) for k in keys}
        solver = z3.Solver()
        solver.set(timeout=10000)
        checks = []
        for box in boxes:
            for i,t in enumerate(tables):
                a = box+(t['tile'],)
                b = tuple((x+d)%n for x,d,n in zip(box,t['offset'],size))+(t['neighbor'],)
                solver.add(z3.Or([z3.And(variables[a] == bool(x),variables[b] == bool(y)) for x,y in allowed[i]]))
                checks.append((a,b,i))
        status = solver.check()
        attempts.append(dict(size=size,status=str(status)))
        if status == z3.sat:
            model = solver.model()
            values = {k:int(z3.is_true(model.eval(v,model_completion=True))) for k,v in variables.items()}
            assert all((values[a],values[b]) in allowed[i] for a,b,i in checks)
            return dict(size=size,assignments=[dict(site=k,handedness=v) for k,v in values.items()],
                        checked_contacts=len(checks)),attempts
    return None,attempts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mask',type=int,nargs='+',default=[0,111,144])
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--level',type=int,default=2)
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts'/'pointwise_groupoid_pilot.json')
    args = parser.parse_args()
    panel_path = ROOT/'artifacts'/'panel_refinement_v2.json'
    geometry_path = ROOT/'artifacts'/'geometry_and_constant_rules.json'
    panels = PanelMaps(json.loads(panel_path.read_text()))
    tables = periodic_tables(panels,json.loads(geometry_path.read_text()))
    base = [p for _,p in child_maps()]
    cs = contacts(base)
    results = []
    for mask in (range(256) if args.all else args.mask):
        first,_ = mirrored_case(mask,base,cs)
        poses = first
        for _ in range(1,args.level):
            poses = [compose(p,q) for p in poses for q in first]
        generators = set()
        partials = []
        for c in contacts_fast(poses):
            ids,partial = panels.contact(poses,c)
            generators.update(ids)
            partials.extend(partial)
        group = Groupoid(panels,sorted(generators))
        for opposite in (False,True):
            proofs,allowed = [],[]
            for t in tables:
                choices = []
                for option in t['options']:
                    derivations = [group.derive(k,opposite) for k in option['maps']]
                    if not option['partial_panels'] and all(p is not None for p in derivations):
                        choices.append(option['handedness'])
                        proofs.append(dict(table=len(allowed),handedness=option['handedness'],derivations=derivations))
                allowed.append(choices)
            witness,attempts = find_periodic(tables,allowed)
            entry = dict(mask=mask,level=args.level,condition='opposite' if opposite else 'equal',
                         generators=sorted(generators),ignored_partial_panel_pairs=sorted(set(partials)),
                         allowed_handedness_pairs=allowed,proofs=proofs,witness=witness,attempts=attempts)
            results.append(entry)
            print(json.dumps(dict(mask=mask,condition=entry['condition'],generators=len(generators),
                                  partials=len(set(partials)),witness_size=witness['size'] if witness else None)),flush=True)
    output = dict(scope='Arbitrary functions on whole panel domains; exact affine identifications; partial generators omitted',
                  panel_corners=panels.corners,maps=panels.maps,periodic_tables=tables,results=results,
                  arguments={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'geometry.py',ROOT/'polynomial_rules.py',ROOT/'periodic_obstruction.py',
                                     ROOT/'reflected_search.py',ROOT/'reflected_controls.py',panel_path,geometry_path,Path(__file__))})
    args.output.write_text(json.dumps(encode(output),indent=2)+'\n')


if __name__ == '__main__':
    main()

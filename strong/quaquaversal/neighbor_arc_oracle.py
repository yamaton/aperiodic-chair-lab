"""Necessary arc propagation and choice certificates for a finite SAT model.

Position keys use a common exact denominator for R and normalized t/scale.
Only present positions enter the arc test. A returned cut explicitly forces
every proof position through the remaining original center-star choices.
"""

from collections import deque
from functools import lru_cache


def members(bits):
    while bits:
        low = bits & -bits
        yield low.bit_length()-1
        bits -= low


class ArcOracle:
    def __init__(self, positions, position_ids, atlas_rotations, atlas_translations,
                 atlas_denominator, cases, domain_bits, reverse):
        self.positions = positions
        self.position_ids = position_ids
        self.ars, self.ats, self.d = atlas_rotations, atlas_translations, atlas_denominator
        self.cases, self.bits, self.reverse = cases, domain_bits, reverse

    @lru_cache(maxsize=200000)
    def rotation(self, r, q):
        a = self.ars[q]
        return tuple(sum(r[3*i+k]*a[k][j] for k in range(3)) for i in range(3) for j in range(3))

    @lru_cache(maxsize=600000)
    def neighbor_key(self, pos, q):
        p = self.positions[pos]
        r = p[:9]
        rr = self.rotation(r, q)
        tt = tuple(p[9+i]*self.d+sum(r[3*i+j]*self.ats[q][j] for j in range(3)) for i in range(3))
        if any(v % self.d for v in rr+tt):
            return None
        return tuple(v//self.d for v in rr+tt)

    @lru_cache(maxsize=100000)
    def possible(self, value):
        return tuple(sorted({q for s in members(value) for q in self.cases[s]}))

    @lru_cache(maxsize=200000)
    def supported(self, value, other, q):
        return sum(1<<s for s in members(value)
                   if q in self.cases[s] and self.bits[self.cases[s][q]] & other)

    def run(self, requirements, intersection):
        ds = {pos:intersection(rs) for pos,rs in requirements.items()}
        assert all(ds.values())
        adjacency = {pos:{} for pos in ds}
        for pos,value in ds.items():
            for q in self.possible(value):
                other = self.position_ids.get(self.neighbor_key(pos,q))
                if other in ds:
                    assert other != pos
                    assert other not in adjacency[pos] or adjacency[pos][other] == q
                    adjacency[pos][other] = q
                    adjacency[other][pos] = self.reverse[q]
        edges = [(x,y,q) for x,row in adjacency.items() for y,q in row.items()]
        queue, queued = deque(edges), set(edges)
        trace = []
        while queue:
            x,y,q = queue.popleft()
            queued.remove((x,y,q))
            new = self.supported(ds[x],ds[y],q)
            if new == ds[x]:
                continue
            trace.append((x,y,q))
            ds[x] = new
            if not new:
                break
            for z,r in adjacency[x].items():
                edge = z,x,self.reverse[r]
                if edge not in queued:
                    queue.append(edge)
                    queued.add(edge)
        info = dict(directed_edges=len(edges),reductions=len(trace))
        if all(ds.values()):
            info['retained_domains'] = [[p,list(members(v))] for p,v in sorted(ds.items())]
            return None,info
        target = trace[-1][0]
        needed, sliced = {target}, []
        for x,y,q in reversed(trace):
            if x in needed:
                needed.add(y)
                sliced.append((x,y,q))
        sliced.reverse()
        rs = {p:requirements[p] for p in sorted(needed)}
        choices = {(r['tile'],r['star']) for reasons in rs.values() for r in reasons}

        def replay(hypotheses):
            domains = {}
            for pos,reasons in rs.items():
                kept = [r for r in reasons if (r['tile'],r['star']) in hypotheses]
                if not kept:
                    return False  # Presence cannot be silently assumed.
                domains[pos] = intersection(kept)
            for x,y,q in sliced:
                domains[x] = self.supported(domains[x],domains[y],q)
            return not domains[target]

        assert replay(choices)
        unminimized = len(choices)
        for choice in sorted(choices):
            if replay(choices-{choice}):
                choices.remove(choice)
        assert replay(choices)
        certificate = dict(target=target,reduction_trace=sliced,
                           requirements=[[p,[r for r in reasons if (r['tile'],r['star']) in choices]]
                                         for p,reasons in rs.items()],unminimized_choices=unminimized)
        return (tuple(sorted(choices)),certificate),info

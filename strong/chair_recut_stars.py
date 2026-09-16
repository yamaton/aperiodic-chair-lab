"""Enumerate complete face-neighborhoods of the remaining recut chair.

Local stars need not extend to infinite tilings. The experiment asks whether
they already force the stationary eight-chair grouping.
"""

from itertools import combinations
import json

from chair_recut import (CHILDREN, CHILD_ROTATIONS, IDENTITY, INVERSE, MULTIPLY,
                         VOXELS, contact_types, rotate)
from offset_dipoles import OUT


def moved_voxels(t, r):
    return {tuple(2 * t[k] + rotate(p, r)[k] for k in range(3)) for p in VOXELS}


def relative(a, b):
    ca, ra = a
    cb, rb = b
    return (rotate(tuple(cb[k] - ca[k] for k in range(3)), INVERSE[ra]),
            MULTIPLY[INVERSE[ra]][rb])


def clusters_at_anchor(template):
    rotations = [CHILD_ROTATIONS[j][q] for j, q in enumerate(template)]
    result = []
    for j, (p, _) in enumerate(CHILDREN):
        r = INVERSE[rotations[j]]
        t = tuple(-v for v in rotate(p, r))
        result.append(frozenset((tuple(t[k] + rotate(c, r)[k] for k in range(3)),
                                 MULTIPLY[r][rotations[u]])
                                for u, (c, _) in enumerate(CHILDREN)))
    return result


def enumerate_stars(profile, types):
    all_types = {(t, r): i for i, (t, r, _) in enumerate(types)}
    labels = profile["labels"]
    allowed = {i for i, (_, _, pairs) in enumerate(types)
               if all(labels[a] == -labels[b] for a, b in pairs)}
    candidates = sorted(allowed)
    placements = [(types[i][0], types[i][1]) for i in candidates]
    masks = [sum(1 << face for face in {a // 8 for a, _ in types[i][2]})
             for i in candidates]
    voxels = [moved_voxels(*p) for p in placements]
    compatible = [(1 << len(candidates)) - 1 for _ in candidates]
    for i, j in combinations(range(len(candidates)), 2):
        contact = all_types.get(relative(placements[i], placements[j]))
        if masks[i] & masks[j] or voxels[i] & voxels[j] or (contact is not None and contact not in allowed):
            compatible[i] &= ~(1 << j)
            compatible[j] &= ~(1 << i)
    by_face = [sum(1 << i for i, mask in enumerate(masks) if mask & (1 << f)) for f in range(24)]
    full = (1 << 24) - 1
    stars, nodes = [], 0

    def visit(covered, available, selected):
        nonlocal nodes
        nodes += 1
        if covered == full:
            stars.append(tuple(sorted(selected)))
            return
        choices = min((by_face[f] & available for f in range(24) if not covered & (1 << f)),
                      key=int.bit_count)
        while choices:
            bit = choices & -choices
            choices ^= bit
            i = bit.bit_length() - 1
            visit(covered | masks[i], available & compatible[i] & ~bit, (*selected, i))

    visit(0, (1 << len(candidates)) - 1, ())
    assert len(stars) == len(set(stars))
    return placements, stars, nodes, all_types, allowed


def run():
    index = 1
    profile = json.loads((OUT / "chair_recut_synthesis.json").read_text())["profiles"][index]
    types = contact_types()
    placements, stars, nodes, all_types, allowed = enumerate_stars(profile, types)
    print(f"Complete stars: {len(stars)}, search nodes: {nodes}", flush=True)
    anchor = ((0, 0, 0), IDENTITY)
    neighborhoods = [frozenset([anchor, *(placements[i] for i in star)]) for star in stars]
    groups = clusters_at_anchor(profile["template"])
    central = [groups[0] <= neighborhood for neighborhood in neighborhoods]

    # Can two candidate substitution groups coexist if they share the anchor?
    overlapping_groups = []
    for i, j in combinations(range(8), 2):
        union = groups[i] | groups[j]
        occupied = set()
        for placement in union:
            cubes = moved_voxels(*placement)
            if occupied & cubes:
                break
            occupied |= cubes
        else:
            if all((t := all_types.get(relative(a, b))) is None or t in allowed
                   for a, b in combinations(union, 2)):
                overlapping_groups.append((i, j))

    # A neighbor's full star must contain every member of this star that
    # touches it, as well as the anchor. These are necessary compatibility
    # conditions only; unresolved stars are not infinite counterexamples.
    outcomes = []
    for s, neighborhood in enumerate(neighborhoods):
        witnesses = []
        for neighbor in neighborhood - {anchor}:
            required = {relative(neighbor, tile) for tile in neighborhood
                        if tile != neighbor and relative(neighbor, tile) in all_types}
            possibilities = [j for j, candidate in enumerate(neighborhoods) if required <= candidate]
            anchor_from_neighbor = relative(neighbor, anchor)
            if possibilities and all(central[j] and anchor_from_neighbor in groups[0] for j in possibilities):
                witnesses.append({"neighbor": neighbor, "compatible_stars": possibilities})
        outcomes.append({"star_index": s, "anchor_is_central": central[s],
                         "forced_parent_neighbors": witnesses})
    result = {"profile_index": index, "candidate_neighbor_placements": placements,
              "stars": stars, "star_count": len(stars), "search_nodes": nodes,
              "central_stars": sum(central), "outcomes": outcomes,
              "stars_without_group_certificate": [o["star_index"] for o in outcomes
                                                  if not o["anchor_is_central"] and not o["forced_parent_neighbors"]],
              "compatible_overlapping_group_pairs": overlapping_groups,
              "limit": "Complete face stars are necessary local configurations, not certified infinite tilings; the parent test uses only one ring of star compatibility."}
    (OUT / "chair_recut_stars.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("candidate_neighbor_placements", "stars", "outcomes")}, indent=2))


if __name__ == "__main__":
    run()

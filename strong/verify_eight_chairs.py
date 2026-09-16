"""Independently check cluster screening, exact covers, and a periodic control."""

from collections import Counter
from itertools import product
import json

from chair_clusters import key, patch
from offset_dipoles import OUT
from open_chair_clusters import placements, region, shapes_at_anchor
from verify_open_chairs import independent_cover


def voxel_union(chairs):
    voxels = set()
    for c, s in chairs:
        for p in product((-1, 1), repeat=3):
            if p == (1, 1, 1):
                continue
            q = tuple(2 * c[k] + s[k] * p[k] for k in range(3))
            assert q not in voxels
            voxels.add(q)
    return voxels


def run():
    report = json.loads((OUT / "chair_screen_8_level5.json").read_text())
    assert report["enumeration_complete"]
    assert report["rooted_clusters_examined"] == report["accepted_rooted_clusters"] + sum(report["rejected_at_target"])
    tiles, _, distances = region(5)
    core = set(report["core_chairs"])
    assert core == {i for i, d in distances.items() if d >= 7}
    assert distances[report["root"]] >= 7
    assert set(report["targets"]) | {report["root"]} == core

    # Cross-check the compiled enumeration against the original set-growth
    # method in smaller, completely enumerated control cases.
    controls = []
    for size in (4, 5):
        other = json.loads((OUT / f"chair_screen_{size}_level4.json").read_text())
        small_tiles, adjacency, _ = region(4)
        _, rooted_count = shapes_at_anchor(small_tiles, adjacency, other["root"], size)
        assert other["enumeration_complete"] and rooted_count == other["rooted_clusters_examined"]
        controls.append({"size": size, "rooted_clusters": rooted_count})

    rejected_checked = 0
    for example in report["rejection_examples"]:
        shape = [tiles[i] for i in example["cluster"]]
        assert not placements(shape, tiles, {example["target"]})
        rejected_checked += 1

    exact_checks, satisfiable = [], []
    for index, record in enumerate(report["shapes"]):
        shape = [(tuple(c), tuple(s)) for c, s in record["chairs"]]
        options = placements(shape, tiles, core)
        assert len(options) == record["placements"]
        assert set().union(*(set(p) for p in options)) >= core
        result = record["cover"]
        if result["status"] == "sat":
            selected = result["selected"]
            allowed = set(options)
            assert all(tuple(ids) in allowed for ids in selected)
            count = Counter(i for ids in selected for i in ids)
            assert max(count.values()) == 1 and all(count[i] == 1 for i in core)
            satisfiable.append(index)
        else:
            required = core
            certificate_file = OUT / "eight_chair_small_certificate.json"
            if index == 1 and certificate_file.exists():
                certificate = json.loads(certificate_file.read_text())
                required = set(certificate["required_chairs"])
                assert required <= core and certificate["shape_index"] == index
                options = [ids for ids in options if required.intersection(ids)]
                assert options == [tuple(ids) for ids in certificate["all_placements_touching_required_chairs"]]
                assert len(required) % 2 == 1
                assert all(len(required.intersection(ids)) % 2 == 0 for ids in options)
            sat, stats = independent_cover(options, required)
            assert not sat and result["status"] == "unsat"
            exact_checks.append({"shape_index": index, "required_chairs_checked": len(required), **stats})
    assert len(satisfiable) == 1
    survivor = report["shapes"][satisfiable[0]]["chairs"]
    assert key(survivor) == key(patch(1))

    # Independent physical control: the unmarked survivor is just a scaled
    # chair. Seven 2x2x2 voxel cubes represent binary residues 0..6 modulo 7.
    standard = voxel_union(patch(1))
    assert len(standard) == 56
    shifted = {tuple((v + 3) // 2 for v in p) for p in standard}
    expected = {p for p in product(range(4), repeat=3) if not all(v >= 2 for v in p)}
    assert shifted == expected

    # Lattice columns (14,0,0), (-4,2,0), (-8,0,2), determinant 56.
    # Each voxel of the tile occupies one distinct quotient class.
    def residue(p):
        x, y, z = p
        q, z = divmod(z, 2)
        x += 8 * q
        q, y = divmod(y, 2)
        x += 4 * q
        return (x % 14, y, z)
    residues = Counter(residue(p) for p in shifted)
    assert len(residues) == 56 and set(residues.values()) == {1}

    result = {"status": "passed", "enumeration_controls": controls,
              "rooted_eight_clusters": report["rooted_clusters_examined"],
              "rejected_placement_witnesses_checked": rejected_checked,
              "surviving_occurrence_classes": len(report["shapes"]),
              "independent_exact_cover_exclusions": exact_checks,
              "valid_cover_shape_index": satisfiable[0], "survivor_is_standard_supertile": True,
              "unmarked_survivor_periodic_control": {
                  "voxel_volume": 56, "lattice_basis_columns": [[14, 0, 0], [-4, 2, 0], [-8, 0, 2]],
                  "distinct_quotient_voxels": 56, "holes": 0, "overlaps": 0,
                  "limit": "This periodic certificate concerns the unmarked coarse polycube, not a hypothetical keyed fusion."},
              "scope": "Whole-chair groups with proper rotations and sufficient halo; not arbitrary 3D monotiles."}
    (OUT / "eight_chair_verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "independent_exact_cover_exclusions"}, indent=2))


if __name__ == "__main__":
    run()

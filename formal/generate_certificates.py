"""Generate untrusted contact witnesses for the Lean certificate checker.

Coordinates come only from the frozen JSON. Lean checks these witnesses against
its own reconstructed solids and proves coverage; this Python search is not a
proof dependency. Run using uv. --check checks deterministic reproduction.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from generate_input import SOURCE, SHA256, vec

HERE = Path(__file__).resolve().parent
NORMALS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(k, a):
    return tuple(k * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def rotations():
    return [tuple(zip(u, v, cross(u, v))) for u in NORMALS for v in NORMALS if dot(u, v) == 0]


def apply(r, p):
    return tuple(dot(row, p) for row in r)


def move_cube(r, t, q):
    return add(add(apply(r, q), tuple(sum(min(x, 0) for x in row) for row in r)), t)


def move_port(r, t, p):
    pos, key, u, v, n = p
    return add(apply(r, pos), scale(16, t)), key, apply(r, u), apply(r, v), apply(r, n)


def make_solid(cells, ports):
    occupied = set(cells)
    faces = []
    for q in cells:
        for n in NORMALS:
            if add(q, n) in occupied:
                continue
            center = add(add(scale(2, q), (1, 1, 1)), n)
            on_face = [p[:4] for p in ports if p[4] == n and
                       p[0] == add(add(scale(8, center), scale(3, p[2])), p[3])]
            assert len(on_face) == 8
            faces.append((center, n, on_face))
    return cells, faces


def move_solid(r, solid):
    cells, faces = solid
    return ([move_cube(r, (0, 0, 0), q) for q in cells],
            [(apply(r, f), apply(r, n),
              [(apply(r, p), k, apply(r, u), apply(r, v)) for p, k, u, v in ps])
             for f, n, ps in faces])


def fitting(a, b, t):
    return set(a) == {(add(p, scale(16, t)), -k, u, v) for p, k, u, v in b}


def witnesses(s, u):
    cells, faces = s
    other_cells, other_faces = u
    offsets = dict.fromkeys(
        tuple((x-y)//2 for x, y in zip(a, b))
        for a, an, _ in faces for b, bn, _ in other_faces
        if an == scale(-1, bn) and all((x-y) % 2 == 0 for x, y in zip(a, b))
    )
    accepted, rejected = [], []
    own_index = {q: i for i, q in enumerate(cells)}
    own_faces = {(f, n): i for i, (f, n, _) in enumerate(faces)}
    for t in offsets:
        overlap = next(((own_index[add(q, t)], j) for j, q in enumerate(other_cells)
                        if add(q, t) in own_index), None)
        if overlap is not None:
            rejected.append((t, "overlap", *overlap))
            continue
        mismatch = None
        touched = False
        for j, (f, n, ps) in enumerate(other_faces):
            i = own_faces.get((add(f, scale(2, t)), scale(-1, n)))
            if i is not None:
                touched = True
                if not fitting(faces[i][2], ps, t):
                    mismatch = i, j
                    break
        assert touched
        if mismatch is not None:
            rejected.append((t, "mismatch", *mismatch))
        else:
            accepted.append(t)
    return accepted, rejected


def construction():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA256
    data = json.loads(raw)
    cells = [tuple(q) for q in data["coarse_cubes"]]
    ports = []
    for p in data["ports"]:
        p16 = [16*Fraction(v) for v in p["center"]]
        assert all(v.denominator == 1 for v in p16)
        ports.append((tuple(int(v) for v in p16), p["signed_key"], tuple(p["u_axis"]),
                      tuple(p["v_axis"]), tuple(p["outward_normal"])))
    macro_cells, macro_ports = [], []
    for child in data["children"]:
        r, t = child["matrix"], tuple(child["center"])
        macro_cells.extend(move_cube(r, t, q) for q in cells)
        macro_ports.extend(move_port(r, t, p) for p in ports)
    return make_solid(cells, ports), make_solid(macro_cells, macro_ports)


def render():
    fine, macro = construction()
    lines = ["-- Untrusted witnesses; all are checked by Lean. Generated; do not edit.",
             f"-- Frozen candidate SHA-256: {SHA256}",
             "import Chair.Certificate", "import Chair.Candidate", "", "namespace Chair.Witnesses", ""]
    results = []
    for i, r in enumerate(rotations()):
        fa, fr = witnesses(fine, move_solid(r, fine))
        ma, mr = witnesses(macro, move_solid(r, macro))
        assert set(ma) == {scale(2, t) for t in fa}
        results.append(dict(orientation=i, matrix=r, fine_accepted=fa,
                            macro_accepted=ma, fine_rejected=len(fr), macro_rejected=len(mr)))
        for name, accepted, rejected in [("fine", fa, fr), ("macro", ma, mr)]:
            lines.append(f"def {name}Accepted{i} : List V3 := [{', '.join(map(vec, accepted))}]")
            entries = ",\n  ".join(f"({vec(t)}, .{kind} {a} {b})" for t, kind, a, b in rejected)
            lines.append(f"def {name}Rejected{i} : List (V3 × RejectWitness) := [\n  {entries}]\n")
    lines.extend(["end Chair.Witnesses", ""])
    assert sum(len(row["fine_accepted"]) for row in results) == 44
    return "\n".join(lines), dict(candidate_sha256=SHA256, orientations=results,
                                  scope="Untrusted generated certificate summary; Lean checks the witnesses.")


def render_cache():
    """Normalization is only an optimization: Lean proves both equalities."""
    fine, macro = construction()
    lines = ["-- Untrusted evaluation cache: equalities below are kernel-checked.",
             "import Chair.Candidate", "", "namespace Chair",
             "set_option maxHeartbeats 0", "set_option maxRecDepth 100000",
             ""]
    for name, (cells, faces) in [("Fine", fine), ("Macro", macro)]:
        entries = []
        for f, n, ps in faces:
            ports = ", ".join(f"⟨{vec(p)}, {k}, {vec(u)}, {vec(v)}⟩" for p, k, u, v in ps)
            entries.append(f"⟨{vec(f)}, {vec(n)}, [{ports}]⟩")
        lines.append(f"def cached{name} : Solid := ⟨[{', '.join(map(vec, cells))}], [\n  "
                     + ",\n  ".join(entries) + "]⟩\n")
    lines.extend(["theorem fine_eq_cached : fine = cachedFine := by decide +kernel",
                  "theorem macro_eq_cached : macroSolid = cachedMacro := by decide +kernel",
                  "", "end Chair", ""])
    return "\n".join(lines)


def render_batch(batch):
    lines = ["import Chair.Witnesses", "import Chair.Cache", "", "namespace Chair",
             "open Witnesses", "", "set_option maxHeartbeats 0",
             "set_option maxRecDepth 100000", "set_option Elab.async false", ""]
    for i in range(6 * batch, 6 * (batch + 1)):
        for name, solid, orient in [("fine", "fine", "orientedFine"),
                                    ("macro", "macroSolid", "orientedMacro")]:
            lines.extend([f"theorem {name}_certificate_{i} :",
                          f"    certificateCheck {solid} ({orient} {i}) {name}Accepted{i} {name}Rejected{i} = true := by",
                          f"  simp only [{orient}, {name}_eq_cached]", "  decide +kernel", ""])
    lines.extend(["end Chair", ""])
    return "\n".join(lines)


def render_checks():
    lines = [*(f"import Chair.Batches.Batch{i}" for i in range(4)), "",
             "namespace Chair", "open Witnesses", "",
             "set_option maxRecDepth 100000", ""]
    for name in ["fine", "macro"]:
        for typ in ["Accepted", "Rejected"]:
            result = "List V3" if typ == "Accepted" else "List (V3 × RejectWitness)"
            lines.append(f"def {name}{typ} (r : Fin 24) : {result} := match r.val with")
            lines.extend(f"  | {i} => {name}{typ}{i}" for i in range(24))
            lines.extend(["  | _ => []", ""])
        solid = "fine" if name == "fine" else "macroSolid"
        orient = "orientedFine" if name == "fine" else "orientedMacro"
        lines.extend([f"theorem {name}_certificates (r : Fin 24) :",
                      f"    certificateCheck {solid} ({orient} r) ({name}Accepted r) ({name}Rejected r) = true := by"])
        proof = "(fun r => Fin.elim0 r)"
        for i in reversed(range(24)):
            proof = f"(Fin.cases {name}_certificate_{i} {proof})"
        lines.extend(["  revert r", f"  exact {proof}", ""])
    lines.extend(["end Chair", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    lean, summary = render()
    outputs = {HERE / "Chair/Witnesses.lean": lean,
               HERE / "Chair/Cache.lean": render_cache(),
               HERE / "Chair/Checked.lean": render_checks(),
               HERE / "certificate_summary.json": json.dumps(summary, indent=2) + "\n"}
    outputs.update({HERE / f"Chair/Batches/Batch{i}.lean": render_batch(i) for i in range(4)})
    for path, content in outputs.items():
        if args.check:
            assert path.read_text() == content, f"Stale generated file: {path}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print("Contact witnesses: deterministic match" if args.check else "Generated contact witnesses for 24 orientations")


if __name__ == "__main__":
    main()

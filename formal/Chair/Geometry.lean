import Chair.Model

namespace Chair

def V3.dot (a b : V3) : Int := a.x*b.x + a.y*b.y + a.z*b.z
def V3.cross (a b : V3) : V3 :=
  ⟨a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x⟩

/-- Matrices are stored by rows. -/
structure Mat where
  x : V3
  y : V3
  z : V3
  deriving DecidableEq, BEq, Repr

def Mat.apply (r : Mat) (p : V3) : V3 := ⟨r.x.dot p, r.y.dot p, r.z.dot p⟩
def Mat.ofColumns (u v w : V3) : Mat :=
  ⟨⟨u.x,v.x,w.x⟩, ⟨u.y,v.y,w.y⟩, ⟨u.z,v.z,w.z⟩⟩

def normals : List V3 :=
  [⟨-1,0,0⟩, ⟨1,0,0⟩, ⟨0,-1,0⟩, ⟨0,1,0⟩, ⟨0,0,-1⟩, ⟨0,0,1⟩]

/-- All choices of perpendicular signed coordinate columns, completed by cross product.
No coarse-chair symmetry quotient is taken. -/
def rotations : List Mat := normals.flatMap fun u =>
  (normals.filter fun v => u.dot v == 0).map fun v => Mat.ofColumns u v (u.cross v)

theorem rotations_length : rotations.length = 24 := by decide_cbv
theorem rotations_distinct : rotations.Nodup := by decide_cbv

def rotation (r : Fin 24) : Mat := rotations[r.val]'(by rw [rotations_length]; exact r.isLt)

/-- Minimum corner of the image of a unit cube under a signed permutation. -/
def Mat.cube (r : Mat) (q : V3) : V3 :=
  let negSum (v : V3) := min v.x 0 + min v.y 0 + min v.z 0
  (r.apply q).add ⟨negSum r.x, negSum r.y, negSum r.z⟩

structure RawPort where
  pos16 : V3
  key : Int
  u : V3
  v : V3
  normal : V3
  deriving DecidableEq, BEq, Repr

structure Placement where
  shift : V3
  frame : Mat
  deriving DecidableEq, BEq, Repr

def RawPort.move (g : Placement) (p : RawPort) : RawPort :=
  ⟨(g.frame.apply p.pos16).add (g.shift.scale 16), p.key,
    g.frame.apply p.u, g.frame.apply p.v, g.frame.apply p.normal⟩

def faceCenter2 (q n : V3) : V3 := ((q.scale 2).add ⟨1,1,1⟩).add n

/-- Recover exposed unit faces from cells and assign ports by the exact frozen
offset equation p16 = 8*faceCenter2 + 3*u + v. -/
def makeSolid (cells : List V3) (ports : List RawPort) : Solid :=
  ⟨cells, cells.flatMap fun q =>
    (normals.filter fun n => !(cells.contains (q.add n))).map fun n =>
      let f := faceCenter2 q n
      let ps := ports.filter fun p => p.normal == n &&
        p.pos16 == ((f.scale 8).add (p.u.scale 3)).add p.v
      ⟨f, n, ps.map fun p => ⟨p.pos16, p.key, p.u, p.v⟩⟩⟩

def moveSolid (g : Placement) (s : Solid) : Solid :=
  ⟨s.cells.map fun q => (g.frame.cube q).add g.shift,
   s.faces.map fun f =>
     ⟨(g.frame.apply f.center2).add (g.shift.scale 2), g.frame.apply f.normal,
      f.ports.map fun p =>
        ⟨(g.frame.apply p.pos16).add (g.shift.scale 16), p.key,
          g.frame.apply p.u, g.frame.apply p.v⟩⟩⟩

end Chair

"""Explicit SCD biprism, using column-vector rotations and unambiguous angles.

The construction is known, not a claim of a new monotile. See RESEARCH.md.
"""

from dataclasses import dataclass
from itertools import product

import numpy as np
from scipy.spatial import ConvexHull


@dataclass(frozen=True)
class Block:
    cosine: float = 1 / 3
    ridge: float = 1 / 3
    height: float = 2 / 5

    @property
    def angle(self):
        return np.arccos(self.cosine)

    @property
    def basis(self):
        return np.array([[1., self.cosine], [0., np.sqrt(1 - self.cosine**2)]])

    @property
    def vertices(self):
        a = np.array([1., 0., 0.])
        b = np.r_[self.basis[:, 1], 0.]
        c = self.ridge * b + [0., 0., self.height]
        d = self.ridge * a - [0., 0., self.height]
        return np.array([a * 0, a, b, a + b, c, a + c, d, b + d])

    @property
    def center_shift(self):
        return self.vertices[4]

    def rotation(self, layer):
        t = -layer * self.angle
        return np.array([[np.cos(t), -np.sin(t), 0.],
                         [np.sin(t), np.cos(t), 0.], [0., 0., 1.]])

    def tile(self, layer, i, j, slip=None):
        offset = np.r_[self.basis @ [i, j], 0.] - self.center_shift
        vertices = (self.vertices + offset) @ self.rotation(layer).T
        vertices += [0., 0., layer * self.height]
        if slip is not None:
            vertices += slip
        return vertices

    def tent(self, t):
        t = np.asarray(t) % 1
        return np.minimum(t / self.ridge, (1 - t) / (1 - self.ridge))

    def surfaces(self, xy, layer, slip=None):
        xy = np.asarray(xy)
        if slip is not None:
            xy = xy - np.asarray(slip)[:2]
        local = xy @ self.rotation(layer)[:2, :2]
        uv = local @ np.linalg.inv(self.basis).T
        lower = self.height * (layer - 1 - self.tent(uv[:, 0]))
        upper = self.height * (layer - 1 + self.tent(uv[:, 1] + self.ridge))
        return lower, upper


def triangles(vertices):
    """Hull triangles with outward orientation, suitable for STL."""
    hull = ConvexHull(vertices)
    faces = hull.simplices.copy()
    for face, plane in zip(faces, hull.equations):
        p, q, r = vertices[face]
        if np.dot(np.cross(q - p, r - p), plane[:3]) < 0:
            face[1], face[2] = face[2], face[1]
    return faces


def polygon_faces(vertices):
    """Merge the hull's coplanar triangles for uncluttered display."""
    hull = ConvexHull(vertices)
    groups = {}
    for tri, equation in zip(hull.simplices, hull.equations):
        key = tuple(np.round(equation, 9))
        groups.setdefault(key, set()).update(tri)
    faces = []
    for equation, indices in groups.items():
        indices = np.array(sorted(indices))
        points = vertices[indices]
        center = points.mean(axis=0)
        u = points[0] - center
        u /= np.linalg.norm(u)
        v = np.cross(equation[:3], u)
        angles = np.arctan2((points - center) @ v, (points - center) @ u)
        faces.append(indices[np.argsort(angles)].tolist())
    return faces


def patch(block, layers=range(7), radius=2, fault=False):
    result = []
    for m, i, j in product(layers, range(-radius, radius + 1), range(-radius, radius + 1)):
        # The seam between layers 0 and 1 runs parallel to a, the x axis.
        slip = [np.sqrt(2) / 10, 0., 0.] if fault and m >= 1 else None
        result.append((m, i, j, block.tile(m, i, j, slip)))
    return result

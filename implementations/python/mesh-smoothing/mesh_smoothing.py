"""Uniform Laplacian and Taubin smoothing for triangular surface meshes."""
from __future__ import annotations
from collections import Counter
from collections.abc import Sequence
import numpy as np

def _prepare(vertices: Sequence[Sequence[float]], faces: Sequence[Sequence[int]]):
    points = np.asarray(vertices, dtype=float)
    triangles = np.asarray(faces, dtype=int)
    if points.ndim != 2 or points.shape[1] != 3 or not np.isfinite(points).all():
        raise ValueError("vertices must be a finite (n, 3) array")
    if triangles.ndim != 2 or triangles.shape[1] != 3:
        raise ValueError("faces must be an (m, 3) triangle index array")
    if triangles.size and (triangles.min() < 0 or triangles.max() >= len(points)):
        raise ValueError("face index is outside the vertex array")
    if triangles.size and any(len(set(map(int, f))) != 3 for f in triangles):
        raise ValueError("each face must contain three distinct vertex indices")
    adjacency = [set() for _ in range(len(points))]
    edge_counts = Counter()
    for face in triangles:
        a, b, c = map(int, face)
        for u, v in ((a,b),(b,c),(c,a)):
            adjacency[u].add(v); adjacency[v].add(u)
            edge_counts[(min(u,v), max(u,v))] += 1
    if any(count > 2 for count in edge_counts.values()):
        raise ValueError("non-manifold edges (incident to more than two faces) are unsupported")
    boundary = {v for edge, count in edge_counts.items() if count == 1 for v in edge}
    return points.copy(), adjacency, boundary

def _fixed_indices(count, fixed_vertices):
    fixed = set() if fixed_vertices is None else {int(i) for i in fixed_vertices}
    if any(i < 0 or i >= count for i in fixed):
        raise ValueError("fixed vertex index is outside the vertex array")
    return fixed

def _step(points, adjacency, fixed, factor):
    updated = points.copy()
    for i, neighbours in enumerate(adjacency):
        if i not in fixed and neighbours:
            mean = points[sorted(neighbours)].mean(axis=0)
            updated[i] = points[i] + factor * (mean - points[i])
    return updated

def laplacian_smooth(vertices, faces, *, iterations=1, lam=0.5,
                     fixed_vertices=None, fix_boundary=False):
    """Simultaneous uniform one-ring Laplacian smoothing."""
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 0:
        raise ValueError("iterations must be a non-negative integer")
    if not np.isfinite(lam) or not 0 <= lam <= 1:
        raise ValueError("lam must be finite and in [0, 1]")
    points, adjacency, boundary = _prepare(vertices, faces)
    fixed = _fixed_indices(len(points), fixed_vertices)
    if fix_boundary: fixed |= boundary
    for _ in range(iterations): points = _step(points, adjacency, fixed, float(lam))
    return points

def taubin_smooth(vertices, faces, *, iterations=1, lam=0.5, mu=-0.53,
                  fixed_vertices=None, fix_boundary=False):
    """Alternate positive lambda and negative mu Laplacian passes."""
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 0:
        raise ValueError("iterations must be a non-negative integer")
    if not np.isfinite(lam) or not np.isfinite(mu):
        raise ValueError("lambda and mu must be finite")
    if not 0 < lam <= 1 or not -1 <= mu < 0:
        raise ValueError("require 0 < lam <= 1 and -1 <= mu < 0")
    points, adjacency, boundary = _prepare(vertices, faces)
    fixed = _fixed_indices(len(points), fixed_vertices)
    if fix_boundary: fixed |= boundary
    for _ in range(iterations):
        points = _step(points, adjacency, fixed, float(lam))
        points = _step(points, adjacency, fixed, float(mu))
    return points

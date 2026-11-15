"""Shortest paths on the edge graph of a triangular mesh.

This is not a continuous polyhedral-surface geodesic solver (MMP/Chen-Han).
It restricts paths to mesh edges and therefore generally overestimates the
true surface geodesic.
"""
from __future__ import annotations
from heapq import heappop, heappush
from math import dist, isfinite
from typing import Iterable, Sequence


def _mesh(vertices: Sequence[Sequence[float]], faces: Iterable[Sequence[int]]):
    points = [tuple(float(c) for c in v) for v in vertices]
    if not points or any(len(v) != 3 or any(not isfinite(c) for c in v) for v in points):
        raise ValueError("vertices must be non-empty finite 3D coordinates")
    adjacency = [dict() for _ in points]
    for face in faces:
        if len(face) != 3 or any(not isinstance(i, int) or isinstance(i, bool) for i in face):
            raise ValueError("each face must contain three integer vertex indices")
        a, b, c = face
        if len({a, b, c}) != 3 or min(a, b, c) < 0 or max(a, b, c) >= len(points):
            raise ValueError("face indices must be distinct valid vertex indices")
        for u, v in ((a, b), (b, c), (c, a)):
            w = dist(points[u], points[v])
            if w == 0:
                raise ValueError("mesh edges must have positive length")
            adjacency[u][v] = min(adjacency[u].get(v, float("inf")), w)
            adjacency[v][u] = min(adjacency[v].get(u, float("inf")), w)
    if not any(adjacency):
        raise ValueError("mesh must contain at least one edge")
    return adjacency


def mesh_edge_distances(vertices: Sequence[Sequence[float]],
                        faces: Iterable[Sequence[int]], source: int) -> list[float]:
    """Dijkstra distances from one source vertex along mesh edges."""
    graph = _mesh(vertices, faces)
    if not isinstance(source, int) or isinstance(source, bool) or not 0 <= source < len(graph):
        raise ValueError("source must be a valid vertex index")
    distances = [float("inf")] * len(graph)
    distances[source] = 0.0
    queue = [(0.0, source)]
    while queue:
        current, u = heappop(queue)
        if current != distances[u]:
            continue
        for v, weight in graph[u].items():
            candidate = current + weight
            if candidate < distances[v]:
                distances[v] = candidate
                heappush(queue, (candidate, v))
    return distances


def mesh_edge_shortest_path(vertices: Sequence[Sequence[float]],
                            faces: Iterable[Sequence[int]],
                            source: int, target: int) -> tuple[list[int], float]:
    """Return edge-constrained vertex path and length; unreachable gives ([], inf)."""
    graph = _mesh(vertices, faces)
    n = len(graph)
    if any(not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < n
           for i in (source, target)):
        raise ValueError("source and target must be valid vertex indices")
    distances = [float("inf")] * n
    previous = [-1] * n
    distances[source] = 0.0
    queue = [(0.0, source)]
    while queue:
        current, u = heappop(queue)
        if current != distances[u]:
            continue
        if u == target:
            break
        for v, weight in graph[u].items():
            candidate = current + weight
            if candidate < distances[v]:
                distances[v], previous[v] = candidate, u
                heappush(queue, (candidate, v))
    if distances[target] == float("inf"):
        return [], float("inf")
    path, node = [], target
    while node != -1:
        path.append(node)
        if node == source:
            break
        node = previous[node]
    path.reverse()
    return path, distances[target]

"""Exact reverse k-nearest-neighbour queries using a static 2D k-d tree."""
from __future__ import annotations
from math import isfinite, nextafter, sqrt
from typing import Iterable, Sequence
from kd_tree import KDTree2D

def _point(value: Iterable[float]) -> tuple[float, float]:
    try:
        coords = tuple(float(v) for v in value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("each point must contain two finite coordinates") from exc
    if len(coords) != 2 or not all(isfinite(v) for v in coords):
        raise ValueError("each point must contain two finite coordinates")
    return coords[0], coords[1]

def reverse_k_nearest_neighbors(data_points: Sequence[Sequence[float]],
                                query_points: Sequence[Sequence[float]],
                                k: int = 1) -> list[list[int]]:
    """Return data indices for which each query is among the k nearest.

    Ties are inclusive: q qualifies for p when fewer than k data records are
    strictly closer to p than q. The index is built once. Radius queries
    generate candidates; strict squared-distance comparisons decide inclusion.
    Worst-case work is O(m*n^2) for m queries and n data records.
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    data = [_point(p) for p in data_points]
    queries = [_point(p) for p in query_points]
    if not data or not queries:
        return [[] for _ in queries]
    tree = KDTree2D(data)
    results = []
    for qx, qy in queries:
        matches = []
        for data_index, (x, y) in enumerate(data):
            dx, dy = qx-x, qy-y
            query_d2 = dx*dx + dy*dy
            radius = nextafter(sqrt(query_d2), float("inf"))
            candidates = tree.radius_query((x, y), radius)
            closer = 0
            for j in candidates:
                if j == data_index:
                    continue
                px, py = data[j]
                cx, cy = px-x, py-y
                if cx*cx + cy*cy < query_d2:
                    closer += 1
                    if closer >= k:
                        break
            if closer < k:
                matches.append(data_index)
        results.append(matches)
    return results

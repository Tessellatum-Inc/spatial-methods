"""Exact point k-nearest-neighbour join using the repository's static k-d tree.

The right-hand index is built once and queried for every left-hand point.
Distances are planar Euclidean distances squared, matching KDTree2D's API.
"""
from __future__ import annotations

from collections.abc import Iterable

from kd_tree import KDTree2D


def _point(value: Iterable[float], label: str) -> tuple[float, float]:
    try:
        coords = tuple(float(v) for v in value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{label} must contain two finite coordinates") from exc
    from math import isfinite
    if len(coords) != 2 or not all(isfinite(v) for v in coords):
        raise ValueError(f"{label} must contain two finite coordinates")
    return coords[0], coords[1]


def knn_join(
    left_points: Iterable[Iterable[float]],
    right_points: Iterable[Iterable[float]],
    k: int = 1,
) -> list[tuple[int, int, float]]:
    """Return (left_id, right_id, squared_distance) for each left point's kNN.

    Right-hand ties are resolved by original right input index. Results are
    grouped by left input index, then ordered by (distance squared, right ID).
    If k exceeds the right relation size, all right points are returned.
    Empty relations produce an empty result. Self-matches are not excluded:
    the two relations are independent inputs even if they contain equal points.
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    left = tuple(_point(p, "left point") for p in left_points)
    right = tuple(_point(p, "right point") for p in right_points)
    if not left or not right:
        return []
    index = KDTree2D(right)
    output = []
    for left_id, point in enumerate(left):
        for right_id, distance_sq in index.k_nearest(point, k):
            output.append((left_id, right_id, distance_sq))
    return output

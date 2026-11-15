"""Discrete Hausdorff and Frechet distances for planar point sequences.

The routines operate on finite sequences of points in a common Cartesian
coordinate system. They deliberately implement *discrete* distances: only
the supplied vertices participate; segments are not continuously traversed.
"""
from __future__ import annotations

from collections.abc import Sequence
from math import hypot, isfinite

Point = tuple[float, float]


def _validate_curve(curve: Sequence[Point], name: str) -> list[Point]:
    points: list[Point] = []
    for point in curve:
        if len(point) != 2:
            raise ValueError(f"{name} must contain 2D points")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError(f"{name} coordinates must be finite")
        points.append((x, y))
    if not points:
        raise ValueError(f"{name} must contain at least one point")
    return points


def _distance(a: Point, b: Point) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])


def directed_hausdorff(source: Sequence[Point], target: Sequence[Point]) -> float:
    """Maximum, over source vertices, of distance to the nearest target vertex.

    Time O(m*n), auxiliary space O(1) beyond the normalized inputs.
    """
    a = _validate_curve(source, "source")
    b = _validate_curve(target, "target")
    return max(min(_distance(p, q) for q in b) for p in a)


def hausdorff_distance(a: Sequence[Point], b: Sequence[Point]) -> float:
    """Symmetric discrete Hausdorff distance between two point sets/sequences."""
    return max(directed_hausdorff(a, b), directed_hausdorff(b, a))


def discrete_frechet_distance(a: Sequence[Point], b: Sequence[Point]) -> float:
    """Compute the discrete Frechet distance with O(m*n) time and O(n) space.

    This is the minimum leash length over monotone, endpoint-preserving
    couplings of the two vertex sequences. It is not the continuous Frechet
    distance between the underlying polygonal curves.
    """
    first = _validate_curve(a, "a")
    second = _validate_curve(b, "b")
    previous = [float("inf")] * len(second)
    for i, p in enumerate(first):
        current = [float("inf")] * len(second)
        for j, q in enumerate(second):
            d = _distance(p, q)
            if i == 0 and j == 0:
                current[j] = d
            elif i == 0:
                current[j] = max(current[j - 1], d)
            elif j == 0:
                current[j] = max(previous[j], d)
            else:
                current[j] = max(
                    min(previous[j], previous[j - 1], current[j - 1]), d
                )
        previous = current
    return previous[-1]

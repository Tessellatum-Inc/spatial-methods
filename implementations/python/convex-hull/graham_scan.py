"""Planar convex-hull algorithms for finite two-dimensional point sets.

These teaching implementations use ordinary floating-point orientation
predicates. They are not robust kernels for adversarial near-degenerate data.
"""
from __future__ import annotations

from collections.abc import Sequence
from functools import cmp_to_key
from math import isfinite

Point = tuple[float, float]


def _points(points: Sequence[Point]) -> list[Point]:
    """Normalize, deduplicate and validate a finite point collection."""
    result = sorted({(float(x), float(y)) for x, y in points})
    if any(not isfinite(x) or not isfinite(y) for x, y in result):
        raise ValueError("coordinates must be finite")
    return result


def _cross(origin: Point, a: Point, b: Point) -> float:
    return ((a[0] - origin[0]) * (b[1] - origin[1])
            - (a[1] - origin[1]) * (b[0] - origin[0]))


def _compare_polar(pivot: Point, a: Point, b: Point) -> int:
    """Order vectors counter-clockwise from the positive x direction."""
    cross = _cross(pivot, a, b)
    if cross > 0:
        return -1
    if cross < 0:
        return 1
    da = (a[0] - pivot[0]) ** 2 + (a[1] - pivot[1]) ** 2
    db = (b[0] - pivot[0]) ** 2 + (b[1] - pivot[1]) ** 2
    return (da > db) - (da < db)


def convex_hull(points: Sequence[Point]) -> list[Point]:
    """Return Graham scan's CCW extreme vertices, without a repeated closure."""
    unique = _points(points)
    if len(unique) <= 1:
        return unique

    pivot = min(unique, key=lambda point: (point[1], point[0]))
    candidates = sorted(
        (point for point in unique if point != pivot),
        key=cmp_to_key(lambda a, b: _compare_polar(pivot, a, b)),
    )
    radial: list[Point] = []
    for point in candidates:
        if radial and _cross(pivot, radial[-1], point) == 0:
            radial[-1] = point
        else:
            radial.append(point)

    stack: list[Point] = [pivot]
    for point in radial:
        while len(stack) >= 2 and _cross(stack[-2], stack[-1], point) <= 0:
            stack.pop()
        stack.append(point)
    return stack


def jarvis_march(points: Sequence[Point]) -> list[Point]:
    """Return the CCW hull using gift wrapping (O(nh), h hull vertices).

    Duplicate points are removed, collinear edge points are reduced to the
    farthest endpoint, and the returned ring is not explicitly closed.
    """
    unique = _points(points)
    if len(unique) <= 1:
        return unique
    start = min(unique, key=lambda point: (point[0], point[1]))
    hull: list[Point] = []
    current = start
    while True:
        hull.append(current)
        candidate = unique[0] if unique[0] != current else unique[1]
        for point in unique:
            if point == current or point == candidate:
                continue
            turn = _cross(current, candidate, point)
            if turn < 0:
                candidate = point
            elif turn == 0:
                dc = ((candidate[0] - current[0]) ** 2
                      + (candidate[1] - current[1]) ** 2)
                dp = ((point[0] - current[0]) ** 2
                      + (point[1] - current[1]) ** 2)
                if dp > dc:
                    candidate = point
        current = candidate
        if current == start:
            break
        if len(hull) > len(unique):
            raise RuntimeError("gift wrapping failed to close")
    return hull


def quickhull(points: Sequence[Point]) -> list[Point]:
    """Return the CCW hull using recursive farthest-point partitioning.

    Expected time is O(n log n) on typical distributions; the worst case is
    O(nh), which is O(n²). Collinear boundary points are omitted.
    """
    unique = _points(points)
    if len(unique) <= 1:
        return unique
    left = unique[0]
    right = unique[-1]
    if _cross(left, right, unique[len(unique) // 2]) == 0 and all(
        _cross(left, right, point) == 0 for point in unique
    ):
        return [left, right]

    def chain(a: Point, b: Point, candidates: list[Point]) -> list[Point]:
        if not candidates:
            return []
        pivot = max(candidates, key=lambda p: _cross(a, b, p))
        first = [p for p in candidates if _cross(a, pivot, p) > 0]
        second = [p for p in candidates if _cross(pivot, b, p) > 0]
        return chain(a, pivot, first) + [pivot] + chain(pivot, b, second)

    upper = [p for p in unique if _cross(left, right, p) > 0]
    lower = [p for p in unique if _cross(right, left, p) > 0]
    # Each recursive chain follows its directed baseline. Reverse the lower
    # right-to-left chain and upper left-to-right chain to form a CCW ring.
    return ([left] + list(reversed(chain(right, left, lower))) + [right]
            + list(reversed(chain(left, right, upper))))

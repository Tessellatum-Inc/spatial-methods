"""Visibility polygon for a viewpoint inside a simple polygon.

This dependency-free implementation uses angular ray casting toward every
vertex and two nearby directions. It is an O(n^2 log n) reference method,
not an exact rotational-sweep geometry kernel.
"""
from __future__ import annotations

from collections.abc import Sequence
from math import atan2, cos, hypot, isfinite, pi, sin

Point = tuple[float, float]


def _ring(values: Sequence[Point]) -> list[Point]:
    ring = [(float(x), float(y)) for x, y in values]
    if len(ring) > 1 and ring[0] == ring[-1]:
        ring.pop()
    if len(ring) < 3:
        raise ValueError("polygon must contain at least three distinct vertices")
    if any(not isfinite(x) or not isfinite(y) for x, y in ring):
        raise ValueError("polygon coordinates must be finite")
    if len(set(ring)) < 3:
        raise ValueError("polygon must contain at least three distinct vertices")
    return ring


def _cross(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _inside(point: Point, ring: list[Point]) -> bool:
    """Even-odd containment; boundary points are reported separately."""
    x, y = point
    inside = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        ap = (x - a[0], y - a[1])
        ab = (b[0] - a[0], b[1] - a[1])
        cross = _cross(ab, ap)
        if cross == 0.0 and min(a[0], b[0]) <= x <= max(a[0], b[0]) and min(a[1], b[1]) <= y <= max(a[1], b[1]):
            raise ValueError("viewpoint must lie strictly inside the polygon")
        if (a[1] > y) != (b[1] > y):
            x_cross = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < x_cross:
                inside = not inside
    return inside


def _ray_hit(origin: Point, direction: Point, a: Point, b: Point):
    """Return ray parameter t for origin+t*direction intersecting segment ab."""
    segment = (b[0] - a[0], b[1] - a[1])
    offset = (a[0] - origin[0], a[1] - origin[1])
    denominator = _cross(direction, segment)
    if denominator == 0.0:
        return None
    t = _cross(offset, segment) / denominator
    u = _cross(offset, direction) / denominator
    if t >= 0.0 and 0.0 <= u <= 1.0:
        return t
    return None


def visibility_polygon(
    viewpoint: Point,
    polygon: Sequence[Point],
    *,
    angular_epsilon: float = 1e-9,
) -> list[Point]:
    """Return the visible boundary as an angle-ordered polygonal ring.

    The viewpoint must be strictly inside a simple polygon. For every polygon
    vertex, cast rays at its angle and at angle +/- angular_epsilon; the nearest
    edge intersection is retained. Runtime is O(n^2 log n) due to O(n) rays,
    O(n) edge tests per ray, and angular sorting.

    The small angular perturbation resolves visibility discontinuities at
    vertices. Results use floating-point arithmetic and are not guaranteed
    robust for nearly coincident or extremely scaled geometry.
    """
    ring = _ring(polygon)
    x, y = float(viewpoint[0]), float(viewpoint[1])
    if not isfinite(x) or not isfinite(y):
        raise ValueError("viewpoint coordinates must be finite")
    origin = (x, y)
    if not _inside(origin, ring):
        raise ValueError("viewpoint must lie strictly inside the polygon")
    epsilon = float(angular_epsilon)
    if not isfinite(epsilon) or epsilon <= 0.0 or epsilon >= pi / 4:
        raise ValueError("angular_epsilon must be finite and between 0 and pi/4")

    angles: set[float] = set()
    for vx, vy in ring:
        angle = atan2(vy - y, vx - x)
        angles.add(angle)
        angles.add(angle - epsilon)
        angles.add(angle + epsilon)

    hits: list[tuple[float, Point]] = []
    edges = list(zip(ring, ring[1:] + ring[:1]))
    for angle in sorted(angles):
        direction = (cos(angle), sin(angle))
        nearest = float("inf")
        for a, b in edges:
            t = _ray_hit(origin, direction, a, b)
            if t is not None and t < nearest:
                nearest = t
        if nearest < float("inf"):
            hits.append((angle, (x + nearest * direction[0],
                                 y + nearest * direction[1])))

    result: list[Point] = []
    for _, point in hits:
        if not result or hypot(point[0] - result[-1][0],
                               point[1] - result[-1][1]) > 1e-12:
            result.append(point)
    if len(result) > 1 and hypot(result[0][0] - result[-1][0],
                                 result[0][1] - result[-1][1]) <= 1e-12:
        result.pop()
    return result

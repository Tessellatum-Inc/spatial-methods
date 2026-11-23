"""Dependency-free incremental Bowyer–Watson Delaunay triangulation.

Predicates use exact rational arithmetic over the decimal representation of
input coordinates. This is a deliberately small teaching baseline.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import isfinite
from typing import Iterable, Sequence

Point = tuple[Fraction, Fraction]
Triangle = tuple[Point, Point, Point]


def _point(value: Sequence[float | int]) -> Point:
    if len(value) != 2:
        raise ValueError("each point must contain exactly two coordinates")
    coordinates = []
    for coordinate in value:
        if isinstance(coordinate, bool):
            raise ValueError("boolean coordinates are not supported")
        number = float(coordinate)
        if not isfinite(number):
            raise ValueError("coordinates must be finite")
        coordinates.append(Fraction(str(coordinate)))
    return coordinates[0], coordinates[1]


def orient(a: Point, b: Point, c: Point) -> Fraction:
    """Twice the signed area; positive means counter-clockwise."""
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def _ccw(a: Point, b: Point, c: Point) -> Triangle | None:
    turn = orient(a, b, c)
    if turn == 0:
        return None
    return (a, b, c) if turn > 0 else (a, c, b)


def incircle(a: Point, b: Point, c: Point, p: Point) -> Fraction:
    """Return the exact translated in-circle determinant.

    For counter-clockwise a,b,c, positive means p is strictly inside the
    circumcircle, zero means cocircular, and negative means outside.
    """
    ax, ay = a[0] - p[0], a[1] - p[1]
    bx, by = b[0] - p[0], b[1] - p[1]
    cx, cy = c[0] - p[0], c[1] - p[1]
    return (
        (ax * ax + ay * ay) * (bx * cy - by * cx)
        - (bx * bx + by * by) * (ax * cy - ay * cx)
        + (cx * cx + cy * cy) * (ax * by - ay * bx)
    )


def _edge(a: Point, b: Point) -> tuple[Point, Point]:
    return (a, b) if a < b else (b, a)


def delaunay_triangulate(
    points: Iterable[Sequence[float | int]],
) -> list[Triangle]:
    """Return a planar Delaunay triangulation using incremental cavity removal.

    Duplicate coordinates and collinear point sets are rejected. Points are
    inserted in caller order. Cocircular ties are resolved conservatively:
    triangles whose circumcircles contain the new point strictly are removed;
    zero-determinant ties are retained.
    """
    sites = [_point(point) for point in points]
    if len(sites) < 3:
        raise ValueError("at least three points are required")
    if len(set(sites)) != len(sites):
        raise ValueError("duplicate point coordinates are not supported")

    min_x = min(p[0] for p in sites)
    max_x = max(p[0] for p in sites)
    min_y = min(p[1] for p in sites)
    max_y = max(p[1] for p in sites)
    span = max(max_x - min_x, max_y - min_y)
    if span == 0:
        raise ValueError("all points are coincident")
    if all(orient(sites[0], sites[1], point) == 0 for point in sites[2:]):
        raise ValueError("a two-dimensional triangulation requires non-collinear points")

    centre_x = (min_x + max_x) / 2
    centre_y = (min_y + max_y) / 2
    # A wide enclosing triangle keeps the finite triangulation away from
    # super-triangle circumcircle artefacts for ordinary, non-degenerate clouds.
    # A finite multiplier cannot bound arbitrarily near-collinear inputs; the
    # Euler and empty-circle tests define the verified teaching envelope.
    super_points: tuple[Point, Point, Point] = (
        (centre_x - 128 * span, centre_y - 64 * span),
        (centre_x + 128 * span, centre_y - 64 * span),
        (centre_x, centre_y + 128 * span),
    )
    super_set = set(super_points)
    initial = _ccw(*super_points)
    assert initial is not None
    triangles: list[Triangle] = [initial]

    for point in sites:
        bad = [
            triangle for triangle in triangles
            if incircle(*triangle, point) > 0
        ]
        if not bad:
            raise RuntimeError(
                "no circumcircle cavity found; input may be numerically or "
                "geometrically degenerate for this teaching implementation"
            )

        edge_counts: Counter[tuple[Point, Point]] = Counter()
        edge_orientation: dict[tuple[Point, Point], tuple[Point, Point]] = {}
        for triangle in bad:
            for a, b in (
                (triangle[0], triangle[1]),
                (triangle[1], triangle[2]),
                (triangle[2], triangle[0]),
            ):
                key = _edge(a, b)
                edge_counts[key] += 1
                edge_orientation.setdefault(key, (a, b))

        bad_ids = {id(triangle) for triangle in bad}
        triangles = [triangle for triangle in triangles if id(triangle) not in bad_ids]

        for key, count in edge_counts.items():
            if count != 1:
                continue
            a, b = edge_orientation[key]
            replacement = _ccw(a, b, point)
            if replacement is not None:
                triangles.append(replacement)

    finite = [
        triangle for triangle in triangles
        if not any(vertex in super_set for vertex in triangle)
    ]
    # A deterministic presentation order; topology is not canonical for
    # cocircular input, but the output is stable for a fixed insertion order.
    finite.sort(key=lambda tri: tuple(sorted(tri)))
    if not finite:
        raise RuntimeError("triangulation produced no finite faces")
    return finite

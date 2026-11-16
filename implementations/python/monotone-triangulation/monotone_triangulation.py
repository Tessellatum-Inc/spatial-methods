"""Stack-based triangulation of strictly y-monotone simple polygons.

This first version deliberately requires distinct vertex y-coordinates.  It uses
exact rational predicates and emits CCW triangles.  It is not a general polygon
partitioner and does not accept holes.
"""
from __future__ import annotations

from fractions import Fraction
from math import isfinite
from typing import Iterable, Sequence

Point = tuple[Fraction, Fraction]
Triangle = tuple[Point, Point, Point]


def _point(value: Sequence[float | int]) -> Point:
    if len(value) != 2:
        raise ValueError("Each vertex must contain exactly x and y.")
    result = []
    for coordinate in value:
        if isinstance(coordinate, float) and not isfinite(coordinate):
            raise ValueError("Coordinates must be finite.")
        result.append(Fraction(str(coordinate)))
    return result[0], result[1]


def orient(a: Point, b: Point, c: Point) -> Fraction:
    return ((b[0] - a[0]) * (c[1] - a[1]) -
            (b[1] - a[1]) * (c[0] - a[0]))


def _area2(ring: Sequence[Point]) -> Fraction:
    return sum((ring[i][0] * ring[(i + 1) % len(ring)][1] -
                ring[(i + 1) % len(ring)][0] * ring[i][1])
               for i in range(len(ring)))


def _on_segment(a: Point, b: Point, p: Point) -> bool:
    return (orient(a, b, p) == 0 and
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _intersects(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if ((o1 > 0 > o2 or o2 > 0 > o1) and
            (o3 > 0 > o4 or o4 > 0 > o3)):
        return True
    return ((o1 == 0 and _on_segment(a, b, c)) or
            (o2 == 0 and _on_segment(a, b, d)) or
            (o3 == 0 and _on_segment(c, d, a)) or
            (o4 == 0 and _on_segment(c, d, b)))


def _clean(vertices: Iterable[Sequence[float | int]]) -> list[Point]:
    ring = [_point(v) for v in vertices]
    if len(ring) > 1 and ring[0] == ring[-1]:
        ring.pop()
    compact = []
    for p in ring:
        if not compact or compact[-1] != p:
            compact.append(p)
    if len(compact) > 1 and compact[0] == compact[-1]:
        compact.pop()
    if len(compact) < 3 or len(set(compact)) != len(compact):
        raise ValueError("A simple polygon needs at least three distinct vertices.")
    if _area2(compact) == 0:
        raise ValueError("Polygon area must be non-zero.")
    n = len(compact)
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if _intersects(compact[i], compact[(i + 1) % n],
                           compact[j], compact[(j + 1) % n]):
                raise ValueError("Input ring is not a simple polygon.")
    if _area2(compact) < 0:
        compact.reverse()
    return compact


def _monotone_chains(ring: Sequence[Point]) -> tuple[set[int], set[int], int, int]:
    ys = [p[1] for p in ring]
    if len(set(ys)) != len(ys):
        raise ValueError("This implementation requires distinct vertex y-coordinates.")
    top = max(range(len(ring)), key=lambda i: ring[i][1])
    bottom = min(range(len(ring)), key=lambda i: ring[i][1])
    n = len(ring)

    forward = []
    i = top
    while True:
        forward.append(i)
        if i == bottom:
            break
        i = (i + 1) % n
    backward = []
    i = top
    while True:
        backward.append(i)
        if i == bottom:
            break
        i = (i - 1) % n

    for chain in (forward, backward):
        if any(ring[chain[k]][1] <= ring[chain[k + 1]][1]
               for k in range(len(chain) - 1)):
            raise ValueError("Polygon is not y-monotone.")
    # For a CCW ring, the forward top-to-bottom chain is the left boundary.
    return set(forward), set(backward), top, bottom


def _ccw(a: Point, b: Point, c: Point) -> Triangle | None:
    turn = orient(a, b, c)
    if turn == 0:
        return None
    return (a, b, c) if turn > 0 else (a, c, b)


def triangulate(vertices: Iterable[Sequence[float | int]]) -> list[Triangle]:
    """Triangulate a strictly y-monotone simple polygon in O(n log n).

    Distinct y-coordinates avoid ambiguous horizontal event ordering.  Input
    may be clockwise or counter-clockwise; output triangles are always CCW.
    """
    ring = _clean(vertices)
    left, right, top, bottom = _monotone_chains(ring)
    order = sorted(range(len(ring)), key=lambda i: (-ring[i][1], ring[i][0]))
    chain = {i: ("left" if i in left else "right") for i in range(len(ring))}
    chain[top] = chain[bottom] = "both"

    stack = [order[0], order[1]]
    triangles: list[Triangle] = []
    for position in range(2, len(order) - 1):
        current = order[position]
        if chain[current] != chain[stack[-1]] and chain[current] != "both" and chain[stack[-1]] != "both":
            while len(stack) > 1:
                a, b = stack.pop(), stack[-1]
                tri = _ccw(ring[current], ring[a], ring[b])
                if tri:
                    triangles.append(tri)
            stack = [order[position - 1], current]
        else:
            last = stack.pop()
            while stack:
                candidate = _ccw(ring[current], ring[last], ring[stack[-1]])
                if candidate is None:
                    last = stack.pop()
                    continue
                turn = orient(ring[current], ring[last], ring[stack[-1]])
                # A diagonal lies inside when the turn faces the polygon interior.
                inside = (turn < 0 if chain[current] == "left" else turn > 0)
                if not inside:
                    break
                triangles.append(candidate)
                last = stack.pop()
            stack.extend((last, current))

    final = order[-1]
    stack.pop()
    while len(stack) > 1:
        a, b = stack.pop(), stack[-1]
        tri = _ccw(ring[final], ring[a], ring[b])
        if tri:
            triangles.append(tri)

    if len(triangles) != len(ring) - 2:
        raise RuntimeError("Triangulation did not produce exactly n-2 triangles.")
    if sum((abs(orient(*t)) for t in triangles), Fraction(0)) != abs(_area2(ring)):
        raise RuntimeError("Triangulation failed exact area conservation.")
    return triangles


def triangle_area(triangle: Triangle) -> Fraction:
    return abs(orient(*triangle)) / 2


def polygon_area(vertices: Iterable[Sequence[float | int]]) -> Fraction:
    return abs(_area2(_clean(vertices))) / 2

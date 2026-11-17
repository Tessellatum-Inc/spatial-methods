"""Dependency-free incremental 2D Delaunay triangulation (Bowyer–Watson)."""
from __future__ import annotations

from collections import Counter
from math import isfinite
from typing import Iterable, Sequence

Point = tuple[float, float]
Triangle = tuple[int, int, int]


def _orient(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _ccw(tri: Triangle, pts: Sequence[Point]) -> Triangle:
    a, b, c = tri
    return tri if _orient(pts[a], pts[b], pts[c]) > 0 else (a, c, b)


def _incircle(a: Point, b: Point, c: Point, p: Point) -> float:
    """Positive iff p is inside circumcircle abc when abc is counter-clockwise."""
    ax, ay = a[0] - p[0], a[1] - p[1]
    bx, by = b[0] - p[0], b[1] - p[1]
    cx, cy = c[0] - p[0], c[1] - p[1]
    return ((ax*ax + ay*ay) * (bx*cy - by*cx)
            - (bx*bx + by*by) * (ax*cy - ay*cx)
            + (cx*cx + cy*cy) * (ax*by - ay*bx))


def triangulate(points: Iterable[Sequence[float]]) -> tuple[Triangle, ...]:
    """Triangulate unique, non-collinear planar sites.

    Returns CCW triangles indexing the input order. This transparent teaching
    implementation uses a super-triangle and scans every current triangle for
    each insertion, giving O(n^2) time and O(n) working storage for ordinary
    planar inputs. Predicates use float arithmetic and a scale-relative
    tolerance, so nearly degenerate inputs may remain numerically ambiguous.
    Cocircular choices are resolved deterministically by the insertion order.
    """
    raw = list(points)
    if len(raw) < 3:
        raise ValueError("at least three points are required")
    pts: list[Point] = []
    for item in raw:
        if len(item) != 2:
            raise ValueError("each point must have exactly two coordinates")
        x, y = float(item[0]), float(item[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError("coordinates must be finite")
        pts.append((x, y))
    if len(set(pts)) != len(pts):
        raise ValueError("duplicate points are not allowed")
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    span = max(maxx-minx, maxy-miny)
    if span == 0 or not any(abs(_orient(pts[0], pts[1], p)) > 0 for p in pts[2:]):
        raise ValueError("points must span a non-collinear 2D area")
    cx, cy = (minx+maxx)/2, (miny+maxy)/2
    super_ids = (len(pts), len(pts)+1, len(pts)+2)
    work = pts + [(cx-32*span, cy-16*span),
                  (cx+32*span, cy-16*span), (cx, cy+32*span)]
    triangles: list[Triangle] = [_ccw(super_ids, work)]
    for idx, point in enumerate(pts):
        bad = []
        for tri in triangles:
            a, b, c = (work[k] for k in tri)
            det = _incircle(a, b, c, point)
            # Incircle determinant has coordinate-units^4. Scale from
            # point-relative differences, not absolute world coordinates:
            # translating a dataset must not change the tolerance.
            local_scale = max(abs(a[0]-point[0]), abs(a[1]-point[1]),
                              abs(b[0]-point[0]), abs(b[1]-point[1]),
                              abs(c[0]-point[0]), abs(c[1]-point[1]))
            tolerance = 1e-14 * local_scale**4
            if det >= -tolerance:
                bad.append(tri)
        if not bad:
            raise ArithmeticError("point insertion found no circumcircle cavity")
        counts: Counter[tuple[int, int]] = Counter()
        directed: dict[tuple[int, int], tuple[int, int]] = {}
        for tri in bad:
            for u, v in ((tri[0],tri[1]), (tri[1],tri[2]), (tri[2],tri[0])):
                key = (min(u,v), max(u,v))
                counts[key] += 1
                directed[key] = (u,v)
        boundary = [directed[e] for e,n in counts.items() if n == 1]
        bad_set = set(bad)
        triangles = [t for t in triangles if t not in bad_set]
        for u, v in boundary:
            if abs(_orient(work[u], work[v], point)) > 1e-14 * span**2:
                triangles.append(_ccw((u,v,idx), work))
    result = []
    for tri in triangles:
        if all(v < len(pts) for v in tri):
            result.append(_ccw(tri, work))
    return tuple(sorted(result))


def edges(triangles: Iterable[Triangle]) -> tuple[tuple[int, int], ...]:
    """Return unique undirected edges in lexicographic order."""
    found = {tuple(sorted(edge)) for t in triangles
             for edge in ((t[0],t[1]),(t[1],t[2]),(t[2],t[0]))}
    return tuple(sorted(found))

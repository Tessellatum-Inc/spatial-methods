"""Teaching implementations of point-set and polyline geometric metrics."""
from __future__ import annotations
from math import hypot, isfinite
from random import Random
from typing import Iterable, Sequence

Point = tuple[float, float]

def _points(values: Iterable[Sequence[float]], *, minimum: int = 0) -> list[Point]:
    result = []
    for p in values:
        if len(p) != 2:
            raise ValueError("each point must contain exactly two coordinates")
        x, y = float(p[0]), float(p[1])
        if not (isfinite(x) and isfinite(y)):
            raise ValueError("coordinates must be finite")
        result.append((x, y))
    if len(result) < minimum:
        raise ValueError(f"at least {minimum} point(s) are required")
    return result

def _distance(a: Point, b: Point) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])

def directed_hausdorff_distance(a, b) -> float:
    """Maximum, over points in A, of distance to the nearest point in B."""
    aa, bb = _points(a, minimum=1), _points(b, minimum=1)
    return max(min(_distance(p, q) for q in bb) for p in aa)

def hausdorff_distance(a, b) -> float:
    """Symmetric Hausdorff distance between two finite point sets."""
    return max(directed_hausdorff_distance(a, b), directed_hausdorff_distance(b, a))

def discrete_frechet_distance(curve_a, curve_b) -> float:
    """Discrete Fréchet distance between ordered vertex sequences."""
    a, b = _points(curve_a, minimum=1), _points(curve_b, minimum=1)
    previous = [float("inf")] * len(b)
    for i, pa in enumerate(a):
        current = [float("inf")] * len(b)
        for j, pb in enumerate(b):
            d = _distance(pa, pb)
            if i == 0 and j == 0:
                current[j] = d
            elif i == 0:
                current[j] = max(current[j - 1], d)
            elif j == 0:
                current[j] = max(previous[j], d)
            else:
                current[j] = max(min(previous[j], previous[j - 1], current[j - 1]), d)
        previous = current
    return previous[-1]

def _circle_two(a: Point, b: Point):
    cx, cy = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    return (cx, cy, _distance(a, b) / 2.0)

def _circle_three(a: Point, b: Point, c: Point):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    scale = max(1.0, abs(ax), abs(ay), abs(bx), abs(by), abs(cx), abs(cy))
    if abs(d) <= 1e-14 * scale * scale:
        pairs = [(a, b), (a, c), (b, c)]
        return max((_circle_two(p, q) for p, q in pairs), key=lambda circle: circle[2])
    aa, bb, cc = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    ux = (aa * (by - cy) + bb * (cy - ay) + cc * (ay - by)) / d
    uy = (aa * (cx - bx) + bb * (ax - cx) + cc * (bx - ax)) / d
    return (ux, uy, hypot(ux - ax, uy - ay))

def smallest_enclosing_circle(points, *, seed: int = 0):
    """Return (center_x, center_y, radius) using randomized Welzl recursion."""
    pts = _points(points)
    if not pts:
        return None
    Random(seed).shuffle(pts)
    def contains(circle, p):
        if circle is None:
            return False
        x, y, r = circle
        return _distance((x, y), p) <= r + 1e-10 * max(1.0, r)
    def welzl(n, boundary):
        if n == 0 or len(boundary) == 3:
            if not boundary:
                return None
            if len(boundary) == 1:
                return (boundary[0][0], boundary[0][1], 0.0)
            if len(boundary) == 2:
                return _circle_two(*boundary)
            return _circle_three(*boundary)
        p = pts[n - 1]
        circle = welzl(n - 1, boundary)
        if contains(circle, p):
            return circle
        return welzl(n - 1, boundary + [p])
    return welzl(len(pts), [])


def convex_hull(points):
    """Return the strict counter-clockwise monotone-chain hull."""
    pts = sorted(set(_points(points)))
    if len(pts) <= 1:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def convex_polygon_diameter(points):
    """Return (endpoint_a, endpoint_b, distance) using rotating calipers.

    The convex hull is built internally. Total time is O(n log n) for hull
    construction plus O(h) for the antipodal-pair sweep.
    """
    hull = convex_hull(points)
    n = len(hull)
    if n == 0:
        return None
    if n == 1:
        return (hull[0], hull[0], 0.0)
    if n == 2:
        return (hull[0], hull[1], _distance(hull[0], hull[1]))
    def area(i, j):
        a, b, c = hull[i], hull[(i+1) % n], hull[j]
        return abs((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
    best = (hull[0], hull[1], _distance(hull[0], hull[1]))
    j = 1
    for i in range(n):
        ni = (i+1) % n
        while area(i, (j+1) % n) > area(i, j) + 1e-14:
            j = (j+1) % n
        for a, b in ((hull[i], hull[j]), (hull[ni], hull[j])):
            d = _distance(a, b)
            if d > best[2]:
                best = (a, b, d)
        nj = (j+1) % n
        if abs(area(i, nj)-area(i, j)) <= 1e-14:
            for a, b in ((hull[i], hull[nj]), (hull[ni], hull[nj])):
                d = _distance(a, b)
                if d > best[2]:
                    best = (a, b, d)
    return best

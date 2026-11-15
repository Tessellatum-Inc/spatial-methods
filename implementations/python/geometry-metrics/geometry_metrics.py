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


def _ring(values):
    ring = _points(values, minimum=3)
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    if len(set(ring[:-1])) < 3:
        raise ValueError("each polygon ring must contain at least three unique vertices")
    return ring


def _point_in_ring(point, ring):
    x, y = point
    inside = False
    for a, b in zip(ring, ring[1:]):
        if (a[1] > y) != (b[1] > y):
            x_cross = a[0] + (y-a[1]) * (b[0]-a[0]) / (b[1]-a[1])
            if x < x_cross:
                inside = not inside
    return inside


def _point_segment_distance(point, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    denom = dx*dx + dy*dy
    if denom == 0:
        return _distance(point, a)
    t = max(0.0, min(1.0, ((point[0]-a[0])*dx + (point[1]-a[1])*dy) / denom))
    return hypot(point[0]-a[0]-t*dx, point[1]-a[1]-t*dy)


def polylabel(outer_ring, holes=(), *, precision=1.0, max_cells=1_000_000):
    """Approximate a polygon's pole of inaccessibility.

    Returns (x, y, radius, cells_examined). The radius is the distance to the
    nearest polygon boundary. Outer and hole rings must form a valid polygon.
    Precision is an absolute planar distance tolerance.
    """
    from heapq import heappop, heappush
    from math import sqrt
    outer = _ring(outer_ring)
    hole_rings = [_ring(r) for r in holes]
    if not isfinite(precision) or precision <= 0:
        raise ValueError("precision must be finite and positive")
    if not isinstance(max_cells, int) or isinstance(max_cells, bool) or max_cells < 1:
        raise ValueError("max_cells must be a positive integer")
    all_rings = [outer] + hole_rings
    min_x = min(p[0] for p in outer[:-1])
    min_y = min(p[1] for p in outer[:-1])
    max_x = max(p[0] for p in outer[:-1])
    max_y = max(p[1] for p in outer[:-1])
    width, height = max_x-min_x, max_y-min_y
    if width == 0 or height == 0:
        raise ValueError("polygon exterior must have positive area")

    def signed_distance(point):
        inside = _point_in_ring(point, outer) and not any(_point_in_ring(point, h) for h in hole_rings)
        distance = min(_point_segment_distance(point, a, b)
                       for ring in all_rings for a, b in zip(ring, ring[1:]))
        return distance if inside else -distance

    def make_cell(x, y, half):
        d = signed_distance((x, y))
        return (d + half*sqrt(2.0), x, y, half, d)

    cell_size = min(width, height)
    half = cell_size / 2.0
    heap = []
    x = min_x
    while x < max_x:
        y = min_y
        while y < max_y:
            cell = make_cell(x+half, y+half, half)
            heappush(heap, (-cell[0], cell[1], cell[2], cell[3], cell[4]))
            y += cell_size
        x += cell_size

    best = make_cell((min_x+max_x)/2.0, (min_y+max_y)/2.0, 0.0)
    cells_examined = 0
    while heap:
        neg_max, cx, cy, half, d = heappop(heap)
        upper_bound = -neg_max
        cells_examined += 1
        if cells_examined > max_cells:
            raise RuntimeError("polylabel exceeded max_cells; relax precision or raise the limit")
        if d > best[4]:
            best = (upper_bound, cx, cy, half, d)
        if upper_bound-best[4] <= precision:
            continue
        quarter = half/2.0
        for dx in (-quarter, quarter):
            for dy in (-quarter, quarter):
                child = make_cell(cx+dx, cy+dy, quarter)
                heappush(heap, (-child[0], child[1], child[2], child[3], child[4]))
    return (best[1], best[2], max(0.0, best[4]), cells_examined)

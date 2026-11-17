"""Polygon compactness metrics for districting and territory design."""
import math


def _points(ring):
    try:
        pts = [(float(point[0]), float(point[1])) for point in ring]
    except (TypeError, ValueError, IndexError):
        raise ValueError("ring must be a sequence of finite 2D coordinates")
    if any(not math.isfinite(x) or not math.isfinite(y) for x, y in pts):
        raise ValueError("ring coordinates must be finite")
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts.pop()
    if len(set(pts)) < 3:
        raise ValueError("ring must contain at least three distinct vertices")
    return pts


def _distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _diameter_circle(a, b):
    center = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    return center, _distance(a, b) / 2.0


def _contains(circle, point):
    if circle is None:
        return False
    center, radius = circle
    return _distance(center, point) <= radius + 1e-10 * max(1.0, radius)


def _three_point_circle(a, b, c):
    pair_candidates = [
        _diameter_circle(a, b),
        _diameter_circle(a, c),
        _diameter_circle(b, c),
    ]
    enclosing = [circle for circle in pair_candidates
                 if all(_contains(circle, p) for p in (a, b, c))]
    if enclosing:
        return min(enclosing, key=lambda circle: circle[1])
    ax, ay = a
    bx, by = b
    cx, cy = c
    determinant = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(determinant) <= 1e-14:
        return max(pair_candidates, key=lambda circle: circle[1])
    aa, bb, cc = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    ux = (aa * (by - cy) + bb * (cy - ay) + cc * (ay - by)) / determinant
    uy = (aa * (cx - bx) + bb * (ax - cx) + cc * (bx - ax)) / determinant
    center = (ux, uy)
    return center, _distance(center, a)


def minimum_enclosing_circle(points):
    """Deterministic incremental minimum enclosing circle for 2D points."""
    pts = sorted(set((float(x), float(y)) for x, y in points))
    if not pts:
        raise ValueError("at least one point is required")
    circle = None
    for i, point in enumerate(pts):
        if not _contains(circle, point):
            circle = (point, 0.0)
            for j in range(i):
                other = pts[j]
                if not _contains(circle, other):
                    circle = _diameter_circle(point, other)
                    for k in range(j):
                        third = pts[k]
                        if not _contains(circle, third):
                            circle = _three_point_circle(point, other, third)
    return {"center": circle[0], "radius": circle[1]}


def polygon_compactness(ring):
    """Return Polsby-Popper, Reock and Schwartzberg scores for a simple ring.

    Coordinates are planar and must use a suitable projected CRS. Holes are
    not represented; the input is one simple exterior boundary ring.
    """
    pts = _points(ring)
    twice_area = sum(
        pts[i][0] * pts[(i + 1) % len(pts)][1]
        - pts[(i + 1) % len(pts)][0] * pts[i][1]
        for i in range(len(pts))
    )
    area = abs(twice_area) / 2.0
    perimeter = sum(_distance(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))
    if area <= 0 or perimeter <= 0:
        raise ValueError("ring must enclose positive area")
    circle = minimum_enclosing_circle(pts)
    if circle["radius"] <= 0:
        raise ValueError("minimum enclosing circle must have positive radius")
    polsby_popper = 4.0 * math.pi * area / (perimeter * perimeter)
    reock = area / (math.pi * circle["radius"] ** 2)
    schwartzberg = perimeter / (2.0 * math.sqrt(math.pi * area))
    return {
        "area": area,
        "perimeter": perimeter,
        "polsby_popper": min(1.0, max(0.0, polsby_popper)),
        "reock": min(1.0, max(0.0, reock)),
        "schwartzberg_ratio": schwartzberg,
        "minimum_enclosing_circle": circle,
    }

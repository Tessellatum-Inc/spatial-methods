"""Educational ray-crossing point-in-ring test.

Boundary is reported separately. This is for one simple planar ring and uses
exact floating-point comparisons; it is not a robust geometry engine.
"""

from enum import Enum
from math import isfinite
from typing import Sequence

Coordinate = tuple[float, float]


class PointLocation(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"
    BOUNDARY = "boundary"


def _on_segment(point: Coordinate, start: Coordinate, end: Coordinate) -> bool:
    px, py = point
    ax, ay = start
    bx, by = end
    cross = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
    if cross != 0:
        return False
    return (
        min(ax, bx) <= px <= max(ax, bx)
        and min(ay, by) <= py <= max(ay, by)
    )


def locate_point(point: Coordinate, ring: Sequence[Coordinate]) -> PointLocation:
    """Classify a point relative to a closed or implicitly closed simple ring.

    The ring must contain at least three distinct vertices. The first vertex
    may, but need not, be repeated at the end.
    """
    vertices = list(ring)
    if len(vertices) > 1 and vertices[0] == vertices[-1]:
        vertices.pop()
    if len(vertices) < 3 or len(set(vertices)) < 3:
        raise ValueError("A ring must contain at least three distinct vertices.")

    x, y = point
    inside = False
    previous = vertices[-1]

    for current in vertices:
        if _on_segment(point, previous, current):
            return PointLocation.BOUNDARY

        x1, y1 = previous
        x2, y2 = current
        # Half-open vertical interval prevents counting a shared vertex twice.
        crosses_scanline = (y1 > y) != (y2 > y)
        if crosses_scanline:
            crossing_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < crossing_x:
                inside = not inside
        previous = current

    return PointLocation.INSIDE if inside else PointLocation.OUTSIDE


if __name__ == "__main__":
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    for candidate in [(2, 2), (5, 2), (4, 2)]:
        print(candidate, locate_point(candidate, square).value)


def winding_number(point: Coordinate, ring: Sequence[Coordinate]) -> int:
    """Return the signed winding number of a query point around one ring.

    Boundary points are not assigned a winding number by this function;
    callers should use :func:`locate_point_winding` for the three-way result.
    Positive and negative values distinguish ring orientation. A non-zero
    value denotes the interior under the nonzero winding fill rule.
    """
    vertices = list(ring)
    if len(vertices) > 1 and vertices[0] == vertices[-1]:
        vertices.pop()
    if len(vertices) < 3 or len(set(vertices)) < 3:
        raise ValueError("A ring must contain at least three distinct vertices.")
    px, py = float(point[0]), float(point[1])
    if not (isfinite(px) and isfinite(py)):
        raise ValueError("point coordinates must be finite")
    normalized = []
    for vertex in vertices:
        if len(vertex) != 2:
            raise ValueError("each ring vertex must contain x and y")
        x, y = float(vertex[0]), float(vertex[1])
        if not (isfinite(x) and isfinite(y)):
            raise ValueError("ring coordinates must be finite")
        normalized.append((x, y))
    p = (px, py)
    count = 0
    for a, b in zip(normalized, normalized[1:] + normalized[:1]):
        if _on_segment(p, a, b):
            raise ValueError("point lies on the ring boundary; use locate_point_winding")
        side = (b[0] - a[0]) * (py - a[1]) - (px - a[0]) * (b[1] - a[1])
        if a[1] <= py:
            if b[1] > py and side > 0:
                count += 1
        elif b[1] <= py and side < 0:
            count -= 1
    return count


def locate_point_winding(point: Coordinate, ring: Sequence[Coordinate]) -> PointLocation:
    """Classify a point using the nonzero winding-number fill rule.

    The boundary is returned separately. Unlike even-odd parity, the
    nonzero rule is sensitive to the signed number of turns around a point;
    this distinction matters for self-intersecting paths and compound rings.
    """
    vertices = list(ring)
    if len(vertices) > 1 and vertices[0] == vertices[-1]:
        vertices.pop()
    if len(vertices) < 3 or len(set(vertices)) < 3:
        raise ValueError("A ring must contain at least three distinct vertices.")
    p = (float(point[0]), float(point[1]))
    if not all(isfinite(v) for v in p):
        raise ValueError("point coordinates must be finite")
    normalized = []
    for vertex in vertices:
        if len(vertex) != 2:
            raise ValueError("each ring vertex must contain x and y")
        q = (float(vertex[0]), float(vertex[1]))
        if not all(isfinite(v) for v in q):
            raise ValueError("ring coordinates must be finite")
        normalized.append(q)
    for a, b in zip(normalized, normalized[1:] + normalized[:1]):
        if _on_segment(p, a, b):
            return PointLocation.BOUNDARY
    count = 0
    for a, b in zip(normalized, normalized[1:] + normalized[:1]):
        side = (b[0] - a[0]) * (p[1] - a[1]) - (p[0] - a[0]) * (b[1] - a[1])
        if a[1] <= p[1]:
            if b[1] > p[1] and side > 0:
                count += 1
        elif b[1] <= p[1] and side < 0:
            count -= 1
    return PointLocation.INSIDE if count != 0 else PointLocation.OUTSIDE


# Exact-rational variants ----------------------------------------------------

from fractions import Fraction

ExactCoordinate = tuple[Fraction, Fraction]


def _exact_number(value: object) -> Fraction:
    """Convert a finite numeric coordinate to its exact decimal rational."""
    if isinstance(value, bool):
        raise ValueError("boolean coordinates are not supported")
    try:
        numeric = float(value)
        if not isfinite(numeric):
            raise ValueError("coordinates must be finite")
        return Fraction(str(value))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("coordinates must be finite numeric values") from exc


def _exact_point(value: Sequence[object]) -> ExactCoordinate:
    if len(value) != 2:
        raise ValueError("each point must contain exactly two coordinates")
    return _exact_number(value[0]), _exact_number(value[1])


def _exact_ring(ring: Sequence[Sequence[object]]) -> list[ExactCoordinate]:
    vertices = [_exact_point(vertex) for vertex in ring]
    if len(vertices) > 1 and vertices[0] == vertices[-1]:
        vertices.pop()
    if len(vertices) < 3 or len(set(vertices)) < 3:
        raise ValueError("A ring must contain at least three distinct vertices.")
    return vertices


def _exact_orientation(a: ExactCoordinate, b: ExactCoordinate,
                       p: ExactCoordinate) -> Fraction:
    """Exact signed cross product; positive is left of directed edge a→b."""
    return ((b[0] - a[0]) * (p[1] - a[1])
            - (b[1] - a[1]) * (p[0] - a[0]))


def _exact_on_segment(p: ExactCoordinate, a: ExactCoordinate,
                      b: ExactCoordinate) -> bool:
    return (
        _exact_orientation(a, b, p) == 0
        and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )


def locate_point_exact(point: Sequence[object],
                       ring: Sequence[Sequence[object]]) -> PointLocation:
    """Exact-rational even–odd ray crossing for one simple planar ring.

    Finite input coordinates are converted from their string representation
    to Fraction. Boundary is tested first; half-open vertical intervals and
    orientation signs avoid division and ambiguous vertex double-counting.
    """
    p = _exact_point(point)
    vertices = _exact_ring(ring)
    inside = False
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        if _exact_on_segment(p, a, b):
            return PointLocation.BOUNDARY
        side = _exact_orientation(a, b, p)
        if a[1] <= p[1] < b[1] and side > 0:
            inside = not inside
        elif b[1] <= p[1] < a[1] and side < 0:
            inside = not inside
    return PointLocation.INSIDE if inside else PointLocation.OUTSIDE


def winding_number_exact(point: Sequence[object],
                         ring: Sequence[Sequence[object]]) -> int:
    """Exact signed winding number; raises when the query is on the boundary."""
    p = _exact_point(point)
    vertices = _exact_ring(ring)
    count = 0
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        if _exact_on_segment(p, a, b):
            raise ValueError("point lies on the ring boundary; use locate_point_winding_exact")
        side = _exact_orientation(a, b, p)
        if a[1] <= p[1] < b[1] and side > 0:
            count += 1
        elif b[1] <= p[1] < a[1] and side < 0:
            count -= 1
    return count


def locate_point_winding_exact(point: Sequence[object],
                               ring: Sequence[Sequence[object]]) -> PointLocation:
    """Exact-rational three-way classifier using the nonzero winding rule."""
    p = _exact_point(point)
    vertices = _exact_ring(ring)
    count = 0
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        if _exact_on_segment(p, a, b):
            return PointLocation.BOUNDARY
        side = _exact_orientation(a, b, p)
        if a[1] <= p[1] < b[1] and side > 0:
            count += 1
        elif b[1] <= p[1] < a[1] and side < 0:
            count -= 1
    return PointLocation.INSIDE if count != 0 else PointLocation.OUTSIDE

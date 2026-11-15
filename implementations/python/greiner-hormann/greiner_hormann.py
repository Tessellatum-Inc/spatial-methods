"""Greiner–Hormann intersection for simple, non-degenerate polygons.

This teaching implementation supports one simple ring per input, proper
(transverse) boundary crossings, and area intersections. It intentionally
rejects touching/collinear boundary events and does not model holes.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite
from collections.abc import Sequence

Point = tuple[float, float]


@dataclass
class _Node:
    point: Point
    intersection: bool = False
    entry: bool = False
    visited: bool = False
    alpha: float = 0.0
    next: "_Node | None" = None
    prev: "_Node | None" = None
    neighbor: "_Node | None" = None


def _cross(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _area(ring: Sequence[Point]) -> float:
    return 0.5 * sum(ring[i][0] * ring[(i + 1) % len(ring)][1]
                     - ring[(i + 1) % len(ring)][0] * ring[i][1]
                     for i in range(len(ring)))


def _prepare(points: Sequence[Point], name: str, eps: float) -> list[Point]:
    ring = []
    for point in points:
        if len(point) != 2 or not all(isfinite(float(v)) for v in point):
            raise ValueError(f"{name} coordinates must be finite 2D points")
        p = (float(point[0]), float(point[1]))
        if not ring or hypot(p[0] - ring[-1][0], p[1] - ring[-1][1]) > eps:
            ring.append(p)
    if len(ring) > 1 and hypot(ring[0][0] - ring[-1][0],
                               ring[0][1] - ring[-1][1]) <= eps:
        ring.pop()
    if len(ring) < 3:
        raise ValueError(f"{name} must have at least three vertices")
    if len(set(ring)) != len(ring):
        raise ValueError(f"{name} must not repeat non-consecutive vertices")
    # Reject self-crossing rings; this implementation assumes simple polygons.
    n = len(ring)
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        for j in range(i + 1, n):
            if j in (i, (i + 1) % n) or (j + 1) % n in (i, (i + 1) % n):
                continue
            c, d = ring[j], ring[(j + 1) % n]
            if _segments_intersect(a, b, c, d, eps, include_touch=True):
                raise ValueError(f"{name} must be a simple ring")
    if abs(_area(ring)) <= eps:
        raise ValueError(f"{name} must have non-zero area")
    return ring if _area(ring) > 0 else list(reversed(ring))


def _on_segment(a: Point, b: Point, p: Point, eps: float) -> bool:
    return (min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps
            and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps)


def _segments_intersect(a: Point, b: Point, c: Point, d: Point,
                        eps: float, include_touch: bool = False) -> bool:
    o1, o2 = _cross(a, b, c), _cross(a, b, d)
    o3, o4 = _cross(c, d, a), _cross(c, d, b)
    proper = ((o1 > eps and o2 < -eps) or (o1 < -eps and o2 > eps)) and (
        (o3 > eps and o4 < -eps) or (o3 < -eps and o4 > eps))
    if proper or not include_touch:
        return proper
    return (
        (abs(o1) <= eps and _on_segment(a, b, c, eps))
        or (abs(o2) <= eps and _on_segment(a, b, d, eps))
        or (abs(o3) <= eps and _on_segment(c, d, a, eps))
        or (abs(o4) <= eps and _on_segment(c, d, b, eps))
    )


def _inside(point: Point, ring: Sequence[Point]) -> bool:
    x, y = point
    result = False
    for i, a in enumerate(ring):
        b = ring[(i + 1) % len(ring)]
        if (a[1] > y) != (b[1] > y):
            x_cross = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < x_cross:
                result = not result
    return result


def _intersection(a: Point, b: Point, c: Point, d: Point,
                  eps: float) -> tuple[float, float, Point] | None:
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    denominator = rx * sy - ry * sx
    qx, qy = c[0] - a[0], c[1] - a[1]
    if abs(denominator) <= eps:
        if abs(qx * ry - qy * rx) <= eps:
            # Collinear overlap or touch is outside this algorithm's contract.
            if _segments_intersect(a, b, c, d, eps, include_touch=True):
                raise NotImplementedError("collinear boundary events are not supported")
        return None
    t = (qx * sy - qy * sx) / denominator
    u = (qx * ry - qy * rx) / denominator
    if -eps <= t <= 1 + eps and -eps <= u <= 1 + eps:
        if t <= eps or t >= 1 - eps or u <= eps or u >= 1 - eps:
            raise NotImplementedError("vertex-touch events are not supported")
        return t, u, (a[0] + t * rx, a[1] + t * ry)
    return None


def _make_ring(points: Sequence[Point]) -> list[_Node]:
    nodes = [_Node(p) for p in points]
    for i, node in enumerate(nodes):
        node.next = nodes[(i + 1) % len(nodes)]
        node.prev = nodes[(i - 1) % len(nodes)]
    return nodes


def _insert_events(vertices: list[_Node], events: list[list[tuple[float, _Node]]]) -> None:
    for i, edge_events in enumerate(events):
        previous = vertices[i]
        for alpha, node in sorted(edge_events, key=lambda item: item[0]):
            following = previous.next
            node.prev, node.next = previous, following
            previous.next = node
            following.prev = node
            previous = node


def _nodes(start: _Node):
    node = start
    while True:
        yield node
        node = node.next
        if node is start:
            break


def _clean_ring(points: list[Point], eps: float) -> list[Point]:
    clean: list[Point] = []
    for p in points:
        if not clean or hypot(p[0] - clean[-1][0], p[1] - clean[-1][1]) > eps:
            clean.append(p)
    if len(clean) > 1 and hypot(clean[0][0] - clean[-1][0],
                                clean[0][1] - clean[-1][1]) <= eps:
        clean.pop()
    if len(clean) >= 3 and _area(clean) < 0:
        clean.reverse()
    return clean


def greiner_hormann_intersection(subject: Sequence[Point],
                                 clip: Sequence[Point], *,
                                 epsilon: float = 1e-9) -> list[list[Point]]:
    """Return intersection components as CCW rings.

    Inputs are simple, hole-free polygons in one planar coordinate system.
    Proper crossings are supported. Vertex touches and collinear boundary
    overlaps raise NotImplementedError. Containment and disjoint cases are
    handled without intersection events. Empty/line/point results are [].
    """
    if not isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be finite and positive")
    a = _prepare(subject, "subject", epsilon)
    b = _prepare(clip, "clip", epsilon)
    a_nodes, b_nodes = _make_ring(a), _make_ring(b)
    a_events: list[list[tuple[float, _Node]]] = [[] for _ in a]
    b_events: list[list[tuple[float, _Node]]] = [[] for _ in b]
    count = 0

    for i, p in enumerate(a):
        p2 = a[(i + 1) % len(a)]
        for j, q in enumerate(b):
            q2 = b[(j + 1) % len(b)]
            event = _intersection(p, p2, q, q2, epsilon)
            if event is None:
                continue
            ta, tb, point = event
            na, nb = _Node(point, intersection=True, alpha=ta), _Node(
                point, intersection=True, alpha=tb)
            na.neighbor, nb.neighbor = nb, na
            a_events[i].append((ta, na))
            b_events[j].append((tb, nb))
            count += 1

    if count == 0:
        if _inside(a[0], b):
            return [a]
        if _inside(b[0], a):
            return [b]
        return []

    _insert_events(a_nodes, a_events)
    _insert_events(b_nodes, b_events)

    # An intersection is an entry exactly when the following boundary arc
    # lies inside the other polygon. The paired event is complementary.
    for node in _nodes(a_nodes[0]):
        if node.intersection:
            midpoint = ((node.point[0] + node.next.point[0]) / 2,
                        (node.point[1] + node.next.point[1]) / 2)
            node.entry = _inside(midpoint, b)
    for node in _nodes(b_nodes[0]):
        if node.intersection:
            midpoint = ((node.point[0] + node.next.point[0]) / 2,
                        (node.point[1] + node.next.point[1]) / 2)
            node.entry = _inside(midpoint, a)

    result: list[list[Point]] = []
    for start in _nodes(a_nodes[0]):
        if not start.intersection or not start.entry or start.visited:
            continue
        ring: list[Point] = []
        current = start
        forward = True
        while True:
            if current is start and current.visited:
                break
            ring.append(current.point)
            if current.intersection:
                if current.visited:
                    break
                current.visited = True
                if current.neighbor is start:
                    break
                current = current.neighbor
                current.visited = True
                forward = current.entry
                current = current.next if forward else current.prev
            else:
                current = current.next if forward else current.prev
        cleaned = _clean_ring(ring, epsilon)
        if len(cleaned) >= 3 and abs(_area(cleaned)) > epsilon:
            result.append(cleaned)

    return result

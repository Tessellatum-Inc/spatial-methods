"""Planar alpha-shape boundaries from a Delaunay triangulation.

The parameter is a circumradius threshold (not its reciprocal).
"""
from __future__ import annotations
from collections import defaultdict
from math import isfinite
from numbers import Real
from typing import Sequence
import numpy as np
from scipy.spatial import Delaunay, QhullError

Point = tuple[float, float]
Ring = list[Point]

def _normalise(points: Sequence[Sequence[float]]) -> list[Point]:
    result = []
    for point in points:
        if len(point) != 2:
            raise ValueError("each point must have two coordinates")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError("coordinates must be finite")
        result.append((x, y))
    return sorted(set(result))

def _signed_area(ring: Ring) -> float:
    return 0.5 * sum(
        ring[i][0] * ring[(i + 1) % len(ring)][1]
        - ring[(i + 1) % len(ring)][0] * ring[i][1]
        for i in range(len(ring))
    )

def alpha_shape(points: Sequence[Sequence[float]], alpha: Real) -> list[Ring]:
    """Return unclosed boundary rings for triangles with circumradius <= alpha.

    Alpha is a positive distance threshold in the input coordinate units.
    Outer rings are counter-clockwise; hole rings are clockwise. Inputs with
    fewer than three unique or collinear points return no polygon rings.
    """
    if isinstance(alpha, bool) or not isinstance(alpha, Real):
        raise ValueError("alpha must be a positive finite circumradius threshold")
    alpha = float(alpha)
    if not isfinite(alpha) or alpha <= 0:
        raise ValueError("alpha must be a positive finite circumradius threshold")
    pts = _normalise(points)
    if len(pts) < 3:
        return []
    coordinates = np.asarray(pts, dtype=float)
    try:
        triangulation = Delaunay(coordinates)
    except QhullError:
        return []

    # Each undirected edge stores its first CCW orientation and incidence.
    edge_incidence: dict[tuple[int, int], list[int]] = {}
    for simplex in triangulation.simplices:
        a, b, c = map(int, simplex)
        pa, pb, pc = coordinates[[a, b, c]]
        cross = ((pb[0] - pa[0]) * (pc[1] - pa[1])
                 - (pb[1] - pa[1]) * (pc[0] - pa[0]))
        twice_area = abs(float(cross))
        if twice_area == 0:
            continue
        side_a = float(np.linalg.norm(pb - pc))
        side_b = float(np.linalg.norm(pa - pc))
        side_c = float(np.linalg.norm(pa - pb))
        circumradius = side_a * side_b * side_c / (2.0 * twice_area)
        if circumradius > alpha * (1.0 + 1e-12):
            continue
        if cross < 0:
            b, c = c, b
        for u, v in ((a, b), (b, c), (c, a)):
            key = (min(u, v), max(u, v))
            if key in edge_incidence:
                edge_incidence[key][2] += 1
            else:
                edge_incidence[key] = [u, v, 1]

    boundary_edges = [(u, v) for u, v, n in edge_incidence.values() if n == 1]
    if not boundary_edges:
        return []
    outgoing: dict[int, list[int]] = defaultdict(list)
    for u, v in boundary_edges:
        outgoing[u].append(v)
    if any(len(neighbours) != 1 for neighbours in outgoing.values()):
        raise ValueError("alpha complex has a non-manifold boundary")

    unused = set(boundary_edges)
    rings: list[Ring] = []
    while unused:
        start, current = min(unused)
        ring = [pts[start]]
        previous = start
        while current != start:
            edge = (previous, current)
            if edge not in unused:
                raise ValueError("alpha boundary does not form disjoint simple rings")
            unused.remove(edge)
            ring.append(pts[current])
            neighbours = outgoing.get(current, [])
            if len(neighbours) != 1:
                raise ValueError("alpha complex has an open boundary")
            previous, current = current, neighbours[0]
            if len(ring) > len(boundary_edges):
                raise ValueError("alpha boundary failed to close")
        closing_edge = (previous, start)
        if closing_edge not in unused:
            raise ValueError("alpha boundary does not form disjoint simple rings")
        unused.remove(closing_edge)
        if len(ring) >= 3 and _signed_area(ring) != 0:
            rings.append(ring)
    rings.sort(key=lambda ring: (-abs(_signed_area(ring)), -_signed_area(ring), ring[0]))
    return rings

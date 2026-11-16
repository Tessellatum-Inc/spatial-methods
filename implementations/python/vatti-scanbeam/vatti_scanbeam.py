"""Native scanbeam decomposition primitives for a Vatti-family polygon clipper.

This module deliberately stops before active-edge intersection processing and
Boolean output construction. It extracts scanbeams, horizontal edges, bound
edges and local minima from polygon contours.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from collections.abc import Sequence

Point = tuple[float, float]

def _q(value):
    return Fraction(str(value))

@dataclass(frozen=True)
class BoundEdge:
    edge_id: int
    ring_id: int
    start_vertex: int
    lower: Point
    upper: Point
    winding_delta: int
    @property
    def dx_dy(self):
        return (_q(self.upper[0]) - _q(self.lower[0])) / (_q(self.upper[1]) - _q(self.lower[1]))

@dataclass(frozen=True)
class HorizontalEdge:
    edge_id: int
    ring_id: int
    start_vertex: int
    a: Point
    b: Point

@dataclass(frozen=True)
class LocalMinimum:
    y: float
    left_bound: BoundEdge
    right_bound: BoundEdge
    horizontal_edges: tuple[HorizontalEdge, ...]

@dataclass(frozen=True)
class ScanbeamDecomposition:
    scanbeams: tuple[float, ...]
    bounds: tuple[BoundEdge, ...]
    horizontals: tuple[HorizontalEdge, ...]
    minima: tuple[LocalMinimum, ...]


def _point(p, ring_id, index):
    if len(p) != 2:
        raise ValueError(f"ring {ring_id} vertex {index} must be 2D")
    x, y = float(p[0]), float(p[1])
    if not isfinite(x) or not isfinite(y):
        raise ValueError(f"ring {ring_id} coordinates must be finite")
    return (x, y)


def decompose_scanbeams(rings: Sequence[Sequence[Point]]) -> ScanbeamDecomposition:
    """Extract y scanbeams and local-minimum bound pairs from closed rings.

    Coordinates use a Cartesian y-up convention. Rings may be clockwise or
    counter-clockwise. Horizontal runs at a local minimum are represented as
    horizontal edges and a single minimum whose bounds start at the run's
    endpoints. Collinear consecutive vertices are retained as distinct edges.
    """
    all_y = set()
    bounds = []
    horizontals = []
    minima = []
    edge_id = 0
    prepared = []
    for rid, ring in enumerate(rings):
        pts = [_point(p, rid, i) for i, p in enumerate(ring)]
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts.pop()
        if len(pts) < 3 or len(set(pts)) < 3:
            raise ValueError(f"ring {rid} needs at least three distinct vertices")
        if len(set(pts)) != len(pts):
            raise ValueError(f"ring {rid} contains repeated non-closing vertices")
        prepared.append(pts)
        all_y.update(p[1] for p in pts)

    for rid, pts in enumerate(prepared):
        n = len(pts)
        ring_edges = []
        for i, a in enumerate(pts):
            b = pts[(i + 1) % n]
            if a[1] == b[1]:
                edge = HorizontalEdge(edge_id, rid, i, a, b)
                horizontals.append(edge)
                ring_edges.append(("h", edge))
            else:
                lower, upper = (a, b) if a[1] < b[1] else (b, a)
                delta = 1 if a[1] < b[1] else -1
                edge = BoundEdge(edge_id, rid, i, lower, upper, delta)
                bounds.append(edge)
                ring_edges.append(("b", edge))
            edge_id += 1

        # A minimum is a maximal horizontal run whose two adjacent
        # non-horizontal edges both rise away from the run.
        for start in range(n):
            prev_i = (start - 1) % n
            if pts[prev_i][1] == pts[start][1]:
                continue  # not the first vertex after a horizontal predecessor
            run = [start]
            end = start
            while pts[(end + 1) % n][1] == pts[start][1]:
                end = (end + 1) % n
                if end == start:
                    break
                run.append(end)
            if end == start and len(run) == 1:
                pass
            prev_vertex = pts[(start - 1) % n]
            next_vertex = pts[(end + 1) % n]
            y0 = pts[start][1]
            if prev_vertex[1] <= y0 or next_vertex[1] <= y0:
                continue
            incoming_index = (start - 1) % n
            outgoing_index = end
            incoming = next(e for kind, e in ring_edges
                            if kind == "b" and e.start_vertex == incoming_index)
            outgoing = next(e for kind, e in ring_edges
                            if kind == "b" and e.start_vertex == outgoing_index)
            left, right = sorted((incoming, outgoing), key=lambda e: e.dx_dy)
            run_edges = tuple(e for kind, e in ring_edges
                              if kind == "h" and e.start_vertex in run)
            minima.append(LocalMinimum(y0, left, right, run_edges))

    minima.sort(key=lambda m: (m.y, m.left_bound.lower[0], m.right_bound.lower[0],
                               m.left_bound.edge_id))
    return ScanbeamDecomposition(tuple(sorted(all_y)), tuple(bounds),
                                 tuple(horizontals), tuple(minima))

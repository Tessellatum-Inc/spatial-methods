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


@dataclass(frozen=True)
class EdgeCrossing:
    y: Fraction
    x: Fraction
    first_edge_id: int
    second_edge_id: int


def _x_at(edge: BoundEdge, y: Fraction) -> Fraction:
    y0 = _q(edge.lower[1])
    x0 = _q(edge.lower[0])
    return x0 + edge.dx_dy * (y - y0)


def active_edges_for_band(
    decomposition: ScanbeamDecomposition, lower_y: float, upper_y: float
) -> tuple[BoundEdge, ...]:
    """Return the active-edge list order for one open scanbeam band.

    The order is evaluated at the exact rational midpoint of two consecutive
    scanbeam levels. Edges touching but not spanning the open band are omitted.
    """
    lower, upper = _q(lower_y), _q(upper_y)
    if not lower < upper:
        raise ValueError("scanbeam band must have positive height")
    levels = tuple(_q(y) for y in decomposition.scanbeams)
    if lower not in levels or upper not in levels or levels.index(upper) != levels.index(lower) + 1:
        raise ValueError("band endpoints must be consecutive scanbeam levels")
    mid = (lower + upper) / 2
    active = [edge for edge in decomposition.bounds
              if _q(edge.lower[1]) <= lower and _q(edge.upper[1]) >= upper]
    active.sort(key=lambda edge: (_x_at(edge, mid), edge.dx_dy, edge.edge_id))
    return tuple(active)


def crossings_in_band(
    active_edges: Sequence[BoundEdge], lower_y: float, upper_y: float
) -> tuple[EdgeCrossing, ...]:
    """Find pairwise bound-edge crossings strictly inside a scanbeam band.

    This transparent O(m²) event generator is a correctness-oriented
    foundation, not Vatti's optimized neighbour-only intersection scheduler.
    """
    lower, upper = _q(lower_y), _q(upper_y)
    if not lower < upper:
        raise ValueError("scanbeam band must have positive height")
    events = []
    for i, first in enumerate(active_edges):
        m1 = first.dx_dy
        b1 = _q(first.lower[0]) - m1 * _q(first.lower[1])
        for second in active_edges[i + 1:]:
            m2 = second.dx_dy
            if m1 == m2:
                continue
            b2 = _q(second.lower[0]) - m2 * _q(second.lower[1])
            y = (b2 - b1) / (m1 - m2)
            if lower < y < upper:
                x = m1 * y + b1
                events.append(EdgeCrossing(y, x,
                    min(first.edge_id, second.edge_id),
                    max(first.edge_id, second.edge_id)))
    events.sort(key=lambda event: (event.y, event.x,
                                   event.first_edge_id, event.second_edge_id))
    return tuple(events)


@dataclass(frozen=True)
class ActiveEdgeSlice:
    lower_y: Fraction
    upper_y: Fraction
    edges: tuple[BoundEdge, ...]


def sweep_active_edge_slices(
    active_edges: Sequence[BoundEdge], lower_y: float, upper_y: float
) -> tuple[ActiveEdgeSlice, ...]:
    """Split a scanbeam band at every pairwise crossing and order each slice.

    At an isolated crossing the two edges exchange horizontal order in the
    adjacent open slices. Coincident/overlapping edges are not resolved here;
    equal-slope pairs are left in deterministic edge-id order. This O(m²)
    routine is an explicit reference model for later neighbour-event logic.
    """
    lower, upper = _q(lower_y), _q(upper_y)
    if not lower < upper:
        raise ValueError("scanbeam band must have positive height")
    events = crossings_in_band(active_edges, lower_y, upper_y)
    levels = [lower]
    for event in events:
        if event.y != levels[-1]:
            levels.append(event.y)
    if levels[-1] != upper:
        levels.append(upper)
    slices = []
    for lo, hi in zip(levels, levels[1:]):
        mid = (lo + hi) / 2
        ordered = tuple(sorted(active_edges,
            key=lambda edge: (_x_at(edge, mid), edge.dx_dy, edge.edge_id)))
        slices.append(ActiveEdgeSlice(lo, hi, ordered))
    return tuple(slices)


def winding_states(edges: Sequence[BoundEdge]) -> tuple[int, ...]:
    """Return cumulative signed winding after each edge in left-to-right order.

    This exposes the raw winding transitions only. Subject/clip attribution,
    fill-rule evaluation and horizontal-boundary semantics belong to the
    Boolean clipping layer and are intentionally not inferred here.
    """
    total = 0
    states = []
    for edge in edges:
        total += edge.winding_delta
        states.append(total)
    return tuple(states)


@dataclass(frozen=True)
class HorizontalEvent:
    y: Fraction
    x_start: Fraction
    x_end: Fraction
    horizontal_edge_id: int
    other_edge_id: int
    kind: str  # "point" or "overlap"
    other_kind: str  # "bound" or "horizontal"


def horizontal_events_at(
    decomposition: ScanbeamDecomposition, y_value: float
) -> tuple[HorizontalEvent, ...]:
    """Find intersections involving horizontal edges on one scanbeam.

    Horizontal/bound intersections include bound endpoints and interior
    crossings. Horizontal/horizontal contacts are classified as point contacts
    or positive-length overlaps. All comparisons and returned coordinates use
    exact rational representations of the input decimal coordinates.
    """
    y = _q(y_value)
    events = []
    horizontals = [edge for edge in decomposition.horizontals
                   if _q(edge.a[1]) == y]
    bounds = [edge for edge in decomposition.bounds
              if _q(edge.lower[1]) <= y <= _q(edge.upper[1])]
    for horizontal in horizontals:
        hx0, hx1 = sorted((_q(horizontal.a[0]), _q(horizontal.b[0])))
        for bound in bounds:
            x = _x_at(bound, y)
            if hx0 <= x <= hx1:
                events.append(HorizontalEvent(
                    y, x, x, horizontal.edge_id, bound.edge_id, "point", "bound"
                ))
    for i, first in enumerate(horizontals):
        a0, a1 = sorted((_q(first.a[0]), _q(first.b[0])))
        for second in horizontals[i + 1:]:
            if first.ring_id == second.ring_id:
                continue
            b0, b1 = sorted((_q(second.a[0]), _q(second.b[0])))
            lo, hi = max(a0, b0), min(a1, b1)
            if lo <= hi:
                events.append(HorizontalEvent(
                    y, lo, hi, first.edge_id, second.edge_id,
                    "point" if lo == hi else "overlap", "horizontal"
                ))
    events.sort(key=lambda event: (
        event.x_start, event.x_end, event.horizontal_edge_id,
        event.other_edge_id, event.other_kind
    ))
    return tuple(events)


def is_filled(winding: int, fill_rule: str = "non_zero") -> bool:
    """Evaluate one contour-set winding count under a Clipper-style fill rule."""
    rules = {
        "even_odd": lambda value: abs(value) % 2 == 1,
        "non_zero": lambda value: value != 0,
        "positive": lambda value: value > 0,
        "negative": lambda value: value < 0,
    }
    try:
        predicate = rules[fill_rule]
    except KeyError as exc:
        raise ValueError(f"unsupported fill rule: {fill_rule}") from exc
    return predicate(int(winding))


def boolean_result(
    subject_winding: int,
    clip_winding: int,
    operation: str,
    fill_rule: str = "non_zero",
) -> bool:
    """Evaluate a Boolean operation from subject and clip winding counts.

    This is the point-classification truth table only; it does not build a
    planar arrangement or derive winding counts from polygon edges.
    """
    subject = is_filled(subject_winding, fill_rule)
    clip = is_filled(clip_winding, fill_rule)
    operations = {
        "intersection": subject and clip,
        "union": subject or clip,
        "difference": subject and not clip,
        "xor": subject != clip,
    }
    try:
        return operations[operation]
    except KeyError as exc:
        raise ValueError(f"unsupported Boolean operation: {operation}") from exc


@dataclass(frozen=True)
class FillTransition:
    edge_id: int
    ring_id: int
    subject_before: int
    subject_after: int
    clip_before: int
    clip_after: int
    result_before: bool
    result_after: bool


def fill_transitions(
    active_edges: Sequence[BoundEdge],
    subject_ring_ids: set[int],
    clip_ring_ids: set[int],
    operation: str = "intersection",
    fill_rule: str = "non_zero",
) -> tuple[FillTransition, ...]:
    """Propagate subject/clip winding counts across a left-to-right edge list.

    The caller supplies edges in their current left-to-right order and assigns
    every ring to exactly one operand. This computes fill-state transitions
    only; it does not schedule intersections, repair coincident edges, or
    construct output contours.
    """
    if subject_ring_ids & clip_ring_ids:
        raise ValueError("subject and clip ring sets must be disjoint")
    if operation not in {"intersection", "union", "difference", "xor"}:
        raise ValueError(f"unsupported Boolean operation: {operation}")
    known = subject_ring_ids | clip_ring_ids
    if any(edge.ring_id not in known for edge in active_edges):
        raise ValueError("every active edge must belong to subject or clip")
    subject = clip = 0
    transitions = []
    for edge in active_edges:
        before_subject, before_clip = subject, clip
        if edge.ring_id in subject_ring_ids:
            subject += edge.winding_delta
        else:
            clip += edge.winding_delta
        before = boolean_result(before_subject, before_clip, operation, fill_rule)
        after = boolean_result(subject, clip, operation, fill_rule)
        transitions.append(FillTransition(
            edge.edge_id, edge.ring_id,
            before_subject, subject, before_clip, clip, before, after
        ))
    return tuple(transitions)

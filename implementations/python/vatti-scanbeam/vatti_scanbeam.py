"""Reference scanbeam and Boolean-cell pipeline for a Vatti-family clipper.

The implementation prioritizes exact-rational reference calculations and
explicitly documents where it is not yet a production Vatti event scheduler.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from collections.abc import Sequence
from functools import cmp_to_key

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


@dataclass(frozen=True)
class HorizontalFillTransition:
    """An interval whose Boolean fill state changes across a scanbeam level."""
    y: Fraction
    x_start: Fraction
    x_end: Fraction
    below_filled: bool
    above_filled: bool
    horizontal_edge_ids: tuple[int, ...]


@dataclass(frozen=True)
class ScanbeamLevel:
    y: Fraction
    starting_edges: tuple[BoundEdge, ...]
    ending_edges: tuple[BoundEdge, ...]
    horizontal_edges: tuple[HorizontalEdge, ...]
    horizontal_events: tuple[HorizontalEvent, ...]
    local_minima: tuple[LocalMinimum, ...]
    fill_transitions: tuple[HorizontalFillTransition, ...] = ()


@dataclass(frozen=True)
class FilledCell:
    """One Boolean-filled trapezoid/triangle in a crossing-free sweep slice."""
    lower_y: Fraction
    upper_y: Fraction
    left_edge_id: int
    right_edge_id: int
    vertices: tuple[tuple[Fraction, Fraction], ...]


@dataclass(frozen=True)
class BooleanSweep:
    levels: tuple[ScanbeamLevel, ...]
    cells: tuple[FilledCell, ...]
    band_slice_count: int


def _filled_spans(
    edges: Sequence[BoundEdge],
    subject_ring_ids: set[int],
    clip_ring_ids: set[int],
    operation: str,
    fill_rule: str,
) -> tuple[tuple[BoundEdge, BoundEdge], ...]:
    transitions = fill_transitions(
        edges, subject_ring_ids, clip_ring_ids, operation, fill_rule
    )
    by_id = {edge.edge_id: edge for edge in edges}
    spans = []
    left = None
    for transition in transitions:
        if not transition.result_before and transition.result_after:
            if left is not None:
                raise ValueError("Boolean fill entered twice without an exit")
            left = by_id[transition.edge_id]
        elif transition.result_before and not transition.result_after:
            if left is None:
                raise ValueError("Boolean fill exited without a matching entry")
            spans.append((left, by_id[transition.edge_id]))
            left = None
    if left is not None:
        raise ValueError("active edges leave an unbounded filled interval")
    return tuple(spans)


def sweep_boolean(
    decomposition: ScanbeamDecomposition,
    subject_ring_ids: set[int],
    clip_ring_ids: set[int],
    operation: str = "intersection",
    fill_rule: str = "non_zero",
) -> BooleanSweep:
    """Sweep all scanbeam bands and decompose the Boolean result into cells.

    Every band first coalesces coincident active bounds into operand-aware
    winding bundles. A neighbour-event heap schedules adjacent bundle
    intersections; simultaneous multiway crossings are reordered atomically.
    Each crossing-free slice propagates subject/clip winding states and emits
    exact-rational filled cells. Horizontal contacts are attached to scanbeam
    levels and inserted as noding points along cell boundaries before contour
    assembly. The result is a reference sweep, not yet the complete Vatti
    intersection-list algorithm.
    """
    if not subject_ring_ids or not clip_ring_ids:
        raise ValueError("subject and clip ring sets must both be non-empty")
    if subject_ring_ids & clip_ring_ids:
        raise ValueError("subject and clip ring sets must be disjoint")
    if operation not in {"intersection", "union", "difference", "xor"}:
        raise ValueError(f"unsupported Boolean operation: {operation}")
    # Validate operand ownership even for edges which are not active in a band.
    if any(edge.ring_id not in subject_ring_ids | clip_ring_ids
           for edge in decomposition.bounds):
        raise ValueError("every bound edge must belong to subject or clip")

    levels = []
    cells = []
    for y in decomposition.scanbeams:
        qy = _q(y)
        starts = tuple(sorted(
            (edge for edge in decomposition.bounds if _q(edge.lower[1]) == qy),
            key=lambda edge: (edge.lower[0], edge.edge_id)))
        ends = tuple(sorted(
            (edge for edge in decomposition.bounds if _q(edge.upper[1]) == qy),
            key=lambda edge: (edge.upper[0], edge.edge_id)))
        horizontal = tuple(edge for edge in decomposition.horizontals
                           if _q(edge.a[1]) == qy)
        minima = tuple(minimum for minimum in decomposition.minima
                       if _q(minimum.y) == qy)
        levels.append(ScanbeamLevel(
            qy, starts, ends, horizontal,
            horizontal_events_at(decomposition, y), minima
        ))

    slice_count = 0
    for lower_y, upper_y in zip(decomposition.scanbeams,
                                decomposition.scanbeams[1:]):
        active = active_edges_for_band(decomposition, lower_y, upper_y)
        bundles = bundle_active_edges(active, subject_ring_ids, clip_ring_ids)
        slices = sweep_neighbour_ordered_bundles(bundles, lower_y, upper_y)
        slice_count += len(slices)
        for slice_ in slices:
            spans = _bundle_spans(slice_.bundles, operation, fill_rule)
            for left_bundle, right_bundle in spans:
                left, right = left_bundle.representative, right_bundle.representative
                lo, hi = slice_.lower_y, slice_.upper_y
                vertices = (
                    (_x_at(left, lo), lo),
                    (_x_at(right, lo), lo),
                    (_x_at(right, hi), hi),
                    (_x_at(left, hi), hi),
                )
                # A crossing can collapse a trapezoid to a triangle. Reject
                # only truly zero-area cells, retaining exact rational area.
                twice_area = sum(
                    vertices[i][0] * vertices[(i + 1) % 4][1]
                    - vertices[(i + 1) % 4][0] * vertices[i][1]
                    for i in range(4)
                )
                if twice_area:
                    cells.append(FilledCell(
                        lo, hi, left.edge_id, right.edge_id, vertices
                    ))
    levels = [
        ScanbeamLevel(
            level.y, level.starting_edges, level.ending_edges,
            level.horizontal_edges, level.horizontal_events,
            level.local_minima,
            horizontal_fill_transitions(
                decomposition, level.y, subject_ring_ids, clip_ring_ids,
                operation, fill_rule
            )
        )
        for level in levels
    ]
    cells = list(_node_cells_at_horizontal_events(cells, levels))
    return BooleanSweep(tuple(levels), tuple(cells), slice_count)


@dataclass(frozen=True)
class ContourResult:
    """Closed output rings; shells are CCW and holes are CW by construction."""
    rings: tuple[tuple[tuple[Fraction, Fraction], ...], ...]
    boundary_edge_count: int


def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _polar_compare(a, b):
    """Exact CCW polar ordering for non-zero vectors."""
    ha = 0 if (a[1] > 0 or (a[1] == 0 and a[0] >= 0)) else 1
    hb = 0 if (b[1] > 0 or (b[1] == 0 and b[0] >= 0)) else 1
    if ha != hb:
        return -1 if ha < hb else 1
    cross = _cross(a, b)
    if cross:
        return -1 if cross > 0 else 1
    da = a[0] * a[0] + a[1] * a[1]
    db = b[0] * b[0] + b[1] * b[1]
    return (da > db) - (da < db)


def _point_on_segment(a, b, p):
    return (_cross((b[0]-a[0], b[1]-a[1]),
                   (p[0]-a[0], p[1]-a[1])) == 0 and
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _segment_parameter(a, b, p):
    dx, dy = b[0]-a[0], b[1]-a[1]
    return (p[0]-a[0])/dx if dx else (p[1]-a[1])/dy


def _cell_boundary_segments(cells):
    """Node cell edges at every cell vertex before cancelling shared edges.

    This handles unequal subdivisions of a shared straight boundary (for
    example, a long edge adjacent to two shorter edges) without floating point.
    """
    raw = []
    vertices = set()
    for cell in cells:
        points = cell.vertices
        vertices.update(points)
        raw.extend((points[i], points[(i+1) % len(points)])
                   for i in range(len(points)))
    atomic = []
    for a, b in raw:
        cuts = sorted((p for p in vertices if _point_on_segment(a, b, p)),
                      key=lambda p: _segment_parameter(a, b, p))
        atomic.extend((u, v) for u, v in zip(cuts, cuts[1:]) if u != v)
    return atomic


def _cancel_shared_cell_edges(cells):
    """Return directed exterior atomic edges after exact reverse-edge cancel."""
    counts = {}
    for a, b in _cell_boundary_segments(cells):
        key = (a, b) if a < b else (b, a)
        direction = 1 if (a, b) == key else -1
        counts[key] = counts.get(key, 0) + direction
    boundary = []
    for (a, b), count in counts.items():
        if abs(count) > 1:
            raise ValueError("overlapping filled cells produce duplicate boundary edges")
        if count == 1:
            boundary.append((a, b))
        elif count == -1:
            boundary.append((b, a))
    return tuple(boundary)


def _ring_area2(ring):
    return sum(ring[i][0] * ring[(i+1) % len(ring)][1] -
               ring[(i+1) % len(ring)][0] * ring[i][1]
               for i in range(len(ring)))


def _simplify_ring(ring):
    """Remove redundant collinear vertices while retaining exact coordinates."""
    points = list(ring)
    changed = True
    while changed and len(points) > 3:
        changed = False
        kept = []
        n = len(points)
        for i, point in enumerate(points):
            prev, nxt = points[(i-1) % n], points[(i+1) % n]
            if _cross((point[0]-prev[0], point[1]-prev[1]),
                      (nxt[0]-point[0], nxt[1]-point[1])) == 0:
                changed = True
            else:
                kept.append(point)
        if len(kept) < 3:
            raise ValueError("contour collapsed during collinear simplification")
        points = kept
    return tuple(points)


def stitch_filled_cells(cells: Sequence[FilledCell]) -> ContourResult:
    """Cancel cell seams and stitch exact directed boundary edges into rings.

    Each input cell is CCW, so its filled interior lies to the left of every
    directed edge. Shared seams are noded at all cell vertices and cancelled.
    At a multi-edge vertex, the clockwise predecessor of the incoming twin
    defines the same local face-walk convention used by a planar DCEL.
    """
    boundary = _cancel_shared_cell_edges(cells)
    if not boundary:
        return ContourResult((), 0)

    outgoing = {}
    incoming_count = {}
    for eid, (a, b) in enumerate(boundary):
        outgoing.setdefault(a, []).append(eid)
        incoming_count[b] = incoming_count.get(b, 0) + 1
    if set(outgoing) != set(incoming_count):
        raise ValueError("cell boundary has dangling vertices")
    for vertex, edges in outgoing.items():
        if len(edges) != incoming_count[vertex]:
            raise ValueError("cell boundary is not balanced at a vertex")

    successor = {}
    for eid, (a, b) in enumerate(boundary):
        candidates = outgoing[b]
        reverse = (a[0]-b[0], a[1]-b[1])
        ordered = sorted(candidates, key=cmp_to_key(
            lambda first, second: _polar_compare(
                (boundary[first][1][0]-b[0], boundary[first][1][1]-b[1]),
                (boundary[second][1][0]-b[0], boundary[second][1][1]-b[1])
            )))
        predecessor = None
        for candidate in ordered:
            vector = (boundary[candidate][1][0]-b[0],
                      boundary[candidate][1][1]-b[1])
            if _polar_compare(vector, reverse) < 0:
                predecessor = candidate
            else:
                break
        successor[eid] = predecessor if predecessor is not None else ordered[-1]

    if len(set(successor.values())) != len(boundary):
        raise ValueError("boundary face-walk is not one-to-one at a vertex")

    visited = set()
    rings = []
    for start in range(len(boundary)):
        if start in visited:
            continue
        ring = []
        current = start
        while current not in visited:
            visited.add(current)
            ring.append(boundary[current][0])
            current = successor[current]
        if current != start:
            raise ValueError("boundary walk entered a previously visited contour")
        ring = _simplify_ring(ring)
        if _ring_area2(ring) == 0:
            raise ValueError("stitched contour has zero signed area")
        rings.append(tuple(ring) + (ring[0],))

    # Deterministic ordering: shells first, then holes; larger rings first.
    rings.sort(key=lambda ring: (
        0 if _ring_area2(ring[:-1]) > 0 else 1,
        -abs(_ring_area2(ring[:-1])),
        ring[0]
    ))
    return ContourResult(tuple(rings), len(boundary))


def clip_rings(
    decomposition: ScanbeamDecomposition,
    subject_ring_ids: set[int],
    clip_ring_ids: set[int],
    operation: str = "intersection",
    fill_rule: str = "non_zero",
) -> ContourResult:
    """Reference Boolean clipping API returning stitched polygon boundary rings."""
    sweep = sweep_boolean(
        decomposition, subject_ring_ids, clip_ring_ids, operation, fill_rule
    )
    return stitch_filled_cells(sweep.cells)


@dataclass(frozen=True)
class ActiveEdgeBundle:
    """Coincident active bounds with operand-specific aggregate winding."""
    representative: BoundEdge
    members: tuple[BoundEdge, ...]
    subject_delta: int
    clip_delta: int

    @property
    def slope(self):
        return self.representative.dx_dy

    def x_at(self, y):
        return _x_at(self.representative, y)


@dataclass(frozen=True)
class BundleSlice:
    lower_y: Fraction
    upper_y: Fraction
    bundles: tuple[ActiveEdgeBundle, ...]


def bundle_active_edges(
    edges: Sequence[BoundEdge],
    subject_ring_ids: set[int],
    clip_ring_ids: set[int],
) -> tuple[ActiveEdgeBundle, ...]:
    """Coalesce geometrically coincident bounds and sum winding per operand.

    All active edges span the same open scanbeam band. Equal slope and equal
    exact intercept therefore means they coincide throughout that band.
    Oppositely directed copies cancel algebraically without losing provenance.
    """
    grouped = {}
    for edge in edges:
        slope = edge.dx_dy
        intercept = _q(edge.lower[0]) - slope * _q(edge.lower[1])
        grouped.setdefault((slope, intercept), []).append(edge)
    bundles = []
    for key, members in grouped.items():
        members = tuple(sorted(members, key=lambda e: e.edge_id))
        subject_delta = sum(e.winding_delta for e in members
                            if e.ring_id in subject_ring_ids)
        clip_delta = sum(e.winding_delta for e in members
                         if e.ring_id in clip_ring_ids)
        bundles.append(ActiveEdgeBundle(
            members[0], members, subject_delta, clip_delta
        ))
    bundles.sort(key=lambda b: (
        b.x_at((_q(b.representative.lower[1]) +
                _q(b.representative.upper[1])) / 2),
        b.slope, b.representative.edge_id
    ))
    return tuple(bundles)


def _bundle_spans(
    bundles: Sequence[ActiveEdgeBundle],
    operation: str,
    fill_rule: str,
) -> tuple[tuple[ActiveEdgeBundle, ActiveEdgeBundle], ...]:
    subject = clip = 0
    left = None
    spans = []
    for bundle in bundles:
        before = boolean_result(subject, clip, operation, fill_rule)
        subject += bundle.subject_delta
        clip += bundle.clip_delta
        after = boolean_result(subject, clip, operation, fill_rule)
        if not before and after:
            if left is not None:
                raise ValueError("coincident bundles create nested Boolean entries")
            left = bundle
        elif before and not after:
            if left is None:
                raise ValueError("Boolean bundle exits without an entry")
            spans.append((left, bundle))
            left = None
    if left is not None:
        raise ValueError("bundle list leaves an unbounded filled interval")
    return tuple(spans)


def _bundle_intersection_y(first, second):
    if first.slope == second.slope:
        return None
    f = first.representative
    g = second.representative
    bf = _q(f.lower[0]) - first.slope * _q(f.lower[1])
    bg = _q(g.lower[0]) - second.slope * _q(g.lower[1])
    return (bg - bf) / (first.slope - second.slope)


def sweep_neighbour_ordered_bundles(
    bundles: Sequence[ActiveEdgeBundle],
    lower_y: float,
    upper_y: float,
) -> tuple[BundleSlice, ...]:
    """Schedule only adjacent bundle crossings with a rational event heap.

    At a multiway event, all bundles meeting at the same (x,y) are reordered
    together by slope. Only newly adjacent pairs are scheduled afterwards.
    Equal-line bundles have already been coalesced, so coincident edges do not
    create an infinite stream of zero-distance crossing events.
    """
    import heapq

    lower, upper = _q(lower_y), _q(upper_y)
    if not lower < upper:
        raise ValueError("scanbeam band must have positive height")
    ordered = list(sorted(bundles, key=lambda b: (
        b.x_at(lower), b.slope, b.representative.edge_id
    )))
    if len(ordered) < 2:
        return (BundleSlice(lower, upper, tuple(ordered)),) if ordered else ()

    events = []
    scheduled = set()
    serial = 0

    def schedule(index, current_y):
        nonlocal serial
        if index < 0 or index + 1 >= len(ordered):
            return
        first, second = ordered[index], ordered[index + 1]
        y = _bundle_intersection_y(first, second)
        if y is None or not current_y < y < upper:
            return
        pair = tuple(sorted((first.representative.edge_id,
                             second.representative.edge_id)))
        token = (pair, y)
        if token in scheduled:
            return
        scheduled.add(token)
        x = first.x_at(y)
        heapq.heappush(events, (y, x, serial, index, pair))
        serial += 1

    for i in range(len(ordered)-1):
        schedule(i, lower)

    slices = []
    current_y = lower
    while events:
        y, x, _, index, pair = heapq.heappop(events)
        if y < current_y:
            continue
        if y >= upper:
            break
        # A stale event is ignored unless its two bundles remain adjacent.
        if index + 1 >= len(ordered):
            continue
        a, b = ordered[index], ordered[index+1]
        if tuple(sorted((a.representative.edge_id,
                         b.representative.edge_id))) != pair:
            continue
        if a.x_at(y) != x or b.x_at(y) != x:
            continue
        if y > current_y:
            slices.append(BundleSlice(current_y, y, tuple(ordered)))
            current_y = y

        # Expand the event to every bundle incident at this same geometric
        # vertex, handling multiway crossings as one atomic order change.
        lo = index
        while lo > 0 and ordered[lo-1].x_at(y) == x:
            lo -= 1
        hi = index + 1
        while hi + 1 < len(ordered) and ordered[hi+1].x_at(y) == x:
            hi += 1
        ordered[lo:hi+1] = sorted(
            ordered[lo:hi+1],
            key=lambda bundle: (bundle.slope,
                                bundle.representative.edge_id)
        )
        for j in range(max(0, lo-1), min(len(ordered)-1, hi+1)+1):
            schedule(j, current_y)

    if current_y < upper:
        slices.append(BundleSlice(current_y, upper, tuple(ordered)))
    return tuple(slices)


def _node_cells_at_horizontal_events(cells, levels):
    """Insert horizontal contact coordinates into cell edges before stitching."""
    event_points = {}
    for level in levels:
        for event in level.horizontal_events:
            event_points.setdefault(event.y, set()).update(
                ((event.x_start, event.y), (event.x_end, event.y))
            )
        for transition in level.fill_transitions:
            event_points.setdefault(transition.y, set()).update(
                ((transition.x_start, transition.y),
                 (transition.x_end, transition.y))
            )
    noded = []
    for cell in cells:
        points = list(cell.vertices)
        expanded = []
        for i, a in enumerate(points):
            b = points[(i+1) % len(points)]
            expanded.append(a)
            if a[1] != b[1]:
                continue
            candidates = event_points.get(a[1], set())
            interior = [p for p in candidates
                        if p != a and p != b and
                        min(a[0], b[0]) < p[0] < max(a[0], b[0])]
            if b[0] < a[0]:
                interior.reverse()
            expanded.extend(interior)
        noded.append(FilledCell(
            cell.lower_y, cell.upper_y, cell.left_edge_id,
            cell.right_edge_id, tuple(expanded)
        ))
    return tuple(noded)



def horizontal_fill_transitions(
    decomposition: ScanbeamDecomposition,
    y: Fraction,
    subject_ring_ids: set[int],
    clip_ring_ids: set[int],
    operation: str = "intersection",
    fill_rule: str = "non_zero",
) -> tuple[HorizontalFillTransition, ...]:
    """Derive Boolean fill changes immediately below and above a scanbeam.

    Each adjacent open band supplies its own edge order at the level. Edges
    tied at a vertex are ordered by slope in the appropriate one-sided limit:
    descending slope below, ascending slope above. The resulting filled
    intervals are overlaid with horizontal source-edge endpoints and contact
    events. Every interval whose Boolean occupancy changes is emitted as a
    horizontal fill transition and becomes a contour noding constraint.
    """
    levels = tuple(_q(value) for value in decomposition.scanbeams)
    if y not in levels:
        raise ValueError("horizontal transition level must be a scanbeam")
    index = levels.index(y)

    def intervals_for_band(lower, upper, below):
        active = active_edges_for_band(decomposition, lower, upper)
        bundles = bundle_active_edges(active, subject_ring_ids, clip_ring_ids)
        if below:
            ordered = sorted(bundles, key=lambda b: (
                b.x_at(y), -b.slope, b.representative.edge_id
            ))
        else:
            ordered = sorted(bundles, key=lambda b: (
                b.x_at(y), b.slope, b.representative.edge_id
            ))
        spans = _bundle_spans(ordered, operation, fill_rule)
        return tuple((left.x_at(y), right.x_at(y)) for left, right in spans
                     if left.x_at(y) < right.x_at(y))

    below = intervals_for_band(levels[index-1], y, True) if index > 0 else ()
    above = intervals_for_band(y, levels[index+1], False) if index+1 < len(levels) else ()

    horizontal = [edge for edge in decomposition.horizontals
                  if _q(edge.a[1]) == y]
    cuts = {x for interval in below + above for x in interval}
    for edge in horizontal:
        cuts.update((_q(edge.a[0]), _q(edge.b[0])))
    for event in horizontal_events_at(decomposition, y):
        cuts.update((event.x_start, event.x_end))
    ordered_cuts = sorted(cuts)
    transitions = []
    for x0, x1 in zip(ordered_cuts, ordered_cuts[1:]):
        if x0 == x1:
            continue
        midpoint = (x0 + x1) / 2
        below_filled = any(a < midpoint < b for a, b in below)
        above_filled = any(a < midpoint < b for a, b in above)
        if below_filled == above_filled:
            continue
        source_ids = tuple(sorted(
            edge.edge_id for edge in horizontal
            if min(_q(edge.a[0]), _q(edge.b[0])) <= midpoint <=
               max(_q(edge.a[0]), _q(edge.b[0]))
        ))
        transitions.append(HorizontalFillTransition(
            y, x0, x1, below_filled, above_filled, source_ids
        ))
    return tuple(transitions)

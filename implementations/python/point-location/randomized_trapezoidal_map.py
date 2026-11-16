"""Randomized trapezoidal decomposition and point-location search DAG.

This is a correctness-first reference implementation for bounded, non-crossing,
non-vertical segments in general position. Segments are inserted in a seeded
random permutation. After each insertion the vertical decomposition and search
DAG are rebuilt from the current set. This deliberately simple update strategy
makes the insertion order and map invariants inspectable, but is NOT the
asymptotically efficient local-update Seidel algorithm.

The final map supports point-to-trapezoid queries. Original segment boundaries
return BOUNDARY; points outside the bounding box return None.
"""
from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from random import Random
from typing import Iterable, Sequence

Point = tuple[float, float]
Segment = tuple[Point, Point]
BOUNDARY = "BOUNDARY"


@dataclass
class Trapezoid:
    id: tuple[int, ...]
    x_left: float
    x_right: float
    bottom_segment: int | None
    top_segment: int | None
    left_neighbors: tuple[tuple[int, ...], ...] = ()
    right_neighbors: tuple[tuple[int, ...], ...] = ()


@dataclass(frozen=True)
class CorridorSplit:
    """Local replacement pieces created when one segment crosses a cell."""
    source_trapezoid: Trapezoid
    lower: Trapezoid
    upper: Trapezoid


@dataclass(frozen=True)
class _YNode:
    segment_id: int
    left: "_YNode | Trapezoid"
    right: "_YNode | Trapezoid"


@dataclass(frozen=True)
class _XNode:
    split_x: float
    left: "_XNode | tuple[_YNode | Trapezoid, tuple[float, ...]]"
    right: "_XNode | tuple[_YNode | Trapezoid, tuple[float, ...]]"


def _point(value: Sequence[float]) -> Point:
    if len(value) != 2:
        raise ValueError("points must contain exactly two coordinates")
    x, y = float(value[0]), float(value[1])
    if not (isfinite(x) and isfinite(y)):
        raise ValueError("coordinates must be finite")
    return x, y


def _orient(a: Point, b: Point, c: Point) -> Fraction:
    ax, ay = map(lambda v: Fraction(str(v)), a)
    bx, by = map(lambda v: Fraction(str(v)), b)
    cx, cy = map(lambda v: Fraction(str(v)), c)
    return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)


def _on_segment(p: Point, a: Point, b: Point, eps: float) -> bool:
    cross = abs(_orient(a, b, p))
    scale = max(1.0, abs(b[0]-a[0]), abs(b[1]-a[1]))
    return (cross <= eps*scale and
            min(a[0], b[0])-eps <= p[0] <= max(a[0], b[0])+eps and
            min(a[1], b[1])-eps <= p[1] <= max(a[1], b[1])+eps)


def _intersects(a: Segment, b: Segment) -> bool:
    p, q = a
    r, s = b
    o1, o2 = _orient(p, q, r), _orient(p, q, s)
    o3, o4 = _orient(r, s, p), _orient(r, s, q)
    return ((o1 == 0 and _on_segment(r, p, q, 0.0)) or
            (o2 == 0 and _on_segment(s, p, q, 0.0)) or
            (o3 == 0 and _on_segment(p, r, s, 0.0)) or
            (o4 == 0 and _on_segment(q, r, s, 0.0)) or
            ((o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)))


def _y_at(segment: Segment, x: float) -> float:
    (x1, y1), (x2, y2) = segment
    return y1 + (x-x1)*(y2-y1)/(x2-x1)


class RandomizedTrapezoidalMap:
    """Build a trapezoidal map for a non-crossing segment set.

    General-position contract:
    * all input segments are non-vertical and have distinct endpoint x-values;
    * no two segments intersect, touch, or overlap;
    * all segments lie strictly inside the supplied bounding box.

    The implementation uses a randomized insertion permutation but rebuilds
    the vertical decomposition after each insertion. Search uses a balanced
    x-decision tree followed by a balanced y-decision tree in the selected
    slab. This is a reference search DAG, not the optimized history DAG.
    """

    def __init__(self, segments: Iterable[Sequence[Sequence[float]]],
                 bounds: Sequence[float], *, seed: int = 0, epsilon: float = 1e-10):
        if len(bounds) != 4:
            raise ValueError("bounds must be (xmin, ymin, xmax, ymax)")
        xmin, ymin, xmax, ymax = map(float, bounds)
        if not all(map(isfinite, (xmin, ymin, xmax, ymax))) or not xmin < xmax or not ymin < ymax:
            raise ValueError("bounds must be finite with positive width and height")
        if not isfinite(epsilon) or epsilon < 0:
            raise ValueError("epsilon must be finite and non-negative")
        self.bounds = (xmin, ymin, xmax, ymax)
        self.epsilon = epsilon
        normalised: list[Segment] = []
        endpoint_x: set[float] = set()
        for raw in segments:
            if len(raw) != 2:
                raise ValueError("each segment must have two endpoints")
            a, b = _point(raw[0]), _point(raw[1])
            if a == b:
                raise ValueError("zero-length segments are not supported")
            if a[0] == b[0]:
                raise ValueError("vertical input segments are not supported")
            if a[0] > b[0]:
                a, b = b, a
            if not (xmin < a[0] < xmax and xmin < b[0] < xmax and
                    ymin < a[1] < ymax and ymin < b[1] < ymax):
                raise ValueError("segments must lie strictly inside the bounding box")
            if a[0] in endpoint_x or b[0] in endpoint_x:
                raise ValueError("all endpoint x-coordinates must be distinct")
            endpoint_x.update((a[0], b[0]))
            normalised.append((a, b))
        for i, a in enumerate(normalised):
            for b in normalised[i+1:]:
                if _intersects(a, b):
                    raise ValueError("segments must be pairwise disjoint and non-touching")
        self.segments = tuple(normalised)
        self._endpoint_segments: dict[float, set[int]] = {}
        for sid, (a, b) in enumerate(self.segments):
            self._endpoint_segments.setdefault(a[0], set()).add(sid)
            self._endpoint_segments.setdefault(b[0], set()).add(sid)
        order = list(range(len(normalised)))
        Random(seed).shuffle(order)
        self.insertion_order = tuple(order)
        # Rebuild after each random insertion. This is intentionally a
        # transparent reference update, not the optimal local-update method.
        inserted: list[int] = []
        self.insertion_rebuild_sizes = []
        self.insertion_corridors: list[tuple[Trapezoid, ...]] = []
        self.insertion_splits: list[tuple[CorridorSplit, ...]] = []
        for sid in order:
            self._build(tuple(inserted))
            corridor = self._trace_segment_corridor(sid)
            self.insertion_corridors.append(tuple(corridor))
            self.insertion_splits.append(tuple(
                self._split_corridor_cell(sid, cell) for cell in corridor
            ))
            inserted.append(sid)
            self.insertion_rebuild_sizes.append(len(self.trapezoids))
        self._build(tuple(order))

    def _trace_segment_corridor(self, segment_id: int) -> list[Trapezoid]:
        """Walk right-neighbor links through the cells crossed by a new segment.

        The segment starts strictly inside one existing slab because endpoint
        x-coordinates are distinct. At each right wall its y-coordinate selects
        the unique adjacent trapezoid containing that point. This follows the
        actual cell adjacency graph rather than rescanning every slab.
        """
        segment = self.segments[segment_id]
        x0, x1 = segment[0][0], segment[1][0]
        slab_index = bisect_left(self.x_events, x0)
        if slab_index == 0 or slab_index >= len(self.x_events):
            raise ValueError("segment endpoint is outside the existing slab domain")
        slab_index -= 1
        active, cells, _root = self.slabs[slab_index]
        start_y = _y_at(segment, x0)
        gap = sum(_y_at(self.segments[sid], x0) < start_y for sid in active)
        current = cells[gap]
        by_id = {cell.id: cell for cell in self.trapezoids}
        corridor = [current]
        visited = {current.id}

        while current.x_right < x1:
            wall = current.x_right
            probe_y = _y_at(segment, wall)
            candidates = []
            for neighbor_id in current.right_neighbors:
                neighbor = by_id[neighbor_id]
                bottom = (self.bounds[1] if neighbor.bottom_segment is None else
                          _y_at(self.segments[neighbor.bottom_segment], wall))
                top = (self.bounds[3] if neighbor.top_segment is None else
                       _y_at(self.segments[neighbor.top_segment], wall))
                if bottom < probe_y < top:
                    candidates.append(neighbor)
            if len(candidates) != 1:
                raise ValueError(
                    "corridor walk expected one adjacent trapezoid at each vertical wall"
                )
            current = candidates[0]
            if current.id in visited:
                raise ValueError("corridor adjacency contains a cycle")
            visited.add(current.id)
            corridor.append(current)
        return corridor

    def _split_corridor_cell(self, segment_id: int,
                             cell: Trapezoid) -> CorridorSplit:
        """Describe the two local cells replacing one crossed trapezoid."""
        segment = self.segments[segment_id]
        left = max(cell.x_left, segment[0][0])
        right = min(cell.x_right, segment[1][0])
        if not left < right:
            raise ValueError("segment does not cross the supplied trapezoid")
        lower = Trapezoid(
            (segment_id, cell.id[0], cell.id[1], 0), left, right,
            cell.bottom_segment, segment_id,
        )
        upper = Trapezoid(
            (segment_id, cell.id[0], cell.id[1], 1), left, right,
            segment_id, cell.top_segment,
        )
        return CorridorSplit(cell, lower, upper)

    def _build(self, segment_ids: tuple[int, ...]) -> None:
        xmin, ymin, xmax, ymax = self.bounds
        self.x_events = tuple(sorted(
            {xmin, xmax} |
            {x for sid in segment_ids for x in
             (self.segments[sid][0][0], self.segments[sid][1][0])}
        ))
        slab_inputs = []
        for left, right in zip(self.x_events, self.x_events[1:]):
            mid = (left+right)/2
            active = [sid for sid in segment_ids
                      if self.segments[sid][0][0] < mid < self.segments[sid][1][0]]
            active.sort(key=lambda sid: _y_at(self.segments[sid], mid))
            slab_inputs.append((left, right, mid, active))

        # Consecutive slab intervals with the same upper/lower segment pair
        # are one trapezoid. This lets endpoint walls stop at the first
        # segment they encounter instead of extending through the whole map.
        self.slabs = []
        self.trapezoids = []
        previous: dict[tuple[int | None, int | None], Trapezoid] = {}
        self._y_node_cache = {}
        for slab_index, (left, right, mid, active) in enumerate(slab_inputs):
            cells = []
            current = {}
            for gap in range(len(active)+1):
                bottom = active[gap-1] if gap else None
                top = active[gap] if gap < len(active) else None
                pair = (bottom, top)
                if pair in previous:
                    cell = previous[pair]
                    cell.x_right = right
                else:
                    cell = Trapezoid((slab_index, gap), left, right, bottom, top)
                    self.trapezoids.append(cell)
                cells.append(cell)
                current[pair] = cell
            root = self._build_y_tree(active, cells, mid)
            self.slabs.append((tuple(active), tuple(cells), root))
            previous = current
        self._link_trapezoid_neighbors()
        self._x_root = self._build_x_tree(0, len(self.slabs))

    def _link_trapezoid_neighbors(self) -> None:
        """Build reciprocal adjacency across shared vertical trapezoid sides."""
        xmin, ymin, xmax, ymax = self.bounds
        ending: dict[float, list[Trapezoid]] = {}
        starting: dict[float, list[Trapezoid]] = {}
        for cell in self.trapezoids:
            ending.setdefault(cell.x_right, []).append(cell)
            starting.setdefault(cell.x_left, []).append(cell)
        left_links = {cell.id: set() for cell in self.trapezoids}
        right_links = {cell.id: set() for cell in self.trapezoids}

        def vertical_interval(cell: Trapezoid, x: float) -> tuple[float, float]:
            bottom = (ymin if cell.bottom_segment is None else
                      _y_at(self.segments[cell.bottom_segment], x))
            top = (ymax if cell.top_segment is None else
                   _y_at(self.segments[cell.top_segment], x))
            return bottom, top

        for wall in ending.keys() & starting.keys():
            for left_cell in ending[wall]:
                left_bottom, left_top = vertical_interval(left_cell, wall)
                for right_cell in starting[wall]:
                    right_bottom, right_top = vertical_interval(right_cell, wall)
                    if max(left_bottom, right_bottom) < min(left_top, right_top):
                        right_links[left_cell.id].add(right_cell.id)
                        left_links[right_cell.id].add(left_cell.id)
        for cell in self.trapezoids:
            cell.left_neighbors = tuple(sorted(left_links[cell.id]))
            cell.right_neighbors = tuple(sorted(right_links[cell.id]))

    def _build_y_tree(self, active: list[int], cells: list[Trapezoid],
                      mid: float):
        def build(lo: int, hi: int):
            if lo == hi:
                return cells[lo]
            split = (lo+hi)//2
            sid = active[split]
            left = build(lo, split)
            right = build(split+1, hi)
            key = (sid, id(left), id(right))
            node = self._y_node_cache.get(key)
            if node is None:
                node = _YNode(sid, left, right)
                self._y_node_cache[key] = node
            return node
        return build(0, len(active))

    def _build_x_tree(self, lo: int, hi: int):
        if hi-lo == 1:
            active, cells, root = self.slabs[lo]
            return (root, active)
        mid = (lo+hi)//2
        return _XNode(self.x_events[mid],
                      self._build_x_tree(lo, mid),
                      self._build_x_tree(mid, hi))

    def locate(self, x: float, y: float):
        x, y = float(x), float(y)
        if not (isfinite(x) and isfinite(y)):
            raise ValueError("query coordinates must be finite")
        xmin, ymin, xmax, ymax = self.bounds
        if x < xmin or x > xmax or y < ymin or y > ymax:
            return None
        # Deterministic right-side convention on artificial vertical walls.
        node = self._x_root
        while isinstance(node, _XNode):
            node = node.left if x < node.split_x else node.right
        node, _active = node
        event_pos = bisect_left(self.x_events, x)
        p = (x, y)
        for pos in (event_pos-1, event_pos):
            if 0 <= pos < len(self.x_events) and abs(self.x_events[pos]-x) <= self.epsilon:
                if any(_on_segment(p, *self.segments[sid], self.epsilon)
                       for sid in self._endpoint_segments.get(self.x_events[pos], ())):
                    return BOUNDARY
        while isinstance(node, _YNode):
            edge_y = _y_at(self.segments[node.segment_id], x)
            if abs(y-edge_y) <= self.epsilon:
                return BOUNDARY
            node = node.left if y < edge_y else node.right
        return node

    @property
    def search_node_count(self) -> int:
        seen = set()
        def count_y(node):
            key = id(node)
            if key in seen:
                return 0
            seen.add(key)
            if isinstance(node, Trapezoid):
                return 1
            return 1 + count_y(node.left) + count_y(node.right)
        total = sum(count_y(root) for _active, _cells, root in self.slabs)
        def count_x(node):
            if not isinstance(node, _XNode):
                return 0
            return 1 + count_x(node.left) + count_x(node.right)
        return total + count_x(self._x_root)

"""Randomized trapezoidal decomposition with a persistent history-DAG prototype.

The bounded input contract is pairwise disjoint, non-vertical segments in
general position. Insertions follow a seeded random permutation. A persistent
trapezoid-cell graph and search-history DAG are updated by corridor replacement.
Public queries traverse the persistent history DAG; a rebuilt slab decomposition
is retained as an independent reference oracle. The prototype recomputes neighbor
links globally and does not claim Seidel's expected construction bound.

The public locate() query uses the persistent history DAG; the private _locate_slab() method remains the independently rebuilt differential oracle.
Original segment boundaries return BOUNDARY; outside points return None.
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
class CorridorReplacement:
    """Persistent cell-graph replacement record for one segment insertion."""
    segment_id: int
    removed_cell_ids: tuple[tuple[int, ...], ...]
    added_cells: tuple[Trapezoid, ...]
    lower_chains: tuple[tuple[tuple[int, ...], ...], ...]
    upper_chains: tuple[tuple[tuple[int, ...], ...], ...]


@dataclass(frozen=True)
class _HistoryLeaf:
    cell: Trapezoid


@dataclass(frozen=True)
class _HistoryYNode:
    segment_id: int
    below: "_HistoryNode"
    above: "_HistoryNode"


@dataclass(frozen=True)
class _HistoryXNode:
    split_x: float
    left: "_HistoryNode"
    right: "_HistoryNode"


_HistoryNode = _HistoryLeaf | _HistoryYNode | _HistoryXNode


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

    The implementation maintains a corridor-replaced cell graph and a
    persistent history DAG, while rebuilding a static slab locator as a
    differential reference. Public locate() queries traverse the history DAG;
    _locate_slab() is retained as the independent reference implementation.
    Neighbor maintenance is global per insertion, so optimized expected-time
    claims are not made.
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
        self.insertion_replacements: list[CorridorReplacement] = []
        self.replacement_graph_snapshots: list[tuple[Trapezoid, ...]] = []
        self._build(())
        self._persistent_cells: dict[tuple[int, ...], Trapezoid] = {
            cell.id: cell for cell in self.trapezoids
        }
        initial_cell = next(iter(self._persistent_cells.values()))
        self._history_root: _HistoryNode = _HistoryLeaf(initial_cell)
        for insertion_index, sid in enumerate(order):
            self._build(tuple(inserted))
            traced = self._trace_segment_corridor(sid)
            persistent_by_geometry = {
                (cell.x_left, cell.x_right, cell.bottom_segment, cell.top_segment): cell
                for cell in self._persistent_cells.values()
            }
            try:
                corridor = [
                    persistent_by_geometry[
                        (cell.x_left, cell.x_right, cell.bottom_segment, cell.top_segment)
                    ] for cell in traced
                ]
            except KeyError:
                raise ValueError(
                    "persistent trapezoid graph does not match rebuilt decomposition"
                ) from None
            self.insertion_corridors.append(tuple(corridor))
            self.insertion_splits.append(tuple(
                self._split_corridor_cell(sid, cell) for cell in corridor
            ))
            replacement = self._apply_corridor_replacement(
                insertion_index, sid, corridor
            )
            self.insertion_replacements.append(replacement)
            self._update_history_dag(insertion_index, sid, corridor, replacement)
            # Freeze an independent snapshot: later insertions refresh
            # neighbor links on surviving live cells.
            self.replacement_graph_snapshots.append(tuple(
                Trapezoid(
                    cell.id, cell.x_left, cell.x_right,
                    cell.bottom_segment, cell.top_segment,
                    tuple(cell.left_neighbors), tuple(cell.right_neighbors),
                )
                for cell in sorted(self._persistent_cells.values(), key=lambda item: item.id)
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

    def _apply_corridor_replacement(
        self, insertion_index: int, segment_id: int,
        corridor: list[Trapezoid],
    ) -> CorridorReplacement:
        """Replace crossed cells in a persistent decomposition snapshot.

        Endpoint cells retain their uncrossed left/right caps. Lower pieces
        with the same bottom boundary and upper pieces with the same top
        boundary are coalesced across consecutive corridor cells. This
        records a genuine local cell replacement; neighbor links are then
        re-derived for the snapshot, so adjacency maintenance is not yet
        asymptotically local and the point-location DAG is still rebuilt.
        """
        segment = self.segments[segment_id]
        x0, x1 = segment[0][0], segment[1][0]
        removed_ids = tuple(cell.id for cell in corridor)
        for cell_id in removed_ids:
            if cell_id not in self._persistent_cells:
                raise ValueError("corridor cell is absent from persistent map")
        added: list[Trapezoid] = []
        lower_fragments: list[Trapezoid] = []
        upper_fragments: list[Trapezoid] = []
        serial = 0

        def make(left, right, bottom, top):
            nonlocal serial
            cell = Trapezoid(
                (-1, insertion_index, serial), left, right, bottom, top
            )
            serial += 1
            added.append(cell)
            return cell

        for index, cell in enumerate(corridor):
            if index == 0 and cell.x_left < x0:
                make(cell.x_left, x0, cell.bottom_segment, cell.top_segment)
            left = max(cell.x_left, x0)
            right = min(cell.x_right, x1)
            if left < right:
                lower_fragments.append(make(
                    left, right, cell.bottom_segment, segment_id
                ))
                upper_fragments.append(make(
                    left, right, segment_id, cell.top_segment
                ))
            if index == len(corridor)-1 and x1 < cell.x_right:
                make(x1, cell.x_right, cell.bottom_segment, cell.top_segment)

        def coalesce(fragments, *, lower):
            chains = []
            current = []
            for fragment in fragments:
                boundary = fragment.bottom_segment if lower else fragment.top_segment
                previous_boundary = (
                    current[-1].bottom_segment if lower else current[-1].top_segment
                ) if current else object()
                if current and current[-1].x_right == fragment.x_left and boundary == previous_boundary:
                    current.append(fragment)
                else:
                    if current:
                        chains.append(current)
                    current = [fragment]
            if current:
                chains.append(current)
            merged_ids = []
            for chain in chains:
                if len(chain) == 1:
                    merged_ids.append((chain[0].id,))
                    continue
                first, last = chain[0], chain[-1]
                merged = make(
                    first.x_left, last.x_right,
                    first.bottom_segment, last.top_segment,
                )
                for fragment in chain:
                    added.remove(fragment)
                merged_ids.append((merged.id,))
            return tuple(merged_ids)

        lower_chains = coalesce(lower_fragments, lower=True)
        upper_chains = coalesce(upper_fragments, lower=False)
        for cell_id in removed_ids:
            del self._persistent_cells[cell_id]
        for cell in added:
            self._persistent_cells[cell.id] = cell
        self._assign_neighbor_links(list(self._persistent_cells.values()))
        return CorridorReplacement(
            segment_id, removed_ids, tuple(added), lower_chains, upper_chains
        )

    def _update_history_dag(
        self, insertion_index: int, segment_id: int,
        corridor: list[Trapezoid], replacement: CorridorReplacement,
    ) -> None:
        """Replace old trapezoid leaves with endpoint and segment decisions."""
        segment = self.segments[segment_id]
        x0, x1 = segment[0][0], segment[1][0]
        added = replacement.added_cells
        substitutions = {}

        for index, old_cell in enumerate(corridor):
            left = max(old_cell.x_left, x0)
            right = min(old_cell.x_right, x1)
            lower = next((cell for cell in added
                          if cell.bottom_segment == old_cell.bottom_segment
                          and cell.top_segment == segment_id
                          and cell.x_left <= left and cell.x_right >= right), None)
            upper = next((cell for cell in added
                          if cell.bottom_segment == segment_id
                          and cell.top_segment == old_cell.top_segment
                          and cell.x_left <= left and cell.x_right >= right), None)
            if lower is None or upper is None:
                raise ValueError("replacement graph is missing a lower or upper search leaf")
            subtree: _HistoryNode = _HistoryYNode(
                segment_id, _HistoryLeaf(lower), _HistoryLeaf(upper)
            )
            if index == 0:
                cap = next((cell for cell in added
                            if cell.x_left == old_cell.x_left and cell.x_right == x0
                            and cell.bottom_segment == old_cell.bottom_segment
                            and cell.top_segment == old_cell.top_segment), None)
                if cap is None:
                    raise ValueError("left endpoint cap is missing from replacement")
                subtree = _HistoryXNode(x0, _HistoryLeaf(cap), subtree)
            if index == len(corridor)-1:
                cap = next((cell for cell in added
                            if cell.x_left == x1 and cell.x_right == old_cell.x_right
                            and cell.bottom_segment == old_cell.bottom_segment
                            and cell.top_segment == old_cell.top_segment), None)
                if cap is None:
                    raise ValueError("right endpoint cap is missing from replacement")
                subtree = _HistoryXNode(x1, subtree, _HistoryLeaf(cap))
            substitutions[old_cell.id] = subtree

        memo = {}
        def replace(node: _HistoryNode) -> _HistoryNode:
            key = id(node)
            if key in memo:
                return memo[key]
            if isinstance(node, _HistoryLeaf):
                result = substitutions.get(node.cell.id, node)
            elif isinstance(node, _HistoryYNode):
                below, above = replace(node.below), replace(node.above)
                result = (node if below is node.below and above is node.above
                          else _HistoryYNode(node.segment_id, below, above))
            else:
                left, right = replace(node.left), replace(node.right)
                result = (node if left is node.left and right is node.right
                          else _HistoryXNode(node.split_x, left, right))
            memo[key] = result
            return result
        self._history_root = replace(self._history_root)

    def _locate_history(self, x: float, y: float):
        """Query the persistent insertion history DAG (right-side x convention)."""
        x, y = float(x), float(y)
        if not (isfinite(x) and isfinite(y)):
            raise ValueError("query coordinates must be finite")
        xmin, ymin, xmax, ymax = self.bounds
        if x < xmin or x > xmax or y < ymin or y > ymax:
            return None
        event_pos = bisect_left(self.x_events, x)
        point = (x, y)
        for pos in (event_pos-1, event_pos):
            if 0 <= pos < len(self.x_events) and abs(self.x_events[pos]-x) <= self.epsilon:
                if any(_on_segment(point, *self.segments[sid], self.epsilon)
                       for sid in self._endpoint_segments.get(self.x_events[pos], ())):
                    return BOUNDARY
        node = self._history_root
        while not isinstance(node, _HistoryLeaf):
            if isinstance(node, _HistoryXNode):
                node = node.left if x < node.split_x else node.right
            else:
                edge_y = _y_at(self.segments[node.segment_id], x)
                if abs(y-edge_y) <= self.epsilon:
                    return BOUNDARY
                node = node.below if y < edge_y else node.above
        return node.cell

    @property
    def history_node_count(self) -> int:
        seen = set()
        def visit(node):
            if id(node) in seen:
                return 0
            seen.add(id(node))
            if isinstance(node, _HistoryLeaf):
                return 1
            if isinstance(node, _HistoryXNode):
                return 1 + visit(node.left) + visit(node.right)
            return 1 + visit(node.below) + visit(node.above)
        return visit(self._history_root)

    def _assign_neighbor_links(self, cells: list[Trapezoid]) -> None:
        """Assign reciprocal links for a trapezoid graph snapshot."""
        xmin, ymin, xmax, ymax = self.bounds
        ending: dict[float, list[Trapezoid]] = {}
        starting: dict[float, list[Trapezoid]] = {}
        for cell in cells:
            ending.setdefault(cell.x_right, []).append(cell)
            starting.setdefault(cell.x_left, []).append(cell)
        left_links = {cell.id: set() for cell in cells}
        right_links = {cell.id: set() for cell in cells}

        def interval(cell, x):
            bottom = ymin if cell.bottom_segment is None else _y_at(
                self.segments[cell.bottom_segment], x
            )
            top = ymax if cell.top_segment is None else _y_at(
                self.segments[cell.top_segment], x
            )
            return bottom, top

        for wall in ending.keys() & starting.keys():
            for left in ending[wall]:
                lb, lt = interval(left, wall)
                for right in starting[wall]:
                    rb, rt = interval(right, wall)
                    if max(lb, rb) < min(lt, rt):
                        right_links[left.id].add(right.id)
                        left_links[right.id].add(left.id)
        for cell in cells:
            cell.left_neighbors = tuple(sorted(left_links[cell.id]))
            cell.right_neighbors = tuple(sorted(right_links[cell.id]))

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
        self._assign_neighbor_links(self.trapezoids)

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

    def _locate_slab(self, x: float, y: float):
        """Independent static-slab reference query."""
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

    def locate(self, x: float, y: float):
        """Locate a point by traversing the persistent randomized history DAG."""
        return self._locate_history(x, y)

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

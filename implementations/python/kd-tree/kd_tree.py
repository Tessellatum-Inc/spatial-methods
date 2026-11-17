"""A small static 2D k-d tree for exact Euclidean nearest-neighbour search.

The implementation returns the original input index and squared distance.
It is a teaching implementation, not a dynamic or high-dimensional index.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, TypeAlias

Point: TypeAlias = tuple[float, float]


@dataclass(frozen=True)
class _Node:
    index: int
    point: Point
    axis: int
    left: _Node | None
    right: _Node | None


def _point(value: Iterable[float]) -> Point:
    coords = tuple(float(v) for v in value)
    if len(coords) != 2:
        raise ValueError("each point must contain exactly two coordinates")
    if not all(isfinite(v) for v in coords):
        raise ValueError("point coordinates must be finite")
    return coords[0], coords[1]


def _build(items: list[tuple[int, Point]]) -> _Node | None:
    if not items:
        return None

    min_x = min(point[0] for _, point in items)
    max_x = max(point[0] for _, point in items)
    min_y = min(point[1] for _, point in items)
    max_y = max(point[1] for _, point in items)
    axis = 0 if max_x - min_x >= max_y - min_y else 1

    items.sort(key=lambda item: (item[1][axis], item[0]))
    middle = len(items) // 2
    index, point = items[middle]

    return _Node(
        index=index,
        point=point,
        axis=axis,
        left=_build(items[:middle]),
        right=_build(items[middle + 1 :]),
    )


class KDTree2D:
    """Static 2D k-d tree with exact nearest-neighbour queries.

    Ties are resolved by the smallest original input index. The metric is
    planar Euclidean distance in the coordinate units supplied by the caller.
    """

    def __init__(self, points: Iterable[Iterable[float]]) -> None:
        self._points = tuple(_point(point) for point in points)
        items = list(enumerate(self._points))
        self._root = _build(items)

    def __len__(self) -> int:
        return len(self._points)

    def nearest(self, query: Iterable[float]) -> tuple[int, float] | None:
        """Return (original_index, squared_distance), or None for an empty tree."""
        qx, qy = _point(query)
        if self._root is None:
            return None

        best: tuple[float, int] | None = None

        def visit(node: _Node | None) -> None:
            nonlocal best
            if node is None:
                return

            dx = qx - node.point[0]
            dy = qy - node.point[1]
            distance_sq = dx * dx + dy * dy
            candidate = (distance_sq, node.index)
            if best is None or candidate < best:
                best = candidate

            query_coordinate = (qx, qy)[node.axis]
            delta = query_coordinate - node.point[node.axis]
            near, far = (
                (node.left, node.right) if delta <= 0
                else (node.right, node.left)
            )
            visit(near)

            # The split plane is a lower bound for every point in the far
            # subtree. Equality is visited so a lower-index tie can be found.
            if best is None or delta * delta <= best[0]:
                visit(far)

        visit(self._root)
        assert best is not None
        return best[1], best[0]

    def range_query(
        self, minimum: Iterable[float], maximum: Iterable[float]
    ) -> list[int]:
        """Return original indices inside an inclusive axis-aligned rectangle.

        The rectangle is defined by its lower-left and upper-right corners.
        Results are sorted by original input index, independent of tree shape.
        Split-plane tests are inclusive because equal split coordinates may
        occur in either subtree under the deterministic median partition.
        """
        low_x, low_y = _point(minimum)
        high_x, high_y = _point(maximum)
        if low_x > high_x or low_y > high_y:
            raise ValueError("minimum corner must not exceed maximum corner")

        found: list[int] = []

        def visit(node: _Node | None) -> None:
            if node is None:
                return
            x, y = node.point
            if low_x <= x <= high_x and low_y <= y <= high_y:
                found.append(node.index)

            split = node.point[node.axis]
            lower = (low_x, low_y)[node.axis]
            upper = (high_x, high_y)[node.axis]
            if lower <= split:
                visit(node.left)
            if upper >= split:
                visit(node.right)

        visit(self._root)
        return sorted(found)

    def radius_query(
        self, query: Iterable[float], radius: float
    ) -> list[int]:
        """Return original indices at distance <= radius from query.

        The radius boundary is inclusive. Split-plane pruning visits a far
        subtree whenever its minimum possible squared distance is <= r².
        Results are sorted by original input index.
        """
        qx, qy = _point(query)
        if isinstance(radius, bool):
            raise ValueError("radius must be finite and non-negative")
        try:
            limit = float(radius)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("radius must be finite and non-negative") from exc
        if not isfinite(limit) or limit < 0.0:
            raise ValueError("radius must be finite and non-negative")
        radius_sq = limit * limit
        found: list[int] = []

        def visit(node: _Node | None) -> None:
            if node is None:
                return
            dx = qx - node.point[0]
            dy = qy - node.point[1]
            if dx * dx + dy * dy <= radius_sq:
                found.append(node.index)

            delta = (qx, qy)[node.axis] - node.point[node.axis]
            near, far = ((node.left, node.right) if delta <= 0
                         else (node.right, node.left))
            visit(near)
            if delta * delta <= radius_sq:
                visit(far)

        visit(self._root)
        return sorted(found)

    def k_nearest(
        self, query: Iterable[float], k: int
    ) -> list[tuple[int, float]]:
        """Return up to k nearest (original_index, squared_distance) pairs.

        Results are sorted by (squared distance, original index). A bounded
        max-heap stores the current k best candidates; split-plane pruning is
        performed against the current kth-best squared distance.
        """
        import heapq

        qx, qy = _point(query)
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise ValueError("k must be a non-negative integer")
        if k == 0 or self._root is None:
            return []
        limit = min(k, len(self._points))
        # Negated keys make heap[0] the worst retained (largest distance,
        # then largest input index) candidate.
        heap: list[tuple[float, int, int]] = []

        def visit(node: _Node | None) -> None:
            if node is None:
                return
            dx = qx - node.point[0]
            dy = qy - node.point[1]
            distance_sq = dx * dx + dy * dy
            candidate = (-distance_sq, -node.index, node.index)
            if len(heap) < limit:
                heapq.heappush(heap, candidate)
            else:
                worst_distance = -heap[0][0]
                worst_index = -heap[0][1]
                if (distance_sq, node.index) < (worst_distance, worst_index):
                    heapq.heapreplace(heap, candidate)

            delta = (qx, qy)[node.axis] - node.point[node.axis]
            near, far = ((node.left, node.right) if delta <= 0
                         else (node.right, node.left))
            visit(near)
            if len(heap) < limit or delta * delta <= -heap[0][0]:
                visit(far)

        visit(self._root)
        return sorted(
            ((index, -neg_distance) for neg_distance, _neg_index, index in heap),
            key=lambda item: (item[1], item[0]),
        )



@dataclass
class _DynamicNode:
    index: int
    point: Point
    axis: int
    left: _DynamicNode | None = None
    right: _DynamicNode | None = None
    active: bool = True
    size: int = 1
    active_count: int = 1


def _dynamic_refresh(node: _DynamicNode) -> None:
    node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)
    node.active_count = int(node.active) + (node.left.active_count if node.left else 0) + (node.right.active_count if node.right else 0)


def _dynamic_collect(node: _DynamicNode | None, items: list[tuple[int, Point]]) -> None:
    if node is None:
        return
    if node.active:
        items.append((node.index, node.point))
    _dynamic_collect(node.left, items)
    _dynamic_collect(node.right, items)


def _dynamic_build(items: list[tuple[int, Point]]) -> _DynamicNode | None:
    if not items:
        return None
    min_x = min(point[0] for _, point in items)
    max_x = max(point[0] for _, point in items)
    min_y = min(point[1] for _, point in items)
    max_y = max(point[1] for _, point in items)
    axis = 0 if max_x - min_x >= max_y - min_y else 1
    items.sort(key=lambda item: (item[1][axis], item[0]))
    middle = len(items) // 2
    index, point = items[middle]
    node = _DynamicNode(
        index=index, point=point, axis=axis,
        left=_dynamic_build(items[:middle]),
        right=_dynamic_build(items[middle + 1:]),
    )
    _dynamic_refresh(node)
    return node


class DynamicKDTree2D:
    """Scapegoat-style dynamic 2D k-d tree with stable insertion IDs.

    Insertions rebuild an imbalanced subtree. Deletions are lazy and trigger
    rebuilding when the inactive fraction exceeds 1-alpha. All query results
    use stable IDs; duplicate coordinates are allowed and ties use the lower ID.
    """

    def __init__(self, points: Iterable[Iterable[float]] = (), *, alpha: float = 0.75) -> None:
        try:
            alpha = float(alpha)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("alpha must be finite and in (0.5, 1)") from exc
        if not isfinite(alpha) or not 0.5 < alpha < 1.0:
            raise ValueError("alpha must be finite and in (0.5, 1)")
        self.alpha = alpha
        self._root: _DynamicNode | None = None
        self._points: dict[int, Point] = {}
        self._next_id = 0
        for point in points:
            self.insert(point)

    def __len__(self) -> int:
        return len(self._points)

    def _rebuild(self, node: _DynamicNode) -> _DynamicNode | None:
        items: list[tuple[int, Point]] = []
        _dynamic_collect(node, items)
        return _dynamic_build(items)

    def _needs_rebuild(self, node: _DynamicNode) -> bool:
        left_size = node.left.size if node.left else 0
        right_size = node.right.size if node.right else 0
        return (
            max(left_size, right_size) > self.alpha * node.size
            or node.active_count < self.alpha * node.size
        )

    def insert(self, value: Iterable[float]) -> int:
        point = _point(value)
        index = self._next_id
        self._next_id += 1
        self._points[index] = point

        def add(node: _DynamicNode | None) -> _DynamicNode:
            if node is None:
                return _DynamicNode(index=index, point=point, axis=0)
            key = (point[node.axis], index)
            node_key = (node.point[node.axis], node.index)
            if key < node_key:
                node.left = add(node.left)
            else:
                node.right = add(node.right)
            _dynamic_refresh(node)
            if self._needs_rebuild(node):
                rebuilt = self._rebuild(node)
                assert rebuilt is not None
                return rebuilt
            return node

        self._root = add(self._root)
        return index

    def delete(self, index: int) -> bool:
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("index must be an integer insertion ID")
        point = self._points.get(index)
        if point is None:
            return False

        def remove(node: _DynamicNode | None) -> tuple[_DynamicNode | None, bool]:
            if node is None:
                return None, False
            key = (point[node.axis], index)
            node_key = (node.point[node.axis], node.index)
            if node.index == index:
                node.active = False
            elif key < node_key:
                node.left, _ = remove(node.left)
            else:
                node.right, _ = remove(node.right)
            _dynamic_refresh(node)
            if node.active_count == 0:
                return None, True
            if self._needs_rebuild(node):
                return self._rebuild(node), True
            return node, True

        self._root, removed = remove(self._root)
        if removed:
            del self._points[index]
        return removed

    def nearest(self, query: Iterable[float]) -> tuple[int, float] | None:
        qx, qy = _point(query)
        best: tuple[float, int] | None = None

        def visit(node: _DynamicNode | None) -> None:
            nonlocal best
            if node is None:
                return
            if node.active:
                dx, dy = qx - node.point[0], qy - node.point[1]
                candidate = (dx * dx + dy * dy, node.index)
                if best is None or candidate < best:
                    best = candidate
            delta = (qx, qy)[node.axis] - node.point[node.axis]
            near, far = ((node.left, node.right) if delta <= 0
                         else (node.right, node.left))
            visit(near)
            if best is None or delta * delta <= best[0]:
                visit(far)

        visit(self._root)
        return None if best is None else (best[1], best[0])

    def range_query(self, minimum: Iterable[float], maximum: Iterable[float]) -> list[int]:
        low_x, low_y = _point(minimum)
        high_x, high_y = _point(maximum)
        if low_x > high_x or low_y > high_y:
            raise ValueError("minimum corner must not exceed maximum corner")
        found = []

        def visit(node: _DynamicNode | None) -> None:
            if node is None:
                return
            x, y = node.point
            if node.active and low_x <= x <= high_x and low_y <= y <= high_y:
                found.append(node.index)
            split = node.point[node.axis]
            if (low_x, low_y)[node.axis] <= split:
                visit(node.left)
            if (high_x, high_y)[node.axis] >= split:
                visit(node.right)

        visit(self._root)
        return sorted(found)

    def radius_query(self, query: Iterable[float], radius: float) -> list[int]:
        qx, qy = _point(query)
        if isinstance(radius, bool):
            raise ValueError("radius must be finite and non-negative")
        try:
            limit = float(radius)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("radius must be finite and non-negative") from exc
        if not isfinite(limit) or limit < 0:
            raise ValueError("radius must be finite and non-negative")
        radius_sq = limit * limit
        found = []

        def visit(node: _DynamicNode | None) -> None:
            if node is None:
                return
            if node.active:
                dx, dy = qx - node.point[0], qy - node.point[1]
                if dx * dx + dy * dy <= radius_sq:
                    found.append(node.index)
            delta = (qx, qy)[node.axis] - node.point[node.axis]
            near, far = ((node.left, node.right) if delta <= 0
                         else (node.right, node.left))
            visit(near)
            if delta * delta <= radius_sq:
                visit(far)

        visit(self._root)
        return sorted(found)

    def k_nearest(self, query: Iterable[float], k: int) -> list[tuple[int, float]]:
        import heapq
        qx, qy = _point(query)
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise ValueError("k must be a non-negative integer")
        if k == 0 or self._root is None:
            return []
        heap: list[tuple[float, int, int]] = []

        def visit(node: _DynamicNode | None) -> None:
            if node is None:
                return
            if node.active:
                dx, dy = qx - node.point[0], qy - node.point[1]
                distance_sq = dx * dx + dy * dy
                candidate = (-distance_sq, -node.index, node.index)
                if len(heap) < k:
                    heapq.heappush(heap, candidate)
                elif (distance_sq, node.index) < (-heap[0][0], -heap[0][1]):
                    heapq.heapreplace(heap, candidate)
            delta = (qx, qy)[node.axis] - node.point[node.axis]
            near, far = ((node.left, node.right) if delta <= 0
                         else (node.right, node.left))
            visit(near)
            if len(heap) < k or delta * delta <= -heap[0][0]:
                visit(far)

        visit(self._root)
        return sorted(((i, -d) for d, _i, i in heap), key=lambda item: (item[1], item[0]))

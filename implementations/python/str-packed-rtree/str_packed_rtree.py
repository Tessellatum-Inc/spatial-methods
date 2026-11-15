"""A small immutable STR-packed R-tree for axis-aligned 2D bounding boxes.

The tree returns envelope-intersection candidates. For non-rectangular
geometries, refine candidates with the exact geometric predicate.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, hypot, isfinite, sqrt
from typing import Iterable, TypeAlias

Bounds: TypeAlias = tuple[float, float, float, float]


@dataclass(frozen=True)
class _Entry:
    index: int
    bounds: Bounds


@dataclass(frozen=True)
class _Node:
    bounds: Bounds
    children: tuple[_Entry | _Node, ...]
    leaf: bool


def _validate_bounds(bounds: Iterable[float]) -> Bounds:
    values = tuple(float(value) for value in bounds)
    if len(values) != 4:
        raise ValueError("bounds must contain minx, miny, maxx, maxy")
    minx, miny, maxx, maxy = values
    if not all(isfinite(value) for value in values):
        raise ValueError("bounds must contain only finite coordinates")
    if minx > maxx or miny > maxy:
        raise ValueError("minimum coordinates must not exceed maximum coordinates")
    return minx, miny, maxx, maxy


def _union_bounds(items: tuple[_Entry | _Node, ...]) -> Bounds:
    return (
        min(item.bounds[0] for item in items),
        min(item.bounds[1] for item in items),
        max(item.bounds[2] for item in items),
        max(item.bounds[3] for item in items),
    )


def _center_x(item: _Entry | _Node) -> float:
    return (item.bounds[0] + item.bounds[2]) / 2


def _center_y(item: _Entry | _Node) -> float:
    return (item.bounds[1] + item.bounds[3]) / 2


def _pack(items: list[_Entry] | list[_Node], capacity: int, leaf: bool) -> list[_Node]:
    """Pack one tree level using Sort-Tile-Recursive ordering."""
    if not items:
        return []

    node_count = ceil(len(items) / capacity)
    slice_count = ceil(sqrt(node_count))
    slice_size = ceil(len(items) / slice_count)

    ordered = sorted(items, key=lambda item: (_center_x(item), _center_y(item)))
    nodes: list[_Node] = []

    for start in range(0, len(ordered), slice_size):
        tile = ordered[start : start + slice_size]
        tile.sort(key=lambda item: (_center_y(item), _center_x(item)))
        for group_start in range(0, len(tile), capacity):
            children = tuple(tile[group_start : group_start + capacity])
            nodes.append(_Node(_union_bounds(children), children, leaf))

    return nodes


def _intersects(a: Bounds, b: Bounds) -> bool:
    """Return True when two closed axis-aligned boxes intersect or touch."""
    return not (
        a[2] < b[0]
        or b[2] < a[0]
        or a[3] < b[1]
        or b[3] < a[1]
    )


class STRPackedRTree:
    """Build-once STR-packed R-tree over a sequence of 2D bounding boxes.

    The returned query indices refer to the original input order.
    The index is immutable after construction.
    """

    def __init__(self, bounds: Iterable[Iterable[float]], node_capacity: int = 10):
        if not isinstance(node_capacity, int) or node_capacity < 2:
            raise ValueError("node_capacity must be an integer of at least 2")

        self.node_capacity = node_capacity
        self._bounds = tuple(_validate_bounds(item) for item in bounds)
        entries = [_Entry(index, item) for index, item in enumerate(self._bounds)]

        level = _pack(entries, node_capacity, leaf=True)
        while len(level) > 1:
            level = _pack(level, node_capacity, leaf=False)

        self._root = level[0] if level else None

    def query(self, bounds: Iterable[float]) -> list[int]:
        """Return sorted input indices whose stored bounding boxes intersect query bounds."""
        query_bounds = _validate_bounds(bounds)
        if self._root is None:
            return []

        matches: list[int] = []
        stack = [self._root]

        while stack:
            node = stack.pop()
            if not _intersects(node.bounds, query_bounds):
                continue

            if node.leaf:
                for child in node.children:
                    if _intersects(child.bounds, query_bounds):
                        matches.append(child.index)
            else:
                for child in node.children:
                    if _intersects(child.bounds, query_bounds):
                        if isinstance(child, _Node):
                            stack.append(child)

        return sorted(matches)

    def __len__(self) -> int:
        return len(self._bounds)


    def nearest(self, point: Iterable[float], k: int = 1) -> list[tuple[int, float]]:
        """Return k nearest boxes as (input_index, Euclidean_distance) pairs.

        Best-first branch-and-bound uses node-envelope distance as a lower
        bound. A bounded max-heap retains only the best k entries; equal
        distances are ordered by original input index.
        """
        from heapq import heappop, heappush, heapreplace
        coordinates = tuple(float(value) for value in point)
        if len(coordinates) != 2 or not all(isfinite(value) for value in coordinates):
            raise ValueError("point must contain two finite coordinates")
        if not isinstance(k, int) or isinstance(k, bool) or k < 0:
            raise ValueError("k must be a non-negative integer")
        if k == 0 or self._root is None:
            return []

        def distance_to_bounds(bounds: Bounds) -> float:
            x, y = coordinates
            dx = max(bounds[0] - x, 0.0, x - bounds[2])
            dy = max(bounds[1] - y, 0.0, y - bounds[3])
            return hypot(dx, dy)

        queue = []
        sequence = 0
        heappush(queue, (distance_to_bounds(self._root.bounds), sequence, self._root))
        # Negated keys make the root the worst retained (distance, index).
        best: list[tuple[float, int, int]] = []
        while queue:
            lower_bound, _order, item = heappop(queue)
            if len(best) == k and lower_bound > -best[0][0]:
                break
            if isinstance(item, _Entry):
                candidate = (-lower_bound, -item.index, item.index)
                if len(best) < k:
                    heappush(best, candidate)
                elif (lower_bound, item.index) < (-best[0][0], -best[0][1]):
                    heapreplace(best, candidate)
                continue
            for child in item.children:
                sequence += 1
                heappush(queue, (distance_to_bounds(child.bounds), sequence, child))

        ordered = sorted(((-distance, index) for distance, _neg_index, index in best),
                         key=lambda pair: (pair[0], pair[1]))
        return [(index, distance) for distance, index in ordered]

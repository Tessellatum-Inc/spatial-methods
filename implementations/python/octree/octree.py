"""Bucket point-region octree for exact 3D point queries.

The root box is closed. Mid-plane ties go to the high-side child on each
axis. Window queries are inclusive and return stable insertion IDs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from itertools import count
from math import dist, isfinite
from typing import Iterable, TypeAlias

Point3: TypeAlias = tuple[float, float, float]
Bounds3: TypeAlias = tuple[float, float, float, float, float, float]
Entry: TypeAlias = tuple[int, Point3]


def _point(value: Iterable[float], label: str = "point") -> Point3:
    coords = tuple(float(v) for v in value)
    if len(coords) != 3 or not all(isfinite(v) for v in coords):
        raise ValueError(f"{label} must contain exactly three finite coordinates")
    return coords  # type: ignore[return-value]


def _bounds(value: Iterable[float], label: str) -> Bounds3:
    c = tuple(float(v) for v in value)
    if len(c) != 6 or not all(isfinite(v) for v in c):
        raise ValueError(f"{label} must contain six finite values")
    if any(c[i] > c[i + 3] for i in range(3)):
        raise ValueError(f"{label} minimums must not exceed maximums")
    return c  # type: ignore[return-value]


@dataclass
class _Node:
    bounds: Bounds3
    depth: int
    entries: list[Entry] = field(default_factory=list)
    children: tuple["_Node", ...] | None = None


class PointRegionOctree:
    """Fixed-root bucket octree with insertion, lazy deletion, range and exact kNN.

    Deleted IDs remain reserved. Tombstones are periodically purged by a
    whole-tree rebuild. Points outside the root box are rejected; coincident
    points may remain in over-capacity leaves at max_depth or midpoint collapse.
    """
    def __init__(self, extent: Iterable[float], points: Iterable[Iterable[float]] = (),
                 *, capacity: int = 8, max_depth: int = 16) -> None:
        self.extent = _bounds(extent, "extent")
        if any(self.extent[i] == self.extent[i + 3] for i in range(3)):
            raise ValueError("extent must have positive width on all axes")
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 0:
            raise ValueError("max_depth must be a non-negative integer")
        self.capacity, self.max_depth = capacity, max_depth
        self._root = _Node(self.extent, 0)
        self._points: list[Point3] = []
        self._active: list[bool] = []
        self._active_count = 0
        self._tombstones = 0
        for p in points:
            self.insert(p)

    def __len__(self) -> int:
        return self._active_count

    def insert(self, value: Iterable[float]) -> int:
        p = _point(value)
        if not self._contains(self.extent, p):
            raise ValueError("point lies outside the root extent")
        idx = len(self._points)
        self._points.append(p)
        self._active.append(True)
        self._active_count += 1
        self._insert(self._root, (idx, p))
        return idx

    def delete(self, point_id: int) -> bool:
        """Lazily delete an insertion ID; periodically rebuild to purge tombstones."""
        if not isinstance(point_id, int) or isinstance(point_id, bool) or not 0 <= point_id < len(self._points):
            raise ValueError("point_id must be a valid insertion ID")
        if not self._active[point_id]:
            return False
        self._active[point_id] = False
        self._active_count -= 1
        self._tombstones += 1
        if (self._tombstones >= self.capacity
                and self._tombstones / len(self._points) >= 0.3):
            self.rebuild()
        return True

    def rebuild(self) -> None:
        """Rebuild the tree from active entries without changing stable IDs."""
        self._root = _Node(self.extent, 0)
        for idx, point in enumerate(self._points):
            if self._active[idx]:
                self._insert(self._root, (idx, point))
        self._tombstones = 0

    def query(self, window: Iterable[float]) -> list[int]:
        """Return IDs in insertion order for points inside an inclusive box."""
        b = _bounds(window, "window")
        found: list[int] = []
        self._query(self._root, b, found)
        found.sort()
        return found

    def query_points(self, window: Iterable[float]) -> list[Point3]:
        return [self._points[i] for i in self.query(window)]

    def k_nearest(self, query: Iterable[float], k: int) -> list[tuple[int, Point3, float]]:
        """Return (point_id, point, Euclidean distance), ordered by distance then ID."""
        q = _point(query, "query")
        if not isinstance(k, int) or isinstance(k, bool) or k < 1:
            raise ValueError("k must be a positive integer")
        if self._active_count == 0:
            return []
        # Min-heap of unexplored nodes, ordered by a lower bound on distance.
        serial = count()
        nodes = [(self._box_distance(q, self._root.bounds), next(serial), self._root)]
        # Max-heap of current answers: negative distance and negative ID.
        best: list[tuple[float, int, int]] = []
        while nodes:
            lower, _, node = heappop(nodes)
            if len(best) == k and lower > -best[0][0]:
                break
            if node.children is None:
                for idx, p in node.entries:
                    if not self._active[idx]:
                        continue
                    d = dist(q, p)
                    item = (-d, -idx, idx)
                    if len(best) < k:
                        heappush(best, item)
                    elif item > best[0]:
                        heappush(best, item)
                        heappop(best)
            else:
                for child in node.children:
                    bound = self._box_distance(q, child.bounds)
                    if len(best) < k or bound <= -best[0][0]:
                        heappush(nodes, (bound, next(serial), child))
        ids = [item[2] for item in best]
        ids.sort(key=lambda i: (dist(q, self._points[i]), i))
        return [(i, self._points[i], dist(q, self._points[i])) for i in ids]

    @staticmethod
    def _contains(b: Bounds3, p: Point3) -> bool:
        return all(b[i] <= p[i] <= b[i + 3] for i in range(3))

    @staticmethod
    def _intersects(a: Bounds3, b: Bounds3) -> bool:
        return all(not (a[i + 3] < b[i] or b[i + 3] < a[i]) for i in range(3))

    @staticmethod
    def _box_distance(p: Point3, b: Bounds3) -> float:
        delta = [max(b[i] - p[i], 0.0, p[i] - b[i + 3]) for i in range(3)]
        return dist((0.0, 0.0, 0.0), delta)

    @staticmethod
    def _midpoints(b: Bounds3) -> tuple[float, float, float] | None:
        m = tuple(b[i] + (b[i + 3] - b[i]) / 2 for i in range(3))
        if any(m[i] in (b[i], b[i + 3]) for i in range(3)):
            return None
        return m  # type: ignore[return-value]

    @classmethod
    def _child_index(cls, b: Bounds3, p: Point3) -> int:
        m = cls._midpoints(b)
        if m is None:
            raise RuntimeError("cannot subdivide a box without distinct midpoints")
        return sum((1 << axis) for axis in range(3) if p[axis] >= m[axis])

    @classmethod
    def _make_children(cls, b: Bounds3, depth: int) -> tuple[_Node, ...] | None:
        m = cls._midpoints(b)
        if m is None:
            return None
        children = []
        for octant in range(8):
            lo, hi = [], []
            for axis in range(3):
                if octant & (1 << axis):
                    lo.append(m[axis]); hi.append(b[axis + 3])
                else:
                    lo.append(b[axis]); hi.append(m[axis])
            children.append(_Node(tuple(lo + hi), depth))
        return tuple(children)

    def _insert(self, node: _Node, entry: Entry) -> None:
        if node.children is not None:
            self._insert(node.children[self._child_index(node.bounds, entry[1])], entry)
            return
        node.entries.append(entry)
        if len(node.entries) <= self.capacity or node.depth >= self.max_depth:
            return
        children = self._make_children(node.bounds, node.depth + 1)
        if children is None:
            return
        old, node.entries, node.children = node.entries, [], children
        for item in old:
            self._insert(node.children[self._child_index(node.bounds, item[1])], item)

    def _query(self, node: _Node, window: Bounds3, found: list[int]) -> None:
        if not self._intersects(node.bounds, window):
            return
        if node.children is None:
            found.extend(i for i, p in node.entries if self._active[i] and self._contains(window, p))
        else:
            for child in node.children:
                self._query(child, window, found)

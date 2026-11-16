"""Exact static 2D ball tree for Euclidean range and k-nearest queries."""
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappop, heappush
from math import fsum, hypot, isfinite, nextafter, inf
from typing import Sequence

Point = tuple[float, float]

def _point(value: Sequence[float]) -> Point:
    if len(value) != 2:
        raise ValueError("each point must contain x and y")
    x, y = float(value[0]), float(value[1])
    if not isfinite(x) or not isfinite(y):
        raise ValueError("coordinates must be finite")
    return x, y

@dataclass(slots=True)
class _Node:
    center: Point
    radius: float
    indices: list[int] | None = None
    left: "_Node | None" = None
    right: "_Node | None" = None

class BallTree2D:
    """Static Euclidean index with enclosing-ball branch-and-bound."""
    def __init__(self, points: Sequence[Sequence[float]], leaf_size: int = 12):
        if not isinstance(leaf_size, int) or isinstance(leaf_size, bool) or leaf_size < 1:
            raise ValueError("leaf_size must be a positive integer")
        self.points = [_point(point) for point in points]
        self.leaf_size = leaf_size
        self.root = self._build(list(range(len(self.points)))) if self.points else None

    def _build(self, indices: list[int]) -> _Node:
        cx = fsum(self.points[i][0] for i in indices) / len(indices)
        cy = fsum(self.points[i][1] for i in indices) / len(indices)
        center = (cx, cy)
        radius = nextafter(max(hypot(self.points[i][0] - cx, self.points[i][1] - cy)
                               for i in indices), inf)
        if len(indices) <= self.leaf_size:
            return _Node(center, radius, sorted(indices))
        xs = [self.points[i][0] for i in indices]
        ys = [self.points[i][1] for i in indices]
        axis = 0 if max(xs) - min(xs) >= max(ys) - min(ys) else 1
        ordered = sorted(indices, key=lambda i: (self.points[i][axis], i))
        middle = len(ordered) // 2
        return _Node(center, radius, None,
                     self._build(ordered[:middle]), self._build(ordered[middle:]))

    @staticmethod
    def _lower_bound(query: Point, node: _Node) -> float:
        distance = hypot(query[0] - node.center[0], query[1] - node.center[1])
        return max(0.0, nextafter(distance - node.radius, -inf))

    def query(self, point: Sequence[float], k: int = 1) -> list[tuple[int, float]]:
        """Return up to k exact nearest records as (input_index, distance)."""
        query = _point(point)
        if not isinstance(k, int) or isinstance(k, bool) or k < 1:
            raise ValueError("k must be a positive integer")
        if self.root is None:
            return []
        count = min(k, len(self.points))
        pending = []
        serial = 0
        heappush(pending, (self._lower_bound(query, self.root), serial, self.root))
        best: list[tuple[float, int, int]] = []
        while pending:
            lower, _, node = heappop(pending)
            if len(best) == count and lower > -best[0][0]:
                break
            if node.indices is not None:
                for index in node.indices:
                    px, py = self.points[index]
                    distance = hypot(px - query[0], py - query[1])
                    candidate = (-distance, -index, index)
                    if len(best) < count:
                        heappush(best, candidate)
                    elif (distance, index) < (-best[0][0], -best[0][1]):
                        heappop(best)
                        heappush(best, candidate)
            else:
                for child in (node.left, node.right):
                    if child is None:
                        continue
                    bound = self._lower_bound(query, child)
                    if len(best) < count or bound <= -best[0][0]:
                        serial += 1
                        heappush(pending, (bound, serial, child))
        return sorted(((i, -d) for d, _, i in best), key=lambda item: (item[1], item[0]))

    def query_radius(self, point: Sequence[float], radius: float) -> list[tuple[int, float]]:
        """Return all records within an inclusive Euclidean radius."""
        query = _point(point)
        if isinstance(radius, bool) or not isinstance(radius, (int, float)):
            raise ValueError("radius must be a finite non-negative number")
        radius = float(radius)
        if not isfinite(radius) or radius < 0:
            raise ValueError("radius must be a finite non-negative number")
        if self.root is None:
            return []
        found = []
        pending = [self.root]
        while pending:
            node = pending.pop()
            if self._lower_bound(query, node) > radius:
                continue
            if node.indices is not None:
                for index in node.indices:
                    px, py = self.points[index]
                    distance = hypot(px - query[0], py - query[1])
                    if distance <= radius:
                        found.append((index, distance))
            else:
                if node.left is not None:
                    pending.append(node.left)
                if node.right is not None:
                    pending.append(node.right)
        return sorted(found, key=lambda item: (item[1], item[0]))

    def __len__(self) -> int:
        return len(self.points)

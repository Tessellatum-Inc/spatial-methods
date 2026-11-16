"""Exact Euclidean vantage-point tree for static 2D point data."""
from __future__ import annotations

from dataclasses import dataclass
from heapq import heappush, heapreplace
from math import hypot, isfinite
from collections.abc import Sequence

Point = tuple[float, float]


def _point(value: Sequence[float], name: str) -> Point:
    if len(value) != 2:
        raise ValueError(f"{name} must be a 2D point")
    x, y = float(value[0]), float(value[1])
    if not isfinite(x) or not isfinite(y):
        raise ValueError(f"{name} coordinates must be finite")
    return x, y


@dataclass(frozen=True)
class _Node:
    point: Point
    index: int
    radius: float
    inner: _Node | None
    outer: _Node | None


class VantagePointTree:
    """Static VP-tree with exact Euclidean k-nearest-neighbour queries.

    Construction uses a balanced median split by distance from each vantage
    point. Query pruning uses the triangle inequality. The structure is
    immutable after construction and preserves duplicate input observations.
    """

    def __init__(self, points: Sequence[Sequence[float]]):
        self.points = tuple(_point(p, "point") for p in points)
        records = list(enumerate(self.points))
        self.root = self._build(records)

    @staticmethod
    def _build(records: list[tuple[int, Point]]) -> _Node | None:
        if not records:
            return None
        # Select the final record as vantage point; deterministic and cheap.
        index, vantage = records[-1]
        remaining = records[:-1]
        if not remaining:
            return _Node(vantage, index, 0.0, None, None)
        ranked = sorted(
            ((hypot(p[0] - vantage[0], p[1] - vantage[1]), i, p)
             for i, p in remaining),
            key=lambda item: (item[0], item[1]),
        )
        split = (len(ranked) + 1) // 2
        inner_records = [(i, p) for _, i, p in ranked[:split]]
        outer_records = [(i, p) for _, i, p in ranked[split:]]
        # The midpoint keeps every inner distance <= radius and every outer
        # distance >= radius. When the outer side is empty, use the largest
        # inner distance as the radius. Equality is explored on both sides.
        radius = (ranked[split - 1][0] if split == len(ranked) else
                  (ranked[split - 1][0] + ranked[split][0]) / 2.0)
        return _Node(
            vantage, index, radius,
            VantagePointTree._build(inner_records),
            VantagePointTree._build(outer_records),
        )

    def query(self, point: Sequence[float], k: int = 1) -> list[tuple[Point, float]]:
        """Return up to k nearest (point, distance) pairs, sorted nearest first.

        Equal-distance results retain input order. Query time is data-dependent;
        worst-case search is O(n), while balanced construction is O(n log² n).
        """
        target = _point(point, "query")
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        if self.root is None:
            return []
        heap: list[tuple[float, int, Point]] = []

        def visit(node: _Node | None) -> None:
            if node is None:
                return
            distance = hypot(target[0] - node.point[0],
                             target[1] - node.point[1])
            item = (-distance, -node.index, node.point)
            if len(heap) < k:
                heappush(heap, item)
            elif (distance, node.index) < (-heap[0][0], -heap[0][1]):
                heapreplace(heap, item)

            tau = -heap[0][0] if len(heap) == k else float("inf")
            if distance < node.radius:
                if distance - tau <= node.radius:
                    visit(node.inner)
                if distance + tau >= node.radius:
                    visit(node.outer)
            else:
                if distance + tau >= node.radius:
                    visit(node.outer)
                if distance - tau <= node.radius:
                    visit(node.inner)

        visit(self.root)
        ordered = sorted(
            ((-d, -i, p) for d, i, p in heap),
            key=lambda item: (item[0], item[1]),
        )
        return [(p, d) for d, _, p in ordered]

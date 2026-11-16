"""Mutable 2D R*-tree with overlap-aware insertion and forced reinsertion.

This is an in-memory teaching implementation for finite axis-aligned boxes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from itertools import count
from math import ceil, isfinite
from typing import Iterable

Bounds = tuple[float, float, float, float]


def _bounds(values: Iterable[float]) -> Bounds:
    b = tuple(float(v) for v in values)
    if len(b) != 4 or not all(isfinite(v) for v in b):
        raise ValueError("bounds must contain four finite values")
    if b[0] > b[2] or b[1] > b[3]:
        raise ValueError("minimum bounds must not exceed maximum bounds")
    return b


def _area(b):
    return (b[2] - b[0]) * (b[3] - b[1])


def _margin(b):
    return 2 * ((b[2] - b[0]) + (b[3] - b[1]))


def _union(a, b):
    return min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])


def _overlap(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0.0, min(a[3], b[3]) - max(a[1], b[1])
    )


def _center_distance_squared(a, b):
    ax, ay = (a[0] + a[2]) / 2.0, (a[1] + a[3]) / 2.0
    bx, by = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
    return (ax - bx) ** 2 + (ay - by) ** 2


@dataclass
class _Node:
    leaf: bool
    children: list = field(default_factory=list)
    parent: "_Node | None" = None
    bounds: Bounds | None = None


@dataclass(frozen=True)
class _Entry:
    index: int
    bounds: Bounds


class RStarTree:
    """Incremental in-memory R*-tree for planar 2D bounding boxes.

    Insertions use overlap-enlargement subtree selection near leaves,
    margin-based split-axis selection, overlap/area split distribution and
    forced reinsertion once per level during a top-level insertion.
    """

    def __init__(self, max_entries: int = 8, min_fill: float = 0.4):
        if not isinstance(max_entries, int) or isinstance(max_entries, bool) or max_entries < 4:
            raise ValueError("max_entries must be an integer >= 4")
        if not isinstance(min_fill, (int, float)) or isinstance(min_fill, bool) or not 0.3 <= min_fill <= 0.5:
            raise ValueError("min_fill must be between 0.3 and 0.5")
        self.max_entries = max_entries
        self.min_entries = max(2, int(max_entries * min_fill + 0.999999))
        if self.min_entries * 2 > max_entries + 1:
            raise ValueError("infeasible minimum fill")
        self.root = _Node(True)
        self._records: list[Bounds] = []
        self._active: list[bool] = []
        self._active_count = 0
        self._reinsertion_count = 0

    def _refresh(self, node):
        if not node.children:
            node.bounds = None
            return
        b = node.children[0].bounds
        for child in node.children[1:]:
            b = _union(b, child.bounds)
        node.bounds = b
        for child in node.children:
            if isinstance(child, _Node):
                child.parent = node

    @staticmethod
    def _node_level(node):
        """Leaves are level zero; internal levels count upward."""
        level = 0
        while not node.leaf:
            node = node.children[0]
            level += 1
        return level

    def _choose_node(self, box, target_level):
        node = self.root
        level = self._node_level(node)
        if target_level > level:
            raise ValueError("cannot reinsert an item above the current root level")
        while level > target_level:
            scored = []
            for child in node.children:
                cb = child.bounds
                enlarged = _union(cb, box)
                area_growth = _area(enlarged) - _area(cb)
                if level == 1:
                    overlap_growth = sum(
                        _overlap(enlarged, other.bounds) - _overlap(cb, other.bounds)
                        for other in node.children if other is not child
                    )
                    score = (overlap_growth, area_growth, _area(cb), len(child.children))
                else:
                    score = (area_growth, _area(cb), len(child.children))
                scored.append((score, child))
            node = min(scored, key=lambda pair: pair[0])[1]
            level -= 1
        return node

    def _split(self, node):
        items = node.children
        minimum, count = self.min_entries, len(items)
        best_axis, best_margin = 0, float("inf")
        for axis in (0, 1):
            total = 0.0
            for lower in (True, False):
                ordered = sorted(
                    items,
                    key=lambda item: (
                        item.bounds[axis] if lower else item.bounds[axis + 2],
                        item.bounds[axis + 2] if lower else item.bounds[axis],
                    ),
                )
                for cut in range(minimum, count - minimum + 1):
                    left, right = ordered[:cut], ordered[cut:]
                    lb, rb = left[0].bounds, right[0].bounds
                    for item in left[1:]:
                        lb = _union(lb, item.bounds)
                    for item in right[1:]:
                        rb = _union(rb, item.bounds)
                    total += _margin(lb) + _margin(rb)
            if total < best_margin:
                best_axis, best_margin = axis, total

        choices = []
        for lower in (True, False):
            ordered = sorted(
                items,
                key=lambda item: (
                    item.bounds[best_axis] if lower else item.bounds[best_axis + 2],
                    item.bounds[best_axis + 2] if lower else item.bounds[best_axis],
                ),
            )
            for cut in range(minimum, count - minimum + 1):
                left, right = ordered[:cut], ordered[cut:]
                lb, rb = left[0].bounds, right[0].bounds
                for item in left[1:]:
                    lb = _union(lb, item.bounds)
                for item in right[1:]:
                    rb = _union(rb, item.bounds)
                choices.append((_overlap(lb, rb), _area(lb) + _area(rb), cut, left, right))
        _, _, _, left, right = min(choices, key=lambda item: item[:3])
        node.children = list(left)
        self._refresh(node)
        sibling = _Node(node.leaf, list(right), node.parent)
        self._refresh(sibling)
        return sibling

    def _adjust_after_insert(self, node, reinserted_levels, queue):
        while node is not None:
            self._refresh(node)
            if len(node.children) <= self.max_entries:
                node = node.parent
                continue

            if node is not self.root:
                level = self._node_level(node)
                if level not in reinserted_levels:
                    reinserted_levels.add(level)
                    self._reinsertion_count += 1
                    # R*-tree forced reinsertion removes the farthest entries
                    # from the overflowing node's centre, retaining min-fill.
                    remove_count = min(
                        max(1, ceil(0.3 * (self.max_entries + 1))),
                        self.max_entries + 1 - self.min_entries,
                    )
                    center = node.bounds
                    ranked = sorted(
                        node.children,
                        key=lambda item: _center_distance_squared(center, item.bounds),
                        reverse=True,
                    )
                    removed = ranked[:remove_count]
                    removed_ids = {id(item) for item in removed}
                    node.children = [item for item in node.children if id(item) not in removed_ids]
                    self._refresh(node)
                    ancestor = node.parent
                    while ancestor is not None:
                        self._refresh(ancestor)
                        ancestor = ancestor.parent
                    for item in removed:
                        # Reinsert entries at leaf level and subtrees at the
                        # level of their former parent.
                        queue.append((item, level))
                    return

            sibling = self._split(node)
            if node is self.root:
                new_root = _Node(False, [node, sibling])
                self.root = new_root
                self._refresh(new_root)
                return
            parent = node.parent
            parent.children.append(sibling)
            sibling.parent = parent
            node = parent

    def insert(self, bounds: Iterable[float]) -> int:
        box = _bounds(bounds)
        index = len(self._records)
        self._records.append(box)
        self._active.append(True)
        self._active_count += 1
        queue = [(_Entry(index, box), 0)]
        reinserted_levels = set()
        while queue:
            item, target_level = queue.pop(0)
            target = self._choose_node(item.bounds, target_level)
            target.children.append(item)
            if isinstance(item, _Node):
                item.parent = target
            self._adjust_after_insert(target, reinserted_levels, queue)
        return index

    def query(self, bounds: Iterable[float]) -> list[int]:
        query_box = _bounds(bounds)
        if self.root.bounds is None:
            return []
        found = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            b = node.bounds
            if b[2] < query_box[0] or query_box[2] < b[0] or b[3] < query_box[1] or query_box[3] < b[1]:
                continue
            for child in node.children:
                b = child.bounds
                if b[2] < query_box[0] or query_box[2] < b[0] or b[3] < query_box[1] or query_box[3] < b[1]:
                    continue
                if isinstance(child, _Entry):
                    found.append(child.index)
                else:
                    stack.append(child)
        return sorted(found)

    def k_nearest(self, point, k: int = 1) -> list[tuple[int, float]]:
        """Return k nearest rectangles as (stable_id, squared_distance).

        Distance is the exact Euclidean lower-bound distance from the query
        point to each indexed axis-aligned rectangle, not to an underlying
        non-rectangular geometry.
        """
        if len(point) != 2:
            raise ValueError("point must contain x and y")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError("query coordinates must be finite")
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        if self.root.bounds is None:
            return []

        def distance_squared(box):
            dx = max(box[0] - x, 0.0, x - box[2])
            dy = max(box[1] - y, 0.0, y - box[3])
            return dx * dx + dy * dy

        serial = count()
        queue = [(distance_squared(self.root.bounds), next(serial), self.root)]
        best = []
        while queue:
            lower_bound, _, node = heappop(queue)
            if len(best) == k and lower_bound > best[-1][1]:
                break
            for child in node.children:
                d2 = distance_squared(child.bounds)
                if isinstance(child, _Entry):
                    best.append((child.index, d2))
                    best.sort(key=lambda item: (item[1], item[0]))
                    if len(best) > k:
                        best.pop()
                elif len(best) < k or d2 <= best[-1][1]:
                    heappush(queue, (d2, next(serial), child))
        return [(index, d2) for index, d2 in best]

    def delete(self, index: int) -> bool:
        """Delete a record by stable insertion ID; return False if already absent."""
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("record ID must be an integer")
        if index < 0 or index >= len(self._records) or not self._active[index]:
            return False

        leaf = None
        stack = [self.root]
        while stack and leaf is None:
            node = stack.pop()
            if node.leaf:
                if any(item.index == index for item in node.children):
                    leaf = node
            else:
                stack.extend(child for child in node.children if child.bounds is not None)
        if leaf is None:
            raise RuntimeError("active record is missing from the index")

        leaf.children = [item for item in leaf.children if item.index != index]
        self._active[index] = False
        self._active_count -= 1
        queue = []
        node = leaf
        while node is not self.root:
            parent = node.parent
            if len(node.children) < self.min_entries:
                parent.children.remove(node)
                level = self._node_level(node)
                queue.extend((child, level) for child in node.children)
                node.parent = None
            else:
                self._refresh(node)
            node = parent

        if not self.root.leaf and len(self.root.children) == 1:
            self.root = self.root.children[0]
            self.root.parent = None
        elif not self.root.leaf and not self.root.children:
            self.root = _Node(True)
        else:
            self._refresh(self.root)

        # Condense-tree orphans are reinserted from highest level downward.
        # Raise the root temporarily when a detached subtree is taller than
        # the surviving tree; this preserves the subtree's original level.
        queue.sort(key=lambda pair: pair[1], reverse=True)
        no_forced_reinsert = set(range(self._node_level(self.root) + 1))
        while queue:
            item, target_level = queue.pop(0)
            while self._node_level(self.root) < target_level:
                old_root = self.root
                self.root = _Node(False, [old_root])
                self._refresh(self.root)
            no_forced_reinsert.update(range(self._node_level(self.root) + 1))
            target_node = self._choose_node(item.bounds, target_level)
            target_node.children.append(item)
            if isinstance(item, _Node):
                item.parent = target_node
            self._adjust_after_insert(target_node, no_forced_reinsert, queue)
        return True

    def __len__(self):
        return self._active_count

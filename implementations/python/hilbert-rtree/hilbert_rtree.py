"""Immutable Hilbert-ordered packed R-tree for 2D bounding boxes."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Iterable

Bounds = tuple[float, float, float, float]

@dataclass(frozen=True)
class _Entry:
    index: int
    bounds: Bounds
    key: int

@dataclass(frozen=True)
class _Node:
    bounds: Bounds
    children: tuple["_Entry | _Node", ...]
    leaf: bool
    key: int

def _validate_bounds(values: Iterable[float]) -> Bounds:
    b = tuple(float(v) for v in values)
    if len(b) != 4 or not all(isfinite(v) for v in b):
        raise ValueError("bounds must contain four finite coordinates")
    if b[0] > b[2] or b[1] > b[3]:
        raise ValueError("minimum bounds must not exceed maximum bounds")
    return b

def _union(items) -> Bounds:
    return (min(item.bounds[0] for item in items),
            min(item.bounds[1] for item in items),
            max(item.bounds[2] for item in items),
            max(item.bounds[3] for item in items))

def _center(bounds: Bounds) -> tuple[float, float]:
    return ((bounds[0] + bounds[2]) / 2.0, (bounds[1] + bounds[3]) / 2.0)

def hilbert_index(x: int, y: int, bits: int = 16) -> int:
    """Return the 2D Hilbert distance for integer grid coordinates."""
    if isinstance(bits, bool) or not isinstance(bits, int) or not 1 <= bits <= 31:
        raise ValueError("bits must be an integer from 1 through 31")
    n = 1 << bits
    if (isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, int)
            or not isinstance(y, int) or not 0 <= x < n or not 0 <= y < n):
        raise ValueError("x and y must be integers inside the Hilbert grid")
    distance = 0
    scale = n >> 1
    while scale:
        rx = 1 if x & scale else 0
        ry = 1 if y & scale else 0
        distance += scale * scale * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x
        scale >>= 1
    return distance

def _quantize(value: float, lower: float, upper: float, bits: int) -> int:
    maximum = (1 << bits) - 1
    if upper == lower:
        return 0
    return min(maximum, max(0, int((value - lower) / (upper - lower) * maximum)))

def _intersects(a: Bounds, b: Bounds) -> bool:
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])

class HilbertPackedRTree:
    """Build-once R-tree whose entries are bulk-loaded in Hilbert order.

    This is a static Hilbert-packed baseline, not a dynamic Hilbert R-tree.
    Query results are envelope-intersection candidates in original input order.
    """
    def __init__(self, bounds: Iterable[Iterable[float]], node_capacity: int = 10,
                 hilbert_bits: int = 16):
        if isinstance(node_capacity, bool) or not isinstance(node_capacity, int) or node_capacity < 2:
            raise ValueError("node_capacity must be an integer of at least 2")
        if isinstance(hilbert_bits, bool) or not isinstance(hilbert_bits, int) or not 1 <= hilbert_bits <= 31:
            raise ValueError("hilbert_bits must be an integer from 1 through 31")
        self.node_capacity = node_capacity
        self.hilbert_bits = hilbert_bits
        self._bounds = tuple(_validate_bounds(item) for item in bounds)
        centers = [_center(b) for b in self._bounds]
        if centers:
            xmin, xmax = min(x for x, _ in centers), max(x for x, _ in centers)
            ymin, ymax = min(y for _, y in centers), max(y for _, y in centers)
        else:
            xmin = xmax = ymin = ymax = 0.0
        entries = []
        for index, (box, (x, y)) in enumerate(zip(self._bounds, centers)):
            qx = _quantize(x, xmin, xmax, hilbert_bits)
            qy = _quantize(y, ymin, ymax, hilbert_bits)
            entries.append(_Entry(index, box, hilbert_index(qx, qy, hilbert_bits)))
        entries.sort(key=lambda entry: (entry.key, entry.index))
        level = []
        for start in range(0, len(entries), node_capacity):
            children = tuple(entries[start:start + node_capacity])
            level.append(_Node(_union(children), children, True,
                               hilbert_index(*self._node_grid_center(_union(children), xmin, xmax, ymin, ymax), hilbert_bits)))
        while len(level) > 1:
            level.sort(key=lambda node: (node.key, node.bounds))
            next_level = []
            for start in range(0, len(level), node_capacity):
                children = tuple(level[start:start + node_capacity])
                box = _union(children)
                key = hilbert_index(*self._node_grid_center(box, xmin, xmax, ymin, ymax), hilbert_bits)
                next_level.append(_Node(box, children, False, key))
            level = next_level
        self._root = level[0] if level else None

    @staticmethod
    def _node_grid_center(bounds, xmin, xmax, ymin, ymax, bits=16):
        x, y = _center(bounds)
        return (_quantize(x, xmin, xmax, bits), _quantize(y, ymin, ymax, bits))

    def query(self, bounds: Iterable[float]) -> list[int]:
        query_bounds = _validate_bounds(bounds)
        if self._root is None:
            return []
        found = []
        stack = [self._root]
        while stack:
            node = stack.pop()
            if not _intersects(node.bounds, query_bounds):
                continue
            if node.leaf:
                found.extend(child.index for child in node.children
                             if _intersects(child.bounds, query_bounds))
            else:
                stack.extend(child for child in node.children
                             if _intersects(child.bounds, query_bounds))
        return sorted(found)

    def __len__(self) -> int:
        return len(self._bounds)

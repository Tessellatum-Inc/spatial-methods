"""Broad-phase 2-D axis-aligned bounding-box collision candidates."""
from dataclasses import dataclass
from math import floor, isfinite


Box = tuple[float, float, float, float]


def _box(raw):
    if len(raw) != 4:
        raise ValueError("each box must be (xmin, ymin, xmax, ymax)")
    b = tuple(float(v) for v in raw)
    if not all(isfinite(v) for v in b) or b[0] > b[2] or b[1] > b[3]:
        raise ValueError("box coordinates must be finite and ordered")
    return b


def _boxes(values):
    return [_box(b) for b in values]


def intersects(a: Box, b: Box) -> bool:
    """Inclusive AABB overlap; touching edges and corners count as contact."""
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def brute_force_pairs(boxes):
    data = _boxes(boxes)
    return {(i, j) for i in range(len(data)) for j in range(i+1, len(data))
            if intersects(data[i], data[j])}


def sweep_and_prune(boxes):
    """Return exact overlapping pairs using a 1-D x-axis sweep."""
    data = _boxes(boxes)
    order = sorted(range(len(data)), key=lambda i: (data[i][0], data[i][2], i))
    active, pairs = [], set()
    for idx in order:
        current = data[idx]
        active = [j for j in active if data[j][2] >= current[0]]
        for j in active:
            if data[j][3] >= current[1] and current[3] >= data[j][1]:
                pairs.add((min(idx, j), max(idx, j)))
        active.append(idx)
    return pairs


def spatial_hash_pairs(boxes, cell_size):
    """Return exact pairs using a uniform grid broad phase and AABB narrow phase."""
    if not isfinite(float(cell_size)) or cell_size <= 0:
        raise ValueError("cell_size must be finite and positive")
    data = _boxes(boxes)
    buckets = {}
    for idx, (xmin, ymin, xmax, ymax) in enumerate(data):
        ix0, iy0 = floor(xmin/cell_size), floor(ymin/cell_size)
        ix1, iy1 = floor(xmax/cell_size), floor(ymax/cell_size)
        for ix in range(ix0, ix1+1):
            for iy in range(iy0, iy1+1):
                buckets.setdefault((ix, iy), []).append(idx)
    candidates = set()
    for members in buckets.values():
        for pos, i in enumerate(members):
            for j in members[pos+1:]:
                candidates.add((min(i,j), max(i,j)))
    return {(i,j) for i,j in candidates if intersects(data[i], data[j])}


@dataclass
class _Node:
    bounds: Box
    indices: tuple[int, ...] = ()
    left: "_Node | None" = None
    right: "_Node | None" = None


def _union(data, indices):
    return (min(data[i][0] for i in indices), min(data[i][1] for i in indices),
            max(data[i][2] for i in indices), max(data[i][3] for i in indices))


def build_bvh(boxes, leaf_size=4):
    """Build a median-split static AABB BVH; returns an immutable node tree."""
    data = _boxes(boxes)
    if leaf_size < 1:
        raise ValueError("leaf_size must be positive")
    def build(indices):
        bounds = _union(data, indices)
        if len(indices) <= leaf_size:
            return _Node(bounds, tuple(sorted(indices)))
        axis = 0 if bounds[2]-bounds[0] >= bounds[3]-bounds[1] else 1
        ordered = sorted(indices, key=lambda i: ((data[i][axis]+data[i][axis+2])/2, i))
        mid = len(ordered)//2
        return _Node(bounds, (), build(ordered[:mid]), build(ordered[mid:]))
    return (build(list(range(len(data)))) if data else None, data)


def bvh_query(tree, data, query_box):
    """Return original indices whose AABBs overlap query_box."""
    if tree is None:
        return []
    query = _box(query_box)
    found, stack = [], [tree]
    while stack:
        node = stack.pop()
        if not intersects(node.bounds, query):
            continue
        if node.indices:
            found.extend(i for i in node.indices if intersects(data[i], query))
        else:
            if node.right is not None: stack.append(node.right)
            if node.left is not None: stack.append(node.left)
    return sorted(found)


def bvh_pairs(boxes, leaf_size=4):
    """Return exact all-pairs overlaps by querying a static BVH per box."""
    tree, data = build_bvh(boxes, leaf_size)
    pairs = set()
    for i, box in enumerate(data):
        for j in bvh_query(tree, data, box):
            if j > i:
                pairs.add((i,j))
    return pairs

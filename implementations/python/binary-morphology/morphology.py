"""Binary mathematical morphology and connected components on 2-D rasters.

All operators use an explicit finite structuring element. Outside-raster
samples are false. This is a transparent reference implementation, not a
replacement for optimised image-processing libraries.
"""
from __future__ import annotations

import numpy as np


def _binary(image, name="image"):
    a = np.asarray(image)
    if a.ndim != 2 or a.size == 0:
        raise ValueError(f"{name} must be a non-empty 2-D array")
    if not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must contain finite values")
    return a.astype(bool, copy=False)


def _structure(structure):
    s = np.asarray(structure)
    if s.ndim != 2 or s.size == 0 or not np.any(s):
        raise ValueError("structure must be a non-empty 2-D array with at least one active cell")
    if not np.all(np.isfinite(s)):
        raise ValueError("structure must contain finite values")
    s = s.astype(bool, copy=False)
    cy, cx = s.shape[0] // 2, s.shape[1] // 2
    return [(int(y-cy), int(x-cx)) for y, x in np.argwhere(s)]


def _apply(image, offsets, operation):
    a = _binary(image)
    out = np.ones_like(a) if operation == "erosion" else np.zeros_like(a)
    h, w = a.shape
    for dy, dx in offsets:
        shifted = np.zeros_like(a)
        y0, y1 = max(0, -dy), min(h, h-dy)
        x0, x1 = max(0, -dx), min(w, w-dx)
        if y0 < y1 and x0 < x1:
            shifted[y0:y1, x0:x1] = a[y0+dy:y1+dy, x0+dx:x1+dx]
        if operation == "erosion":
            out &= shifted
        else:
            out |= shifted
    return out


def erosion(image, structure=None):
    """Binary erosion; out-of-bounds samples are background (False)."""
    if structure is None:
        structure = np.ones((3, 3), dtype=bool)
    return _apply(image, _structure(structure), "erosion")


def dilation(image, structure=None):
    """Binary dilation; out-of-bounds samples are background (False)."""
    if structure is None:
        structure = np.ones((3, 3), dtype=bool)
    return _apply(image, _structure(structure), "dilation")


def opening(image, structure=None):
    """Erosion followed by dilation using the same structuring element."""
    if structure is None:
        structure = np.ones((3, 3), dtype=bool)
    return dilation(erosion(image, structure), structure)


def closing(image, structure=None):
    """Dilation followed by erosion using the same structuring element."""
    if structure is None:
        structure = np.ones((3, 3), dtype=bool)
    return erosion(dilation(image, structure), structure)


def hit_or_miss(image, foreground, background):
    """Detect a binary pattern; both structuring elements are anchored centrally."""
    a = _binary(image)
    fg = _structure(foreground)
    bg = _structure(background)
    hit = _apply(a, fg, "erosion")
    miss = _apply(~a, bg, "erosion")
    return hit & miss


def geodesic_reconstruction(marker, mask, structure=None, max_iterations=None):
    """Binary reconstruction by dilation under a mask until a fixed point.

    Marker must be a subset of mask. The default structuring element is the
    3x3 neighbourhood. A finite max_iterations is an explicit safety limit;
    reaching it before convergence raises RuntimeError.
    """
    m, limit = _binary(marker, "marker"), _binary(mask, "mask")
    if m.shape != limit.shape:
        raise ValueError("marker and mask must have the same shape")
    if np.any(m & ~limit):
        raise ValueError("marker must be a subset of mask")
    if structure is None:
        structure = np.ones((3, 3), dtype=bool)
    offsets = _structure(structure)
    if max_iterations is not None and (not isinstance(max_iterations, int) or max_iterations < 0):
        raise ValueError("max_iterations must be a non-negative integer or None")
    current = m.copy()
    iterations = 0
    while True:
        if max_iterations is not None and iterations >= max_iterations:
            raise RuntimeError("reconstruction did not converge within max_iterations")
        updated = _apply(current, offsets, "dilation") & limit
        iterations += 1
        if np.array_equal(updated, current):
            return current
        current = updated


def connected_components(image, connectivity=4):
    """Label foreground components in row-major discovery order.

    Returns (labels, component_sizes). Background label is 0; foreground
    labels are 1..k. Connectivity is 4 or 8.
    """
    a = _binary(image)
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    neighbours = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    if connectivity == 8:
        neighbours += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    h, w = a.shape
    labels = np.zeros((h, w), dtype=np.int32)
    sizes = []
    next_label = 0
    for y in range(h):
        for x in range(w):
            if not a[y, x] or labels[y, x]:
                continue
            next_label += 1
            stack = [(y, x)]
            labels[y, x] = next_label
            size = 0
            while stack:
                cy, cx = stack.pop()
                size += 1
                for dy, dx in neighbours:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and a[ny, nx] and labels[ny, nx] == 0:
                        labels[ny, nx] = next_label
                        stack.append((ny, nx))
            sizes.append(size)
    return labels, np.asarray(sizes, dtype=np.int64)

def zhang_suen_thinning(image, max_iterations=None):
    """Return a 1-pixel skeleton using the two-subiteration Zhang-Suen rule.

    The raster is zero-padded outside its extent. Each complete iteration
    applies the two deletion substeps until neither removes a pixel. A
    finite iteration cap raises RuntimeError rather than returning a partial
    skeleton.
    """
    a = _binary(image).copy()
    if max_iterations is not None and (not isinstance(max_iterations, int) or max_iterations < 0):
        raise ValueError("max_iterations must be a non-negative integer or None")
    h, w = a.shape
    iterations = 0
    while True:
        if max_iterations is not None and iterations >= max_iterations:
            raise RuntimeError("thinning did not converge within max_iterations")
        changed = False
        for step in (0, 1):
            p = np.pad(a, 1, constant_values=False)
            p2 = p[:-2, 1:-1]
            p3 = p[:-2, 2:]
            p4 = p[1:-1, 2:]
            p5 = p[2:, 2:]
            p6 = p[2:, 1:-1]
            p7 = p[2:, :-2]
            p8 = p[1:-1, :-2]
            p9 = p[:-2, :-2]
            neighbours = [p2, p3, p4, p5, p6, p7, p8, p9]
            count = sum(n.astype(np.uint8) for n in neighbours)
            transitions = sum(
                ((~neighbours[i]) & neighbours[(i + 1) % 8]).astype(np.uint8)
                for i in range(8)
            )
            common = a & (count >= 2) & (count <= 6) & (transitions == 1)
            if step == 0:
                remove = common & ~(p2 & p4 & p6) & ~(p4 & p6 & p8)
            else:
                remove = common & ~(p2 & p4 & p8) & ~(p2 & p6 & p8)
            if np.any(remove):
                a[remove] = False
                changed = True
        iterations += 1
        if not changed:
            return a

def two_pass_connected_components(image, connectivity=8):
    """Two-pass union-find connected-component labelling.

    Neighbourhood is 4- or 8-connected. The first raster pass assigns
    provisional labels and unions equivalent labels; the second pass
    replaces each provisional label with its canonical root label. Final
    labels are compact and ordered by first row-major occurrence.
    """
    a = _binary(image)
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    h, w = a.shape
    labels = np.zeros((h, w), dtype=np.int32)
    parent = [0]

    def make_set():
        parent.append(len(parent))
        return len(parent) - 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[max(rx, ry)] = min(rx, ry)

    previous = [(-1, 0), (0, -1)]
    if connectivity == 8:
        previous += [(-1, -1), (-1, 1)]
    for y in range(h):
        for x in range(w):
            if not a[y, x]:
                continue
            neighbours = []
            for dy, dx in previous:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and labels[ny, nx] > 0:
                    neighbours.append(int(labels[ny, nx]))
            if not neighbours:
                labels[y, x] = make_set()
            else:
                smallest = min(neighbours)
                labels[y, x] = smallest
                for other in neighbours:
                    union(smallest, other)

    root_to_compact = {}
    sizes = []
    next_label = 0
    for y in range(h):
        for x in range(w):
            provisional = int(labels[y, x])
            if provisional == 0:
                continue
            root = find(provisional)
            if root not in root_to_compact:
                next_label += 1
                root_to_compact[root] = next_label
                sizes.append(0)
            compact = root_to_compact[root]
            labels[y, x] = compact
            sizes[compact - 1] += 1
    return labels, np.asarray(sizes, dtype=np.int64)

def binary_granulometry(image, structures):
    """Measure a binary opening granulometry over nested structuring elements.

    Returns original-plus-opened foreground areas and the pattern spectrum
    (area removed at each successive scale). Structures must form an
    increasing family around their common floor-centred origin.
    """
    a = _binary(image)
    family = list(structures)
    if not family:
        raise ValueError("at least one structuring element is required")
    offsets = [_structure(s) for s in family]
    for previous, current in zip(offsets, offsets[1:]):
        if not set(previous).issubset(current):
            raise ValueError("structuring elements must be nested in increasing order")
    areas = [int(np.count_nonzero(a))]
    for structure in family:
        area = int(np.count_nonzero(opening(a, structure)))
        if area > areas[-1]:
            raise RuntimeError("opening area increased; check nesting and border convention")
        areas.append(area)
    area_array = np.asarray(areas, dtype=np.int64)
    return {"areas": area_array, "pattern_spectrum": area_array[:-1] - area_array[1:]}

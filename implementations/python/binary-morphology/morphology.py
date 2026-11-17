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

def binary_granulometry(image, radii):
    """Measure a square-opening granulometry at strictly increasing radii.

    Each radius r uses the full (2r+1)-by-(2r+1) square structuring element.
    This homothetic square family forms a granulometric scale sequence. The
    result contains the original-plus-opened foreground areas and the
    pattern spectrum (area removed between successive scales).
    """
    a = _binary(image)
    scales = list(radii)
    if not scales:
        raise ValueError("at least one radius is required")
    if any(not isinstance(r, (int, np.integer)) or isinstance(r, (bool, np.bool_)) or r < 0 for r in scales):
        raise ValueError("radii must be non-negative integers")
    if any(right <= left for left, right in zip(scales, scales[1:])):
        raise ValueError("radii must be strictly increasing")
    areas = [int(np.count_nonzero(a))]
    for radius in scales:
        structure = np.ones((2 * int(radius) + 1, 2 * int(radius) + 1), dtype=bool)
        area = int(np.count_nonzero(opening(a, structure)))
        if area > areas[-1]:
            raise RuntimeError("square granulometry area increased; check morphology boundary semantics")
        areas.append(area)
    area_array = np.asarray(areas, dtype=np.int64)
    return {
        "radii": np.asarray(scales, dtype=np.int64),
        "areas": area_array,
        "pattern_spectrum": area_array[:-1] - area_array[1:],
    }


def _grayscale_components(mask, connectivity):
    """Return row-major connected components as sorted flat-index tuples."""
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    neighbours = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    if connectivity == 8:
        neighbours += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    components = []
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            seen[y, x] = True
            stack = [(y, x)]
            pixels = []
            while stack:
                cy, cx = stack.pop()
                pixels.append(cy * w + cx)
                for dy, dx in neighbours:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            components.append(tuple(sorted(pixels)))
    return components


def grayscale_component_tree(image, polarity="max", connectivity=4):
    """Build an explicit max-tree or min-tree for a finite 2-D grayscale raster.

    The implementation repeatedly labels connected upper-level sets (max-tree)
    or lower-level sets (min-tree), then links components as thresholds expand.
    It is an inspectable reference, not a memory-efficient production algorithm:
    pixel membership is stored per node and threshold components are recomputed.

    Returns a dictionary with nodes and roots. Each node has a stable row-major
    id, its birth level, sorted pixels as (row, column) pairs, area and a parent
    node id (or None for a root). For a max-tree, parent levels are lower than
    child levels; for a min-tree they are higher.
    """
    a = np.asarray(image)
    if a.ndim != 2 or a.size == 0 or not (
        np.issubdtype(a.dtype, np.number) or np.issubdtype(a.dtype, np.bool_)
    ):
        raise ValueError("image must be a non-empty 2-D numeric array")
    if not np.all(np.isfinite(a)):
        raise ValueError("image must contain finite values")
    if polarity not in ("max", "min"):
        raise ValueError("polarity must be 'max' or 'min'")
    if connectivity not in (4, 8) or isinstance(connectivity, (bool, np.bool_)):
        raise ValueError("connectivity must be 4 or 8")

    levels = np.unique(a)
    levels = levels[::-1] if polarity == "max" else levels
    nodes = []
    previous = []
    h, w = a.shape

    for level in levels:
        mask = a >= level if polarity == "max" else a <= level
        components = _grayscale_components(mask, connectivity)
        current = []
        previous_by_pixels = {pixels: node_id for pixels, node_id in previous}
        for pixels in components:
            exact = previous_by_pixels.get(pixels)
            if exact is not None:
                current.append((pixels, exact))
                continue

            node_id = len(nodes)
            coordinates = tuple((index // w, index % w) for index in pixels)
            nodes.append({
                "id": node_id,
                "level": level.item() if isinstance(level, np.generic) else level,
                "pixels": coordinates,
                "area": len(pixels),
                "parent": None,
            })
            pixel_set = set(pixels)
            for old_pixels, old_id in previous:
                if set(old_pixels).issubset(pixel_set):
                    nodes[old_id]["parent"] = node_id
            current.append((pixels, node_id))
        previous = current

    roots = [node["id"] for node in nodes if node["parent"] is None]
    return {
        "polarity": polarity,
        "connectivity": connectivity,
        "shape": tuple(int(v) for v in a.shape),
        "nodes": nodes,
        "roots": roots,
    }


def grayscale_alpha_tree(image, connectivity=4):
    """Build an alpha hierarchy from adjacent-pixel absolute differences.

    At threshold alpha, quasi-flat zones are components of the grid graph
    retaining edges with abs(I[p]-I[q]) <= alpha. This transparent reference
    stores each node's pixels and recomputes components at each edge weight;
    it is intended for small rasters, not production-scale images. The
    definition is explicit because alpha-tree conventions vary in the literature.
    """
    a = np.asarray(image)
    if a.ndim != 2 or a.size == 0 or not np.issubdtype(a.dtype, np.number):
        raise ValueError("image must be a non-empty 2-D numeric array")
    if not np.all(np.isfinite(a)):
        raise ValueError("image must contain finite values")
    if connectivity not in (4, 8) or isinstance(connectivity, (bool, np.bool_)):
        raise ValueError("connectivity must be 4 or 8")
    h, w = a.shape
    directions = [(0, 1), (1, 0)] + ([(1, 1), (1, -1)] if connectivity == 8 else [])
    edges = []
    for y in range(h):
        for x in range(w):
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    weight = float(abs(float(a[y, x]) - float(a[ny, nx])))
                    edges.append((weight, y*w+x, ny*w+nx))
    levels = sorted({edge[0] for edge in edges}) or [0.0]
    nodes, previous = [], []
    for alpha in levels:
        parent = list(range(h*w))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for weight, u, v in edges:
            if weight <= alpha:
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[max(ru, rv)] = min(ru, rv)
        groups = {}
        for index in range(h*w):
            groups.setdefault(find(index), []).append(index)
        current = []
        previous_by_pixels = {pixels: node_id for pixels, node_id in previous}
        for indices in sorted(groups.values(), key=lambda xs: xs[0]):
            pixels = tuple(indices)
            existing = previous_by_pixels.get(pixels)
            if existing is not None:
                current.append((pixels, existing))
                continue
            node_id = len(nodes)
            nodes.append({"id": node_id, "alpha": float(alpha),
                          "pixels": tuple((i // w, i % w) for i in pixels),
                          "area": len(pixels), "parent": None})
            pixel_set = set(pixels)
            for old_pixels, old_id in previous:
                if set(old_pixels).issubset(pixel_set):
                    nodes[old_id]["parent"] = node_id
            current.append((pixels, node_id))
        previous = current
    return {"connectivity": connectivity, "shape": (h, w), "nodes": nodes,
            "roots": [node["id"] for node in nodes if node["parent"] is None]}



def grayscale_area_attribute_filter(image, min_area, polarity="max", connectivity=4):
    """Apply a grayscale area opening (max-tree) or area closing (min-tree).

    min_area is the minimum connected-component pixel count to retain.
    Bright upper-level components smaller than the threshold are lowered for
    max-tree opening; dark lower-level components are raised for min-tree
    closing. This explicit component-tree reference is for small teaching
    rasters, not production-scale images.
    """
    a = np.asarray(image)
    if a.ndim != 2 or a.size == 0 or not (
        np.issubdtype(a.dtype, np.number) or np.issubdtype(a.dtype, np.bool_)
    ):
        raise ValueError("image must be a non-empty 2-D numeric array")
    if not np.all(np.isfinite(a)):
        raise ValueError("image must contain finite values")
    if not isinstance(min_area, (int, np.integer)) or isinstance(min_area, (bool, np.bool_)) or min_area < 1:
        raise ValueError("min_area must be a positive integer")
    if polarity not in ("max", "min"):
        raise ValueError("polarity must be 'max' or 'min'")

    tree = grayscale_component_tree(a, polarity=polarity, connectivity=connectivity)
    nodes = tree["nodes"]
    h, w = a.shape
    owner = np.full((h, w), -1, dtype=np.int64)
    for node in nodes:
        level = node["level"]
        for y, x in node["pixels"]:
            current = owner[y, x]
            if current < 0:
                owner[y, x] = node["id"]
            else:
                old_level = nodes[int(current)]["level"]
                if (polarity == "max" and level > old_level) or (polarity == "min" and level < old_level):
                    owner[y, x] = node["id"]

    result = np.empty_like(a)
    fallback = np.min(a) if polarity == "max" else np.max(a)
    for y in range(h):
        for x in range(w):
            node_id = int(owner[y, x])
            while node_id >= 0 and nodes[node_id]["area"] < int(min_area):
                parent = nodes[node_id]["parent"]
                node_id = -1 if parent is None else int(parent)
            result[y, x] = fallback if node_id < 0 else nodes[node_id]["level"]
    return result


def moore_neighbor_contours(image, connectivity=8):
    """Trace one outer Moore-neighbour contour for each foreground component.

    Returns a list of integer arrays of (row, column) coordinates. The
    start pixel is the topmost, then leftmost, foreground pixel in each
    component. The start is not repeated at the end. Components are ordered
    by row-major discovery. This teaching implementation traces outer
    component boundaries only; it does not emit hole contours or subpixel
    polygon geometry. Moore tracing uses the 8-neighbourhood even when
    4-connectivity is selected for separating foreground components.
    """
    a = _binary(image)
    if connectivity not in (4, 8) or isinstance(connectivity, (bool, np.bool_)):
        raise ValueError("connectivity must be 4 or 8")
    labels, sizes = connected_components(a, connectivity)
    clockwise = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                 (1, 0), (1, -1), (0, -1), (-1, -1)]
    contours = []
    for component_id in range(1, len(sizes) + 1):
        component = labels == component_id
        coordinates = np.argwhere(component)
        start = tuple(int(v) for v in coordinates[0])
        current = start
        backtrack = (start[0], start[1] - 1)
        contour = [start]
        first_next = None
        max_steps = max(8, int(sizes[component_id - 1]) * 16)
        for _ in range(max_steps):
            relative = (backtrack[0] - current[0], backtrack[1] - current[1])
            try:
                back_index = clockwise.index(relative)
            except ValueError as exc:
                raise RuntimeError("invalid Moore backtrack state") from exc

            found = None
            preceding = None
            for offset in range(1, 9):
                index = (back_index + offset) % 8
                dy, dx = clockwise[index]
                candidate = (current[0] + dy, current[1] + dx)
                if (0 <= candidate[0] < a.shape[0]
                        and 0 <= candidate[1] < a.shape[1]
                        and component[candidate]):
                    found = candidate
                    previous_index = (index - 1) % 8
                    pdy, pdx = clockwise[previous_index]
                    preceding = (current[0] + pdy, current[1] + pdx)
                    break
            if found is None:
                break
            if current == start and first_next is not None and found == first_next:
                break
            if first_next is None:
                first_next = found
            contour.append(found)
            backtrack, current = preceding, found
        else:
            raise RuntimeError("Moore contour did not close within the safety bound")

        # A component with no 8-neighbour has a one-pixel contour.
        contours.append(np.asarray(contour, dtype=np.int64))
    return contours

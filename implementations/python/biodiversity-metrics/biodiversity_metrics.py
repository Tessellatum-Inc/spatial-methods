"""Grid-based biodiversity range metrics and occurrence summaries."""
from __future__ import annotations
import numpy as np
from scipy.spatial import ConvexHull, QhullError


def _occurrences(points):
    values = np.asarray(points, dtype=float)
    if values.ndim != 2 or values.shape[1] != 2 or values.shape[0] == 0:
        raise ValueError("points must be a non-empty (n, 2) array")
    if not np.isfinite(values).all():
        raise ValueError("points must contain only finite coordinates")
    return values


def extent_of_occurrence(points):
    """Return convex-hull vertices and planar area for projected occurrences."""
    values = np.unique(_occurrences(points), axis=0)
    if len(values) < 3:
        return {"polygon": values, "area": 0.0}
    try:
        hull = ConvexHull(values)
    except QhullError:
        direction = values[-1] - values[0]
        if np.linalg.norm(direction) == 0:
            endpoints = values[:1]
        else:
            projection = (values - values[0]) @ direction
            endpoints = values[[int(np.argmin(projection)), int(np.argmax(projection))]]
        return {"polygon": endpoints, "area": 0.0}
    return {"polygon": values[hull.vertices], "area": float(hull.volume)}


def area_of_occupancy(points, *, cell_size=2000.0, origin=(0.0, 0.0)):
    """Count distinct occupied square cells on a declared aligned grid."""
    values = _occurrences(points)
    try:
        size, offset = float(cell_size), np.asarray(origin, dtype=float)
    except (TypeError, ValueError):
        raise ValueError("cell_size and origin must be numeric") from None
    if not np.isfinite(size) or size <= 0:
        raise ValueError("cell_size must be finite and positive")
    if offset.shape != (2,) or not np.isfinite(offset).all():
        raise ValueError("origin must contain two finite coordinates")
    cells = np.floor((values - offset) / size).astype(np.int64)
    unique = np.unique(cells, axis=0)
    return {"area": float(len(unique) * size * size),
            "occupied_cells": int(len(unique)), "cell_indices": unique}


def species_richness(presence):
    """Count present species per cell in a binary cells-by-species matrix."""
    matrix = np.asarray(presence)
    if matrix.ndim != 2 or 0 in matrix.shape:
        raise ValueError("presence must be a non-empty 2D matrix")
    if not np.isfinite(matrix).all() or not np.isin(matrix, [0, 1, False, True]).all():
        raise ValueError("presence must contain only binary finite values")
    return matrix.astype(bool).sum(axis=1).astype(int)


def weighted_endemism(presence):
    """Sum inverse occupied-cell range sizes for species present in each cell."""
    richness = species_richness(presence)
    binary = np.asarray(presence, dtype=bool)
    ranges = binary.sum(axis=0)
    weights = np.divide(1.0, ranges, out=np.zeros(ranges.shape, dtype=float), where=ranges > 0)
    return binary @ weights


def landscape_patch_metrics(
    classes,
    *,
    cell_size=1.0,
    connectivity=4,
    nodata=None,
):
    """Summarise class patches and internal edge density in a categorical raster.

    Patches are 4- or 8-neighbour connected components within each class.
    Edges count horizontal/vertical adjacencies between valid, different
    classes; the outer raster boundary and NoData perimeter are excluded.
    Area units are the square of cell_size; edge density is length per
    hectare when cell_size is in metres.
    """
    from scipy import ndimage

    raster = np.asarray(classes)
    if raster.ndim != 2 or 0 in raster.shape:
        raise ValueError("classes must be a non-empty 2D raster")
    if not np.issubdtype(raster.dtype, np.number):
        raise TypeError("classes must be numeric categorical values")
    if np.issubdtype(raster.dtype, np.floating):
        finite = np.isfinite(raster)
        if nodata is None and not finite.all():
            raise ValueError("non-finite cells require an explicit nodata value")
    else:
        finite = np.ones(raster.shape, dtype=bool)
    if nodata is None:
        valid = finite
    else:
        valid = finite & (raster != nodata)
    if not valid.any():
        raise ValueError("raster must contain at least one valid cell")
    if not np.isfinite(cell_size) or cell_size <= 0:
        raise ValueError("cell_size must be finite and positive")
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")

    structure = ndimage.generate_binary_structure(2, 1 if connectivity == 4 else 2)
    classes_present = np.unique(raster[valid])
    cell_area = float(cell_size) ** 2
    landscape_area = int(valid.sum()) * cell_area
    records = {}
    total_patches = 0
    for cls in classes_present:
        mask = valid & (raster == cls)
        labels, count = ndimage.label(mask, structure=structure)
        sizes = np.bincount(labels.ravel())[1:]
        total_patches += int(count)
        records[cls.item() if hasattr(cls, "item") else cls] = {
            "patch_count": int(count),
            "cell_count": int(sizes.sum()),
            "area": float(sizes.sum() * cell_area),
            "mean_patch_area": float(sizes.mean() * cell_area) if count else 0.0,
            "largest_patch_index": float(sizes.max() * cell_area / landscape_area * 100.0)
            if count else 0.0,
            "patch_sizes_cells": sizes.astype(int),
        }

    horizontal = valid[:, :-1] & valid[:, 1:]
    vertical = valid[:-1, :] & valid[1:, :]
    edge_count = int(np.count_nonzero(horizontal & (raster[:, :-1] != raster[:, 1:])))
    edge_count += int(np.count_nonzero(vertical & (raster[:-1, :] != raster[1:, :])))
    edge_length = edge_count * float(cell_size)
    landscape_area_ha = landscape_area / 10_000.0
    return {
        "classes": records,
        "valid_cells": int(valid.sum()),
        "landscape_area": float(landscape_area),
        "total_patch_count": total_patches,
        "edge_count": edge_count,
        "edge_length": float(edge_length),
        "edge_density_per_ha": float(edge_length / landscape_area_ha)
        if landscape_area_ha > 0 else 0.0,
        "connectivity": connectivity,
    }


def shannon_diversity(class_raster, *, nodata=None):
    """Compute Shannon class diversity (natural logarithm) over valid cells."""
    raster = np.asarray(class_raster)
    if raster.ndim != 2 or raster.size == 0:
        raise ValueError("class_raster must be a non-empty 2D array")
    if np.issubdtype(raster.dtype, np.floating):
        finite = np.isfinite(raster)
    else:
        finite = np.ones(raster.shape, dtype=bool)
    valid = finite if nodata is None else finite & (raster != nodata)
    values = raster[valid]
    if values.size == 0:
        raise ValueError("class_raster must contain at least one valid cell")
    _, counts = np.unique(values, return_counts=True)
    proportions = counts / counts.sum()
    return float(-np.sum(proportions * np.log(proportions)))

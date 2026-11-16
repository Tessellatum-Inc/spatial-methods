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

"""Deterministic point-cloud voxel indexing and aggregation."""
from __future__ import annotations
import numpy as np


def voxelize(points, voxel_size, *, origin=None):
    """Group XYZ points into axis-aligned voxels and return summary arrays.

    Voxel coordinates are floor((point-origin)/voxel_size), with half-open
    cells. If origin is omitted, the coordinate-wise minimum point is used.
    """
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 3 or p.shape[0] == 0 or not np.all(np.isfinite(p)):
        raise ValueError("points must be a nonempty finite N x 3 array")
    size = np.asarray(voxel_size, dtype=float)
    if size.ndim == 0:
        size = np.repeat(size, 3)
    if size.shape != (3,) or not np.all(np.isfinite(size)) or np.any(size <= 0):
        raise ValueError("voxel_size must be a positive scalar or three positive values")
    base = np.min(p, axis=0) if origin is None else np.asarray(origin, dtype=float)
    if base.shape != (3,) or not np.all(np.isfinite(base)):
        raise ValueError("origin must contain three finite coordinates")
    coords = np.floor((p - base) / size).astype(np.int64)
    unique, inverse, counts = np.unique(coords, axis=0, return_inverse=True, return_counts=True)
    sums = np.zeros((len(unique), 3), dtype=float)
    np.add.at(sums, inverse, p)
    centroids = sums / counts[:, None]
    minima = np.full((len(unique), 3), np.inf)
    maxima = np.full((len(unique), 3), -np.inf)
    np.minimum.at(minima, inverse, p)
    np.maximum.at(maxima, inverse, p)
    return {"voxel_indices": unique, "point_to_voxel": inverse,
            "counts": counts, "centroids": centroids,
            "minima": minima, "maxima": maxima,
            "origin": base.copy(), "voxel_size": size.copy()}

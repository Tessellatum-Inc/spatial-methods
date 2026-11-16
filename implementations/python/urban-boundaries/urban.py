"""Exploratory urban boundary delineation from building points and density grids."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import label
from sklearn.cluster import DBSCAN


def cluster_building_points(points, *, eps, min_samples=5):
    """DBSCAN building-centroid clusters in a projected coordinate system."""
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2 or len(p) == 0 or not np.all(np.isfinite(p)):
        raise ValueError("points must be a non-empty finite (n, 2) array")
    try:
        radius = float(eps)
    except (TypeError, ValueError):
        raise ValueError("eps must be finite and positive") from None
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("eps must be finite and positive")
    if isinstance(min_samples, (bool, np.bool_)) or not isinstance(min_samples, (int, np.integer)) or min_samples < 1:
        raise ValueError("min_samples must be a positive integer")
    return DBSCAN(eps=radius, min_samples=int(min_samples)).fit_predict(p)


def building_density_grid(points, x_edges, y_edges):
    """Count building centroids in a north-up grid defined by increasing edges."""
    p = np.asarray(points, dtype=float)
    x = np.asarray(x_edges, dtype=float)
    y = np.asarray(y_edges, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2 or not np.all(np.isfinite(p)):
        raise ValueError("points must have shape (n, 2) and finite coordinates")
    if x.ndim != 1 or y.ndim != 1 or len(x) < 2 or len(y) < 2:
        raise ValueError("grid edges must be 1D vectors with at least two values")
    if not np.all(np.isfinite(x)) or not np.all(np.diff(x) > 0) or not np.all(np.isfinite(y)) or not np.all(np.diff(y) > 0):
        raise ValueError("grid edges must be finite and strictly increasing")
    counts, _, _ = np.histogram2d(p[:, 1], p[:, 0], bins=(y, x))
    return counts.astype(np.int64)


def connected_urban_areas(density, *, minimum_density=1, connectivity=8,
                          minimum_cells=1):
    """Label connected cells meeting a building-density threshold."""
    z = np.asarray(density, dtype=float)
    if z.ndim != 2 or not np.all(np.isfinite(z)) or np.any(z < 0):
        raise ValueError("density must be a finite non-negative 2D array")
    if isinstance(minimum_density, (bool, np.bool_)) or not np.isfinite(minimum_density) or minimum_density < 0:
        raise ValueError("minimum_density must be finite and non-negative")
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    if isinstance(minimum_cells, (bool, np.bool_)) or not isinstance(minimum_cells, (int, np.integer)) or minimum_cells < 1:
        raise ValueError("minimum_cells must be a positive integer")
    structure = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=int) if connectivity == 4 else np.ones((3,3), dtype=int)
    raw, count = label(z >= minimum_density, structure=structure)
    sizes = np.bincount(raw.ravel(), minlength=count+1)
    keep = np.flatnonzero(sizes >= minimum_cells)
    keep = keep[keep != 0]
    mask = np.isin(raw, keep)
    labels = np.zeros(raw.shape, dtype=np.int32)
    for new_id, old_id in enumerate(keep, start=1):
        labels[raw == old_id] = new_id
    return {"mask": mask, "labels": labels,
            "sizes": np.asarray([np.count_nonzero(labels == i) for i in range(1, len(keep)+1)], dtype=np.int64)}


def head_tail_natural_city_threshold(density, *, max_iterations=20,
                                     maximum_head_fraction=0.4):
    """Return recursive head/tail threshold and diagnostic split sequence.

    Zero-valued cells are excluded. At each iteration the mean of the current
    heavy tail becomes the next threshold; recursion stops when the head
    fraction is no longer below maximum_head_fraction or only one value remains.
    """
    z = np.asarray(density, dtype=float)
    if z.ndim != 2 or not np.all(np.isfinite(z)) or np.any(z < 0):
        raise ValueError("density must be a finite non-negative 2D array")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    try:
        fraction = float(maximum_head_fraction)
    except (TypeError, ValueError):
        raise ValueError("maximum_head_fraction must be in (0, 0.5]") from None
    if not np.isfinite(fraction) or not 0 < fraction <= 0.5:
        raise ValueError("maximum_head_fraction must be in (0, 0.5]")
    tail = z[z > 0]
    if tail.size == 0:
        return {"threshold": np.inf, "thresholds": [], "iterations": 0}
    thresholds = []
    for _ in range(int(max_iterations)):
        threshold = float(np.mean(tail))
        thresholds.append(threshold)
        head = tail[tail > threshold]
        if head.size == 0 or head.size / tail.size >= fraction:
            break
        tail = head
    return {"threshold": thresholds[-1], "thresholds": thresholds,
            "iterations": len(thresholds)}


def natural_city_candidates(density, **kwargs):
    """Extract connected candidate natural-city cells above a head/tail threshold."""
    result = head_tail_natural_city_threshold(density, **kwargs)
    if not np.isfinite(result["threshold"]):
        mask = np.zeros(np.asarray(density).shape, dtype=bool)
    else:
        mask = np.asarray(density, dtype=float) > result["threshold"]
    return {**result, "mask": mask}

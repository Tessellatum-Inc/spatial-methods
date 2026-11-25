"""Rectangular spatial subsampling intervals for a complete block grid.

This is an experimental subsampling estimator. It deliberately refuses
irregular masks in this first implementation because variable subsample sizes
need a separately justified scaling rule.
"""
from __future__ import annotations
import math
import numpy as np


def spatial_subsampling_mean_interval(
    block_ids, block_values, *, grid_rows: int, grid_columns: int,
    subsample_width_blocks: int, confidence_level: float = 0.95,
    min_subwindows: int = 20,
):
    """Enumerate every b-by-b window and invert the subsampling distribution.

    Statistics are sqrt(m)*(mean_window - mean_full), m=b². If q_lo and q_hi
    are their alpha/2 and 1-alpha/2 quantiles, the interval is
    [mean_full-q_hi/sqrt(m), mean_full-q_lo/sqrt(m)].
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    values = np.asarray(block_values, dtype=float)
    if ids.ndim != 1 or values.ndim != 1 or ids.shape != values.shape:
        raise ValueError("Block IDs and values must be matching one-dimensional arrays")
    if grid_rows < 1 or grid_columns < 1 or subsample_width_blocks < 1:
        raise ValueError("Grid dimensions and subsample width must be positive")
    if not 0 < confidence_level < 1 or min_subwindows < 1:
        raise ValueError("Invalid confidence level or minimum subwindow count")
    if np.any(ids < 0) or np.unique(ids).size != ids.size:
        raise ValueError("block_ids must be non-negative and unique")
    valid = np.isfinite(values)
    ids, values = ids[valid], values[valid]
    n, b = int(values.size), int(subsample_width_blocks)
    estimate = float(values.mean()) if n else None
    base = {
        "estimate": estimate, "lower": None, "upper": None,
        "eligible_blocks": n, "grid_rows": int(grid_rows),
        "grid_columns": int(grid_columns), "subsample_width_blocks": b,
        "subsample_blocks": b*b, "subwindows": 0,
        "interval_status": "insufficient_subwindows",
        "confidence_level": float(confidence_level),
    }
    if n != grid_rows*grid_columns or not np.array_equal(
        np.sort(ids), np.arange(grid_rows*grid_columns, dtype=np.int64)
    ):
        return {**base, "interval_status": "irregular_mask_unsupported"}
    if b > min(grid_rows, grid_columns):
        return {**base, "interval_status": "subsample_larger_than_grid"}
    grid = np.empty((grid_rows, grid_columns), dtype=float)
    grid[ids//grid_columns, ids%grid_columns] = values
    integral = np.pad(grid, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    sums = (integral[b:, b:] - integral[:-b, b:]
            - integral[b:, :-b] + integral[:-b, :-b])
    m = b*b
    stats = math.sqrt(m) * (sums.ravel()/m - estimate)
    count = int(stats.size)
    base["subwindows"] = count
    if count < min_subwindows:
        return base
    alpha = 1.0-confidence_level
    q_lo, q_hi = np.quantile(stats, [alpha/2, 1-alpha/2])
    scale = math.sqrt(m)
    return {
        **base, "lower": float(estimate-q_hi/scale),
        "upper": float(estimate-q_lo/scale),
        "interval_status": "spatial_subsampling",
    }

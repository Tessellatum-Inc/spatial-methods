"""Overlapping moving-window bootstrap for irregular spatial block contrasts.

Candidate windows are every k-by-k lattice window that contains at least one
eligible base block. The origin range is extended beyond the observed grid so
that every eligible base block belongs to exactly k**2 candidate windows,
including at study edges. This equal-inclusion construction avoids the
edge-weighting problem of clipping windows to the observed bounding box.
"""
from __future__ import annotations

import math
import numpy as np


def moving_window_membership(block_ids, *, grid_columns: int, window_width_blocks: int):
    """Return candidate moving windows as arrays of eligible-block indices.

    IDs use row-major encoding: row * grid_columns + column. Windows overlap.
    Empty windows are omitted. Every eligible block appears in exactly
    window_width_blocks**2 candidate windows, regardless of edge position or
    missing cells.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    if ids.ndim != 1:
        raise ValueError("block_ids must be one-dimensional")
    if grid_columns < 1 or window_width_blocks < 1:
        raise ValueError("grid_columns and window_width_blocks must be positive")
    if np.any(ids < 0):
        raise ValueError("block_ids must be non-negative")
    if np.unique(ids).size != ids.size:
        raise ValueError("Each eligible block ID must occur once")
    if ids.size == 0:
        return []

    rows = ids // int(grid_columns)
    cols = ids % int(grid_columns)
    width = int(window_width_blocks)
    windows = {}
    for index, (row, col) in enumerate(zip(rows, cols)):
        for origin_row in range(int(row) - width + 1, int(row) + 1):
            for origin_col in range(int(col) - width + 1, int(col) + 1):
                key = (origin_row, origin_col)
                windows.setdefault(key, []).append(index)
    return [np.asarray(windows[key], dtype=np.int64) for key in sorted(windows)]


def moving_spatial_block_bootstrap_interval(
    block_ids,
    block_values,
    *,
    grid_columns: int,
    window_width_blocks: int,
    replicates: int = 2000,
    seed: int = 20261125,
    min_windows: int = 20,
    min_blocks: int = 20,
):
    """Percentile bootstrap by sampling overlapping k-by-k spatial windows.

    Each replicate samples M/k**2 windows (rounded up) with replacement,
    where M is the number of non-empty candidate windows. Because every
    eligible base block belongs to exactly k**2 candidate windows, all blocks
    have equal first-order inclusion probability, including at edges and in
    irregular masks. The replicate statistic is the mean of the sampled block
    occurrences. Overlap intentionally carries local spatial dependence into
    the resampling distribution.

    This is an experimental moving-window bootstrap, not a calibrated method.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    values = np.asarray(block_values, dtype=float)
    if ids.ndim != 1 or values.ndim != 1 or ids.shape != values.shape:
        raise ValueError("Block IDs and values must be matching one-dimensional arrays")
    if replicates < 1 or min_windows < 1 or min_blocks < 1:
        raise ValueError("replicates, min_windows and min_blocks must be positive")
    if grid_columns < 1 or window_width_blocks < 1:
        raise ValueError("grid_columns and window_width_blocks must be positive")
    if np.any(ids < 0):
        raise ValueError("block_ids must be non-negative")
    if np.unique(ids).size != ids.size:
        raise ValueError("Each eligible block ID must occur once")

    valid = np.isfinite(values)
    ids, values = ids[valid], values[valid]
    base = {
        "estimate_db": float(values.mean()) if values.size else None,
        "lower_95_db": None,
        "upper_95_db": None,
        "eligible_blocks": int(values.size),
        "window_width_blocks": int(window_width_blocks),
        "candidate_windows": 0,
        "windows_per_replicate": 0,
        "interval_status": "insufficient_windows",
        "minimum_windows": int(min_windows),
        "minimum_blocks": int(min_blocks),
        "replicates": 0,
        "seed": int(seed),
    }
    if values.size == 0:
        return base

    if values.size < min_blocks:
        base["interval_status"] = "insufficient_blocks"
        return base

    windows = moving_window_membership(
        ids, grid_columns=grid_columns,
        window_width_blocks=window_width_blocks,
    )
    n_windows = len(windows)
    width_squared = int(window_width_blocks) ** 2
    draws_per_replicate = int(math.ceil(n_windows / width_squared))
    base.update({
        "candidate_windows": n_windows,
        "windows_per_replicate": draws_per_replicate,
        "interval_status": "insufficient_windows",
    })
    if n_windows < min_windows:
        return base

    window_sums = np.fromiter(
        (values[index].sum() for index in windows), dtype=float, count=n_windows
    )
    window_counts = np.fromiter(
        (index.size for index in windows), dtype=np.int64, count=n_windows
    )
    rng = np.random.default_rng(seed)
    sampled = rng.integers(
        0, n_windows, size=(int(replicates), draws_per_replicate)
    )
    # Every eligible block appears in exactly width_squared candidate
    # windows. Therefore a uniformly sampled window sum divided by
    # width_squared is an unbiased estimate of the equal-block population
    # mean, even when irregular masks make window sizes differ. Do not divide
    # by the random number of sampled block occurrences: that ratio can
    # reweight sparse and dense windows under irregular eligibility masks.
    sums = window_sums[sampled].sum(axis=1)
    estimates = sums / (draws_per_replicate * width_squared)
    lower, upper = np.quantile(estimates, [0.025, 0.975])
    return {
        **base,
        "lower_95_db": float(lower),
        "upper_95_db": float(upper),
        "interval_status": "percentile_moving_spatial_block_bootstrap",
        "replicates": int(replicates),
    }

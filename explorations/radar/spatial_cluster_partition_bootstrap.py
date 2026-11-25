"""Spatial superblock partitioning with explicit grid-phase sensitivity."""
from __future__ import annotations

import numpy as np


def spatial_cluster_partition_ids(
    block_ids,
    *,
    grid_columns: int,
    cluster_width_blocks: int,
    origin_row_offset: int = 0,
    origin_col_offset: int = 0,
):
    """Map eligible base-grid IDs to contiguous square superblock IDs.

    Offsets are integer base-block cells in [0, cluster_width_blocks). Varying
    them enumerates distinct phases of the non-overlapping superblock lattice.
    Negative superblock row/column indices at the western/southern boundary are
    intentional and preserve square geometry at every edge.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    if ids.ndim != 1:
        raise ValueError("block_ids must be one-dimensional")
    if grid_columns < 1 or cluster_width_blocks < 1:
        raise ValueError("grid_columns and cluster_width_blocks must be positive")
    if not (0 <= origin_row_offset < cluster_width_blocks):
        raise ValueError("origin_row_offset must be within the cluster width")
    if not (0 <= origin_col_offset < cluster_width_blocks):
        raise ValueError("origin_col_offset must be within the cluster width")
    if np.any(ids < 0):
        raise ValueError("block_ids must be non-negative")
    if np.unique(ids).size != ids.size:
        raise ValueError("Each eligible block ID must occur once")

    rows = ids // int(grid_columns)
    cols = ids % int(grid_columns)
    cluster_rows = np.floor_divide(rows - origin_row_offset, cluster_width_blocks)
    cluster_cols = np.floor_divide(cols - origin_col_offset, cluster_width_blocks)
    _, inverse = np.unique(
        np.column_stack((cluster_rows, cluster_cols)), axis=0, return_inverse=True
    )
    return inverse.astype(np.int64, copy=False)


def spatial_cluster_bootstrap_interval(
    block_ids,
    block_values,
    *,
    grid_columns: int,
    cluster_width_blocks: int,
    origin_row_offset: int = 0,
    origin_col_offset: int = 0,
    replicates: int = 2000,
    seed: int = 20261125,
    min_clusters: int = 20,
):
    """Percentile bootstrap of contiguous superblocks at a declared lattice phase.

    Each replicate samples superblocks with replacement and uses the ratio of
    sampled block-contrast sums to sampled base-block counts. This preserves
    equal weighting of eligible base blocks when edge superblocks are partial.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    values = np.asarray(block_values, dtype=float)
    if ids.ndim != 1 or values.ndim != 1 or ids.shape != values.shape:
        raise ValueError("Block IDs and values must be matching one-dimensional arrays")
    if replicates < 1 or min_clusters < 1:
        raise ValueError("replicates and min_clusters must be positive")
    valid = np.isfinite(values)
    ids, values = ids[valid], values[valid]
    if ids.size == 0:
        return {
            "estimate_db": None, "lower_95_db": None, "upper_95_db": None,
            "eligible_blocks": 0, "eligible_clusters": 0,
            "cluster_width_blocks": int(cluster_width_blocks),
            "origin_row_offset_blocks": int(origin_row_offset),
            "origin_col_offset_blocks": int(origin_col_offset),
            "interval_status": "insufficient_clusters",
            "minimum_clusters": int(min_clusters), "replicates": 0, "seed": int(seed),
        }
    partition = spatial_cluster_partition_ids(
        ids, grid_columns=grid_columns,
        cluster_width_blocks=cluster_width_blocks,
        origin_row_offset=origin_row_offset,
        origin_col_offset=origin_col_offset,
    )
    n_blocks = int(values.size)
    n_clusters = int(np.unique(partition).size)
    cluster_sums = np.bincount(partition, weights=values, minlength=n_clusters)
    cluster_counts = np.bincount(partition, minlength=n_clusters)
    result = {
        "estimate_db": float(values.mean()),
        "lower_95_db": None, "upper_95_db": None,
        "eligible_blocks": n_blocks, "eligible_clusters": n_clusters,
        "cluster_width_blocks": int(cluster_width_blocks),
        "origin_row_offset_blocks": int(origin_row_offset),
        "origin_col_offset_blocks": int(origin_col_offset),
        "interval_status": "insufficient_clusters",
        "minimum_clusters": int(min_clusters), "replicates": 0, "seed": int(seed),
    }
    if n_clusters < min_clusters:
        return result
    rng = np.random.default_rng(seed)
    draw_ids = rng.integers(0, n_clusters, size=(replicates, n_clusters))
    draw_sums = cluster_sums[draw_ids].sum(axis=1)
    draw_counts = cluster_counts[draw_ids].sum(axis=1)
    draws = draw_sums / draw_counts
    lower, upper = np.quantile(draws, [0.025, 0.975])
    return {
        **result, "lower_95_db": float(lower), "upper_95_db": float(upper),
        "interval_status": "percentile_spatial_cluster_bootstrap",
        "replicates": int(replicates),
    }

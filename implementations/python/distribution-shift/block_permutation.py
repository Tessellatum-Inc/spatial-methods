"""Block-level permutation calibration for spatial MMD diagnostics."""
from __future__ import annotations
import numpy as np
from distribution_shift import mmd_squared


def _block_array(blocks, name):
    x = np.asarray(blocks, dtype=float)
    if x.ndim != 3 or min(x.shape) < 1 or x.shape[1] < 2:
        raise ValueError(f"{name} must have shape (n_blocks, equal_block_rows, n_features)")
    if not np.all(np.isfinite(x)):
        raise ValueError(f"{name} must contain only finite values")
    return x


def block_mmd_permutation_test(source_blocks, target_blocks, bandwidth,
                               n_permutations=999, random_state=0):
    """Permute whole equal-sized blocks, never individual spatial rows.

    Validity requires blocks to be mutually independent and exchangeable under
    the null, with a common sampling/measurement design. Blocks should be
    defined from the spatial dependence range and deployment question before
    inspecting the result. This function cannot make a poor block design valid.
    """
    a = _block_array(source_blocks, "source_blocks")
    b = _block_array(target_blocks, "target_blocks")
    if a.shape[1:] != b.shape[1:]:
        raise ValueError("source and target blocks must have equal rows and features")
    if a.shape[0] < 2 or b.shape[0] < 2:
        raise ValueError("at least two blocks are required in each domain")
    if not isinstance(n_permutations, int) or isinstance(n_permutations, bool) or n_permutations < 1:
        raise ValueError("n_permutations must be a positive integer")
    h = float(bandwidth)
    if not np.isfinite(h) or h <= 0:
        raise ValueError("bandwidth must be finite and positive")

    blocks = np.concatenate([a, b], axis=0)
    n_source = a.shape[0]
    observed = mmd_squared(a.reshape(-1, a.shape[-1]),
                           b.reshape(-1, b.shape[-1]), h)
    rng = np.random.default_rng(random_state)
    null = np.empty(n_permutations, dtype=float)
    all_ids = np.arange(blocks.shape[0])
    for i in range(n_permutations):
        order = rng.permutation(all_ids)
        left = blocks[order[:n_source]].reshape(-1, blocks.shape[-1])
        right = blocks[order[n_source:]].reshape(-1, blocks.shape[-1])
        null[i] = mmd_squared(left, right, h)
    p_value = (1 + np.count_nonzero(null >= observed)) / (n_permutations + 1)
    return {
        "statistic": observed,
        "p_value": float(p_value),
        "null_statistics": null,
        "n_source_blocks": int(a.shape[0]),
        "n_target_blocks": int(b.shape[0]),
        "rows_per_block": int(a.shape[1]),
        "permutation_unit": "whole_block",
    }


def _rbf_kernel(a, b, bandwidth):
    squared = (np.sum(a * a, axis=1)[:, None]
               + np.sum(b * b, axis=1)[None, :] - 2 * a @ b.T)
    return np.exp(-np.maximum(squared, 0.0) / (2 * bandwidth ** 2))


def _mmd2_unbiased_from_block_kernel(kernel, labels):
    left = np.flatnonzero(labels == 0)
    right = np.flatnonzero(labels == 1)
    if left.size < 2 or right.size < 2:
        raise ValueError("each group needs at least two exchangeable blocks")
    k_left = kernel[np.ix_(left, left)]
    k_right = kernel[np.ix_(right, right)]
    k_cross = kernel[np.ix_(left, right)]
    return float(
        (k_left.sum() - np.trace(k_left)) / (left.size * (left.size - 1))
        + (k_right.sum() - np.trace(k_right)) / (right.size * (right.size - 1))
        - 2 * k_cross.mean()
    )


def spatial_block_mmd_test(
    features, group_labels, block_ids, *, bandwidth=None,
    permutations=999, alpha=0.05, seed=0,
):
    """Block-kernel MMD with whole-block label permutations.

    Each block belongs to exactly one of two groups. The kernel between two
    blocks is the mean RBF similarity over all cross-block observation pairs.
    This supports unequal block sizes. Validity requires block labels to be
    exchangeable under the null; spatial tiles are not automatically
    independent or exchangeable.
    """
    x = np.asarray(features, dtype=float)
    labels = np.asarray(group_labels)
    blocks = np.asarray(block_ids)
    if x.ndim != 2 or x.shape[0] < 4 or x.shape[1] < 1 or not np.all(np.isfinite(x)):
        raise ValueError("features must be a finite n by d matrix with n >= 4")
    n = x.shape[0]
    if labels.ndim != 1 or blocks.ndim != 1 or labels.size != n or blocks.size != n:
        raise ValueError("group_labels and block_ids must have length n")
    if not np.all(np.isin(labels, [0, 1])) or set(np.unique(labels).tolist()) != {0, 1}:
        raise ValueError("group_labels must contain both binary labels 0 and 1")

    block_rows, block_groups = [], []
    for block in np.unique(blocks):
        indices = np.flatnonzero(blocks == block)
        group = np.unique(labels[indices])
        if group.size != 1:
            raise ValueError("each spatial block must belong to exactly one group")
        block_rows.append(indices)
        block_groups.append(int(group[0]))
    block_labels = np.asarray(block_groups, dtype=int)
    if np.sum(block_labels == 0) < 2 or np.sum(block_labels == 1) < 2:
        raise ValueError("each group needs at least two spatial blocks")

    if bandwidth is None:
        delta = x[:, None, :] - x[None, :, :]
        distances = np.sqrt(np.sum(delta * delta, axis=2))
        positive = distances[np.triu_indices(n, 1)]
        positive = positive[positive > 0]
        if positive.size == 0:
            raise ValueError("automatic bandwidth is undefined for identical feature vectors")
        bandwidth = float(np.median(positive))
    else:
        bandwidth = float(bandwidth)
        if not np.isfinite(bandwidth) or bandwidth <= 0:
            raise ValueError("bandwidth must be finite and positive")
    if isinstance(permutations, bool) or int(permutations) != permutations or permutations < 1:
        raise ValueError("permutations must be a positive integer")
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")

    count = len(block_rows)
    block_kernel = np.empty((count, count), dtype=float)
    for i, rows_i in enumerate(block_rows):
        for j in range(i, count):
            value = float(_rbf_kernel(x[rows_i], x[block_rows[j]], bandwidth).mean())
            block_kernel[i, j] = block_kernel[j, i] = value

    observed = _mmd2_unbiased_from_block_kernel(block_kernel, block_labels)
    rng = np.random.default_rng(seed)
    null = np.empty(int(permutations), dtype=float)
    for i in range(int(permutations)):
        null[i] = _mmd2_unbiased_from_block_kernel(block_kernel, rng.permutation(block_labels))
    p_value = float((1 + np.count_nonzero(null >= observed)) / (int(permutations) + 1))
    return {
        "mmd2_unbiased": observed,
        "p_value": p_value,
        "reject": p_value <= alpha,
        "alpha": float(alpha),
        "bandwidth": bandwidth,
        "permutation_statistics": null,
        "n_observations": n,
        "n_blocks": count,
        "n_blocks_group_0": int(np.sum(block_labels == 0)),
        "n_blocks_group_1": int(np.sum(block_labels == 1)),
        "permutations": int(permutations),
        "seed": seed,
        "permutation_unit": "whole spatial block",
        "validity_assumption": "block labels exchangeable under the null",
    }

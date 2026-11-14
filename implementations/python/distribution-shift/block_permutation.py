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

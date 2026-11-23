"""Empirical pairwise extremal dependence summaries for block maxima."""
from __future__ import annotations
import numpy as np

def _midranks(values):
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(values.size, dtype=float)
    start = 0
    while start < values.size:
        end = start + 1
        while end < values.size and sorted_values[end] == sorted_values[start]:
            end += 1
        ranks[order[start:end]] = 0.5 * ((start + 1) + end)
        start = end
    return ranks

def f_madogram(block_maxima, *, coordinates=None, min_pairs=10):
    """Estimate pairwise F-madograms and max-stable extremal coefficients.

    Rows are blocks and columns are sites. NaN is treated as missing;
    infinities are rejected. Pairwise empirical CDF values use average
    ranks divided by n+1. The extremal-coefficient transform is not clipped,
    so finite-sample estimates outside [1, 2] remain visible diagnostically.
    """
    data = np.asarray(block_maxima, dtype=float)
    if data.ndim != 2 or data.shape[0] < 3 or data.shape[1] < 2:
        raise ValueError("block_maxima must be 2-D with >=3 blocks and >=2 sites")
    if np.any(np.isinf(data)):
        raise ValueError("block_maxima may contain finite values or NaN, not infinity")
    if isinstance(min_pairs, bool) or int(min_pairs) != min_pairs or min_pairs < 3:
        raise ValueError("min_pairs must be an integer of at least three")
    n_sites = data.shape[1]
    valid_counts = np.sum(np.isfinite(data), axis=0)
    if np.any(valid_counts < min_pairs):
        raise ValueError("each site must have at least min_pairs finite block maxima")
    nu = np.zeros((n_sites, n_sites), dtype=float)
    theta = np.ones((n_sites, n_sites), dtype=float)
    counts = np.zeros((n_sites, n_sites), dtype=int)
    np.fill_diagonal(counts, valid_counts)
    for i in range(n_sites):
        for j in range(i + 1, n_sites):
            valid = np.isfinite(data[:, i]) & np.isfinite(data[:, j])
            count = int(np.count_nonzero(valid))
            if count < min_pairs:
                raise ValueError(
                    f"sites {i} and {j} have {count} pairwise-complete blocks; "
                    f"need at least {min_pairs}"
                )
            left = _midranks(data[valid, i]) / (count + 1.0)
            right = _midranks(data[valid, j]) / (count + 1.0)
            estimate = 0.5 * float(np.mean(np.abs(left - right)))
            coefficient = (1.0 + 2.0 * estimate) / (1.0 - 2.0 * estimate)
            nu[i, j] = nu[j, i] = estimate
            theta[i, j] = theta[j, i] = coefficient
            counts[i, j] = counts[j, i] = count
    result = {"f_madogram": nu, "extremal_coefficient": theta, "pair_counts": counts}
    if coordinates is not None:
        xy = np.asarray(coordinates, dtype=float)
        if xy.ndim != 2 or xy.shape[0] != n_sites or xy.shape[1] < 1:
            raise ValueError("coordinates must have one finite row per site")
        if not np.all(np.isfinite(xy)):
            raise ValueError("coordinates must be finite")
        result["distances"] = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=2)
    return result

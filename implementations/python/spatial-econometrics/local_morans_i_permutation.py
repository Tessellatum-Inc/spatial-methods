"""Local Moran's I with conditional randomization and FDR adjustment."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np

Alternative = Literal["two-sided", "greater", "less"]
Adjustment = Literal["none", "bh"]


@dataclass(frozen=True)
class LocalMoranResult:
    local_i: np.ndarray
    expected_value: np.ndarray
    spatial_lag: np.ndarray
    p_values: np.ndarray
    adjusted_p_values: np.ndarray
    cluster_labels: tuple[str, ...]
    permutations: int
    alternative: str
    adjustment: str
    alpha: float


def _benjamini_hochberg(p_values: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values, preserving NaNs for islands."""
    adjusted = np.full(p_values.shape, np.nan, dtype=float)
    valid = np.flatnonzero(np.isfinite(p_values))
    if valid.size == 0:
        return adjusted
    order = valid[np.argsort(p_values[valid], kind="mergesort")]
    ranked = p_values[order] * valid.size / np.arange(1, valid.size + 1)
    monotone = np.minimum.accumulate(ranked[::-1])[::-1]
    adjusted[order] = np.minimum(monotone, 1.0)
    return adjusted


def local_morans_i_permutation(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 999,
    alternative: Alternative = "two-sided",
    adjustment: Adjustment = "bh",
    alpha: float = 0.05,
    seed: int | None = None,
) -> LocalMoranResult:
    """Compute local Moran statistics and conditional permutation p-values.

    For each focal observation i, its centred value is held fixed and the
    remaining centred values are randomly reassigned to all other locations.
    The supplied weights row is held fixed. P-values use the plus-one
    correction. BH adjustment is applied across non-island locations.

    Cluster labels are HH, LL, HL or LH only when the adjusted p-value is
    at most alpha; otherwise they are 'not-significant'. Rows with no outgoing
    weight are islands and receive NaN p-values and the 'island' label.
    """
    x = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    if x.ndim != 1 or x.size < 3:
        raise ValueError("values must be a one-dimensional vector with at least three observations")
    n = x.size
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching values")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(w)):
        raise ValueError("values and weights must contain only finite numbers")
    if np.any(w < 0):
        raise ValueError("weights must be non-negative")
    if np.any(np.diag(w) != 0):
        raise ValueError("weights diagonal must be zero")
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 99:
        raise ValueError("permutations must be an integer of at least 99")
    if alternative not in ("two-sided", "greater", "less"):
        raise ValueError("alternative must be 'two-sided', 'greater' or 'less'")
    if adjustment not in ("none", "bh"):
        raise ValueError("adjustment must be 'none' or 'bh'")
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be strictly between zero and one")

    centred = x - float(np.mean(x))
    m2 = float(centred @ centred / n)
    if not np.isfinite(m2) or m2 <= np.finfo(float).eps:
        raise ValueError("values must have positive variance")
    spatial_lag = w @ centred
    row_sums = w.sum(axis=1)
    local_i = centred * spatial_lag / m2
    expected = -(centred ** 2) * row_sums / ((n - 1) * m2)

    p_values = np.full(n, np.nan, dtype=float)
    rng = np.random.default_rng(seed)
    tolerance = np.finfo(float).eps * 32
    all_indices = np.arange(n)
    for i in range(n):
        if row_sums[i] <= np.finfo(float).eps:
            continue
        other_indices = all_indices[all_indices != i]
        other_values = centred[other_indices]
        simulated = np.empty(permutations, dtype=float)
        row_weights = w[i, other_indices]
        for b in range(permutations):
            permuted = rng.permutation(other_values)
            simulated[b] = centred[i] * float(row_weights @ permuted) / m2
        if alternative == "greater":
            extreme = np.count_nonzero(simulated >= local_i[i] - tolerance)
        elif alternative == "less":
            extreme = np.count_nonzero(simulated <= local_i[i] + tolerance)
        else:
            extreme = np.count_nonzero(
                np.abs(simulated - expected[i])
                >= abs(local_i[i] - expected[i]) - tolerance
            )
        p_values[i] = (extreme + 1.0) / (permutations + 1.0)

    adjusted = p_values.copy() if adjustment == "none" else _benjamini_hochberg(p_values)
    labels = []
    for i in range(n):
        if not np.isfinite(p_values[i]):
            labels.append("island")
        elif adjusted[i] > alpha:
            labels.append("not-significant")
        elif centred[i] >= 0 and spatial_lag[i] >= 0:
            labels.append("HH")
        elif centred[i] < 0 and spatial_lag[i] < 0:
            labels.append("LL")
        elif centred[i] >= 0 and spatial_lag[i] < 0:
            labels.append("HL")
        else:
            labels.append("LH")

    return LocalMoranResult(
        local_i=local_i,
        expected_value=expected,
        spatial_lag=spatial_lag,
        p_values=p_values,
        adjusted_p_values=adjusted,
        cluster_labels=tuple(labels),
        permutations=permutations,
        alternative=alternative,
        adjustment=adjustment,
        alpha=float(alpha),
    )

"""Global Moran's I with randomization-based permutation inference."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np

Alternative = Literal["two-sided", "greater", "less"]


@dataclass(frozen=True)
class MoranPermutationResult:
    statistic: float
    expected_value: float
    permutation_mean: float
    permutation_standard_deviation: float
    p_value: float
    alternative: str
    permutations: int
    simulations: tuple[float, ...]


def morans_i_permutation(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 999,
    alternative: Alternative = "two-sided",
    seed: int | None = None,
) -> MoranPermutationResult:
    """Calculate global Moran's I and a plus-one Monte Carlo permutation p-value.

    The two-sided alternative compares absolute deviations from -1/(n-1).
    Weights are used exactly as supplied; the permutation null treats values
    as exchangeable across the fixed locations.
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
    s0 = float(np.sum(w))
    if not np.isfinite(s0) or s0 <= np.finfo(float).eps:
        raise ValueError("weights must have a positive finite sum")
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 99:
        raise ValueError("permutations must be an integer of at least 99")
    if alternative not in ("two-sided", "greater", "less"):
        raise ValueError("alternative must be 'two-sided', 'greater' or 'less'")
    centred = x - float(np.mean(x))
    denominator = float(centred @ centred)
    if not np.isfinite(denominator) or denominator <= np.finfo(float).eps:
        raise ValueError("values must have positive variance")

    scale = n / s0 / denominator
    observed = float(scale * (centred @ w @ centred))
    expected = -1.0 / (n - 1)
    rng = np.random.default_rng(seed)
    simulated = np.empty(permutations, dtype=float)
    for i in range(permutations):
        permuted = rng.permutation(centred)
        simulated[i] = scale * float(permuted @ w @ permuted)

    tolerance = np.finfo(float).eps * 32
    if alternative == "greater":
        extreme = int(np.count_nonzero(simulated >= observed - tolerance))
    elif alternative == "less":
        extreme = int(np.count_nonzero(simulated <= observed + tolerance))
    else:
        extreme = int(np.count_nonzero(
            np.abs(simulated - expected) >= abs(observed - expected) - tolerance
        ))
    return MoranPermutationResult(
        statistic=observed,
        expected_value=expected,
        permutation_mean=float(np.mean(simulated)),
        permutation_standard_deviation=float(np.std(simulated, ddof=1)),
        p_value=float((extreme + 1.0) / (permutations + 1.0)),
        alternative=alternative,
        permutations=permutations,
        simulations=tuple(float(v) for v in simulated),
    )

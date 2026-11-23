"""Hansen–Hurwitz estimation for independent with-replacement draws."""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class HansenHurwitzResult:
    total_estimate: float
    total_variance_estimate: float | None
    mean_estimate: float | None
    mean_variance_estimate: float | None
    draw_estimates: np.ndarray


def hansen_hurwitz(values, draw_probabilities, *, population_size: int | None = None) -> HansenHurwitzResult:
    """Estimate a finite-population total from independent draws with replacement.

    Each observed value y_i is weighted by its draw probability p_i:
        total_hat = mean(y_i / p_i).
    The estimated variance of the total is s²(y_i / p_i) / n, where s² is
    the sample variance of draw-level estimates. Variance is None for n=1.
    When population_size is supplied, mean and mean-variance estimates are
    returned by dividing the total and its variance by N and N².

    This requires the original ordered draw sequence, independent draws with
    replacement, known strictly positive probabilities for each sampled unit,
    and values corresponding to those same draws. Duplicate draws are retained.
    """
    y = np.asarray(values, dtype=float)
    p = np.asarray(draw_probabilities, dtype=float)
    if y.ndim != 1 or p.ndim != 1 or y.size == 0 or y.shape != p.shape:
        raise ValueError("values and draw_probabilities must be aligned non-empty vectors")
    if not np.isfinite(y).all():
        raise ValueError("values must be finite")
    if not np.isfinite(p).all() or np.any(p <= 0) or np.any(p > 1):
        raise ValueError("draw probabilities must be finite and in (0, 1]")
    if population_size is not None and (isinstance(population_size, bool) or not isinstance(population_size, (int, np.integer)) or population_size <= 0):
        raise ValueError("population_size must be a positive integer")
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        estimates = y / p
        total = float(estimates.mean())
        var_total = float(estimates.var(ddof=1) / y.size) if y.size > 1 else None
        mean = total / population_size if population_size is not None else None
        var_mean = var_total / (population_size ** 2) if var_total is not None and population_size is not None else None
    if not np.isfinite(estimates).all() or not math.isfinite(total):
        raise ValueError("draw estimates or total estimate overflowed to a non-finite value")
    if var_total is not None and not math.isfinite(var_total):
        raise ValueError("variance estimate overflowed to a non-finite value")
    if mean is not None and not math.isfinite(mean):
        raise ValueError("mean estimate overflowed to a non-finite value")
    if var_mean is not None and not math.isfinite(var_mean):
        raise ValueError("mean variance estimate overflowed to a non-finite value")
    return HansenHurwitzResult(total, var_total, mean, var_mean, estimates.copy())

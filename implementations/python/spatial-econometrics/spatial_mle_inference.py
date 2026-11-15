"""Profile-likelihood intervals for the SAR, SEM or SDM spatial parameter.

The interval inverts the one-parameter likelihood-ratio test using the
concentrated Gaussian likelihood and chi-square(1) cutoff. It is conditional
on the supplied W and the estimator's conservative nonsingularity interval.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log, pi
from typing import Sequence

import numpy as np

from maximum_likelihood import (spatial_error_mle, spatial_lag_mle, spatial_durbin_mle, _validate)


@dataclass(frozen=True)
class SpatialParameterInterval:
    model: str
    estimate: float
    lower: float
    upper: float
    likelihood_ratio_cutoff: float
    lower_truncated: bool
    upper_truncated: bool
    log_likelihood_maximum: float


def _sdm_augmented_design(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Build [X, WX] after dropping WX columns already spanned by X."""
    current = x.copy()
    rank = np.linalg.matrix_rank(current)
    for column in (w @ x).T:
        candidate = np.column_stack((current, column))
        next_rank = np.linalg.matrix_rank(candidate)
        if next_rank > rank:
            current = candidate
            rank = next_rank
    return current


def _profile_log_likelihood(y: np.ndarray, x: np.ndarray, w: np.ndarray,
                            parameter: float, model: str) -> float:
    n = y.size
    a = np.eye(n) - parameter * w
    sign, logdet = np.linalg.slogdet(a)
    if sign <= 0 or not np.isfinite(logdet):
        return -np.inf
    ay = y - parameter * (w @ y)
    if model == "SAR":
        transformed_x = x
    elif model == "SEM":
        transformed_x = x - parameter * (w @ x)
    else:
        transformed_x = _sdm_augmented_design(x, w)
    beta, _, rank, _ = np.linalg.lstsq(transformed_x, ay, rcond=None)
    if rank < transformed_x.shape[1]:
        return -np.inf
    residual = ay - transformed_x @ beta
    sigma2 = float(residual @ residual / n)
    if not np.isfinite(sigma2) or sigma2 <= np.finfo(float).tiny:
        return -np.inf
    return float(logdet - n / 2.0 * (log(2.0 * pi) + 1.0 + log(sigma2)))


def _bisect_boundary(function, outside: float, inside: float,
                     cutoff: float, tolerance: float, max_iterations: int) -> float:
    """Find LR=cutoff, with outside outside the set and inside inside it."""
    lo, hi = sorted((outside, inside))
    for _ in range(max_iterations):
        mid = (lo + hi) / 2.0
        if abs(hi - lo) <= tolerance * (1.0 + abs(mid)):
            break
        if function(mid) <= cutoff:
            if outside < inside:
                hi = mid
            else:
                lo = mid
        else:
            if outside < inside:
                lo = mid
            else:
                hi = mid
    return (lo + hi) / 2.0


def spatial_parameter_profile_interval(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    model: str = "SAR",
    likelihood_ratio_cutoff: float = 3.841458820694124,
    grid_size: int = 201,
    tolerance: float = 1e-7,
    max_iterations: int = 100,
) -> SpatialParameterInterval:
    """Invert the LR test for SAR rho, SEM lambda or SDM rho (default 95% cutoff).

    likelihood_ratio_cutoff is the chi-square(1) quantile, 3.8414588 for
    a conventional 95% interval. Endpoints are clipped to the estimator's
    conservative nonsingularity interval when the LR set reaches its edge;
    the corresponding truncation flag is then true.
    """
    if model not in ("SAR", "SEM", "SDM"):
        raise ValueError("model must be 'SAR', 'SEM' or 'SDM'")
    if not np.isfinite(likelihood_ratio_cutoff) or likelihood_ratio_cutoff <= 0:
        raise ValueError("likelihood_ratio_cutoff must be positive and finite")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be positive and finite")

    response, design, w, bounds = _validate(y, x, weights)
    if model == "SAR":
        fit = spatial_lag_mle(response, design, w, grid_size=grid_size, tolerance=tolerance)
    elif model == "SEM":
        fit = spatial_error_mle(response, design, w, grid_size=grid_size, tolerance=tolerance)
    else:
        fit = spatial_durbin_mle(response, design, w, grid_size=grid_size, tolerance=tolerance)
    estimate = fit.spatial_parameter
    maximum = fit.log_likelihood
    lower_bound, upper_bound = bounds

    def lr(value):
        return max(0.0, 2.0 * (maximum - _profile_log_likelihood(
            response, design, w, value, model
        )))

    lower_truncated = lr(lower_bound) <= likelihood_ratio_cutoff
    upper_truncated = lr(upper_bound) <= likelihood_ratio_cutoff
    lower = (lower_bound if lower_truncated else
             _bisect_boundary(lr, lower_bound, estimate, likelihood_ratio_cutoff,
                              tolerance, max_iterations))
    upper = (upper_bound if upper_truncated else
             _bisect_boundary(lr, upper_bound, estimate, likelihood_ratio_cutoff,
                              tolerance, max_iterations))
    if not lower <= estimate <= upper:
        raise ArithmeticError("profile likelihood interval failed to contain its MLE")
    return SpatialParameterInterval(
        model=model, estimate=float(estimate), lower=float(lower), upper=float(upper),
        likelihood_ratio_cutoff=float(likelihood_ratio_cutoff),
        lower_truncated=bool(lower_truncated), upper_truncated=bool(upper_truncated),
        log_likelihood_maximum=float(maximum),
    )

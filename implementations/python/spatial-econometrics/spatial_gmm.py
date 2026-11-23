"""Two-step heteroskedasticity-robust GMM for a spatial-lag model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialLagGMMResult:
    rho: float
    beta: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    covariance: tuple[tuple[float, ...], ...]
    standard_errors: tuple[float, ...]
    j_statistic: float
    j_degrees_of_freedom: int
    first_step_objective: float
    second_step_objective: float
    instruments_used: int
    regressors: int
    instrument_orders: int


def _independent_columns(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    kept: list[int] = []
    current = np.empty((matrix.shape[0], 0), dtype=float)
    rank = 0
    for j in range(matrix.shape[1]):
        candidate = np.column_stack([current, matrix[:, j]])
        next_rank = np.linalg.matrix_rank(candidate, tol=tolerance)
        if next_rank > rank:
            kept.append(j)
            current = candidate
            rank = next_rank
    return matrix[:, kept]


def spatial_lag_gmm(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    instrument_orders: int = 2,
) -> SpatialLagGMMResult:
    """Estimate SAR by two-step efficient GMM with heteroskedasticity-robust moments.

    Structural regressors are [Wy, X]. Instruments are [X, WX, ..., W^q X].
    The first step uses the conventional 2SLS GMM weighting matrix (Z'Z/n)^-1.
    The second step estimates the moment covariance from z_i z_i' u_i^2 and
    uses its inverse as the efficient heteroskedasticity-robust weighting matrix.

    This is a cross-sectional linear IV-GMM estimator. It assumes X and the
    selected spatial lags of X are valid instruments, requires more observations
    than independent instruments, and does not model spatially correlated
    disturbances or automatically establish instrument relevance/exogeneity.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 8:
        raise ValueError("y must be a vector with at least eight observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation")
    if design.shape[1] + 1 >= n:
        raise ValueError("X must leave residual degrees of freedom for the spatial lag")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(w < 0) or np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be non-negative, nonzero and have a zero diagonal")
    if isinstance(instrument_orders, bool) or not isinstance(instrument_orders, int) or instrument_orders < 1:
        raise ValueError("instrument_orders must be a positive integer")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    columns = [design]
    lagged = design.copy()
    for _ in range(instrument_orders):
        lagged = w @ lagged
        columns.append(lagged)
    instruments = _independent_columns(np.column_stack(columns))
    z_count = instruments.shape[1]
    if z_count < design.shape[1] + 1:
        raise ValueError("instruments do not identify the spatial lag model")
    if z_count >= n:
        raise ValueError("sample size must exceed the number of independent instruments")

    regressors = np.column_stack([w @ response, design])
    k = regressors.shape[1]
    if np.linalg.matrix_rank(instruments.T @ regressors) < k:
        raise ValueError("instruments fail the order/rank identification condition")

    ztz = instruments.T @ instruments / n
    if np.linalg.matrix_rank(ztz) < z_count:
        raise ValueError("instrument second moments are singular")
    first_weight = np.linalg.inv(ztz)
    rtz = regressors.T @ instruments / n
    rty = regressors.T @ response / n
    first_normal = rtz @ first_weight @ rtz.T
    if np.linalg.matrix_rank(first_normal) < k:
        raise ValueError("first-step GMM normal matrix is singular")
    first_beta = np.linalg.solve(first_normal, rtz @ first_weight @ (instruments.T @ response / n))
    first_residual = response - regressors @ first_beta
    first_moments = instruments.T @ first_residual / n
    first_objective = float(n * first_moments @ first_weight @ first_moments)

    moment_covariance = (instruments.T * (first_residual ** 2)) @ instruments / n
    if np.linalg.matrix_rank(moment_covariance) < z_count:
        raise ValueError("heteroskedasticity-robust moment covariance is singular")
    second_weight = np.linalg.inv(moment_covariance)
    second_normal = rtz @ second_weight @ rtz.T
    if np.linalg.matrix_rank(second_normal) < k:
        raise ValueError("second-step GMM normal matrix is singular")
    coefficients = np.linalg.solve(
        second_normal,
        rtz @ second_weight @ (instruments.T @ response / n),
    )
    fitted = regressors @ coefficients
    residuals = response - fitted
    moments = instruments.T @ residuals / n
    second_objective = float(n * moments @ second_weight @ moments)

    # Two-step GMM sandwich covariance, using the second-step moment covariance.
    bread = np.linalg.inv(second_normal)
    covariance = bread @ (rtz @ second_weight @ moment_covariance @ second_weight @ rtz.T) @ bread / n
    covariance = (covariance + covariance.T) / 2.0
    diagonal = np.diag(covariance)
    if np.any(diagonal < -1e-10):
        raise ValueError("GMM covariance has materially negative diagonal entries")
    standard_errors = np.sqrt(np.maximum(diagonal, 0.0))
    j_df = z_count - k

    return SpatialLagGMMResult(
        rho=float(coefficients[0]),
        beta=tuple(float(value) for value in coefficients[1:]),
        fitted=tuple(float(value) for value in fitted),
        residuals=tuple(float(value) for value in residuals),
        covariance=tuple(tuple(float(value) for value in row) for row in covariance),
        standard_errors=tuple(float(value) for value in standard_errors),
        j_statistic=second_objective,
        j_degrees_of_freedom=int(j_df),
        first_step_objective=first_objective,
        second_step_objective=second_objective,
        instruments_used=int(z_count),
        regressors=int(k),
        instrument_orders=int(instrument_orders),
    )

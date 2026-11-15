"""Heteroskedastic-robust KP generalized moments for spatial-error dependence.

This is the disturbance-parameter moment stage: callers supply a consistent
predictor of the spatial regression disturbance. It does not estimate the
regression equation or report the full joint KP (2010) covariance.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class HeteroskedasticSpatialErrorGMResult:
    """KP heteroskedastic GM point estimate and its two sample moments."""

    lambda_: float
    moment_objective: float
    moment_residuals: tuple[float, float]
    gamma: tuple[float, float]
    gamma_matrix: tuple[tuple[float, float], tuple[float, float]]
    rho_bounds: tuple[float, float]
    evaluations: int


def _golden_minimum(function, left: float, right: float, tolerance: float = 1e-8):
    ratio = (np.sqrt(5.0) - 1.0) / 2.0
    x1 = right - ratio * (right - left)
    x2 = left + ratio * (right - left)
    f1, f2 = function(x1), function(x2)
    evaluations = 2
    while right - left > tolerance:
        if f1 <= f2:
            right, x2, f2 = x2, x1, f1
            x1 = right - ratio * (right - left)
            f1 = function(x1)
        else:
            left, x1, f1 = x1, x2, f2
            x2 = left + ratio * (right - left)
            f2 = function(x2)
        evaluations += 1
    point = (left + right) / 2.0
    return point, function(point), evaluations + 1


def heteroskedastic_spatial_error_gm(
    residual_predictor: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    rho_bounds: tuple[float, float] = (-0.95, 0.95),
    grid_size: int = 401,
) -> HeteroskedasticSpatialErrorGMResult:
    """Estimate lambda in u = lambda W u + epsilon with heteroskedastic epsilon.

    The caller supplies a consistent predictor u_tilde of the regression
    disturbance. Let v=W u_tilde, w=W v, and d_i=sum_j W_ji^2 (the squared column norms). The two
    heteroskedasticity-robust KP moments are represented as
    gamma - Gamma [lambda, lambda^2]' = 0, where the zero-diagonal quadratic
    forms remove the unknown diagonal innovation-variance contribution.

    Identity weighting gives a consistent nonlinear least-squares GM
    estimator under the KP (2010) regularity and identification conditions.
    This function estimates lambda only. It does not construct u_tilde, fit
    the regression coefficients, provide the full joint asymptotic covariance,
    or perform feasible generalized 2SLS.
    """
    u = np.asarray(residual_predictor, dtype=float)
    matrix = np.asarray(weights, dtype=float)
    if u.ndim != 1 or u.size < 8:
        raise ValueError("residual_predictor must be a vector with at least eight observations")
    n = u.size
    if matrix.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching residual_predictor")
    if not (np.all(np.isfinite(u)) and np.all(np.isfinite(matrix))):
        raise ValueError("residual_predictor and weights must contain only finite values")
    if np.any(np.diag(matrix) != 0) or np.allclose(matrix, 0):
        raise ValueError("weights must be nonzero with a zero diagonal")
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size < 21:
        raise ValueError("grid_size must be an integer of at least 21")
    if (not isinstance(rho_bounds, tuple) or len(rho_bounds) != 2
            or not np.all(np.isfinite(rho_bounds)) or rho_bounds[0] >= rho_bounds[1]):
        raise ValueError("rho_bounds must be a finite increasing pair")

    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(matrix))))
    if spectral_radius <= np.finfo(float).eps:
        raise ValueError("weights must have a positive spectral radius")
    admissible = 1.0 / spectral_radius
    lower, upper = map(float, rho_bounds)
    if lower <= -admissible or upper >= admissible:
        raise ValueError("rho_bounds must lie strictly inside the nonsingularity interval")

    v = matrix @ u
    w = matrix @ v
    column_squared_norms = np.sum(matrix * matrix, axis=0)

    gamma = np.array([
        (v @ v - np.dot(column_squared_norms, u * u)) / n,
        (u @ v) / n,
    ], dtype=float)
    gamma_matrix = np.array([
        [
            2.0 * (v @ w - np.dot(column_squared_norms, u * v)) / n,
            -(w @ w - np.dot(column_squared_norms, v * v)) / n,
        ],
        [
            (v @ v + w @ u) / n,
            -(w @ v) / n,
        ],
    ], dtype=float)

    if not np.all(np.isfinite(gamma)) or not np.all(np.isfinite(gamma_matrix)):
        raise ValueError("spatial-error moments are not finite")
    if np.linalg.matrix_rank(gamma_matrix) < 2:
        raise ValueError("heteroskedastic spatial-error moments do not identify lambda")

    def profile(value: float):
        residual = gamma - gamma_matrix @ np.array([value, value * value])
        return float(residual @ residual)

    grid = np.linspace(lower, upper, grid_size)
    values = np.array([profile(float(value)) for value in grid])
    best = int(np.argmin(values))
    if best == 0 or best == grid_size - 1:
        raise ValueError("spatial-error moment minimum lies on rho_bounds; widen or reconsider bounds")
    estimate, objective, evaluations = _golden_minimum(
        profile, float(grid[best - 1]), float(grid[best + 1])
    )
    residual = gamma - gamma_matrix @ np.array([estimate, estimate * estimate])
    if not np.isfinite(objective):
        raise ValueError("heteroskedastic spatial-error GM objective is not finite")

    return HeteroskedasticSpatialErrorGMResult(
        lambda_=float(estimate),
        moment_objective=float(objective),
        moment_residuals=(float(residual[0]), float(residual[1])),
        gamma=(float(gamma[0]), float(gamma[1])),
        gamma_matrix=tuple(tuple(float(value) for value in row) for row in gamma_matrix),
        rho_bounds=(lower, upper),
        evaluations=int(grid_size + evaluations),
    )

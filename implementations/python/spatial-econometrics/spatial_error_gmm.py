"""Kelejian–Prucha generalized-moments estimation for spatial-error models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialErrorGMMResult:
    """Two-step spatial-error GM/feasible-GLS result (homoskedastic innovations)."""

    lambda_: float
    beta: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    filtered_innovations: tuple[float, ...]
    innovation_variance: float
    covariance: tuple[tuple[float, ...], ...]
    standard_errors: tuple[float, ...]
    moment_objective: float
    moment_residuals: tuple[float, float, float]
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


def spatial_error_gmm(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    rho_bounds: tuple[float, float] = (-0.99, 0.99),
    grid_size: int = 401,
) -> SpatialErrorGMMResult:
    """Estimate y = X beta + u, u = lambda W u + epsilon by KP generalized moments.

    OLS residuals provide a root-N-consistent predictor of u. For each candidate
    lambda, form e(lambda)=(I-lambda W)e and W e(lambda). The three KP moments
    are E[epsilon'epsilon/N]=sigma2, E[(W epsilon)'(W epsilon)/N]
    =sigma2*tr(W'W)/N, and E[(W epsilon)'epsilon/N]=0. A bounded
    nonlinear least-squares fit profiles out sigma2, then feasible GLS filters
    y and X by I-lambda W.

    This is the homoskedastic-innovation KP (1999) estimator, not the
    heteroskedastic extension in Kelejian & Prucha (2010). The dense NumPy
    implementation is intended for teaching-sized matrices.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 8:
        raise ValueError("y must be a vector with at least eight observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be nonzero and have a zero diagonal")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size < 21:
        raise ValueError("grid_size must be an integer of at least 21")
    if (not isinstance(rho_bounds, tuple) or len(rho_bounds) != 2
            or not np.all(np.isfinite(rho_bounds)) or rho_bounds[0] >= rho_bounds[1]):
        raise ValueError("rho_bounds must be a finite increasing pair")
    lower, upper = map(float, rho_bounds)
    if lower < -1.0 or upper > 1.0:
        raise ValueError("rho_bounds must lie within [-1, 1]")

    beta_ols = np.linalg.lstsq(design, response, rcond=None)[0]
    ols_residual = response - design @ beta_ols
    wtw_trace = float(np.sum(w * w))
    if wtw_trace <= 0:
        raise ValueError("weights must have positive squared norm")
    scale = max(float(ols_residual @ ols_residual / n), 1e-12)
    variance_upper = max(100.0 * scale, 1e-8)

    def moments_at(lam: float):
        innovation = ols_residual - lam * (w @ ols_residual)
        spatial_innovation = w @ innovation
        m1 = float(innovation @ innovation / n)
        m2 = float(spatial_innovation @ spatial_innovation / n)
        m3 = float(spatial_innovation @ innovation / n)
        return np.array([m1, m2, m3]), innovation

    trace_scale = wtw_trace / n

    def profile(lam: float):
        raw, _ = moments_at(lam)
        target = np.array([1.0, trace_scale])
        sigma2 = float(np.clip(target @ raw[:2] / (target @ target), 0.0, variance_upper))
        residual = np.array([raw[0] - sigma2, raw[1] - sigma2 * trace_scale, raw[2]])
        return float(residual @ residual), sigma2, residual

    grid = np.linspace(lower, upper, grid_size)
    values = np.array([profile(float(value))[0] for value in grid])
    best = int(np.argmin(values))
    if best == 0 or best == grid_size - 1:
        raise ValueError("spatial-error moment minimum lies on rho_bounds; widen or reconsider bounds")
    lam, objective, evaluations = _golden_minimum(
        lambda value: profile(value)[0], float(grid[best - 1]), float(grid[best + 1])
    )
    objective, sigma2, moment_residual = profile(lam)
    if sigma2 <= 0 or not np.isfinite(objective):
        raise ValueError("spatial-error moments did not identify a positive innovation variance")

    transform = np.eye(n) - lam * w
    if np.linalg.matrix_rank(transform) < n or np.linalg.cond(transform) > 1e12:
        raise ValueError("I - lambda W is singular or numerically ill-conditioned at the estimate")
    filtered_y = transform @ response
    filtered_x = transform @ design
    normal = filtered_x.T @ filtered_x
    if np.linalg.matrix_rank(normal) < design.shape[1]:
        raise ValueError("feasible-GLS design is rank deficient")
    covariance_base = np.linalg.inv(normal)
    beta = np.linalg.solve(normal, filtered_x.T @ filtered_y)
    fitted = design @ beta
    residuals = response - fitted
    covariance = sigma2 * covariance_base
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    filtered_innovations = transform @ residuals

    return SpatialErrorGMMResult(
        lambda_=float(lam),
        beta=tuple(float(value) for value in beta),
        fitted=tuple(float(value) for value in fitted),
        residuals=tuple(float(value) for value in residuals),
        filtered_innovations=tuple(float(value) for value in filtered_innovations),
        innovation_variance=float(sigma2),
        covariance=tuple(tuple(float(value) for value in row) for row in covariance),
        standard_errors=tuple(float(value) for value in standard_errors),
        moment_objective=float(objective),
        moment_residuals=tuple(float(value) for value in moment_residual),
        rho_bounds=(lower, upper),
        evaluations=int(grid_size + evaluations),
    )

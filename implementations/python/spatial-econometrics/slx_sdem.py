"""SLX and SDEM estimators for spatially lagged covariates."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from maximum_likelihood import spatial_error_mle


@dataclass(frozen=True)
class SLXFit:
    coefficients: tuple[float, ...]
    spatial_covariate_coefficients: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    sigma2_ols: float
    rank: int


@dataclass(frozen=True)
class SDEMFit:
    error_parameter: float
    coefficients: tuple[float, ...]
    spatial_covariate_coefficients: tuple[float, ...]
    sigma2_mle: float
    log_likelihood: float
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    parameter_bounds: tuple[float, float]
    evaluations: int


def _prepare(y, x, weights, *, minimum_n=5):
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < minimum_n:
        raise ValueError(f"y must be a vector with at least {minimum_n} observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation and at least one column")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(w < 0) or np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be non-negative, nonzero and have a zero diagonal")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    return response, design, w


def _expanded_design(design: np.ndarray, w: np.ndarray):
    """Return [X, selected WX] and original WX-column indices."""
    wx = w @ design
    expanded = design.copy()
    selected = []
    rank = np.linalg.matrix_rank(expanded)
    for j in range(wx.shape[1]):
        candidate = np.column_stack([expanded, wx[:, j]])
        next_rank = np.linalg.matrix_rank(candidate)
        if next_rank > rank:
            expanded = candidate
            selected.append(j)
            rank = next_rank
    return expanded, selected, wx


def spatial_lx_ols(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
) -> SLXFit:
    """Estimate the SLX model y = X beta + W X gamma + epsilon by OLS.

    Spatially lagged columns exactly collinear with the included design are
    omitted and their reported gamma coefficients are set to zero. In
    particular, W times an intercept is redundant for row-standardised W.
    """
    response, design, w = _prepare(y, x, weights)
    expanded, selected, wx = _expanded_design(design, w)
    if expanded.shape[1] >= response.size:
        raise ValueError("SLX design must leave residual degrees of freedom")
    coefficients, _, rank, _ = np.linalg.lstsq(expanded, response, rcond=None)
    if rank < expanded.shape[1]:
        raise ValueError("expanded SLX design is rank deficient")
    fitted = expanded @ coefficients
    residuals = response - fitted
    sigma2 = float(residuals @ residuals / (response.size - expanded.shape[1]))
    beta = coefficients[:design.shape[1]]
    gamma = np.zeros(design.shape[1], dtype=float)
    for coefficient, original_index in zip(coefficients[design.shape[1]:], selected):
        gamma[original_index] = coefficient
    return SLXFit(
        coefficients=tuple(float(v) for v in beta),
        spatial_covariate_coefficients=tuple(float(v) for v in gamma),
        fitted=tuple(float(v) for v in fitted),
        residuals=tuple(float(v) for v in residuals),
        sigma2_ols=sigma2,
        rank=int(rank),
    )


def spatial_dem_mle(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    grid_size: int = 81,
    tolerance: float = 1e-6,
) -> SDEMFit:
    """Estimate SDEM: y = X beta + WX gamma + u; u = lambda W u + e.

    The existing concentrated SEM likelihood is applied to the independent
    columns of [X, WX]. This estimates a spatial-error process, not a spatial
    lag of y. A row-standardised intercept's WX column is dropped as redundant.
    """
    response, design, w = _prepare(y, x, weights)
    expanded, selected, _ = _expanded_design(design, w)
    if expanded.shape[1] >= response.size - 1:
        raise ValueError("SDEM design must leave residual degrees of freedom")
    fit = spatial_error_mle(
        response, expanded, w, grid_size=grid_size, tolerance=tolerance
    )
    beta = fit.coefficients[:design.shape[1]]
    gamma = np.zeros(design.shape[1], dtype=float)
    for coefficient, original_index in zip(
        fit.coefficients[design.shape[1]:], selected
    ):
        gamma[original_index] = coefficient
    return SDEMFit(
        error_parameter=fit.spatial_parameter,
        coefficients=tuple(float(v) for v in beta),
        spatial_covariate_coefficients=tuple(float(v) for v in gamma),
        sigma2_mle=fit.sigma2_mle,
        log_likelihood=fit.log_likelihood,
        fitted=fit.fitted,
        residuals=fit.residuals,
        parameter_bounds=fit.rho_bounds,
        evaluations=fit.evaluations,
    )

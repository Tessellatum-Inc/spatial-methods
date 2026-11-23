"""Instrumental-variables estimator for the spatial Durbin model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialDurbin2SLSResult:
    rho: float
    beta: tuple[float, ...]
    gamma: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    instruments_used: int
    regressors: int


def _append_independent(current: np.ndarray, candidate: np.ndarray,
                        tolerance: float = 1e-10) -> np.ndarray:
    """Append candidate columns only when they increase matrix rank."""
    result = current
    rank = np.linalg.matrix_rank(result, tol=tolerance) if result.shape[1] else 0
    for j in range(candidate.shape[1]):
        trial = np.column_stack([result, candidate[:, j]])
        next_rank = np.linalg.matrix_rank(trial, tol=tolerance)
        if next_rank > rank:
            result = trial
            rank = next_rank
    return result


def spatial_durbin_2sls(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    instrument_orders: int = 2,
) -> SpatialDurbin2SLSResult:
    """Estimate y = rho Wy + X beta + WX gamma + epsilon by 2SLS.

    X and WX are included as exogenous regressors. Wy is endogenous and is
    instrumented using excluded higher-order spatial lags W²X, ..., W^qX.
    The instrument matrix also includes all included exogenous regressors.
    Linearly dependent columns are removed in stable order, which handles
    row-standardised intercepts (W 1 = 1).

    This assumes X and its spatial lags are exogenous and that the excluded
    higher-order lags are relevant. It does not calculate standard errors,
    weak-instrument diagnostics or robust GMM covariance estimates.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 8:
        raise ValueError("y must be a vector with at least eight observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation")
    if design.shape[1] * 2 + 1 >= n:
        raise ValueError("X must leave residual degrees of freedom for the SDM")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(w < 0) or np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be non-negative, nonzero and have a zero diagonal")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    if isinstance(instrument_orders, bool) or not isinstance(instrument_orders, int) or instrument_orders < 2:
        raise ValueError("instrument_orders must be an integer of at least 2")

    wx = w @ design
    included_exogenous = design.copy()
    included_wx_indices = []
    for j in range(wx.shape[1]):
        expanded = np.column_stack([included_exogenous, wx[:, j]])
        if np.linalg.matrix_rank(expanded, tol=1e-10) > np.linalg.matrix_rank(included_exogenous, tol=1e-10):
            included_exogenous = expanded
            included_wx_indices.append(j)
    wy = w @ response
    structural = np.column_stack([wy, included_exogenous])

    # The instrument matrix includes every included exogenous regressor.
    # Only spatial lags of order two and above are excluded instruments.
    instruments = included_exogenous.copy()
    spatial_lag = wx.copy()
    for _ in range(2, instrument_orders + 1):
        spatial_lag = w @ spatial_lag
        instruments = _append_independent(instruments, spatial_lag)

    if instruments.shape[1] < structural.shape[1]:
        raise ValueError("underidentified SDM: fewer independent instruments than regressors")
    if np.linalg.matrix_rank(instruments) < structural.shape[1]:
        raise ValueError("underidentified SDM: instrument matrix lacks required rank")

    projected_structural = instruments @ np.linalg.lstsq(instruments, structural, rcond=None)[0]
    projected_response = instruments @ np.linalg.lstsq(instruments, response, rcond=None)[0]
    if np.linalg.matrix_rank(projected_structural) < structural.shape[1]:
        raise ValueError("underidentified SDM: projected regressors lack full column rank")
    coefficients = np.linalg.lstsq(projected_structural, projected_response, rcond=None)[0]
    rho = float(coefficients[0])
    exogenous_coefficients = coefficients[1:]
    beta = exogenous_coefficients[:design.shape[1]]
    gamma = np.zeros(design.shape[1], dtype=float)
    for coefficient, j in zip(exogenous_coefficients[design.shape[1]:], included_wx_indices):
        gamma[j] = coefficient

    fitted = rho * wy + design @ beta + wx @ gamma
    residuals = response - fitted
    return SpatialDurbin2SLSResult(
        rho=rho,
        beta=tuple(float(v) for v in beta),
        gamma=tuple(float(v) for v in gamma),
        fitted=tuple(float(v) for v in fitted),
        residuals=tuple(float(v) for v in residuals),
        instruments_used=int(instruments.shape[1]),
        regressors=int(structural.shape[1]),
    )

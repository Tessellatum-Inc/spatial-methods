"""Instrumental-variables 2SLS baseline for a spatial lag regression."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Spatial2SLSResult:
    rho: float
    beta: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    instruments_used: int
    regressors: int


def _independent_columns(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    """Keep columns in input order, dropping numerical linear dependencies."""
    kept = []
    current = np.empty((matrix.shape[0], 0), dtype=float)
    rank = 0
    for column in range(matrix.shape[1]):
        candidate = np.column_stack([current, matrix[:, column]])
        next_rank = np.linalg.matrix_rank(candidate, tol=tolerance)
        if next_rank > rank:
            kept.append(column)
            current = candidate
            rank = next_rank
    return matrix[:, kept]


def spatial_lag_2sls(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    instrument_orders: int = 1,
) -> Spatial2SLSResult:
    """Estimate y = rho W y + X beta + error by spatial 2SLS.

    Instruments are constructed as [X, WX, ..., W^q X]. Linearly dependent
    instrument columns are removed in stable input order (important when a
    row-standardised W maps an intercept column back to itself).

    This teaching estimator assumes X is exogenous and the selected spatial
    lags of X are valid, relevant instruments. It does not estimate spatial
    error dependence, calculate standard errors, or implement Kelejian-Prucha
    heteroskedasticity-robust GMM.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 4:
        raise ValueError("y must be a vector with at least four observations")
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
    if np.any(w < 0) or np.any(np.diag(w) != 0):
        raise ValueError("weights must be non-negative with a zero diagonal")
    if np.allclose(w, 0):
        raise ValueError("weights must contain a nonzero connection")
    if (isinstance(instrument_orders, bool)
            or not isinstance(instrument_orders, int)
            or instrument_orders < 1):
        raise ValueError("instrument_orders must be a positive integer")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    instruments = [design]
    lagged = design.copy()
    for _ in range(instrument_orders):
        lagged = w @ lagged
        instruments.append(lagged)
    z = _independent_columns(np.column_stack(instruments))
    if z.shape[1] < design.shape[1] + 1:
        raise ValueError("instruments do not identify the spatial lag and regression coefficients")

    spatial_lag = w @ response
    regressors = np.column_stack([spatial_lag, design])
    projected = z @ np.linalg.lstsq(z, regressors, rcond=None)[0]
    if np.linalg.matrix_rank(projected) < regressors.shape[1]:
        raise ValueError("instrumented regressors are rank deficient; model is underidentified")
    beta_all = np.linalg.lstsq(projected, z @ np.linalg.lstsq(z, response, rcond=None)[0],
                               rcond=None)[0]
    fitted = regressors @ beta_all
    residuals = response - fitted
    return Spatial2SLSResult(
        rho=float(beta_all[0]),
        beta=tuple(float(value) for value in beta_all[1:]),
        fitted=tuple(float(value) for value in fitted),
        residuals=tuple(float(value) for value in residuals),
        instruments_used=int(z.shape[1]),
        regressors=int(regressors.shape[1]),
    )

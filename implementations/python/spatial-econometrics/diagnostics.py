"""Classic Lagrange Multiplier diagnostics for spatial dependence after OLS.

This is a dense-matrix teaching implementation of the classic LM-lag and
LM-error tests. It does not implement robust LM variants or estimate SAR/SEM.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import erfc, isfinite, sqrt
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialLMResult:
    statistic: float
    p_value: float
    degrees_of_freedom: int = 1


@dataclass(frozen=True)
class SpatialDiagnostics:
    coefficients: tuple[float, ...]
    residuals: tuple[float, ...]
    sigma2_mle: float
    lm_lag: SpatialLMResult
    lm_error: SpatialLMResult
    trace_term: float
    lag_denominator: float


def _inputs(y: Sequence[float], x: Sequence[Sequence[float]],
            weights: Sequence[Sequence[float]]):
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 3:
        raise ValueError("y must be a one-dimensional vector with at least three observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must be a two-dimensional matrix with one row per observation")
    if design.shape[1] >= n:
        raise ValueError("X must leave positive residual degrees of freedom")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(w < 0):
        raise ValueError("weights must be non-negative")
    if np.any(np.diag(w) != 0):
        raise ValueError("weights diagonal must be zero")
    if np.allclose(w, 0):
        raise ValueError("weights must contain at least one nonzero connection")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    return response, design, w


def _chi_square_1_sf(value: float) -> float:
    return erfc(sqrt(max(0.0, value) / 2.0))


def spatial_lm_diagnostics(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
) -> SpatialDiagnostics:
    """Calculate classic LM-lag and LM-error tests from an OLS regression.

    LM-error = (e' W e / sigma2)^2 / T, where
    T = tr(W'W + W^2).

    LM-lag = (e' W y / sigma2)^2 / D, where
    D = (W X beta)' M (W X beta) / sigma2 + T and M is
    the residual-maker for X. Both statistics are asymptotic chi-square(1).

    These are classic (not robust) score tests. They are diagnostics, not a
    rule that automatically selects a model. Use a maintained spatial
    econometrics package for estimation and robust LM variants.
    """
    response, design, w = _inputs(y, x, weights)
    n = response.size
    beta, _, _, _ = np.linalg.lstsq(design, response, rcond=None)
    residual = response - design @ beta
    sigma2 = float(residual @ residual / n)
    if not isfinite(sigma2) or sigma2 <= np.finfo(float).eps:
        raise ValueError("OLS residual variance must be positive")
    trace_term = float(np.trace(w.T @ w + w @ w))
    if not isfinite(trace_term) or trace_term <= np.finfo(float).eps:
        raise ValueError("weights produce a zero LM trace term")
    we = w @ residual
    wy = w @ response
    lm_error = float((residual @ we / sigma2) ** 2 / trace_term)

    wx_beta = w @ (design @ beta)
    # M v = v - X (X'X)^-1 X'v, evaluated with a least-squares projection.
    projected = design @ np.linalg.lstsq(design, wx_beta, rcond=None)[0]
    residualised_wx_beta = wx_beta - projected
    lag_denominator = float(
        residualised_wx_beta @ residualised_wx_beta / sigma2 + trace_term
    )
    lm_lag = float((residual @ wy / sigma2) ** 2 / lag_denominator)
    return SpatialDiagnostics(
        coefficients=tuple(float(v) for v in beta),
        residuals=tuple(float(v) for v in residual),
        sigma2_mle=sigma2,
        lm_lag=SpatialLMResult(lm_lag, _chi_square_1_sf(lm_lag)),
        lm_error=SpatialLMResult(lm_error, _chi_square_1_sf(lm_error)),
        trace_term=trace_term,
        lag_denominator=lag_denominator,
    )

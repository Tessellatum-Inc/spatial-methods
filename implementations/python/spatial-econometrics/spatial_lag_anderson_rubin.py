"""Anderson–Rubin tests for a proposed spatial-lag coefficient."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialLagAndersonRubinResult:
    """Joint-exclusion tests for one candidate value of the SAR coefficient."""

    rho_null: float
    classical_f: float
    classical_f_numerator_df: int
    classical_f_denominator_df: int
    robust_wald_chi2: float
    robust_wald_degrees_of_freedom: int
    excluded_instruments: int
    instruments_used: int
    transformed_coefficients: tuple[float, ...]
    transformed_residual_variance: float


def _independent_columns(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    """Keep linearly independent columns in stable input order."""
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


def spatial_lag_anderson_rubin(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    rho_null: float,
    *,
    instrument_orders: int = 2,
) -> SpatialLagAndersonRubinResult:
    """Test H0: rho = rho_null in y = rho W y + X beta + u.

    Under the null, transform the response to y0 = y - rho_null W y.
    Regress y0 on [X, WX, ..., W^q X] and test joint exclusion of the
    independent columns beyond X. The classical partial F is exact under
    the conventional iid homoskedastic Gaussian linear-model assumptions.
    The HC1 Wald chi-square is a heteroskedasticity-robust asymptotic test
    under independent-observation sampling; it is not spatial-HAC robust.

    This Anderson–Rubin construction does not require strong instruments for
    its null-size argument, but it still requires valid excluded instruments.
    It tests one supplied candidate value; it does not invert the test into a
    confidence set, which may be unbounded or disjoint.
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
    if np.any(w < 0) or np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be non-negative, nonzero and have a zero diagonal")
    if (isinstance(instrument_orders, bool)
            or not isinstance(instrument_orders, int)
            or instrument_orders < 1):
        raise ValueError("instrument_orders must be a positive integer")
    if not np.isscalar(rho_null) or not np.isfinite(rho_null):
        raise ValueError("rho_null must be a finite scalar")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    columns = [design]
    lagged = design.copy()
    for _ in range(instrument_orders):
        lagged = w @ lagged
        columns.append(lagged)
    instruments = _independent_columns(np.column_stack(columns))
    exogenous_count = design.shape[1]
    if instruments.shape[1] <= exogenous_count:
        raise ValueError("no independent excluded spatial instruments remain")
    p = instruments.shape[1]
    q = p - exogenous_count
    denominator_df = n - p
    if denominator_df <= 0:
        raise ValueError("sample size must exceed the retained instrument count")

    transformed = response - float(rho_null) * (w @ response)
    restricted_beta = np.linalg.lstsq(design, transformed, rcond=None)[0]
    restricted_residuals = transformed - design @ restricted_beta
    restricted_ssr = float(restricted_residuals @ restricted_residuals)
    coefficients = np.linalg.lstsq(instruments, transformed, rcond=None)[0]
    residuals = transformed - instruments @ coefficients
    unrestricted_ssr = float(residuals @ residuals)
    if restricted_ssr <= np.finfo(float).eps:
        raise ValueError("restricted transformed regression has no residual variation")
    residual_variance = unrestricted_ssr / denominator_df
    if residual_variance <= np.finfo(float).eps:
        raise ValueError("unrestricted transformed regression has zero residual variance")
    improvement = max(restricted_ssr - unrestricted_ssr, 0.0)
    classical_f = (improvement / q) / residual_variance

    bread = np.linalg.inv(instruments.T @ instruments)
    meat = (instruments.T * (residuals ** 2)) @ instruments
    covariance = (n / denominator_df) * bread @ meat @ bread
    covariance = (covariance + covariance.T) / 2.0
    excluded = coefficients[exogenous_count:]
    excluded_covariance = covariance[exogenous_count:, exogenous_count:]
    if np.linalg.matrix_rank(excluded_covariance) < q:
        raise ValueError("HC1 covariance for excluded instruments is singular")
    robust_chi2 = float(excluded @ np.linalg.solve(excluded_covariance, excluded))
    if not np.isfinite(robust_chi2) or robust_chi2 < -1e-10:
        raise ValueError("robust Anderson–Rubin statistic is not finite and non-negative")

    return SpatialLagAndersonRubinResult(
        rho_null=float(rho_null),
        classical_f=float(max(classical_f, 0.0)),
        classical_f_numerator_df=int(q),
        classical_f_denominator_df=int(denominator_df),
        robust_wald_chi2=float(max(robust_chi2, 0.0)),
        robust_wald_degrees_of_freedom=int(q),
        excluded_instruments=int(q),
        instruments_used=int(p),
        transformed_coefficients=tuple(float(v) for v in coefficients),
        transformed_residual_variance=float(residual_variance),
    )

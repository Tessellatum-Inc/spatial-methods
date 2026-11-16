"""First-stage relevance diagnostics for spatial-lag IV estimators."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialLagInstrumentDiagnostics:
    """First-stage relevance summaries for the endogenous spatial lag Wy."""

    partial_r_squared: float
    classical_partial_f: float
    classical_f_numerator_df: int
    classical_f_denominator_df: int
    robust_wald_f: float
    robust_f_numerator_df: int
    robust_f_denominator_df: int
    excluded_instruments: int
    instruments_used: int
    first_stage_coefficients: tuple[float, ...]
    first_stage_standard_errors_hc1: tuple[float, ...]
    first_stage_residual_variance: float


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


def spatial_lag_instrument_diagnostics(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    instrument_orders: int = 2,
) -> SpatialLagInstrumentDiagnostics:
    """Assess excluded spatial-lag instrument relevance in the Wy first stage.

    The endogenous first-stage outcome is Wy. The unrestricted first stage
    regresses Wy on [X, WX, ..., W^q X], while the restricted model uses X only.
    Redundant columns are removed in stable order. Returned statistics are the
    classical partial F and an HC1 heteroskedasticity-robust Wald F for the
    joint null that all retained excluded-instrument coefficients are zero.

    The robust statistic is a first-stage Wald diagnostic, not the
    Kleibergen–Paap rk statistic. Neither statistic establishes instrument
    exogeneity, and conventional F cutoffs are not universal weak-instrument
    guarantees. The HC1 covariance assumes independent observations; it does
    not correct spatially correlated first-stage disturbances.
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
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    endogenous = w @ response
    columns = [design]
    lagged = design.copy()
    for _ in range(instrument_orders):
        lagged = w @ lagged
        columns.append(lagged)
    full_design = _independent_columns(np.column_stack(columns))
    exogenous_count = design.shape[1]
    if full_design.shape[1] <= exogenous_count:
        raise ValueError("no independent excluded spatial instruments remain")
    p = full_design.shape[1]
    q = p - exogenous_count
    denominator_df = n - p
    if denominator_df <= 0:
        raise ValueError("sample size must exceed the first-stage instrument count")

    restricted_beta = np.linalg.lstsq(design, endogenous, rcond=None)[0]
    restricted_residual = endogenous - design @ restricted_beta
    restricted_ssr = float(restricted_residual @ restricted_residual)
    coefficients = np.linalg.lstsq(full_design, endogenous, rcond=None)[0]
    residuals = endogenous - full_design @ coefficients
    unrestricted_ssr = float(residuals @ residuals)
    if restricted_ssr <= np.finfo(float).eps:
        raise ValueError("restricted first stage has no residual variation to explain")
    improvement = max(restricted_ssr - unrestricted_ssr, 0.0)
    partial_r2 = improvement / restricted_ssr
    residual_variance = unrestricted_ssr / denominator_df
    if residual_variance <= np.finfo(float).eps:
        raise ValueError("unrestricted first stage has zero residual variance")
    classical_f = (improvement / q) / residual_variance

    cross = full_design.T @ full_design
    bread = np.linalg.inv(cross)
    meat = (full_design.T * (residuals ** 2)) @ full_design
    covariance = (n / denominator_df) * bread @ meat @ bread
    covariance = (covariance + covariance.T) / 2.0
    excluded_coefficients = coefficients[exogenous_count:]
    excluded_covariance = covariance[exogenous_count:, exogenous_count:]
    if np.linalg.matrix_rank(excluded_covariance) < q:
        raise ValueError("HC1 covariance for excluded first-stage instruments is singular")
    robust_wald_f = float(
        excluded_coefficients @ np.linalg.solve(excluded_covariance, excluded_coefficients) / q
    )
    if robust_wald_f < -1e-10 or not np.isfinite(robust_wald_f):
        raise ValueError("robust first-stage Wald statistic is not finite and non-negative")
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))

    return SpatialLagInstrumentDiagnostics(
        partial_r_squared=float(np.clip(partial_r2, 0.0, 1.0)),
        classical_partial_f=float(max(classical_f, 0.0)),
        classical_f_numerator_df=int(q),
        classical_f_denominator_df=int(denominator_df),
        robust_wald_f=float(max(robust_wald_f, 0.0)),
        robust_f_numerator_df=int(q),
        robust_f_denominator_df=int(denominator_df),
        excluded_instruments=int(q),
        instruments_used=int(p),
        first_stage_coefficients=tuple(float(v) for v in coefficients),
        first_stage_standard_errors_hc1=tuple(float(v) for v in standard_errors),
        first_stage_residual_variance=float(residual_variance),
    )

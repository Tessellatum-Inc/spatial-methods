"""Three-step heteroskedastic SARAR estimation by KP generalized spatial 2SLS."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from heteroskedastic_spatial_error_gm import heteroskedastic_spatial_error_gm
from spatial_sarar_joint_covariance import spatial_sarar_joint_covariance


@dataclass(frozen=True)
class SpatialSARARGTSLSResult:
    """Three-step SARAR point estimates with conditional and joint KP covariance."""

    rho: float
    lambda_: float
    beta: tuple[float, ...]
    coefficients: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    filtered_residuals: tuple[float, ...]
    covariance_hc1_conditional: tuple[tuple[float, ...], ...]
    standard_errors_hc1_conditional: tuple[float, ...]
    covariance_joint_kp: tuple[tuple[float, ...], ...]
    standard_errors_joint_kp: tuple[float, ...]
    instruments_used: int
    first_stage_rank: int
    transformed_stage_rank: int


def _independent_columns(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    keep: list[int] = []
    current = np.empty((matrix.shape[0], 0), dtype=float)
    rank = 0
    for j in range(matrix.shape[1]):
        candidate = np.column_stack([current, matrix[:, j]])
        next_rank = np.linalg.matrix_rank(candidate, tol=tolerance)
        if next_rank > rank:
            keep.append(j)
            current, rank = candidate, next_rank
    return matrix[:, keep]


def spatial_sarar_gtsls(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    instrument_orders: int = 2,
    rho_bounds: tuple[float, float] = (-0.95, 0.95),
    grid_size: int = 401,
) -> SpatialSARARGTSLSResult:
    """Fit y = rho W y + X beta + u; u = lambda W u + epsilon.

    Implements the three-step Kelejian–Prucha (2010) procedure for W=M:
    (1) spatial-lag 2SLS using H=[X, WX, ..., W^q X];
    (2) estimate lambda by the heteroskedastic two-moment GM procedure from
        the first-stage IV residuals;
    (3) Cochrane–Orcutt transform y and [X, Wy] by I-lambda W and re-run
        2SLS using the original H instruments.

    The result includes both a conditional HC1 sandwich and the KP (2010)
    plug-in joint asymptotic covariance for [beta..., rho, lambda]. The joint
    covariance accounts for generated first-stage residuals and cross-
    covariance between the final transformed IV score and the GM moments.
    It uses identity weighting for the GM moments and the common-weights case
    M=W; it is not a finite-sample exact or spatial-HAC covariance.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 10:
        raise ValueError("y must be a vector with at least ten observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be nonzero with a zero diagonal")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    if isinstance(instrument_orders, bool) or not isinstance(instrument_orders, int) or instrument_orders < 1:
        raise ValueError("instrument_orders must be a positive integer")
    if not isinstance(rho_bounds, tuple) or len(rho_bounds) != 2 or not np.all(np.isfinite(rho_bounds)) or rho_bounds[0] >= rho_bounds[1]:
        raise ValueError("rho_bounds must be a finite increasing pair")

    instrument_blocks = [design]
    lagged = design.copy()
    for _ in range(instrument_orders):
        lagged = w @ lagged
        instrument_blocks.append(lagged)
    h = _independent_columns(np.column_stack(instrument_blocks))
    z = np.column_stack([design, w @ response])
    k = z.shape[1]
    if h.shape[1] < k:
        raise ValueError("instrument matrix has fewer columns than endogenous regressors")
    if np.linalg.matrix_rank(h) < h.shape[1]:
        raise ValueError("instrument matrix is rank deficient")

    def two_stage_least_squares(target: np.ndarray, regressors: np.ndarray):
        hth = h.T @ h
        projected_regressors = h @ np.linalg.solve(hth, h.T @ regressors)
        projected_target = h @ np.linalg.solve(hth, h.T @ target)
        cross = projected_regressors.T @ regressors
        if np.linalg.matrix_rank(cross) < regressors.shape[1]:
            raise ValueError("instrumented regression is underidentified or rank deficient")
        estimate = np.linalg.solve(cross, projected_regressors.T @ target)
        return estimate, projected_regressors

    first_estimate, _ = two_stage_least_squares(response, z)
    first_residuals = response - z @ first_estimate
    gm = heteroskedastic_spatial_error_gm(
        first_residuals, w, rho_bounds=rho_bounds, grid_size=grid_size
    )
    lam = gm.lambda_
    transform = np.eye(n) - lam * w
    if np.linalg.matrix_rank(transform) < n or np.linalg.cond(transform) > 1e12:
        raise ValueError("I - lambda W is singular or ill-conditioned at the GM estimate")
    filtered_y = transform @ response
    filtered_z = transform @ z
    estimate, projected_filtered_z = two_stage_least_squares(filtered_y, filtered_z)
    residuals = response - z @ estimate
    filtered_residuals = filtered_y - filtered_z @ estimate

    cross = projected_filtered_z.T @ filtered_z
    bread = np.linalg.inv(cross)
    meat = projected_filtered_z.T @ (projected_filtered_z * (filtered_residuals ** 2)[:, None])
    covariance = (n / (n - k)) * bread @ meat @ bread.T
    covariance = (covariance + covariance.T) / 2.0
    if not np.all(np.isfinite(covariance)):
        raise ValueError("conditional HC1 covariance is not finite")
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    joint = spatial_sarar_joint_covariance(
        response, design, w, h, lam, first_residuals, estimate
    )

    return SpatialSARARGTSLSResult(
        rho=float(estimate[-1]),
        lambda_=float(lam),
        beta=tuple(float(value) for value in estimate[:-1]),
        coefficients=tuple(float(value) for value in estimate),
        fitted=tuple(float(value) for value in z @ estimate),
        residuals=tuple(float(value) for value in residuals),
        filtered_residuals=tuple(float(value) for value in filtered_residuals),
        covariance_hc1_conditional=tuple(tuple(float(value) for value in row) for row in covariance),
        standard_errors_hc1_conditional=tuple(float(value) for value in standard_errors),
        covariance_joint_kp=joint.covariance,
        standard_errors_joint_kp=joint.standard_errors,
        instruments_used=int(h.shape[1]),
        first_stage_rank=int(np.linalg.matrix_rank(h)),
        transformed_stage_rank=int(np.linalg.matrix_rank(projected_filtered_z)),
    )

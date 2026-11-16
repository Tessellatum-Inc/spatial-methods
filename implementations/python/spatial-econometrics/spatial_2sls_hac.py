"""Spatial 2SLS with Conley-style spatial HAC covariance."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Spatial2SLSHACResult:
    rho: float
    beta: tuple[float, ...]
    coefficients: tuple[float, ...]
    covariance: tuple[tuple[float, ...], ...]
    standard_errors: tuple[float, ...]
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    instruments_used: int
    bandwidth: float
    nonzero_off_diagonal_pairs: int
    small_sample_correction: bool


def _independent_columns(matrix: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    kept: list[int] = []
    current = np.empty((matrix.shape[0], 0), dtype=float)
    rank = 0
    for j in range(matrix.shape[1]):
        candidate = np.column_stack([current, matrix[:, j]])
        next_rank = np.linalg.matrix_rank(candidate, tol=tolerance)
        if next_rank > rank:
            kept.append(j)
            current, rank = candidate, next_rank
    return matrix[:, kept]


def spatial_lag_2sls_hac(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    coordinates: Sequence[Sequence[float]],
    *,
    bandwidth: float,
    instrument_orders: int = 1,
    small_sample_correction: bool = True,
) -> Spatial2SLSHACResult:
    """Estimate SAR by 2SLS and Conley-style HAC covariance.

    Instruments are H=[X, WX, ..., W^q X]. The covariance uses the
    Wendland C2 compact-support kernel over projected planar coordinates.
    It is robust to heteroskedasticity and residual cross-correlation within
    the declared bandwidth, conditional on valid instruments and the
    spatial-IV identifying assumptions. It does not make invalid instruments
    valid and is not a weak-instrument-robust inferential procedure.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    points = np.asarray(coordinates, dtype=float)
    if response.ndim != 1 or response.size < 5:
        raise ValueError("y must be a vector with at least five observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or not 1 <= design.shape[1] < n - 1:
        raise ValueError("X must have one row per observation and leave residual degrees of freedom")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if points.shape != (n, 2):
        raise ValueError("coordinates must be an N-by-2 planar coordinate array")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w)) and np.all(np.isfinite(points))):
        raise ValueError("y, X, weights and coordinates must contain only finite values")
    if np.any(w < 0) or np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be non-negative, nonzero and have a zero diagonal")
    if not np.isfinite(bandwidth) or bandwidth <= 0:
        raise ValueError("bandwidth must be positive and finite")
    if isinstance(instrument_orders, bool) or not isinstance(instrument_orders, int) or instrument_orders < 1:
        raise ValueError("instrument_orders must be a positive integer")
    if not isinstance(small_sample_correction, (bool, np.bool_)):
        raise ValueError("small_sample_correction must be boolean")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    instrument_blocks = [design]
    lagged = design.copy()
    for _ in range(instrument_orders):
        lagged = w @ lagged
        instrument_blocks.append(lagged)
    instruments = _independent_columns(np.column_stack(instrument_blocks))
    if instruments.shape[1] < design.shape[1] + 1:
        raise ValueError("instruments do not identify the spatial lag model")
    if instruments.shape[1] >= n:
        raise ValueError("sample size must exceed the number of independent instruments")

    regressors = np.column_stack([w @ response, design])
    if np.linalg.matrix_rank(instruments.T @ regressors) < regressors.shape[1]:
        raise ValueError("instruments fail the order/rank identification condition")
    hth = instruments.T @ instruments
    if np.linalg.matrix_rank(hth) < instruments.shape[1]:
        raise ValueError("instrument cross-product is singular")
    projected = instruments @ np.linalg.solve(hth, instruments.T @ regressors)
    cross = projected.T @ regressors
    if np.linalg.matrix_rank(cross) < regressors.shape[1]:
        raise ValueError("projected regression cross-product is singular")
    coefficients = np.linalg.solve(cross, projected.T @ response)
    fitted = regressors @ coefficients
    residuals = response - fitted

    delta = points[:, None, :] - points[None, :, :]
    distances = np.sqrt(np.sum(delta * delta, axis=2))
    scaled = distances / float(bandwidth)
    kernel = np.where(scaled < 1.0, (1.0 - scaled) ** 4 * (4.0 * scaled + 1.0), 0.0)
    scores = projected * residuals[:, None]
    meat = scores.T @ kernel @ scores
    bread = np.linalg.inv(cross)
    covariance = bread @ meat @ bread.T
    if small_sample_correction:
        covariance *= n / (n - regressors.shape[1])
    covariance = (covariance + covariance.T) / 2.0
    diagonal = np.diag(covariance)
    if np.any(diagonal < -1e-10):
        raise ValueError("spatial HAC covariance has materially negative diagonal entries")
    standard_errors = np.sqrt(np.maximum(diagonal, 0.0))

    return Spatial2SLSHACResult(
        rho=float(coefficients[0]),
        beta=tuple(float(value) for value in coefficients[1:]),
        coefficients=tuple(float(value) for value in coefficients),
        covariance=tuple(tuple(float(value) for value in row) for row in covariance),
        standard_errors=tuple(float(value) for value in standard_errors),
        fitted=tuple(float(value) for value in fitted),
        residuals=tuple(float(value) for value in residuals),
        instruments_used=int(instruments.shape[1]),
        bandwidth=float(bandwidth),
        nonzero_off_diagonal_pairs=int(np.count_nonzero(np.triu(kernel, k=1))),
        small_sample_correction=bool(small_sample_correction),
    )

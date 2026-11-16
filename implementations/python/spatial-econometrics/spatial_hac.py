"""OLS with Conley-style spatial heteroskedasticity-and-autocorrelation covariance."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialHACFit:
    coefficients: tuple[float, ...]
    covariance: tuple[tuple[float, ...], ...]
    standard_errors: tuple[float, ...]
    residuals: tuple[float, ...]
    bandwidth: float
    nonzero_off_diagonal_pairs: int
    small_sample_correction: bool


def spatial_hac_ols(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    coordinates: Sequence[Sequence[float]],
    *,
    bandwidth: float,
    small_sample_correction: bool = True,
) -> SpatialHACFit:
    """Fit OLS and calculate a compact-support Wendland spatial HAC covariance.

    Coordinates must be projected planar coordinates in a common linear unit.
    The isotropic Wendland C2 kernel is (1-r)^4(4r+1) for r<1 and zero otherwise, including unit diagonal.
    The estimator allows heteroskedasticity and spatial correlation within the
    bandwidth; it does not correct for endogeneity or spatially lagged outcomes.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    points = np.asarray(coordinates, dtype=float)
    if response.ndim != 1 or response.size < 3:
        raise ValueError("y must be a vector with at least three observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or not 1 <= design.shape[1] < n:
        raise ValueError("X must have one row per observation and leave residual degrees of freedom")
    if points.shape != (n, 2):
        raise ValueError("coordinates must be an N-by-2 planar coordinate array")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(points))):
        raise ValueError("y, X and coordinates must contain only finite values")
    if not np.isfinite(bandwidth) or bandwidth <= 0:
        raise ValueError("bandwidth must be positive and finite")
    if not isinstance(small_sample_correction, (bool, np.bool_)):
        raise ValueError("small_sample_correction must be boolean")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    beta, _, _, _ = np.linalg.lstsq(design, response, rcond=None)
    residual = response - design @ beta
    bread = np.linalg.inv(design.T @ design)

    differences = points[:, None, :] - points[None, :, :]
    distances = np.sqrt(np.sum(differences * differences, axis=2))
    scaled = distances / float(bandwidth)
    kernel = np.where(scaled < 1.0, (1.0 - scaled) ** 4 * (4.0 * scaled + 1.0), 0.0)
    weighted_scores = design * residual[:, None]
    meat = weighted_scores.T @ kernel @ weighted_scores
    covariance = bread @ meat @ bread
    if small_sample_correction:
        covariance *= n / (n - design.shape[1])
    covariance = (covariance + covariance.T) / 2.0
    diagonal = np.diag(covariance)
    if np.any(diagonal < -1e-10):
        raise ValueError("spatial HAC covariance has materially negative diagonal entries")
    standard_errors = np.sqrt(np.maximum(diagonal, 0.0))
    return SpatialHACFit(
        coefficients=tuple(float(value) for value in beta),
        covariance=tuple(tuple(float(value) for value in row) for row in covariance),
        standard_errors=tuple(float(value) for value in standard_errors),
        residuals=tuple(float(value) for value in residual),
        bandwidth=float(bandwidth),
        nonzero_off_diagonal_pairs=int(np.count_nonzero(np.triu(kernel, k=1))),
        small_sample_correction=bool(small_sample_correction),
    )

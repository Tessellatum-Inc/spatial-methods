"""Dense concentrated maximum-likelihood estimators for SAR, SEM, SDM and SARAR models.

These implementations are intended for small teaching problems. They use a
conservative, automatically derived rho interval that guarantees nonsingularity
for every candidate in the interval, rather than claiming the full admissible
parameter space.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log, pi
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialMLEFit:
    model: str
    spatial_parameter: float
    coefficients: tuple[float, ...]
    sigma2_mle: float
    log_likelihood: float
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    rho_bounds: tuple[float, float]
    evaluations: int
    spatial_covariate_coefficients: tuple[float, ...] = ()
    error_parameter: float | None = None


def _validate(y, x, weights):
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    w = np.asarray(weights, dtype=float)
    if response.ndim != 1 or response.size < 5:
        raise ValueError("y must be a vector with at least five observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation and at least one column")
    if design.shape[1] >= n - 1:
        raise ValueError("X must leave residual degrees of freedom")
    if w.shape != (n, n):
        raise ValueError("weights must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(w))):
        raise ValueError("y, X and weights must contain only finite values")
    if np.any(w < 0) or np.any(np.diag(w) != 0) or np.allclose(w, 0):
        raise ValueError("weights must be non-negative, nonzero and have a zero diagonal")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    norm = float(np.max(np.sum(np.abs(w), axis=1)))
    if not np.isfinite(norm) or norm <= 0:
        raise ValueError("weights must have a positive finite infinity norm")
    # The Neumann-series condition |parameter| * ||W||_inf < 1 guarantees
    # I - parameter*W is nonsingular; its determinant remains positive.
    limit = 0.98 / norm
    return response, design, w, (-limit, limit)


def _golden_max(function, left, right, tolerance=1e-7, max_iter=160):
    ratio = (np.sqrt(5.0) - 1.0) / 2.0
    c = right - ratio * (right - left)
    d = left + ratio * (right - left)
    fc, fd = function(c), function(d)
    evaluations = 2
    for _ in range(max_iter):
        if right - left <= tolerance * (1.0 + abs(left) + abs(right)):
            break
        if fc > fd:
            right, d, fd = d, c, fc
            c = right - ratio * (right - left)
            fc = function(c)
        else:
            left, c, fc = c, d, fd
            d = left + ratio * (right - left)
            fd = function(d)
        evaluations += 1
    point = (left + right) / 2.0
    return point, function(point), evaluations + 1


def _fit(y, x, w, model, grid_size, tolerance):
    n = y.size
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size < 21:
        raise ValueError("grid_size must be an integer of at least 21")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be positive and finite")
    wy = w @ y
    wx = w @ x
    bounds = _validate(y, x, w)[3]
    lower, upper = bounds
    evaluations = 0

    def profile(parameter):
        nonlocal evaluations
        a = np.eye(n) - parameter * w
        sign, logdet = np.linalg.slogdet(a)
        evaluations += 1
        if sign <= 0 or not np.isfinite(logdet):
            return -np.inf
        ay = y - parameter * wy
        if model == "SAR":
            transformed_x = x
        else:  # SEM: transform both sides by I - lambda W.
            transformed_x = x - parameter * wx
        coefficients, _, rank, _ = np.linalg.lstsq(transformed_x, ay, rcond=None)
        if rank < x.shape[1]:
            return -np.inf
        residual = ay - transformed_x @ coefficients
        sigma2 = float(residual @ residual / n)
        if not np.isfinite(sigma2) or sigma2 <= np.finfo(float).tiny:
            return -np.inf
        return float(logdet - (n / 2.0) * (log(2.0 * pi) + 1.0 + log(sigma2)))

    grid = np.linspace(lower, upper, grid_size)
    scores = np.array([profile(float(value)) for value in grid])
    best = int(np.argmax(scores))
    if not np.isfinite(scores[best]):
        raise ValueError("no finite likelihood found in the conservative parameter interval")
    # Refine around the best grid cell. The grid scan reduces the risk of
    # assuming the concentrated likelihood is globally unimodal.
    left = float(grid[max(0, best - 1)])
    right = float(grid[min(grid_size - 1, best + 1)])
    if left == right:
        parameter, likelihood = float(grid[best]), float(scores[best])
        refine_evaluations = 0
    else:
        refined_parameter, refined_likelihood, refine_evaluations = _golden_max(
            profile, left, right, tolerance=tolerance
        )
        if refined_likelihood > scores[best]:
            parameter, likelihood = refined_parameter, refined_likelihood
        else:
            parameter, likelihood = float(grid[best]), float(scores[best])
    ay = y - parameter * wy
    transformed_x = x if model == "SAR" else x - parameter * wx
    coefficients = np.linalg.lstsq(transformed_x, ay, rcond=None)[0]
    residual = ay - transformed_x @ coefficients
    sigma2 = float(residual @ residual / n)
    if model == "SAR":
        fitted = parameter * wy + x @ coefficients
    else:
        # E[y|X] under SEM is X beta; the transformed residual is the
        # innovation, while the original-scale residual is y - X beta.
        fitted = x @ coefficients
        residual = y - fitted
    return SpatialMLEFit(
        model=model,
        spatial_parameter=float(parameter),
        coefficients=tuple(float(v) for v in coefficients),
        sigma2_mle=sigma2,
        log_likelihood=float(likelihood),
        fitted=tuple(float(v) for v in fitted),
        residuals=tuple(float(v) for v in residual),
        rho_bounds=(float(lower), float(upper)),
        evaluations=int(evaluations + refine_evaluations),
    )


def spatial_lag_mle(y: Sequence[float], x: Sequence[Sequence[float]],
                    weights: Sequence[Sequence[float]], *,
                    grid_size: int = 201, tolerance: float = 1e-7) -> SpatialMLEFit:
    """Concentrated Gaussian ML for y = rho W y + X beta + epsilon."""
    response, design, w, _ = _validate(y, x, weights)
    return _fit(response, design, w, "SAR", grid_size, tolerance)


def spatial_error_mle(y: Sequence[float], x: Sequence[Sequence[float]],
                      weights: Sequence[Sequence[float]], *,
                      grid_size: int = 201, tolerance: float = 1e-7) -> SpatialMLEFit:
    """Concentrated Gaussian ML for y = X beta + u, u = lambda W u + epsilon."""
    response, design, w, _ = _validate(y, x, weights)
    return _fit(response, design, w, "SEM", grid_size, tolerance)



def spatial_durbin_mle(y: Sequence[float], x: Sequence[Sequence[float]],
                       weights: Sequence[Sequence[float]], *,
                       grid_size: int = 201, tolerance: float = 1e-7) -> SpatialMLEFit:
    """Concentrated Gaussian ML for y = rho Wy + X beta + WX gamma.

    Columns of WX that are linearly dependent on X or earlier retained WX
    columns are omitted from estimation and returned as zero gamma entries.
    This handles, for example, the spatial lag of an intercept under
    row-standardised weights. The rho search uses the same conservative
    norm-bounded interval as the SAR and SEM estimators.
    """
    response, design, w, bounds = _validate(y, x, weights)
    n, k = design.shape
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size < 21:
        raise ValueError("grid_size must be an integer of at least 21")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be positive and finite")

    wx = w @ design
    retained = []
    retained_indices = []
    current = design.copy()
    for j in range(k):
        candidate = np.column_stack([current, wx[:, j]])
        if np.linalg.matrix_rank(candidate) > np.linalg.matrix_rank(current):
            retained.append(wx[:, j])
            retained_indices.append(j)
            current = candidate
    if current.shape[1] >= n - 1:
        raise ValueError("SDM design must leave residual degrees of freedom")
    if np.linalg.matrix_rank(current) < current.shape[1]:
        raise ValueError("augmented SDM design must have full column rank")

    lower, upper = bounds
    wy = w @ response
    evaluations = 0

    def profile(rho):
        nonlocal evaluations
        a = np.eye(n) - rho * w
        sign, logdet = np.linalg.slogdet(a)
        evaluations += 1
        if sign <= 0 or not np.isfinite(logdet):
            return -np.inf
        ay = response - rho * wy
        coef, _, rank, _ = np.linalg.lstsq(current, ay, rcond=None)
        if rank < current.shape[1]:
            return -np.inf
        residual = ay - current @ coef
        sigma2 = float(residual @ residual / n)
        if not np.isfinite(sigma2) or sigma2 <= np.finfo(float).tiny:
            return -np.inf
        return float(logdet - (n / 2.0) *
                     (log(2.0 * pi) + 1.0 + log(sigma2)))

    grid = np.linspace(lower, upper, grid_size)
    scores = np.array([profile(float(v)) for v in grid])
    best = int(np.argmax(scores))
    if not np.isfinite(scores[best]):
        raise ValueError("no finite likelihood found in the conservative parameter interval")
    left = float(grid[max(0, best - 1)])
    right = float(grid[min(grid_size - 1, best + 1)])
    if left == right:
        rho, likelihood, refine_evaluations = float(grid[best]), float(scores[best]), 0
    else:
        candidate_rho, candidate_ll, refine_evaluations = _golden_max(
            profile, left, right, tolerance=tolerance)
        if candidate_ll > scores[best]:
            rho, likelihood = candidate_rho, candidate_ll
        else:
            rho, likelihood = float(grid[best]), float(scores[best])

    ay = response - rho * wy
    coef = np.linalg.lstsq(current, ay, rcond=None)[0]
    transformed_residual = ay - current @ coef
    sigma2 = float(transformed_residual @ transformed_residual / n)
    beta = coef[:k]
    gamma = np.zeros(k)
    for position, original_index in enumerate(retained_indices):
        gamma[original_index] = coef[k + position]
    fitted = rho * wy + design @ beta + wx @ gamma
    residuals = response - fitted
    return SpatialMLEFit(
        model="SDM",
        spatial_parameter=float(rho),
        coefficients=tuple(float(v) for v in beta),
        sigma2_mle=sigma2,
        log_likelihood=float(likelihood),
        fitted=tuple(float(v) for v in fitted),
        residuals=tuple(float(v) for v in residuals),
        rho_bounds=(float(lower), float(upper)),
        evaluations=int(evaluations + refine_evaluations),
        spatial_covariate_coefficients=tuple(float(v) for v in gamma),
    )



def spatial_sarar_mle(y: Sequence[float], x: Sequence[Sequence[float]],
                      weights: Sequence[Sequence[float]], *,
                      grid_size: int = 41, tolerance: float = 1e-6,
                      coordinate_iterations: int = 8) -> SpatialMLEFit:
    """Concentrated Gaussian ML for SARAR/SAC:
    y = rho W y + X beta + u; u = lambda W u + epsilon.

    A coarse two-dimensional grid locates a starting point, followed by
    alternating one-dimensional golden-section refinements in rho and lambda.
    Both parameters use the conservative norm-bounded interval.
    """
    response, design, w, bounds = _validate(y, x, weights)
    n = response.size
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size < 11:
        raise ValueError("grid_size must be an integer of at least 11")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be positive and finite")
    if (isinstance(coordinate_iterations, bool)
            or not isinstance(coordinate_iterations, int)
            or coordinate_iterations < 1):
        raise ValueError("coordinate_iterations must be a positive integer")

    lower, upper = bounds
    wy = w @ response
    wx = w @ design
    identity = np.eye(n)
    evaluations = 0

    def profile(rho, lam):
        nonlocal evaluations
        ar = identity - rho * w
        al = identity - lam * w
        sign_r, logdet_r = np.linalg.slogdet(ar)
        sign_l, logdet_l = np.linalg.slogdet(al)
        evaluations += 1
        if sign_r <= 0 or sign_l <= 0:
            return -np.inf
        transformed_y = (response - rho * wy) - lam * (w @ (response - rho * wy))
        transformed_x = design - lam * wx
        coefficients, _, rank, _ = np.linalg.lstsq(transformed_x, transformed_y, rcond=None)
        if rank < design.shape[1]:
            return -np.inf
        residual = transformed_y - transformed_x @ coefficients
        sigma2 = float(residual @ residual / n)
        if not np.isfinite(sigma2) or sigma2 <= np.finfo(float).tiny:
            return -np.inf
        return float(logdet_r + logdet_l -
                     (n / 2.0) * (log(2.0 * pi) + 1.0 + log(sigma2)))

    grid = np.linspace(lower, upper, grid_size)
    best_score = -np.inf
    best_rho = best_lam = 0.0
    for rho in grid:
        for lam in grid:
            score = profile(float(rho), float(lam))
            if score > best_score:
                best_score, best_rho, best_lam = score, float(rho), float(lam)
    if not np.isfinite(best_score):
        raise ValueError("no finite likelihood found in the conservative parameter region")

    rho, lam = best_rho, best_lam
    grid_step = float(grid[1] - grid[0])
    rho_left, rho_right = max(lower, best_rho - grid_step), min(upper, best_rho + grid_step)
    lam_left, lam_right = max(lower, best_lam - grid_step), min(upper, best_lam + grid_step)
    for _ in range(coordinate_iterations):
        old_rho, old_lam = rho, lam
        rho, _, rho_evaluations = _golden_max(lambda value: profile(value, lam),
                                               rho_left, rho_right, tolerance=tolerance)
        lam, _, lam_evaluations = _golden_max(lambda value: profile(rho, value),
                                               lam_left, lam_right, tolerance=tolerance)
        evaluations += rho_evaluations + lam_evaluations
        if abs(rho - old_rho) + abs(lam - old_lam) <= tolerance * (
                1.0 + abs(rho) + abs(lam)):
            break

    likelihood = profile(rho, lam)
    if likelihood < best_score:
        rho, lam, likelihood = best_rho, best_lam, best_score
    ar_y = response - rho * wy
    transformed_y = ar_y - lam * (w @ ar_y)
    transformed_x = design - lam * wx
    coefficients = np.linalg.lstsq(transformed_x, transformed_y, rcond=None)[0]
    innovation = transformed_y - transformed_x @ coefficients
    sigma2 = float(innovation @ innovation / n)
    fitted = rho * wy + design @ coefficients
    residuals = response - fitted
    return SpatialMLEFit(
        model="SARAR",
        spatial_parameter=float(rho),
        coefficients=tuple(float(v) for v in coefficients),
        sigma2_mle=sigma2,
        log_likelihood=float(likelihood),
        fitted=tuple(float(v) for v in fitted),
        residuals=tuple(float(v) for v in residuals),
        rho_bounds=(float(lower), float(upper)),
        evaluations=int(evaluations),
        error_parameter=float(lam),
    )

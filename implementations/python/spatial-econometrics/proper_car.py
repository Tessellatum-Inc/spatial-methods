"""Gaussian proper-CAR regression by concentrated maximum likelihood.

The precision is Q = tau * (D - alpha A), where A is a symmetric,
non-negative adjacency/weight matrix and D contains its row sums.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log, pi
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ProperCARFit:
    alpha: float
    tau: float
    coefficients: tuple[float, ...]
    variance_scale: float
    conditional_variances: tuple[float, ...]
    log_likelihood: float
    fitted: tuple[float, ...]
    residuals: tuple[float, ...]
    alpha_bounds: tuple[float, float]
    evaluations: int


def _validate(y, x, adjacency):
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    a = np.asarray(adjacency, dtype=float)
    if response.ndim != 1 or response.size < 5:
        raise ValueError("y must be a vector with at least five observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation and at least one column")
    if design.shape[1] >= n:
        raise ValueError("X must leave residual degrees of freedom")
    if a.shape != (n, n):
        raise ValueError("adjacency must be an N-by-N matrix matching y")
    if not (np.all(np.isfinite(response)) and np.all(np.isfinite(design))
            and np.all(np.isfinite(a))):
        raise ValueError("y, X and adjacency must contain only finite values")
    if np.any(a < 0) or np.any(np.diag(a) != 0) or np.allclose(a, 0):
        raise ValueError("adjacency must be non-negative, nonzero and have a zero diagonal")
    if not np.allclose(a, a.T, rtol=1e-10, atol=1e-12):
        raise ValueError("proper CAR adjacency must be symmetric")
    degree = a.sum(axis=1)
    if np.any(degree <= 0):
        raise ValueError("proper CAR requires every observation to have positive degree")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")

    inv_sqrt_degree = 1.0 / np.sqrt(degree)
    normalised = inv_sqrt_degree[:, None] * a * inv_sqrt_degree[None, :]
    eigenvalues = np.linalg.eigvalsh(normalised)
    largest = float(eigenvalues[-1])
    smallest = float(eigenvalues[0])
    if largest <= 0:
        raise ValueError("adjacency has no positive normalised eigenvalue")
    # Positive definiteness requires 1 - alpha*lambda > 0 for every eigenvalue.
    lower = 1.0 / smallest if smallest < -1e-12 else -np.inf
    upper = 1.0 / largest
    # Stay slightly inside the exact admissible interval for stable log determinants.
    span = upper - lower if np.isfinite(lower) else upper
    if np.isfinite(lower):
        margin = max(1e-8, 1e-6 * span)
        lower += margin
        upper -= margin
    else:
        lower = -max(upper, 1.0)
        upper -= max(1e-8, 1e-6 * upper)
    if not lower < upper:
        raise ValueError("could not derive a nonempty positive-definite alpha interval")
    return response, design, a, degree, (float(lower), float(upper))


def _golden_max(function, left, right, tolerance, max_iter=180):
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


def proper_car_mle(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    adjacency: Sequence[Sequence[float]],
    *,
    grid_size: int = 81,
    tolerance: float = 1e-7,
) -> ProperCARFit:
    """Fit Gaussian proper-CAR regression with unknown dependence alpha and precision tau.

    The graph must be represented by a symmetric, non-negative adjacency
    matrix with no self-links or isolated observations. The admissible alpha
    interval is derived from eigenvalues of D^(-1/2) A D^(-1/2), ensuring
    D - alpha A is positive definite throughout the search.
    """
    response, design, a, degree, bounds = _validate(y, x, adjacency)
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size < 21:
        raise ValueError("grid_size must be an integer of at least 21")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be positive and finite")

    n = response.size
    lower, upper = bounds
    evaluations = 0

    def profile(alpha):
        nonlocal evaluations
        precision_base = np.diag(degree) - alpha * a
        sign, logdet = np.linalg.slogdet(precision_base)
        evaluations += 1
        if sign <= 0 or not np.isfinite(logdet):
            return -np.inf
        qy = precision_base @ response
        qx = precision_base @ design
        information = design.T @ qx
        if np.linalg.matrix_rank(information) < design.shape[1]:
            return -np.inf
        beta = np.linalg.solve(information, design.T @ qy)
        residual = response - design @ beta
        quadratic = float(residual @ precision_base @ residual)
        if not np.isfinite(quadratic) or quadratic <= np.finfo(float).tiny:
            return -np.inf
        return float(0.5 * logdet -
                     (n / 2.0) * (log(2.0 * pi) + 1.0 + log(quadratic / n)))

    grid = np.linspace(lower, upper, grid_size)
    scores = np.array([profile(float(value)) for value in grid])
    best = int(np.argmax(scores))
    if not np.isfinite(scores[best]):
        raise ValueError("no finite proper-CAR likelihood found in admissible alpha interval")
    left = float(grid[max(0, best - 1)])
    right = float(grid[min(grid_size - 1, best + 1)])
    if left < right:
        alpha_refined, score_refined, refine_evaluations = _golden_max(
            profile, left, right, tolerance
        )
        if score_refined > scores[best]:
            alpha, likelihood = alpha_refined, score_refined
        else:
            alpha, likelihood = float(grid[best]), float(scores[best])
    else:
        alpha, likelihood, refine_evaluations = float(grid[best]), float(scores[best]), 0

    precision_base = np.diag(degree) - alpha * a
    information = design.T @ precision_base @ design
    beta = np.linalg.solve(information, design.T @ precision_base @ response)
    residual = response - design @ beta
    quadratic = float(residual @ precision_base @ residual)
    tau = float(n / quadratic)
    variance_scale = float(1.0 / tau)
    conditional_variances = 1.0 / (tau * degree)
    return ProperCARFit(
        alpha=float(alpha),
        tau=tau,
        coefficients=tuple(float(v) for v in beta),
        variance_scale=variance_scale,
        conditional_variances=tuple(float(v) for v in conditional_variances),
        log_likelihood=float(likelihood),
        fitted=tuple(float(v) for v in design @ beta),
        residuals=tuple(float(v) for v in residual),
        alpha_bounds=bounds,
        evaluations=int(evaluations + refine_evaluations),
    )

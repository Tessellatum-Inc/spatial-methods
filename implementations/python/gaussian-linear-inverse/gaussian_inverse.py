"""Exact conjugate Gaussian linear inverse problem."""
from __future__ import annotations

import numpy as np


def _vector(values, name):
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be a finite one-dimensional vector")
    return array


def _matrix(values, name, shape=None):
    array = np.asarray(values, dtype=float)
    if array.ndim != 2 or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be a finite two-dimensional matrix")
    if shape is not None and array.shape != shape:
        raise ValueError(f"{name} must have shape {shape}")
    return array


def _positive_definite(matrix, name):
    if matrix.shape[0] != matrix.shape[1] or not np.allclose(matrix, matrix.T, rtol=1e-10, atol=1e-12):
        raise ValueError(f"{name} must be symmetric and square")
    try:
        return np.linalg.cholesky(matrix)
    except np.linalg.LinAlgError as exc:
        raise ValueError(f"{name} must be positive definite") from exc


def solve_gaussian_linear_inverse(
    design,
    observations,
    prior_mean,
    prior_covariance,
    noise_covariance,
) -> dict:
    """Condition a Gaussian parameter prior on linear Gaussian observations.

    Model: y = A x + epsilon, x ~ N(m0, C0), epsilon ~ N(0, R).
    Dense Cholesky solves avoid explicitly forming matrix inverses.
    """
    a = _matrix(design, "design")
    y = _vector(observations, "observations")
    m0 = _vector(prior_mean, "prior_mean")
    if a.shape[0] != y.size or a.shape[1] != m0.size or min(a.shape) < 1:
        raise ValueError("design, observations and prior_mean dimensions do not agree")
    c0 = _matrix(prior_covariance, "prior_covariance", (m0.size, m0.size))
    r = _matrix(noise_covariance, "noise_covariance", (y.size, y.size))
    _positive_definite(c0, "prior_covariance")
    _positive_definite(r, "noise_covariance")

    innovation = y - a @ m0
    marginal_covariance = a @ c0 @ a.T + r
    chol = _positive_definite(marginal_covariance, "marginal observation covariance")
    solved_innovation = np.linalg.solve(chol.T, np.linalg.solve(chol, innovation))
    gain_numerator = c0 @ a.T
    posterior_mean = m0 + gain_numerator @ solved_innovation
    solved_design = np.linalg.solve(chol.T, np.linalg.solve(chol, a @ c0))
    posterior_covariance = c0 - gain_numerator @ solved_design
    posterior_covariance = (posterior_covariance + posterior_covariance.T) / 2
    logdet = 2 * float(np.sum(np.log(np.diag(chol))))
    log_evidence = -0.5 * (
        y.size * np.log(2 * np.pi)
        + logdet
        + float(innovation @ solved_innovation)
    )
    return {
        "posterior_mean": posterior_mean,
        "posterior_covariance": posterior_covariance,
        "posterior_std": np.sqrt(np.maximum(0.0, np.diag(posterior_covariance))),
        "innovation": innovation,
        "marginal_observation_covariance": marginal_covariance,
        "log_marginal_likelihood": float(log_evidence),
    }

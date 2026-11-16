"""Kelejian–Prucha joint SARAR covariance for regression and error parameters.

Implements the plug-in joint covariance in Kelejian and Prucha (2010),
Theorem 4 and Section 4.1, for the common-weights W=M, two-step GM / final
GTSLS procedure. The GM weighting matrix is the identity, matching the
current heteroskedastic spatial-error GM estimator.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SpatialSARARJointCovariance:
    """Joint asymptotic covariance, ordered [beta..., rho, lambda]."""

    covariance: tuple[tuple[float, ...], ...]
    standard_errors: tuple[float, ...]
    gm_moment_covariance: tuple[tuple[float, float], tuple[float, float]]
    stacked_moment_covariance: tuple[tuple[float, ...], ...]
    initial_iv_map: tuple[tuple[float, ...], ...]
    final_iv_map: tuple[tuple[float, ...], ...]


def _iv_map(instruments: np.ndarray, regressors: np.ndarray) -> np.ndarray:
    """Return the p-by-k asymptotic 2SLS map P."""
    n = instruments.shape[0]
    qhh = instruments.T @ instruments / n
    qhz = instruments.T @ regressors / n
    if np.linalg.matrix_rank(qhh) < qhh.shape[0]:
        raise ValueError("instrument cross-product is rank deficient")
    middle = qhz.T @ np.linalg.solve(qhh, qhz)
    if np.linalg.matrix_rank(middle) < middle.shape[0]:
        raise ValueError("instrumented regressors are underidentified")
    return np.linalg.solve(qhh, qhz) @ np.linalg.inv(middle)


def spatial_sarar_joint_covariance(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    instruments: Sequence[Sequence[float]],
    lambda_hat: float,
    first_stage_residuals: Sequence[float],
    final_coefficients: Sequence[float],
) -> SpatialSARARJointCovariance:
    """Estimate the KP joint covariance for final GTSLS coefficients and lambda.

    The returned covariance is for [beta..., rho, lambda]. It accounts for
    (i) the first-stage IV estimation error entering the GM disturbance
    moments, and (ii) covariance between the final transformed IV estimator
    and those GM moments. It uses the KP plug-in innovation variance
    estimator diag(epsilon_hat**2), identity weighting of the two GM moments,
    and the KP zero-diagonal quadratic-form covariance formula.

    This is an asymptotic covariance under the paper's independence,
    boundedness, identification and moment assumptions; it is not a
    finite-sample exact covariance. W=M is required.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    matrix = np.asarray(weights, dtype=float)
    h = np.asarray(instruments, dtype=float)
    u_hat = np.asarray(first_stage_residuals, dtype=float)
    delta_hat = np.asarray(final_coefficients, dtype=float)
    if response.ndim != 1:
        raise ValueError("y must be a vector")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must have one row per observation")
    if matrix.shape != (n, n) or h.ndim != 2 or h.shape[0] != n:
        raise ValueError("weights and instruments must match y")
    k = design.shape[1] + 1
    if u_hat.shape != (n,) or delta_hat.shape != (k,):
        raise ValueError("residuals or final coefficients have incompatible dimensions")
    if not np.isfinite(lambda_hat):
        raise ValueError("lambda_hat must be finite")
    if not all(np.all(np.isfinite(v)) for v in (response, design, matrix, h, u_hat, delta_hat)):
        raise ValueError("all inputs must be finite")
    if np.any(np.diag(matrix) != 0) or np.allclose(matrix, 0):
        raise ValueError("weights must be nonzero with a zero diagonal")
    if np.linalg.matrix_rank(h) < h.shape[1]:
        raise ValueError("instruments must have full column rank")
    if h.shape[1] < k:
        raise ValueError("instrument count must be at least the regressor count")

    wy = matrix @ response
    z = np.column_stack([design, wy])
    identity = np.eye(n)
    transform = identity - float(lambda_hat) * matrix
    if np.linalg.matrix_rank(transform) < n or np.linalg.cond(transform) > 1e12:
        raise ValueError("I - lambda W is singular or ill-conditioned")

    # Initial IV influence map: T = (I-lambda M')^-1 H P.
    p_initial = _iv_map(h, z)
    f_initial = np.linalg.solve(transform.T, h)
    t_initial = f_initial @ p_initial

    # KP (2010) zero-diagonal quadratic-form matrices.
    a1 = matrix.T @ matrix
    a1 = a1 - np.diag(np.diag(a1))
    a2 = matrix.copy()
    sym_a = (a1 + a1.T, a2 + a2.T)
    d = -z

    # Plug-in estimates of a_r = T alpha_r, with D=-Z.
    a_vectors = []
    for a_sym in sym_a:
        filtered_form = transform.T @ a_sym @ transform
        alpha = d.T @ filtered_form @ u_hat / n
        a_vectors.append(t_initial @ alpha)
    a_stack = np.column_stack(a_vectors)

    epsilon_hat = transform @ u_hat
    sigma = epsilon_hat * epsilon_hat

    # Psi for the two GM quadratic moments, including generated-residual
    # uncertainty through a_r; zero diagonals eliminate third/fourth
    # innovation cumulant terms in the KP formula.
    psi_gm = np.empty((2, 2), dtype=float)
    for r in range(2):
        for s in range(2):
            quadratic = np.trace(
                sym_a[r] @ (sigma[:, None] * np.eye(n))
                @ sym_a[s] @ (sigma[:, None] * np.eye(n))
            ) / (2.0 * n)
            linear = float(a_vectors[r] @ (sigma * a_vectors[s])) / n
            psi_gm[r, s] = quadratic + linear
    psi_gm = (psi_gm + psi_gm.T) / 2.0

    # Final transformed IV influence map, with F*=H (KP Lemma 4).
    z_star = transform @ z
    p_final = _iv_map(h, z_star)
    psi_delta_delta = h.T @ (sigma[:, None] * h) / n
    psi_delta_rho = h.T @ (sigma[:, None] * a_stack) / n
    psi_stacked = np.block([
        [psi_delta_delta, psi_delta_rho],
        [psi_delta_rho.T, psi_gm],
    ])
    psi_stacked = (psi_stacked + psi_stacked.T) / 2.0

    # Identity-weighted nonlinear least-squares GM derivative map.
    j = np.array([1.0, 2.0 * float(lambda_hat)])
    j_norm = float(j @ j)
    if not np.isfinite(j_norm) or j_norm <= np.finfo(float).eps:
        raise ValueError("GM derivative is not identified")
    gm_map = j / j_norm

    # Map [H' epsilon, GM moments] to [delta_hat, lambda_hat].
    transform_map = np.zeros((k + 1, h.shape[1] + 2), dtype=float)
    transform_map[:k, :h.shape[1]] = p_final.T
    transform_map[k, h.shape[1]:] = gm_map
    covariance_delta_lambda = transform_map @ psi_stacked @ transform_map.T
    covariance_delta_lambda = (covariance_delta_lambda + covariance_delta_lambda.T) / 2.0
    diagonal = np.diag(covariance_delta_lambda)
    if not np.all(np.isfinite(covariance_delta_lambda)) or np.any(diagonal < -1e-10):
        raise ValueError("joint covariance is not finite positive semidefinite")
    standard_errors = np.sqrt(np.maximum(diagonal, 0.0))

    # Delta order is [beta..., rho]; append lambda as the final parameter.
    return SpatialSARARJointCovariance(
        covariance=tuple(tuple(float(v) for v in row) for row in covariance_delta_lambda),
        standard_errors=tuple(float(v) for v in standard_errors),
        gm_moment_covariance=tuple(tuple(float(v) for v in row) for row in psi_gm),
        stacked_moment_covariance=tuple(tuple(float(v) for v in row) for row in psi_stacked),
        initial_iv_map=tuple(tuple(float(v) for v in row) for row in p_initial),
        final_iv_map=tuple(tuple(float(v) for v in row) for row in p_final),
    )

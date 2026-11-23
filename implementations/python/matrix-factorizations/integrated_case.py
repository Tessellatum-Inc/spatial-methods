"""Integrated synthetic spatial case: affine control, terrain plane and GLS."""

from __future__ import annotations

import json

import numpy as np
from scipy.linalg import lu_factor, lu_solve


def run_case() -> dict[str, object]:
    # Three non-collinear local control points determine a 2-D affine map.
    control_local = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 8.0]])
    control_map = np.array([[500.0, 1000.0], [510.2, 1001.0], [499.2, 1008.4]])
    control_design = np.column_stack((control_local, np.ones(3)))
    lu, piv = lu_factor(control_design)
    x_parameters = lu_solve((lu, piv), control_map[:, 0])
    y_parameters = lu_solve((lu, piv), control_map[:, 1])

    # Transform a small, deliberately non-grid-like set of synthetic samples.
    local_samples = np.array([
        [1.0, 1.0], [3.0, 1.5], [6.0, 1.0], [9.0, 2.0],
        [1.5, 4.0], [4.0, 3.5], [7.0, 4.5], [9.0, 6.0],
        [2.0, 7.0], [5.0, 6.5], [7.5, 7.0], [8.5, 3.5],
    ])
    sample_design = np.column_stack((local_samples, np.ones(len(local_samples))))
    map_x = sample_design @ x_parameters
    map_y = sample_design @ y_parameters

    # Synthetic elevation observations with a fixed, reproducible error pattern.
    design = np.column_stack((np.ones(len(map_x)), map_x, map_y))
    truth = np.array([80.0, 0.12, -0.07])
    errors = np.array([0.018, -0.011, 0.026, -0.020, 0.009, -0.015,
                       0.022, -0.006, -0.018, 0.013, -0.004, 0.016])
    observed = design @ truth + errors

    # Ordinary least squares via QR (not normal equations).
    q, r = np.linalg.qr(design, mode="reduced")
    ols_parameters = np.linalg.solve(r, q.T @ observed)
    ols_residuals = observed - design @ ols_parameters

    # GLS under an explicitly assumed AR(1)-style covariance model.
    sigma = 0.03
    rho = 0.45
    indices = np.arange(len(observed))
    covariance = sigma**2 * rho ** np.abs(indices[:, None] - indices[None, :])
    chol = np.linalg.cholesky(covariance)
    whitened_design = np.linalg.solve(chol, design)
    whitened_observed = np.linalg.solve(chol, observed)
    qw, rw = np.linalg.qr(whitened_design, mode="reduced")
    gls_parameters = np.linalg.solve(rw, qw.T @ whitened_observed)
    gls_residuals = observed - design @ gls_parameters
    whitened_residuals = np.linalg.solve(chol, gls_residuals)

    # SVD reports numerical rank and conditioning of the whitened model.
    singular_values = np.linalg.svd(whitened_design, compute_uv=False)
    rank_tolerance = np.finfo(float).eps * max(whitened_design.shape) * singular_values[0]
    numerical_rank = int(np.sum(singular_values > rank_tolerance))

    return {
        "affine_x_parameters": x_parameters,
        "affine_y_parameters": y_parameters,
        "affine_control_condition_number": float(np.linalg.cond(control_design)),
        "ols_plane_parameters": ols_parameters,
        "gls_plane_parameters": gls_parameters,
        "ols_residual_rms": float(np.sqrt(np.mean(ols_residuals**2))),
        "gls_residual_rms": float(np.sqrt(np.mean(gls_residuals**2))),
        "gls_whitened_residual_norm": float(np.linalg.norm(whitened_residuals)),
        "whitened_design_singular_values": singular_values,
        "whitened_design_condition_number": float(singular_values[0] / singular_values[-1]),
        "rank_tolerance": float(rank_tolerance),
        "whitened_design_numerical_rank": numerical_rank,
        "assumed_error_sigma": sigma,
        "assumed_error_correlation": rho,
    }


def _json_ready(value: object) -> object:
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


if __name__ == "__main__":
    print(json.dumps({k: _json_ready(v) for k, v in run_case().items()}, indent=2))

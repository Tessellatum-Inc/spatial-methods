"""Reproducible matrix-factorization examples for spatial science.

All data are synthetic, dimensionless teaching values.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import lu, lu_factor, lu_solve


def lu_coordinate_system():
    """Factor and solve a small square coordinate-parameter system."""
    a = np.array([[0.0, 2.0, 1.0], [1.0, -2.0, -3.0], [2.0, 3.0, 1.0]])
    expected = np.array([2.0, -1.0, 3.0])
    b = a @ expected
    p, l, u = lu(a)
    lu_packed, pivots = lu_factor(a)
    solution = lu_solve((lu_packed, pivots), b)
    return {"A": a, "b": b, "P": p, "L": l, "U": u,
            "solution": solution, "factorization_error": np.linalg.norm(a-p@l@u)}


def qr_terrain_plane():
    """Fit z = c + ax + by to synthetic sample points using QR."""
    xy = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.],
                   [2., 0.], [0., 2.], [2., 1.]])
    noise = np.array([0.02, -0.01, 0.01, -0.02, 0.01, -0.01, 0.0])
    z = 100.0 + 2.0*xy[:, 0] - 0.5*xy[:, 1] + noise
    design = np.column_stack((np.ones(len(xy)), xy))
    q, r = np.linalg.qr(design, mode="reduced")
    beta = np.linalg.solve(r, q.T @ z)
    residuals = z - design @ beta
    return {"coefficients": beta, "residual_sum_squares": residuals @ residuals,
            "orthogonality_error": np.linalg.norm(design.T @ residuals)}


def cholesky_gls():
    """Whiten a synthetic correlated-observation model, then solve by QR."""
    design = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
    observations = np.array([10.1, 11.0, 12.2, 12.9])
    covariance = np.array([[1.00, 0.30, 0.10, 0.00],
                           [0.30, 1.00, 0.30, 0.10],
                           [0.10, 0.30, 1.00, 0.30],
                           [0.00, 0.10, 0.30, 1.00]])
    lower = np.linalg.cholesky(covariance)
    aw = np.linalg.solve(lower, design)
    yw = np.linalg.solve(lower, observations)
    q, r = np.linalg.qr(aw, mode="reduced")
    beta = np.linalg.solve(r, q.T @ yw)
    residuals = observations - design @ beta
    whitened_residuals = np.linalg.solve(lower, residuals)
    return {"coefficients": beta, "covariance_cholesky": lower,
            "weighted_residual_sum_squares": whitened_residuals @ whitened_residuals}


def svd_near_dependency():
    """Inspect singular values of almost dependent synthetic directions."""
    a = np.array([[1., 1.], [1., 1.000001], [1., 0.999999]])
    u, singular_values, vt = np.linalg.svd(a, full_matrices=False)
    tolerance = np.finfo(float).eps * max(a.shape) * singular_values[0]
    rank = int(np.sum(singular_values > tolerance))
    return {"singular_values": singular_values, "numerical_rank": rank,
            "tolerance": tolerance, "right_singular_vectors": vt}


def svd_pca():
    """Use SVD of centred synthetic 2D points to obtain principal axes."""
    points = np.array([[0., 0.], [1., 1.1], [2., 1.9],
                       [3., 3.2], [4., 3.9], [5., 5.1]])
    centred = points - points.mean(axis=0)
    u, singular_values, vt = np.linalg.svd(centred, full_matrices=False)
    variances = singular_values**2 / (len(points)-1)
    scores = centred @ vt.T
    return {"mean": points.mean(axis=0), "explained_variances": variances,
            "principal_axes_as_rows": vt, "scores": scores}


def main():
    lu_result = lu_coordinate_system()
    qr_result = qr_terrain_plane()
    gls_result = cholesky_gls()
    svd_result = svd_near_dependency()
    pca_result = svd_pca()
    print("LU solution:", np.round(lu_result["solution"], 6))
    print("LU factorization error:", f'{lu_result["factorization_error"]:.3e}')
    print("QR plane coefficients [c, a, b]:", np.round(qr_result["coefficients"], 6))
    print("QR residual orthogonality error:", f'{qr_result["orthogonality_error"]:.3e}')
    print("Cholesky-whitened GLS coefficients:", np.round(gls_result["coefficients"], 6))
    print("SVD singular values:", np.round(svd_result["singular_values"], 9))
    print("SVD numerical rank at stated tolerance:", svd_result["numerical_rank"])
    print("PCA explained variances:", np.round(pca_result["explained_variances"], 6))


if __name__ == "__main__":
    main()

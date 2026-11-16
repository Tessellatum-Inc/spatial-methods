"""Fay-Herriot area-level empirical best linear unbiased prediction."""
import math
import numpy as np
from scipy.optimize import minimize_scalar


def fay_herriot(direct_estimates, sampling_variances, covariates=None, *,
                tolerance=1e-10, max_iterations=1000):
    """Fit the normal-normal area-level model by REML and return EBLUPs.

    The plug-in MSE is conditional on estimated A and omits variance-component
    estimation uncertainty.
    """
    y = np.asarray(direct_estimates, dtype=float)
    d = np.asarray(sampling_variances, dtype=float)
    if y.ndim != 1 or len(y) < 3 or not np.isfinite(y).all():
        raise ValueError("direct_estimates must be finite 1D values with n>=3")
    if d.shape != y.shape or not np.isfinite(d).all() or np.any(d <= 0):
        raise ValueError("sampling_variances must be finite, positive and aligned")
    X = np.ones((len(y), 1)) if covariates is None else np.asarray(covariates, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if X.ndim != 2 or X.shape[0] != len(y) or X.shape[1] < 1 or not np.isfinite(X).all():
        raise ValueError("covariates must be a finite n-by-p matrix")
    n, p = X.shape
    if n <= p:
        raise ValueError("REML requires more areas than fixed-effect coefficients")
    if np.linalg.matrix_rank(X) != p:
        raise ValueError("covariate design matrix must have full column rank")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")

    def objective(A):
        v = d + A
        xtvx = X.T @ (X / v[:, None])
        sign, logdet = np.linalg.slogdet(xtvx)
        if sign <= 0:
            return math.inf
        beta = np.linalg.solve(xtvx, X.T @ (y / v))
        residual = y - X @ beta
        return 0.5 * (float(np.log(v).sum()) + float(logdet)
                      + float(np.sum(residual * residual / v))
                      + (n - p) * math.log(2 * math.pi))

    scale = max(float(np.var(y)), float(np.mean(d)), 1e-8)
    opt = minimize_scalar(
        lambda log_a: objective(math.exp(log_a)),
        bounds=(math.log(scale * 1e-12), math.log(scale * 1e4)),
        method="bounded", options={"xatol": float(tolerance), "maxiter": max_iterations},
    )
    candidate = math.exp(float(opt.x))
    A = 0.0 if objective(0.0) <= float(opt.fun) else candidate
    v = d + A
    xtvx = X.T @ (X / v[:, None])
    beta_cov = np.linalg.inv(xtvx)
    beta = beta_cov @ (X.T @ (y / v))
    regression = X @ beta
    shrinkage = A / v
    predictions = regression + shrinkage * (y - regression)
    mse = shrinkage * d + (1 - shrinkage) ** 2 * np.einsum("ij,jk,ik->i", X, beta_cov, X)
    return {
        "random_effect_variance": float(A), "beta": beta.tolist(),
        "predictions": predictions.tolist(), "regression_component": regression.tolist(),
        "shrinkage_factors": shrinkage.tolist(), "mse_plugin": mse.tolist(),
        "se_plugin": np.sqrt(np.maximum(mse, 0)).tolist(),
        "reml_objective": float(objective(A)), "converged": bool(opt.success),
        "iterations": int(opt.nfev), "area_count": int(n), "coefficient_count": int(p),
    }

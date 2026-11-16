"""Effort-offset Poisson and NB2 log-linear CPUE standardization."""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln


def fit_cpue_model(catch, effort, covariates, *, distribution="poisson",
                   max_iterations=2000, tolerance=1e-9):
    """Fit a log-linear catch model with log(effort) offset.

    Covariates are numeric columns without an intercept; an intercept is
    added internally. The standardized index predicts catch at unit effort
    and the sample mean covariate vector. NB2 variance is mu + alpha*mu^2.
    """
    y = np.asarray(catch, dtype=float)
    e = np.asarray(effort, dtype=float)
    x = np.asarray(covariates, dtype=float)
    if y.ndim != 1 or e.shape != y.shape or x.ndim != 2 or x.shape[0] != len(y) or len(y) <= x.shape[1]+1:
        raise ValueError("catch, effort and covariates must be aligned with more observations than coefficients")
    if not np.all(np.isfinite(y)) or np.any(y < 0) or np.any(y != np.floor(y)):
        raise ValueError("catch must contain finite non-negative integer counts")
    if not np.all(np.isfinite(e)) or np.any(e <= 0):
        raise ValueError("effort must be finite and positive")
    if not np.all(np.isfinite(x)):
        raise ValueError("covariates must be finite")
    dist = str(distribution).lower()
    if dist not in {"poisson", "nb2"}:
        raise ValueError("distribution must be 'poisson' or 'nb2'")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    design = np.column_stack((np.ones(len(y)), x))
    offset = np.log(e)
    def objective(params):
        beta = params[:design.shape[1]]
        eta = np.clip(offset + design @ beta, -30., 30.)
        mu = np.exp(eta)
        if dist == "poisson":
            loglik = y*eta - mu - gammaln(y+1)
        else:
            alpha = np.exp(np.clip(params[-1], -12., 8.))
            size = 1.0/alpha
            loglik = (gammaln(y+size)-gammaln(size)-gammaln(y+1)
                      + size*(np.log(size)-np.log(size+mu))
                      + y*(eta-np.log(size+mu)))
        return -float(np.sum(loglik))
    initial = np.zeros(design.shape[1] + (1 if dist == "nb2" else 0))
    if dist == "nb2":
        initial[-1] = np.log(.1)
    fit = minimize(objective, initial, method="BFGS",
                   options={"maxiter": int(max_iterations), "gtol": float(tolerance)})
    if not np.all(np.isfinite(fit.x)) or not np.isfinite(fit.fun):
        raise RuntimeError("CPUE likelihood optimization did not produce finite estimates")
    beta = fit.x[:design.shape[1]]
    reference = np.r_[1.0, x.mean(axis=0)]
    standardized = float(np.exp(np.clip(reference @ beta, -30., 30.)))
    fitted = np.exp(np.clip(offset + design @ beta, -30., 30.))
    return {"coefficients": beta, "fitted_catch": fitted,
            "standardized_cpue": standardized,
            "dispersion": float(np.exp(fit.x[-1])) if dist == "nb2" else 0.0,
            "distribution": dist, "negative_log_likelihood": float(fit.fun),
            "converged": bool(fit.success), "optimizer_message": str(fit.message),
            "reference_covariates": x.mean(axis=0)}


def predict_cpue(model, covariates, *, effort=1.0):
    """Predict catch for new covariates and effort using a fitted model."""
    x = np.asarray(covariates, dtype=float)
    if x.ndim == 1:
        x = x[None, :]
    beta = np.asarray(model["coefficients"], dtype=float)
    if x.ndim != 2 or x.shape[1] != len(beta)-1 or not np.all(np.isfinite(x)):
        raise ValueError("covariates must be finite with the fitted feature count")
    e = np.asarray(effort, dtype=float)
    if not np.all(np.isfinite(e)) or np.any(e <= 0):
        raise ValueError("effort must be finite and positive")
    eta = np.log(e) + beta[0] + x @ beta[1:]
    return np.exp(np.clip(eta, -30., 30.))

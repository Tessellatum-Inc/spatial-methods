"""Two-market long-run price relation and error-correction model."""
from __future__ import annotations
import numpy as np
from scipy.stats import t as student_t


def fit_error_correction_model(source_price, target_price):
    """Fit a two-stage long-run relation and short-run error-correction model.

    Stage 1: target_t = c + beta*source_t + residual_t.
    Stage 2: delta(target_t) = a + lambda*residual_(t-1)
              + gamma*delta(source_t) + error_t.
    The adjustment coefficient lambda is expected to be negative when the
    target market corrects positive long-run disequilibrium.
    """
    source = np.asarray(source_price, dtype=float)
    target = np.asarray(target_price, dtype=float)
    if source.ndim != 1 or target.ndim != 1 or source.shape != target.shape or len(source) < 10:
        raise ValueError("price series must be matching 1D arrays with at least ten observations")
    if not np.all(np.isfinite(source)) or not np.all(np.isfinite(target)):
        raise ValueError("price series must be finite")
    if np.ptp(source) <= np.finfo(float).eps:
        raise ValueError("source price must vary")
    long_design = np.column_stack((np.ones(len(source)), source))
    long_coef, _, rank, _ = np.linalg.lstsq(long_design, target, rcond=None)
    if rank < 2:
        raise ValueError("long-run price relation is rank deficient")
    residual = target - long_design @ long_coef
    dy, dx, lagged_error = np.diff(target), np.diff(source), residual[:-1]
    short_design = np.column_stack((np.ones(len(dy)), lagged_error, dx))
    coef, _, rank, _ = np.linalg.lstsq(short_design, dy, rcond=None)
    if rank < short_design.shape[1]:
        raise ValueError("short-run error-correction design is rank deficient")
    fitted = short_design @ coef
    errors = dy - fitted
    dof = len(dy) - short_design.shape[1]
    if dof <= 0:
        raise ValueError("insufficient residual degrees of freedom")
    sigma2 = float(errors @ errors / dof)
    covariance = sigma2 * np.linalg.inv(short_design.T @ short_design)
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    t_statistics = np.divide(coef, standard_errors,
                             out=np.full_like(coef, np.nan),
                             where=standard_errors > 0)
    p_values = 2.0 * student_t.sf(np.abs(t_statistics), dof)
    total = float(np.sum((dy-dy.mean())**2))
    r_squared = 1.0 - float(errors @ errors)/total if total > 0 else 1.0
    return {"long_run_intercept": float(long_coef[0]),
            "long_run_elasticity": float(long_coef[1]),
            "long_run_residuals": residual,
            "short_run_intercept": float(coef[0]),
            "error_correction_speed": float(coef[1]),
            "source_price_change_effect": float(coef[2]),
            "standard_errors": standard_errors,
            "t_statistics": t_statistics, "p_values": p_values,
            "short_run_r_squared": r_squared,
            "residual_variance": sigma2, "degrees_of_freedom": int(dof)}

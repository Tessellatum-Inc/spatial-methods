"""Residual-based snapshot RAIM screening for a linearised measurement model."""
from __future__ import annotations

import numpy as np
from scipy.stats import chi2


def _validate_inputs(y, design, covariance):
    y = np.asarray(y, dtype=float)
    h = np.asarray(design, dtype=float)
    r = np.asarray(covariance, dtype=float)
    if y.ndim != 1 or h.ndim != 2 or r.ndim != 2:
        raise ValueError("y, design and covariance must be 1D, 2D and 2D")
    m, n = h.shape
    if y.shape != (m,) or r.shape != (m, m) or m <= n:
        raise ValueError("require y length m, covariance (m,m), and m > n")
    if not (np.all(np.isfinite(y)) and np.all(np.isfinite(h)) and np.all(np.isfinite(r))):
        raise ValueError("inputs must be finite")
    if not np.allclose(r, r.T, rtol=1e-10, atol=1e-12):
        raise ValueError("covariance must be symmetric")
    try:
        lower = np.linalg.cholesky(r)
    except np.linalg.LinAlgError as exc:
        raise ValueError("covariance must be positive definite") from exc
    return y, h, r, lower


def weighted_least_squares(y, design, covariance):
    """Fit y = Hx + noise with known positive-definite observation covariance.

    Returns the GLS estimate, its covariance, residuals and weighted residual
    sum of squares. The model is linearised/snapshot; no temporal or nonlinear
    navigation model is implied.
    """
    y, h, r, lower = _validate_inputs(y, design, covariance)
    yw = np.linalg.solve(lower, y)
    hw = np.linalg.solve(lower, h)
    if np.linalg.matrix_rank(hw) < h.shape[1]:
        raise ValueError("whitened design matrix must have full column rank")
    x, _, _, _ = np.linalg.lstsq(hw, yw, rcond=None)
    normal = hw.T @ hw
    x_cov = np.linalg.inv(normal)
    residual = y - h @ x
    rw = np.linalg.solve(lower, residual)
    statistic = float(rw @ rw)
    return {
        "estimate": x,
        "estimate_covariance": x_cov,
        "residuals": residual,
        "weighted_residual_sum_squares": statistic,
        "degrees_of_freedom": int(len(y) - h.shape[1]),
    }


def residual_global_test(y, design, covariance, false_alarm_probability=0.001):
    """Chi-square global consistency test under known Gaussian covariance.

    The null statistic is chi-square with m - rank(H) degrees of freedom.
    """
    alpha = float(false_alarm_probability)
    if not np.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("false_alarm_probability must lie strictly between 0 and 1")
    fit = weighted_least_squares(y, design, covariance)
    dof = fit["degrees_of_freedom"]
    threshold = float(chi2.ppf(1.0 - alpha, dof))
    statistic = fit["weighted_residual_sum_squares"]
    return {
        **fit,
        "threshold": threshold,
        "p_value": float(chi2.sf(statistic, dof)),
        "false_alarm_probability": alpha,
        "alarm": bool(statistic > threshold),
    }


def single_fault_exclusion(y, design, covariance, false_alarm_probability=0.001):
    """Run a global test and evaluate each single-measurement deletion.

    Candidate subset tests use a Bonferroni-adjusted upper-tail level
    alpha/m. A unique passing deletion is reported as the isolated index;
    zero or multiple passing deletions remain unresolved. This is a teaching
    FDE baseline, not a certified aviation RAIM algorithm.
    """
    y, h, r, _ = _validate_inputs(y, design, covariance)
    alpha = float(false_alarm_probability)
    if not np.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("false_alarm_probability must lie strictly between 0 and 1")
    global_result = residual_global_test(y, h, r, alpha)
    if not global_result["alarm"]:
        return {
            "global_test": global_result,
            "candidate_tests": [],
            "excluded_index": None,
            "status": "no_global_alarm",
        }

    m = len(y)
    adjusted_alpha = alpha / m
    candidates = []
    for index in range(m):
        keep = np.arange(m) != index
        try:
            fit = weighted_least_squares(y[keep], h[keep], r[np.ix_(keep, keep)])
        except ValueError as exc:
            candidates.append({"excluded_index": index, "passes": False, "reason": str(exc)})
            continue
        dof = fit["degrees_of_freedom"]
        threshold = float(chi2.ppf(1.0 - adjusted_alpha, dof))
        statistic = fit["weighted_residual_sum_squares"]
        candidates.append({
            "excluded_index": index,
            "statistic": statistic,
            "degrees_of_freedom": dof,
            "threshold": threshold,
            "p_value": float(chi2.sf(statistic, dof)),
            "adjusted_alpha": adjusted_alpha,
            "passes": bool(statistic <= threshold),
        })
    passing = [item["excluded_index"] for item in candidates if item["passes"]]
    if len(passing) == 1:
        status, excluded = "single_fault_isolated", passing[0]
    elif len(passing) > 1:
        status, excluded = "ambiguous_multiple_candidates", None
    else:
        status, excluded = "fault_not_isolated", None
    return {
        "global_test": global_result,
        "candidate_tests": candidates,
        "excluded_index": excluded,
        "status": status,
    }

"""Weighted least-squares adjustment and Baarda-style data-snooping diagnostics."""
from __future__ import annotations
import numpy as np


def adjust_and_snoop(design, observations, covariance=None, sigma0=1.0, critical_value=3.29):
    """Fit a full-rank linear Gauss-Markov model and compute global/local tests.

    Model: l = A x + e, Cov(e) = sigma0**2 * Q_ll. covariance is Q_ll,
    the observation cofactor/correlation-scale matrix (identity by default).
    The global statistic is v' Q_ll^-1 v / sigma0**2 with m-rank(A) degrees
    of freedom. Local w_i = v_i / (sigma0 * sqrt(Q_vv[i,i])).

    The caller supplies a critical value so multiple-testing policy is explicit.
    This is a single-adjustment diagnostic, not automatic iterative deletion.
    """
    A=np.asarray(design,dtype=float); l=np.asarray(observations,dtype=float)
    if A.ndim!=2 or l.ndim!=1 or A.shape[0]!=l.size:
        raise ValueError("design must be 2D and observations must match its rows")
    m,n=A.shape
    if m<=n or n<1 or not np.all(np.isfinite(A)) or not np.all(np.isfinite(l)):
        raise ValueError("need finite design/observations and positive residual degrees of freedom")
    if np.linalg.matrix_rank(A)<n:
        raise ValueError("design matrix must have full column rank")
    if not np.isfinite(sigma0) or sigma0<=0:
        raise ValueError("sigma0 must be finite and positive")
    if not np.isfinite(critical_value) or critical_value<=0:
        raise ValueError("critical_value must be finite and positive")
    Q=np.eye(m) if covariance is None else np.asarray(covariance,dtype=float)
    if Q.shape!=(m,m) or not np.all(np.isfinite(Q)) or not np.allclose(Q,Q.T,atol=1e-10):
        raise ValueError("covariance must be a finite symmetric m by m matrix")
    try: np.linalg.cholesky(Q)
    except np.linalg.LinAlgError as exc: raise ValueError("covariance must be positive definite") from exc
    QinvA=np.linalg.solve(Q,A); Qinvl=np.linalg.solve(Q,l)
    normal=A.T@QinvA
    try: Qxx=np.linalg.inv(normal)
    except np.linalg.LinAlgError as exc: raise ValueError("normal matrix is singular") from exc
    xhat=Qxx@(A.T@Qinvl); residual=l-A@xhat
    Qvv=Q-A@Qxx@A.T; Qvv=(Qvv+Qvv.T)/2
    qdiag=np.diag(Qvv)
    tol=100*np.finfo(float).eps*np.maximum(1.0,np.diag(Q))
    if np.any(qdiag < -tol):
        raise ValueError("computed residual covariance is not positive semidefinite")
    qdiag=np.maximum(qdiag,0.0)
    identifiable=qdiag>tol
    w=np.full(m,np.nan)
    w[identifiable]=residual[identifiable]/(sigma0*np.sqrt(qdiag[identifiable]))
    if not np.any(identifiable):
        raise ValueError("no observations have positive residual redundancy")
    global_stat=float(residual@np.linalg.solve(Q,residual)/(sigma0**2))
    largest=int(np.nanargmax(np.abs(w)))
    return {
        "estimate":xhat, "parameter_covariance":sigma0**2*Qxx,
        "residuals":residual, "residual_covariance":sigma0**2*Qvv,
        "redundancy_numbers":np.diag(Qvv)/np.diag(Q),
        "standardized_residuals":w, "suspect_indices":np.flatnonzero(np.abs(w)>critical_value),
        "largest_absolute_w_index":largest,
        "global_statistic":global_stat, "global_degrees_of_freedom":m-n,
        "local_critical_value":float(critical_value),
        "local_test_defined":identifiable,
    }


def pope_tau_test(design, observations, covariance=None, significance_level=0.05):
    """Pope's internally studentized residual test with a Bonferroni family level.

    The a-posteriori variance factor is s0² = v' Q_ll^-1 v / r, where
    r = m - rank(A). Each residual statistic is |v_i|/(s0 sqrt(q_vv,ii)).
    The tau critical value is the Student-t transform with r degrees of
    freedom, using t_(r-1). A two-sided alpha/m tail allocation controls
    family-wise error conservatively across m tested observations.

    This is a single-adjustment diagnostic. It does not iteratively delete
    observations or solve masking/swamping caused by multiple outliers.
    """
    from scipy.stats import t as student_t

    alpha = float(significance_level)
    if not np.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("significance_level must lie strictly between 0 and 1")
    fit = adjust_and_snoop(
        design, observations, covariance=covariance,
        sigma0=1.0, critical_value=np.finfo(float).max,
    )
    dof = int(fit["global_degrees_of_freedom"])
    if dof < 2:
        raise ValueError("Pope tau test requires at least two residual degrees of freedom")
    m = len(fit["residuals"])
    t_critical = float(student_t.ppf(1.0 - alpha / (2.0 * m), dof - 1))
    critical_tau = float(np.sqrt(dof) * t_critical / np.sqrt(dof - 1 + t_critical**2))
    variance_factor = float(fit["global_statistic"] / dof)
    qvv = np.asarray(fit["residual_covariance"], dtype=float)
    qdiag = np.diag(qvv)
    residuals = np.asarray(fit["residuals"], dtype=float)
    tau = np.full(m, np.nan)
    scale = max(1.0, float(np.max(np.abs(qdiag))), float(np.max(np.abs(residuals)))**2)
    tolerance = 100.0 * np.finfo(float).eps * scale
    valid = qdiag > tolerance
    if variance_factor <= tolerance:
        return {
            "status": "zero_residual_variance",
            "estimate": fit["estimate"],
            "residuals": residuals,
            "variance_factor": variance_factor,
            "degrees_of_freedom": dof,
            "tau_statistics": tau,
            "critical_tau": critical_tau,
            "critical_t": t_critical,
            "significance_level": alpha,
            "familywise_adjusted_tail_probability": alpha / (2.0 * m),
            "largest_absolute_tau_index": None,
            "flagged_indices": [],
        }
    tau[valid] = np.abs(residuals[valid]) / np.sqrt(variance_factor * qdiag[valid])
    if not np.any(valid):
        raise ValueError("no observations have positive residual redundancy")
    largest = int(np.nanargmax(tau))
    flagged = np.flatnonzero(tau > critical_tau)
    return {
        "status": "outlier_flagged" if len(flagged) else "no_outlier_flagged",
        "estimate": fit["estimate"],
        "residuals": residuals,
        "variance_factor": variance_factor,
        "degrees_of_freedom": dof,
        "tau_statistics": tau,
        "critical_tau": critical_tau,
        "critical_t": t_critical,
        "significance_level": alpha,
        "familywise_adjusted_tail_probability": alpha / (2.0 * m),
        "largest_absolute_tau_index": largest,
        "flagged_indices": flagged,
    }

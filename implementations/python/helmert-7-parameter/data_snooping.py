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
    if np.any(qdiag<=np.finfo(float).eps*np.maximum(1.0,np.diag(Q))):
        raise ValueError("one or more observations have zero numerical residual redundancy")
    w=residual/(sigma0*np.sqrt(qdiag))
    global_stat=float(residual@np.linalg.solve(Q,residual)/(sigma0**2))
    return {
        "estimate":xhat, "parameter_covariance":sigma0**2*Qxx,
        "residuals":residual, "residual_covariance":sigma0**2*Qvv,
        "redundancy_numbers":np.diag(Qvv)/np.diag(Q),
        "standardized_residuals":w, "suspect_indices":np.flatnonzero(np.abs(w)>critical_value),
        "largest_absolute_w_index":int(np.argmax(np.abs(w))),
        "global_statistic":global_stat, "global_degrees_of_freedom":m-n,
        "local_critical_value":float(critical_value),
    }

"""Cross-sectional absolute/conditional beta-convergence OLS baseline."""
from __future__ import annotations
import numpy as np


def beta_convergence(income_start, income_end, periods=1.0, controls=None):
    """Fit annualized log growth on initial log income and optional controls.

    log(y_T/y_0)/T = intercept + beta*log(y_0) + controls*gamma + error.
    Reports conventional OLS estimates and HC1 heteroskedasticity-robust
    covariance. A negative beta indicates absolute (or conditional, when
    controls are supplied) beta-convergence under this specification.
    """
    y0=np.asarray(income_start,dtype=float); y1=np.asarray(income_end,dtype=float)
    if y0.ndim!=1 or y1.ndim!=1 or y0.size!=y1.size or y0.size<4:
        raise ValueError("income arrays must be equal-length vectors with at least four regions")
    if not np.all(np.isfinite(y0)) or not np.all(np.isfinite(y1)) or np.any(y0<=0) or np.any(y1<=0):
        raise ValueError("income values must be finite and strictly positive")
    T=float(periods)
    if not np.isfinite(T) or T<=0: raise ValueError("periods must be finite and positive")
    n=y0.size; x0=np.log(y0); growth=np.log(y1/y0)/T
    if controls is None: C=np.empty((n,0))
    else:
        C=np.asarray(controls,dtype=float)
        if C.ndim==1: C=C[:,None]
        if C.ndim!=2 or C.shape[0]!=n or not np.all(np.isfinite(C)):
            raise ValueError("controls must be a finite n by p matrix")
    X=np.column_stack([np.ones(n),x0,C]); k=X.shape[1]
    if n<=k: raise ValueError("number of regions must exceed number of regression parameters")
    if np.linalg.matrix_rank(X)<k: raise ValueError("regression design must have full column rank")
    xtx_inv=np.linalg.inv(X.T@X); coef=xtx_inv@(X.T@growth)
    residual=growth-X@coef; dof=n-k
    sse=float(residual@residual); sst=float(np.sum((growth-growth.mean())**2))
    sigma2=sse/dof
    ols_cov=sigma2*xtx_inv
    meat=X.T@((residual**2)[:,None]*X)
    hc1_cov=(n/dof)*xtx_inv@meat@xtx_inv
    beta=float(coef[1]); speed=None; half_life=None
    if -1.0<beta<0.0:
        speed=float(-np.log1p(beta)/T)
        half_life=float(np.log(2)/speed)
    return {"coefficients":coef,"ols_standard_errors":np.sqrt(np.maximum(0,np.diag(ols_cov))),
            "hc1_standard_errors":np.sqrt(np.maximum(0,np.diag(hc1_cov))),
            "residuals":residual,"r_squared":1-sse/sst if sst>0 else np.nan,
            "n_regions":int(n),"n_parameters":int(k),"degrees_of_freedom":int(dof),
            "beta":beta,"convergence_speed_per_period":speed,"half_life_periods":half_life,
            "specification":"conditional" if controls is not None else "absolute"}

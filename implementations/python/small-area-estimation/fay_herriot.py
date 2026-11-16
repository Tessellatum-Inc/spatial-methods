"""Area-level Fay-Herriot empirical-Bayes small-area estimation."""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize_scalar


def fay_herriot(direct_estimates, sampling_variances, covariates, *, reml=True):
    """Fit area-level Gaussian Fay-Herriot model by ML or REML.

    Model: y = X beta + u + e, with u~N(0,tau2 I) and
    e~N(0,diag(sampling_variances)). Covariates must include an intercept
    column if one is wanted. Returns plug-in EB estimates and conditional
    random-effect posterior variances (not full MSE including variance-
    component and beta estimation uncertainty).
    """
    y=np.asarray(direct_estimates,dtype=float)
    d=np.asarray(sampling_variances,dtype=float)
    x=np.asarray(covariates,dtype=float)
    if y.ndim!=1 or len(y)<3 or not np.isfinite(y).all():
        raise ValueError("direct_estimates must be a finite vector with at least three areas")
    if d.shape!=y.shape or not np.isfinite(d).all() or np.any(d<=0):
        raise ValueError("sampling_variances must be finite, positive and match estimates")
    if x.ndim!=2 or x.shape[0]!=len(y) or x.shape[1]<1 or not np.isfinite(x).all():
        raise ValueError("covariates must be a finite area-by-predictor matrix")
    p=x.shape[1]
    if len(y)<=p or np.linalg.matrix_rank(x)<p:
        raise ValueError("covariate design must have full column rank and fewer predictors than areas")
    if not isinstance(reml,(bool,np.bool_)):
        raise ValueError("reml must be boolean")

    def solve(tau2, return_all=False):
        v=d+tau2
        w=1.0/v
        xtwx=x.T@(w[:,None]*x)
        if np.linalg.matrix_rank(xtwx)<p:
            return np.inf if not return_all else None
        cov_beta=np.linalg.inv(xtwx)
        beta=cov_beta@(x.T@(w*y))
        residual=y-x@beta
        q=float(np.sum(w*residual**2))
        sign,logdet_v=np.linalg.slogdet(np.diag(v))
        if sign<=0: return np.inf if not return_all else None
        objective=logdet_v+q
        if reml:
            sign2,logdet_x=np.linalg.slogdet(xtwx)
            if sign2<=0: return np.inf if not return_all else None
            objective+=logdet_x
        if return_all: return beta,cov_beta,residual,v
        return .5*objective

    scale=max(float(np.var(y)),float(np.mean(d)),1e-8)
    upper=scale*1e4
    opt=minimize_scalar(solve,bounds=(0.0,upper),method="bounded",
                        options={"xatol":max(1e-12,scale*1e-10)})
    candidates=[(0.0,solve(0.0))]
    if opt.success: candidates.append((float(opt.x),float(opt.fun)))
    tau2,value=min(candidates,key=lambda z:z[1])
    fitted=solve(tau2,True)
    if fitted is None: raise RuntimeError("Fay-Herriot GLS system is singular")
    beta,cov_beta,residual,v=fitted
    shrink=tau2/(tau2+d)
    estimate=x@beta+shrink*residual
    conditional_var=tau2*d/(tau2+d)
    return {"estimate":estimate,"regression_mean":x@beta,
            "shrinkage_factor":shrink,"conditional_random_effect_variance":conditional_var,
            "beta":beta,"beta_covariance":cov_beta,"between_area_variance":float(tau2),
            "objective":float(value),"variance_estimator":"REML" if reml else "ML",
            "n_areas":int(len(y))}

"""Laplace posterior approximation and componentwise slice sampling."""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import minimize


@dataclass(frozen=True)
class LaplaceResult:
    mode: np.ndarray
    covariance: np.ndarray
    precision: np.ndarray
    log_density_mode: float
    log_evidence: float
    optimizer_success: bool
    optimizer_message: str


def _finite_log_density(log_density, x):
    value=float(log_density(np.asarray(x,dtype=float)))
    if not math.isfinite(value): raise ValueError("log_density must be finite at evaluated points")
    return value


def _negative_hessian(log_density, mode):
    x=np.asarray(mode,dtype=float);n=x.size
    steps=np.finfo(float).eps**0.25*np.maximum(1.0,np.abs(x))
    h=np.empty((n,n),dtype=float);f0=_finite_log_density(log_density,x)
    for i in range(n):
        ei=np.zeros(n);ei[i]=steps[i]
        h[i,i]=-(_finite_log_density(log_density,x+ei)-2*f0+_finite_log_density(log_density,x-ei))/(steps[i]**2)
        for j in range(i):
            ej=np.zeros(n);ej[j]=steps[j]
            value=-(_finite_log_density(log_density,x+ei+ej)-_finite_log_density(log_density,x+ei-ej)
                    -_finite_log_density(log_density,x-ei+ej)+_finite_log_density(log_density,x-ei-ej))/(4*steps[i]*steps[j])
            h[i,j]=h[j,i]=value
    return (h+h.T)/2


def laplace_approximation(log_density, initial, *, max_iter=2000, tolerance=1e-9):
    """Find the posterior mode and approximate covariance/evidence locally."""
    x0=np.asarray(initial,dtype=float)
    if x0.ndim!=1 or x0.size==0 or not np.isfinite(x0).all():
        raise ValueError("initial must be a non-empty finite vector")
    if not isinstance(max_iter,int) or max_iter<1 or not np.isfinite(tolerance) or tolerance<=0:
        raise ValueError("max_iter and tolerance must be positive")
    result=minimize(lambda x:-float(log_density(x)),x0,method="BFGS",
                    options={"maxiter":max_iter,"gtol":tolerance})
    mode=np.asarray(result.x,dtype=float)
    log_mode=_finite_log_density(log_density,mode)
    precision=_negative_hessian(log_density,mode)
    try:
        chol=np.linalg.cholesky(precision)
    except np.linalg.LinAlgError as exc:
        raise ValueError("negative log-density Hessian at mode must be positive definite") from exc
    covariance=np.linalg.solve(precision,np.eye(mode.size))
    logdet=2*np.log(np.diag(chol)).sum()
    log_evidence=log_mode+0.5*mode.size*math.log(2*math.pi)-0.5*logdet
    return LaplaceResult(mode,covariance,precision,log_mode,float(log_evidence),
                         bool(result.success),str(result.message))


def slice_sample(log_density, initial, *, n_samples=1000, burn_in=500,
                 width=1.0, max_steps_out=100, seed=None):
    """Componentwise univariate stepping-out slice sampler."""
    x=np.asarray(initial,dtype=float).copy()
    if x.ndim!=1 or x.size==0 or not np.isfinite(x).all():
        raise ValueError("initial must be a non-empty finite vector")
    if not isinstance(n_samples,int) or n_samples<1 or not isinstance(burn_in,int) or burn_in<0:
        raise ValueError("n_samples must be positive and burn_in nonnegative")
    if not np.isfinite(width) or width<=0 or not isinstance(max_steps_out,int) or max_steps_out<1:
        raise ValueError("width and max_steps_out must be positive")
    current=_finite_log_density(log_density,x);rng=np.random.default_rng(seed)
    out=np.empty((n_samples,x.size),dtype=float)
    for sweep in range(burn_in+n_samples):
        for dimension in range(x.size):
            level=current+math.log(rng.random())
            left=x[dimension]-width*rng.random();right=left+width
            left_steps=int(rng.integers(max_steps_out+1));right_steps=max_steps_out-left_steps
            probe=x.copy()
            for _ in range(left_steps):
                probe[dimension]=left
                if float(log_density(probe))<=level: break
                left-=width
            for _ in range(right_steps):
                probe[dimension]=right
                if float(log_density(probe))<=level: break
                right+=width
            while True:
                candidate=rng.uniform(left,right);probe=x.copy();probe[dimension]=candidate
                candidate_log=float(log_density(probe))
                if candidate_log>=level:
                    x=probe;current=candidate_log;break
                if candidate<x[dimension]: left=candidate
                else: right=candidate
        if sweep>=burn_in: out[sweep-burn_in]=x
    return out

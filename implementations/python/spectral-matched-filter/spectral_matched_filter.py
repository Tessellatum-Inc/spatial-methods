"""Adaptive spectral matched filter for a known target signature."""
from __future__ import annotations
import numpy as np

def spectral_matched_filter(cube, target, background_mask=None, covariance=None, regularization=1e-6):
    """Return matched-filter scores under a global background covariance model."""
    x=np.asarray(cube,dtype=float); t=np.asarray(target,dtype=float)
    if x.ndim!=3 or t.shape!=(x.shape[-1],): raise ValueError("cube must be rows x cols x bands and target one spectrum")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(t)): raise ValueError("inputs must be finite")
    if not (0<=regularization<1): raise ValueError("regularization must be in [0,1)")
    valid=np.ones(x.shape[:2],bool) if background_mask is None else np.asarray(background_mask,dtype=bool)
    if valid.shape!=x.shape[:2] or valid.sum()<2: raise ValueError("background mask must select at least two pixels")
    bg=x[valid]; mean=bg.mean(axis=0)
    cov=np.cov(bg,rowvar=False,ddof=1) if covariance is None else np.asarray(covariance,dtype=float)
    cov=np.atleast_2d(cov)
    if cov.shape!=(x.shape[-1],x.shape[-1]) or not np.all(np.isfinite(cov)): raise ValueError("covariance shape or values invalid")
    cov=(cov+cov.T)/2
    eig,vec=np.linalg.eigh(cov); scale=max(float(np.max(np.abs(eig))),np.finfo(float).eps)
    if np.min(eig)<-scale*1e-8: raise ValueError("covariance must be positive semidefinite")
    floor=max(scale*regularization,scale*1e-12)
    inv=vec@np.diag(1/np.maximum(eig,floor))@vec.T
    delta=t-mean; denom=float(delta@inv@delta)
    if denom<=floor: raise ValueError("target signature is indistinguishable from background mean")
    weights=inv@delta/denom
    scores=np.einsum("...i,i->...",x-mean,weights)
    return {"scores":scores,"weights":weights,"background_mean":mean,
            "covariance":cov,"target_contrast":delta,"eigenvalue_floor":floor}

"""Adaptive Coherence Estimator (ACE) spectral target detector."""
import numpy as np

def ace_detect(cube, target, background_mask=None, covariance=None, regularization=1e-6):
    x=np.asarray(cube,dtype=float); t=np.asarray(target,dtype=float)
    if x.ndim!=3 or t.shape!=(x.shape[-1],): raise ValueError("cube must be rows x cols x bands and target one spectrum")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(t)): raise ValueError("inputs must be finite")
    if not 0<=regularization<1: raise ValueError("regularization must be in [0,1)")
    mask=np.ones(x.shape[:2],bool) if background_mask is None else np.asarray(background_mask,dtype=bool)
    if mask.shape!=x.shape[:2] or mask.sum()<2: raise ValueError("mask must select at least two pixels")
    bg=x[mask]; mean=bg.mean(axis=0)
    C=np.cov(bg,rowvar=False,ddof=1) if covariance is None else np.asarray(covariance,dtype=float)
    C=np.atleast_2d(C)
    if C.shape!=(x.shape[-1],x.shape[-1]) or not np.all(np.isfinite(C)): raise ValueError("covariance shape or values invalid")
    C=(C+C.T)/2; vals,vec=np.linalg.eigh(C); scale=max(float(np.max(np.abs(vals))),np.finfo(float).eps)
    if vals.min() < -scale*1e-8: raise ValueError("covariance must be positive semidefinite")
    floor=max(scale*regularization,scale*1e-12)
    inv=vec@np.diag(1/np.maximum(vals,floor))@vec.T
    d=t-mean; dnorm=float(d@inv@d)
    if dnorm<=floor: raise ValueError("target indistinguishable from background mean")
    centered=x-mean
    numerator=np.einsum("...i,ij,j->...",centered,inv,d)**2
    energy=np.einsum("...i,ij,...j->...",centered,inv,centered)
    scores=np.divide(numerator,dnorm*energy,out=np.zeros_like(energy),where=energy>floor)
    scores=np.clip(scores,0.,1.)
    return {"scores":scores,"background_mean":mean,"covariance":C,
            "target_contrast":d,"eigenvalue_floor":floor}

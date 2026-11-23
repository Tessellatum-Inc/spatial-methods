"""Global Reed-Xiaoli (RX) hyperspectral anomaly detector."""
from __future__ import annotations
import numpy as np

def rx_detector(cube, mask=None, covariance=None, regularization=1e-6):
    """Return squared Mahalanobis RX scores and estimated background moments."""
    x=np.asarray(cube,dtype=float)
    if x.ndim!=3 or not np.all(np.isfinite(x)): raise ValueError("cube must be finite rows x cols x bands")
    valid=np.ones(x.shape[:2],bool) if mask is None else np.asarray(mask,dtype=bool)
    if valid.shape!=x.shape[:2] or valid.sum()<2: raise ValueError("mask must select at least two pixels")
    if not (0<=regularization<1): raise ValueError("regularization must be in [0,1)")
    samples=x[valid]; mean=samples.mean(axis=0); centered=samples-mean
    cov=np.cov(centered,rowvar=False,ddof=1)
    cov=np.atleast_2d(cov)
    if covariance is not None:
        cov=np.asarray(covariance,dtype=float)
        if cov.shape!=(x.shape[-1],x.shape[-1]) or not np.all(np.isfinite(cov)):
            raise ValueError("covariance must be finite bands x bands")
    cov=(cov+cov.T)/2
    eig,vec=np.linalg.eigh(cov)
    scale=max(float(np.max(np.abs(eig))),np.finfo(float).eps)
    if np.min(eig)<-scale*1e-8: raise ValueError("covariance must be positive semidefinite")
    floor=max(scale*regularization,scale*1e-12)
    inv=vec @ np.diag(1/np.maximum(eig,floor)) @ vec.T
    delta=x-mean
    scores=np.einsum("...i,ij,...j->...",delta,inv,delta)
    scores[~valid]=np.nan
    return {"scores":scores,"mean":mean,"covariance":cov,"eigenvalue_floor":floor}

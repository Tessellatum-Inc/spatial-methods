"""Minimum Noise Fraction transform for pixel-by-band data."""
from __future__ import annotations
import numpy as np

def estimate_noise_covariance(data, mask=None):
    """Estimate band noise covariance from adjacent differences / 2.

    Assumes locally smooth signal and approximately independent, stationary
    noise between adjacent pixels. Horizontal and vertical pairs are pooled.
    """
    x=np.asarray(data,dtype=float)
    if x.ndim!=3 or not np.all(np.isfinite(x)): raise ValueError("data must be finite (rows, cols, bands)")
    valid=np.ones(x.shape[:2],bool) if mask is None else np.asarray(mask,dtype=bool)
    if valid.shape!=x.shape[:2]: raise ValueError("mask shape mismatch")
    diffs=[]
    for a,b in ((x[:,:-1],x[:,1:]),(x[:-1,:],x[1:,:])):
        ok=valid[:,:-1]&valid[:,1:] if a.shape[1]!=x.shape[1] else valid[:-1,:]&valid[1:,:]
        if np.any(ok): diffs.append((a-b)[ok])
    if not diffs: raise ValueError("not enough valid adjacent pixel pairs")
    d=np.concatenate(diffs,axis=0)
    if d.shape[0]<2: raise ValueError("at least two valid differences are required")
    return np.cov(d,rowvar=False,ddof=1)/2.0

def mnf_transform(data, noise_covariance=None, mask=None, n_components=None, regularization=1e-8):
    """Return MNF scores, eigenvalues, band loadings and covariance diagnostics.

    Rows/columns are pixels and the final axis is spectral bands. The noise
    covariance may be supplied or estimated from adjacent-pixel differences.
    """
    x=np.asarray(data,dtype=float)
    if x.ndim!=3 or not np.all(np.isfinite(x)): raise ValueError("data must be finite (rows, cols, bands)")
    bands=x.shape[2]
    valid=np.ones(x.shape[:2],bool) if mask is None else np.asarray(mask,dtype=bool)
    if valid.shape!=x.shape[:2] or valid.sum()<2: raise ValueError("mask must select at least two pixels")
    if not (0<=regularization<1): raise ValueError("regularization must be in [0, 1)")
    samples=x[valid]
    mean=samples.mean(axis=0)
    centered=samples-mean
    signal_cov=np.atleast_2d(np.cov(centered,rowvar=False,ddof=1))
    noise=estimate_noise_covariance(x,valid) if noise_covariance is None else np.asarray(noise_covariance,dtype=float)
    if noise.shape!=(bands,bands) or not np.all(np.isfinite(noise)): raise ValueError("noise_covariance must be finite bands x bands")
    noise=(noise+noise.T)/2
    vals,vecs=np.linalg.eigh(noise)
    scale=max(float(np.max(np.abs(vals))),np.finfo(float).eps)
    floor=max(scale*regularization,scale*1e-12)
    if np.min(vals)<-scale*1e-8: raise ValueError("noise covariance must be positive semidefinite")
    vals=np.maximum(vals,floor)
    whitening=vecs @ np.diag(1/np.sqrt(vals)) @ vecs.T
    whitened=whitening @ signal_cov @ whitening
    eig,rot=np.linalg.eigh((whitened+whitened.T)/2)
    order=np.argsort(eig)[::-1]
    eig=np.maximum(eig[order],0)
    loadings=whitening @ rot[:,order]
    k=bands if n_components is None else n_components
    if not isinstance(k,(int,np.integer)) or k<1 or k>bands: raise ValueError("n_components must be between 1 and band count")
    loadings=loadings[:,:k]; eig=eig[:k]
    scores=np.full(x.shape[:2]+(k,),np.nan,dtype=float)
    scores[valid]=centered @ loadings
    return {"scores":scores,"eigenvalues":eig,"loadings":loadings,"mean":mean,
            "signal_covariance":signal_cov,"noise_covariance":noise,
            "noise_eigenvalue_floor":floor}

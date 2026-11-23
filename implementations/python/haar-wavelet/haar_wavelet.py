"""Orthonormal 2-D Haar wavelet decomposition and reconstruction."""
from __future__ import annotations
import numpy as np

def haar2d(image, levels=1):
    a=np.asarray(image,dtype=float)
    if a.ndim!=2 or not np.all(np.isfinite(a)): raise ValueError("image must be finite and 2-D")
    if not isinstance(levels,(int,np.integer)) or levels<1: raise ValueError("levels must be a positive integer")
    approx=a.copy(); details=[]
    for _ in range(levels):
        h,w=approx.shape
        if h%2 or w%2: raise ValueError("each decomposition level requires even row and column dimensions")
        a00=approx[0::2,0::2]; a01=approx[0::2,1::2]
        a10=approx[1::2,0::2]; a11=approx[1::2,1::2]
        ll=(a00+a01+a10+a11)/2
        lh=(a00-a01+a10-a11)/2
        hl=(a00+a01-a10-a11)/2
        hh=(a00-a01-a10+a11)/2
        details.append((lh,hl,hh))
        approx=ll
    return {"approximation":approx,"details":details,"original_shape":a.shape}

def inverse_haar2d(coefficients):
    approx=np.asarray(coefficients["approximation"],dtype=float).copy()
    details=coefficients["details"]
    for lh,hl,hh in reversed(details):
        lh=np.asarray(lh); hl=np.asarray(hl); hh=np.asarray(hh)
        if lh.shape!=approx.shape or hl.shape!=approx.shape or hh.shape!=approx.shape:
            raise ValueError("detail coefficient shapes must match approximation")
        a00=(approx+lh+hl+hh)/2
        a01=(approx-lh+hl-hh)/2
        a10=(approx+lh-hl-hh)/2
        a11=(approx-lh-hl+hh)/2
        out=np.empty((approx.shape[0]*2,approx.shape[1]*2),dtype=float)
        out[0::2,0::2]=a00; out[0::2,1::2]=a01
        out[1::2,0::2]=a10; out[1::2,1::2]=a11
        approx=out
    if "original_shape" in coefficients and approx.shape!=tuple(coefficients["original_shape"]):
        raise ValueError("reconstructed shape differs from original_shape")
    return approx

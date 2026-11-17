"""Spectral Angle Mapper (SAM) and Spectral Information Divergence (SID)."""
from __future__ import annotations
import numpy as np

def spectral_angle(a,b,axis=-1,zero_policy="nan"):
    x=np.asarray(a,dtype=float); y=np.asarray(b,dtype=float)
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)): raise ValueError("spectra must be finite")
    if x.shape[-1]!=y.shape[-1]: raise ValueError("spectral band dimensions must match")
    dot=np.sum(x*y,axis=axis)
    nx=np.linalg.norm(x,axis=axis); ny=np.linalg.norm(y,axis=axis)
    denom=nx*ny
    if zero_policy not in ("nan","zero"): raise ValueError("zero_policy must be nan or zero")
    cos=np.divide(dot,denom,out=np.zeros_like(dot,dtype=float),where=denom>0)
    cos=np.clip(cos,-1,1)
    # Round-off can leave mathematically identical spectra a few ulps below 1.
    cos=np.where(np.abs(cos-1.0)<=1e-12,1.0,np.where(np.abs(cos+1.0)<=1e-12,-1.0,cos))
    angle=np.arccos(cos)
    return np.where(denom>0,angle,np.nan if zero_policy=="nan" else 0.0)

def spectral_information_divergence(a,b,axis=-1,epsilon=1e-12):
    x=np.asarray(a,dtype=float); y=np.asarray(b,dtype=float)
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)): raise ValueError("spectra must be finite")
    if x.shape[-1]!=y.shape[-1]: raise ValueError("spectral band dimensions must match")
    if np.any(x<0) or np.any(y<0): raise ValueError("SID requires nonnegative spectra")
    if epsilon<=0: raise ValueError("epsilon must be positive")
    px=x+epsilon; py=y+epsilon
    px=px/px.sum(axis=axis,keepdims=True); py=py/py.sum(axis=axis,keepdims=True)
    return np.sum(px*np.log(px/py)+py*np.log(py/px),axis=axis)

def spectral_angle_map(cube, reference, zero_policy="nan"):
    x=np.asarray(cube,dtype=float); r=np.asarray(reference,dtype=float)
    if x.ndim!=3 or r.shape!=(x.shape[-1],): raise ValueError("cube must be rows x cols x bands and reference one spectrum")
    return spectral_angle(x,r,axis=-1,zero_policy=zero_policy)

def sid_map(cube, reference, epsilon=1e-12):
    x=np.asarray(cube,dtype=float); r=np.asarray(reference,dtype=float)
    if x.ndim!=3 or r.shape!=(x.shape[-1],): raise ValueError("cube must be rows x cols x bands and reference one spectrum")
    return spectral_information_divergence(x,r,axis=-1,epsilon=epsilon)

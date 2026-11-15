"""Constrained Energy Minimisation (CEM) spectral detector."""
import numpy as np

def cem_detect(cube, target, background_mask=None, correlation=None, regularization=1e-6):
    x=np.asarray(cube,dtype=float); d=np.asarray(target,dtype=float)
    if x.ndim!=3 or d.shape!=(x.shape[-1],): raise ValueError("cube must be rows x cols x bands and target one spectrum")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(d)): raise ValueError("inputs must be finite")
    if not 0<=regularization<1: raise ValueError("regularization must be in [0,1)")
    mask=np.ones(x.shape[:2],bool) if background_mask is None else np.asarray(background_mask,dtype=bool)
    if mask.shape!=x.shape[:2] or mask.sum()<2: raise ValueError("mask must select at least two pixels")
    Y=x[mask]; R=Y.T@Y/Y.shape[0] if correlation is None else np.asarray(correlation,dtype=float)
    if R.shape!=(x.shape[-1],x.shape[-1]) or not np.all(np.isfinite(R)): raise ValueError("correlation matrix shape or values invalid")
    R=(R+R.T)/2; vals,vec=np.linalg.eigh(R); scale=max(float(np.max(np.abs(vals))),np.finfo(float).eps)
    if vals.min() < -scale*1e-8: raise ValueError("correlation matrix must be positive semidefinite")
    floor=max(scale*regularization,scale*1e-12)
    inv=vec@np.diag(1/np.maximum(vals,floor))@vec.T
    q=inv@d; denom=float(d@q)
    if denom<=floor: raise ValueError("target has no stable energy in correlation metric")
    weights=q/denom
    return {"scores":np.einsum("...i,i->...",x,weights),"weights":weights,
            "correlation":R,"constraint_response":float(d@weights),"eigenvalue_floor":floor}

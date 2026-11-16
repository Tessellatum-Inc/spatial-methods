"""Fully constrained least-squares spectral unmixing."""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize

def fcls_unmix(cube, endmembers, max_iter=500, tolerance=1e-9):
    """Estimate nonnegative abundances constrained to sum to one.

    cube: rows x columns x bands; endmembers: bands x endmembers.
    Returns abundance cube, reconstructed cube, residual RMSE per pixel,
    and optimizer success flags.
    """
    x=np.asarray(cube,dtype=float); E=np.asarray(endmembers,dtype=float)
    if x.ndim!=3 or E.ndim!=2 or x.shape[-1]!=E.shape[0]:
        raise ValueError("cube must be rows x cols x bands and endmembers bands x components")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(E)): raise ValueError("inputs must be finite")
    bands,k=E.shape
    if k<1: raise ValueError("at least one endmember is required")
    if max_iter<1 or tolerance<=0: raise ValueError("max_iter and tolerance must be positive")
    pixels=x.reshape(-1,bands); abund=np.empty((pixels.shape[0],k)); success=np.zeros(pixels.shape[0],bool)
    gram=E.T@E
    for i,y in enumerate(pixels):
        linear=E.T@y
        def objective(a): return .5*float(a@gram@a)-float(linear@a)
        def jac(a): return gram@a-linear
        initial=np.full(k,1/k)
        if k==1:
            abund[i]=1.; success[i]=True; continue
        result=minimize(objective,initial,jac=jac,method="SLSQP",
                        bounds=[(0.,1.)]*k,
                        constraints={"type":"eq","fun":lambda a: np.sum(a)-1.,
                                     "jac":lambda a: np.ones_like(a)},
                        options={"maxiter":max_iter,"ftol":tolerance,"disp":False})
        abund[i]=np.clip(result.x,0,1)
        total=abund[i].sum()
        if total>0: abund[i]/=total
        success[i]=bool(result.success and abs(abund[i].sum()-1)<1e-6 and np.min(abund[i])>=-1e-10)
    reconstruction=(abund@E.T).reshape(x.shape)
    residual=np.sqrt(np.mean((x-reconstruction)**2,axis=-1))
    return {"abundances":abund.reshape(x.shape[:2]+(k,)),
            "reconstruction":reconstruction,"rmse":residual,
            "success":success.reshape(x.shape[:2])}

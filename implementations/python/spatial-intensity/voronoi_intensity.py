"""Bounded-window Voronoi tessellation intensity estimator."""
from __future__ import annotations
import numpy as np


def _clip_half_plane(poly, normal, bound, tol):
    if len(poly)==0: return poly
    out=[]
    prev=poly[-1]; dp=bound-float(normal@prev)
    for curr in poly:
        dc=bound-float(normal@curr)
        pin=dp>=-tol; cin=dc>=-tol
        if pin != cin:
            denom=dp-dc
            if abs(denom)>np.finfo(float).eps:
                t=dp/denom
                out.append(prev+t*(curr-prev))
        if cin: out.append(curr)
        prev,dp=curr,dc
    return np.asarray(out,dtype=float).reshape((-1,2))


def _area(poly):
    if len(poly)<3: return 0.0
    x=poly[:,0]; y=poly[:,1]
    return abs(float(np.dot(x,np.roll(y,-1))-np.dot(y,np.roll(x,-1))))/2


def voronoi_intensity(points, window):
    """Partition an axis-aligned rectangular window into clipped Voronoi cells.

    Returns each cell polygon, its area and the piecewise-constant intensity
    estimate 1/area on that cell. Points must be unique and lie in the window.
    The dense half-plane clipping algorithm is intended for small point sets.
    """
    P=np.asarray(points,dtype=float); W=np.asarray(window,dtype=float)
    if P.ndim!=2 or P.shape[1]!=2 or P.shape[0]<1 or not np.all(np.isfinite(P)):
        raise ValueError("points must be a finite n by 2 array with n >= 1")
    if W.shape!=(4,) or not np.all(np.isfinite(W)):
        raise ValueError("window must be (xmin, ymin, xmax, ymax) with finite values")
    xmin,ymin,xmax,ymax=map(float,W)
    if xmax<=xmin or ymax<=ymin: raise ValueError("window must have positive width and height")
    if np.unique(P,axis=0).shape[0]!=P.shape[0]: raise ValueError("duplicate sites are not supported")
    if np.any(P[:,0]<xmin) or np.any(P[:,0]>xmax) or np.any(P[:,1]<ymin) or np.any(P[:,1]>ymax):
        raise ValueError("all sites must lie inside the study window")
    rect=np.array([[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]],dtype=float)
    scale=max(1.0,abs(xmin),abs(ymin),abs(xmax),abs(ymax))
    tol=100*np.finfo(float).eps*scale**2
    cells=[]; areas=[]
    for i,pi in enumerate(P):
        poly=rect.copy()
        for j,pj in enumerate(P):
            if i==j: continue
            normal=2*(pj-pi); bound=float(pj@pj-pi@pi)
            poly=_clip_half_plane(poly,normal,bound,tol)
            if len(poly)==0: break
        area=_area(poly)
        if area<=tol: raise ValueError("a Voronoi cell has zero or numerically negligible area")
        cells.append(poly); areas.append(area)
    areas=np.asarray(areas)
    window_area=(xmax-xmin)*(ymax-ymin)
    if not np.isclose(areas.sum(),window_area,rtol=1e-9,atol=1e-9*window_area):
        raise ArithmeticError("computed Voronoi cells do not partition the study window")
    return {"cells":cells,"areas":areas,"intensity":1/areas,
            "window_area":window_area,"n_sites":int(P.shape[0]),
            "estimator":"inverse clipped Voronoi cell area"}

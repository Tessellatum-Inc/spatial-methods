"""Translation-corrected space-time K estimator."""
from __future__ import annotations
import numpy as np

def space_time_k_function(points,times,radii,time_lags,*,window,time_window):
    xy=np.asarray(points,dtype=float);t=np.asarray(times,dtype=float)
    r=np.asarray(radii,dtype=float);tau=np.asarray(time_lags,dtype=float)
    if xy.ndim!=2 or xy.shape[1]!=2 or len(xy)<2 or not np.isfinite(xy).all():
        raise ValueError("points must be a finite N-by-2 array with N>=2")
    n=len(xy)
    if t.shape!=(n,) or not np.isfinite(t).all():raise ValueError("times must match points and be finite")
    if r.ndim!=1 or not len(r) or not np.isfinite(r).all() or np.any(r<0):raise ValueError("radii must be finite and nonnegative")
    if tau.ndim!=1 or not len(tau) or not np.isfinite(tau).all() or np.any(tau<0):raise ValueError("time_lags must be finite and nonnegative")
    if len(window)!=4 or len(time_window)!=2:raise ValueError("invalid spatial or temporal window")
    xmin,ymin,xmax,ymax=map(float,window);tmin,tmax=map(float,time_window)
    if not np.isfinite([xmin,ymin,xmax,ymax,tmin,tmax]).all() or xmax<=xmin or ymax<=ymin or tmax<=tmin:
        raise ValueError("windows must have positive finite extent")
    if np.any(xy[:,0]<xmin) or np.any(xy[:,0]>xmax) or np.any(xy[:,1]<ymin) or np.any(xy[:,1]>ymax):
        raise ValueError("points must lie inside spatial window")
    if np.any(t<tmin) or np.any(t>tmax):raise ValueError("times must lie inside time_window")
    area=(xmax-xmin)*(ymax-ymin);duration=tmax-tmin
    dists=[];lags=[];weights=[]
    for i in range(n):
        for j in range(i+1,n):
            dx=abs(float(xy[i,0]-xy[j,0]));dy=abs(float(xy[i,1]-xy[j,1]));dt=abs(float(t[i]-t[j]))
            ws=((xmax-xmin-dx)*(ymax-ymin-dy))/area
            wt=(duration-dt)/duration
            if ws<=0 or wt<=0:continue
            dists.append(float(np.hypot(dx,dy)));lags.append(dt);weights.append(1/(ws*wt))
    dists=np.asarray(dists);lags=np.asarray(lags);weights=np.asarray(weights)
    out=np.zeros((len(r),len(tau)));factor=2*area*duration/(n*(n-1))
    for i,rad in enumerate(r):
        for j,lag in enumerate(tau):
            out[i,j]=factor*float(weights[(dists<=rad)&(lags<=lag)].sum())
    if not np.isfinite(out).all():raise ValueError("space-time K estimate overflowed")
    return {"radii":r.copy(),"time_lags":tau.copy(),"K":out,"n_events":n,
            "spatial_area":area,"time_duration":duration,
            "edge_correction":"rectangular spatial and temporal translation"}

"""Standard line Hough transform for binary edge images."""
from __future__ import annotations
import numpy as np


def hough_lines(edges, theta=None, rho_resolution=1.0):
    e=np.asarray(edges)
    if e.ndim!=2: raise ValueError("edges must be 2-D")
    if not np.all(np.isfinite(e)): raise ValueError("edges must be finite")
    if not np.isfinite(rho_resolution) or rho_resolution<=0: raise ValueError("rho_resolution must be finite and positive")
    ys,xs=np.nonzero(e)
    theta=np.linspace(-np.pi/2,np.pi/2,180,endpoint=False) if theta is None else np.asarray(theta,dtype=float)
    if theta.ndim!=1 or theta.size==0 or not np.all(np.isfinite(theta)): raise ValueError("theta must be a nonempty finite vector")
    diag=np.hypot(e.shape[0]-1,e.shape[1]-1)
    rho_limit=np.ceil(diag/rho_resolution)*rho_resolution
    rhos=np.arange(-rho_limit,rho_limit+rho_resolution*0.5,rho_resolution)
    acc=np.zeros((rhos.size,theta.size),dtype=np.uint64)
    if xs.size:
        rho=xs[:,None]*np.cos(theta)[None,:]+ys[:,None]*np.sin(theta)[None,:]
        ri=np.rint((rho-rhos[0])/rho_resolution).astype(int)
        ri=np.clip(ri,0,rhos.size-1)
        ti=np.broadcast_to(np.arange(theta.size),ri.shape)
        np.add.at(acc,(ri.ravel(),ti.ravel()),1)
    return acc,rhos,theta


def hough_peaks(accumulator,rhos,theta,num_peaks=10,min_votes=1,nhood=(9,9)):
    a=np.asarray(accumulator)
    if a.ndim!=2 or a.shape!=(len(rhos),len(theta)): raise ValueError("accumulator shape mismatch")
    if num_peaks<1 or min_votes<1: raise ValueError("num_peaks and min_votes must be positive")
    nr,nt=nhood
    if nr<1 or nt<1 or nr%2==0 or nt%2==0: raise ValueError("nhood dimensions must be positive odd integers")
    work=a.copy();peaks=[];hr,hc=nr//2,nt//2
    for _ in range(num_peaks):
        flat=int(np.argmax(work));r,t=np.unravel_index(flat,work.shape);votes=int(work[r,t])
        if votes<min_votes: break
        peaks.append((float(rhos[r]),float(theta[t]),votes))
        work[max(0,r-hr):r+hr+1,max(0,t-hc):t+hc+1]=0
    return peaks

"""Binned two-dimensional Gaussian KDE accelerated by FFT convolution."""
from __future__ import annotations
import math
import numpy as np
from scipy.signal import fftconvolve


def fft_grid_kde(points, *, extent, shape=(128,128), bandwidth=1.0,
                 weights=None, boundary_correction=False, truncate=4.0):
    """Estimate a planar density on a regular grid using weighted binning + FFT.

    The returned density has inverse-square coordinate units and integrates
    approximately to one over the requested grid when boundary effects are
    negligible. Optional boundary correction divides by the fraction of the
    discrete kernel supported inside the grid.
    """
    p=np.asarray(points,dtype=float)
    if p.ndim!=2 or p.shape[1]!=2 or p.shape[0]==0 or not np.isfinite(p).all():
        raise ValueError("points must be a non-empty finite (n,2) array")
    if len(extent)!=4: raise ValueError("extent must be xmin,xmax,ymin,ymax")
    xmin,xmax,ymin,ymax=map(float,extent)
    if not np.isfinite([xmin,xmax,ymin,ymax]).all() or xmax<=xmin or ymax<=ymin:
        raise ValueError("extent bounds must be finite and increasing")
    if len(shape)!=2 or any(not isinstance(n,(int,np.integer)) or n<2 for n in shape):
        raise ValueError("shape must contain two integers >= 2")
    nx,ny=map(int,shape)
    if not math.isfinite(bandwidth) or bandwidth<=0: raise ValueError("bandwidth must be finite and positive")
    if not math.isfinite(truncate) or truncate<=0: raise ValueError("truncate must be finite and positive")
    if weights is None: w=np.ones(len(p),dtype=float)
    else:
        w=np.asarray(weights,dtype=float)
        if w.shape!=(len(p),) or not np.isfinite(w).all() or np.any(w<0):
            raise ValueError("weights must be a finite non-negative vector matching points")
    if w.sum()<=0: raise ValueError("weights must have positive total")
    inside=(p[:,0]>=xmin)&(p[:,0]<=xmax)&(p[:,1]>=ymin)&(p[:,1]<=ymax)
    if not inside.any() or w[inside].sum()<=0: raise ValueError("no positive-weight points fall inside extent")
    dx=(xmax-xmin)/nx;dy=(ymax-ymin)/ny
    counts,_,_=np.histogram2d(p[inside,0],p[inside,1],bins=(nx,ny),
                              range=((xmin,xmax),(ymin,ymax)),weights=w[inside])
    rx=max(1,int(math.ceil(truncate*bandwidth/dx)))
    ry=max(1,int(math.ceil(truncate*bandwidth/dy)))
    gx=np.arange(-rx,rx+1)*dx;gy=np.arange(-ry,ry+1)*dy
    xx,yy=np.meshgrid(gx,gy,indexing="ij")
    kernel=np.exp(-(xx*xx+yy*yy)/(2*bandwidth*bandwidth))
    kernel/=kernel.sum()
    smoothed=np.maximum(fftconvolve(counts,kernel,mode="same"),0.0)
    if boundary_correction:
        support=fftconvolve(np.ones_like(counts),kernel,mode="same")
        smoothed=np.divide(smoothed,support,out=np.zeros_like(smoothed),where=support>0)
    density=smoothed/(w[inside].sum()*dx*dy)
    x=xmin+(np.arange(nx)+.5)*dx
    y=ymin+(np.arange(ny)+.5)*dy
    return x,y,density

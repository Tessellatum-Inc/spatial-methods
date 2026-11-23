"""Discrete Radon transform by bilinear sampling along parallel lines."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import map_coordinates

def radon_transform(image, theta=None, rho_resolution=1.0, circle=False):
    """Return sinogram, rho coordinates and angles in degrees.

    Lines use x*cos(theta) + y*sin(theta) = rho, with origin at image centre.
    The integral is approximated by unit-spaced bilinear samples along each line.
    """
    a=np.asarray(image,dtype=float)
    if a.ndim!=2 or not np.all(np.isfinite(a)): raise ValueError("image must be finite and 2-D")
    if rho_resolution<=0: raise ValueError("rho_resolution must be positive")
    angles=np.arange(180,dtype=float) if theta is None else np.asarray(theta,dtype=float)
    if angles.ndim!=1 or angles.size==0 or not np.all(np.isfinite(angles)): raise ValueError("theta must be a nonempty finite vector")
    h,w=a.shape; cy=(h-1)/2; cx=(w-1)/2
    if circle:
        if h!=w: raise ValueError("circle=True requires a square image")
        radius=min(cx,cy)
        work=a.copy()
        yy,xx=np.indices(a.shape)
        work[(xx-cx)**2+(yy-cy)**2>radius**2]=0
    else: work=a
    diag=np.hypot(h-1,w-1)/2
    limit=diag if not circle else min(cx,cy)
    rho=np.arange(-limit,limit+rho_resolution*.5,rho_resolution)
    t=np.arange(-np.ceil(diag),np.ceil(diag)+1,1.0)
    sino=np.zeros((rho.size,angles.size),dtype=float)
    for j,deg in enumerate(angles):
        rad=np.deg2rad(deg); co=np.cos(rad); si=np.sin(rad)
        for i,r in enumerate(rho):
            # A point on the line plus its unit direction vector.
            x=cx+r*co-t*si; y=cy+r*si+t*co
            vals=map_coordinates(work,[y,x],order=1,mode="constant",cval=0.0,prefilter=False)
            sino[i,j]=vals.sum()
    return sino,rho,angles

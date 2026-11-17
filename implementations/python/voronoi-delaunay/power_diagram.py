"""Clipped weighted Voronoi (power) diagram by half-plane intersection."""
from __future__ import annotations
import numpy as np


def _clip_half_plane(polygon, normal, bound, tolerance):
    if not polygon:
        return []
    output=[]
    def value(point):
        return normal[0]*point[0]+normal[1]*point[1]-bound
    previous=polygon[-1];vp=value(previous);prev_in=vp<=tolerance
    for current in polygon:
        vc=value(current);cur_in=vc<=tolerance
        if prev_in and cur_in:
            output.append(current)
        elif prev_in and not cur_in:
            denominator=vp-vc
            if denominator!=0:
                t=vp/denominator
                output.append((previous[0]+t*(current[0]-previous[0]),
                               previous[1]+t*(current[1]-previous[1])))
        elif not prev_in and cur_in:
            denominator=vp-vc
            if denominator!=0:
                t=vp/denominator
                output.append((previous[0]+t*(current[0]-previous[0]),
                               previous[1]+t*(current[1]-previous[1])))
            output.append(current)
        previous,vp,prev_in=current,vc,cur_in
    return output


def polygon_area(vertices):
    if len(vertices)<3:return 0.0
    return abs(sum(vertices[i][0]*vertices[(i+1)%len(vertices)][1]
                   -vertices[(i+1)%len(vertices)][0]*vertices[i][1]
                   for i in range(len(vertices))))/2.0


def power_diagram(sites, *, weights=None, bounds):
    """Return one clipped power cell per site as lists of (x,y) vertices.

    Cell i contains points minimizing ||x-site_i||^2 - weights[i].
    Cells are clipped to the closed rectangle (xmin,ymin,xmax,ymax).
    """
    xy=np.asarray(sites,dtype=float)
    if xy.ndim!=2 or xy.shape[1]!=2 or len(xy)<1 or not np.isfinite(xy).all():
        raise ValueError("sites must be a finite nonempty N-by-2 array")
    if len(np.unique(xy,axis=0))!=len(xy):
        raise ValueError("site coordinates must be unique")
    if weights is None:w=np.zeros(len(xy),dtype=float)
    else:
        w=np.asarray(weights,dtype=float)
        if w.shape!=(len(xy),) or not np.isfinite(w).all():
            raise ValueError("weights must be a finite vector matching sites")
    b=np.asarray(bounds,dtype=float)
    if b.shape!=(4,) or not np.isfinite(b).all() or b[2]<=b[0] or b[3]<=b[1]:
        raise ValueError("bounds must be a finite positive-area rectangle")
    xmin,ymin,xmax,ymax=map(float,b)
    rectangle=[(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)]
    scale=max(1.0,float(np.max(np.abs(xy))),float(np.max(np.abs(b))))
    cells=[]
    for i,site in enumerate(xy):
        cell=list(rectangle)
        for j,other in enumerate(xy):
            if i==j or not cell:continue
            normal=2.0*(other-site)
            bound=float(other@other-w[j]-site@site+w[i])
            tol=1e-12*max(scale*float(np.linalg.norm(normal)),abs(bound),1.0)
            cell=_clip_half_plane(cell,normal,bound,tol)
        # Remove adjacent near-duplicate vertices created at coincident corners.
        cleaned=[]
        for point in cell:
            if not cleaned or np.hypot(point[0]-cleaned[-1][0],point[1]-cleaned[-1][1])>1e-12*scale:
                cleaned.append((float(point[0]),float(point[1])))
        if len(cleaned)>1 and np.hypot(cleaned[0][0]-cleaned[-1][0],cleaned[0][1]-cleaned[-1][1])<=1e-12*scale:
            cleaned.pop()
        cells.append(cleaned if polygon_area(cleaned)>1e-14*scale*scale else [])
    return cells

"""D-infinity and multiple-flow-direction routing for gridded elevation models."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from math import atan2, hypot, pi
import numpy as np

_NEIGHBOURS=((0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1))

@dataclass(frozen=True)
class RoutingResult:
    receiver_rows: np.ndarray
    receiver_cols: np.ndarray
    proportions: np.ndarray
    direction: np.ndarray
    slope: np.ndarray

def _validate_dem(dem,cellsize):
    z=np.asarray(dem,dtype=float)
    if z.ndim!=2 or not z.size: raise ValueError("dem must be a non-empty 2D array")
    dx,dy=map(float,cellsize)
    if not np.isfinite((dx,dy)).all() or dx<=0 or dy<=0:
        raise ValueError("cellsize must contain positive finite (x, y) spacing")
    return z,dx,dy

def _dinf_cell(z,r,c,dx,dy,valid):
    z0=z[r,c]; neighbours=[]
    for dr,dc in _NEIGHBOURS:
        rr,cc=r+dr,c+dc
        if 0<=rr<z.shape[0] and 0<=cc<z.shape[1] and valid[rr,cc]:
            neighbours.append((dr,dc,dc*dx,-dr*dy,z[rr,cc]-z0))
        else: neighbours.append(None)
    best=None; tau=2*pi
    for i in range(8):
        a,b=neighbours[i],neighbours[(i+1)%8]
        if a is None or b is None: continue
        _,_,x1,y1,dz1=a; _,_,x2,y2,dz2=b
        det=x1*y2-x2*y1
        if det==0: continue
        gx=(dz1*y2-dz2*y1)/det; gy=(x1*dz2-x2*dz1)/det
        mag=hypot(gx,gy)
        if mag<=0: continue
        angle=atan2(-gy,-gx)%tau
        a1=atan2(y1,x1)%tau; a2=atan2(y2,x2)%tau
        delta=(angle-a1)%tau; width=(a2-a1)%tau
        if delta<=width+1e-12:
            f=min(1.0,max(0.0,delta/width)) if width else 0.0
            candidate=(mag,angle,(a,b),(1-f,f))
        else:
            edges=[]
            for item in (a,b):
                dr,dc,x,y,dz=item; drop=-dz
                if drop>0: edges.append((drop/hypot(x,y),atan2(y,x)%tau,item))
            if not edges: continue
            slope,ang,item=max(edges,key=lambda q:q[0])
            candidate=(slope,ang,(item,None),(1.0,0.0))
        if best is None or candidate[0]>best[0]: best=candidate
    # A valid descending edge remains usable even if its adjacent facet has NoData.
    for item in neighbours:
        if item is None: continue
        dr,dc,x,y,dz=item; drop=-dz
        if drop<=0: continue
        slope=drop/hypot(x,y)
        if best is None or slope>best[0]:
            best=(slope,atan2(y,x)%tau,(item,None),(1.0,0.0))
    if best is None: return None
    slope,angle,items,weights=best
    chosen=[(it,w) for it,w in zip(items,weights) if it is not None and w>1e-14]
    total=sum(w for _,w in chosen)
    return (slope,angle,[(it[0],it[1],w/total) for it,w in chosen]) if total else None

def route_d_infinity(dem,*,cellsize=(1.0,1.0),nodata=None):
    """Facet-based D-infinity receivers; angle is radians CCW from east."""
    z,dx,dy=_validate_dem(dem,cellsize); valid=np.isfinite(z)
    if nodata is not None: valid &= z!=float(nodata)
    rows,cols=z.shape
    rr=np.full((rows,cols,2),-1,dtype=int); cc=rr.copy()
    w=np.zeros((rows,cols,2)); direction=np.full(z.shape,np.nan); slope=np.zeros(z.shape)
    for r,c in zip(*np.where(valid)):
        result=_dinf_cell(z,int(r),int(c),dx,dy,valid)
        if result is None: continue
        slope[r,c],direction[r,c],receivers=result
        for k,(dr,dc,weight) in enumerate(receivers[:2]):
            rr[r,c,k]=r+dr; cc[r,c,k]=c+dc; w[r,c,k]=weight
    return RoutingResult(rr,cc,w,direction,slope)

def route_multiple_flow_direction(dem,*,cellsize=(1.0,1.0),exponent=1.1,nodata=None):
    """Route to all lower neighbours using normalised slope**exponent weights."""
    z,dx,dy=_validate_dem(dem,cellsize); power=float(exponent)
    if not np.isfinite(power) or power<=0: raise ValueError("exponent must be positive and finite")
    valid=np.isfinite(z)
    if nodata is not None: valid &= z!=float(nodata)
    rows,cols=z.shape
    rr=np.full((rows,cols,8),-1,dtype=int); cc=rr.copy()
    w=np.zeros((rows,cols,8)); direction=np.full(z.shape,np.nan); slope=np.zeros(z.shape)
    for r,c in zip(*np.where(valid)):
        candidates=[]
        for dr,dc in _NEIGHBOURS:
            nr,nc=int(r+dr),int(c+dc)
            if 0<=nr<rows and 0<=nc<cols and valid[nr,nc]:
                drop=z[r,c]-z[nr,nc]
                if drop>0:
                    distance=hypot(dc*dx,dr*dy); grad=drop/distance
                    candidates.append((dr,dc,grad**power,grad))
        total=sum(q[2] for q in candidates)
        if total<=0: continue
        slope[r,c]=max(q[3] for q in candidates)
        vx=vy=0.0
        for k,(dr,dc,raw,grad) in enumerate(candidates):
            weight=raw/total; rr[r,c,k]=r+dr; cc[r,c,k]=c+dc; w[r,c,k]=weight
            distance=hypot(dc*dx,dr*dy); vx+=weight*dc*dx/distance; vy+=weight*(-dr)*dy/distance
        if vx or vy: direction[r,c]=atan2(vy,vx)%(2*pi)
    return RoutingResult(rr,cc,w,direction,slope)

def flow_accumulation(routing,*,valid_mask=None):
    """Topologically accumulate unit source contributions; reject cycles."""
    rr,cc,w=routing.receiver_rows,routing.receiver_cols,routing.proportions
    if rr.shape!=cc.shape or rr.shape!=w.shape or rr.ndim!=3:
        raise ValueError("receiver arrays and proportions must have matching 3D shapes")
    rows,cols,slots=rr.shape
    valid=np.ones((rows,cols),dtype=bool) if valid_mask is None else np.asarray(valid_mask,dtype=bool)
    if valid.shape!=(rows,cols): raise ValueError("valid_mask must match the routing grid")
    indegree=np.zeros((rows,cols),dtype=int)
    for r in range(rows):
        for c in range(cols):
            if not valid[r,c]: continue
            for k in range(slots):
                nr,nc,weight=int(rr[r,c,k]),int(cc[r,c,k]),float(w[r,c,k])
                if not np.isfinite(weight) or weight<0: raise ValueError("flow proportions must be finite and non-negative")
                if weight==0: continue
                if not(0<=nr<rows and 0<=nc<cols and valid[nr,nc]):
                    raise ValueError("positive flow weights require valid in-grid receivers")
                indegree[nr,nc]+=1
    queue=deque((int(r),int(c)) for r,c in zip(*np.where(valid&(indegree==0))))
    acc=np.full((rows,cols),np.nan); acc[valid]=1.0; processed=0
    while queue:
        r,c=queue.popleft(); processed+=1
        for k in range(slots):
            nr,nc,weight=int(rr[r,c,k]),int(cc[r,c,k]),float(w[r,c,k])
            if weight<=0: continue
            acc[nr,nc]+=acc[r,c]*weight; indegree[nr,nc]-=1
            if indegree[nr,nc]==0: queue.append((nr,nc))
    if processed!=int(valid.sum()): raise ValueError("receiver graph contains a cycle")
    return acc

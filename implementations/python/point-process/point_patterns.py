"""Planar point-pattern summaries for rectangular observation windows."""
from __future__ import annotations
from math import hypot, isfinite, pi

def _validate(points, window):
    pts=[(float(p[0]),float(p[1])) for p in points]
    if len(pts)<2 or any(not isfinite(x) or not isfinite(y) for x,y in pts):
        raise ValueError("at least two finite points are required")
    if len(window)!=4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin,ymin,xmax,ymax=map(float,window)
    if not all(map(isfinite,(xmin,ymin,xmax,ymax))) or xmax<=xmin or ymax<=ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    if any(x<xmin or x>xmax or y<ymin or y>ymax for x,y in pts):
        raise ValueError("all points must lie within the observation window")
    if len(set(pts))!=len(pts):
        raise ValueError("duplicate point coordinates are not supported")
    return pts,(xmin,ymin,xmax,ymax)

def nearest_neighbor_distances(points):
    """Distance from each point to its closest other point."""
    if len(points)<2:
        raise ValueError("at least two points are required")
    pts=[(float(p[0]),float(p[1])) for p in points]
    if any(not isfinite(x) or not isfinite(y) for x,y in pts):
        raise ValueError("coordinates must be finite")
    if len(set(pts))!=len(pts):
        raise ValueError("duplicate point coordinates are not supported")
    return [min(hypot(x-a,y-b) for j,(a,b) in enumerate(pts) if j!=i)
            for i,(x,y) in enumerate(pts)]

def nearest_neighbor_cdf(points, radii):
    """Empirical nearest-neighbor distance CDF evaluated at requested radii."""
    distances=nearest_neighbor_distances(points)
    rs=[float(r) for r in radii]
    if any(not isfinite(r) or r<0 for r in rs):
        raise ValueError("radii must be finite and non-negative")
    return [sum(d<=r for d in distances)/len(distances) for r in rs]

def ripley_k_translation(points, window, radii):
    """Homogeneous Ripley K with rectangular translation edge correction.

    The translation weight is the inverse fraction of window overlap after
    shifting by each ordered pair displacement. Assumes stationarity and
    isotropy; output units are squared coordinate units.
    """
    pts,(xmin,ymin,xmax,ymax)=_validate(points,window)
    rs=[float(r) for r in radii]
    if not rs or any(not isfinite(r) or r<0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    width,height=xmax-xmin,ymax-ymin
    area=width*height;n=len(pts)
    pairs=[]
    for i,(x,y) in enumerate(pts):
        for j,(a,b) in enumerate(pts):
            if i==j: continue
            dx,dy=abs(x-a),abs(y-b)
            overlap=((width-dx)/width)*((height-dy)/height)
            if overlap>0:
                pairs.append((hypot(dx,dy),1.0/overlap))
    result=[]
    for radius in rs:
        total=sum(weight for distance,weight in pairs if distance<=radius)
        result.append(area*total/(n*(n-1)))
    return result

def pair_correlation_from_k(radii, k_values):
    """Finite-difference g(r)=K'(r)/(2*pi*r) on strictly increasing radii."""
    rs=[float(r) for r in radii]; ks=[float(k) for k in k_values]
    if len(rs)!=len(ks) or len(rs)<3:
        raise ValueError("at least three matching radii and K values are required")
    if any(not isfinite(r) or r<=0 for r in rs) or any(rs[i]>=rs[i+1] for i in range(len(rs)-1)):
        raise ValueError("radii must be finite, positive and strictly increasing")
    if any(not isfinite(k) for k in ks):
        raise ValueError("K values must be finite")
    out=[]
    for i,r in enumerate(rs):
        lo=max(0,i-1);hi=min(len(rs)-1,i+1)
        derivative=(ks[hi]-ks[lo])/(rs[hi]-rs[lo])
        out.append(derivative/(2*pi*r))
    return out

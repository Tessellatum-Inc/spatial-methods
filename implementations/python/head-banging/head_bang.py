"""Weighted two-dimensional head-banging smoother."""
from __future__ import annotations
from itertools import combinations
from math import acos, cos, degrees, fsum, hypot, isfinite, radians
from numbers import Integral

def _weighted_median(values, weights):
    pairs=sorted((float(v),float(w)) for v,w in zip(values,weights) if w>0)
    if not pairs: raise ValueError("weighted median requires positive total weight")
    total=fsum(w for _,w in pairs); half=total/2; cumulative=0.0
    for i,(value,weight) in enumerate(pairs):
        cumulative+=weight
        if cumulative>half+1e-12*total: return value
        if abs(cumulative-half)<=1e-12*total:
            return (value+pairs[i+1][0])/2 if i+1<len(pairs) else value
    return pairs[-1][0]

def _validate(points,values,weights):
    try:
        raw=list(points)
        if any(len(p)!=2 for p in raw): raise ValueError("each point must have two coordinates")
        pts=[(float(p[0]),float(p[1])) for p in raw]
        vals=[float(v) for v in values]
        w=[1.0]*len(vals) if weights is None else [float(v) for v in weights]
    except (TypeError,ValueError,IndexError) as exc:
        raise ValueError("points, values and weights must be numeric sequences") from exc
    if not pts or len(pts)!=len(vals) or len(w)!=len(vals):
        raise ValueError("non-empty points, values and weights must have equal length")
    if any(not isfinite(x) or not isfinite(y) for x,y in pts): raise ValueError("coordinates must be finite")
    if any(not isfinite(v) for v in vals): raise ValueError("values must be finite")
    if any(not isfinite(v) or v<=0 for v in w): raise ValueError("weights must be finite and strictly positive")
    if len(set(pts))!=len(pts): raise ValueError("point coordinates must be unique")
    return pts,vals,w

def head_bang(points,values,weights=None,*,n_neighbors=30,max_triples=None,
              max_deviation_degrees=45.0,max_iterations=10,tolerance=1e-12):
    """Smooth values using nearest-neighbour, nearly-collinear triples and weighted medians.

    Geometry/triple membership is fixed; updates are synchronous. Locations
    without qualifying triples remain unchanged as a conservative boundary rule.
    """
    pts,original,w=_validate(points,values,weights); n=len(pts)
    if isinstance(n_neighbors,bool) or not isinstance(n_neighbors,Integral) or n_neighbors<2:
        raise ValueError("n_neighbors must be an integer >= 2")
    if isinstance(max_iterations,bool) or not isinstance(max_iterations,Integral) or max_iterations<1:
        raise ValueError("max_iterations must be a positive integer")
    if isinstance(max_deviation_degrees,bool): raise ValueError("angular deviation must be in [0,90]")
    try: phi=float(max_deviation_degrees)
    except (TypeError,ValueError) as exc: raise ValueError("angular deviation must be in [0,90]") from exc
    if not isfinite(phi) or not 0<=phi<=90: raise ValueError("angular deviation must be in [0,90]")
    if isinstance(tolerance,bool): raise ValueError("tolerance must be finite and nonnegative")
    try: tol=float(tolerance)
    except (TypeError,ValueError) as exc: raise ValueError("tolerance must be finite and nonnegative") from exc
    if not isfinite(tol) or tol<0: raise ValueError("tolerance must be finite and nonnegative")
    if max_triples is not None and (isinstance(max_triples,bool) or not isinstance(max_triples,Integral) or max_triples<1):
        raise ValueError("max_triples must be a positive integer or None")
    k=min(int(n_neighbors),n-1); neighbors_by_point=[]; triples_by_point=[]
    threshold=cos(radians(180-phi))
    for i,(xi,yi) in enumerate(pts):
        candidates=sorted(((hypot(x-xi,y-yi),j) for j,(x,y) in enumerate(pts) if j!=i),key=lambda t:(t[0],t[1]))[:k]
        neighbors=[j for _,j in candidates]; neighbors_by_point.append(neighbors)
        eligible=[]
        for j,ell in combinations(neighbors,2):
            v1=(pts[j][0]-xi,pts[j][1]-yi); v2=(pts[ell][0]-xi,pts[ell][1]-yi)
            norm=hypot(*v1)*hypot(*v2)
            cosine=(v1[0]*v2[0]+v1[1]*v2[1])/norm
            if cosine<=threshold+1e-15:
                deviation=abs(180-degrees(acos(max(-1.0,min(1.0,cosine)))))
                eligible.append((deviation,j,ell))
        eligible.sort()
        limit=int(max_triples) if max_triples is not None else max(1,(2*k)//3)
        triples_by_point.append([(j,ell) for _,j,ell in eligible[:limit]])
    current=list(original); converged=False; iterations=0
    for iteration in range(1,int(max_iterations)+1):
        updated=list(current)
        for i,pairs in enumerate(triples_by_point):
            if not pairs: continue
            low_values=[];low_weights=[];high_values=[];high_weights=[]
            for j,ell in pairs:
                lo,hi=(j,ell) if current[j]<=current[ell] else (ell,j)
                low_values.append(current[lo]);low_weights.append(w[lo])
                high_values.append(current[hi]);high_weights.append(w[hi])
            low=_weighted_median(low_values,low_weights); high=_weighted_median(high_values,high_weights)
            updated[i]=_weighted_median([low,current[i],high],
                [fsum(low_weights),len(pairs)*w[i],fsum(high_weights)])
        change=max(abs(a-b) for a,b in zip(updated,current))
        current=updated;iterations=iteration
        if change<=tol: converged=True;break
    return {"smoothed_values":current,"iterations":iterations,"converged":converged,
            "neighbors":neighbors_by_point,"triples":triples_by_point}

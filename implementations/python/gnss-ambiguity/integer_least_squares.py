"""Exact bounded-dimension integer least-squares search (educational baseline)."""
from __future__ import annotations
from math import floor, isfinite, sqrt

def _cholesky(matrix):
    n=len(matrix); lower=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            value=matrix[i][j]-sum(lower[i][k]*lower[j][k] for k in range(j))
            if i==j:
                if value<=1e-14: raise ValueError("covariance must be positive definite")
                lower[i][j]=sqrt(value)
            else:
                lower[i][j]=value/lower[j][j]
    return lower

def integer_least_squares(float_ambiguities, covariance):
    """Return the two best integer vectors for min (a-z)' Q^-1 (a-z).

    A Cholesky-ordered sphere enumeration is used without LAMBDA decorrelation.
    This is exact for the supplied positive-definite covariance, but can be
    very slow for correlated/high-dimensional ambiguities.
    """
    a=[float(x) for x in float_ambiguities]; n=len(a)
    if n==0 or any(not isfinite(x) for x in a):
        raise ValueError("float ambiguities must be a non-empty finite vector")
    q=[list(map(float,row)) for row in covariance]
    if len(q)!=n or any(len(row)!=n for row in q):
        raise ValueError("covariance must be square and match ambiguity dimension")
    if any(not isfinite(v) for row in q for v in row):
        raise ValueError("covariance entries must be finite")
    for i in range(n):
        for j in range(n):
            if abs(q[i][j]-q[j][i])>1e-10:
                raise ValueError("covariance must be symmetric")
    L=_cholesky(q)

    def objective(z):
        y=[]
        for i in range(n):
            y.append((a[i]-z[i]-sum(L[i][j]*y[j] for j in range(i)))/L[i][i])
        return sum(v*v for v in y)

    base=[floor(x+0.5) for x in a]
    seeds=[base[:]]
    for i in range(n):
        for step in (-1,1):
            z=base[:];z[i]+=step;seeds.append(z)
    candidates={}
    for z in seeds: candidates[tuple(z)]=objective(z)
    best=sorted(candidates.items(),key=lambda item:item[1])[:2]
    if len(best)<2: raise RuntimeError("could not initialize two candidates")
    radius=best[1][1]
    z=[0]*n; y=[0.0]*n

    def visit(i, partial):
        nonlocal best, radius
        if i==n:
            key=tuple(z); score=partial
            if key not in candidates or score<candidates[key]:
                candidates[key]=score
                best=sorted(candidates.items(),key=lambda item:item[1])[:2]
                if len(best)==2: radius=best[1][1]
            return
        center=a[i]-sum(L[i][j]*y[j] for j in range(i))
        center/=L[i][i]
        reach=sqrt(max(0.0,radius-partial))*L[i][i]
        low=floor(center-reach)-1; high=floor(center+reach)+1
        values=sorted(range(low,high+1),key=lambda v:abs(v-center))
        for value in values:
            yi=(a[i]-value-sum(L[i][j]*y[j] for j in range(i)))/L[i][i]
            score=partial+yi*yi
            if score<=radius+1e-12:
                z[i]=value;y[i]=yi
                visit(i+1,score)

    visit(0,0.0)
    best=sorted(best,key=lambda item:item[1])
    return {"best":list(best[0][0]),"best_objective":best[0][1],
            "second_best":list(best[1][0]),"second_best_objective":best[1][1],
            "ratio":best[1][1]/max(best[0][1],1e-15)}

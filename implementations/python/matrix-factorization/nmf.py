"""Non-negative matrix factorization with Euclidean multiplicative updates."""
from __future__ import annotations
from math import isfinite, sqrt

def _matrix(values):
    matrix=[list(map(float,row)) for row in values]
    if not matrix or not matrix[0] or any(len(row)!=len(matrix[0]) for row in matrix):
        raise ValueError("V must be a non-empty rectangular matrix")
    if any(not isfinite(v) or v<0 for row in matrix for v in row):
        raise ValueError("V must contain finite non-negative values")
    return matrix

def _objective(v,w,h):
    m,n=len(v),len(v[0]);k=len(h)
    return sum((v[i][j]-sum(w[i][a]*h[a][j] for a in range(k)))**2
               for i in range(m) for j in range(n))

def nmf_euclidean(values, rank, *, max_iter=300, tolerance=1e-6, epsilon=1e-12):
    """Factor V≈WH using Lee–Seung Euclidean multiplicative updates.

    Deterministic positive initialization makes the teaching examples
    reproducible. Returns W, H and the Frobenius reconstruction-error history.
    Alternating optimization is non-convex jointly and converges only to a
    stationary/local solution; initialization and rank matter.
    """
    v=_matrix(values);m,n=len(v),len(v[0])
    if isinstance(rank,bool) or not isinstance(rank,int) or rank<1 or rank>min(m,n):
        raise ValueError("rank must be an integer between 1 and min(V.shape)")
    if isinstance(max_iter,bool) or not isinstance(max_iter,int) or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    if not isfinite(float(tolerance)) or tolerance<0:
        raise ValueError("tolerance must be finite and non-negative")
    if not isfinite(float(epsilon)) or epsilon<=0:
        raise ValueError("epsilon must be finite and positive")
    w=[[1.0+(((i+1)*(a+2))%11)/11 for a in range(rank)] for i in range(m)]
    h=[[1.0+(((a+3)*(j+1))%13)/13 for j in range(n)] for a in range(rank)]
    history=[sqrt(_objective(v,w,h))]
    for _ in range(max_iter):
        # H <- H * (W^T V) / (W^T W H)
        wt_v=[[sum(w[i][a]*v[i][j] for i in range(m)) for j in range(n)] for a in range(rank)]
        wt_w=[[sum(w[i][a]*w[i][b] for i in range(m)) for b in range(rank)] for a in range(rank)]
        for a in range(rank):
            for j in range(n):
                denominator=sum(wt_w[a][b]*h[b][j] for b in range(rank))
                h[a][j] *= wt_v[a][j]/max(denominator,epsilon)
        # W <- W * (V H^T) / (W H H^T)
        v_ht=[[sum(v[i][j]*h[a][j] for j in range(n)) for a in range(rank)] for i in range(m)]
        h_ht=[[sum(h[a][j]*h[b][j] for j in range(n)) for b in range(rank)] for a in range(rank)]
        for i in range(m):
            for a in range(rank):
                denominator=sum(w[i][b]*h_ht[b][a] for b in range(rank))
                w[i][a] *= v_ht[i][a]/max(denominator,epsilon)
        # Fix scale indeterminacy by normalizing each W column and rescaling H.
        for a in range(rank):
            norm=sum(w[i][a] for i in range(m))
            if norm>epsilon:
                for i in range(m): w[i][a]/=norm
                for j in range(n): h[a][j]*=norm
        error=sqrt(_objective(v,w,h))
        history.append(error)
        if abs(history[-2]-error)<=tolerance*max(1.0,history[-2]):
            break
    return {"W":w,"H":h,"errors":history}

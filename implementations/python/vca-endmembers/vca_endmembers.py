"""Vertex Component Analysis (VCA) endmember extraction."""
from __future__ import annotations
import numpy as np

def vca(data, n_endmembers, seed=0, mask=None, regularization=1e-10):
    """Extract endmembers from rows x columns x bands data using VCA.

    Returns spectra (bands x endmembers), selected flattened pixel indices,
    and the affine/linear projection metadata. This is a reproducible VCA
    baseline; stochastic directions are controlled by seed.
    """
    x=np.asarray(data,dtype=float)
    if x.ndim!=3 or not np.all(np.isfinite(x)): raise ValueError("data must be finite rows x cols x bands")
    rows,cols,bands=x.shape
    if not isinstance(n_endmembers,(int,np.integer)) or not 1<=n_endmembers<=bands:
        raise ValueError("n_endmembers must be between 1 and band count")
    valid=np.ones((rows,cols),bool) if mask is None else np.asarray(mask,dtype=bool)
    if valid.shape!=(rows,cols) or valid.sum()<n_endmembers: raise ValueError("mask must select at least n_endmembers pixels")
    Y=x[valid].T
    mean=Y.mean(axis=1,keepdims=True)
    Yc=Y-mean
    # Signal subspace from the leading left singular vectors.
    U,s,_=np.linalg.svd(Yc,full_matrices=False)
    p=n_endmembers
    if p==1:
        idx=np.array([int(np.argmax(np.linalg.norm(Yc,axis=0)))])
        return {"endmembers":Y[:,idx],"pixel_indices":np.flatnonzero(valid)[idx],
                "mean":mean[:,0],"subspace":U[:,:1],"seed":seed}
    P=U[:,:p]
    projected=P.T@Y
    rng=np.random.default_rng(seed)
    chosen=[]
    # VCA affine projection embeds the p-1 dimensional affine simplex in p dimensions.
    for _ in range(p):
        direction=rng.normal(size=p)
        if chosen:
            basis=projected[:,chosen]
            q,_=np.linalg.qr(basis)
            direction=direction-q@(q.T@direction)
        norm=np.linalg.norm(direction)
        if norm<regularization:
            direction=rng.normal(size=p); norm=np.linalg.norm(direction)
        direction/=norm
        scores=direction@projected
        scores[chosen]=-np.inf
        chosen.append(int(np.argmax(scores)))
    local=np.asarray(chosen,dtype=int)
    flat=np.flatnonzero(valid)[local]
    return {"endmembers":Y[:,local],"pixel_indices":flat,"mean":mean[:,0],
            "subspace":P,"seed":seed}

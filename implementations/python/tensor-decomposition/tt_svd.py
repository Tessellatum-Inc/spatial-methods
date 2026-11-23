"""Tensor-train decomposition and simple data-consistent completion."""
from __future__ import annotations
import numpy as np

def _validate_tensor(tensor):
    x=np.asarray(tensor,dtype=float)
    if x.ndim<2 or any(d<1 for d in x.shape) or not np.all(np.isfinite(x)):
        raise ValueError("tensor must be finite, nonempty and have order >= 2")
    return x

def _rank_from_singular_values(s, tolerance, norm, max_rank):
    if max_rank is not None:
        if isinstance(max_rank,bool) or int(max_rank)!=max_rank or max_rank<1:
            raise ValueError("max_rank must be a positive integer")
        cap=int(max_rank)
    else:
        cap=len(s)
    if tolerance is None or tolerance==0:
        rank=len(s)
    else:
        if not np.isfinite(tolerance) or tolerance<0:
            raise ValueError("tolerance must be finite and nonnegative")
        tail=np.sqrt(np.cumsum((s[::-1]**2)))[::-1]
        threshold=float(tolerance)*norm
        candidates=np.flatnonzero(tail<=threshold)
        rank=int(candidates[0]) if len(candidates) else len(s)
        rank=max(1,rank)
    return max(1,min(rank,cap,len(s)))

def tt_svd(tensor, max_rank=None, tolerance=0.0):
    """Approximate a dense tensor by TT-SVD.

    max_rank caps every internal TT rank. tolerance is a relative Frobenius
    truncation budget distributed across the N-1 SVD splits; the classical
    quasi-optimal bound applies to the exact-arithmetic TT-SVD truncation,
    subject to rank caps. Returns cores shaped (r[k], n[k], r[k+1]).
    """
    x=_validate_tensor(tensor)
    if max_rank is not None and (isinstance(max_rank,bool) or int(max_rank)!=max_rank or max_rank<1):
        raise ValueError("max_rank must be a positive integer")
    if not np.isfinite(tolerance) or tolerance<0:
        raise ValueError("tolerance must be finite and nonnegative")
    norm=float(np.linalg.norm(x))
    if norm==0:
        cores=[]
        for n in x.shape:
            cores.append(np.zeros((1,n,1)))
        return {"cores":cores,"ranks":[1]*(x.ndim+1),"shape":x.shape,
                "relative_error":0.0,"frobenius_error":0.0}
    remainder=x.copy()
    r_prev=1
    cores=[]
    local_tol=float(tolerance)/np.sqrt(max(1,x.ndim-1))
    for mode,n in enumerate(x.shape[:-1]):
        matrix=remainder.reshape(r_prev*n,-1)
        u,s,vt=np.linalg.svd(matrix,full_matrices=False)
        rank=_rank_from_singular_values(s,local_tol,norm,max_rank)
        cores.append(u[:,:rank].reshape(r_prev,n,rank))
        remainder=(s[:rank,None]*vt[:rank,:])
        r_prev=rank
    cores.append(remainder.reshape(r_prev,x.shape[-1],1))
    reconstructed=tt_reconstruct(cores)
    err=float(np.linalg.norm(x-reconstructed))
    return {"cores":cores,"ranks":[int(g.shape[0]) for g in cores]+[1],
            "shape":x.shape,"relative_error":err/norm,"frobenius_error":err}

def tt_reconstruct(cores):
    """Reconstruct a dense tensor from TT cores."""
    if not isinstance(cores,(list,tuple)) or len(cores)<2:
        raise ValueError("cores must contain at least two TT cores")
    checked=[]
    for i,core in enumerate(cores):
        g=np.asarray(core,dtype=float)
        if g.ndim!=3 or any(d<1 for d in g.shape) or not np.all(np.isfinite(g)):
            raise ValueError("each core must be a finite nonempty 3D array")
        if i==0 and g.shape[0]!=1: raise ValueError("first TT rank must be one")
        if i and checked[-1].shape[2]!=g.shape[0]: raise ValueError("adjacent TT ranks do not match")
        checked.append(g)
    if checked[-1].shape[2]!=1: raise ValueError("last TT rank must be one")
    result=checked[0][0,:,:]
    for g in checked[1:]:
        result=np.tensordot(result,g,axes=([-1],[0]))
    return np.squeeze(result,axis=-1)

def tt_complete(observations, observed_mask, max_rank, max_iter=100,
                tolerance=1e-6, initialization="mean"):
    """Heuristic TT-SVD projection completion with exact observed-data fidelity.

    Missing entries are initialized to zero or the observed mean. Each
    iteration projects the filled tensor onto a rank-capped TT-SVD model and
    restores observed entries. This is alternating projection, not a global
    optimizer; results depend on rank, mask, initialization and local behavior.
    """
    raw=np.asarray(observations,dtype=float)
    mask=np.asarray(observed_mask,dtype=bool)
    if raw.ndim<2 or mask.shape!=raw.shape or any(d<1 for d in raw.shape):
        raise ValueError("observations and mask must share a nonempty order>=2 shape")
    if not np.all(np.isfinite(raw[mask])):
        raise ValueError("observed entries must be finite")
    if not np.any(mask): raise ValueError("at least one observation is required")
    if np.all(mask): raise ValueError("completion requires at least one missing entry")
    if isinstance(max_iter,bool) or int(max_iter)!=max_iter or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    if not np.isfinite(tolerance) or tolerance<0:
        raise ValueError("tolerance must be finite and nonnegative")
    if initialization not in ("mean","zero"):
        raise ValueError("initialization must be 'mean' or 'zero'")
    mean=float(np.mean(raw[mask]))
    filled=np.where(mask,raw,mean if initialization=="mean" else 0.0)
    history=[]
    for _ in range(int(max_iter)):
        model=tt_svd(filled,max_rank=max_rank,tolerance=0.0)
        projected=tt_reconstruct(model["cores"])
        previous=filled[~mask].copy()
        filled=np.where(mask,raw,projected)
        change=float(np.linalg.norm(filled[~mask]-previous))
        scale=max(1.0,float(np.linalg.norm(previous)))
        history.append(change/scale)
        if history[-1]<=tolerance: break
    model=tt_svd(filled,max_rank=max_rank,tolerance=0.0)
    return {"completed":filled,"cores":model["cores"],"ranks":model["ranks"],
            "relative_change_history":history,"iterations":len(history),
            "observed_rmse":float(np.sqrt(np.mean((filled[mask]-raw[mask])**2)))}

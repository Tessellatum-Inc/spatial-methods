"""Automatic Target Generation Process (ATGP) for candidate endmembers."""
import numpy as np

def atgp(data, n_endmembers, mask=None, tolerance=1e-10):
    x=np.asarray(data,dtype=float)
    if x.ndim!=3 or not np.all(np.isfinite(x)): raise ValueError("data must be finite rows x cols x bands")
    r,c,b=x.shape
    if not isinstance(n_endmembers,(int,np.integer)) or not 1<=n_endmembers<=b: raise ValueError("n_endmembers must be in [1, bands]")
    valid=np.ones((r,c),bool) if mask is None else np.asarray(mask,dtype=bool)
    if valid.shape!=(r,c) or valid.sum()<n_endmembers: raise ValueError("mask must select at least n_endmembers pixels")
    if tolerance<=0: raise ValueError("tolerance must be positive")
    Y=x[valid].T; residual=Y.copy(); selected=[]
    for _ in range(n_endmembers):
        energy=np.einsum("ij,ij->j",residual,residual)
        if selected: energy[selected]=-np.inf
        idx=int(np.argmax(energy)); selected.append(idx)
        v=Y[:,idx]
        # Orthogonally remove the subspace spanned by all selected signatures.
        Q,_=np.linalg.qr(Y[:,selected])
        residual=Y-Q@(Q.T@Y)
        if np.linalg.norm(residual)<tolerance: break
    local=np.asarray(selected,dtype=int); flat=np.flatnonzero(valid)[local]
    return {"endmembers":Y[:,local],"pixel_indices":flat,"selected_count":len(local)}

"""N-FINDR endmember extraction using simplex-volume maximisation."""
import numpy as np

def nfindr(data, n_endmembers, max_iter=3, seed=0, mask=None):
    x=np.asarray(data,dtype=float)
    if x.ndim!=3 or not np.all(np.isfinite(x)): raise ValueError("data must be finite rows x cols x bands")
    r,c,b=x.shape; p=n_endmembers
    if not isinstance(p,(int,np.integer)) or not 2<=p<=b: raise ValueError("n_endmembers must be in [2, bands]")
    if max_iter<1: raise ValueError("max_iter must be positive")
    valid=np.ones((r,c),bool) if mask is None else np.asarray(mask,dtype=bool)
    if valid.shape!=(r,c) or valid.sum()<p: raise ValueError("mask must select at least p pixels")
    Y=x[valid].T; mean=Y.mean(axis=1,keepdims=True)
    U,_,_=np.linalg.svd(Y-mean,full_matrices=False); Z=U[:,:p-1].T@(Y-mean)
    rng=np.random.default_rng(seed); chosen=rng.choice(Y.shape[1],p,replace=False).tolist()
    def volume(indices):
        # Homogeneous coordinates: determinant magnitude is proportional to simplex volume.
        M=np.vstack((Z[:,indices],np.ones(p)))
        return abs(float(np.linalg.det(M)))
    best=volume(chosen); iterations=0
    for _ in range(max_iter):
        changed=False
        for j in range(p):
            for candidate in range(Y.shape[1]):
                if candidate in chosen: continue
                trial=chosen.copy(); trial[j]=candidate
                score=volume(trial)
                if score>best*(1+1e-12):
                    chosen=trial; best=score; changed=True
        iterations+=1
        if not changed: break
    local=np.asarray(chosen,dtype=int); flat=np.flatnonzero(valid)[local]
    return {"endmembers":Y[:,local],"pixel_indices":flat,"simplex_volume_determinant":best,
            "iterations":iterations,"seed":seed}

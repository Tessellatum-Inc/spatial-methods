"""Permutation-based Knox test for space-time interaction."""
from __future__ import annotations
import numpy as np

def knox_test(coordinates,times,*,spatial_threshold,temporal_threshold,
              permutations=999,seed=None):
    """Count pairs close in both space and time; permute times for null.

    Coordinates are planar in a common linear unit. Times are numeric in a
    common time unit. The one-sided alternative is excess close pairs.
    """
    xy=np.asarray(coordinates,dtype=float); t=np.asarray(times,dtype=float)
    if xy.ndim!=2 or xy.shape[1]!=2 or len(xy)<3 or not np.isfinite(xy).all():
        raise ValueError("coordinates must be a finite (n, 2) array with n >= 3")
    if t.shape!=(len(xy),) or not np.isfinite(t).all():
        raise ValueError("times must be a finite vector matching coordinates")
    ds=float(spatial_threshold); dt=float(temporal_threshold)
    if not np.isfinite([ds,dt]).all() or ds<=0 or dt<=0:
        raise ValueError("spatial and temporal thresholds must be finite and positive")
    if isinstance(permutations,(bool,np.bool_)) or not isinstance(permutations,(int,np.integer)) or permutations<1:
        raise ValueError("permutations must be an integer >= 1")
    delta=xy[:,None,:]-xy[None,:,:]
    distance=np.sqrt(np.sum(delta*delta,axis=2))
    spatial=(distance<=ds)
    temporal=np.abs(t[:,None]-t[None,:])<=dt
    upper=np.triu(np.ones((len(t),len(t)),dtype=bool),1)
    observed=int(np.count_nonzero(spatial & temporal & upper))
    rng=np.random.default_rng(seed)
    counts=np.empty(int(permutations),dtype=np.int64)
    for k in range(int(permutations)):
        perm=rng.permutation(t)
        counts[k]=np.count_nonzero(spatial & (np.abs(perm[:,None]-perm[None,:])<=dt) & upper)
    p=float((1+np.count_nonzero(counts>=observed))/(int(permutations)+1))
    expected=float(np.mean(counts))
    sd=float(np.std(counts,ddof=1)) if len(counts)>1 else 0.0
    z=float((observed-expected)/sd) if sd>0 else (0.0 if observed==expected else float("inf"))
    return {"observed_pairs":observed,"null_mean":expected,"null_standard_deviation":sd,
            "z_score":z,"p_value_upper":p,"permutation_counts":counts,
            "spatial_threshold":ds,"temporal_threshold":dt,
            "permutations":int(permutations)}

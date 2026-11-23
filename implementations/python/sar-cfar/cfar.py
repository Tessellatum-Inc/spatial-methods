"""Two-dimensional CA-CFAR and OS-CFAR for SAR intensity rasters."""
from dataclasses import dataclass
import math
import numpy as np

@dataclass(frozen=True)
class CFARResult:
    detections: np.ndarray
    threshold: np.ndarray
    background: np.ndarray
    valid: np.ndarray

def _validate(image, guard_cells, training_cells, pfa):
    x=np.asarray(image,dtype=float)
    if x.ndim!=2 or min(x.shape)<1: raise ValueError("image must be non-empty and 2-D")
    if not isinstance(guard_cells,(int,np.integer)) or guard_cells<0: raise ValueError("guard_cells must be a non-negative integer")
    if not isinstance(training_cells,(int,np.integer)) or training_cells<1: raise ValueError("training_cells must be a positive integer")
    if training_cells<=guard_cells: raise ValueError("training_cells must exceed guard_cells")
    if not np.isscalar(pfa) or not np.isfinite(pfa) or not 0<pfa<1: raise ValueError("pfa must be between zero and one")
    if np.any(x[np.isfinite(x)]<0): raise ValueError("intensity must be non-negative")
    return x

def _ring(x,r,c,g,t):
    return [float(x[rr,cc]) for rr in range(r-t,r+t+1) for cc in range(c-t,c+t+1)
            if max(abs(rr-r),abs(cc-c))>g and np.isfinite(x[rr,cc])]

def ca_cfar_2d(image,guard_cells=1,training_cells=4,false_alarm_rate=1e-3,min_training_cells=1):
    """Square-ring cell-averaging CFAR for exponential intensity."""
    x=_validate(image,guard_cells,training_cells,false_alarm_rate)
    if not isinstance(min_training_cells,(int,np.integer)) or min_training_cells<1: raise ValueError("min_training_cells must be positive")
    n=(2*training_cells+1)**2-(2*guard_cells+1)**2
    alpha=n*(false_alarm_rate**(-1.0/n)-1.0)
    return _detect(x,guard_cells,training_cells,min_training_cells,lambda v:float(np.mean(v)),alpha)

def _os_alpha(n,k,pfa):
    def prob(a): return math.exp(sum(math.log((n-i)/(n-i+a)) for i in range(k)))
    lo,hi=0.0,1.0
    while prob(hi)>pfa: hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if prob(mid)>pfa: lo=mid
        else: hi=mid
    return (lo+hi)/2

def os_cfar_2d(image,guard_cells=1,training_cells=4,false_alarm_rate=1e-3,rank=None,min_training_cells=None):
    """Ordered-statistics CFAR; rank is one-based among ascending training values."""
    x=_validate(image,guard_cells,training_cells,false_alarm_rate)
    n=(2*training_cells+1)**2-(2*guard_cells+1)**2
    if rank is None: rank=max(1,math.ceil(.75*n))
    if not isinstance(rank,(int,np.integer)) or not 1<=rank<=n: raise ValueError("rank must be in [1, nominal training count]")
    minimum=rank if min_training_cells is None else min_training_cells
    if not isinstance(minimum,(int,np.integer)) or minimum<rank: raise ValueError("min_training_cells must be at least rank")
    alpha=_os_alpha(n,int(rank),float(false_alarm_rate))
    return _detect(x,guard_cells,training_cells,minimum,lambda v:float(np.partition(v,int(rank)-1)[int(rank)-1]),alpha)

def _detect(x,g,t,minimum,estimator,alpha):
    shape=x.shape
    threshold=np.full(shape,np.nan); background=np.full(shape,np.nan)
    valid=np.zeros(shape,dtype=bool); detections=np.zeros(shape,dtype=bool)
    for r in range(t,shape[0]-t):
        for c in range(t,shape[1]-t):
            cut=x[r,c]
            if not np.isfinite(cut): continue
            values=_ring(x,r,c,g,t)
            if len(values)<minimum: continue
            noise=estimator(np.asarray(values))
            background[r,c]=noise; threshold[r,c]=alpha*noise
            valid[r,c]=True; detections[r,c]=cut>threshold[r,c]
    return CFARResult(detections,threshold,background,valid)

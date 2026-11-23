"""Local adaptive thresholding for finite grayscale arrays."""
from __future__ import annotations
import numpy as np

def _box_mean(a, size):
    p=size//2
    x=np.pad(a,((p,p),(p,p)),mode="reflect")
    integral=np.pad(x,((1,0),(1,0))).cumsum(0).cumsum(1)
    sums=integral[size:,size:]-integral[:-size,size:]-integral[size:,:-size]+integral[:-size,:-size]
    return sums/(size*size)

def adaptive_threshold(image, window_size=15, offset=0.0, method="mean"):
    """Return (binary, local_threshold); foreground is image > local_threshold.

    Gaussian mode uses a separable Gaussian approximation with reflect padding.
    """
    a=np.asarray(image,dtype=float)
    if a.ndim!=2 or not np.all(np.isfinite(a)): raise ValueError("image must be a finite 2-D array")
    if not isinstance(window_size,(int,np.integer)) or window_size<3 or window_size%2==0:
        raise ValueError("window_size must be an odd integer >= 3")
    if not np.isfinite(offset): raise ValueError("offset must be finite")
    if method=="mean": local=_box_mean(a,window_size)
    elif method=="gaussian":
        sigma=max(window_size/6,0.5); coords=np.arange(window_size)-window_size//2
        k=np.exp(-(coords**2)/(2*sigma**2)); k/=k.sum()
        p=window_size//2
        tmp=np.pad(a,((0,0),(p,p)),mode="reflect")
        tmp=np.apply_along_axis(lambda r: np.convolve(r,k,mode="valid"),1,tmp)
        tmp=np.pad(tmp,((p,p),(0,0)),mode="reflect")
        local=np.apply_along_axis(lambda c: np.convolve(c,k,mode="valid"),0,tmp)
    else: raise ValueError("method must be mean or gaussian")
    threshold=local-offset
    return a>threshold, threshold

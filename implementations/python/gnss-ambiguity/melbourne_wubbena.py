"""Sequential Melbourne-Wubbena wide-lane cycle-slip screening."""
from __future__ import annotations
import numpy as np

def detect_melbourne_wubbena_slips(values, epochs=None, sigma_multiplier=4.0,
                                    initial_sigma=0.1, max_gap=None):
    """Flag MW discontinuities against a running arc mean and standard deviation.

    MW values are in wide-lane cycles. The first value initializes an arc.
    A candidate exceeding sigma_multiplier * prior_sigma is flagged and
    starts a new arc at that epoch. Large epoch gaps also reset the arc but
    are not themselves marked as cycle slips.

    This is a transparent threshold screen, not the full Springer algorithm,
    TurboEdit, integer slip identification, or a repair method. Tune the
    initial_sigma/noise model to the receiver, signal and observation setup.
    """
    y=np.asarray(values,dtype=float)
    if y.ndim!=1 or len(y)<2 or not np.all(np.isfinite(y)):
        raise ValueError("values must be a finite 1D series with at least two observations")
    if not np.isfinite(sigma_multiplier) or sigma_multiplier<=0:
        raise ValueError("sigma_multiplier must be finite and positive")
    if not np.isfinite(initial_sigma) or initial_sigma<=0:
        raise ValueError("initial_sigma must be finite and positive")
    if epochs is None:
        t=np.arange(len(y),dtype=float)
    else:
        t=np.asarray(epochs,dtype=float)
        if t.shape!=y.shape or not np.all(np.isfinite(t)) or np.any(np.diff(t)<=0):
            raise ValueError("epochs must be finite, strictly increasing and match values")
    if max_gap is not None and (not np.isfinite(max_gap) or max_gap<=0):
        raise ValueError("max_gap must be finite and positive")
    flags=np.zeros(len(y),dtype=bool)
    gap_resets=np.zeros(len(y),dtype=bool)
    residuals=np.full(len(y),np.nan)
    thresholds=np.full(len(y),np.nan)
    mean=float(y[0]); count=1; m2=0.0; sigma=float(initial_sigma)
    for i in range(1,len(y)):
        if max_gap is not None and t[i]-t[i-1]>max_gap:
            gap_resets[i]=True
            mean=float(y[i]); count=1; m2=0.0; sigma=float(initial_sigma)
            continue
        residual=float(y[i]-mean)
        threshold=float(sigma_multiplier*sigma)
        residuals[i]=residual; thresholds[i]=threshold
        if abs(residual)>threshold:
            flags[i]=True
            mean=float(y[i]); count=1; m2=0.0; sigma=float(initial_sigma)
            continue
        count+=1
        delta=float(y[i]-mean)
        mean+=delta/count
        m2+=delta*(y[i]-mean)
        sigma=max(float(initial_sigma),float(np.sqrt(m2/(count-1))) if count>1 else float(initial_sigma))
    return {"flags":flags,"gap_resets":gap_resets,"residuals":residuals,
            "thresholds":thresholds}

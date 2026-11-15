"""Sequential geometry-free carrier-phase cycle-slip screening."""
from __future__ import annotations
import numpy as np

def detect_geometry_free_slips(values, epochs=None, window=7, threshold=0.08, max_gap=None):
    """Flag GF phase-combination jumps using a local quadratic predictor.

    Parameters
    ----------
    values : 1D array
        Geometry-free carrier-phase combination, in metres.
    epochs : 1D array, optional
        Strictly increasing epoch coordinates in seconds. Defaults to
        equally spaced integer epochs.
    window : int
        Number of preceding accepted observations used for least squares.
    threshold : float
        Absolute prediction-residual threshold in metres.
    max_gap : float, optional
        A gap larger than this resets the prediction history.

    Notes
    -----
    This is a transparent screening baseline, not a complete TurboEdit
    implementation. It detects discontinuities in the supplied GF series;
    it does not estimate or repair integer cycle slips and can confuse
    rapid ionospheric variation, multipath or outliers with slips.
    """
    y=np.asarray(values,dtype=float)
    if y.ndim!=1 or len(y)<window+1 or not np.all(np.isfinite(y)):
        raise ValueError("values must be a finite 1D series with at least window+1 observations")
    if not isinstance(window,int) or isinstance(window,bool) or window<3:
        raise ValueError("window must be an integer >= 3")
    if not np.isfinite(threshold) or threshold<=0:
        raise ValueError("threshold must be finite and positive")
    if epochs is None:
        t=np.arange(len(y),dtype=float)
    else:
        t=np.asarray(epochs,dtype=float)
        if t.shape!=y.shape or not np.all(np.isfinite(t)) or np.any(np.diff(t)<=0):
            raise ValueError("epochs must be finite, strictly increasing and match values")
    if max_gap is not None and (not np.isfinite(max_gap) or max_gap<=0):
        raise ValueError("max_gap must be finite and positive")
    flags=np.zeros(len(y),dtype=bool)
    residuals=np.full(len(y),np.nan)
    # Keep the first window as the initial arc. A gap starts a fresh arc.
    accepted=list(range(window))
    for i in range(window,len(y)):
        if max_gap is not None and t[i]-t[i-1]>max_gap:
            accepted=[i]
            continue
        history=accepted[-window:]
        if len(history)<window:
            accepted.append(i)
            continue
        x=t[history]-t[i]
        design=np.column_stack([np.ones(window),x,x*x])
        coef=np.linalg.lstsq(design,y[history],rcond=None)[0]
        prediction=float(coef[0])
        residual=float(y[i]-prediction)
        residuals[i]=residual
        if abs(residual)>threshold:
            flags[i]=True
            # Start a new arc at the flagged epoch; never fit across the jump.
            accepted=[i]
        else:
            accepted.append(i)
    return {"flags":flags,"residuals":residuals,"accepted_indices":np.asarray(accepted,dtype=int)}

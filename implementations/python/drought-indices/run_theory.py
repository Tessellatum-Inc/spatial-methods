"""Threshold-run event detection for drought and climate time series."""
from __future__ import annotations
import numpy as np


def run_theory_events(series, threshold, *, direction="below",
                      min_duration=1, max_gap=0):
    """Extract threshold runs and event severity from a one-dimensional series.

    A run is a contiguous sequence of threshold-exceedance observations.
    Brief non-exceedance gaps may be bridged; missing values always terminate
    a run. Duration counts calendar samples from start through end, while
    exceedance_days counts only samples beyond the threshold. Severity is
    summed over exceedance samples only.
    """
    x=np.asarray(series,dtype=float)
    if x.ndim!=1 or x.size==0: raise ValueError("series must be a non-empty vector")
    if not np.isfinite(threshold): raise ValueError("threshold must be finite")
    if direction not in ("below","above"): raise ValueError("direction must be below or above")
    if not isinstance(min_duration,int) or min_duration<1 or not isinstance(max_gap,int) or max_gap<0:
        raise ValueError("min_duration must be positive and max_gap nonnegative")
    valid=np.isfinite(x)
    exceed=(x<threshold if direction=="below" else x>threshold)&valid
    severity=np.where(exceed,threshold-x if direction=="below" else x-threshold,0.0)
    indices=np.flatnonzero(exceed)
    if indices.size==0: return []
    groups=[];start=previous=int(indices[0])
    for idx in indices[1:]:
        gap=int(idx)-previous-1
        if gap>max_gap or not valid[previous+1:int(idx)].all():
            groups.append((start,previous));start=int(idx)
        previous=int(idx)
    groups.append((start,previous))
    events=[]
    for start,end in groups:
        event_severity=severity[start:end+1]
        count=int(exceed[start:end+1].sum())
        duration=end-start+1
        if count<min_duration: continue
        vals=event_severity[event_severity>0]
        events.append({"start":start,"end":end,"duration":duration,
          "exceedance_days":count,"severity":float(vals.sum()),
          "peak_severity":float(vals.max()),"mean_severity":float(vals.mean())})
    return events

"""Explicit interval-based raster reclassification."""
from __future__ import annotations
import math
import numpy as np


def reclassify_ranges(values, rules, *, default=np.nan, nodata=None):
    """Map numeric values through non-overlapping [lower, upper) rules.

    rules is an iterable of (lower, upper, replacement). Bounds must be finite,
    each lower bound must be less than its upper bound, and rules may not
    overlap. Gaps receive default. If nodata is supplied, matching source
    cells remain nodata in the output. NaN source cells are always preserved
    as NaN. Output is float to support NaN defaults.
    """
    x=np.asarray(values,dtype=float)
    if x.size==0 or not np.isfinite(x[~np.isnan(x)]).all():
        raise ValueError("values must be a non-empty numeric array without infinities")
    if not math.isfinite(default) and not math.isnan(default):
        raise ValueError("default must be finite or NaN")
    parsed=[]
    for rule in rules:
        if len(rule)!=3:
            raise ValueError("each rule must be (lower, upper, replacement)")
        lo,hi,new=map(float,rule)
        if not math.isfinite(lo) or not math.isfinite(hi) or lo>=hi:
            raise ValueError("rule bounds must be finite with lower < upper")
        if not math.isfinite(new):
            raise ValueError("replacement values must be finite")
        parsed.append((lo,hi,new))
    parsed.sort(key=lambda r:r[0])
    for previous,current in zip(parsed,parsed[1:]):
        if current[0]<previous[1]:
            raise ValueError("range rules must not overlap")
    out=np.full(x.shape,float(default),dtype=float)
    for lo,hi,new in parsed:
        out[(x>=lo)&(x<hi)]=new
    nan_mask = np.isnan(x)
    if nodata is not None:
        nodata_mask = nan_mask if isinstance(nodata, (float, np.floating)) and math.isnan(float(nodata)) else x == nodata
        out[nodata_mask] = float(nodata)
    # NaN is missing data independently of a numeric NoData sentinel.
    if not (nodata is not None and isinstance(nodata, (float, np.floating)) and math.isnan(float(nodata))):
        out[nan_mask] = np.nan
    return out

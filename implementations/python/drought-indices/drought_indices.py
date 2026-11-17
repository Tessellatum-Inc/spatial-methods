"""Vegetation, thermal and precipitation drought indicators."""
from __future__ import annotations
import numpy as np
from scipy.stats import gamma,norm

def _same_shape(*arrays):
    values=[np.asarray(a,dtype=float) for a in arrays]
    if any(a.shape!=values[0].shape for a in values[1:]): raise ValueError("all input arrays must have the same shape")
    return values

def _range_index(value,minimum,maximum,reverse=False):
    x,lo,hi=_same_shape(value,minimum,maximum)
    if np.any(np.isfinite(lo)&np.isfinite(hi)&(hi<lo)): raise ValueError("minimum must not exceed maximum")
    span=hi-lo;num=hi-x if reverse else x-lo
    return np.divide(100*num,span,out=np.full(x.shape,np.nan),where=np.isfinite(span)&(span>0))

def vegetation_condition_index(ndvi,ndvi_min,ndvi_max):
    """VCI = 100 (NDVI - min)/(max - min), clipped to [0,100]."""
    return np.clip(_range_index(ndvi,ndvi_min,ndvi_max),0,100)

def temperature_condition_index(lst,lst_min,lst_max):
    """TCI = 100 (max LST - LST)/(max - min), clipped to [0,100]."""
    return np.clip(_range_index(lst,lst_min,lst_max,True),0,100)

def vegetation_health_index(vci,tci,*,alpha=.5):
    """Weighted VCI/TCI combination."""
    v,t=_same_shape(vci,tci)
    if not np.isfinite(alpha) or not 0<=alpha<=1: raise ValueError("alpha must be between 0 and 1")
    return alpha*v+(1-alpha)*t

def standardized_precipitation_index(precipitation,*,axis=0,min_samples=30,min_positive=10,clip_probability=1e-10):
    """Gamma SPI with mixed zero-rainfall probability, fitted per time series.

    H(x)=q+(1-q)G(x), where q is zero fraction and G is a gamma CDF fitted
    to positive rainfall with location fixed at zero. This is a single-
    population fit, not calendar-month-specific SPI; group comparable
    seasons before fitting where seasonality matters.
    """
    x=np.asarray(precipitation,dtype=float)
    if x.ndim==0 or x.shape[axis]==0: raise ValueError("precipitation needs a non-empty time axis")
    if np.any(np.isfinite(x)&(x<0)): raise ValueError("precipitation must be non-negative")
    if not isinstance(min_samples,int) or min_samples<2 or not isinstance(min_positive,int) or min_positive<2: raise ValueError("sample thresholds must be integers >= 2")
    if not np.isfinite(clip_probability) or not 0<clip_probability<.5: raise ValueError("clip_probability must be between 0 and 0.5")
    moved=np.moveaxis(x,axis,0);out=np.full(moved.shape,np.nan);spatial=moved.shape[1:]
    for idx in np.ndindex(spatial):
        series=moved[(slice(None),)+idx];valid=np.isfinite(series);sample=series[valid]
        if sample.size<min_samples: continue
        positive=sample[sample>0]
        if positive.size<min_positive: continue
        q=1-positive.size/sample.size
        shape,loc,scale=gamma.fit(positive,floc=0)
        if not np.isfinite(shape+scale) or shape<=0 or scale<=0: continue
        probs=q+(1-q)*gamma.cdf(series[valid],shape,loc=0,scale=scale)
        out[(valid,)+idx]=norm.ppf(np.clip(probs,clip_probability,1-clip_probability))
    return np.moveaxis(out,0,axis)


def growing_degree_days(tmin, tmax, *, base_temperature, upper_temperature=None):
    """Daily mean-method growing degree days, optionally capped at an upper mean.

    Returns daily increments; accumulate them over the crop's specified
    growing period. Missing daily temperatures remain NaN.
    """
    lo, hi = _same_shape(tmin, tmax)
    if np.any(np.isfinite(lo) & np.isfinite(hi) & (hi < lo)):
        raise ValueError("tmax must not be below tmin")
    if not np.isfinite(base_temperature):
        raise ValueError("base_temperature must be finite")
    mean = (lo + hi) / 2.0
    if upper_temperature is not None:
        if not np.isfinite(upper_temperature) or upper_temperature < base_temperature:
            raise ValueError("upper_temperature must be finite and at least base_temperature")
        mean = np.minimum(mean, upper_temperature)
    return np.maximum(mean - base_temperature, 0.0)

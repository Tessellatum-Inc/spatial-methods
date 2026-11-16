"""Shannon, Renyi, Tsallis and ordinal-pattern entropy measures."""
from __future__ import annotations
import math
import numpy as np


def _probabilities(values):
    x=np.asarray(values,dtype=float)
    if x.ndim!=1 or x.size==0 or not np.isfinite(x).all() or np.any(x<0):
        raise ValueError("values must be a non-empty finite non-negative vector")
    total=x.sum()
    if total<=0: raise ValueError("values must have positive total")
    p=x/total
    return p[p>0]


def shannon_entropy(values, *, base=2.0):
    """Shannon entropy of counts or nonnegative weights."""
    if not math.isfinite(base) or base<=0 or base==1: raise ValueError("base must be positive and not one")
    p=_probabilities(values)
    return float(-np.sum(p*np.log(p))/math.log(base))


def renyi_entropy(values, *, order=2.0, base=2.0):
    """Renyi entropy of positive order; the order-one limit is Shannon."""
    if not math.isfinite(order) or order<=0: raise ValueError("order must be finite and positive")
    if not math.isfinite(base) or base<=0 or base==1: raise ValueError("base must be positive and not one")
    p=_probabilities(values)
    if math.isclose(order,1.0,rel_tol=1e-8,abs_tol=1e-10):
        return shannon_entropy(values,base=base)
    return float(np.log(np.sum(p**order))/((1-order)*math.log(base)))


def tsallis_entropy(values, *, q=2.0):
    """Tsallis entropy with its Shannon limit at q=1."""
    if not math.isfinite(q) or q<=0: raise ValueError("q must be finite and positive")
    p=_probabilities(values)
    if math.isclose(q,1.0,rel_tol=1e-8,abs_tol=1e-10):
        return shannon_entropy(values)
    return float((1-np.sum(p**q))/(q-1))


def categorical_entropy(values, *, mask=None, base=2.0):
    """Entropy of a categorical raster or vector after optional boolean masking."""
    x=np.asarray(values)
    if x.size==0: raise ValueError("values must be non-empty")
    if mask is not None:
        m=np.asarray(mask)
        if m.shape!=x.shape or m.dtype!=bool: raise ValueError("mask must be boolean and match values")
        x=x[m]
    if x.size==0: raise ValueError("mask leaves no observations")
    _,counts=np.unique(x,return_counts=True)
    return shannon_entropy(counts,base=base)


def permutation_entropy(series, *, order=3, delay=1, normalize=True):
    """Ordinal-pattern entropy using stable tie ordering.

    Ties are deterministically broken by original position. For quantized
    signals with many ties, results depend on this convention.
    """
    x=np.asarray(series,dtype=float)
    if x.ndim!=1 or not np.isfinite(x).all(): raise ValueError("series must be a finite one-dimensional vector")
    if not isinstance(order,int) or order<2 or not isinstance(delay,int) or delay<1:
        raise ValueError("order must be >=2 and delay must be >=1")
    n=x.size-(order-1)*delay
    if n<1: raise ValueError("series is too short for order and delay")
    patterns={}
    for start in range(n):
        window=x[start:start+order*delay:delay]
        pattern=tuple(np.argsort(window,kind="stable"))
        patterns[pattern]=patterns.get(pattern,0)+1
    h=shannon_entropy(list(patterns.values()),base=math.e)
    return h/math.log(math.factorial(order)) if normalize else h

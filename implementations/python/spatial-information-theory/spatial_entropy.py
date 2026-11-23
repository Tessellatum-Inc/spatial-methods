"""Entropy measures for categorical rasters, spatial edges and time series."""
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
    if math.isclose(order,1.0,rel_tol=1e-8,abs_tol=1e-10): return shannon_entropy(values,base=base)
    return float(np.log(np.sum(p**order))/((1-order)*math.log(base)))


def tsallis_entropy(values, *, q=2.0):
    """Tsallis entropy with its Shannon limit at q=1."""
    if not math.isfinite(q) or q<=0: raise ValueError("q must be finite and positive")
    p=_probabilities(values)
    if math.isclose(q,1.0,rel_tol=1e-8,abs_tol=1e-10): return shannon_entropy(values)
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
    """Ordinal-pattern entropy; stable sorting breaks ties by original position."""
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


def sample_entropy(series, *, m=2, r=0.2, normalize_r=True):
    """Sample entropy: -log(A/B) for matching length-(m+1) vs length-m pairs.

    Uses Chebyshev distance and unordered, non-self template pairs. If r is
    normalized, the tolerance is r times the population standard deviation.
    """
    x=np.asarray(series,dtype=float)
    if x.ndim!=1 or not np.isfinite(x).all(): raise ValueError("series must be finite and one-dimensional")
    if not isinstance(m,int) or m<1: raise ValueError("m must be a positive integer")
    if not math.isfinite(r) or r<=0: raise ValueError("r must be finite and positive")
    if x.size<m+2: raise ValueError("series is too short for m")
    tolerance=r*float(np.std(x)) if normalize_r else r
    templates_m=np.lib.stride_tricks.sliding_window_view(x,m)[:-1]
    templates_m1=np.lib.stride_tricks.sliding_window_view(x,m+1)
    def matches(templates):
        count=0
        for i in range(len(templates)-1):
            count += int(np.count_nonzero(np.max(np.abs(templates[i+1:]-templates[i]),axis=1)<=tolerance))
        return count
    b=matches(templates_m)
    if b==0: raise ValueError("no matching template pairs of length m; increase r or reduce m")
    a=matches(templates_m1)
    if a==0: return math.inf
    return float(-math.log(a/b))


def _spatial_edge_entropies(values, adjacency, *, base=2.0):
    """Return origin, neighbour, joint entropy for weighted directed edges."""
    labels=np.asarray(values)
    w=np.asarray(adjacency,dtype=float)
    n=labels.size
    if labels.ndim!=1 or n==0 or w.shape!=(n,n): raise ValueError("values must be non-empty 1-D and adjacency must be n by n")
    if not np.isfinite(w).all() or np.any(w<0): raise ValueError("adjacency weights must be finite and non-negative")
    if not math.isfinite(base) or base<=0 or base==1: raise ValueError("base must be positive and not one")
    w=w.copy()
    np.fill_diagonal(w,0.0)
    origins, neighbours=np.nonzero(w>0)
    edge_weights=w[origins,neighbours]
    if edge_weights.size==0: raise ValueError("adjacency must contain at least one positive off-diagonal edge")
    _,oi=np.unique(labels,return_inverse=True)
    _,ni=np.unique(labels,return_inverse=True)
    k=int(max(oi.max(),ni.max())+1)
    joint=np.zeros((k,k),dtype=float)
    np.add.at(joint,(oi[origins],ni[neighbours]),edge_weights)
    origin=joint.sum(axis=1)
    neighbour=joint.sum(axis=0)
    h_origin=shannon_entropy(origin,base=base)
    h_neighbour=shannon_entropy(neighbour,base=base)
    h_joint=shannon_entropy(joint.ravel(),base=base)
    return h_origin,h_neighbour,h_joint


def spatial_conditional_entropy(values, adjacency, *, base=2.0):
    """Weighted directed-edge H(category at neighbour | category at origin)."""
    h_origin,_,h_joint=_spatial_edge_entropies(values,adjacency,base=base)
    return max(0.0,float(h_joint-h_origin))


def spatial_mutual_information(values, adjacency, *, base=2.0):
    """Mutual information between endpoint categories over weighted directed edges."""
    h_origin,h_neighbour,h_joint=_spatial_edge_entropies(values,adjacency,base=base)
    return max(0.0,float(h_origin+h_neighbour-h_joint))

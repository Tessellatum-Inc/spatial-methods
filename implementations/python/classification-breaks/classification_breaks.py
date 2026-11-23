"""One-dimensional thematic classification breaks for spatial attributes."""
from __future__ import annotations
import math
import numpy as np

def _values(data):
    values = np.asarray(data, dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or not np.isfinite(values).all():
        raise ValueError("values must be a non-empty finite one-dimensional array")
    return values

def _validate_class_count(n_classes, unique_count):
    if not isinstance(n_classes, int) or not 1 <= n_classes <= unique_count:
        raise ValueError("n_classes must be an integer between 1 and the number of unique values")

def geometric_interval_breaks(data, n_classes):
    """Geometric-progression class edges for strictly positive observations."""
    values = _values(data); unique_count = len(np.unique(values)); _validate_class_count(n_classes, unique_count)
    if np.any(values <= 0): raise ValueError("geometric intervals require strictly positive values")
    lower, upper = float(values.min()), float(values.max())
    if unique_count == 1 or n_classes == 1:
        return np.array([lower]) if lower == upper else np.array([lower, upper])
    log_ratio = (math.log(upper) - math.log(lower)) / n_classes
    edges = [lower]
    edges.extend(math.exp(math.log(lower) + i * log_ratio) for i in range(1, n_classes))
    edges.append(upper)
    return np.unique(np.asarray(edges, dtype=float))

def standard_deviation_breaks(data, half_steps=2):
    """Mean +/- integer-standard-deviation boundaries, clipped to data range."""
    values = _values(data)
    if not isinstance(half_steps, int) or half_steps < 1: raise ValueError("half_steps must be a positive integer")
    lower, upper = float(values.min()), float(values.max())
    mean, std = float(values.mean()), float(values.std(ddof=0))
    interior = [np.clip(mean + step * std, lower, upper) for step in range(-half_steps, half_steps + 1)]
    return np.unique(np.asarray([lower, *interior, upper], dtype=float))

def box_plot_breaks(data):
    """Minimum, clipped Tukey fences, quartiles, median and maximum."""
    values = _values(data); lower, upper = float(values.min()), float(values.max())
    q1, median, q3 = np.quantile(values, [0.25, 0.5, 0.75]); iqr = q3-q1
    low = np.clip(q1-1.5*iqr, lower, upper); high = np.clip(q3+1.5*iqr, lower, upper)
    return np.unique(np.asarray([lower, low, q1, median, q3, high, upper]))

def head_tail_breaks(data, max_classes=6, min_head_fraction=0.4):
    """Recursively split a heavy-tailed distribution at the current head mean."""
    values = _values(data)
    if not isinstance(max_classes, int) or max_classes < 1: raise ValueError("max_classes must be a positive integer")
    if not math.isfinite(min_head_fraction) or not 0 < min_head_fraction < 1:
        raise ValueError("min_head_fraction must be strictly between 0 and 1")
    lower, upper = float(values.min()), float(values.max()); boundaries=[lower, upper]; current=values
    for _ in range(max_classes-1):
        if current.size < 2: break
        mean=float(current.mean()); head=current[current>mean]
        if head.size == 0: break
        boundaries.append(mean)
        if head.size/current.size <= min_head_fraction: break
        current=head
    return np.unique(np.asarray(boundaries,dtype=float))

def dalenius_hodges_breaks(data, n_classes, bins=None):
    """Approximate optimal stratification using cumulative square-root frequencies."""
    values=_values(data); unique_count=len(np.unique(values)); _validate_class_count(n_classes,unique_count)
    lower,upper=float(values.min()),float(values.max())
    if unique_count==1 or n_classes==1:
        return np.array([lower]) if lower==upper else np.array([lower,upper])
    if bins is None: bins=max(n_classes,min(100,math.ceil(math.sqrt(values.size))))
    if not isinstance(bins,int) or bins<n_classes: raise ValueError("bins must be an integer at least as large as n_classes")
    frequencies,edges=np.histogram(values,bins=bins); cumulative=np.cumsum(np.sqrt(frequencies.astype(float))); total=cumulative[-1]
    boundaries=[lower]
    for j in range(1,n_classes):
        index=int(np.searchsorted(cumulative,total*j/n_classes,side="left"))
        boundaries.append(float(edges[min(index+1,len(edges)-1)]))
    boundaries.append(upper)
    return np.unique(np.asarray(boundaries,dtype=float))

def ckmeans_breaks(data, n_classes):
    """Exact 1D k-means breaks by dynamic programming; O(k*m^2), m unique values."""
    values=_values(data); unique,counts=np.unique(values,return_counts=True); m=len(unique)
    _validate_class_count(n_classes,m)
    if m==1: return np.array([float(unique[0])])
    if n_classes==1: return np.array([float(unique[0]),float(unique[-1])])
    weights=np.concatenate(([0.0],np.cumsum(counts.astype(float))))
    sums=np.concatenate(([0.0],np.cumsum(unique*counts)))
    sums2=np.concatenate(([0.0],np.cumsum(unique*unique*counts)))
    def cost(start,stop):
        w=weights[stop]-weights[start]; total=sums[stop]-sums[start]; total2=sums2[stop]-sums2[start]
        return max(0.0,total2-total*total/w)
    dp=np.full((n_classes+1,m+1),np.inf); previous=np.full((n_classes+1,m+1),-1,dtype=int); dp[0,0]=0.0
    for classes in range(1,n_classes+1):
        for stop in range(classes,m+1):
            best,best_start=np.inf,-1
            for start in range(classes-1,stop):
                candidate=dp[classes-1,start]+cost(start,stop)
                if candidate<best: best,best_start=candidate,start
            dp[classes,stop]=best; previous[classes,stop]=best_start
    boundaries=[]; stop=m
    for classes in range(n_classes,1,-1):
        start=previous[classes,stop]; boundaries.append((unique[start-1]+unique[start])/2.0); stop=start
    return np.unique(np.asarray([unique[0],*boundaries,unique[-1]],dtype=float))

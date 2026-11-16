"""Recurrence plots and recurrence-quantification analysis for scalar series."""
from __future__ import annotations
import math
import numpy as np


def _embedded(series, dimension, delay):
    x=np.asarray(series,dtype=float)
    if x.ndim!=1 or x.size==0 or not np.isfinite(x).all():
        raise ValueError("series must be a non-empty finite one-dimensional vector")
    if not isinstance(dimension,int) or dimension<1:
        raise ValueError("dimension must be a positive integer")
    if not isinstance(delay,int) or delay<1:
        raise ValueError("delay must be a positive integer")
    count=x.size-(dimension-1)*delay
    if count<2:
        raise ValueError("series is too short for the requested embedding")
    return np.stack([x[i*delay:i*delay+count] for i in range(dimension)],axis=1)


def recurrence_plot(series, *, threshold, dimension=1, delay=1, metric="chebyshev"):
    """Return a boolean recurrence matrix using a fixed distance threshold."""
    if not math.isfinite(threshold) or threshold<0:
        raise ValueError("threshold must be finite and non-negative")
    if metric not in {"chebyshev","euclidean"}:
        raise ValueError("metric must be 'chebyshev' or 'euclidean'")
    points=_embedded(series,dimension,delay)
    delta=np.abs(points[:,None,:]-points[None,:,:])
    distances=np.max(delta,axis=2) if metric=="chebyshev" else np.sqrt(np.sum(delta**2,axis=2))
    return distances<=threshold


def _run_lengths(mask):
    """Lengths of contiguous True runs in a one-dimensional boolean vector."""
    padded=np.concatenate(([False],np.asarray(mask,dtype=bool),[False]))
    changes=np.diff(padded.astype(np.int8))
    starts=np.flatnonzero(changes==1)
    ends=np.flatnonzero(changes==-1)
    return ends-starts


def recurrence_quantification(series, *, threshold, dimension=1, delay=1,
                              metric="chebyshev", theiler=1,
                              min_diagonal=2, min_vertical=2):
    """Calculate RR, DET, L, Lmax, DIV, ENTR, LAM, TT and Vmax.

    The Theiler window excludes cells with |i-j| <= theiler. Diagonal
    structures are counted once (upper triangle); vertical structures use
    the full symmetric recurrence matrix. ENTR is the Shannon entropy of
    qualifying diagonal-line lengths, in nats.
    """
    if not isinstance(theiler,int) or theiler<0:
        raise ValueError("theiler must be a non-negative integer")
    if not isinstance(min_diagonal,int) or min_diagonal<2:
        raise ValueError("min_diagonal must be an integer >= 2")
    if not isinstance(min_vertical,int) or min_vertical<2:
        raise ValueError("min_vertical must be an integer >= 2")
    r=recurrence_plot(series,threshold=threshold,dimension=dimension,delay=delay,metric=metric)
    n=r.shape[0]
    r=r.copy()
    rows,cols=np.indices(r.shape)
    r[np.abs(rows-cols)<=theiler]=False

    diagonal_lengths=[]
    recurrence_pairs=0
    eligible_pairs=sum(n-offset for offset in range(theiler+1,n))
    for offset in range(theiler+1,n):
        diagonal=np.diagonal(r,offset=offset)
        recurrence_pairs+=int(diagonal.sum())
        diagonal_lengths.extend(_run_lengths(diagonal).tolist())
    qualifying_diagonal=[v for v in diagonal_lengths if v>=min_diagonal]
    diagonal_points=sum(qualifying_diagonal)
    if diagonal_lengths:
        hist=np.bincount(diagonal_lengths)
        probs=hist[hist>0]/sum(hist[hist>0])
        entropy=float(-np.sum(probs*np.log(probs)))
    else:
        entropy=0.0

    vertical_lengths=[]
    for col in range(n):
        vertical_lengths.extend(_run_lengths(r[:,col]).tolist())
    qualifying_vertical=[v for v in vertical_lengths if v>=min_vertical]
    vertical_points=sum(qualifying_vertical)
    all_recurrences=int(r.sum())
    return {
        "recurrence_rate": float(recurrence_pairs/eligible_pairs) if eligible_pairs else 0.0,
        "determinism": float(diagonal_points/recurrence_pairs) if recurrence_pairs else 0.0,
        "mean_diagonal_length": float(np.mean(qualifying_diagonal)) if qualifying_diagonal else 0.0,
        "max_diagonal_length": int(max(qualifying_diagonal)) if qualifying_diagonal else 0,
        "divergence": float(1/max(qualifying_diagonal)) if qualifying_diagonal else 0.0,
        "diagonal_entropy": entropy,
        "laminarity": float(vertical_points/all_recurrences) if all_recurrences else 0.0,
        "trapping_time": float(np.mean(qualifying_vertical)) if qualifying_vertical else 0.0,
        "max_vertical_length": int(max(qualifying_vertical)) if qualifying_vertical else 0,
        "recurrence_pairs": recurrence_pairs,
        "eligible_pairs": eligible_pairs,
        "recurrence_matrix": r,
    }


def largest_lyapunov_rosenstein(series, *, dimension=3, delay=1, theiler=10,
                                max_horizon=20, fit_range=(1, 6), sampling_interval=1.0):
    """Estimate the largest Lyapunov exponent with the Rosenstein method.

    Nearest neighbours are selected in delay-coordinate space while excluding
    temporally adjacent points within theiler samples. Their trajectories are
    followed for max_horizon steps; the slope of mean log separation over the
    half-open fit_range is the exponent per unit time.
    """
    if not isinstance(theiler,int) or theiler<0:
        raise ValueError("theiler must be a non-negative integer")
    if not isinstance(max_horizon,int) or max_horizon<2:
        raise ValueError("max_horizon must be an integer >= 2")
    if not math.isfinite(sampling_interval) or sampling_interval<=0:
        raise ValueError("sampling_interval must be finite and positive")
    if len(fit_range)!=2 or not all(isinstance(v,int) for v in fit_range):
        raise ValueError("fit_range must be a pair of integer indices")
    fit_start,fit_stop=fit_range
    if fit_start<0 or fit_stop>max_horizon or fit_stop-fit_start<2:
        raise ValueError("fit_range must select at least two points within the divergence curve")
    points=_embedded(series,dimension,delay)
    usable=len(points)-max_horizon
    if usable<2:
        raise ValueError("series is too short for max_horizon")
    initial=np.linalg.norm(points[:usable,None,:]-points[None,:usable,:],axis=2)
    np.fill_diagonal(initial,np.inf)
    rows,cols=np.indices(initial.shape)
    initial[np.abs(rows-cols)<=theiler]=np.inf
    neighbours=np.argmin(initial,axis=1)
    distances=initial[np.arange(usable),neighbours]
    valid=np.isfinite(distances)&(distances>0)
    anchors=np.flatnonzero(valid)
    neighbours=neighbours[valid]
    if anchors.size<2:
        raise ValueError("fewer than two valid temporally separated nearest-neighbour pairs")
    curve=np.full(max_horizon+1,np.nan,dtype=float)
    counts=np.zeros(max_horizon+1,dtype=int)
    for step in range(max_horizon+1):
        separation=np.linalg.norm(points[anchors+step]-points[neighbours+step],axis=1)
        positive=separation>0
        if np.any(positive):
            curve[step]=float(np.mean(np.log(separation[positive])))
            counts[step]=int(np.count_nonzero(positive))
    selected=np.arange(fit_start,fit_stop)
    finite=np.isfinite(curve[selected])
    if np.count_nonzero(finite)<2:
        raise ValueError("fit range has fewer than two finite mean log-divergence values")
    slope,intercept=np.polyfit(selected[finite]*sampling_interval,curve[selected][finite],1)
    return {"exponent":float(slope),"intercept":float(intercept),
            "divergence_curve":curve,"pair_counts":counts,
            "anchor_indices":anchors,"neighbor_indices":neighbours,
            "fit_range":fit_range,"sampling_interval":float(sampling_interval)}

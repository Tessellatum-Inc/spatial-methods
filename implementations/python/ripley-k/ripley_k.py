"""Uncorrected and translation-corrected Ripley's K and L estimators."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite,pi
from typing import Sequence
import numpy as np

@dataclass(frozen=True)
class RipleyKResult:
    radii: np.ndarray
    k_values: np.ndarray
    l_values: np.ndarray

def ripley_k(points: Sequence[Sequence[float]]|np.ndarray, *, bounds: Sequence[float], radii: Sequence[float]|np.ndarray, edge_correction: str="none") -> RipleyKResult:
    """Return K(r) and L(r) for a rectangular planar window.

    edge_correction='none' uses the uncorrected ordered-pair estimator.
    'translation' weights each pair by window area / overlap area after
    translating the window by the pair displacement. Both use A/n^2.
    """
    events=np.asarray(points,dtype=float)
    if events.ndim!=2 or events.shape[1]!=2 or events.shape[0]<2:
        raise ValueError("points must contain at least two coordinate pairs")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")
    if len(bounds)!=4:
        raise ValueError("bounds must be (xmin, xmax, ymin, ymax)")
    xmin,xmax,ymin,ymax=map(float,bounds)
    if not all(isfinite(v) for v in (xmin,xmax,ymin,ymax)):
        raise ValueError("bounds must be finite")
    if not (xmin<xmax and ymin<ymax):
        raise ValueError("bounds must have positive width and height")
    if ((events[:,0]<xmin).any() or (events[:,0]>xmax).any() or (events[:,1]<ymin).any() or (events[:,1]>ymax).any()):
        raise ValueError("all point coordinates must lie inside bounds")
    if edge_correction not in ("none","translation"):
        raise ValueError("edge_correction must be 'none' or 'translation'")
    rs=np.asarray(radii,dtype=float)
    if rs.ndim!=1 or rs.size==0:
        raise ValueError("radii must be a non-empty one-dimensional sequence")
    if not np.isfinite(rs).all() or (rs<0).any():
        raise ValueError("radii must be finite and non-negative")
    n=events.shape[0]
    i,j=np.triu_indices(n,k=1)
    delta=events[j]-events[i]
    pair_distances=np.hypot(delta[:,0],delta[:,1])
    if edge_correction=="translation":
        width=xmax-xmin; height=ymax-ymin
        overlap=(width-np.abs(delta[:,0]))*(height-np.abs(delta[:,1]))
        if (overlap<=0).any():
            raise ValueError("translation correction is undefined for pairs with zero overlap area")
        pair_weights=(width*height)/overlap
    else:
        pair_weights=np.ones(pair_distances.shape,dtype=float)
    order=np.argsort(pair_distances,kind="stable")
    sorted_distances=pair_distances[order]
    cumulative_weights=np.cumsum(pair_weights[order])
    counts=np.searchsorted(sorted_distances,rs,side="right")
    area=(xmax-xmin)*(ymax-ymin)
    weighted_ordered_pairs=np.where(counts>0,2*cumulative_weights[np.maximum(counts-1,0)],0.0)
    k_values=(area/(n*n))*weighted_ordered_pairs
    l_values=np.sqrt(k_values/pi)
    return RipleyKResult(rs.copy(),k_values,l_values)


def inhomogeneous_ripley_k(
    points: Sequence[Sequence[float]] | np.ndarray,
    intensities: Sequence[float] | np.ndarray,
    *,
    bounds: Sequence[float],
    radii: Sequence[float] | np.ndarray,
    edge_correction: str = "translation",
) -> RipleyKResult:
    """Estimate inhomogeneous K from supplied positive event intensities.

    Uses the ordered-pair estimator
      K_inhom(r) = 1/A sum_{i != j} 1[d_ij <= r] /
                   (lambda_i lambda_j),
    optionally multiplied by rectangular-window translation weights A/overlap.
    Intensities must be in events per unit area. Supplying an estimated
    intensity surface is the caller's responsibility; estimation uncertainty
    and bandwidth selection are not included.
    """
    events = np.asarray(points, dtype=float)
    lam = np.asarray(intensities, dtype=float)
    if events.ndim != 2 or events.shape[1] != 2 or len(events) < 2:
        raise ValueError("points must contain at least two coordinate pairs")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")
    if lam.shape != (len(events),) or not np.isfinite(lam).all() or np.any(lam <= 0):
        raise ValueError("intensities must be positive finite values matching points")
    if len(bounds) != 4:
        raise ValueError("bounds must be (xmin, xmax, ymin, ymax)")
    xmin, xmax, ymin, ymax = map(float, bounds)
    if not all(isfinite(v) for v in (xmin, xmax, ymin, ymax)):
        raise ValueError("bounds must be finite")
    if not (xmin < xmax and ymin < ymax):
        raise ValueError("bounds must have positive width and height")
    if ((events[:, 0] < xmin).any() or (events[:, 0] > xmax).any()
            or (events[:, 1] < ymin).any() or (events[:, 1] > ymax).any()):
        raise ValueError("all point coordinates must lie inside bounds")
    if edge_correction not in ("none", "translation"):
        raise ValueError("edge_correction must be 'none' or 'translation'")
    rs = np.asarray(radii, dtype=float)
    if rs.ndim != 1 or rs.size == 0 or not np.isfinite(rs).all() or np.any(rs < 0):
        raise ValueError("radii must be a non-empty finite non-negative sequence")
    i, j = np.triu_indices(len(events), k=1)
    delta = events[j] - events[i]
    distances = np.hypot(delta[:, 0], delta[:, 1])
    pair_weights = 1.0 / (lam[i] * lam[j])
    area = (xmax - xmin) * (ymax - ymin)
    if edge_correction == "translation":
        overlap = ((xmax - xmin) - np.abs(delta[:, 0])) * (
            (ymax - ymin) - np.abs(delta[:, 1])
        )
        if np.any(overlap <= 0):
            raise ValueError("translation correction is undefined for pairs with zero overlap area")
        pair_weights *= area / overlap
    order = np.argsort(distances, kind="stable")
    sorted_distances = distances[order]
    cumulative = np.cumsum(pair_weights[order])
    counts = np.searchsorted(sorted_distances, rs, side="right")
    ordered_pair_sum = np.where(counts > 0, 2.0 * cumulative[np.maximum(counts - 1, 0)], 0.0)
    k_values = ordered_pair_sum / area
    return RipleyKResult(rs.copy(), k_values, np.sqrt(k_values / pi))

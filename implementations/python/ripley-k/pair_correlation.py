"""Translation-corrected pair-correlation g(r) for rectangular planar windows."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite, pi
from typing import Sequence
import numpy as np

@dataclass(frozen=True)
class PairCorrelationResult:
    radii: np.ndarray
    g_values: np.ndarray
    pair_counts: np.ndarray
    bin_edges: np.ndarray


def pair_correlation(points: Sequence[Sequence[float]] | np.ndarray, *,
                     bounds: Sequence[float],
                     bin_edges: Sequence[float] | np.ndarray,
                     edge_correction: str = "translation") -> PairCorrelationResult:
    """Estimate g(r) in annular bins using none or rectangular translation correction.

    Bounds follow the ripley_k package convention: (xmin, xmax, ymin, ymax).
    Bins are left-closed/right-open, except the final bin includes its upper
    edge. The estimator uses A/[n(n-1)] times the ordered-pair sum divided by
    annulus area. Pair counts are unordered and unweighted.
    """
    events = np.asarray(points, dtype=float)
    if events.ndim != 2 or events.shape[1] != 2 or events.shape[0] < 2:
        raise ValueError("points must contain at least two coordinate pairs")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")
    if len(bounds) != 4:
        raise ValueError("bounds must be (xmin, xmax, ymin, ymax)")
    xmin, xmax, ymin, ymax = map(float, bounds)
    if not all(isfinite(v) for v in (xmin, xmax, ymin, ymax)):
        raise ValueError("bounds must be finite")
    if not (xmin < xmax and ymin < ymax):
        raise ValueError("bounds must have positive width and height")
    if ((events[:, 0] < xmin).any() or (events[:, 0] > xmax).any()
            or (events[:, 1] < ymin).any() or (events[:, 1] > ymax).any()):
        raise ValueError("all points must lie inside bounds")
    if edge_correction not in ("none", "translation"):
        raise ValueError("edge_correction must be 'none' or 'translation'")
    edges = np.asarray(bin_edges, dtype=float)
    if (edges.ndim != 1 or edges.size < 2 or not np.isfinite(edges).all()
            or (edges < 0).any() or np.any(np.diff(edges) <= 0)):
        raise ValueError("bin_edges must be finite, nonnegative and strictly increasing")

    n = events.shape[0]
    i, j = np.triu_indices(n, k=1)
    delta = events[j] - events[i]
    distances = np.hypot(delta[:, 0], delta[:, 1])
    area = (xmax - xmin) * (ymax - ymin)
    if edge_correction == "translation":
        overlap = ((xmax - xmin - np.abs(delta[:, 0]))
                   * (ymax - ymin - np.abs(delta[:, 1])))
        if (overlap <= 0).any():
            raise ValueError("translation correction is undefined for zero-overlap pairs")
        weights = area / overlap
    else:
        weights = np.ones(distances.shape, dtype=float)

    weighted_pairs, _ = np.histogram(distances, bins=edges, weights=weights)
    pair_counts, _ = np.histogram(distances, bins=edges)
    annulus_areas = pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    k_increments = (2.0 * area / (n * (n - 1))) * weighted_pairs
    g_values = k_increments / annulus_areas
    radii = (edges[:-1] + edges[1:]) / 2.0
    return PairCorrelationResult(radii, g_values, pair_counts, edges.copy())

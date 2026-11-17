"""Small, explicit spatial outlier diagnostics for projected coordinates."""
from __future__ import annotations

import numpy as np


def _matrix(values, name="values"):
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 1:
        raise ValueError(f"{name} must be a 2-D array with at least two rows")
    if not np.isfinite(x).all():
        raise ValueError(f"{name} must contain only finite values")
    return x


def z_scores(values):
    """Column-wise population-standardised scores; constant columns return 0."""
    x = np.asarray(values, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    x = _matrix(x)
    sd = x.std(axis=0, ddof=0)
    out = np.zeros_like(x)
    np.divide(x - x.mean(axis=0), sd, out=out, where=sd > 0)
    return out[:, 0] if np.asarray(values).ndim == 1 else out


def spatial_scatter_data(values, weights):
    """Return (observed, spatial_lag) for a row-standardised weights matrix."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size < 2 or not np.isfinite(x).all():
        raise ValueError("values must be a finite 1-D array with at least two entries")
    w = np.asarray(weights, dtype=float)
    if w.shape != (x.size, x.size) or not np.isfinite(w).all() or (w < 0).any():
        raise ValueError("weights must be a finite, non-negative square matrix matching values")
    if not np.allclose(np.diag(w), 0):
        raise ValueError("weights diagonal must be zero")
    rows = w.sum(axis=1)
    wr = np.zeros_like(w)
    np.divide(w, rows[:, None], out=wr, where=rows[:, None] > 0)
    centered = x - x.mean()
    return centered, wr @ centered


def variogram_cloud(coordinates, values):
    """Return pair distances and semivariances for all unique point pairs."""
    xy = _matrix(coordinates, "coordinates")
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or y.size != xy.shape[0] or not np.isfinite(y).all():
        raise ValueError("values must be finite 1-D data matching coordinates")
    i, j = np.triu_indices(y.size, k=1)
    distance = np.linalg.norm(xy[i] - xy[j], axis=1)
    gamma = 0.5 * (y[i] - y[j]) ** 2
    return distance, gamma


def local_outlier_factor(features, k=5):
    """Brute-force Euclidean LOF; returns 1 for locally uniform observations."""
    x = _matrix(features, "features")
    n = x.shape[0]
    if not isinstance(k, (int, np.integer)) or k < 1 or k >= n:
        raise ValueError("k must be an integer in [1, n_samples - 1]")
    d = np.linalg.norm(x[:, None, :] - x[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    neighbours = np.argsort(d, axis=1, kind="stable")[:, :k]
    kdist = np.take_along_axis(d, neighbours[:, -1, None], axis=1).ravel()
    reach = np.maximum(d[np.arange(n)[:, None], neighbours], kdist[neighbours])
    lrd = 1.0 / np.maximum(reach.mean(axis=1), np.finfo(float).tiny)
    return np.mean(lrd[neighbours], axis=1) / lrd


def geographically_weighted_scores(coordinates, values, radius):
    """Distance-weighted local deviation from neighbouring values, excluding self."""
    xy = _matrix(coordinates, "coordinates")
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or y.size != xy.shape[0] or not np.isfinite(y).all():
        raise ValueError("values must be finite 1-D data matching coordinates")
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("radius must be finite and positive")
    d = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=2)
    weights = np.exp(-0.5 * (d / radius) ** 2)
    np.fill_diagonal(weights, 0.0)
    sums = weights.sum(axis=1)
    if np.any(sums <= np.finfo(float).tiny):
        raise ValueError("each observation needs at least one effective neighbour")
    mean = (weights @ y) / sums
    variance = (weights @ ((y[None, :] - mean[:, None]) ** 2)) / sums
    scale = np.sqrt(variance)
    # A perfectly constant neighbourhood has zero local variance. Fall back
    # to the global population scale so a genuine local spike is not hidden.
    fallback = float(y.std(ddof=0))
    scale = np.where(scale > np.finfo(float).eps, scale, fallback)
    score = np.zeros_like(y)
    np.divide(y - mean, scale, out=score, where=scale > np.finfo(float).eps)
    return score

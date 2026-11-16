"""Planar spatial and space-time Gaussian kernel intensity estimators."""
from __future__ import annotations
import numpy as np


def _points(value, name):
    a = np.asarray(value, dtype=float)
    if a.ndim != 2 or a.shape[1] != 2 or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite N-by-2 coordinate array")
    return a


def _weights(value, n):
    if value is None:
        return np.ones(n, dtype=float)
    w = np.asarray(value, dtype=float)
    if w.shape != (n,) or not np.all(np.isfinite(w)) or np.any(w < 0):
        raise ValueError("weights must be finite, nonnegative and match event count")
    return w


def gaussian_spatial_intensity(events, query, bandwidth, weights=None):
    """Estimate planar event intensity (events per squared coordinate unit).

    This is an unnormalised point-process intensity estimate: event weights are
    summed, not divided by their total. Coordinates must use a planar metric CRS.
    """
    x = _points(events, "events")
    q = _points(query, "query")
    if x.shape[0] == 0:
        raise ValueError("events must contain at least one point")
    if not np.isfinite(bandwidth) or bandwidth <= 0:
        raise ValueError("bandwidth must be positive and finite")
    w = _weights(weights, x.shape[0])
    delta = q[:, None, :] - x[None, :, :]
    d2 = np.sum(delta * delta, axis=2)
    h2 = float(bandwidth) ** 2
    kernel = np.exp(-0.5 * d2 / h2) / (2.0 * np.pi * h2)
    return kernel @ w


def gaussian_spacetime_intensity(events, event_times, query, query_times,
                                 spatial_bandwidth, temporal_bandwidth,
                                 weights=None):
    """Product-kernel space-time intensity (events per area per time unit)."""
    x = _points(events, "events")
    q = _points(query, "query")
    t = np.asarray(event_times, dtype=float)
    tq = np.asarray(query_times, dtype=float)
    if x.shape[0] == 0 or t.shape != (x.shape[0],) or not np.all(np.isfinite(t)):
        raise ValueError("event_times must be finite and match nonempty events")
    if tq.ndim != 1 or tq.size != q.shape[0] or not np.all(np.isfinite(tq)):
        raise ValueError("query_times must be finite and match query locations")
    if not np.isfinite(spatial_bandwidth) or spatial_bandwidth <= 0:
        raise ValueError("spatial_bandwidth must be positive and finite")
    if not np.isfinite(temporal_bandwidth) or temporal_bandwidth <= 0:
        raise ValueError("temporal_bandwidth must be positive and finite")
    w = _weights(weights, x.shape[0])
    spatial_delta = q[:, None, :] - x[None, :, :]
    spatial_d2 = np.sum(spatial_delta * spatial_delta, axis=2)
    time_delta = tq[:, None] - t[None, :]
    hs2 = float(spatial_bandwidth) ** 2
    ht2 = float(temporal_bandwidth) ** 2
    spatial = np.exp(-0.5 * spatial_d2 / hs2) / (2.0 * np.pi * hs2)
    temporal = np.exp(-0.5 * time_delta * time_delta / ht2) / (np.sqrt(2.0 * np.pi) * temporal_bandwidth)
    return (spatial * temporal) @ w

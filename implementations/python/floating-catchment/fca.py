"""Two-step floating catchment accessibility models."""
from __future__ import annotations
import numpy as np


def _inputs(distance, demand, supply):
    d = np.asarray(distance, dtype=float)
    p = np.asarray(demand, dtype=float)
    s = np.asarray(supply, dtype=float)
    if d.ndim != 2 or p.ndim != 1 or s.ndim != 1 or d.shape != (len(p), len(s)):
        raise ValueError("distance must have shape (n_demand, n_supply)")
    if not (np.all(np.isfinite(d)) and np.all(np.isfinite(p)) and np.all(np.isfinite(s))):
        raise ValueError("inputs must be finite")
    if np.any(d < 0) or np.any(p < 0) or np.any(s < 0):
        raise ValueError("distances, demand and supply must be non-negative")
    return d, p, s


def _access(distance, demand, supply, weights):
    n, m = distance.shape
    ratios = np.zeros(m, dtype=float)
    for j in range(m):
        denominator = float(np.sum(demand * weights[:, j]))
        if denominator > 0:
            ratios[j] = supply[j] / denominator
    access = np.sum(weights * ratios[None, :], axis=1) if m else np.zeros(n)
    return access, ratios


def two_step_fca(distance, demand, supply, catchment_radius):
    """Uniform 2SFCA accessibility with a closed distance threshold.

    distance[i,j] is the network or Euclidean distance from demand location i
    to supply location j. Demand and supply must share compatible units.
    """
    d, p, s = _inputs(distance, demand, supply)
    radius = float(catchment_radius)
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("catchment_radius must be finite and positive")
    weights = (d <= radius).astype(float)
    access, ratios = _access(d, p, s, weights)
    return {"accessibility": access, "supply_demand_ratios": ratios,
            "catchment_weights": weights, "method": "2SFCA"}


def enhanced_two_step_fca(distance, demand, supply, distance_breaks, zone_weights):
    """E2SFCA with explicit increasing upper bounds and zone weights.

    distance_breaks define inclusive upper bounds for successive distance
    zones. A pair beyond the last bound receives zero weight. Weights must be
    finite, non-negative and match the number of breaks.
    """
    d, p, s = _inputs(distance, demand, supply)
    breaks = np.asarray(distance_breaks, dtype=float)
    weights_by_zone = np.asarray(zone_weights, dtype=float)
    if breaks.ndim != 1 or breaks.size == 0 or not np.all(np.isfinite(breaks)):
        raise ValueError("distance_breaks must be a non-empty finite vector")
    if np.any(breaks <= 0) or np.any(np.diff(breaks) <= 0):
        raise ValueError("distance_breaks must be positive and strictly increasing")
    if weights_by_zone.shape != breaks.shape or not np.all(np.isfinite(weights_by_zone)):
        raise ValueError("zone_weights must be finite and match distance_breaks")
    if np.any(weights_by_zone < 0) or not np.any(weights_by_zone > 0):
        raise ValueError("zone_weights must be non-negative and at least one positive")
    weights = np.zeros_like(d)
    lower = 0.0
    for upper, weight in zip(breaks, weights_by_zone):
        zone = (d > lower) & (d <= upper)
        if lower == 0:
            zone |= d == 0
        weights[zone] = weight
        lower = float(upper)
    access, ratios = _access(d, p, s, weights)
    return {"accessibility": access, "supply_demand_ratios": ratios,
            "catchment_weights": weights, "method": "E2SFCA"}

def gaussian_decay(distance, scale):
    """Gaussian travel-time decay exp(-0.5 * (distance / scale)^2)."""
    d = np.asarray(distance, dtype=float)
    s = float(scale)
    if not np.all(np.isfinite(d)) or np.any(d < 0):
        raise ValueError("distance must be finite and non-negative")
    if not np.isfinite(s) or s <= 0:
        raise ValueError("scale must be finite and positive")
    return np.exp(-0.5 * (d / s) ** 2)


def power_decay(distance, scale, exponent):
    """Regularised power decay (1 + distance / scale)^(-exponent)."""
    d = np.asarray(distance, dtype=float)
    s, beta = float(scale), float(exponent)
    if not np.all(np.isfinite(d)) or np.any(d < 0):
        raise ValueError("distance must be finite and non-negative")
    if not np.isfinite(s) or s <= 0 or not np.isfinite(beta) or beta <= 0:
        raise ValueError("scale and exponent must be finite and positive")
    return (1.0 + d / s) ** (-beta)


def epanechnikov_decay(distance, bandwidth):
    """Compact-support quadratic kernel max(0, 1 - (distance / h)^2)."""
    d = np.asarray(distance, dtype=float)
    h = float(bandwidth)
    if not np.all(np.isfinite(d)) or np.any(d < 0):
        raise ValueError("distance must be finite and non-negative")
    if not np.isfinite(h) or h <= 0:
        raise ValueError("bandwidth must be finite and positive")
    u = d / h
    return np.where(u < 1.0, 1.0 - u * u, 0.0)

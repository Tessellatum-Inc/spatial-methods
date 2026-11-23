"""Longitudinal channel profile and slope-area morphometry."""
from __future__ import annotations
import numpy as np


def chi_coordinate(distance, drainage_area, *, reference_area, concavity=0.45):
    """Compute the channel chi coordinate by trapezoidal integration.

    chi(x) = integral (A0/A(x))**concavity dx. Distance must increase
    downstream/upstream consistently along one channel and drainage area
    must be positive. The first chi value is zero.
    """
    x, area = np.asarray(distance, float), np.asarray(drainage_area, float)
    try:
        a0, theta = float(reference_area), float(concavity)
    except (TypeError, ValueError):
        raise ValueError("reference_area and concavity must be finite and positive") from None
    if x.ndim != 1 or area.shape != x.shape or x.size < 2:
        raise ValueError("distance and drainage_area must be matching 1D arrays with at least two values")
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(area)) or np.any(area <= 0):
        raise ValueError("distance and drainage_area must be finite; area must be positive")
    if np.any(np.diff(x) <= 0):
        raise ValueError("distance must be strictly increasing")
    if not np.isfinite(a0) or a0 <= 0 or not np.isfinite(theta) or theta <= 0:
        raise ValueError("reference_area and concavity must be finite and positive")
    integrand = (a0 / area) ** theta
    increments = 0.5 * (integrand[1:] + integrand[:-1]) * np.diff(x)
    return np.concatenate(([0.0], np.cumsum(increments)))


def slope_area_relationship(distance, elevation, drainage_area, *, min_slope=1e-8):
    """Fit log10(channel slope) = intercept + exponent*log10(area).

    Returns the area exponent (normally negative), channel steepness
    coefficient, R-squared and pointwise slope. This is descriptive OLS,
    not a tectonic/uplift inversion or a segmented channel analysis.
    """
    x, z, area = map(lambda v: np.asarray(v, float), (distance, elevation, drainage_area))
    if x.ndim != 1 or z.shape != x.shape or area.shape != x.shape or x.size < 3:
        raise ValueError("distance, elevation and area must be matching 1D arrays with at least three values")
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(z)) or np.any(~np.isfinite(area)):
        raise ValueError("inputs must be finite")
    if np.any(np.diff(x) <= 0) or np.any(area <= 0):
        raise ValueError("distance must increase and drainage area must be positive")
    try:
        floor = float(min_slope)
    except (TypeError, ValueError):
        raise ValueError("min_slope must be finite and positive") from None
    if not np.isfinite(floor) or floor <= 0:
        raise ValueError("min_slope must be finite and positive")
    slope = np.abs(np.diff(z) / np.diff(x))
    local_area = 0.5 * (area[:-1] + area[1:])
    valid = np.isfinite(slope) & (slope > floor) & (local_area > 0)
    if np.count_nonzero(valid) < 2:
        raise ValueError("at least two positive-slope segments are required")
    lx, ly = np.log10(local_area[valid]), np.log10(slope[valid])
    exponent, intercept = np.polyfit(lx, ly, 1)
    predicted = intercept + exponent * lx
    ss_res = float(np.sum((ly - predicted) ** 2))
    ss_tot = float(np.sum((ly - ly.mean()) ** 2))
    r2 = 1.0 if ss_tot == 0 and ss_res == 0 else (float("nan") if ss_tot == 0 else 1 - ss_res / ss_tot)
    return {"area_exponent": float(exponent), "channel_steepness": float(10 ** intercept),
            "r_squared": r2, "segment_slope": slope, "segment_area": local_area}


def detect_knickpoints(distance, elevation, *, window_size=5, min_relief=0.0):
    """Detect profile departures from a local endpoint chord.

    For each complete odd window, fit the straight chord joining its end
    elevations and measure the centre's signed residual. Positive residuals
    are convex-up departures and negative residuals concave-up departures
    under the supplied distance/elevation ordering. The absolute residual
    must meet min_relief. Adjacent detections are retained independently.
    """
    x, z = np.asarray(distance, float), np.asarray(elevation, float)
    if x.ndim != 1 or z.shape != x.shape or x.size < 3:
        raise ValueError("distance and elevation must be matching 1D arrays with at least three values")
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(z)) or np.any(np.diff(x) <= 0):
        raise ValueError("distance/elevation must be finite and distance strictly increasing")
    if isinstance(window_size, (bool, np.bool_)) or not isinstance(window_size, (int, np.integer)) or window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer of at least 3")
    try:
        threshold = float(min_relief)
    except (TypeError, ValueError):
        raise ValueError("min_relief must be finite and non-negative") from None
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError("min_relief must be finite and non-negative")
    radius = window_size // 2
    residual = np.full(z.shape, np.nan)
    for i in range(radius, z.size - radius):
        left, right = i - radius, i + radius
        fraction = (x[i] - x[left]) / (x[right] - x[left])
        chord = z[left] + fraction * (z[right] - z[left])
        residual[i] = z[i] - chord
    detected = np.isfinite(residual) & (np.abs(residual) >= threshold) & (np.abs(residual) > 0)
    kind = np.full(z.shape, "", dtype="<U12")
    kind[detected & (residual > 0)] = "convex-up"
    kind[detected & (residual < 0)] = "concave-up"
    return {"knickpoint": detected, "residual": residual, "kind": kind}

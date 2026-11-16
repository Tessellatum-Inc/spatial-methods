"""Per-pixel rainfall-adjusted NDVI residual trend screening (RESTREND)."""
from __future__ import annotations
import numpy as np
from scipy.stats import linregress


def resttrend(ndvi, precipitation, years, *, min_observations=6):
    """Fit NDVI~precipitation and trend residuals independently per pixel.

    ndvi and precipitation have shape (time, rows, cols) or (time, pixels).
    Years are numeric and strictly increasing. Missing pairs are omitted per
    pixel; pixels below min_observations retain NaN diagnostics.
    """
    y = np.asarray(ndvi, dtype=float)
    p = np.asarray(precipitation, dtype=float)
    t = np.asarray(years, dtype=float)
    if y.ndim not in (2, 3) or p.shape != y.shape or y.shape[0] != len(t):
        raise ValueError("ndvi and precipitation must share (time, pixels) or (time, rows, cols) shape")
    if t.ndim != 1 or len(t) < 3 or not np.all(np.isfinite(t)) or np.any(np.diff(t) <= 0):
        raise ValueError("years must be a finite strictly increasing vector")
    if np.any(np.isinf(y)) or np.any(np.isinf(p)):
        raise ValueError("NDVI and precipitation may contain NaN but not infinity")
    if isinstance(min_observations, (bool, np.bool_)) or not isinstance(min_observations, (int, np.integer)) or min_observations < 3:
        raise ValueError("min_observations must be an integer of at least three")
    spatial_shape = y.shape[1:]
    yf = y.reshape(len(t), -1)
    pf = p.reshape(len(t), -1)
    n_pixels = yf.shape[1]
    outputs = {name: np.full(n_pixels, np.nan) for name in
               ("rainfall_intercept", "rainfall_sensitivity", "residual_trend",
                "residual_intercept", "residual_r_squared", "residual_p_value")}
    counts = np.zeros(n_pixels, dtype=np.int32)
    residuals = np.full_like(yf, np.nan)
    for pixel in range(n_pixels):
        valid = np.isfinite(yf[:, pixel]) & np.isfinite(pf[:, pixel])
        n = int(valid.sum())
        counts[pixel] = n
        if n < min_observations or np.ptp(pf[valid, pixel]) <= np.finfo(float).eps:
            continue
        slope, intercept = np.polyfit(pf[valid, pixel], yf[valid, pixel], 1)
        residual = yf[valid, pixel] - (intercept + slope*pf[valid, pixel])
        residuals[valid, pixel] = residual
        trend = linregress(t[valid], residual)
        outputs["rainfall_intercept"][pixel] = intercept
        outputs["rainfall_sensitivity"][pixel] = slope
        outputs["residual_trend"][pixel] = trend.slope
        outputs["residual_intercept"][pixel] = trend.intercept
        outputs["residual_r_squared"][pixel] = trend.rvalue**2
        outputs["residual_p_value"][pixel] = trend.pvalue
    return {**{k: v.reshape(spatial_shape) for k, v in outputs.items()},
            "residuals": residuals.reshape(y.shape),
            "n_observations": counts.reshape(spatial_shape)}

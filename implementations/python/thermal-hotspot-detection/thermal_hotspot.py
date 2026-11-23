"""Robust local-context thermal anomaly screening."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import generic_filter


def _nanmedian(values):
    valid = values[np.isfinite(values)]
    return float(np.median(valid)) if valid.size else np.nan


def detect_thermal_hotspots(temperature, *, absolute_threshold,
                            min_local_excess=5.0, mad_multiplier=3.0,
                            window_size=9):
    """Flag hot pixels by absolute threshold and robust local median/MAD excess.

    Temperature units are caller-defined but must be consistent. The method
    returns a Boolean mask and diagnostic local-background, MAD and excess
    arrays. NaN cells are excluded and remain unclassified.
    """
    data = np.asarray(temperature, dtype=float)
    if data.ndim != 2 or data.size == 0 or not np.any(np.isfinite(data)):
        raise ValueError("temperature must be a nonempty 2-D array with finite observations")
    if not np.isfinite(absolute_threshold):
        raise ValueError("absolute_threshold must be finite")
    if not np.isfinite(min_local_excess) or min_local_excess < 0:
        raise ValueError("min_local_excess must be finite and nonnegative")
    if not np.isfinite(mad_multiplier) or mad_multiplier < 0:
        raise ValueError("mad_multiplier must be finite and nonnegative")
    if not isinstance(window_size, int) or isinstance(window_size, bool) or window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer >= 3")
    background = generic_filter(data, _nanmedian, size=window_size, mode="nearest")
    residual = np.abs(data - background)
    local_mad = generic_filter(residual, _nanmedian, size=window_size, mode="nearest")
    excess = data - background
    threshold = np.maximum(min_local_excess, mad_multiplier * 1.4826 * local_mad)
    hotspots = np.isfinite(data) & np.isfinite(background) & (data >= absolute_threshold) & (excess >= threshold)
    return {"hotspots": hotspots, "background": background,
            "local_mad": local_mad, "excess": excess}

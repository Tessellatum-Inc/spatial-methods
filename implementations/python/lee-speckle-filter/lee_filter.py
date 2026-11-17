"""Adaptive Lee filtering for non-negative SAR intensity rasters."""
import numpy as np


def _box_sum(array, radius):
    h, w = array.shape
    integral = np.pad(array, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    rows, cols = np.arange(h), np.arange(w)
    r0, r1 = np.maximum(rows-radius, 0), np.minimum(rows+radius+1, h)
    c0, c1 = np.maximum(cols-radius, 0), np.minimum(cols+radius+1, w)
    return (integral[r1[:, None], c1[None, :]]
            - integral[r0[:, None], c1[None, :]]
            - integral[r1[:, None], c0[None, :]]
            + integral[r0[:, None], c0[None, :]])


def lee_filter(intensity, window_size=5, equivalent_looks=1.0):
    """Filter a 2D SAR intensity image with a local multiplicative-noise model.

    NaNs are NoData. Neighbourhoods are clipped at image boundaries.
    Equivalent number of looks (ENL) is an explicit model assumption.
    """
    image = np.asarray(intensity, dtype=float)
    if image.ndim != 2 or not image.size:
        raise ValueError("intensity must be a non-empty 2D array")
    if np.isinf(image).any():
        raise ValueError("intensity may contain NaN NoData but not infinity")
    valid = np.isfinite(image)
    if np.any(image[valid] < 0):
        raise ValueError("intensity values must be non-negative")
    if isinstance(window_size, bool) or not isinstance(window_size, (int, np.integer)):
        raise ValueError("window_size must be an odd integer >= 3")
    if window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer >= 3")
    if not np.isfinite(equivalent_looks) or equivalent_looks <= 0:
        raise ValueError("equivalent_looks must be positive and finite")
    radius = window_size // 2
    values = np.where(valid, image, 0.0)
    counts = _box_sum(valid.astype(float), radius)
    sums = _box_sum(values, radius)
    squares = _box_sum(values * values, radius)
    mean = np.divide(sums, counts, out=np.zeros_like(sums), where=counts > 0)
    second = np.divide(squares, counts, out=np.zeros_like(squares), where=counts > 0)
    variance = np.maximum(second - mean * mean, 0.0)
    noise = mean * mean / float(equivalent_looks)
    signal = np.maximum(variance - noise, 0.0)
    weight = np.divide(signal, variance, out=np.zeros_like(variance), where=variance > 0)
    result = mean + weight * (np.where(valid, image, mean) - mean)
    result[(counts == 0) | (~valid)] = np.nan
    return result

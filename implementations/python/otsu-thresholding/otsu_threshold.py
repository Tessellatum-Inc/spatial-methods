"""Exact observed-level, two-class Otsu thresholding."""
import numpy as np


def otsu_threshold(image, *, mask=None):
    """Return midpoint threshold maximising weighted between-class variance.

    Non-finite and masked pixels are excluded. A constant valid image returns
    its sole value. Uses sorted unique values: O(n log n) time, O(n) memory.
    """
    values = np.asarray(image, dtype=float)
    if values.size == 0:
        raise ValueError("image must not be empty")
    valid = np.isfinite(values)
    if mask is not None:
        include = np.asarray(mask)
        if include.shape != values.shape:
            raise ValueError("mask shape must match image")
        if include.dtype != np.bool_:
            raise TypeError("mask must be boolean")
        valid &= include
    samples = values[valid]
    if samples.size == 0:
        raise ValueError("no finite, unmasked pixels")
    levels, counts = np.unique(samples, return_counts=True)
    if levels.size == 1:
        return float(levels[0])
    counts = counts.astype(float)
    n = float(samples.size)
    cumulative_n = np.cumsum(counts)[:-1]
    cumulative_sum = np.cumsum(counts * levels)[:-1]
    total_sum = float(np.dot(counts, levels))
    w0 = cumulative_n / n
    w1 = 1.0 - w0
    m0 = cumulative_sum / cumulative_n
    m1 = (total_sum - cumulative_sum) / (n - cumulative_n)
    score = w0 * w1 * (m0 - m1) ** 2
    i = int(np.argmax(score))
    return float((levels[i] + levels[i + 1]) / 2.0)


def otsu_binarize(image, *, mask=None):
    """Return (threshold, foreground); foreground means intensity > threshold."""
    values = np.asarray(image, dtype=float)
    threshold = otsu_threshold(values, mask=mask)
    valid = np.isfinite(values)
    if mask is not None:
        include = np.asarray(mask)
        if include.shape != values.shape:
            raise ValueError("mask shape must match image")
        if include.dtype != np.bool_:
            raise TypeError("mask must be boolean")
        valid &= include
    return threshold, valid & (values > threshold)

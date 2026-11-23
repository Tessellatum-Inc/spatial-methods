"""Refined Lee-style local speckle suppression for 2-D intensity images.

This is a scalar-intensity Lee filter, not a polarimetric or multichannel
Refined Lee implementation. The caller supplies noise variance explicitly.
"""
import numpy as np


def lee_filter(image, noise_variance, window_size=3, *, min_valid=1):
    """Apply the local-statistics Lee filter to a 2-D array.

    For each valid centre pixel z, compute local mean m and sample variance s²
    over valid pixels in an odd square window. Estimate the local signal
    variance as max(s² - noise_variance, 0), set gain
    W = signal_variance / max(s², noise_variance), and return
    m + W * (z - m). NaN pixels are ignored in neighbourhood statistics and
    remain NaN in the output. Borders use edge replication.

    The filter assumes additive, locally stationary noise variance. For
    multiplicative SAR intensity, estimate/transform the noise model before
    using this pedagogical baseline; it is not a substitute for calibrated
    sensor-specific or polarimetric speckle filtering.
    """
    data = np.asarray(image, dtype=float)
    if data.ndim != 2 or not data.size:
        raise ValueError("image must be a non-empty 2-D array")
    if not np.isfinite(noise_variance) or noise_variance < 0:
        raise ValueError("noise_variance must be finite and non-negative")
    if not isinstance(window_size, int) or isinstance(window_size, bool) or window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer >= 3")
    if not isinstance(min_valid, int) or isinstance(min_valid, bool) or not 1 <= min_valid <= window_size**2:
        raise ValueError("min_valid must be between 1 and window_size squared")

    valid = np.isfinite(data)
    values = np.where(valid, data, 0.0)
    radius = window_size // 2
    padded_values = np.pad(values, radius, mode="edge")
    padded_valid = np.pad(valid.astype(float), radius, mode="edge")
    out = np.full(data.shape, np.nan, dtype=float)

    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            if not valid[row, col]:
                continue
            block = padded_values[row:row+window_size, col:col+window_size]
            mask = padded_valid[row:row+window_size, col:col+window_size]
            count = int(mask.sum())
            if count < min_valid:
                out[row, col] = data[row, col]
                continue
            mean = float(block.sum() / count)
            centered = np.where(mask > 0, block - mean, 0.0)
            variance = float((centered * centered).sum() / max(count - 1, 1))
            signal_variance = max(variance - noise_variance, 0.0)
            gain = signal_variance / max(variance, noise_variance, np.finfo(float).eps)
            out[row, col] = mean + gain * (data[row, col] - mean)
    return out

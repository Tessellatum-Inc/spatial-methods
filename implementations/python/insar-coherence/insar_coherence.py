"""Local interferometric coherence baselines for coregistered complex SLC data."""
from __future__ import annotations

import math
import numpy as np


def _complex_image(values, name):
    try:
        image = np.asarray(values, dtype=np.complex128)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a numeric 2D complex image") from exc
    if image.ndim != 2 or min(image.shape) < 1:
        raise ValueError(f"{name} must be a non-empty 2D image")
    if not np.isfinite(image.real).all() or not np.isfinite(image.imag).all():
        raise ValueError(f"{name} must contain finite values")
    return image


def local_interferometric_coherence(master, slave, *, window_size=5, min_power=0.0):
    """Estimate magnitude coherence over valid square moving windows.

    gamma = |sum(master * conj(slave))| /
             sqrt(sum(|master|^2) * sum(|slave|^2)).

    No padding is applied, so output shape is (H-w+1, W-w+1). The function
    assumes accurately coregistered complex SLC arrays on the same grid.
    Windows with either mean power at or below min_power are returned as NaN.
    """
    m = _complex_image(master, "master")
    s = _complex_image(slave, "slave")
    if m.shape != s.shape:
        raise ValueError("master and slave images must have equal shape")
    if isinstance(window_size, (bool, np.bool_)) or not isinstance(window_size, (int, np.integer)):
        raise ValueError("window_size must be an odd positive integer")
    if window_size < 1 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd positive integer")
    if window_size > min(m.shape):
        raise ValueError("window_size must not exceed either image dimension")
    if isinstance(min_power, (bool, np.bool_)):
        raise ValueError("min_power must be finite and non-negative")
    try:
        threshold = float(min_power)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("min_power must be finite and non-negative") from exc
    if not math.isfinite(threshold) or threshold < 0:
        raise ValueError("min_power must be finite and non-negative")

    height, width = m.shape
    out = np.full((height-window_size+1, width-window_size+1), np.nan, dtype=float)
    for row in range(out.shape[0]):
        for col in range(out.shape[1]):
            a = m[row:row+window_size, col:col+window_size]
            b = s[row:row+window_size, col:col+window_size]
            cross = np.mean(a * np.conjugate(b))
            power_a = float(np.mean(np.abs(a) ** 2))
            power_b = float(np.mean(np.abs(b) ** 2))
            if power_a <= threshold or power_b <= threshold:
                continue
            out[row, col] = np.clip(abs(cross) / math.sqrt(power_a * power_b), 0.0, 1.0)
    return out


def coherence_change(before, after):
    """Return signed after-minus-before coherence change for aligned maps."""
    try:
        a = np.asarray(before, dtype=float)
        b = np.asarray(after, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("coherence maps must be numeric 2D arrays") from exc
    if a.ndim != 2 or a.shape != b.shape or min(a.shape) < 1:
        raise ValueError("coherence maps must be non-empty 2D arrays of equal shape")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("coherence maps must contain finite values")
    if np.any((a < 0) | (a > 1) | (b < 0) | (b > 1)):
        raise ValueError("coherence values must lie in [0, 1]")
    return b - a

"""Exact Euclidean raster distance transform via lower envelopes of parabolas."""
from __future__ import annotations

from math import isfinite
from typing import Sequence

import numpy as np


def distance_transform_1d(values: np.ndarray, spacing: float = 1.0) -> np.ndarray:
    """Compute min_i(values[i] + (spacing * (q-i))**2) for every q in O(n).

    Values may be finite or positive infinity. Infinite entries do not
    contribute candidate parabolas. This is the Felzenszwalb-Huttenlocher
    lower-envelope algorithm for the squared Euclidean distance transform.
    """
    f = np.asarray(values, dtype=float)
    if f.ndim != 1 or f.size == 0:
        raise ValueError("values must be a non-empty one-dimensional array")
    if np.any(np.isnan(f)) or np.any(np.isneginf(f)):
        raise ValueError("values must be finite or positive infinity")
    spacing = float(spacing)
    if not isfinite(spacing) or spacing <= 0:
        raise ValueError("spacing must be finite and greater than zero")

    n = f.size
    candidates = np.flatnonzero(np.isfinite(f))
    if candidates.size == 0:
        return np.full(n, np.inf)
    weight = spacing * spacing

    # v stores parabola centres in the lower envelope; z stores their
    # intersection coordinates, in increasing order.
    v = np.empty(candidates.size, dtype=int)
    z = np.empty(candidates.size + 1, dtype=float)
    k = 0
    v[0] = candidates[0]
    z[0] = -np.inf
    z[1] = np.inf

    for q in candidates[1:]:
        q = int(q)
        while True:
            p = v[k]
            intersection = ((f[q] + weight * q * q)
                            - (f[p] + weight * p * p)) / (2.0 * weight * (q - p))
            if intersection > z[k] or k == 0:
                break
            k -= 1
        k += 1
        v[k] = q
        z[k] = intersection
        z[k + 1] = np.inf

    envelope_size = k + 1
    output = np.empty(n, dtype=float)
    k = 0
    for q in range(n):
        while k + 1 < envelope_size and z[k + 1] < q:
            k += 1
        delta = q - v[k]
        output[q] = f[v[k]] + weight * delta * delta
    return output


def distance_to_targets(
    target_mask: np.ndarray,
    *,
    cell_size: Sequence[float] = (1.0, 1.0),
) -> np.ndarray:
    """Return centre-to-centre Euclidean distance to the nearest True cell.

    Uses two separable one-dimensional lower-envelope passes. cell_size is
    ordered (row_spacing, column_spacing), in map units.
    """
    mask = np.asarray(target_mask, dtype=bool)
    if mask.ndim != 2 or mask.size == 0:
        raise ValueError("target_mask must be a non-empty 2D array")
    try:
        if len(cell_size) != 2:
            raise ValueError("cell_size must contain row and column spacing")
        row_spacing, column_spacing = map(float, cell_size)
    except TypeError as exc:
        raise ValueError("cell_size must contain row and column spacing") from exc
    if not all(isfinite(value) and value > 0 for value in (row_spacing, column_spacing)):
        raise ValueError("cell_size values must be finite and greater than zero")
    if not mask.any():
        raise ValueError("target_mask must contain at least one target cell")

    height, width = mask.shape
    initial = np.where(mask, 0.0, np.inf)
    horizontal = np.empty((height, width), dtype=float)
    for row in range(height):
        horizontal[row, :] = distance_transform_1d(initial[row, :], column_spacing)

    squared = np.empty((height, width), dtype=float)
    for column in range(width):
        squared[:, column] = distance_transform_1d(horizontal[:, column], row_spacing)
    return np.sqrt(squared)

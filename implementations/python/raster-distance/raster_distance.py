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

    candidates = np.flatnonzero(np.isfinite(f))
    if candidates.size == 0:
        return np.full(f.size, np.inf)
    weight = spacing * spacing
    vertices = np.empty(candidates.size, dtype=int)
    boundaries = np.empty(candidates.size + 1, dtype=float)
    k = 0
    vertices[0] = candidates[0]
    boundaries[0], boundaries[1] = -np.inf, np.inf

    for candidate in candidates[1:]:
        q = int(candidate)
        while True:
            p = vertices[k]
            intersection = (
                (f[q] + weight * q * q) - (f[p] + weight * p * p)
            ) / (2.0 * weight * (q - p))
            if intersection > boundaries[k] or k == 0:
                break
            k -= 1
        k += 1
        vertices[k] = q
        boundaries[k] = intersection
        boundaries[k + 1] = np.inf

    envelope_size = k + 1
    output = np.empty(f.size, dtype=float)
    k = 0
    for q in range(f.size):
        while k + 1 < envelope_size and boundaries[k + 1] < q:
            k += 1
        delta = q - vertices[k]
        output[q] = f[vertices[k]] + weight * delta * delta
    return output


def distance_to_targets(
    target_mask: np.ndarray,
    *,
    cell_size: Sequence[float] = (1.0, 1.0),
) -> np.ndarray:
    """Return exact centre-to-centre Euclidean distance to the nearest True cell.

    Uses two separable one-dimensional lower-envelope passes. cell_size is
    ordered (row_spacing, column_spacing), in map units. Runtime is O(H*W).
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


def chamfer_distance_to_targets(
    target_mask: np.ndarray,
    *,
    cell_size: Sequence[float] = (1.0, 1.0),
) -> np.ndarray:
    """Return 8-neighbour chamfer graph distance to the nearest target.

    A forward and reverse raster scan relax the four predecessor/successor
    directions in each half-pass. Orthogonal moves cost their cell spacing;
    diagonal moves cost hypot(row_spacing, column_spacing). This computes
    shortest-path distance on the 8-neighbour raster graph without barriers.
    It is an approximation to continuous Euclidean distance and differs from
    the exact lower-envelope transform in distance_to_targets.
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
    diagonal = float(np.hypot(row_spacing, column_spacing))
    distance = np.where(mask, 0.0, np.inf)

    # Every shortest path in an obstacle-free 8-neighbour grid can be
    # represented by monotone coordinate steps, so the two raster scans
    # recover the exact graph metric for this neighbourhood.
    for row in range(height):
        for col in range(width):
            best = distance[row, col]
            if row > 0:
                best = min(best, distance[row - 1, col] + row_spacing)
                if col > 0:
                    best = min(best, distance[row - 1, col - 1] + diagonal)
                if col + 1 < width:
                    best = min(best, distance[row - 1, col + 1] + diagonal)
            if col > 0:
                best = min(best, distance[row, col - 1] + column_spacing)
            distance[row, col] = best

    for row in range(height - 1, -1, -1):
        for col in range(width - 1, -1, -1):
            best = distance[row, col]
            if row + 1 < height:
                best = min(best, distance[row + 1, col] + row_spacing)
                if col > 0:
                    best = min(best, distance[row + 1, col - 1] + diagonal)
                if col + 1 < width:
                    best = min(best, distance[row + 1, col + 1] + diagonal)
            if col + 1 < width:
                best = min(best, distance[row, col + 1] + column_spacing)
            distance[row, col] = best
    return distance

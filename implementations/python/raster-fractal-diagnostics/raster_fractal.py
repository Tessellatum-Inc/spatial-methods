"""Raster fractal diagnostics: box counting, gliding-box lacunarity and Hurst scaling."""
from __future__ import annotations

from typing import Iterable

import numpy as np


def _raster(values: Iterable[Iterable[float]]) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 2 or min(array.shape, default=0) < 2:
        raise ValueError("values must be a two-dimensional raster at least 2 by 2")
    if not np.all(np.isfinite(array)):
        raise ValueError("values must be finite")
    return array


def box_counting_dimension(
    values: Iterable[Iterable[float]],
    *,
    threshold: float = 0.0,
    box_sizes: Iterable[int] | None = None,
) -> dict:
    """Estimate binary-support box dimension; partial edge boxes are retained."""
    raster = _raster(values)
    if not np.isfinite(threshold):
        raise ValueError("threshold must be finite")
    occupied = raster > threshold
    maximum = min(raster.shape)
    if box_sizes is None:
        sizes = []
        size = 1
        while size <= maximum:
            sizes.append(size)
            size *= 2
    else:
        try:
            sizes = sorted(set(int(x) for x in box_sizes))
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("box_sizes must contain positive integers") from exc
        if len(sizes) < 2 or any(x <= 0 or x > maximum for x in sizes):
            raise ValueError("provide at least two box sizes between 1 and the smaller raster dimension")
    counts = []
    for size in sizes:
        count = 0
        for row in range(0, occupied.shape[0], size):
            for col in range(0, occupied.shape[1], size):
                if np.any(occupied[row:row + size, col:col + size]):
                    count += 1
        counts.append(count)
    valid = np.asarray(counts) > 0
    if np.count_nonzero(valid) < 2:
        dimension = None
    else:
        dimension = float(np.polyfit(np.log(1 / np.asarray(sizes)[valid]), np.log(np.asarray(counts)[valid]), 1)[0])
    return {
        "dimension": dimension,
        "box_sizes": sizes,
        "occupied_box_counts": counts,
        "threshold": float(threshold),
        "occupied_cells": int(np.count_nonzero(occupied)),
    }


def gliding_box_lacunarity(
    values: Iterable[Iterable[float]],
    *,
    box_size: int,
    threshold: float = 0.0,
    stride: int = 1,
) -> dict:
    """Compute binary gliding-box lacunarity from all valid window origins."""
    raster = _raster(values)
    if isinstance(box_size, bool) or int(box_size) != box_size or box_size < 1 or box_size > min(raster.shape):
        raise ValueError("box_size must be an integer within the raster dimensions")
    if isinstance(stride, bool) or int(stride) != stride or stride < 1:
        raise ValueError("stride must be a positive integer")
    if not np.isfinite(threshold):
        raise ValueError("threshold must be finite")
    binary = (raster > threshold).astype(float)
    # Integral image makes each gliding-window mass an O(1) query.
    integral = np.pad(binary, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    k = int(box_size)
    masses = (
        integral[k::stride, k::stride]
        - integral[:-k:stride, k::stride]
        - integral[k::stride, :-k:stride]
        + integral[:-k:stride, :-k:stride]
    ).ravel()
    if masses.size == 0:
        raise ValueError("no gliding windows fit the requested box size and stride")
    mean = float(np.mean(masses))
    lacunarity = float(np.mean(masses ** 2) / (mean ** 2)) if mean > 0 else None
    return {
        "lacunarity": lacunarity,
        "mean_mass": mean,
        "mass_variance": float(np.var(masses)),
        "window_count": int(masses.size),
        "box_size": k,
        "stride": int(stride),
        "threshold": float(threshold),
    }


def estimate_hurst_exponent(
    values: Iterable[Iterable[float]],
    *,
    lags: Iterable[int] | None = None,
) -> dict:
    """Estimate H from isotropically pooled horizontal/vertical semivariograms."""
    raster = _raster(values)
    maximum = min(raster.shape) - 1
    if lags is None:
        lag_values = list(range(1, min(maximum, 8) + 1))
    else:
        try:
            lag_values = sorted(set(int(x) for x in lags))
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("lags must contain positive integers") from exc
        if len(lag_values) < 2 or any(x <= 0 or x > maximum for x in lag_values):
            raise ValueError("provide at least two lags within the raster dimensions")
    semivariances = []
    for lag in lag_values:
        horizontal = raster[:, lag:] - raster[:, :-lag]
        vertical = raster[lag:, :] - raster[:-lag, :]
        gamma = 0.5 * (np.mean(horizontal ** 2) + np.mean(vertical ** 2))
        semivariances.append(float(gamma))
    valid = np.asarray(semivariances) > 0
    if np.count_nonzero(valid) < 2:
        hurst = None
        slope = None
    else:
        slope = float(np.polyfit(np.log(np.asarray(lag_values)[valid]), np.log(np.asarray(semivariances)[valid]), 1)[0])
        hurst = slope / 2
    return {
        "hurst_exponent": hurst,
        "variogram_scaling_exponent": slope,
        "lags": lag_values,
        "semivariances": semivariances,
        "valid_lags": int(np.count_nonzero(valid)),
    }

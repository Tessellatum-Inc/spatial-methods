"""Fixed-bandwidth planar Gaussian kernel density estimation."""
from __future__ import annotations

from math import isfinite, pi
from typing import Sequence

import numpy as np


def gaussian_kde(
    points: Sequence[Sequence[float]] | np.ndarray,
    *,
    bounds: Sequence[float],
    grid_shape: Sequence[int] = (100, 100),
    bandwidth: float,
    weights: Sequence[float] | np.ndarray | None = None,
    chunk_size: int = 2048,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (intensity grid, x cell centres, y cell centres).

    Density is evaluated as sum_i w_i K_h(x - x_i), where K_h is the
    isotropic 2D Gaussian kernel. No edge correction is applied.
    """
    events = np.asarray(points, dtype=float)
    if events.ndim != 2 or events.shape[1] != 2 or events.shape[0] == 0:
        raise ValueError("points must be a non-empty array with shape (n, 2)")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")

    if len(bounds) != 4:
        raise ValueError("bounds must be (xmin, xmax, ymin, ymax)")
    xmin, xmax, ymin, ymax = map(float, bounds)
    if not all(isfinite(v) for v in (xmin, xmax, ymin, ymax)):
        raise ValueError("bounds must be finite")
    if not (xmin < xmax and ymin < ymax):
        raise ValueError("bounds must have positive width and height")
    if (
        (events[:, 0] < xmin).any()
        or (events[:, 0] > xmax).any()
        or (events[:, 1] < ymin).any()
        or (events[:, 1] > ymax).any()
    ):
        raise ValueError("all point coordinates must lie inside bounds")

    if len(grid_shape) != 2:
        raise ValueError("grid_shape must be (rows, columns)")
    rows, cols = grid_shape
    for value in (rows, cols):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value <= 0:
            raise ValueError("grid_shape values must be positive integers")
    try:
        bandwidth = float(bandwidth)
    except (TypeError, ValueError):
        raise ValueError("bandwidth must be finite and greater than zero") from None
    if not isfinite(bandwidth) or bandwidth <= 0:
        raise ValueError("bandwidth must be finite and greater than zero")
    if isinstance(chunk_size, (bool, np.bool_)) or not isinstance(chunk_size, (int, np.integer)) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    if weights is None:
        event_weights = np.ones(events.shape[0], dtype=float)
    else:
        event_weights = np.asarray(weights, dtype=float)
        if event_weights.shape != (events.shape[0],):
            raise ValueError("weights must contain one value per point")
        if not np.isfinite(event_weights).all() or (event_weights < 0).any():
            raise ValueError("weights must be finite and non-negative")

    x_centres = xmin + (np.arange(cols) + 0.5) * ((xmax - xmin) / cols)
    y_centres = ymin + (np.arange(rows) + 0.5) * ((ymax - ymin) / rows)
    xx, yy = np.meshgrid(x_centres, y_centres)
    grid = np.column_stack((xx.ravel(), yy.ravel()))
    density = np.empty(grid.shape[0], dtype=float)
    normaliser = 1.0 / (2.0 * pi * bandwidth * bandwidth)
    denominator = 2.0 * bandwidth * bandwidth

    for start in range(0, grid.shape[0], int(chunk_size)):
        stop = min(start + int(chunk_size), grid.shape[0])
        delta = grid[start:stop, None, :] - events[None, :, :]
        squared_distance = np.einsum("ijk,ijk->ij", delta, delta)
        kernel = np.exp(-squared_distance / denominator)
        density[start:stop] = normaliser * (kernel @ event_weights)

    return density.reshape(rows, cols), x_centres, y_centres



def adaptive_gaussian_kde(
    points: Sequence[Sequence[float]] | np.ndarray,
    *,
    bounds: Sequence[float],
    grid_shape: Sequence[int] = (100, 100),
    bandwidth: float,
    weights: Sequence[float] | np.ndarray | None = None,
    alpha: float = 0.5,
    bandwidth_factor_bounds: Sequence[float] = (0.25, 4.0),
    chunk_size: int = 2048,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Abramson-style sample-point adaptive KDE.

    A fixed-bandwidth leave-one-out pilot density is evaluated at each event.
    Local bandwidths are h_i = h * (g / f_i)**alpha, where g is the
    geometric mean of positive pilot densities. Factors are clipped to the
    supplied bounds. Returns (intensity_grid, x_centres, y_centres,
    local_bandwidths). No edge correction is applied.
    """
    events = np.asarray(points, dtype=float)
    if events.ndim != 2 or events.shape[1] != 2 or events.shape[0] == 0:
        raise ValueError("points must be a non-empty array with shape (n, 2)")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")
    if len(bounds) != 4:
        raise ValueError("bounds must be (xmin, xmax, ymin, ymax)")
    xmin, xmax, ymin, ymax = map(float, bounds)
    if not all(isfinite(v) for v in (xmin, xmax, ymin, ymax)) or xmin >= xmax or ymin >= ymax:
        raise ValueError("bounds must be finite with positive width and height")
    if ((events[:, 0] < xmin).any() or (events[:, 0] > xmax).any()
            or (events[:, 1] < ymin).any() or (events[:, 1] > ymax).any()):
        raise ValueError("all point coordinates must lie inside bounds")
    if len(grid_shape) != 2:
        raise ValueError("grid_shape must be (rows, columns)")
    rows, cols = grid_shape
    if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer)) or v <= 0 for v in (rows, cols)):
        raise ValueError("grid_shape values must be positive integers")
    try:
        bandwidth = float(bandwidth)
    except (TypeError, ValueError):
        raise ValueError("bandwidth must be finite and greater than zero") from None
    if not isfinite(bandwidth) or bandwidth <= 0:
        raise ValueError("bandwidth must be finite and greater than zero")
    try:
        alpha = float(alpha)
    except (TypeError, ValueError):
        raise ValueError("alpha must be finite and in [0, 1]") from None
    if not isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("alpha must be finite and in [0, 1]")
    if len(bandwidth_factor_bounds) != 2:
        raise ValueError("bandwidth_factor_bounds must be (minimum, maximum)")
    factor_min, factor_max = map(float, bandwidth_factor_bounds)
    if not isfinite(factor_min) or not isfinite(factor_max) or factor_min <= 0 or factor_min > factor_max:
        raise ValueError("bandwidth factor bounds must be finite, positive and ordered")
    if isinstance(chunk_size, (bool, np.bool_)) or not isinstance(chunk_size, (int, np.integer)) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    if weights is None:
        event_weights = np.ones(len(events), dtype=float)
    else:
        event_weights = np.asarray(weights, dtype=float)
        if event_weights.shape != (len(events),) or not np.isfinite(event_weights).all() or (event_weights < 0).any():
            raise ValueError("weights must be finite, non-negative and match points")
    if not np.any(event_weights > 0):
        raise ValueError("at least one event weight must be positive")

    n = len(events)
    if n == 1 or alpha == 0:
        local_bandwidths = np.full(n, bandwidth, dtype=float)
    else:
        delta = events[:, None, :] - events[None, :, :]
        squared = np.einsum("ijk,ijk->ij", delta, delta)
        np.fill_diagonal(squared, np.inf)
        kernel = np.exp(-squared / (2 * bandwidth * bandwidth)) * event_weights[None, :]
        np.fill_diagonal(kernel, 0.0)
        other_weight = event_weights.sum() - event_weights
        pilot = kernel.sum(axis=1) / (2 * pi * bandwidth * bandwidth * np.maximum(other_weight, 1e-300))
        positive = pilot[(pilot > 0) & (event_weights > 0)]
        if positive.size == 0:
            local_bandwidths = np.full(n, bandwidth, dtype=float)
        else:
            active = event_weights > 0
            active_pilot = pilot[active]
            floor = max(float(positive.min()) * 1e-12, np.finfo(float).tiny)
            safe_pilot = np.maximum(active_pilot, floor)
            geometric_mean = float(np.exp(np.mean(np.log(safe_pilot))))
            factors = np.ones(n, dtype=float)
            factors[active] = np.clip(
                np.power(geometric_mean / safe_pilot, alpha), factor_min, factor_max
            )
            local_bandwidths = bandwidth * factors

    xs = xmin + (np.arange(cols) + 0.5) * ((xmax - xmin) / cols)
    ys = ymin + (np.arange(rows) + 0.5) * ((ymax - ymin) / rows)
    xx, yy = np.meshgrid(xs, ys)
    grid = np.column_stack((xx.ravel(), yy.ravel()))
    density = np.empty(len(grid), dtype=float)
    for start in range(0, len(grid), int(chunk_size)):
        stop = min(start + int(chunk_size), len(grid))
        delta = grid[start:stop, None, :] - events[None, :, :]
        squared = np.einsum("ijk,ijk->ij", delta, delta)
        variance = local_bandwidths[None, :] ** 2
        kernels = np.exp(-squared / (2 * variance)) / (2 * pi * variance)
        density[start:stop] = kernels @ event_weights
    return density.reshape(rows, cols), xs, ys, local_bandwidths


def select_bandwidth_loo(
    points: Sequence[Sequence[float]] | np.ndarray,
    candidates: Sequence[float],
    *,
    weights: Sequence[float] | np.ndarray | None = None,
) -> tuple[float, list[tuple[float, float]]]:
    """Select Gaussian KDE bandwidth by weighted leave-one-out log likelihood.

    Each event is predicted from all other events; candidate scores are
    weighted mean log predictive densities. Returns best h and scores in
    input candidate order. Direct O(n^2 c) method for modest samples.
    """
    events = np.asarray(points, dtype=float)
    if events.ndim != 2 or events.shape[1] != 2 or len(events) < 2:
        raise ValueError("points must have shape (n, 2) with n >= 2")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")
    hs = [float(h) for h in candidates]
    if not hs or any(not isfinite(h) or h <= 0 for h in hs):
        raise ValueError("candidates must be positive finite bandwidths")
    if weights is None:
        w = np.ones(len(events), dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != (len(events),) or not np.isfinite(w).all() or (w < 0).any():
            raise ValueError("weights must be finite, non-negative and match points")
    if np.count_nonzero(w) < 2:
        raise ValueError("at least two positive event weights are required")
    delta = events[:, None, :] - events[None, :, :]
    squared = np.einsum("ijk,ijk->ij", delta, delta)
    np.fill_diagonal(squared, np.inf)
    evaluation = w > 0
    scores = []
    for h in hs:
        kernels = np.exp(-squared / (2 * h * h)) * w[None, :]
        predictive = kernels.sum(axis=1) / (2 * pi * h * h * (w.sum() - w))
        score = (float("-inf") if np.any(predictive[evaluation] <= 0)
                 else float(np.average(np.log(predictive[evaluation]), weights=w[evaluation])))
        scores.append((h, score))
    return max(scores, key=lambda item: item[1])[0], scores


def silverman_bandwidth(
    points: Sequence[Sequence[float]] | np.ndarray,
    *,
    weights: Sequence[float] | np.ndarray | None = None,
) -> float:
    """Return the isotropic bivariate normal-reference bandwidth.

    For d=2 the multivariate normal-reference factor is one, giving
    h = s * n_eff**(-1/6). Here s is the pooled RMS sample standard
    deviation of x and y; n_eff is the Kish effective sample size.
    Weighted sample variances use the reliability-weight correction.
    This is a scale-based starting value, not a substitute for validation
    or cross-validated bandwidth selection.
    """
    events = np.asarray(points, dtype=float)
    if events.ndim != 2 or events.shape[1] != 2 or len(events) < 2:
        raise ValueError("points must have shape (n, 2) with n >= 2")
    if not np.isfinite(events).all():
        raise ValueError("point coordinates must be finite")

    if weights is None:
        w = np.ones(len(events), dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != (len(events),) or not np.isfinite(w).all() or (w < 0).any():
            raise ValueError("weights must be finite, non-negative and match points")
    positive = w > 0
    if np.count_nonzero(positive) < 2:
        raise ValueError("at least two positive event weights are required")

    active = events[positive]
    active_w = w[positive]
    total = float(active_w.sum())
    sum_squares = float(np.dot(active_w, active_w))
    effective_n = total * total / sum_squares
    denominator = total - sum_squares / total
    if denominator <= 0 or effective_n <= 1:
        raise ValueError("at least two effective observations are required")

    mean = np.average(active, axis=0, weights=active_w)
    variance = np.sum(active_w[:, None] * (active - mean) ** 2, axis=0) / denominator
    pooled_scale = float(np.sqrt(np.mean(variance)))
    if not isfinite(pooled_scale) or pooled_scale <= 0:
        raise ValueError("points must have positive pooled spatial variance")
    return pooled_scale * effective_n ** (-1.0 / 6.0)

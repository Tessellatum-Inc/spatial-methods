"""Harmonic Analysis of Time Series with iterative outlier rejection."""
import math
import numpy as np


def hants(values, *, period, harmonics=2, times=None, direction="low",
          low_reject=0.0, high_reject=0.0, max_iterations=100):
    """Fit Fourier harmonics while iteratively rejecting threshold outliers.

    NaN observations are treated as missing. At each iteration the single
    largest threshold exceedance in the selected direction is removed.
    """
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or y.size < 1 or np.isinf(y).any():
        raise ValueError("values must be 1D finite values or NaN")
    if isinstance(period, bool) or not isinstance(period, (int, float)) or not math.isfinite(period) or period <= 0:
        raise ValueError("period must be finite and positive")
    if isinstance(harmonics, bool) or not isinstance(harmonics, int) or harmonics < 1:
        raise ValueError("harmonics must be a positive integer")
    if direction not in {"low", "high", "both"}:
        raise ValueError("direction must be low, high or both")
    for name, threshold in (("low_reject", low_reject), ("high_reject", high_reject)):
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not math.isfinite(threshold) or threshold < 0:
            raise ValueError(f"{name} must be finite and nonnegative")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if times is None:
        x = np.arange(y.size, dtype=float)
    else:
        x = np.asarray(times, dtype=float)
        if x.shape != y.shape or not np.isfinite(x).all() or np.any(np.diff(x) <= 0):
            raise ValueError("times must be finite, match values and strictly increase")
    origin = float(x[0])
    cols = [np.ones(y.size)]
    for k in range(1, harmonics + 1):
        angle = 2 * math.pi * k * (x - origin) / float(period)
        cols.extend((np.sin(angle), np.cos(angle)))
    design = np.column_stack(cols)
    p = design.shape[1]
    valid = np.isfinite(y)
    if int(valid.sum()) < p + 1:
        raise ValueError("at least p+1 finite observations are required")
    if np.linalg.matrix_rank(design[valid]) < p:
        raise ValueError("harmonic design matrix is rank deficient")
    rejected, converged = [], False
    coefficients = None
    fitted = np.full(y.shape, np.nan)
    residuals = np.full(y.shape, np.nan)
    for iteration in range(1, max_iterations + 1):
        coefficients, _, rank, _ = np.linalg.lstsq(design[valid], y[valid], rcond=None)
        if rank != p:
            raise ValueError("remaining harmonic design matrix is rank deficient")
        fitted = design @ coefficients
        residuals = np.where(np.isfinite(y), y - fitted, np.nan)
        candidates = []
        if direction in {"low", "both"}:
            idx = np.flatnonzero(valid & (residuals < -float(low_reject)))
            candidates.extend((float(-residuals[i] - low_reject), int(i)) for i in idx)
        if direction in {"high", "both"}:
            idx = np.flatnonzero(valid & (residuals > float(high_reject)))
            candidates.extend((float(residuals[i] - high_reject), int(i)) for i in idx)
        if not candidates:
            converged = True
            break
        if int(valid.sum()) <= p + 1:
            break
        _, worst = max(candidates)
        valid[worst] = False
        rejected.append(worst)
    # Ensure returned fitted values and residuals correspond to the final
    # retained set, including when the iteration limit was reached.
    coefficients, _, rank, _ = np.linalg.lstsq(design[valid], y[valid], rcond=None)
    if rank != p:
        raise ValueError("final retained harmonic design matrix is rank deficient")
    fitted = design @ coefficients
    residuals = np.where(np.isfinite(y), y - fitted, np.nan)
    return {
        "fitted": fitted.tolist(), "residuals": residuals.tolist(),
        "coefficients": coefficients.tolist(), "valid_indices": np.flatnonzero(valid).tolist(),
        "rejected_indices": rejected, "missing_indices": np.flatnonzero(~np.isfinite(y)).tolist(),
        "iterations": iteration, "converged": converged,
        "harmonics": harmonics, "period": float(period), "direction": direction,
    }

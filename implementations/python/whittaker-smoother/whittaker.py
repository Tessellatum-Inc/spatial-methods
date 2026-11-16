"""Whittaker-Eilers penalized finite-difference smoothing."""
from __future__ import annotations
import numpy as np


def whittaker_smooth(values, lam=10.0, order=2, weights=None):
    """Smooth a 1D ordered sequence by penalizing finite differences.

    Minimizes sum_i w_i (y_i - z_i)^2 + lam * ||D_order z||_2^2.
    Non-finite observations receive zero weight. The index spacing is assumed
    uniform; this is not a spatially adaptive or irregular-grid smoother.
    """
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or y.size < 2:
        raise ValueError("values must be a 1D sequence with at least two entries")
    if not np.isfinite(lam) or lam < 0:
        raise ValueError("lam must be finite and non-negative")
    if not isinstance(order, (int, np.integer)) or order < 1 or order >= y.size:
        raise ValueError("order must be an integer from 1 to len(values)-1")
    if weights is None:
        w = np.ones(y.size, dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != y.shape or not np.isfinite(w).all() or np.any(w < 0):
            raise ValueError("weights must be finite, non-negative and match values")
    observed = np.isfinite(y)
    w = w.copy()
    w[~observed] = 0.0
    if np.count_nonzero(w > 0) < order:
        raise ValueError("at least order positive-weight observations are required to identify the smoothing null space")
    safe_y = np.where(observed, y, 0.0)
    if lam == 0:
        if np.any(w == 0):
            raise ValueError("lam must be positive when observations are missing or zero-weighted")
        return safe_y.copy()
    difference = np.diff(np.eye(y.size), n=order, axis=0)
    penalty = difference.T @ difference
    system = np.diag(w) + float(lam) * penalty
    rhs = w * safe_y
    try:
        return np.linalg.solve(system, rhs)
    except np.linalg.LinAlgError as exc:
        raise ValueError("smoothing system is singular; increase lam or observation weights") from exc

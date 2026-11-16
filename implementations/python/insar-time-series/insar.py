"""Orbital-ramp correction and small-baseline InSAR network inversion."""
from __future__ import annotations
import numpy as np


def remove_orbital_ramp(phase, *, valid_mask=None, order=1):
    """Fit and remove a spatial polynomial ramp from a 2D phase image.

    Coordinates are normalized to [-1, 1]. Order 1 fits a plane; order 2
    includes quadratic terms. Input is assumed unwrapped and finite or NaN.
    """
    z = np.asarray(phase, dtype=float)
    if z.ndim != 2 or min(z.shape) < 2 or np.any(np.isinf(z)):
        raise ValueError("phase must be a 2D array with no infinite values")
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    if valid_mask is None:
        valid = np.isfinite(z)
    else:
        raw = np.asarray(valid_mask)
        if raw.shape != z.shape or raw.dtype.kind != "b":
            raise ValueError("valid_mask must be boolean and match phase")
        valid = raw & np.isfinite(z)
    rows, cols = z.shape
    yy, xx = np.indices(z.shape, dtype=float)
    x = 2*xx/max(cols-1,1)-1
    y = 2*yy/max(rows-1,1)-1
    columns = [np.ones(z.size), x.ravel(), y.ravel()]
    if order == 2:
        columns.extend([x.ravel()**2, x.ravel()*y.ravel(), y.ravel()**2])
    design = np.column_stack(columns)
    if valid.sum() < design.shape[1]:
        raise ValueError("not enough valid pixels to fit the requested ramp order")
    coefficients, _, rank, _ = np.linalg.lstsq(design[valid.ravel()], z[valid], rcond=None)
    if rank < design.shape[1]:
        raise ValueError("valid pixels do not span the requested ramp design")
    ramp = (design @ coefficients).reshape(z.shape)
    corrected = z - ramp
    corrected[~valid] = np.nan
    return {"corrected": corrected, "ramp": ramp,
            "coefficients": coefficients, "order": int(order)}


def sbas_network_inversion(interferograms, pairs, *, n_dates,
                           reference_date=0, weights=None):
    """Invert unwrapped interferogram differences into per-date displacement.

    Interferogram k is defined as displacement[pairs[k,1]] minus
    displacement[pairs[k,0]]. The reference date is fixed to zero. Pixels
    are solved independently by weighted least squares; rank-deficient
    networks are returned as NaN rather than regularized silently.
    """
    data = np.asarray(interferograms, dtype=float)
    edge = np.asarray(pairs)
    if data.ndim == 0 or data.shape[0] == 0 or np.any(np.isinf(data)):
        raise ValueError("interferograms must be a non-empty stack with no infinite values")
    if edge.shape != (data.shape[0], 2) or not np.issubdtype(edge.dtype, np.integer):
        raise ValueError("pairs must be an integer (n_interferograms, 2) array")
    if isinstance(n_dates, (bool, np.bool_)) or not isinstance(n_dates, (int, np.integer)) or n_dates < 2:
        raise ValueError("n_dates must be an integer of at least two")
    if isinstance(reference_date, (bool, np.bool_)) or not isinstance(reference_date, (int, np.integer)) or not 0 <= reference_date < n_dates:
        raise ValueError("reference_date must be a valid date index")
    if np.any(edge < 0) or np.any(edge >= n_dates) or np.any(edge[:,0] == edge[:,1]):
        raise ValueError("pairs contain invalid or identical date indices")
    if weights is None:
        w = np.ones(data.shape, dtype=float)
    else:
        raw = np.asarray(weights, dtype=float)
        try:
            w = np.broadcast_to(raw, data.shape).copy()
        except ValueError:
            raise ValueError("weights must be broadcastable to interferograms") from None
        if not np.all(np.isfinite(w)) or np.any(w < 0):
            raise ValueError("weights must be finite and non-negative")
    unknown_dates = [i for i in range(n_dates) if i != reference_date]
    col = {date: j for j, date in enumerate(unknown_dates)}
    design = np.zeros((len(edge), n_dates-1), dtype=float)
    for k, (first, second) in enumerate(edge):
        if first != reference_date:
            design[k, col[int(first)]] -= 1.0
        if second != reference_date:
            design[k, col[int(second)]] += 1.0
    spatial_shape = data.shape[1:]
    flat = data.reshape(data.shape[0], -1)
    wf = w.reshape(w.shape[0], -1)
    displacement = np.full((n_dates, flat.shape[1]), np.nan, dtype=float)
    displacement[reference_date] = 0.0
    residuals = np.full_like(flat, np.nan)
    rmse = np.full(flat.shape[1], np.nan)
    count = np.zeros(flat.shape[1], dtype=np.int32)
    rank_out = np.zeros(flat.shape[1], dtype=np.int32)
    for pixel in range(flat.shape[1]):
        valid = np.isfinite(flat[:,pixel]) & (wf[:,pixel] > 0)
        count[pixel] = int(valid.sum())
        if valid.sum() < n_dates-1:
            continue
        a = design[valid] * np.sqrt(wf[valid,pixel,None])
        b = flat[valid,pixel] * np.sqrt(wf[valid,pixel])
        solution, _, rank, _ = np.linalg.lstsq(a, b, rcond=None)
        rank_out[pixel] = rank
        if rank < n_dates-1:
            continue
        displacement[unknown_dates,pixel] = solution
        residual = flat[valid,pixel] - design[valid] @ solution
        residuals[valid,pixel] = residual
        rmse[pixel] = float(np.sqrt(np.mean(residual**2)))
    return {"displacement": displacement.reshape((n_dates,)+spatial_shape),
            "residuals": residuals.reshape(data.shape),
            "rmse": rmse.reshape(spatial_shape),
            "valid_interferogram_count": count.reshape(spatial_shape),
            "design_rank": rank_out.reshape(spatial_shape)}

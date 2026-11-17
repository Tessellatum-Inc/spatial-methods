"""Small-sample geographically weighted least-squares reference implementation."""
from __future__ import annotations
import numpy as np

def _array(value, name, ndim):
    result = np.asarray(value, dtype=float)
    if result.ndim != ndim or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite {ndim}-D array")
    return result

def gwr_fit(coordinates, design, response, bandwidth, *, kernel="bisquare",
            adaptive=False, sample_weights=None, condition_limit=1e12):
    """Fit local weighted least-squares models at every observation location."""
    xy = _array(coordinates, "coordinates", 2)
    x = _array(design, "design", 2)
    y = _array(response, "response", 1)
    n, p = x.shape
    if xy.shape[0] != n or y.size != n or xy.shape[1] < 1:
        raise ValueError("coordinates, design and response must share rows")
    if n <= p or p == 0:
        raise ValueError("at least p+1 observations are required")
    if kernel not in {"bisquare", "gaussian"}:
        raise ValueError("kernel must be 'bisquare' or 'gaussian'")
    if not np.isfinite(condition_limit) or condition_limit <= 1:
        raise ValueError("condition_limit must be finite and greater than one")
    if adaptive:
        if isinstance(bandwidth, bool) or int(bandwidth) != bandwidth:
            raise ValueError("adaptive bandwidth must be an integer neighbour count")
        k = int(bandwidth)
        if k < p + 1 or k >= n:
            raise ValueError("adaptive bandwidth must be between p+1 and n-1")
    else:
        if not np.isfinite(bandwidth) or bandwidth <= 0:
            raise ValueError("fixed bandwidth must be positive and finite")
        h_fixed = float(bandwidth)
    if sample_weights is None:
        base = np.ones(n, dtype=float)
    else:
        base = _array(sample_weights, "sample_weights", 1)
        if base.size != n or np.any(base < 0) or not np.any(base > 0):
            raise ValueError("sample_weights must be nonnegative, length n, and not all zero")
    coefficients = np.empty((n, p), dtype=float)
    fitted = np.empty(n, dtype=float)
    effective_n = np.empty(n, dtype=float)
    conditions = np.empty(n, dtype=float)
    bandwidths = np.empty(n, dtype=float)
    distances = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=2)
    for i in range(n):
        d = distances[i]
        if adaptive:
            h = float(np.sort(d)[k])
            if h <= 0:
                raise ValueError(f"adaptive bandwidth is zero at location {i}")
            h = np.nextafter(h, np.inf)
        else:
            h = h_fixed
        u = d / h
        if kernel == "bisquare":
            spatial = np.square(1.0 - np.square(u))
            spatial[u >= 1.0] = 0.0
        else:
            spatial = np.exp(-0.5 * np.square(u))
        weights = spatial * base
        positive = weights > 0
        if np.count_nonzero(positive) < p:
            raise ValueError(f"insufficient positive local weights at location {i}")
        root = np.sqrt(weights[positive])
        xw = x[positive] * root[:, None]
        yw = y[positive] * root
        beta, _, rank, singular = np.linalg.lstsq(xw, yw, rcond=None)
        if rank < p or singular.size == 0:
            raise ValueError(f"locally rank-deficient design at location {i}")
        condition = float(singular[0] / singular[-1])
        if not np.isfinite(condition) or condition > condition_limit:
            raise ValueError(f"ill-conditioned local design at location {i}")
        coefficients[i] = beta
        fitted[i] = float(x[i] @ beta)
        total = float(np.sum(weights))
        effective_n[i] = total * total / float(np.sum(weights * weights))
        conditions[i] = condition
        bandwidths[i] = h
    residuals = y - fitted
    return {"coefficients": coefficients, "fitted": fitted,
            "residuals": residuals, "effective_n": effective_n,
            "condition_numbers": conditions, "bandwidths": bandwidths}

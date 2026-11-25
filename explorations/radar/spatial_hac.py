"""Product-kernel spatial HAC intervals for a mean on an irregular block grid.

The estimator uses a separable Bartlett kernel over row/column offsets. It is
an experimental long-run variance estimator, not a calibrated default.
"""
from __future__ import annotations

import math
import numpy as np


def spatial_hac_mean_interval(
    block_ids,
    block_values,
    *,
    grid_columns: int,
    bandwidth_rows: int,
    bandwidth_columns: int | None = None,
    confidence_level: float = 0.95,
    min_blocks: int = 20,
):
    """Estimate a block-weighted mean and product-Bartlett spatial HAC interval.

    The variance estimator is N^-2 * sum_i sum_j K_ij (y_i-ybar)(y_j-ybar),
    where K_ij = (1-|dr|/h_r)_+ (1-|dc|/h_c)_+. This product kernel is
    positive semidefinite on the integer lattice; restricting it to an
    irregular subset preserves that property.

    Bandwidths are expressed in base-grid block spacings. The function does
    not select bandwidths. The normal critical value is a working asymptotic
    approximation and must be coverage-tested for the intended design.
    """
    ids = np.asarray(block_ids, dtype=np.int64)
    values = np.asarray(block_values, dtype=float)
    if ids.ndim != 1 or values.ndim != 1 or ids.shape != values.shape:
        raise ValueError("Block IDs and values must be matching one-dimensional arrays")
    if grid_columns < 1 or bandwidth_rows < 1:
        raise ValueError("grid_columns and bandwidth_rows must be positive")
    if bandwidth_columns is None:
        bandwidth_columns = bandwidth_rows
    if bandwidth_columns < 1:
        raise ValueError("bandwidth_columns must be positive")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between zero and one")
    if min_blocks < 2:
        raise ValueError("min_blocks must be at least two")
    if np.any(ids < 0) or np.unique(ids).size != ids.size:
        raise ValueError("block_ids must be non-negative and unique")

    valid = np.isfinite(values)
    ids, values = ids[valid], values[valid]
    n = int(values.size)
    estimate = float(values.mean()) if n else None
    base = {
        "estimate": estimate,
        "standard_error": None,
        "lower": None,
        "upper": None,
        "eligible_blocks": n,
        "bandwidth_rows": int(bandwidth_rows),
        "bandwidth_columns": int(bandwidth_columns),
        "kernel": "product_bartlett",
        "confidence_level": float(confidence_level),
        "interval_status": "insufficient_blocks",
    }
    if n < min_blocks:
        return base
    if float(np.dot(values - values.mean(), values - values.mean())) == 0.0:
        return {**base, "standard_error": 0.0, "lower": estimate, "upper": estimate,
                "interval_status": "no_variation"}

    rows = ids // int(grid_columns)
    cols = ids % int(grid_columns)
    lookup = {(int(r), int(c)): i for i, (r, c) in enumerate(zip(rows, cols))}
    centred = values - values.mean()
    quadratic = float(np.dot(centred, centred))

    hr, hc = int(bandwidth_rows), int(bandwidth_columns)
    # Enumerate each unordered pair once, then double its contribution.
    for i, (row, col) in enumerate(zip(rows, cols)):
        for dr in range(hr):
            dc_values = range(-(hc - 1), hc) if dr > 0 else range(1, hc)
            for dc in dc_values:
                j = lookup.get((int(row) + dr, int(col) + dc))
                if j is None:
                    continue
                weight = (1.0 - dr / hr) * (1.0 - abs(dc) / hc)
                quadratic += 2.0 * weight * centred[i] * centred[j]

    variance = quadratic / (n * n)
    # Product Bartlett is PSD; tolerate only floating-point-scale negatives.
    tolerance = np.finfo(float).eps * max(1.0, abs(quadratic)) * 100
    if variance < -tolerance:
        return {**base, "interval_status": "negative_hac_variance"}
    variance = max(0.0, variance)
    se = math.sqrt(variance)
    alpha = 1.0 - confidence_level
    # Inverse standard-normal CDF via the standard-library error function
    # is not available in closed form; use a high-accuracy rational approximation.
    z = _normal_quantile(1.0 - alpha / 2.0)
    return {
        **base,
        "standard_error": float(se),
        "lower": float(estimate - z * se),
        "upper": float(estimate + z * se),
        "interval_status": "spatial_hac_normal",
    }


def _normal_quantile(p: float) -> float:
    """Acklam inverse-normal approximation; sufficient for confidence limits."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be between zero and one")
    a = (-3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2,
         1.383577518672690e2, -3.066479806614716e1, 2.506628277459239)
    b = (-5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2,
         6.680131188771972e1, -1.328068155288572e1)
    c = (-7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838,
         -2.549732539343734, 4.374664141464968, 2.938163982698783)
    d = (7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996,
         3.754408661907416)
    plow, phigh = 0.02425, 1.0 - 0.02425
    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)
    if p > phigh:
        q = math.sqrt(-2.0 * math.log(1.0-p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)
    q = p - 0.5
    r = q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1.0)

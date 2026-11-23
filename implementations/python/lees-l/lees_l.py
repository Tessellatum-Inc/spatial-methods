"""Lee's L global bivariate spatial association, row-standardized W form."""
from __future__ import annotations

import math
from typing import Iterable, Sequence


def _finite_vector(values: Iterable[float], name: str) -> list[float]:
    try:
        result = [float(value) for value in values]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a one-dimensional numeric sequence") from exc
    if len(result) < 2:
        raise ValueError("at least two spatial units are required")
    if any(not math.isfinite(v) for v in result):
        raise ValueError(f"{name} must contain only finite values")
    if max(result) == min(result):
        raise ValueError(f"{name} must have non-zero variance")
    return result


def row_standardize(weights: Sequence[Sequence[float]]) -> list[list[float]]:
    """Validate W and return a row-standardized copy; islands are rejected."""
    n = len(weights)
    if n < 2 or any(len(row) != n for row in weights):
        raise ValueError("weights must be a square matrix with at least two rows")
    result: list[list[float]] = []
    for row in weights:
        try:
            values = [float(v) for v in row]
        except (TypeError, ValueError) as exc:
            raise ValueError("weights must be numeric") from exc
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise ValueError("weights must be finite and non-negative")
        total = sum(values)
        if total <= 0:
            raise ValueError("islands are not supported by this row-standardized formulation")
        result.append([v / total for v in values])
    if any(result[i][i] != 0.0 for i in range(n)):
        raise ValueError("weights diagonal must be zero (no self-neighbours)")
    return result


def _lag(values: Sequence[float], weights: Sequence[Sequence[float]]) -> list[float]:
    return [sum(weights[i][j] * values[j] for j in range(len(values)))
            for i in range(len(values))]


def lees_l(x: Iterable[float], y: Iterable[float],
           weights: Sequence[Sequence[float]]) -> dict[str, float | list[float]]:
    """Calculate Lee's L using Lee (2001), equation 13/14.

    W is row-standardized internally. Both variables' spatial lags enter the
    numerator. Original-variable means centre the lagged values, following
    the stated row-standardized derivation. This computes the statistic only.
    """
    xv = _finite_vector(x, "x")
    yv = _finite_vector(y, "y")
    n = len(xv)
    if len(yv) != n or len(weights) != n or any(len(row) != n for row in weights):
        raise ValueError("x, y and weights must have the same spatial-unit count")
    w = row_standardize(weights)
    xbar, ybar = sum(xv) / n, sum(yv) / n
    xlag, ylag = _lag(xv, w), _lag(yv, w)
    ssx = sum((v - xbar) ** 2 for v in xv)
    ssy = sum((v - ybar) ** 2 for v in yv)
    sss_x = sum((v - xbar) ** 2 for v in xlag) / ssx
    sss_y = sum((v - ybar) ** 2 for v in ylag) / ssy
    numerator = sum((xlag[i] - xbar) * (ylag[i] - ybar) for i in range(n))
    statistic = numerator / math.sqrt(ssx * ssy)
    return {"L": statistic, "spatial_smoothing_scalar_x": sss_x,
            "spatial_smoothing_scalar_y": sss_y,
            "spatial_lag_x": xlag, "spatial_lag_y": ylag}

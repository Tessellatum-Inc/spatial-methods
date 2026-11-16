"""Educational additive STL-style decomposition using local linear LOESS."""
from __future__ import annotations
from math import isfinite
from statistics import median
from typing import Sequence

def _validate_window(window: int, name: str) -> None:
    if isinstance(window, bool) or not isinstance(window, int) or window < 3 or window % 2 == 0:
        raise ValueError(f"{name} must be an odd integer >= 3")

def _loess(x: Sequence[float], y: Sequence[float], window: int, weights=None) -> list[float]:
    _validate_window(window, "window")
    n = len(x)
    if n != len(y) or n == 0:
        raise ValueError("x and y must have the same non-zero length")
    base = [1.0] * n if weights is None else list(weights)
    if len(base) != n or any(not isfinite(w) or w < 0 for w in base):
        raise ValueError("weights must be finite, non-negative and match y")
    result = []
    for i, x0 in enumerate(x):
        neighbours = sorted(range(n), key=lambda j: (abs(x[j] - x0), j))[:min(window, n)]
        radius = max((abs(x[j] - x0) for j in neighbours), default=0.0) or 1.0
        s0 = s1 = s2 = b0 = b1 = 0.0
        for j in neighbours:
            u = min(abs(x[j] - x0) / radius, 1.0)
            w = (1.0 - u ** 3) ** 3 * base[j]
            dx = x[j] - x0
            s0 += w; s1 += w * dx; s2 += w * dx * dx
            b0 += w * y[j]; b1 += w * dx * y[j]
        det = s0 * s2 - s1 * s1
        if s0 <= 0:
            result.append(float(y[i]))
        elif abs(det) < 1e-14:
            result.append(b0 / s0)
        else:
            result.append((b0 * s2 - b1 * s1) / det)
    return result

def _moving_average(values: Sequence[float], window: int) -> list[float]:
    half = window // 2
    padded = [values[0]] * half + list(values) + [values[-1]] * half
    return [sum(padded[i:i + window]) / window for i in range(len(values))]

def _low_pass(seasonal: Sequence[float], period: int) -> list[float]:
    first = _moving_average(seasonal, period) if period % 2 else _moving_average(_moving_average(seasonal, period), 2)
    return _moving_average(_moving_average(first, period), 3)

def _robust_weights(residual: Sequence[float]) -> list[float]:
    scale = 6.0 * median(abs(v) for v in residual)
    if scale <= 1e-15:
        return [1.0] * len(residual)
    return [(1.0 - (abs(v) / scale) ** 2) ** 2 if abs(v) / scale < 1 else 0.0 for v in residual]

def stl_decompose(values: Sequence[float], period: int, *, seasonal_window: int = 7,
                  trend_window: int | None = None, inner_iterations: int = 2,
                  robust: bool = False, outer_iterations: int = 5) -> dict[str, list[float]]:
    """Decompose a finite equally spaced additive series into STL-style components."""
    y = [float(v) for v in values]
    if len(y) < 2 or any(not isfinite(v) for v in y):
        raise ValueError("values must contain at least two finite observations")
    if isinstance(period, bool) or not isinstance(period, int) or period < 2:
        raise ValueError("period must be an integer >= 2")
    if len(y) < 2 * period:
        raise ValueError("at least two complete seasonal cycles are required")
    _validate_window(seasonal_window, "seasonal_window")
    if trend_window is None:
        trend_window = max(3, (int(1.5 * period) // 2) * 2 + 1)
    _validate_window(trend_window, "trend_window")
    if isinstance(inner_iterations, bool) or not isinstance(inner_iterations, int) or inner_iterations < 1:
        raise ValueError("inner_iterations must be a positive integer")
    if isinstance(outer_iterations, bool) or not isinstance(outer_iterations, int) or outer_iterations < 0:
        raise ValueError("outer_iterations must be a non-negative integer")
    n = len(y); x = list(range(n))
    trend = [0.0] * n; seasonal = [0.0] * n; robust_w = [1.0] * n
    passes = outer_iterations if robust else 0
    for outer in range(passes + 1):
        for _ in range(inner_iterations):
            detrended = [y[i] - trend[i] for i in range(n)]
            raw = [0.0] * n
            for phase in range(period):
                idx = list(range(phase, n, period))
                smooth = _loess(list(range(len(idx))), [detrended[i] for i in idx],
                                 seasonal_window, [robust_w[i] for i in idx])
                for i, value in zip(idx, smooth):
                    raw[i] = value
            low = _low_pass(raw, period)
            seasonal = [raw[i] - low[i] for i in range(n)]
            trend = _loess(x, [y[i] - seasonal[i] for i in range(n)], trend_window, robust_w)
        remainder = [y[i] - trend[i] - seasonal[i] for i in range(n)]
        if robust and outer < passes:
            robust_w = _robust_weights(remainder)
    remainder = [y[i] - trend[i] - seasonal[i] for i in range(n)]
    return {"trend": trend, "seasonal": seasonal, "remainder": remainder, "weights": robust_w}

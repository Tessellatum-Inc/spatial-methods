"""Grid inversion of spatial-lag Anderson–Rubin tests.

The returned set is a finite-grid approximation, not a continuous confidence
set. A component touching a grid endpoint is marked as grid-limited.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import numpy as np
from spatial_lag_anderson_rubin import spatial_lag_anderson_rubin


@dataclass(frozen=True)
class SpatialLagARSegment:
    lower: float
    upper: float
    lower_grid_limited: bool
    upper_grid_limited: bool


@dataclass(frozen=True)
class SpatialLagARConfidenceSet:
    test: str
    critical_value: float
    grid: tuple[float, ...]
    statistics: tuple[float, ...]
    accepted: tuple[bool, ...]
    segments: tuple[SpatialLagARSegment, ...]
    instrument_orders: int


def spatial_lag_ar_confidence_set(
    y: Sequence[float], x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]], rho_grid: Sequence[float], *,
    critical_value: float, test: str = "classical", instrument_orders: int = 2,
) -> SpatialLagARConfidenceSet:
    """Invert candidate-rho AR tests over a strictly increasing parameter grid.

    Retain grid points whose selected AR statistic does not exceed the supplied
    critical value. Classical selects the partial F; robust selects the HC1
    Wald chi-square. Supply a matching critical value yourself.

    Adjacent accepted points form a segment. Endpoints are grid approximations,
    not interpolated roots. A segment touching a grid edge may continue beyond
    the search range. Empty and disconnected sets are retained as such.
    """
    if test not in ("classical", "robust"):
        raise ValueError("test must be 'classical' or 'robust'")
    if not np.isscalar(critical_value) or not np.isfinite(critical_value) or critical_value <= 0:
        raise ValueError("critical_value must be positive and finite")
    grid = np.asarray(rho_grid, dtype=float)
    if (grid.ndim != 1 or grid.size < 3 or not np.all(np.isfinite(grid))
            or np.any(np.diff(grid) <= 0)):
        raise ValueError("rho_grid must contain at least three finite, strictly increasing values")
    if isinstance(instrument_orders, bool) or not isinstance(instrument_orders, int) or instrument_orders < 1:
        raise ValueError("instrument_orders must be a positive integer")

    stats = []
    for rho in grid:
        fit = spatial_lag_anderson_rubin(y, x, weights, float(rho),
                                         instrument_orders=instrument_orders)
        stats.append(float(fit.classical_f if test == "classical" else fit.robust_wald_chi2))
    keep = np.asarray(stats) <= float(critical_value)
    segments = []
    i = 0
    while i < keep.size:
        if not keep[i]:
            i += 1
            continue
        start = i
        while i + 1 < keep.size and keep[i + 1]:
            i += 1
        end = i
        segments.append(SpatialLagARSegment(float(grid[start]), float(grid[end]),
                                            start == 0, end == keep.size - 1))
        i += 1
    return SpatialLagARConfidenceSet(
        test, float(critical_value), tuple(float(v) for v in grid), tuple(stats),
        tuple(bool(v) for v in keep), tuple(segments), instrument_orders,
    )

"""Average direct, indirect and total impacts for SAR and SDM models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Impact:
    direct: float
    indirect: float
    total: float
    impact_matrix: tuple[tuple[float, ...], ...]


def spatial_impacts(
    weights: Sequence[Sequence[float]],
    rho: float,
    beta: Sequence[float],
    gamma: Sequence[float] | None = None,
) -> tuple[Impact, ...]:
    """Calculate average impacts for each covariate in a spatial Durbin model.

    For covariate r, S_r = (I-rho W)^-1 (beta_r I + gamma_r W).
    Average direct impact is trace(S_r)/N; average total impact is the
    average row sum (equivalently sum(S_r)/N); indirect is total minus direct.

    Set gamma=0 for the spatial-lag/SAR special case. Supply one gamma per
    beta; gamma=0 means no spatially lagged covariate for that term.
    """
    w = np.asarray(weights, dtype=float)
    b = np.asarray(beta, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1] or w.shape[0] < 2:
        raise ValueError("weights must be a square matrix with at least two units")
    n = w.shape[0]
    if b.ndim != 1 or b.size == 0:
        raise ValueError("beta must be a nonempty one-dimensional vector")
    if gamma is None:
        g = np.zeros_like(b)
    else:
        g = np.asarray(gamma, dtype=float)
        if g.shape != b.shape:
            raise ValueError("gamma must have one value per beta coefficient")
    if not np.all(np.isfinite(w)) or not np.all(np.isfinite(b)) or not np.all(np.isfinite(g)):
        raise ValueError("weights and coefficients must be finite")
    if not np.isfinite(rho):
        raise ValueError("rho must be finite")
    identity = np.eye(n)
    system = identity - float(rho) * w
    try:
        impacts = []
        for coefficient, spatial_coefficient in zip(b, g):
            right = coefficient * identity + spatial_coefficient * w
            matrix = np.linalg.solve(system, right)
            direct = float(np.trace(matrix) / n)
            total = float(np.sum(matrix) / n)
            indirect = total - direct
            impacts.append(Impact(
                direct=direct,
                indirect=indirect,
                total=total,
                impact_matrix=tuple(tuple(float(v) for v in row) for row in matrix),
            ))
    except np.linalg.LinAlgError as exc:
        raise ValueError("I - rho W must be nonsingular") from exc
    return tuple(impacts)

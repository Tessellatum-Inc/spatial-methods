"""Small, explicit bivariate global Moran's I teaching implementation."""
from __future__ import annotations

import math
import random
from typing import Iterable, Sequence


def _as_finite_vector(values: Iterable[float], name: str) -> list[float]:
    try:
        result = [float(value) for value in values]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a one-dimensional numeric sequence") from exc
    if not result:
        raise ValueError(f"{name} must not be empty")
    if any(not math.isfinite(value) for value in result):
        raise ValueError(f"{name} must contain only finite values")
    return result


def _standardize(values: Sequence[float], name: str) -> list[float]:
    if len(values) < 2:
        raise ValueError("at least two spatial units are required")
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    if variance <= 0.0:
        raise ValueError(f"{name} must have non-zero sample variance")
    scale = math.sqrt(variance)
    return [(value - mean) / scale for value in values]


def row_standardize(weights: Sequence[Sequence[float]]) -> list[list[float]]:
    """Return a row-standardized copy of a finite, non-negative weights matrix."""
    n = len(weights)
    if n == 0 or any(len(row) != n for row in weights):
        raise ValueError("weights must be a non-empty square matrix")
    result: list[list[float]] = []
    for row in weights:
        try:
            values = [float(value) for value in row]
        except (TypeError, ValueError) as exc:
            raise ValueError("weights must be numeric") from exc
        if any(not math.isfinite(value) or value < 0 for value in values):
            raise ValueError("weights must be finite and non-negative")
        total = sum(values)
        result.append([value / total for value in values] if total else [0.0] * n)
    return result


def _statistic(zx: Sequence[float], zy: Sequence[float], weights: Sequence[Sequence[float]]) -> float:
    n = len(zx)
    spatial_lag_y = [
        sum(weights[i][j] * zy[j] for j in range(n))
        for i in range(n)
    ]
    # Sample-standardized zx has sum(zx**2) = n - 1.
    return sum(zx[i] * spatial_lag_y[i] for i in range(n)) / (n - 1)


def bivariate_morans_i(
    x: Iterable[float],
    y: Iterable[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 0,
    seed: int | None = None,
) -> dict[str, float | int | list[float] | None]:
    """Compute global bivariate Moran's I and optional conditional randomization.

    x is held fixed; y is permuted across spatial units. The supplied weights
    matrix is row-standardized internally. The statistic is asymmetric in x,y.
    """
    xv = _as_finite_vector(x, "x")
    yv = _as_finite_vector(y, "y")
    n = len(xv)
    if n < 2:
        raise ValueError("at least two spatial units are required")
    if len(yv) != n or len(weights) != n or any(len(row) != n for row in weights):
        raise ValueError("x, y and the square weights matrix must have equal size")
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 0:
        raise ValueError("permutations must be a non-negative integer")

    zx = _standardize(xv, "x")
    zy = _standardize(yv, "y")
    w = row_standardize(weights)
    if not any(value > 0.0 for row in w for value in row):
        raise ValueError("weights must contain at least one positive link")
    if any(w[i][i] != 0.0 for i in range(n)):
        raise ValueError("weights diagonal must be zero (no self-neighbours)")

    observed = _statistic(zx, zy, w)
    simulations: list[float] = []
    if permutations:
        rng = random.Random(seed)
        for _ in range(permutations):
            shuffled = zy.copy()
            rng.shuffle(shuffled)
            simulations.append(_statistic(zx, shuffled, w))
        mean_sim = sum(simulations) / permutations
        p_sim = (
            1 + sum(abs(value - mean_sim) >= abs(observed - mean_sim) for value in simulations)
        ) / (permutations + 1)
        variance_sim = sum((value - mean_sim) ** 2 for value in simulations) / permutations
        sd_sim = math.sqrt(variance_sim)
        z_sim = (observed - mean_sim) / sd_sim if sd_sim else None
    else:
        p_sim = mean_sim = variance_sim = sd_sim = z_sim = None

    return {
        "I": observed,
        "permutations": permutations,
        "p_sim": p_sim,
        "mean_sim": mean_sim,
        "variance_sim": variance_sim,
        "sd_sim": sd_sim,
        "z_sim": z_sim,
        "simulations": simulations,
    }

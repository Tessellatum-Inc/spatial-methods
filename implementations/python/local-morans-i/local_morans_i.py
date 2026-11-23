"""Local Moran's I with conditional randomisation inference.

The statistic follows the standardised PySAL-style scaling documented in
algorithms/statistics/local-morans-i.md. The permutation p-value here is an
explicit two-sided, centred, plus-one Monte Carlo estimate; it is not claimed
to reproduce every software package's tail convention.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
import random
from typing import Sequence


@dataclass(frozen=True)
class LocalMoransResult:
    """Per-observation local statistic, lag, quadrant and pseudo p-value."""
    local_i: tuple[float, ...]
    spatial_lag: tuple[float, ...]
    standardized_values: tuple[float, ...]
    quadrant: tuple[int, ...]
    p_sim: tuple[float, ...]


def _validate(values: Sequence[float], weights: Sequence[Sequence[float]]):
    n = len(values)
    if n < 2:
        raise ValueError("at least two observations are required")
    x = [float(value) for value in values]
    if not all(isfinite(value) for value in x):
        raise ValueError("values must contain only finite numbers")
    if len(weights) != n:
        raise ValueError("weights must have one row per observation")
    matrix = []
    for i, row in enumerate(weights):
        if len(row) != n:
            raise ValueError("weights must be a square n-by-n matrix")
        clean = []
        for j, raw in enumerate(row):
            value = float(raw)
            if not isfinite(value):
                raise ValueError("weights must contain only finite values")
            if value < 0:
                raise ValueError("weights must be non-negative")
            if i == j and value != 0:
                raise ValueError("self-weights must be zero")
            clean.append(value)
        matrix.append(clean)
    if sum(map(sum, matrix)) <= 0:
        raise ValueError("weights must contain a positive weight")
    return x, matrix


def local_morans_i(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 999,
    seed: int | None = 0,
) -> LocalMoransResult:
    """Calculate local Moran statistics and conditional permutation p-values.

    Conditional permutations hold the focal value fixed and randomly
    reassign all other standardised values to locations. The observed row's
    weight pattern is retained. p_sim is a two-sided, centred Monte Carlo
    estimate (extreme + 1) / (permutations + 1). Islands receive p=1.

    Quadrant codes follow PySAL's default convention: 1=HH, 2=LH, 3=LL,
    4=HL. A zero coordinate is assigned to the non-positive side.
    """
    x, w = _validate(values, weights)
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 0:
        raise ValueError("permutations must be a non-negative integer")
    mean = sum(x) / len(x)
    variance = sum((value - mean) ** 2 for value in x) / len(x)
    if variance <= 0:
        raise ValueError("Local Moran's I is undefined for a constant variable")
    scale = variance ** 0.5
    z = [(value - mean) / scale for value in x]
    n = len(x)
    factor = (n - 1) / n
    rng = random.Random(seed)
    lags, statistics, quadrants, p_values = [], [], [], []

    for i in range(n):
        lag = sum(w[i][j] * z[j] for j in range(n))
        statistic = factor * z[i] * lag
        lags.append(lag)
        statistics.append(statistic)
        quadrants.append(
            1 if z[i] > 0 and lag > 0 else
            2 if z[i] <= 0 and lag > 0 else
            3 if z[i] <= 0 and lag <= 0 else 4
        )
        neighbours = [j for j in range(n) if w[i][j] > 0]
        if not neighbours or permutations == 0:
            p_values.append(1.0)
            continue
        other_indices = [j for j in range(n) if j != i]
        other_values = [z[j] for j in other_indices]
        simulated = []
        for _ in range(permutations):
            shuffled = other_values[:]
            rng.shuffle(shuffled)
            assigned = dict(zip(other_indices, shuffled))
            permuted_lag = sum(w[i][j] * assigned[j] for j in neighbours)
            simulated.append(factor * z[i] * permuted_lag)
        centre = sum(simulated) / permutations
        distance = abs(statistic - centre)
        extreme = sum(abs(value - centre) >= distance - 1e-15 for value in simulated)
        p_values.append((extreme + 1) / (permutations + 1))

    return LocalMoransResult(
        tuple(statistics), tuple(lags), tuple(z), tuple(quadrants), tuple(p_values)
    )

"""Local Geary c_i with conditional randomisation inference."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
import random
from typing import Sequence


@dataclass(frozen=True)
class LocalGearyResult:
    local_c: tuple[float, ...]
    p_sim: tuple[float, ...]


def _validated(values, weights):
    n = len(values)
    if n < 2:
        raise ValueError("at least two observations are required")
    x = [float(v) for v in values]
    if not all(isfinite(v) for v in x):
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


def local_geary(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 999,
    seed: int | None = 0,
) -> LocalGearyResult:
    """Calculate raw local Geary statistics and conditional permutation p-values.

    The statistic is c_i = sum_j w_ij (x_i - x_j)^2. For each focal i,
    conditional permutations keep x_i fixed and reassign the other values
    without replacement to all non-focal locations, preserving row i's
    weights. p_sim is a two-sided, centred plus-one Monte Carlo estimate.
    Islands receive p=1. The result is not rescaled or row-standardised.
    """
    x, w = _validated(values, weights)
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 0:
        raise ValueError("permutations must be a non-negative integer")
    rng = random.Random(seed)
    n = len(x)
    statistics, p_values = [], []
    for i in range(n):
        observed = sum(w[i][j] * (x[i] - x[j]) ** 2 for j in range(n))
        statistics.append(observed)
        neighbours = [j for j in range(n) if w[i][j] > 0]
        if not neighbours or permutations == 0:
            p_values.append(1.0)
            continue
        other_indices = [j for j in range(n) if j != i]
        other_values = [x[j] for j in other_indices]
        simulated = []
        for _ in range(permutations):
            shuffled = other_values[:]
            rng.shuffle(shuffled)
            assigned = dict(zip(other_indices, shuffled))
            simulated.append(sum(
                w[i][j] * (x[i] - assigned[j]) ** 2 for j in neighbours
            ))
        centre = sum(simulated) / permutations
        distance = abs(observed - centre)
        extreme = sum(abs(value - centre) >= distance - 1e-15 for value in simulated)
        p_values.append((extreme + 1) / (permutations + 1))
    return LocalGearyResult(tuple(statistics), tuple(p_values))

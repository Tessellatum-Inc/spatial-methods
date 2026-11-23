"""Global Getis-Ord G and local Getis-Ord Gi* teaching implementations."""
from __future__ import annotations
from dataclasses import dataclass
from math import erfc, isfinite, sqrt
import random
from typing import Sequence


@dataclass(frozen=True)
class GlobalGResult:
    statistic: float
    expected: float
    p_sim: float
    simulated_mean: float | None
    simulated_sd: float | None


@dataclass(frozen=True)
class LocalGiStarResult:
    neighbourhood_sum: tuple[float, ...]
    z_score: tuple[float, ...]
    p_two_sided_normal: tuple[float, ...]


def _values_and_weights(values, weights, *, positive=True, allow_diagonal=False):
    n = len(values)
    if n < 2:
        raise ValueError("at least two observations are required")
    x = [float(v) for v in values]
    if not all(isfinite(v) for v in x):
        raise ValueError("values must contain only finite numbers")
    if positive and any(v <= 0 for v in x):
        raise ValueError("Getis-Ord G requires strictly positive values")
    if len(weights) != n:
        raise ValueError("weights must have one row per observation")
    w = []
    for i, row in enumerate(weights):
        if len(row) != n:
            raise ValueError("weights must be a square n-by-n matrix")
        clean = []
        for j, raw in enumerate(row):
            value = float(raw)
            if not isfinite(value) or value < 0:
                raise ValueError("weights must be finite and non-negative")
            if i == j and value != 0 and not allow_diagonal:
                raise ValueError("global G weights must have a zero diagonal")
            clean.append(value)
        w.append(clean)
    return x, w


def _global_g(x, w):
    n = len(x)
    s0 = sum(map(sum, w))
    if s0 <= 0:
        raise ValueError("weights must contain a positive off-diagonal weight")
    denominator = sum(x[i] * x[j] for i in range(n) for j in range(n) if i != j)
    if denominator <= 0:
        raise ValueError("global G denominator must be positive")
    numerator = sum(w[i][j] * x[i] * x[j]
                    for i in range(n) for j in range(n) if i != j)
    return numerator / denominator, s0 / (n * (n - 1))


def global_getis_ord_g(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 999,
    seed: int | None = 0,
) -> GlobalGResult:
    """Compute global Getis-Ord G and a two-sided permutation p-value.

    The diagonal is excluded. Values must be strictly positive. Weights may
    be directed and non-negative; they are not silently row-standardised.
    Permutations reassign the observed values to locations while holding the
    weights fixed. p_sim is a centred two-sided plus-one Monte Carlo estimate.
    """
    x, w = _values_and_weights(values, weights)
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 0:
        raise ValueError("permutations must be a non-negative integer")
    observed, expected = _global_g(x, w)
    if permutations == 0:
        return GlobalGResult(observed, expected, 1.0, None, None)
    rng = random.Random(seed)
    simulated = []
    for _ in range(permutations):
        shuffled = x[:]
        rng.shuffle(shuffled)
        value, _ = _global_g(shuffled, w)
        simulated.append(value)
    centre = sum(simulated) / permutations
    variance = sum((v - centre) ** 2 for v in simulated) / permutations
    sd = sqrt(variance)
    distance = abs(observed - centre)
    extreme = sum(abs(v - centre) >= distance - 1e-15 for v in simulated)
    p_value = (extreme + 1) / (permutations + 1)
    return GlobalGResult(observed, expected, p_value, centre, sd)


def local_getis_ord_gistar(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
) -> LocalGiStarResult:
    """Compute analytical randomisation z-scores for local Getis-Ord Gi*.

    The weights matrix must be binary, include each focal unit on its own
    diagonal, and is not row-standardised. The standard randomisation
    variance formula is used. The returned p value is a two-sided standard
    normal approximation, clearly separated from permutation inference.
    """
    x, w = _values_and_weights(values, weights, positive=True, allow_diagonal=True)
    n = len(x)
    for i, row in enumerate(w):
        if any(value not in (0.0, 1.0) for value in row):
            raise ValueError("Gi* requires binary weights")
        if row[i] != 1.0:
            raise ValueError("Gi* weights must include the focal observation")
    mean = sum(x) / n
    s = sqrt(sum(value * value for value in x) / n - mean * mean)
    if s == 0:
        raise ValueError("Gi* is undefined for a constant variable")
    sums, z_scores, p_values = [], [], []
    for row in w:
        sum_w = sum(row)
        sum_w2 = sum(value * value for value in row)
        variance_factor = (n * sum_w2 - sum_w * sum_w) / (n - 1)
        if variance_factor <= 0:
            raise ValueError("Gi* neighbourhood has zero randomisation variance")
        total = sum(weight * value for weight, value in zip(row, x))
        z = (total - mean * sum_w) / (s * sqrt(variance_factor))
        sums.append(total)
        z_scores.append(z)
        p_values.append(erfc(abs(z) / sqrt(2.0)))
    return LocalGiStarResult(tuple(sums), tuple(z_scores), tuple(p_values))

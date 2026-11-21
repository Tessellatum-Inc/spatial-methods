"""Design-based stratified sampling allocation and estimation.

This module implements finite-population stratified simple random sampling
without replacement. It does not generate geographic sample coordinates.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Integral, Real
from typing import Sequence


@dataclass(frozen=True)
class StratifiedEstimate:
    """Point and variance estimates for a stratified finite population."""

    total_estimate: float
    mean_estimate: float
    total_variance_estimate: float
    mean_variance_estimate: float
    stratum_variance_contributions: tuple[float, ...]


def _positive_ints(values: Sequence[int], name: str) -> list[int]:
    if isinstance(values, (str, bytes)) or not values:
        raise ValueError(f"{name} must be a non-empty sequence")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, Integral) or value <= 0:
            raise ValueError(f"{name} must contain positive integers")
        result.append(int(value))
    return result


def _finite_nonnegative(values: Sequence[float], name: str) -> list[float]:
    if isinstance(values, (str, bytes)) or not values:
        raise ValueError(f"{name} must be a non-empty sequence")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must contain finite non-negative numbers")
        number = float(value)
        if not math.isfinite(number) or number < 0:
            raise ValueError(f"{name} must contain finite non-negative numbers")
        result.append(number)
    return result


def neyman_allocation(
    population_sizes: Sequence[int],
    standard_deviations: Sequence[float],
    sample_size: int,
) -> tuple[int, ...]:
    """Allocate a fixed-size stratified sample by Neyman's rule.

    For equal per-unit costs, continuous allocations are proportional to
    N_h*S_h. Integer counts use a deterministic largest-remainder procedure.
    At least one unit is assigned to every stratum, and no stratum is allocated
    more units than its finite population contains.

    If every pilot standard deviation is zero, proportional allocation by
    population size is used as a documented fallback. Pilot values are
    planning inputs, not evidence about the realised sample.
    """
    sizes = _positive_ints(population_sizes, "population_sizes")
    spreads = _finite_nonnegative(standard_deviations, "standard_deviations")
    if len(sizes) != len(spreads):
        raise ValueError("population_sizes and standard_deviations must align")
    if isinstance(sample_size, bool) or not isinstance(sample_size, Integral):
        raise ValueError("sample_size must be an integer")
    sample_size = int(sample_size)
    strata = len(sizes)
    if sample_size < strata or sample_size > sum(sizes):
        raise ValueError("sample_size must be between the number of strata and population total")

    weights = [n * s for n, s in zip(sizes, spreads)]
    if math.fsum(weights) == 0:
        weights = [float(n) for n in sizes]

    allocation = [1] * strata
    remaining = sample_size - strata
    while remaining:
        eligible = [i for i in range(strata) if allocation[i] < sizes[i]]
        if not eligible:
            raise ValueError("sample_size exceeds remaining stratum capacity")
        active_weights = [weights[i] for i in eligible]
        if math.fsum(active_weights) == 0:
            active_weights = [float(sizes[i] - allocation[i]) for i in eligible]
        weight_sum = math.fsum(active_weights)
        quotas = [remaining * weight / weight_sum for weight in active_weights]
        floors = [min(sizes[i] - allocation[i], math.floor(q))
                  for i, q in zip(eligible, quotas)]
        placed = sum(floors)
        for i, count in zip(eligible, floors):
            allocation[i] += count
        remaining -= placed
        if remaining == 0:
            break

        fractions = [q - math.floor(q) for q in quotas]
        order = sorted(
            range(len(eligible)),
            key=lambda j: (-fractions[j], eligible[j]),
        )
        progressed = False
        for j in order:
            i = eligible[j]
            if remaining == 0:
                break
            if allocation[i] < sizes[i]:
                allocation[i] += 1
                remaining -= 1
                progressed = True
        if not progressed and placed == 0:
            raise ValueError("could not allocate remaining sample within stratum capacities")

    return tuple(allocation)


def stratified_total_estimate(
    population_sizes: Sequence[int],
    sample_sizes: Sequence[int],
    sample_means: Sequence[float],
    sample_standard_deviations: Sequence[float],
) -> StratifiedEstimate:
    """Estimate a stratified total/mean and their design-based variances.

    Assumes independent simple random sampling without replacement within
    each stratum. For a non-census stratum, at least two observations are
    required to estimate its sample variance. A census stratum contributes
    zero sampling variance.
    """
    sizes = _positive_ints(population_sizes, "population_sizes")
    counts = _positive_ints(sample_sizes, "sample_sizes")
    means = _finite_nonnegative(sample_means, "sample_means")
    spreads = _finite_nonnegative(sample_standard_deviations, "sample_standard_deviations")
    if not (len(sizes) == len(counts) == len(means) == len(spreads)):
        raise ValueError("all stratum input sequences must have equal length")
    if any(n > N for N, n in zip(sizes, counts)):
        raise ValueError("sample_sizes cannot exceed population_sizes")

    total = math.fsum(N * mean for N, mean in zip(sizes, means))
    contributions = []
    for N, n, sd in zip(sizes, counts, spreads):
        if n == N:
            contributions.append(0.0)
        elif n < 2:
            raise ValueError("non-census strata require at least two observations for variance estimation")
        else:
            contributions.append((N ** 2) * (1.0 - n / N) * (sd ** 2) / n)
    variance = math.fsum(contributions)
    population = sum(sizes)
    values = (total, variance, total / population, variance / (population ** 2))
    if any(not math.isfinite(value) for value in values):
        raise ValueError("estimate or variance overflowed to a non-finite value")
    return StratifiedEstimate(
        total_estimate=values[0],
        mean_estimate=values[2],
        total_variance_estimate=values[1],
        mean_variance_estimate=values[3],
        stratum_variance_contributions=tuple(contributions),
    )

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


def _finite_numbers(values: Sequence[float], name: str, *, nonnegative: bool = False) -> list[float]:
    if isinstance(values, (str, bytes)) or not values:
        raise ValueError(f"{name} must be a non-empty sequence")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must contain finite numeric values")
        number = float(value)
        if not math.isfinite(number) or (nonnegative and number < 0):
            qualifier = " non-negative" if nonnegative else ""
            raise ValueError(f"{name} must contain finite{qualifier} numeric values")
        result.append(number)
    return result


def neyman_allocation(
    population_sizes: Sequence[int],
    standard_deviations: Sequence[float],
    sample_size: int,
) -> tuple[int, ...]:
    """Allocate a fixed-size stratified sample by Neyman's rule.

    For equal per-unit costs, continuous allocations are proportional to
    N_h*S_h. Integer counts use largest-remainder apportionment of the
    continuous allocation, subject to at least one unit per stratum and
    finite-population upper bounds.

    If every pilot standard deviation is zero, proportional allocation by
    population size is used as a documented fallback. Pilot values are
    planning inputs, not evidence about the realised sample.
    """
    sizes = _positive_ints(population_sizes, "population_sizes")
    spreads = _finite_numbers(standard_deviations, "standard_deviations", nonnegative=True)
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

    allocation = [0] * strata
    remaining = sample_size
    active = [i for i, capacity in enumerate(sizes) if capacity > 0]

    # Fix strata whose unconstrained quota violates a lower or upper bound,
    # then recompute the remaining continuous allocation over the active set.
    while active:
        active_weights = [weights[i] for i in active]
        if math.fsum(active_weights) == 0:
            active_weights = [float(sizes[i] - allocation[i]) for i in active]
        weight_sum = math.fsum(active_weights)
        quotas = [remaining * weight / weight_sum for weight in active_weights]
        fixed = []
        for position, (i, quota) in enumerate(zip(active, quotas)):
            capacity = sizes[i] - allocation[i]
            if quota < 1.0:
                allocation[i] += 1
                remaining -= 1
                fixed.append(i)
            elif quota > capacity:
                allocation[i] += capacity
                remaining -= capacity
                fixed.append(i)
        if fixed:
            fixed_set = set(fixed)
            active = [i for i in active if i not in fixed_set]
            continue

        floors = [math.floor(quota) for quota in quotas]
        for i, count in zip(active, floors):
            allocation[i] += count
        remaining -= sum(floors)
        fractions_order = sorted(
            range(len(active)),
            key=lambda position: (-(quotas[position] - floors[position]), active[position]),
        )
        for position in fractions_order:
            if remaining == 0:
                break
            i = active[position]
            if allocation[i] < sizes[i]:
                allocation[i] += 1
                remaining -= 1
        break

    if remaining != 0 or sum(allocation) != sample_size:
        raise ValueError("could not allocate requested sample within stratum bounds")
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
    means = _finite_numbers(sample_means, "sample_means")
    spreads = _finite_numbers(sample_standard_deviations, "sample_standard_deviations", nonnegative=True)
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

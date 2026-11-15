"""Circular Poisson spatial scan statistic for areal case counts."""
from __future__ import annotations

from math import isfinite, log
import numpy as np


def _scan_inputs(coordinates, cases, population, max_population_fraction, min_cases):
    coords = np.asarray(coordinates, dtype=float)
    case_counts = np.asarray(cases, dtype=float)
    pop = np.asarray(population, dtype=float)
    if (
        coords.ndim != 2 or coords.shape[1] != 2 or coords.shape[0] < 2
        or not np.all(np.isfinite(coords))
    ):
        raise ValueError("coordinates must be a finite N-by-2 array with N >= 2")
    n = coords.shape[0]
    if (
        case_counts.shape != (n,) or not np.all(np.isfinite(case_counts))
        or np.any(case_counts < 0) or np.any(case_counts != np.floor(case_counts))
    ):
        raise ValueError("cases must be a matching vector of nonnegative integer counts")
    if pop.shape != (n,) or not np.all(np.isfinite(pop)) or np.any(pop <= 0):
        raise ValueError("population must be a matching vector of positive finite values")
    if case_counts.sum() <= 0 or not isfinite(float(case_counts.sum())):
        raise ValueError("total cases must be finite and positive")
    try:
        upper = float(max_population_fraction)
    except (TypeError, ValueError) as exc:
        raise ValueError("max_population_fraction must be in (0, 1]") from exc
    if not isfinite(upper) or not (0 < upper <= 1):
        raise ValueError("max_population_fraction must be in (0, 1]")
    if (
        isinstance(min_cases, (bool, np.bool_))
        or not isinstance(min_cases, (int, np.integer)) or min_cases < 1
    ):
        raise ValueError("min_cases must be a positive integer")
    total_pop = float(pop.sum())
    if not isfinite(total_pop) or total_pop <= 0:
        raise ValueError("total population must be finite and positive")
    return coords, case_counts.astype(int), pop, upper, int(min_cases)


def _log_ratio_term(observed, expected):
    if observed == 0:
        return 0.0
    if expected <= 0:
        return np.inf
    return float(observed * log(observed / expected))


def poisson_spatial_scan(
    coordinates,
    cases,
    population,
    *,
    max_population_fraction=0.5,
    min_cases=2,
):
    """Find the highest-likelihood elevated circular Poisson cluster.

    Candidate circles are centred on each areal centroid and expand through
    sorted centroid distances. The null expectation inside a zone is the total
    case count multiplied by the zone's share of total population.
    """
    coords, case_counts, pop, upper, min_cases = _scan_inputs(
        coordinates, cases, population, max_population_fraction, min_cases
    )
    total_cases = int(case_counts.sum())
    total_pop = float(pop.sum())
    best = {
        "log_likelihood_ratio": 0.0,
        "relative_risk": float("nan"),
        "center_index": None,
        "radius": None,
        "member_indices": (),
        "cases_inside": 0,
        "population_inside": 0.0,
        "expected_cases_inside": 0.0,
        "total_cases": total_cases,
        "total_population": total_pop,
    }

    for center in range(len(case_counts)):
        delta = coords - coords[center]
        distances = np.sqrt(np.sum(delta * delta, axis=1))
        if not np.all(np.isfinite(distances)):
            raise ValueError("coordinate range produces non-finite pair distances")
        order = np.argsort(distances, kind="stable")
        sorted_distances = distances[order]
        cumulative_cases = np.cumsum(case_counts[order])
        cumulative_population = np.cumsum(pop[order])

        start = 0
        while start < len(order):
            radius = float(sorted_distances[start])
            tolerance = 1e-12 * max(1.0, abs(radius))
            end = start + 1
            while (
                end < len(order)
                and abs(float(sorted_distances[end]) - radius) <= tolerance
            ):
                end += 1

            cases_inside = int(cumulative_cases[end - 1])
            population_inside = float(cumulative_population[end - 1])
            population_fraction = population_inside / total_pop
            if (
                population_fraction <= upper + 1e-12
                and population_inside < total_pop - 1e-12
                and cases_inside >= min_cases
            ):
                expected_inside = total_cases * population_fraction
                cases_outside = total_cases - cases_inside
                expected_outside = total_cases - expected_inside
                if cases_inside > expected_inside:
                    llr = (
                        _log_ratio_term(cases_inside, expected_inside)
                        + _log_ratio_term(cases_outside, expected_outside)
                    )
                    llr = max(0.0, llr)
                    if llr > best["log_likelihood_ratio"] + 1e-14:
                        population_outside = total_pop - population_inside
                        risk_inside = cases_inside / population_inside
                        risk_outside = cases_outside / population_outside
                        relative_risk = (
                            risk_inside / risk_outside
                            if risk_outside > 0 else float("inf")
                        )
                        best = {
                            "log_likelihood_ratio": llr,
                            "relative_risk": relative_risk,
                            "center_index": center,
                            "radius": radius,
                            "member_indices": tuple(
                                sorted(int(i) for i in order[:end])
                            ),
                            "cases_inside": cases_inside,
                            "population_inside": population_inside,
                            "expected_cases_inside": expected_inside,
                            "total_cases": total_cases,
                            "total_population": total_pop,
                        }
            start = end
    return best


def monte_carlo_poisson_scan(
    coordinates,
    cases,
    population,
    *,
    n_simulations=999,
    max_population_fraction=0.5,
    min_cases=2,
    rng=None,
):
    """Condition on total cases and estimate a Monte Carlo scan p-value."""
    coords, case_counts, pop, upper, min_cases = _scan_inputs(
        coordinates, cases, population, max_population_fraction, min_cases
    )
    if (
        isinstance(n_simulations, (bool, np.bool_))
        or not isinstance(n_simulations, (int, np.integer))
        or n_simulations < 1
    ):
        raise ValueError("n_simulations must be a positive integer")

    observed = poisson_spatial_scan(
        coords, case_counts, pop,
        max_population_fraction=upper,
        min_cases=min_cases,
    )
    generator = np.random.default_rng(rng)
    probabilities = pop / pop.sum()
    maxima = np.empty(int(n_simulations), dtype=float)
    for simulation in range(int(n_simulations)):
        simulated_cases = generator.multinomial(int(case_counts.sum()), probabilities)
        maxima[simulation] = poisson_spatial_scan(
            coords, simulated_cases, pop,
            max_population_fraction=upper,
            min_cases=min_cases,
        )["log_likelihood_ratio"]
    exceedances = int(np.count_nonzero(
        maxima >= observed["log_likelihood_ratio"] - 1e-14
    ))
    return {
        "observed": observed,
        "p_value": (1 + exceedances) / (int(n_simulations) + 1),
        "n_simulations": int(n_simulations),
        "simulated_maxima": maxima,
    }

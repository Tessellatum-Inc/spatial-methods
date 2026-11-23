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



def _log_combination(n, k):
    """Log binomial coefficient for integer arguments."""
    from math import lgamma
    if k < 0 or k > n:
        return float("-inf")
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def _hypergeometric_upper_tail(population, zone_population, total_cases, observed):
    """P[X >= observed] for X~Hypergeometric(N, K, n), in log space."""
    from math import exp, log
    lower = max(0, total_cases - (population - zone_population), observed)
    upper = min(zone_population, total_cases)
    if lower > upper:
        return 0.0
    denominator = _log_combination(population, total_cases)
    logs = [
        _log_combination(zone_population, x)
        + _log_combination(population - zone_population, total_cases - x)
        - denominator
        for x in range(lower, upper + 1)
    ]
    peak = max(logs)
    probability = exp(peak) * sum(exp(value - peak) for value in logs)
    return min(1.0, max(0.0, probability))


def besag_newell_scan(coordinates, cases, population, *, k=10, alpha=0.05):
    """Area-centred Besag-Newell local scan with an exact hypergeometric tail.

    For each centroid, add the centre and then all equidistant nearest-centroid
    ties until at least k cases are included. The local tail probability is
    computed under fixed-total case allocation without replacement from the
    total population. This is an area-centred formulation; it does not claim
    to reproduce every case-centred convention in the 1991 paper.
    """
    coords = np.asarray(coordinates, dtype=float)
    case_counts = np.asarray(cases, dtype=float)
    pop = np.asarray(population, dtype=float)
    if (coords.ndim != 2 or coords.shape[1] != 2 or coords.shape[0] < 2
            or not np.all(np.isfinite(coords))):
        raise ValueError("coordinates must be a finite N-by-2 array with N >= 2")
    n = len(coords)
    if (case_counts.shape != (n,) or not np.all(np.isfinite(case_counts))
            or np.any(case_counts < 0) or np.any(case_counts != np.floor(case_counts))):
        raise ValueError("cases must be a matching vector of nonnegative integer counts")
    if (pop.shape != (n,) or not np.all(np.isfinite(pop))
            or np.any(pop <= 0) or np.any(pop != np.floor(pop))):
        raise ValueError("population must be a matching vector of positive integer counts")
    if (isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer))
            or k < 1 or k > int(case_counts.sum())):
        raise ValueError("k must be a positive integer no greater than total cases")
    level = float(alpha)
    if not isfinite(level) or not 0 < level < 1:
        raise ValueError("alpha must be in (0, 1)")
    total_population = int(pop.sum())
    total_cases = int(case_counts.sum())
    if total_population < total_cases:
        raise ValueError("total population must be at least total cases")

    results = []
    for centre in range(n):
        delta = coords - coords[centre]
        distances = np.sqrt(np.sum(delta * delta, axis=1))
        if not np.all(np.isfinite(distances)):
            raise ValueError("coordinate range produces non-finite pair distances")
        order = np.argsort(distances, kind="stable")
        cumulative_cases = 0
        cumulative_population = 0
        members = []
        cursor = 0
        while cursor < n and cumulative_cases < int(k):
            radius = float(distances[order[cursor]])
            tolerance = 1e-12 * max(1.0, abs(radius))
            end = cursor + 1
            while end < n and abs(float(distances[order[end]]) - radius) <= tolerance:
                end += 1
            tied = [int(i) for i in order[cursor:end]]
            members.extend(tied)
            cumulative_cases += int(case_counts[tied].sum())
            cumulative_population += int(pop[tied].sum())
            cursor = end
        if cumulative_cases < int(k):
            raise RuntimeError("all areas were exhausted before reaching k cases")
        p_value = _hypergeometric_upper_tail(
            total_population, cumulative_population, total_cases, cumulative_cases
        )
        results.append({
            "center_index": centre,
            "member_indices": tuple(sorted(members)),
            "n_areas": len(members),
            "radius": radius,
            "cases_inside": cumulative_cases,
            "population_inside": cumulative_population,
            "expected_cases_inside": total_cases * cumulative_population / total_population,
            "p_value": p_value,
            "is_cluster": p_value <= level,
        })
    return {
        "local_results": results,
        "significant_centres": tuple(r["center_index"] for r in results if r["is_cluster"]),
        "n_significant": sum(r["is_cluster"] for r in results),
        "k": int(k),
        "alpha": level,
        "total_cases": total_cases,
        "total_population": total_population,
    }


def monte_carlo_besag_newell(coordinates, cases, population, *, k=10, alpha=0.05,
                             n_simulations=999, rng=None):
    """Calibrate the number of significant centres under fixed-total CSR risk.

    Each replicate reallocates the observed total cases multinomially in
    proportion to area population and reruns every local Besag-Newell test.
    The returned global p-value uses the plus-one correction.
    """
    coords = np.asarray(coordinates, dtype=float)
    case_counts = np.asarray(cases, dtype=float)
    pop = np.asarray(population, dtype=float)
    observed = besag_newell_scan(coords, case_counts, pop, k=k, alpha=alpha)
    if (isinstance(n_simulations, (bool, np.bool_))
            or not isinstance(n_simulations, (int, np.integer)) or n_simulations < 1):
        raise ValueError("n_simulations must be a positive integer")
    generator = np.random.default_rng(rng)
    probabilities = pop / pop.sum()
    simulated_counts = np.empty(int(n_simulations), dtype=int)
    for i in range(int(n_simulations)):
        simulated = generator.multinomial(observed["total_cases"], probabilities)
        simulated_counts[i] = besag_newell_scan(
            coords, simulated, pop, k=k, alpha=alpha
        )["n_significant"]
    exceedances = int(np.count_nonzero(
        simulated_counts >= observed["n_significant"]
    ))
    return {
        "observed": observed,
        "simulated_significant_counts": simulated_counts,
        "p_value": (1 + exceedances) / (int(n_simulations) + 1),
        "n_simulations": int(n_simulations),
        "exceedances": exceedances,
    }



def tango_statistic(coordinates, cases, population, *, phi):
    """Compute Tango's global quadratic-form clustering statistic.

    A_ij = exp(-d_ij / phi), r_i = cases_i / total_cases and
    p_i = population_i / total_population. Larger values indicate stronger
    spatial concentration of deviations from the constant-risk expectation.
    """
    coords = np.asarray(coordinates, dtype=float)
    case_counts = np.asarray(cases, dtype=float)
    pop = np.asarray(population, dtype=float)
    if (coords.ndim != 2 or coords.shape[1] != 2 or coords.shape[0] < 2
            or not np.all(np.isfinite(coords))):
        raise ValueError("coordinates must be a finite N-by-2 array with N >= 2")
    n = len(coords)
    if (case_counts.shape != (n,) or not np.all(np.isfinite(case_counts))
            or np.any(case_counts < 0) or np.any(case_counts != np.floor(case_counts))):
        raise ValueError("cases must be a matching vector of nonnegative integer counts")
    if (pop.shape != (n,) or not np.all(np.isfinite(pop))
            or np.any(pop <= 0)):
        raise ValueError("population must be a matching vector of positive finite values")
    total_cases = float(case_counts.sum())
    total_population = float(pop.sum())
    if not isfinite(total_cases) or total_cases <= 0:
        raise ValueError("total cases must be finite and positive")
    if not isfinite(total_population) or total_population <= 0:
        raise ValueError("total population must be finite and positive")
    scale = float(phi)
    if not isfinite(scale) or scale <= 0:
        raise ValueError("phi must be finite and positive")
    delta = coords[:, None, :] - coords[None, :, :]
    distances = np.sqrt(np.sum(delta * delta, axis=2))
    if not np.all(np.isfinite(distances)):
        raise ValueError("coordinate range produces non-finite pair distances")
    closeness = np.exp(-distances / scale)
    observed = case_counts / total_cases
    expected = pop / total_population
    residual = observed - expected
    statistic = float(residual @ closeness @ residual)
    return {
        "statistic": statistic,
        "observed_proportions": observed,
        "expected_proportions": expected,
        "residuals": residual,
        "closeness_matrix": closeness,
        "phi": scale,
    }


def monte_carlo_tango_test(coordinates, cases, population, *, phi,
                           n_simulations=999, rng=None):
    """Conditional multinomial Monte Carlo test for Tango's global statistic."""
    observed = tango_statistic(coordinates, cases, population, phi=phi)
    case_counts = np.asarray(cases, dtype=int)
    pop = np.asarray(population, dtype=float)
    if (isinstance(n_simulations, (bool, np.bool_))
            or not isinstance(n_simulations, (int, np.integer))
            or n_simulations < 1):
        raise ValueError("n_simulations must be a positive integer")
    generator = np.random.default_rng(rng)
    probabilities = pop / pop.sum()
    total_cases = int(case_counts.sum())
    maxima = np.empty(int(n_simulations), dtype=float)
    for i in range(int(n_simulations)):
        simulated = generator.multinomial(total_cases, probabilities)
        maxima[i] = tango_statistic(
            coordinates, simulated, pop, phi=phi
        )["statistic"]
    exceedances = int(np.count_nonzero(
        maxima >= observed["statistic"] - 1e-14
    ))
    return {
        "observed": observed,
        "simulated_statistics": maxima,
        "p_value": (1 + exceedances) / (int(n_simulations) + 1),
        "n_simulations": int(n_simulations),
        "exceedances": exceedances,
    }



def _ellipse_controls(shape_ratios, angles_degrees):
    try:
        shapes = np.asarray(shape_ratios, dtype=float)
        angles = np.asarray(angles_degrees, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("shape ratios and angles must be finite numeric sequences") from exc
    if (shapes.ndim != 1 or shapes.size == 0 or not np.all(np.isfinite(shapes))
            or np.any(shapes < 1)):
        raise ValueError("shape_ratios must be a nonempty sequence of finite values >= 1")
    if (angles.ndim != 1 or angles.size == 0 or not np.all(np.isfinite(angles))
            or np.any(angles < 0) or np.any(angles >= 180)):
        raise ValueError("angles_degrees must be a nonempty sequence in [0, 180)")
    return np.unique(shapes), np.unique(angles)


def elliptical_poisson_scan(
    coordinates,
    cases,
    population,
    *,
    shape_ratios=(1.0, 2.0, 3.0),
    angles_degrees=(0.0, 30.0, 60.0, 90.0, 120.0, 150.0),
    max_population_fraction=0.5,
    min_cases=2,
):
    """Scan a finite grid of centroid-centred elliptical Poisson windows.

    For each centroid, shape ratio and orientation, areas are ordered by the
    ellipse's normalized radial coordinate. Candidate zones are nested
    prefixes, retaining all numerical ties. This is a finite-grid teaching
    implementation, not a bit-for-bit reproduction of SaTScan's candidate
    generation or eccentricity-penalty options.
    """
    coords, case_counts, pop, upper, min_cases = _scan_inputs(
        coordinates, cases, population, max_population_fraction, min_cases
    )
    shapes, angles = _ellipse_controls(shape_ratios, angles_degrees)
    total_cases = int(case_counts.sum())
    total_pop = float(pop.sum())
    best = {
        "log_likelihood_ratio": 0.0,
        "relative_risk": float("nan"),
        "center_index": None,
        "shape_ratio": None,
        "angle_degrees": None,
        "semi_major_axis": None,
        "semi_minor_axis": None,
        "member_indices": (),
        "cases_inside": 0,
        "population_inside": 0.0,
        "expected_cases_inside": 0.0,
        "total_cases": total_cases,
        "total_population": total_pop,
    }
    for center in range(len(case_counts)):
        delta = coords - coords[center]
        for shape in shapes:
            for angle in angles:
                radians = np.deg2rad(angle)
                cosine, sine = np.cos(radians), np.sin(radians)
                along_major = delta[:, 0] * cosine + delta[:, 1] * sine
                along_minor = -delta[:, 0] * sine + delta[:, 1] * cosine
                radial = np.sqrt((along_major / shape) ** 2 + along_minor ** 2)
                if not np.all(np.isfinite(radial)):
                    raise ValueError("coordinate range produces non-finite ellipse distances")
                order = np.argsort(radial, kind="stable")
                sorted_radial = radial[order]
                cumulative_cases = np.cumsum(case_counts[order])
                cumulative_population = np.cumsum(pop[order])
                start = 0
                while start < len(order):
                    threshold = float(sorted_radial[start])
                    tolerance = 1e-12 * max(1.0, abs(threshold))
                    end = start + 1
                    while (end < len(order)
                           and abs(float(sorted_radial[end]) - threshold) <= tolerance):
                        end += 1
                    cases_inside = int(cumulative_cases[end - 1])
                    population_inside = float(cumulative_population[end - 1])
                    fraction = population_inside / total_pop
                    if (fraction <= upper + 1e-12
                            and population_inside < total_pop - 1e-12
                            and cases_inside >= min_cases):
                        expected_inside = total_cases * fraction
                        cases_outside = total_cases - cases_inside
                        expected_outside = total_cases - expected_inside
                        if cases_inside > expected_inside:
                            llr = (
                                _log_ratio_term(cases_inside, expected_inside)
                                + _log_ratio_term(cases_outside, expected_outside)
                            )
                            llr = max(0.0, llr)
                            if llr > best["log_likelihood_ratio"] + 1e-14:
                                outside_population = total_pop - population_inside
                                risk_inside = cases_inside / population_inside
                                risk_outside = cases_outside / outside_population
                                best = {
                                    "log_likelihood_ratio": llr,
                                    "relative_risk": (
                                        risk_inside / risk_outside
                                        if risk_outside > 0 else float("inf")
                                    ),
                                    "center_index": center,
                                    "shape_ratio": float(shape),
                                    "angle_degrees": float(angle),
                                    "semi_major_axis": float(shape * threshold),
                                    "semi_minor_axis": float(threshold),
                                    "member_indices": tuple(sorted(int(i) for i in order[:end])),
                                    "cases_inside": cases_inside,
                                    "population_inside": population_inside,
                                    "expected_cases_inside": expected_inside,
                                    "total_cases": total_cases,
                                    "total_population": total_pop,
                                }
                    start = end
    return best


def monte_carlo_elliptical_poisson_scan(
    coordinates,
    cases,
    population,
    *,
    n_simulations=999,
    shape_ratios=(1.0, 2.0, 3.0),
    angles_degrees=(0.0, 30.0, 60.0, 90.0, 120.0, 150.0),
    max_population_fraction=0.5,
    min_cases=2,
    rng=None,
):
    """Condition on total cases and calibrate the maximum over all ellipses."""
    coords, case_counts, pop, upper, minimum = _scan_inputs(
        coordinates, cases, population, max_population_fraction, min_cases
    )
    if (isinstance(n_simulations, (bool, np.bool_))
            or not isinstance(n_simulations, (int, np.integer))
            or n_simulations < 1):
        raise ValueError("n_simulations must be a positive integer")
    # Validate candidate controls once before spending time on simulations.
    shapes, angles = _ellipse_controls(shape_ratios, angles_degrees)
    observed = elliptical_poisson_scan(
        coords, case_counts, pop,
        shape_ratios=shapes, angles_degrees=angles,
        max_population_fraction=upper, min_cases=minimum,
    )
    generator = np.random.default_rng(rng)
    probabilities = pop / pop.sum()
    maxima = np.empty(int(n_simulations), dtype=float)
    for i in range(int(n_simulations)):
        simulated = generator.multinomial(int(case_counts.sum()), probabilities)
        maxima[i] = elliptical_poisson_scan(
            coords, simulated, pop,
            shape_ratios=shapes, angles_degrees=angles,
            max_population_fraction=upper, min_cases=minimum,
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



def _flexible_scan_inputs(coordinates, cases, population, adjacency,
                          max_cluster_size, max_population_fraction, min_cases):
    coords, case_counts, pop, upper, minimum = _scan_inputs(
        coordinates, cases, population, max_population_fraction, min_cases
    )
    try:
        graph = np.asarray(adjacency, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("adjacency must be a finite numeric matrix") from exc
    n = len(coords)
    if graph.shape != (n, n):
        raise ValueError("adjacency must be an N-by-N matrix matching coordinates")
    if not np.all(np.isfinite(graph)):
        raise ValueError("adjacency must contain only finite values")
    graph = graph.astype(bool)
    if np.any(np.diag(graph)):
        raise ValueError("adjacency diagonal must be false")
    if not np.array_equal(graph, graph.T):
        raise ValueError("adjacency must be symmetric and undirected")
    if (isinstance(max_cluster_size, (bool, np.bool_))
            or not isinstance(max_cluster_size, (int, np.integer))
            or not 1 <= max_cluster_size <= min(n, 15)):
        raise ValueError("max_cluster_size must be an integer in [1, min(N, 15)]")
    return coords, case_counts, pop, graph, int(max_cluster_size), upper, minimum


def flexible_poisson_scan(
    coordinates,
    cases,
    population,
    adjacency,
    *,
    max_cluster_size=8,
    max_population_fraction=0.5,
    min_cases=2,
):
    """Exhaustively scan connected irregular zones in a bounded local universe.

    For each root area, the candidate universe is the root plus its
    max_cluster_size-1 nearest centroid neighbours. Every connected subset
    containing the root, up to max_cluster_size areas, is enumerated exactly
    once. Connectivity is defined by the supplied symmetric adjacency graph.
    The explicit size limit keeps this exponential teaching baseline bounded.
    """
    (coords, case_counts, pop, graph, maximum, upper,
     minimum) = _flexible_scan_inputs(
        coordinates, cases, population, adjacency, max_cluster_size,
        max_population_fraction, min_cases
    )
    total_cases = int(case_counts.sum())
    total_pop = float(pop.sum())
    best = {
        "log_likelihood_ratio": 0.0,
        "relative_risk": float("nan"),
        "root_index": None,
        "member_indices": (),
        "n_areas": 0,
        "cases_inside": 0,
        "population_inside": 0.0,
        "expected_cases_inside": 0.0,
        "total_cases": total_cases,
        "total_population": total_pop,
    }
    for root in range(len(coords)):
        distances = np.sqrt(np.sum((coords - coords[root]) ** 2, axis=1))
        if not np.all(np.isfinite(distances)):
            raise ValueError("coordinate range produces non-finite centroid distances")
        order = np.argsort(distances, kind="stable")
        nearest = [int(i) for i in order if int(i) != root][:maximum - 1]
        universe = {root, *nearest}
        seen = {frozenset((root,))}
        stack = [frozenset((root,))]
        while stack:
            zone = stack.pop()
            members = tuple(sorted(zone))
            cases_inside = int(case_counts[list(members)].sum())
            population_inside = float(pop[list(members)].sum())
            fraction = population_inside / total_pop
            if (len(zone) <= maximum and fraction <= upper + 1e-12
                    and population_inside < total_pop - 1e-12
                    and cases_inside >= minimum):
                expected_inside = total_cases * fraction
                cases_outside = total_cases - cases_inside
                expected_outside = total_cases - expected_inside
                if cases_inside > expected_inside:
                    llr = (
                        _log_ratio_term(cases_inside, expected_inside)
                        + _log_ratio_term(cases_outside, expected_outside)
                    )
                    llr = max(0.0, llr)
                    if llr > best["log_likelihood_ratio"] + 1e-14:
                        risk_inside = cases_inside / population_inside
                        risk_outside = cases_outside / (total_pop - population_inside)
                        best = {
                            "log_likelihood_ratio": llr,
                            "relative_risk": (
                                risk_inside / risk_outside
                                if risk_outside > 0 else float("inf")
                            ),
                            "root_index": root,
                            "member_indices": members,
                            "n_areas": len(members),
                            "cases_inside": cases_inside,
                            "population_inside": population_inside,
                            "expected_cases_inside": expected_inside,
                            "total_cases": total_cases,
                            "total_population": total_pop,
                        }
            if len(zone) >= maximum:
                continue
            frontier = set()
            for member in zone:
                frontier.update(int(j) for j in np.flatnonzero(graph[member]))
            frontier.intersection_update(universe)
            frontier.difference_update(zone)
            for candidate in sorted(frontier, reverse=True):
                expanded = frozenset((*zone, candidate))
                if expanded not in seen:
                    seen.add(expanded)
                    stack.append(expanded)
    best["max_cluster_size"] = maximum
    best["max_population_fraction"] = upper
    return best


def monte_carlo_flexible_poisson_scan(
    coordinates,
    cases,
    population,
    adjacency,
    *,
    n_simulations=999,
    max_cluster_size=8,
    max_population_fraction=0.5,
    min_cases=2,
    rng=None,
):
    """Calibrate the maximum connected-zone LLR under fixed-total risk."""
    (coords, case_counts, pop, graph, maximum, upper,
     minimum) = _flexible_scan_inputs(
        coordinates, cases, population, adjacency, max_cluster_size,
        max_population_fraction, min_cases
    )
    if (isinstance(n_simulations, (bool, np.bool_))
            or not isinstance(n_simulations, (int, np.integer))
            or n_simulations < 1):
        raise ValueError("n_simulations must be a positive integer")
    observed = flexible_poisson_scan(
        coords, case_counts, pop, graph, max_cluster_size=maximum,
        max_population_fraction=upper, min_cases=minimum
    )
    generator = np.random.default_rng(rng)
    probabilities = pop / pop.sum()
    maxima = np.empty(int(n_simulations), dtype=float)
    for i in range(int(n_simulations)):
        simulated = generator.multinomial(int(case_counts.sum()), probabilities)
        maxima[i] = flexible_poisson_scan(
            coords, simulated, pop, graph, max_cluster_size=maximum,
            max_population_fraction=upper, min_cases=minimum
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

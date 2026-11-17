"""Small, dependency-free reference implementation of global Moran's I.

This module computes the statistic only. It does not calculate analytical
or permutation-based significance tests.
"""

from math import isfinite
from typing import Sequence


def _validated_weights(
    weights: Sequence[Sequence[float]], n: int
) -> list[list[float]]:
    """Validate and copy a dense spatial weights matrix."""
    if len(weights) != n:
        raise ValueError("weights must have one row per observation")

    matrix: list[list[float]] = []
    for i, row in enumerate(weights):
        if len(row) != n:
            raise ValueError("weights must be a square n-by-n matrix")

        clean_row: list[float] = []
        for j, raw_weight in enumerate(row):
            weight = float(raw_weight)
            if not isfinite(weight):
                raise ValueError("weights must contain only finite values")
            if weight < 0:
                raise ValueError("weights must be non-negative")
            if i == j and weight != 0:
                raise ValueError("self-weights must be zero")
            clean_row.append(weight)

        matrix.append(clean_row)

    return matrix


def row_standardize(weights: Sequence[Sequence[float]]) -> list[list[float]]:
    """Return row-standardized weights.

    Each nonzero row sums to one. A row with no neighbours remains a row
    of zeros; this represents an island and should be reported by the user.
    """
    n = len(weights)
    if n == 0:
        raise ValueError("weights must contain at least one row")

    matrix = _validated_weights(weights, n)
    standardized: list[list[float]] = []

    for row in matrix:
        row_sum = sum(row)
        if row_sum == 0:
            standardized.append([0.0] * n)
        else:
            standardized.append([weight / row_sum for weight in row])

    return standardized


def morans_i(
    values: Sequence[float], weights: Sequence[Sequence[float]]
) -> float:
    """Calculate global Moran's I for values and a dense weights matrix.

    Args:
        values: One continuous numeric value per spatial unit.
        weights: Dense n-by-n spatial weights matrix. Self-weights must be
            zero and weights must be finite and non-negative.

    Returns:
        The global Moran's I statistic.

    Raises:
        ValueError: If inputs are misaligned, invalid, constant, or contain
            no positive spatial weights.
    """
    n = len(values)
    if n < 2:
        raise ValueError("at least two observations are required")

    x = [float(value) for value in values]
    if not all(isfinite(value) for value in x):
        raise ValueError("values must contain only finite numbers")

    w = _validated_weights(weights, n)
    s0 = sum(sum(row) for row in w)
    if s0 <= 0:
        raise ValueError("the spatial weights matrix must contain a positive weight")

    mean = sum(x) / n
    z = [value - mean for value in x]
    denominator = sum(value * value for value in z)
    if denominator == 0:
        raise ValueError("Moran's I is undefined for a constant variable")

    numerator = sum(
        w[i][j] * z[i] * z[j]
        for i in range(n)
        for j in range(n)
    )

    return (n / s0) * (numerator / denominator)


def morans_i_permutation(
    values: Sequence[float],
    weights: Sequence[Sequence[float]],
    *,
    permutations: int = 999,
    alternative: str = "two-sided",
    seed: int | None = None,
) -> dict:
    """Permutation inference for global Moran's I under random labelling.

    The observed values are randomly reassigned to fixed spatial locations.
    The pseudo-p-value uses the plus-one correction. Two-sided inference is
    centred on the randomisation expectation -1/(n-1), not zero.
    """
    import random

    if not isinstance(permutations, int) or permutations < 1:
        raise ValueError("permutations must be a positive integer")
    if alternative not in {"two-sided", "greater", "less"}:
        raise ValueError("alternative must be two-sided, greater or less")
    x=[float(value) for value in values]
    observed=morans_i(x,weights)
    expected=-1.0/(len(x)-1)
    rng=random.Random(seed)
    simulated=[]
    for _ in range(permutations):
        shuffled=x.copy()
        rng.shuffle(shuffled)
        simulated.append(morans_i(shuffled,weights))
    if alternative=="greater":
        extreme=sum(value>=observed for value in simulated)
    elif alternative=="less":
        extreme=sum(value<=observed for value in simulated)
    else:
        extreme=sum(abs(value-expected)>=abs(observed-expected) for value in simulated)
    p_value=(extreme+1)/(permutations+1)
    mean=sum(simulated)/permutations
    variance=sum((value-mean)**2 for value in simulated)/(permutations-1) if permutations>1 else 0.0
    return {"statistic":observed,"expected":expected,"p_value":p_value,
            "alternative":alternative,"permutations":permutations,
            "simulated":simulated,"simulation_mean":mean,
            "simulation_std":variance**0.5}



def morans_i_correlogram(
    points: Sequence[Sequence[float]],
    values: Sequence[float],
    distance_edges: Sequence[float],
    *,
    row_standardize_weights: bool = False,
    permutations: int = 0,
    seed: int | None = 0,
    confidence_level: float = 0.95,
) -> list[dict]:
    """Compute global Moran statistics over non-overlapping distance bands."""
    import math
    import random
    n = len(values)
    if n < 2:
        raise ValueError("at least two observations are required")
    if len(points) != n or any(len(point) != 2 for point in points):
        raise ValueError("points must contain one 2D coordinate per value")
    xy = [[float(point[0]), float(point[1])] for point in points]
    if not all(isfinite(v) for point in xy for v in point):
        raise ValueError("coordinates must be finite")
    x = [float(v) for v in values]
    if not all(isfinite(v) for v in x):
        raise ValueError("values must be finite")
    edges = [float(v) for v in distance_edges]
    if len(edges) < 2 or not all(isfinite(v) for v in edges):
        raise ValueError("distance_edges must contain at least two finite values")
    if edges[0] < 0 or any(a >= b for a, b in zip(edges, edges[1:])):
        raise ValueError("distance_edges must be non-negative and strictly increasing")
    if isinstance(permutations, bool) or not isinstance(permutations, int) or permutations < 0:
        raise ValueError("permutations must be a non-negative integer")
    if permutations and seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise ValueError("seed must be an integer or None")
    if isinstance(confidence_level, bool) or not isfinite(float(confidence_level)) or not 0 < float(confidence_level) < 1:
        raise ValueError("confidence_level must lie strictly between zero and one")
    if permutations and sum((v - sum(x) / n) ** 2 for v in x) == 0:
        raise ValueError("Moran correlogram is undefined for a constant variable")
    pairs = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            distance = math.hypot(xy[j][0] - xy[i][0], xy[j][1] - xy[i][1])
            if not isfinite(distance):
                raise ValueError("pair distance overflowed")
            pairs.append((distance, i, j))
    output = []
    band_weights = []
    for band, (lower, upper) in enumerate(zip(edges, edges[1:])):
        weights = [[0.0] * n for _ in range(n)]
        selected = 0
        for distance, i, j in pairs:
            inside = distance >= lower and (
                distance <= upper if band == len(edges) - 2 else distance < upper
            )
            if inside:
                weights[i][j] = weights[j][i] = 1.0
                selected += 1
        if selected and row_standardize_weights:
            weights = row_standardize(weights)
        statistic = morans_i(x, weights) if selected else None
        band_weights.append(weights if selected else None)
        output.append({"lower": lower, "upper": upper, "pairs": selected,
                       "statistic": statistic, "expected": -1.0 / (n - 1),
                       "simultaneous_lower": None, "simultaneous_upper": None,
                       "confidence_level": None, "maxT_critical_value": None})
    if permutations:
        rng = random.Random(seed)
        simulated = [[] for _ in output]
        for _ in range(permutations):
            shuffled = x.copy()
            rng.shuffle(shuffled)
            for index, weights in enumerate(band_weights):
                if weights is not None:
                    simulated[index].append(morans_i(shuffled, weights))
        valid = []
        for index, record in enumerate(output):
            if record["statistic"] is None:
                record.update({"simulation_mean": None, "simulation_std": None,
                               "z_score": None, "p_value": None, "p_value_maxT": None})
                continue
            values_sim = simulated[index]
            sim_mean = sum(values_sim) / permutations
            sim_var = (sum((value - sim_mean) ** 2 for value in values_sim) /
                       (permutations - 1)) if permutations > 1 else 0.0
            sim_std = math.sqrt(sim_var)
            expected = record["expected"]
            observed = record["statistic"]
            extreme = sum(abs(value - expected) >= abs(observed - expected)
                          for value in values_sim)
            p_value = (extreme + 1) / (permutations + 1)
            z_score = (observed - expected) / sim_std if sim_std > 0 else None
            record.update({"simulation_mean": sim_mean, "simulation_std": sim_std,
                           "z_score": z_score, "p_value": p_value, "p_value_maxT": None})
            if sim_std > 0:
                valid.append((index, z_score,
                              [(value - expected) / sim_std for value in values_sim]))
        max_statistics = ([max(abs(valid[j][2][rep]) for j in range(len(valid)))
                           for rep in range(permutations)] if valid else [])
        if max_statistics:
            rank = int(math.floor((permutations + 1) * float(confidence_level))) + 1
            critical = (sorted(max_statistics)[rank - 1]
                        if rank <= permutations else math.inf)
        else:
            critical = 0.0
        for record in output:
            record["confidence_level"] = float(confidence_level)
            record["maxT_critical_value"] = critical
            if record["statistic"] is None:
                continue
            if record["simulation_std"] == 0:
                centre = record["simulation_mean"]
                record["simultaneous_lower"] = centre
                record["simultaneous_upper"] = centre
            else:
                centre = record["expected"]
                half_width = critical * record["simulation_std"]
                record["simultaneous_lower"] = centre - half_width
                record["simultaneous_upper"] = centre + half_width
        if max_statistics:
            for index, z_score, _standardized in valid:
                extreme = sum(value >= abs(z_score) for value in max_statistics)
                output[index]["p_value_maxT"] = (extreme + 1) / (permutations + 1)
        # One non-empty band is one test: max-T equals the unadjusted result,
        # including the zero-variance randomisation case.
        nonempty = [record for record in output if record["statistic"] is not None]
        if len(nonempty) == 1:
            nonempty[0]["p_value_maxT"] = nonempty[0]["p_value"]
    return output

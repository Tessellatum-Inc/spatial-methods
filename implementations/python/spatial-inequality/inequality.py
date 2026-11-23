"""Area-level inequality, entropy and two-group segregation summaries."""
from __future__ import annotations
from math import fsum, isfinite, log


def _nonnegative(values, name):
    try:
        result = [float(value) for value in values]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a numeric sequence") from exc
    if not result or any(not isfinite(v) or v < 0 for v in result):
        raise ValueError(f"{name} must be non-empty, finite and nonnegative")
    return result


def _weights(weights, n):
    if weights is None:
        return [1.0] * n
    result = _nonnegative(weights, "weights")
    if len(result) != n:
        raise ValueError("weights and values must have equal length")
    if fsum(result) <= 0:
        raise ValueError("weights must have a positive total")
    return result


def weighted_gini(values, weights=None):
    """Weighted Gini coefficient for nonnegative area-level values.

    This is an inequality summary across areas, not a distance-weighted
    spatial Gini or a measure of spatial autocorrelation.
    """
    x = _nonnegative(values, "values")
    w = _weights(weights, len(x))
    total_w = fsum(w)
    mean = fsum(a * b for a, b in zip(x, w)) / total_w
    if mean == 0.0:
        return 0.0
    # Sorting turns the pairwise absolute-difference sum into a cumulative
    # weighted sum, reducing the calculation from O(n^2) to O(n log n).
    cumulative_weight = 0.0
    cumulative_weighted_value = 0.0
    contributions = []
    for value, weight in sorted(zip(x, w), key=lambda pair: pair[0]):
        contributions.append(
            weight * (value * cumulative_weight - cumulative_weighted_value)
        )
        cumulative_weight += weight
        cumulative_weighted_value += weight * value
    return fsum(contributions) / (mean * total_w * total_w)


def theil_t(values, weights=None):
    """Population-weighted Theil T (Theil entropy) index."""
    x = _nonnegative(values, "values")
    w = _weights(weights, len(x))
    total_w = fsum(w)
    mean = fsum(a * b for a, b in zip(x, w)) / total_w
    if mean == 0.0:
        return 0.0
    return fsum(
        (weight / total_w) * (value / mean) * log(value / mean)
        for value, weight in zip(x, w) if weight > 0 and value > 0
    )


def theil_l(values, weights=None):
    """Population-weighted Theil L (mean log deviation) index.

    Positive-weight areas must have strictly positive values; a zero value
    makes the mathematical mean-log-deviation index infinite.
    """
    x = _nonnegative(values, "values")
    w = _weights(weights, len(x))
    total_w = fsum(w)
    if any(value == 0 and weight > 0 for value, weight in zip(x, w)):
        raise ValueError("Theil L requires positive values wherever weight is positive")
    mean = fsum(a * b for a, b in zip(x, w)) / total_w
    if mean <= 0:
        raise ValueError("Theil L requires a positive weighted mean")
    return fsum(
        (weight / total_w) * log(mean / value)
        for value, weight in zip(x, w) if weight > 0
    )


def spatial_entropy(populations, *, normalize=True):
    """Shannon entropy of the distribution of population across areal units.

    The normalized value divides by log(number of supplied areas), yielding
    a 0-1 evenness summary. It does not incorporate adjacency or distance.
    """
    values = _nonnegative(populations, "populations")
    total = fsum(values)
    if total <= 0:
        raise ValueError("populations must have a positive total")
    entropy = -fsum(
        (value / total) * log(value / total)
        for value in values if value > 0
    )
    normalized = entropy / log(len(values)) if len(values) > 1 else 0.0
    return {
        "entropy": entropy,
        "normalized_entropy": normalized if normalize else None,
        "n_areas": len(values),
    }


def dissimilarity_index(group_a, group_b):
    """Duncan-Duncan two-group dissimilarity index, bounded by 0 and 1."""
    a = _nonnegative(group_a, "group_a")
    b = _nonnegative(group_b, "group_b")
    if len(a) != len(b):
        raise ValueError("both groups must have the same number of areas")
    total_a, total_b = fsum(a), fsum(b)
    if total_a <= 0 or total_b <= 0:
        raise ValueError("each group must have a positive total")
    return 0.5 * fsum(abs(x / total_a - y / total_b) for x, y in zip(a, b))


def exposure_indices(group_a, group_b):
    """Return group-A isolation and interaction indices for two groups."""
    a = _nonnegative(group_a, "group_a")
    b = _nonnegative(group_b, "group_b")
    if len(a) != len(b):
        raise ValueError("both groups must have the same number of areas")
    total_a = fsum(a)
    if total_a <= 0:
        raise ValueError("group_a must have a positive total")
    isolation = fsum(
        (ai / total_a) * (ai / (ai + bi))
        for ai, bi in zip(a, b) if ai + bi > 0
    )
    interaction = fsum(
        (ai / total_a) * (bi / (ai + bi))
        for ai, bi in zip(a, b) if ai + bi > 0
    )
    return {"isolation": isolation, "interaction": interaction}

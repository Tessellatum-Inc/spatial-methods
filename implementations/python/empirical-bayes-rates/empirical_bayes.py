"""Global and local moment empirical-Bayes smoothing for Poisson rates."""
from __future__ import annotations
from math import fsum, isfinite
from numbers import Integral

def _validate_counts_exposure(counts, exposure):
    try:
        y = [float(value) for value in counts]
        e = [float(value) for value in exposure]
    except (TypeError, ValueError) as exc:
        raise ValueError("counts and exposure must be numeric sequences") from exc
    if not y or len(y) != len(e):
        raise ValueError("counts and exposure must be non-empty and have equal length")
    if any(not isfinite(v) or v < 0 or not v.is_integer() for v in y):
        raise ValueError("counts must be finite nonnegative integers")
    if any(not isfinite(v) or v <= 0 for v in e):
        raise ValueError("exposure values must be finite and strictly positive")
    return y, e

def _moment_parameters(counts, exposure):
    total_e, total_y = fsum(exposure), fsum(counts)
    mean = total_y / total_e
    mean_e = total_e / len(exposure)
    rates = [y / e for y, e in zip(counts, exposure)]
    weighted_var = fsum(e * (r - mean) ** 2 for e, r in zip(exposure, rates)) / total_e
    between = max(0.0, weighted_var - mean / mean_e)
    return mean, between, mean_e, weighted_var

def global_empirical_bayes(counts, exposure):
    """Marshall's global Poisson moment shrinkage estimator."""
    y, e = _validate_counts_exposure(counts, exposure)
    mean, between, mean_e, weighted_var = _moment_parameters(y, e)
    crude = [yi / ei for yi, ei in zip(y, e)]
    if between == 0.0:
        factors, estimates = [0.0] * len(y), [mean] * len(y)
    else:
        factors = [between / (between + mean / ei) for ei in e]
        estimates = [mean + c * (r - mean) for c, r in zip(factors, crude)]
    return {
        "crude_rates": crude, "estimates": estimates,
        "shrinkage_factors": factors, "overall_rate": mean,
        "between_area_variance": between, "mean_exposure": mean_e,
        "weighted_rate_variance": weighted_var,
    }

def local_empirical_bayes(counts, exposure, neighborhoods):
    """Marshall-style local moment shrinkage with caller-supplied neighborhoods."""
    y, e = _validate_counts_exposure(counts, exposure)
    try:
        groups = [list(group) for group in neighborhoods]
    except TypeError as exc:
        raise ValueError("neighborhoods must provide one index sequence per area") from exc
    if len(groups) != len(y):
        raise ValueError("one neighborhood is required for each area")
    estimates, details = [], []
    for i, group in enumerate(groups):
        if not group or i not in group:
            raise ValueError("each neighborhood must be non-empty and include its own area")
        if any(isinstance(k, bool) or not isinstance(k, Integral) or k < 0 or k >= len(y) for k in group):
            raise ValueError("neighborhood indices must be valid integer area indices")
        if len(set(group)) != len(group):
            raise ValueError("neighborhood indices must not contain duplicates")
        mean, between, mean_e, weighted_var = _moment_parameters(
            [y[k] for k in group], [e[k] for k in group]
        )
        crude = y[i] / e[i]
        factor = 0.0 if between == 0.0 else between / (between + mean / e[i])
        estimate = mean + factor * (crude - mean)
        estimates.append(estimate)
        details.append({
            "area_index": i, "neighborhood": tuple(group), "local_rate": mean,
            "between_area_variance": between, "mean_exposure": mean_e,
            "weighted_rate_variance": weighted_var,
            "shrinkage_factor": factor, "crude_rate": crude,
        })
    return {"estimates": estimates, "areas": details}

"""Mann-Kendall, seasonal Mann-Kendall and Sen trend estimators."""
import math
from statistics import median


def _values(values, label):
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)) or len(values) < 2:
        raise ValueError(f"{label} must contain at least two observations")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{label} must contain finite numeric values")
        result.append(float(value))
    return result


def _times(times, count):
    if times is None:
        return [float(i) for i in range(count)]
    result = _values(times, "times")
    if len(result) != count:
        raise ValueError("times and values must have equal length")
    if any(b <= a for a, b in zip(result, result[1:])):
        raise ValueError("times must be strictly increasing")
    return result


def _mk_components(series):
    n = len(series)
    score = sum((series[j] > series[i]) - (series[j] < series[i])
                for i in range(n - 1) for j in range(i + 1, n))
    counts = {}
    for value in series:
        counts[value] = counts.get(value, 0) + 1
    tie_term = sum(t * (t - 1) * (2 * t + 5) for t in counts.values() if t > 1)
    variance = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0
    pairs = n * (n - 1) / 2.0
    tied_pairs = sum(t * (t - 1) / 2.0 for t in counts.values())
    return score, variance, pairs, tied_pairs


def _normal_result(score, variance):
    if variance <= 0 or score == 0:
        return 0.0, 1.0
    z = (score - (1.0 if score > 0 else -1.0)) / math.sqrt(variance)
    return z, math.erfc(abs(z) / math.sqrt(2.0))


def mann_kendall(values):
    """Tie-corrected Mann-Kendall test with continuity-corrected normal p-value."""
    y = _values(values, "values")
    score, variance, pairs, tied_pairs = _mk_components(y)
    z, p_value = _normal_result(score, variance)
    denominator = math.sqrt(pairs * (pairs - tied_pairs))
    return {"s": score, "variance_s": variance, "z": z,
            "p_value_two_sided": p_value,
            "tau_b": score / denominator if denominator else 0.0}


def _season_groups(values, seasons):
    y = _values(values, "values")
    if isinstance(seasons, (str, bytes)) or not isinstance(seasons, (list, tuple)):
        raise ValueError("seasons must be a sequence aligned with values")
    if len(seasons) != len(y):
        raise ValueError("seasons and values must have equal length")
    groups = {}
    for index, (season, value) in enumerate(zip(seasons, y)):
        try:
            groups.setdefault(season, []).append((index, value))
        except TypeError as exc:
            raise ValueError("season labels must be hashable") from exc
    if len(groups) < 2:
        raise ValueError("seasonal analysis requires at least two distinct seasons")
    return y, groups


def seasonal_mann_kendall(values, seasons):
    """Sum within-season Mann-Kendall scores and tie-corrected variances.

    Comparisons are restricted to observations sharing a season label. The
    p-value is a continuity-corrected normal approximation. Dependence
    between seasons and serial correlation within seasons are not corrected.
    """
    _, groups = _season_groups(values, seasons)
    total_score = 0
    total_variance = total_pairs = total_tied_pairs = 0.0
    season_results = {}
    for season, indexed in groups.items():
        score, variance, pairs, tied_pairs = _mk_components([v for _, v in indexed])
        total_score += score
        total_variance += variance
        total_pairs += pairs
        total_tied_pairs += tied_pairs
        season_results[season] = {"n": len(indexed), "s": score, "variance_s": variance}
    z, p_value = _normal_result(total_score, total_variance)
    denominator = math.sqrt(total_pairs * (total_pairs - total_tied_pairs))
    return {"s": total_score, "variance_s": total_variance, "z": z,
            "p_value_two_sided": p_value,
            "seasonal_tau": total_score / denominator if denominator else 0.0,
            "season_count": len(groups), "seasons": season_results}


def sen_slope(values, times=None):
    """Return Sen's median pairwise slope and median intercept."""
    y = _values(values, "values")
    x = _times(times, len(y))
    slopes = [(y[j] - y[i]) / (x[j] - x[i])
              for i in range(len(y) - 1) for j in range(i + 1, len(y))]
    slope = median(slopes)
    return {"slope": slope,
            "intercept": median([v - slope * t for t, v in zip(x, y)]),
            "pair_count": len(slopes)}


def seasonal_sen_slope(values, seasons, times=None):
    """Median of pairwise slopes formed only by observations in the same season."""
    y, groups = _season_groups(values, seasons)
    x = _times(times, len(y))
    slopes = []
    for indexed in groups.values():
        for pos, (i, yi) in enumerate(indexed[:-1]):
            for j, yj in indexed[pos + 1:]:
                slopes.append((yj - yi) / (x[j] - x[i]))
    if not slopes:
        raise ValueError("at least one season must contain two observations")
    slope = median(slopes)
    return {"slope": slope,
            "intercept": median([v - slope * t for t, v in zip(x, y)]),
            "pair_count": len(slopes)}


def harmonic_regression(values, times=None, *, period, harmonics=1, include_trend=True):
    """Fit intercept + optional linear trend + Fourier sine/cosine terms.

    Uses least squares. Times must be strictly increasing; period uses the
    same units as times. The returned fit is descriptive and includes no
    inferential standard errors or autocorrelation correction.
    """
    import numpy as np

    y = np.asarray(_values(values, "values"), dtype=float)
    x = np.asarray(_times(times, len(y)), dtype=float)
    if isinstance(period, bool) or not isinstance(period, (int, float)) or not math.isfinite(period) or period <= 0:
        raise ValueError("period must be a finite positive number")
    if isinstance(harmonics, bool) or not isinstance(harmonics, int) or harmonics < 1:
        raise ValueError("harmonics must be a positive integer")
    if not isinstance(include_trend, bool):
        raise ValueError("include_trend must be boolean")
    origin = float(x[0])
    columns = [np.ones(len(x))]
    if include_trend:
        columns.append(x - origin)
    for k in range(1, harmonics + 1):
        angle = 2.0 * math.pi * k * (x - origin) / float(period)
        columns.extend((np.sin(angle), np.cos(angle)))
    design = np.column_stack(columns)
    if len(y) < design.shape[1]:
        raise ValueError("not enough observations for the requested harmonic model")
    coefficients, _, rank, _ = np.linalg.lstsq(design, y, rcond=None)
    if rank != design.shape[1]:
        raise ValueError("harmonic design matrix is rank deficient")
    fitted = design @ coefficients
    residuals = y - fitted
    sse = float(residuals @ residuals)
    centered = y - float(np.mean(y))
    total = float(centered @ centered)
    r_squared = 1.0 - sse / total if total > 0 else (1.0 if sse <= 1e-24 else 0.0)
    return {
        "coefficients": coefficients.tolist(),
        "fitted": fitted.tolist(),
        "residuals": residuals.tolist(),
        "rmse": math.sqrt(sse / len(y)),
        "r_squared": r_squared,
        "rank": int(rank),
        "parameter_count": int(design.shape[1]),
        "time_origin": origin,
        "period": float(period),
        "harmonics": harmonics,
        "include_trend": include_trend,
    }

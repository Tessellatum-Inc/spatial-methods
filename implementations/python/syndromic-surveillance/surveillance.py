"""Reference CUSUM and EARS-style aberration detectors for count series."""
from __future__ import annotations

import math
from statistics import NormalDist
from collections.abc import Sequence


def _finite_number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def cusum(
    observations: Sequence[float],
    target: float,
    *,
    allowance: float = 0.5,
    threshold: float = 5.0,
) -> dict[str, list]:
    """Return two-sided tabular CUSUM statistics and threshold alarms.

    The reference value is target and the allowance is expressed in the same
    units as observations. Each side accumulates deviations beyond allowance.
    This is a deterministic monitoring primitive, not an automatically
    calibrated outbreak detector: target, allowance and threshold must be
    selected for the surveillance process and its false-alarm tolerance.
    """
    if isinstance(observations, (str, bytes)) or not observations:
        raise ValueError("observations must be a non-empty numeric sequence")
    values = [_finite_number(x, "observations") for x in observations]
    target = _finite_number(target, "target")
    allowance = _finite_number(allowance, "allowance")
    threshold = _finite_number(threshold, "threshold")
    if allowance < 0 or threshold <= 0:
        raise ValueError("allowance must be non-negative and threshold positive")
    upper, lower, alarms = [], [], []
    s_high = s_low = 0.0
    for value in values:
        s_high = max(0.0, s_high + value - target - allowance)
        s_low = max(0.0, s_low + target - value - allowance)
        upper.append(s_high)
        lower.append(s_low)
        alarms.append(s_high >= threshold or s_low >= threshold)
    return {"upper": upper, "lower": lower, "alarm": alarms}


def _count_series(counts: Sequence[int]) -> list[int]:
    if isinstance(counts, (str, bytes)) or not counts:
        raise ValueError("counts must be a non-empty sequence")
    values = []
    for value in counts:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("counts must be non-negative integers")
        values.append(value)
    return values


def ears(
    counts: Sequence[int],
    *,
    baseline_window: int = 7,
    c2_exclusion: int = 2,
    threshold: float = 3.0,
) -> dict[str, list]:
    """Compute transparent EARS-style C1, C2 and C3 daily scores.

    C1 compares day t with the immediately preceding baseline_window days.
    C2 compares day t with a window ending c2_exclusion days before t. Each
    score is (observed - baseline mean) / max(sample SD, sqrt(mean), 1).
    C3 is the rolling sum of the positive C2 scores over the current and two
    preceding days. A score is None until its baseline is available.

    This is a deliberately explicit EARS-style implementation, not a claim
    to reproduce every operational CDC/EARS variant or Farrington's model.
    It does not model weekday seasonality, overdispersion beyond the
    conservative variance floor, holidays, covariates or population offsets.
    """
    values = _count_series(counts)
    if isinstance(baseline_window, bool) or not isinstance(baseline_window, int) or baseline_window < 2:
        raise ValueError("baseline_window must be an integer of at least two")
    if isinstance(c2_exclusion, bool) or not isinstance(c2_exclusion, int) or c2_exclusion < 0:
        raise ValueError("c2_exclusion must be a non-negative integer")
    threshold = _finite_number(threshold, "threshold")
    if threshold <= 0:
        raise ValueError("threshold must be positive")

    def z_score(observed, baseline):
        mean = math.fsum(baseline) / len(baseline)
        variance = math.fsum((x - mean) ** 2 for x in baseline) / (len(baseline) - 1)
        scale = max(math.sqrt(variance), math.sqrt(mean), 1.0)
        return (observed - mean) / scale

    c1: list[float | None] = []
    c2: list[float | None] = []
    c3: list[float | None] = []
    for i, observed in enumerate(values):
        c1.append(z_score(observed, values[i-baseline_window:i])
                  if i >= baseline_window else None)
        end = i - c2_exclusion
        start = end - baseline_window
        c2.append(z_score(observed, values[start:end])
                  if start >= 0 else None)
        if i >= 2 and c2[i] is not None and c2[i-1] is not None and c2[i-2] is not None:
            c3.append(math.fsum(max(0.0, c2[j]) for j in (i-2, i-1, i)))
        else:
            c3.append(None)
    return {
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c1_alarm": [score is not None and score >= threshold for score in c1],
        "c2_alarm": [score is not None and score >= threshold for score in c2],
        "c3_alarm": [score is not None and score >= threshold for score in c3],
    }


def _solve_two_parameter_wls(x, y, weights):
    """Solve weighted least squares for columns [1, x] without dependencies."""
    s0 = math.fsum(weights)
    s1 = math.fsum(w * value for w, value in zip(weights, x))
    s2 = math.fsum(w * value * value for w, value in zip(weights, x))
    t0 = math.fsum(w * value for w, value in zip(weights, y))
    t1 = math.fsum(w * xv * value for w, xv, value in zip(weights, x, y))
    determinant = s0 * s2 - s1 * s1
    if not math.isfinite(determinant) or determinant <= 1e-12 * max(1.0, s0 * s2):
        raise ValueError("baseline design is singular")
    return ((t0 * s2 - t1 * s1) / determinant,
            (s0 * t1 - s1 * t0) / determinant,
            (s2 / determinant, -s1 / determinant, s0 / determinant))


def farrington_exceedance(
    counts: Sequence[int],
    *,
    period: int = 52,
    window: int = 3,
    years_back: int = 5,
    alpha: float = 0.01,
    reweight: bool = True,
    reweight_threshold: float = 2.58,
) -> dict:
    """Compute a bounded Farrington-style quasi-Poisson exceedance for the last week.

    Reference observations come from the same seasonal period (plus/minus
    window) in each preceding cycle. A log-linear trend is fitted by Poisson
    IRLS; optional residual reweighting limits historical aberrations. A
    Pearson dispersion estimate and cube-root normal prediction approximation
    produce the upper bound. This is not a bit-for-bit Farrington or Noufaily
    implementation.
    """
    values = _count_series(counts)
    for name, value, minimum in (("period", period, 2), ("window", window, 0),
                                 ("years_back", years_back, 2)):
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    if window * 2 + 1 > period:
        raise ValueError("window must not span more than one seasonal period")
    alpha = _finite_number(alpha, "alpha")
    cutoff = _finite_number(reweight_threshold, "reweight_threshold")
    if not 0 < alpha < 0.5 or cutoff <= 0:
        raise ValueError("alpha must be in (0, 0.5) and reweight_threshold positive")
    if not isinstance(reweight, bool):
        raise ValueError("reweight must be boolean")
    current = len(values) - 1
    reference_indices = []
    for year in range(1, years_back + 1):
        anchor = current - year * period
        for offset in range(-window, window + 1):
            index = anchor + offset
            if 0 <= index < current:
                reference_indices.append(index)
    reference_indices = sorted(set(reference_indices))
    if len(reference_indices) < 6:
        raise ValueError("insufficient seasonal history; at least six reference observations are required")
    x = [(index - current) / period for index in reference_indices]
    y = [float(values[index]) for index in reference_indices]
    robust = [1.0] * len(y)
    beta0, beta1 = math.log(max(math.fsum(y) / len(y), 0.1)), 0.0
    inverse = (0.0, 0.0, 0.0)
    for _ in range(60):
        mu = [math.exp(max(-30.0, min(30.0, beta0 + beta1 * xv))) for xv in x]
        working = [math.log(max(m, 1e-12)) + (obs - m) / max(m, 1e-12)
                   for obs, m in zip(y, mu)]
        weights = [r * m for r, m in zip(robust, mu)]
        next0, next1, inverse = _solve_two_parameter_wls(x, working, weights)
        change = max(abs(next0 - beta0), abs(next1 - beta1))
        beta0, beta1 = next0, next1
        mu = [math.exp(max(-30.0, min(30.0, beta0 + beta1 * xv))) for xv in x]
        if reweight:
            residuals = [(obs - m) / math.sqrt(max(m, 1e-12))
                         for obs, m in zip(y, mu)]
            robust = [min(1.0, cutoff / abs(residual)) if residual else 1.0
                      for residual in residuals]
        if change < 1e-8:
            break
    fitted = [math.exp(max(-30.0, min(30.0, beta0 + beta1 * xv))) for xv in x]
    df = max(1, len(y) - 2)
    dispersion = max(1.0, math.fsum(
        weight * (obs - mean) ** 2 / max(mean, 1e-12)
        for weight, obs, mean in zip(robust, y, fitted)
    ) / df)
    expected = math.exp(max(-30.0, min(30.0, beta0)))
    leverage = max(0.0, inverse[0])
    z_value = NormalDist().inv_cdf(1.0 - alpha)
    transformed_sd = math.sqrt(dispersion * (1.0 + leverage) / 9.0)
    upper = max(0.0, (expected ** (1.0 / 3.0) + z_value * transformed_sd) ** 3)
    observed = values[-1]
    return {
        "observed": observed, "expected": expected, "upper_bound": upper,
        "exceedance": max(0.0, observed - expected),
        "exceedance_score": ((observed - expected) / (upper - expected)
                             if upper > expected else float("inf") if observed > expected else 0.0),
        "alarm": observed > upper, "dispersion": dispersion,
        "trend_per_year": beta1, "reference_indices": tuple(reference_indices),
        "n_reference": len(reference_indices), "alpha": alpha,
        "reweighted": reweight,
    }

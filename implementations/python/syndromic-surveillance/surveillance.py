"""Reference CUSUM and EARS-style aberration detectors for count series."""
from __future__ import annotations

import math
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

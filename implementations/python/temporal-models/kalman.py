"""Scalar local-level Kalman filtering and Rauch-Tung-Striebel smoothing."""
from __future__ import annotations
from math import isfinite
from typing import Iterable


def kalman_local_level(observations: Iterable[float | None], *,
                       process_variance: float, observation_variance: float,
                       initial_mean: float = 0.0, initial_variance: float = 1.0
                       ) -> tuple[list[float], list[float]]:
    """Filter a scalar random-walk state with optional missing observations."""
    y = list(observations)
    if not y:
        raise ValueError("observations must be non-empty")
    if any(v is not None and not isfinite(float(v)) for v in y):
        raise ValueError("observations must be finite or None")
    if not isfinite(process_variance) or process_variance < 0:
        raise ValueError("process_variance must be finite and non-negative")
    if not isfinite(observation_variance) or observation_variance <= 0:
        raise ValueError("observation_variance must be positive and finite")
    if not isfinite(initial_mean) or not isfinite(initial_variance) or initial_variance < 0:
        raise ValueError("initial state parameters must be finite and variance non-negative")
    mean, variance = float(initial_mean), float(initial_variance)
    means, variances = [], []
    for value in y:
        predicted_mean = mean
        predicted_variance = variance + process_variance
        if value is None:
            mean, variance = predicted_mean, predicted_variance
        else:
            innovation_variance = predicted_variance + observation_variance
            gain = predicted_variance / innovation_variance
            mean = predicted_mean + gain * (float(value) - predicted_mean)
            variance = max(0.0, (1.0 - gain) * predicted_variance)
        means.append(mean)
        variances.append(variance)
    return means, variances


def rts_local_level(observations: Iterable[float | None], *,
                    process_variance: float, observation_variance: float,
                    initial_mean: float = 0.0, initial_variance: float = 1.0
                    ) -> tuple[list[float], list[float]]:
    """Return smoothed state means/variances using the scalar RTS backward pass."""
    y = list(observations)
    filtered_mean, filtered_var = kalman_local_level(
        y, process_variance=process_variance,
        observation_variance=observation_variance,
        initial_mean=initial_mean, initial_variance=initial_variance,
    )
    smooth_mean = filtered_mean.copy()
    smooth_var = filtered_var.copy()
    for t in range(len(y) - 2, -1, -1):
        predicted_var_next = filtered_var[t] + process_variance
        gain = filtered_var[t] / predicted_var_next if predicted_var_next > 0 else 0.0
        smooth_mean[t] = filtered_mean[t] + gain * (smooth_mean[t + 1] - filtered_mean[t])
        smooth_var[t] = max(0.0, filtered_var[t] + gain * gain *
                            (smooth_var[t + 1] - predicted_var_next))
    return smooth_mean, smooth_var

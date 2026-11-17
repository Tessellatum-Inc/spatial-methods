"""Greedy Gaussian-process mutual-information sensor selection."""
from __future__ import annotations

import math
import numpy as np


def _points(values, name):
    try:
        result = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be finite numeric coordinates") from exc
    if result.ndim != 2 or result.shape[1] != 2 or len(result) == 0 or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a non-empty finite (n, 2) array")
    return result


def _positive_scalar(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ValueError(f"{name} must be a finite positive number")
    try:
        result = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite positive number") from exc
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    return result


def _kernel(left, right, kind, length_scale):
    delta = left[:, None, :] - right[None, :, :]
    distance = np.sqrt(np.sum(delta * delta, axis=2))
    if kind == "exponential":
        return np.exp(-distance / length_scale)
    return np.exp(-0.5 * (distance / length_scale) ** 2)


def _logdet_spd(matrix, name):
    symmetric = (matrix + matrix.T) * 0.5
    try:
        factor = np.linalg.cholesky(symmetric)
    except np.linalg.LinAlgError as exc:
        raise ValueError(f"{name} must be positive definite") from exc
    diagonal = np.diag(factor)
    return float(2.0 * np.log(diagonal).sum())


def _conditional_covariance(target_covariance, cross_covariance,
                            candidate_covariance, noise, selected):
    if not selected:
        return target_covariance.copy()
    indices = np.asarray(selected, dtype=int)
    observed_covariance = candidate_covariance[np.ix_(indices, indices)]
    observed_covariance = observed_covariance + np.diag(noise[indices])
    cross = cross_covariance[:, indices]
    try:
        solved = np.linalg.solve(observed_covariance, cross.T)
    except np.linalg.LinAlgError as exc:
        raise ValueError("noisy candidate covariance system is singular") from exc
    conditional = target_covariance - cross @ solved
    return (conditional + conditional.T) * 0.5


def gaussian_sensor_mutual_information(
    target_points,
    candidate_points,
    *,
    max_sensors,
    length_scale=1.0,
    noise_variance=0.1,
    kernel="gaussian",
):
    """Greedily select sensors by conditional mutual information in nats.

    The latent field is a zero-mean Gaussian process with unit marginal
    variance and either Gaussian or exponential covariance. Observations
    have independent, candidate-specific noise variances. The objective is
    I(f_target; y_selected), computed from the Gaussian conditional covariance.
    Ties are broken by the lowest original candidate index.
    """
    targets = _points(target_points, "target_points")
    candidates = _points(candidate_points, "candidate_points")
    scale = _positive_scalar(length_scale, "length_scale")
    if not isinstance(kernel, str) or kernel not in {"gaussian", "exponential"}:
        raise ValueError("kernel must be 'gaussian' or 'exponential'")
    if isinstance(max_sensors, (bool, np.bool_)) or not isinstance(max_sensors, (int, np.integer)):
        raise ValueError("max_sensors must be an integer")
    if not 0 <= max_sensors <= len(candidates):
        raise ValueError("max_sensors must be between zero and candidate count")

    if np.isscalar(noise_variance):
        noise_value = _positive_scalar(noise_variance, "noise_variance")
        noise = np.full(len(candidates), noise_value, dtype=float)
    else:
        try:
            noise = np.asarray(noise_variance, dtype=float)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("noise_variance must be positive finite scalar or vector") from exc
        if noise.shape != (len(candidates),) or not np.all(np.isfinite(noise)) or np.any(noise <= 0):
            raise ValueError("noise_variance vector must be positive, finite and match candidates")

    target_cov = _kernel(targets, targets, kernel, scale)
    # A singular target covariance has no finite Gaussian differential entropy.
    _logdet_spd(target_cov, "target covariance")
    cross_cov = _kernel(targets, candidates, kernel, scale)
    candidate_cov = _kernel(candidates, candidates, kernel, scale)
    target_logdet = _logdet_spd(target_cov, "target covariance")

    selected = []
    gains = []
    current_mi = 0.0
    conditional = target_cov.copy()
    for _ in range(int(max_sensors)):
        best_index = None
        best_gain = -float("inf")
        best_conditional = None
        for candidate_index in range(len(candidates)):
            if candidate_index in selected:
                continue
            trial = selected + [candidate_index]
            trial_conditional = _conditional_covariance(
                target_cov, cross_cov, candidate_cov, noise, trial
            )
            trial_logdet = _logdet_spd(trial_conditional, "conditional target covariance")
            trial_mi = max(0.0, 0.5 * (target_logdet - trial_logdet))
            gain = trial_mi - current_mi
            if gain > best_gain + 1e-14:
                best_gain = gain
                best_index = candidate_index
                best_conditional = trial_conditional
        selected.append(best_index)
        gains.append(max(0.0, float(best_gain)))
        current_mi += gains[-1]
        conditional = best_conditional

    return {
        "selected_indices": tuple(selected),
        "mutual_information": float(current_mi),
        "marginal_gains": tuple(gains),
        "conditional_covariance": conditional,
        "kernel": kernel,
        "length_scale": scale,
    }

"""Exact dense Gaussian-process regression with a separable space-time kernel."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class SpaceTimePrediction:
    mean: np.ndarray
    covariance: np.ndarray
    variance: np.ndarray

def _observations(coordinates, times, name):
    xy = np.asarray(coordinates, dtype=float)
    t = np.asarray(times, dtype=float)
    if xy.ndim != 2 or xy.shape[0] == 0 or xy.shape[1] == 0:
        raise ValueError(f"{name} coordinates must be a non-empty (n, d) array")
    if t.ndim != 1 or t.size != xy.shape[0]:
        raise ValueError(f"{name} times must have one value per coordinate")
    if not np.all(np.isfinite(xy)) or not np.all(np.isfinite(t)):
        raise ValueError(f"{name} coordinates and times must be finite")
    return xy, t

def separable_exponential_covariance(coordinates_a, times_a, coordinates_b=None,
                                     times_b=None, *, variance=1.0,
                                     spatial_scale=1.0, temporal_scale=1.0):
    """Product exponential covariance on Euclidean space crossed with linear time."""
    xa, ta = _observations(coordinates_a, times_a, "first")
    if coordinates_b is None:
        xb, tb = xa, ta
    else:
        if times_b is None:
            raise ValueError("times_b is required when coordinates_b is supplied")
        xb, tb = _observations(coordinates_b, times_b, "second")
    if xa.shape[1] != xb.shape[1]:
        raise ValueError("coordinate dimensions must match")
    if not np.isfinite(variance) or variance < 0:
        raise ValueError("variance must be finite and non-negative")
    if not np.isfinite(spatial_scale) or spatial_scale <= 0:
        raise ValueError("spatial_scale must be finite and positive")
    if not np.isfinite(temporal_scale) or temporal_scale <= 0:
        raise ValueError("temporal_scale must be finite and positive")
    distance = np.linalg.norm(xa[:, None, :] - xb[None, :, :], axis=2)
    lag = np.abs(ta[:, None] - tb[None, :])
    return variance * np.exp(-distance / spatial_scale) * np.exp(-lag / temporal_scale)

def predict_spatiotemporal_gp(train_coordinates, train_times, train_values,
                              prediction_coordinates, prediction_times, *,
                              variance=1.0, spatial_scale=1.0,
                              temporal_scale=1.0, noise_variance=0.0,
                              jitter=1e-10, include_observation_noise=False):
    """Condition a zero-mean GP; return posterior mean and covariance."""
    x, t = _observations(train_coordinates, train_times, "training")
    xp, tp = _observations(prediction_coordinates, prediction_times, "prediction")
    y = np.asarray(train_values, dtype=float)
    if y.ndim != 1 or y.size != x.shape[0]:
        raise ValueError("train_values must have one value per training observation")
    if not np.all(np.isfinite(y)):
        raise ValueError("train_values must be finite")
    if x.shape[1] != xp.shape[1]:
        raise ValueError("training and prediction coordinate dimensions must match")
    if not np.isfinite(noise_variance) or noise_variance < 0:
        raise ValueError("noise_variance must be finite and non-negative")
    if not np.isfinite(jitter) or jitter < 0:
        raise ValueError("jitter must be finite and non-negative")
    params = dict(variance=variance, spatial_scale=spatial_scale,
                  temporal_scale=temporal_scale)
    k_train = separable_exponential_covariance(x, t, **params)
    k_cross = separable_exponential_covariance(x, t, xp, tp, **params)
    k_pred = separable_exponential_covariance(xp, tp, **params)
    system = k_train.copy()
    system.flat[::system.shape[0] + 1] += noise_variance + jitter
    try:
        factor = np.linalg.cholesky(system)
    except np.linalg.LinAlgError as exc:
        raise np.linalg.LinAlgError(
            "training covariance is not positive definite; increase jitter or noise_variance"
        ) from exc
    intermediate = np.linalg.solve(factor, k_cross)
    alpha = np.linalg.solve(factor.T, np.linalg.solve(factor, y))
    mean = k_cross.T @ alpha
    covariance = k_pred - intermediate.T @ intermediate
    covariance = (covariance + covariance.T) / 2.0
    if include_observation_noise:
        covariance.flat[::covariance.shape[0] + 1] += noise_variance
    diagonal = np.diag(covariance).copy()
    tolerance = 1e-9 * max(1.0, float(variance))
    if np.any(diagonal < -tolerance):
        raise np.linalg.LinAlgError("predictive covariance has materially negative variance")
    diagonal = np.maximum(diagonal, 0.0)
    return SpaceTimePrediction(mean, covariance, diagonal)

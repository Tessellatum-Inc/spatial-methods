"""Mahalanobis climate analog ranking and climate-velocity vectors."""
from __future__ import annotations
import numpy as np


def _matrix(values, name):
    array = np.asarray(values, dtype=float)
    if array.ndim != 2 or array.shape[0] < 2 or array.shape[1] < 1:
        raise ValueError(f"{name} must have shape (samples >= 2, variables >= 1)")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def mahalanobis_climate_analogs(historical, future, *, n_analogs=1,
                                covariance=None, regularization=1e-8):
    """Rank historical climate samples by Mahalanobis distance to future samples.

    The default covariance is estimated from the historical reference matrix
    using sample covariance. A scale-relative diagonal ridge stabilizes
    singular or collinear climate variables. Returns (indices, distances),
    both shaped (n_future, n_analogs), ordered from nearest to farthest.
    """
    reference = _matrix(historical, "historical")
    targets = np.asarray(future, dtype=float)
    if targets.ndim == 1:
        targets = targets[None, :]
    if targets.ndim != 2 or targets.shape[1] != reference.shape[1] or not np.all(np.isfinite(targets)):
        raise ValueError("future must be a finite vector or matrix matching climate variables")
    if isinstance(n_analogs, (bool, np.bool_)) or not isinstance(n_analogs, (int, np.integer)) or not 1 <= n_analogs <= len(reference):
        raise ValueError("n_analogs must be an integer between 1 and historical sample count")
    try:
        ridge = float(regularization)
    except (TypeError, ValueError):
        raise ValueError("regularization must be finite and non-negative") from None
    if not np.isfinite(ridge) or ridge < 0:
        raise ValueError("regularization must be finite and non-negative")
    if covariance is None:
        cov = np.cov(reference, rowvar=False, ddof=1)
        cov = np.atleast_2d(cov)
    else:
        cov = np.asarray(covariance, dtype=float)
        if cov.shape != (reference.shape[1], reference.shape[1]) or not np.all(np.isfinite(cov)):
            raise ValueError("covariance must be a finite square matrix matching variable count")
        if not np.allclose(cov, cov.T, atol=1e-10, rtol=1e-10):
            raise ValueError("covariance must be symmetric")
    scale = max(float(np.trace(cov) / cov.shape[0]), np.finfo(float).eps)
    regularized = cov + np.eye(cov.shape[0]) * ridge * scale
    try:
        factor = np.linalg.cholesky(regularized)
    except np.linalg.LinAlgError:
        raise ValueError("regularized covariance must be positive definite") from None
    differences = targets[:, None, :] - reference[None, :, :]
    whitened = np.linalg.solve(factor, differences.reshape(-1, reference.shape[1]).T)
    distances = np.sqrt(np.sum(whitened ** 2, axis=0)).reshape(len(targets), len(reference))
    order = np.argsort(distances, axis=1, kind="stable")[:, :int(n_analogs)]
    nearest = np.take_along_axis(distances, order, axis=1)
    return order, nearest


def climate_velocity(temporal_change, gradient_x, gradient_y, *,
                     minimum_gradient=1e-12):
    """Estimate isocline displacement from climate trend and spatial gradient.

    temporal_change is climate units per time; gradients are climate units
    per distance. The vector solves grad(T) dot velocity + dT/dt = 0:
    v = -(dT/dt) grad(T) / ||grad(T)||^2. Magnitude is distance per time.
    Near-zero gradients have infinite speed and undefined direction, returned
    as +inf magnitude and NaN vector components.
    """
    change, gx, gy = np.broadcast_arrays(
        np.asarray(temporal_change, dtype=float),
        np.asarray(gradient_x, dtype=float),
        np.asarray(gradient_y, dtype=float))
    if not (np.all(np.isfinite(change)) and np.all(np.isfinite(gx)) and np.all(np.isfinite(gy))):
        raise ValueError("climate change and gradients must be finite")
    try:
        floor = float(minimum_gradient)
    except (TypeError, ValueError):
        raise ValueError("minimum_gradient must be finite and positive") from None
    if not np.isfinite(floor) or floor <= 0:
        raise ValueError("minimum_gradient must be finite and positive")
    norm2 = gx * gx + gy * gy
    valid = norm2 > floor * floor
    vx = np.full(change.shape, np.nan, dtype=float)
    vy = np.full(change.shape, np.nan, dtype=float)
    speed = np.full(change.shape, np.inf, dtype=float)
    vx[valid] = -change[valid] * gx[valid] / norm2[valid]
    vy[valid] = -change[valid] * gy[valid] / norm2[valid]
    speed[valid] = np.abs(change[valid]) / np.sqrt(norm2[valid])
    if speed.ndim == 0:
        return {"velocity_x": float(vx), "velocity_y": float(vy), "speed": float(speed)}
    return {"velocity_x": vx, "velocity_y": vy, "speed": speed}

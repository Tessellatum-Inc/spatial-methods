"""Constant-velocity moving-object prediction and dead-reckoning update policy."""
from __future__ import annotations
import numpy as np


def predict_constant_velocity(state, covariance, *, time_step,
                              acceleration_noise_std=0.0):
    """Propagate [x, y, vx, vy] and covariance under white acceleration noise."""
    x = np.asarray(state, dtype=float)
    p = np.asarray(covariance, dtype=float)
    if x.shape != (4,) or not np.all(np.isfinite(x)):
        raise ValueError("state must be a finite [x, y, vx, vy] vector")
    if p.shape != (4, 4) or not np.all(np.isfinite(p)):
        raise ValueError("covariance must be a finite 4x4 matrix")
    if not np.allclose(p, p.T, atol=1e-10, rtol=1e-10):
        raise ValueError("covariance must be symmetric")
    if np.min(np.linalg.eigvalsh(p)) < -1e-10:
        raise ValueError("covariance must be positive semidefinite")
    try:
        dt, sigma = float(time_step), float(acceleration_noise_std)
    except (TypeError, ValueError):
        raise ValueError("time_step and acceleration_noise_std must be numeric") from None
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be finite and positive")
    if not np.isfinite(sigma) or sigma < 0:
        raise ValueError("acceleration_noise_std must be finite and non-negative")
    transition = np.array([
        [1., 0., dt, 0.],
        [0., 1., 0., dt],
        [0., 0., 1., 0.],
        [0., 0., 0., 1.]
    ])
    dt2, dt3, dt4 = dt**2, dt**3, dt**4
    process = sigma**2 * np.array([
        [dt4/4, 0., dt3/2, 0.],
        [0., dt4/4, 0., dt3/2],
        [dt3/2, 0., dt2, 0.],
        [0., dt3/2, 0., dt2]
    ])
    predicted_state = transition @ x
    predicted_covariance = transition @ p @ transition.T + process
    return {"state": predicted_state, "covariance": predicted_covariance,
            "transition": transition, "process_noise": process}


def position_confidence_ellipse(state, covariance, *, confidence_level=0.95):
    """Return a 2D Gaussian position confidence ellipse."""
    x = np.asarray(state, dtype=float)
    p = np.asarray(covariance, dtype=float)
    if x.shape != (4,) or not np.all(np.isfinite(x)):
        raise ValueError("state must be a finite [x, y, vx, vy] vector")
    if p.shape != (4, 4) or not np.all(np.isfinite(p)):
        raise ValueError("covariance must be a finite 4x4 matrix")
    position_covariance = p[:2, :2]
    if not np.allclose(position_covariance, position_covariance.T, atol=1e-10):
        raise ValueError("position covariance must be symmetric")
    values, vectors = np.linalg.eigh(position_covariance)
    if values[0] < -1e-10:
        raise ValueError("position covariance must be positive semidefinite")
    try:
        confidence = float(confidence_level)
    except (TypeError, ValueError):
        raise ValueError("confidence_level must be in (0, 1)") from None
    if not np.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence_level must be in (0, 1)")
    # For two degrees of freedom, chi-square quantile is -2 log(1-p).
    quantile = -2.0 * np.log1p(-confidence)
    order = np.argsort(values)[::-1]
    ordered_values = np.maximum(values[order], 0.0)
    major_vector = vectors[:, order[0]]
    return {"center": x[:2].copy(),
            "major_radius": float(np.sqrt(quantile * ordered_values[0])),
            "minor_radius": float(np.sqrt(quantile * ordered_values[1])),
            "orientation_rad": float(np.arctan2(major_vector[1], major_vector[0])),
            "eigenvalues": ordered_values,
            "confidence_level": confidence}


def dead_reckoning_update_decision(predicted_state, predicted_covariance,
                                   reported_position, *, elapsed_since_update,
                                   distance_threshold, uncertainty_threshold,
                                   max_interval, confidence_level=0.95):
    """Decide whether a moving object should transmit a new position report.

    An update is requested when predicted displacement, major confidence
    ellipse radius, or elapsed time reaches its corresponding threshold.
    """
    state = np.asarray(predicted_state, dtype=float)
    reported = np.asarray(reported_position, dtype=float)
    if state.shape != (4,) or not np.all(np.isfinite(state)):
        raise ValueError("predicted_state must be a finite [x, y, vx, vy] vector")
    if reported.shape != (2,) or not np.all(np.isfinite(reported)):
        raise ValueError("reported_position must be a finite 2D vector")
    try:
        elapsed, distance_limit, uncertainty_limit, time_limit = map(
            float, (elapsed_since_update, distance_threshold,
                    uncertainty_threshold, max_interval))
    except (TypeError, ValueError):
        raise ValueError("update thresholds and elapsed time must be numeric") from None
    if not np.isfinite(elapsed) or elapsed < 0:
        raise ValueError("elapsed_since_update must be finite and non-negative")
    if any(not np.isfinite(value) or value <= 0
           for value in (distance_limit, uncertainty_limit, time_limit)):
        raise ValueError("distance, uncertainty and time thresholds must be finite and positive")
    ellipse = position_confidence_ellipse(
        state, predicted_covariance, confidence_level=confidence_level)
    displacement = float(np.linalg.norm(state[:2] - reported))
    triggers = {
        "distance": displacement >= distance_limit,
        "uncertainty": ellipse["major_radius"] >= uncertainty_limit,
        "time": elapsed >= time_limit
    }
    return {"request_update": bool(any(triggers.values())),
            "triggers": triggers,
            "predicted_displacement": displacement,
            "uncertainty_radius": ellipse["major_radius"],
            "ellipse": ellipse}

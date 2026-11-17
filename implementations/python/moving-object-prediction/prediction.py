"""Constant-velocity moving-object prediction and predictive range queries."""
from __future__ import annotations
import math
from collections.abc import Mapping, Sequence


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be representable as a finite float")
    return result


def _point(value, name):
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 2:
        raise ValueError(f"{name} must be a pair of coordinates")
    return (_number(value[0], name), _number(value[1], name))


def _advance(x, y, vx, vy, dt):
    predicted = (x + vx * dt, y + vy * dt)
    if not all(math.isfinite(v) for v in predicted):
        raise ValueError("predicted coordinates overflowed finite numeric range")
    return predicted


def predict_position(position, velocity, horizon):
    """Extrapolate a 2D point using constant Cartesian velocity."""
    x, y = _point(position, "position")
    vx, vy = _point(velocity, "velocity")
    dt = _number(horizon, "horizon")
    if dt < 0:
        raise ValueError("horizon must be non-negative")
    return _advance(x, y, vx, vy, dt)


def predictive_range_query(objects: Mapping, bounds: Sequence[float], horizon: float,
                           *, uncertainty_radius: float = 0.0):
    """Return (id, predicted point, distance) for uncertainty disks intersecting a rectangle.

    Each state is (x, y, vx, vy). Results preserve mapping iteration order.
    """
    if not isinstance(objects, Mapping):
        raise ValueError("objects must be a mapping")
    if isinstance(bounds, (str, bytes)) or not isinstance(bounds, Sequence) or len(bounds) != 4:
        raise ValueError("bounds must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = (_number(v, "bounds") for v in bounds)
    if xmin > xmax or ymin > ymax:
        raise ValueError("rectangle bounds must be ordered")
    dt = _number(horizon, "horizon")
    radius = _number(uncertainty_radius, "uncertainty_radius")
    if dt < 0 or radius < 0:
        raise ValueError("horizon and uncertainty_radius must be non-negative")
    results = []
    for object_id, state in objects.items():
        if isinstance(state, (str, bytes)) or not isinstance(state, Sequence) or len(state) != 4:
            raise ValueError(f"state for {object_id!r} must be (x, y, vx, vy)")
        x, y, vx, vy = (_number(v, f"state for {object_id!r}") for v in state)
        px, py = _advance(x, y, vx, vy, dt)
        nearest_x = min(max(px, xmin), xmax)
        nearest_y = min(max(py, ymin), ymax)
        distance = math.hypot(px - nearest_x, py - nearest_y)
        if distance <= radius:
            results.append((object_id, (px, py), distance))
    return results


def dead_reckoning_update_required(reported_position, reported_velocity,
                                   elapsed_time, observed_position, *, tolerance):
    """Request a report when observed error exceeds the prediction tolerance."""
    predicted = predict_position(reported_position, reported_velocity, elapsed_time)
    observed = _point(observed_position, "observed_position")
    limit = _number(tolerance, "tolerance")
    if limit < 0:
        raise ValueError("tolerance must be non-negative")
    error = math.hypot(observed[0] - predicted[0], observed[1] - predicted[1])
    if not math.isfinite(error):
        raise ValueError("prediction error overflowed finite numeric range")
    return error > limit

"""Analytic potential-path-area and space-time-prism slice diagnostics."""
from __future__ import annotations

from math import hypot, isfinite, pi, sqrt
from typing import Iterable, Sequence

import numpy as np


def _point(value, name):
    try:
        if len(value) != 2:
            raise ValueError
        point = (float(value[0]), float(value[1]))
    except (TypeError, ValueError, IndexError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite planar x/y pair") from exc
    if not all(isfinite(x) for x in point):
        raise ValueError(f"{name} must be a finite planar x/y pair")
    return point


def potential_path_area(
    origin: Sequence[float],
    destination: Sequence[float],
    *,
    duration: float,
    speed: float,
) -> dict:
    """Return the Euclidean potential path area as an ellipse.

    A point is feasible when its distance from origin plus distance to
    destination is no greater than speed * duration.
    """
    start = _point(origin, "origin")
    end = _point(destination, "destination")
    if not isfinite(duration) or duration < 0:
        raise ValueError("duration must be finite and non-negative")
    if not isfinite(speed) or speed <= 0:
        raise ValueError("speed must be finite and positive")
    dx, dy = end[0] - start[0], end[1] - start[1]
    focal_distance = hypot(dx, dy)
    major = speed * duration / 2
    if major < focal_distance / 2:
        return {
            "feasible": False,
            "semi_major": major,
            "semi_minor": 0.0,
            "focal_distance": focal_distance,
            "area": 0.0,
            "bounds": None,
        }
    minor = sqrt(max(0.0, major * major - (focal_distance / 2) ** 2))
    midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
    if focal_distance == 0:
        angle = 0.0
    else:
        from math import atan2
        angle = atan2(dy, dx)
    # Axis-aligned half-width/height of the rotated ellipse.
    half_x = sqrt((major * __import__("math").cos(angle)) ** 2 + (minor * __import__("math").sin(angle)) ** 2)
    half_y = sqrt((major * __import__("math").sin(angle)) ** 2 + (minor * __import__("math").cos(angle)) ** 2)
    return {
        "feasible": True,
        "semi_major": major,
        "semi_minor": minor,
        "focal_distance": focal_distance,
        "orientation_radians": angle,
        "centre": midpoint,
        "area": pi * major * minor,
        "bounds": (midpoint[0] - half_x, midpoint[1] - half_y, midpoint[0] + half_x, midpoint[1] + half_y),
    }


def contains_potential_path_points(
    points: Iterable[Sequence[float]],
    origin: Sequence[float],
    destination: Sequence[float],
    *,
    duration: float,
    speed: float,
    tolerance: float = 1e-12,
) -> np.ndarray:
    """Test points against the sum-of-distances potential-path condition."""
    area = potential_path_area(origin, destination, duration=duration, speed=speed)
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    try:
        candidates = np.asarray([_point(point, "candidate") for point in points], dtype=float)
    except TypeError as exc:
        raise ValueError("points must be an iterable of x/y pairs") from exc
    if candidates.size == 0:
        return np.zeros(0, dtype=bool)
    if candidates.ndim != 2 or candidates.shape[1] != 2:
        raise ValueError("points must be an iterable of x/y pairs")
    if not area["feasible"]:
        return np.zeros(candidates.shape[0], dtype=bool)
    start = np.asarray(_point(origin, "origin"))
    end = np.asarray(_point(destination, "destination"))
    budget = speed * duration + tolerance
    return (np.linalg.norm(candidates - start, axis=1) + np.linalg.norm(candidates - end, axis=1)) <= budget


def space_time_prism_slice(
    origin: Sequence[float],
    destination: Sequence[float],
    *,
    departure_time: float,
    arrival_time: float,
    time: float,
    speed: float,
) -> dict:
    """Describe the cross-section as an intersection of two reachable disks."""
    start = _point(origin, "origin")
    end = _point(destination, "destination")
    if not all(isfinite(x) for x in (departure_time, arrival_time, time)):
        raise ValueError("times must be finite")
    if arrival_time < departure_time or not departure_time <= time <= arrival_time:
        raise ValueError("time must lie within an ordered departure/arrival interval")
    if not isfinite(speed) or speed <= 0:
        raise ValueError("speed must be finite and positive")
    return {
        "time": float(time),
        "disks": [
            {"centre": start, "radius": speed * (time - departure_time)},
            {"centre": end, "radius": speed * (arrival_time - time)},
        ],
    }

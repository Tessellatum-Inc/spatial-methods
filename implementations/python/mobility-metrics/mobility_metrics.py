"""Descriptive mobility metrics for ordered planar trajectories and visit labels."""
from __future__ import annotations

from collections import Counter
from math import exp, isfinite, log, sqrt
from typing import Hashable, Iterable, Sequence

import numpy as np


def _coordinates(points: Iterable[Sequence[float]]) -> np.ndarray:
    array = np.asarray(points, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2 or array.shape[0] < 1:
        raise ValueError("points must be a non-empty n by 2 coordinate array")
    if not np.all(np.isfinite(array)):
        raise ValueError("coordinates must be finite")
    return array


def radius_of_gyration(points: Iterable[Sequence[float]], weights=None) -> float:
    """Weighted RMS distance from the trajectory's weighted centroid."""
    xy = _coordinates(points)
    if weights is None:
        w = np.ones(xy.shape[0], dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.ndim != 1 or w.size != xy.shape[0] or not np.all(np.isfinite(w)) or np.any(w < 0):
            raise ValueError("weights must be a finite non-negative vector matching points")
        if np.sum(w) <= 0:
            raise ValueError("weights must have positive total")
    centre = np.average(xy, axis=0, weights=w)
    return float(sqrt(np.average(np.sum((xy - centre) ** 2, axis=1), weights=w)))


def step_lengths(points: Iterable[Sequence[float]]) -> np.ndarray:
    """Euclidean lengths between consecutive projected positions."""
    xy = _coordinates(points)
    if xy.shape[0] < 2:
        raise ValueError("at least two points are required")
    return np.linalg.norm(np.diff(xy, axis=0), axis=1)


def turning_angles(points: Iterable[Sequence[float]]) -> np.ndarray:
    """Signed turns in radians, in [-pi, pi], between consecutive steps."""
    xy = _coordinates(points)
    if xy.shape[0] < 3:
        raise ValueError("at least three points are required")
    steps = np.diff(xy, axis=0)
    lengths = np.linalg.norm(steps, axis=1)
    if np.any(lengths == 0):
        raise ValueError("consecutive duplicate points make turning angles undefined")
    cross = steps[:-1, 0] * steps[1:, 1] - steps[:-1, 1] * steps[1:, 0]
    dot = np.sum(steps[:-1] * steps[1:], axis=1)
    return np.arctan2(cross, dot)


def visit_entropy(visits: Iterable[Hashable]) -> dict:
    """Shannon entropy and effective number of visited states (natural logs)."""
    try:
        labels = list(visits)
        counts = Counter(labels)
    except TypeError as exc:
        raise ValueError("visit labels must be hashable") from exc
    if not labels:
        raise ValueError("at least one visit label is required")
    probabilities = np.asarray(list(counts.values()), dtype=float) / len(labels)
    entropy = float(-np.sum(probabilities * np.log(probabilities)))
    return {
        "entropy_nats": entropy,
        "effective_states": float(exp(entropy)),
        "unique_states": len(counts),
        "visit_count": len(labels),
        "probabilities": probabilities,
    }


def maximum_predictability(entropy_nats: float, n_states: int) -> float:
    """Solve the Fano entropy bound for maximum next-state predictability."""
    if isinstance(n_states, bool) or int(n_states) != n_states or n_states < 1:
        raise ValueError("n_states must be a positive integer")
    if not isfinite(entropy_nats) or entropy_nats < 0 or entropy_nats > log(n_states) + 1e-12:
        raise ValueError("entropy_nats must lie between zero and log(n_states)")
    if n_states == 1 or entropy_nats <= 1e-14:
        return 1.0
    if entropy_nats >= log(n_states) - 1e-14:
        return 1.0 / n_states

    def f(probability):
        remainder = (1 - probability) / (n_states - 1)
        if remainder <= 0:
            return 0.0
        return -probability * log(probability) - (1 - probability) * log(remainder)

    low, high = 1.0 / n_states, 1.0
    for _ in range(100):
        middle = (low + high) / 2
        if f(middle) > entropy_nats:
            low = middle
        else:
            high = middle
    return float((low + high) / 2)

"""Small-data trajectory processing and similarity baselines.

Coordinates are projected planar x/y values in common linear units. Timestamps
are numeric values in common time units (normally seconds). No CRS or time-zone
conversion is performed.
"""
from __future__ import annotations

import math
import numpy as np


def _points(values, name, *, minimum=1):
    try:
        result = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric coordinates") from exc
    if result.ndim != 2 or result.shape[1] != 2 or len(result) < minimum:
        raise ValueError(f"{name} must have shape (n, 2), n >= {minimum}")
    if not np.isfinite(result).all():
        raise ValueError(f"{name} must contain only finite coordinates")
    return result


def _nonnegative(value, name):
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be finite and non-negative")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be finite and non-negative") from exc
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def detect_stay_points(points, timestamps, *, max_distance, min_duration):
    """Detect start-anchored stay points by distance and elapsed duration.

    For each candidate interval, points are accumulated while they remain
    within max_distance of the interval's first point. An interval is emitted
    when its elapsed time reaches min_duration. Its reported location is the
    arithmetic centroid. The first point after an emitted interval starts the
    next search. This is a transparent baseline, not a diameter-bounded or
    density-based stop detector.
    """
    xy = _points(points, "points", minimum=2)
    try:
        time = np.asarray(timestamps, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("timestamps must be a finite numeric vector") from exc
    if time.shape != (len(xy),) or not np.isfinite(time).all():
        raise ValueError("timestamps must be finite and match points")
    if np.any(np.diff(time) < 0):
        raise ValueError("timestamps must be non-decreasing")
    radius = _nonnegative(max_distance, "max_distance")
    duration = _nonnegative(min_duration, "min_duration")

    stays = []
    start = 0
    while start < len(xy) - 1:
        end = start + 1
        while end < len(xy) and np.linalg.norm(xy[end] - xy[start]) <= radius:
            end += 1
        last = end - 1
        elapsed = float(time[last] - time[start])
        if elapsed >= duration:
            stays.append({
                "start_index": start,
                "end_index": last,
                "start_time": float(time[start]),
                "end_time": float(time[last]),
                "duration": elapsed,
                "location": xy[start:last + 1].mean(axis=0),
            })
            start = last + 1
        else:
            start += 1
    return stays


def _point_segment_distance(point, start, end):
    segment = end - start
    length_squared = float(segment @ segment)
    if length_squared == 0.0:
        return float(np.linalg.norm(point - start))
    fraction = float(np.clip(((point - start) @ segment) / length_squared, 0.0, 1.0))
    projection = start + fraction * segment
    return float(np.linalg.norm(point - projection))


def douglas_peucker_indices(points, *, tolerance):
    """Return retained row indices from iterative planar Douglas-Peucker."""
    xy = _points(points, "points", minimum=1)
    epsilon = _nonnegative(tolerance, "tolerance")
    if len(xy) <= 2:
        return np.arange(len(xy), dtype=int)
    keep = np.zeros(len(xy), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(xy) - 1)]
    while stack:
        first, last = stack.pop()
        if last <= first + 1:
            continue
        distances = [
            _point_segment_distance(xy[index], xy[first], xy[last])
            for index in range(first + 1, last)
        ]
        relative = int(np.argmax(distances))
        maximum = distances[relative]
        if maximum > epsilon:
            split = first + 1 + relative
            keep[split] = True
            stack.append((first, split))
            stack.append((split, last))
    return np.flatnonzero(keep)


def douglas_peucker(points, *, tolerance):
    """Return the simplified coordinate sequence, preserving endpoints."""
    xy = _points(points, "points", minimum=1)
    return xy[douglas_peucker_indices(xy, tolerance=tolerance)]


def dtw_distance(left, right, *, window=None):
    """Compute Euclidean dynamic-time-warping distance with O(m) memory.

    The optional Sakoe-Chiba window limits the absolute difference between
    matched sequence indices. It must be at least abs(m-n).
    """
    a = _points(left, "left", minimum=1)
    b = _points(right, "right", minimum=1)
    if window is None:
        width = max(len(a), len(b))
    else:
        if isinstance(window, (bool, np.bool_)) or not isinstance(window, (int, np.integer)) or window < 0:
            raise ValueError("window must be a non-negative integer or None")
        width = int(window)
    if width < abs(len(a) - len(b)):
        raise ValueError("window must be at least the sequence-length difference")
    previous = np.full(len(b) + 1, np.inf)
    previous[0] = 0.0
    for i in range(1, len(a) + 1):
        current = np.full(len(b) + 1, np.inf)
        lo = max(1, i - width)
        hi = min(len(b), i + width)
        for j in range(lo, hi + 1):
            cost = float(np.linalg.norm(a[i - 1] - b[j - 1]))
            current[j] = cost + min(previous[j], current[j - 1], previous[j - 1])
        previous = current
    return float(previous[-1])


def lcss_similarity(left, right, *, epsilon, delta=None):
    """Return LCSS match fraction in [0, 1] using spatial and index tolerances.

    A pair matches when its Euclidean separation is at most epsilon and its
    sequence-index difference is at most delta. The score is LCSS/min(m,n).
    The dynamic program uses O(n) memory.
    """
    a = _points(left, "left", minimum=1)
    b = _points(right, "right", minimum=1)
    tolerance = _nonnegative(epsilon, "epsilon")
    if delta is None:
        width = max(len(a), len(b))
    else:
        if isinstance(delta, (bool, np.bool_)) or not isinstance(delta, (int, np.integer)) or delta < 0:
            raise ValueError("delta must be a non-negative integer or None")
        width = int(delta)
    previous = np.zeros(len(b) + 1, dtype=int)
    for i in range(1, len(a) + 1):
        current = np.zeros(len(b) + 1, dtype=int)
        lo = max(1, i - width)
        hi = min(len(b), i + width)
        for j in range(lo, hi + 1):
            if np.linalg.norm(a[i - 1] - b[j - 1]) <= tolerance:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return float(previous[-1] / min(len(a), len(b)))

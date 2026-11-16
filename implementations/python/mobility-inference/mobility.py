"""Trace staypoint extraction, candidate home/work inference and activity spaces."""
from __future__ import annotations
import numpy as np
from scipy.spatial import ConvexHull, QhullError
from sklearn.cluster import DBSCAN


def detect_staypoints(coordinates, timestamps, *, radius, minimum_duration):
    """Extract sequential dwell episodes from time-ordered planar fixes.

    A candidate staypoint extends while all fixes remain within radius of
    the episode's first fix. Timestamps are seconds and must be increasing.
    """
    xy = np.asarray(coordinates, dtype=float)
    ts = np.asarray(timestamps, dtype=float)
    if xy.ndim != 2 or xy.shape[1] != 2 or ts.ndim != 1 or len(xy) != len(ts) or len(ts) < 2:
        raise ValueError("coordinates and timestamps must be aligned with at least two fixes")
    if not np.all(np.isfinite(xy)) or not np.all(np.isfinite(ts)) or np.any(np.diff(ts) <= 0):
        raise ValueError("coordinates and timestamps must be finite and timestamps strictly increasing")
    try:
        r, duration = float(radius), float(minimum_duration)
    except (TypeError, ValueError):
        raise ValueError("radius and minimum_duration must be finite and positive") from None
    if not np.isfinite(r) or r <= 0 or not np.isfinite(duration) or duration <= 0:
        raise ValueError("radius and minimum_duration must be finite and positive")
    results = []
    i = 0
    while i < len(ts)-1:
        distances = np.linalg.norm(xy[i+1:] - xy[i], axis=1)
        outside = np.flatnonzero(distances > r)
        j = i + 1 + int(outside[0]) if outside.size else len(ts)
        end = j - 1
        elapsed = ts[end] - ts[i]
        if elapsed >= duration:
            segment = xy[i:end+1]
            results.append({"centroid": segment.mean(axis=0),
                            "start": float(ts[i]), "end": float(ts[end]),
                            "duration": float(elapsed), "start_index": i,
                            "end_index": end})
            i = j
        else:
            i += 1
    return results


def infer_home_work(staypoints, *, eps, min_samples=2,
                    timezone_offset_hours=0.0,
                    home_hours=(20, 6), work_hours=(9, 17)):
    """Infer candidate home/work clusters from night/day staypoints.

    Epoch timestamps are shifted by a fixed timezone offset. The cluster with
    the greatest total dwell duration is selected; output locations are
    dwell-weighted centroids. This is a simple candidate-ranking heuristic.
    """
    if not staypoints:
        return {"home": None, "work": None}
    xy = np.asarray([s["centroid"] for s in staypoints], dtype=float)
    starts = np.asarray([s["start"] for s in staypoints], dtype=float)
    durations = np.asarray([s["duration"] for s in staypoints], dtype=float)
    if xy.ndim != 2 or xy.shape[1] != 2 or not np.all(np.isfinite(xy)) or not np.all(np.isfinite(starts)) or not np.all(np.isfinite(durations)) or np.any(durations <= 0):
        raise ValueError("staypoints must contain finite centroids, starts and positive durations")
    try:
        radius, offset = float(eps), float(timezone_offset_hours)
    except (TypeError, ValueError):
        raise ValueError("eps and timezone offset must be finite") from None
    if not np.isfinite(radius) or radius <= 0 or not np.isfinite(offset):
        raise ValueError("eps must be positive and timezone offset finite")
    if isinstance(min_samples, (bool, np.bool_)) or not isinstance(min_samples, (int, np.integer)) or min_samples < 1:
        raise ValueError("min_samples must be a positive integer")
    def in_window(hour, window):
        start, end = window
        return (start <= hour < end) if start < end else (hour >= start or hour < end)
    hours = np.mod(starts / 3600.0 + offset, 24.0)
    def best(window):
        ids = np.flatnonzero([in_window(h, window) for h in hours])
        if ids.size == 0:
            return None
        labels = DBSCAN(eps=radius, min_samples=int(min_samples)).fit_predict(xy[ids])
        candidates = []
        for label_id in sorted(set(labels) - {-1}):
            members = ids[labels == label_id]
            mass = durations[members]
            candidates.append((float(mass.sum()), members, mass))
        if not candidates:
            return None
        total, members, mass = max(candidates, key=lambda item: (item[0], -int(item[1][0])))
        return {"location": np.average(xy[members], axis=0, weights=mass),
                "total_dwell": total, "visits": int(len(members)),
                "staypoint_indices": members}
    return {"home": best(home_hours), "work": best(work_hours)}


def activity_space_metrics(coordinates):
    """Return radius of gyration and convex-hull area for planar trace points."""
    xy = np.asarray(coordinates, dtype=float)
    if xy.ndim != 2 or xy.shape[1] != 2 or len(xy) == 0 or not np.all(np.isfinite(xy)):
        raise ValueError("coordinates must be a non-empty finite (n, 2) array")
    centre = xy.mean(axis=0)
    rg = float(np.sqrt(np.mean(np.sum((xy-centre)**2, axis=1))))
    area = 0.0
    if len(np.unique(xy, axis=0)) >= 3:
        try:
            area = float(ConvexHull(xy).volume)
        except QhullError:
            area = 0.0
    return {"centroid": centre, "radius_of_gyration": rg,
            "convex_hull_area": area}

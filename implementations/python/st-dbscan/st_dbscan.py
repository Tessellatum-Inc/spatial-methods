"""Spatiotemporal DBSCAN with joint spatial and temporal neighbourhoods."""
from __future__ import annotations
from collections import deque
from math import dist, isfinite
from typing import Sequence


def st_dbscan(
    spatial_points: Sequence[Sequence[float]],
    timestamps: Sequence[float],
    *,
    eps_spatial: float,
    eps_temporal: float,
    min_samples: int = 5,
) -> dict:
    """Cluster points when both spatial and temporal thresholds are satisfied.

    A point j is a neighbour of i iff Euclidean distance in the supplied
    projected coordinate space is <= eps_spatial AND absolute timestamp
    difference is <= eps_temporal. min_samples includes the point itself.
    Ambiguous border points are assigned to the first cluster reached in
    input order, matching a deterministic DBSCAN expansion policy.

    This O(n^2) implementation is intended for teaching and modest datasets.
    """
    points = []
    for row in spatial_points:
        try:
            point = tuple(float(value) for value in row)
        except (TypeError, ValueError):
            raise ValueError("spatial_points must be a finite rectangular coordinate array") from None
        if not point or not all(isfinite(value) for value in point):
            raise ValueError("spatial_points must be a finite rectangular coordinate array")
        points.append(point)
    n = len(points)
    if n == 0:
        raise ValueError("at least one spatial point is required")
    dimensions = len(points[0])
    if any(len(point) != dimensions for point in points):
        raise ValueError("spatial_points must have a consistent coordinate dimension")
    try:
        times = [float(value) for value in timestamps]
    except (TypeError, ValueError):
        raise ValueError("timestamps must be a finite numeric vector") from None
    if len(times) != n or not all(isfinite(value) for value in times):
        raise ValueError("timestamps must be a finite numeric vector matching spatial_points")
    spatial_radius = float(eps_spatial)
    temporal_radius = float(eps_temporal)
    if not isfinite(spatial_radius) or spatial_radius < 0:
        raise ValueError("eps_spatial must be finite and non-negative")
    if not isfinite(temporal_radius) or temporal_radius < 0:
        raise ValueError("eps_temporal must be finite and non-negative")
    if isinstance(min_samples, bool) or not isinstance(min_samples, int) or min_samples < 1:
        raise ValueError("min_samples must be a positive integer")

    neighbours = []
    for i in range(n):
        neighbours.append([
            j for j in range(n)
            if dist(points[i], points[j]) <= spatial_radius
            and abs(times[i] - times[j]) <= temporal_radius
        ])
    counts = [len(items) for items in neighbours]
    core = [count >= min_samples for count in counts]

    unvisited = -2
    noise = -1
    labels = [unvisited] * n
    cluster_id = 0
    for i in range(n):
        if labels[i] != unvisited:
            continue
        if not core[i]:
            labels[i] = noise
            continue
        labels[i] = cluster_id
        queue = deque(neighbours[i])
        queued = set(neighbours[i])
        while queue:
            j = queue.popleft()
            if labels[j] == noise:
                labels[j] = cluster_id
            if labels[j] != unvisited:
                continue
            labels[j] = cluster_id
            if core[j]:
                for candidate in neighbours[j]:
                    if candidate not in queued:
                        queued.add(candidate)
                        queue.append(candidate)
        cluster_id += 1

    return {
        "labels": tuple(labels),
        "core_points": tuple(core),
        "neighbour_counts": tuple(counts),
        "n_clusters": cluster_id,
        "noise_label": noise,
        "eps_spatial": spatial_radius,
        "eps_temporal": temporal_radius,
        "min_samples": min_samples,
    }

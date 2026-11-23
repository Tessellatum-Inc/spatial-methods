"""Exact dense Ward agglomerative hierarchical clustering."""
from __future__ import annotations
import numpy as np


def _observations(values):
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or x.shape[0] == 0 or x.shape[1] == 0:
        raise ValueError("observations must be a non-empty 2-D array")
    if not np.isfinite(x).all():
        raise ValueError("observations must contain only finite values")
    return x


def ward_linkage(observations: np.ndarray) -> np.ndarray:
    """Return an (n-1, 4) Ward linkage matrix for finite Euclidean rows.

    Each row is [left_cluster_id, right_cluster_id, merge_height, size].
    The merge height is sqrt(2 * increase in within-cluster sum of squares).
    Ties are resolved by the lexicographically smallest active cluster pair.
    """
    x = _observations(observations)
    n = len(x)
    if n < 2:
        raise ValueError("at least two observations are required")
    centers = {i: x[i].copy() for i in range(n)}
    sizes = {i: 1 for i in range(n)}
    active = set(range(n))
    rows = []
    for step in range(n - 1):
        best_pair, best_delta = None, np.inf
        ordered = sorted(active)
        for pos, left in enumerate(ordered):
            for right in ordered[pos + 1:]:
                delta = (sizes[left] * sizes[right] / (sizes[left] + sizes[right])
                         * float(np.sum((centers[left] - centers[right]) ** 2)))
                if delta < best_delta:
                    best_delta, best_pair = delta, (left, right)
        left, right = best_pair
        new_id = n + step
        new_size = sizes[left] + sizes[right]
        new_center = (sizes[left] * centers[left] + sizes[right] * centers[right]) / new_size
        rows.append([left, right, np.sqrt(2.0 * best_delta), new_size])
        active.remove(left)
        active.remove(right)
        active.add(new_id)
        centers[new_id], sizes[new_id] = new_center, new_size
    return np.asarray(rows, dtype=float)


def cut_ward_tree(linkage: np.ndarray, n_observations: int, k: int) -> np.ndarray:
    """Cut a Ward linkage matrix into k clusters; labels follow cluster-id order."""
    if isinstance(n_observations, (bool, np.bool_)) or not isinstance(n_observations, (int, np.integer)) or n_observations < 1:
        raise ValueError("n_observations must be a positive integer")
    n = int(n_observations)
    if isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) or not 1 <= k <= n:
        raise ValueError("k must be an integer between 1 and n_observations")
    z = np.asarray(linkage, dtype=float)
    if z.shape != (max(0, n - 1), 4) or not np.isfinite(z).all():
        raise ValueError("linkage must be a finite (n_observations - 1, 4) matrix")
    clusters = {i: {i} for i in range(n)}
    active = set(range(n))
    for step, row in enumerate(z[:n - int(k)]):
        left_f, right_f, height, size_f = row
        if left_f != int(left_f) or right_f != int(right_f):
            raise ValueError("linkage cluster ids must be integers")
        left, right = int(left_f), int(right_f)
        if left == right or left not in active or right not in active:
            raise ValueError("linkage references inactive or identical clusters")
        merged = clusters[left] | clusters[right]
        if size_f != len(merged):
            raise ValueError("linkage cluster size is inconsistent")
        new_id = n + step
        active.remove(left)
        active.remove(right)
        active.add(new_id)
        clusters[new_id] = merged
    labels = np.empty(n, dtype=int)
    for label, cluster_id in enumerate(sorted(active)):
        labels[list(clusters[cluster_id])] = label
    return labels


def ward_clustering(observations: np.ndarray, k: int) -> dict:
    """Fit Ward's hierarchy and return its k-cluster flat partition."""
    x = _observations(observations)
    if isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) or not 1 <= k <= len(x):
        raise ValueError("k must be an integer between 1 and n_observations")
    linkage = ward_linkage(x) if len(x) > 1 else np.empty((0, 4), dtype=float)
    labels = cut_ward_tree(linkage, len(x), int(k))
    return {"linkage": linkage, "labels": labels, "k": int(k)}

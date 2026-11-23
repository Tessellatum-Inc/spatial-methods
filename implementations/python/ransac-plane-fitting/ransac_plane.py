"""Deterministic-seed RANSAC plane fitting for 3D point clouds."""
from __future__ import annotations
import numpy as np


def _normalise_orientation(normal):
    normal = np.asarray(normal, dtype=float)
    pivot = int(np.argmax(np.abs(normal)))
    return -normal if normal[pivot] < 0 else normal


def _fit_plane(points):
    centre = points.mean(axis=0)
    _, singular, vt = np.linalg.svd(points - centre, full_matrices=False)
    if singular.size < 2 or singular[1] <= np.finfo(float).eps * max(singular[0], 1.0) * 10:
        raise ValueError("plane inliers must contain at least three non-collinear points")
    normal = _normalise_orientation(vt[-1])
    offset = -float(normal @ centre)
    return normal, offset


def ransac_plane(points, distance_threshold=0.05, max_trials=1000,
                 min_inliers=3, random_state=None):
    """Fit plane ax+by+cz+d=0 and return model, inliers and residuals.

    RANSAC samples three points, scores absolute orthogonal distances, and
    refits the best consensus set by total least squares (SVD). The returned
    inlier mask is aligned with the input points.
    """
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 3 or p.shape[0] < 3 or not np.all(np.isfinite(p)):
        raise ValueError("points must be a finite N x 3 array with N >= 3")
    if not np.isfinite(distance_threshold) or distance_threshold <= 0:
        raise ValueError("distance_threshold must be finite and positive")
    if not isinstance(max_trials, int) or isinstance(max_trials, bool) or max_trials < 1:
        raise ValueError("max_trials must be a positive integer")
    if not isinstance(min_inliers, int) or isinstance(min_inliers, bool) or min_inliers < 3 or min_inliers > len(p):
        raise ValueError("min_inliers must be an integer between 3 and N")
    rng = np.random.default_rng(random_state)
    best_mask, best_count, best_error = None, -1, np.inf
    for _ in range(max_trials):
        sample = p[rng.choice(len(p), size=3, replace=False)]
        cross = np.cross(sample[1] - sample[0], sample[2] - sample[0])
        norm = float(np.linalg.norm(cross))
        if norm <= np.finfo(float).eps:
            continue
        normal = cross / norm
        offset = -float(normal @ sample[0])
        distances = np.abs(p @ normal + offset)
        mask = distances <= distance_threshold
        count = int(np.count_nonzero(mask))
        error = float(np.sum(distances[mask])) if count else np.inf
        if count > best_count or (count == best_count and error < best_error):
            best_mask, best_count, best_error = mask, count, error
    if best_mask is None or best_count < min_inliers:
        raise ValueError("RANSAC did not find a plane with the required consensus size")
    mask = best_mask
    for _ in range(5):
        normal, offset = _fit_plane(p[mask])
        distances = np.abs(p @ normal + offset)
        updated = distances <= distance_threshold
        if np.array_equal(updated, mask):
            break
        if np.count_nonzero(updated) < min_inliers:
            break
        mask = updated
    normal, offset = _fit_plane(p[mask])
    residuals = np.abs(p @ normal + offset)
    mask = residuals <= distance_threshold
    if np.count_nonzero(mask) < min_inliers:
        raise ValueError("refined plane has fewer than min_inliers")
    normal, offset = _fit_plane(p[mask])
    residuals = np.abs(p @ normal + offset)
    return {"normal": normal, "offset": offset, "inliers": mask,
            "residuals": residuals, "n_inliers": int(np.count_nonzero(mask))}

"""Spherical statistics on S2: intrinsic means, clustering and vMF kernels."""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def _unit_rows(values: ArrayLike, *, name: str = "vectors") -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or x.shape[1] != 3 or x.shape[0] == 0:
        raise ValueError(f"{name} must be a non-empty (n, 3) array")
    if not np.isfinite(x).all():
        raise ValueError(f"{name} must be finite")
    norms = np.linalg.norm(x, axis=1)
    if np.any(norms <= 0):
        raise ValueError(f"{name} cannot contain zero vectors")
    return x / norms[:, None]


def angular_distance(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Great-circle central angles (radians) between broadcastable unit vectors."""
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    if x.shape[-1:] != (3,) or y.shape[-1:] != (3,):
        raise ValueError("vectors must end in dimension three")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("vectors must be finite")
    nx, ny = np.linalg.norm(x, axis=-1), np.linalg.norm(y, axis=-1)
    if np.any(nx <= 0) or np.any(ny <= 0):
        raise ValueError("zero vectors have no spherical direction")
    dots = np.sum((x / nx[..., None]) * (y / ny[..., None]), axis=-1)
    return np.arccos(np.clip(dots, -1.0, 1.0))


def frechet_mean_sphere(
    vectors: ArrayLike, *, tolerance: float = 1e-10, max_iterations: int = 500
) -> dict:
    """Approximate intrinsic Fréchet mean on S2 by Karcher tangent updates.

    A medoid initializes the iteration. The method minimizes squared geodesic
    distances locally; points at the antipode of an iterate are cut-locus
    singularities and are rejected rather than assigned an arbitrary tangent.
    """
    x = _unit_rows(vectors)
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    dots = np.clip(x @ x.T, -1.0, 1.0)
    distances = np.arccos(dots)
    objective = np.sum(distances * distances, axis=1)
    mean = x[int(np.argmin(objective))].copy()
    converged = False
    iterations = 0
    for iteration in range(1, int(max_iterations) + 1):
        dots = np.clip(x @ mean, -1.0, 1.0)
        theta = np.arccos(dots)
        if np.any((np.pi - theta) < 1e-10):
            raise ValueError("Fréchet iteration encountered an antipodal cut-locus point")
        tangent = x - dots[:, None] * mean[None, :]
        norms = np.linalg.norm(tangent, axis=1)
        factors = np.divide(theta, norms, out=np.ones_like(theta), where=norms > 1e-14)
        logs = tangent * factors[:, None]
        update = np.mean(logs, axis=0)
        update -= np.dot(update, mean) * mean
        step = float(np.linalg.norm(update))
        iterations = iteration
        if step <= tolerance:
            converged = True
            break
        # Exponential map on the sphere.
        direction = update / step
        candidate = np.cos(step) * mean + np.sin(step) * direction
        mean = candidate / np.linalg.norm(candidate)
    final_angles = np.arccos(np.clip(x @ mean, -1.0, 1.0))
    return {
        "mean": mean,
        "mean_squared_geodesic_distance": float(np.mean(final_angles**2)),
        "mean_geodesic_distance": float(np.mean(final_angles)),
        "iterations": iterations,
        "converged": converged,
    }


def spherical_kmeans(
    vectors: ArrayLike, n_clusters: int, *, max_iterations: int = 300,
    tolerance: float = 1e-8, seed: int = 0
) -> dict:
    """Spherical k-means minimizing cosine/angular dissimilarity on S2.

    Uses seeded spherical k-means++ initialization and normalized resultant
    centroids. Empty clusters are reseeded at the currently worst represented
    observation. Cluster labels are zero-based; objective is sum(1 - cosine).
    """
    x = _unit_rows(vectors)
    n = len(x)
    if isinstance(n_clusters, (bool, np.bool_)) or not isinstance(n_clusters, (int, np.integer)) or not 1 <= n_clusters <= n:
        raise ValueError("n_clusters must be an integer between one and n")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)):
        raise ValueError("seed must be an integer")
    rng = np.random.default_rng(int(seed))
    centers = [x[int(rng.integers(n))]]
    while len(centers) < int(n_clusters):
        similarity = x @ np.asarray(centers).T
        nearest_distance = np.maximum(0.0, 1.0 - np.max(similarity, axis=1))
        probabilities = nearest_distance**2
        if probabilities.sum() <= 1e-15:
            remaining = [i for i in range(n) if not any(np.allclose(x[i], c) for c in centers)]
            centers.append(x[remaining[0] if remaining else len(centers) % n])
        else:
            centers.append(x[int(rng.choice(n, p=probabilities/probabilities.sum()))])
    centers = np.asarray(centers, dtype=float)
    labels = np.full(n, -1, dtype=int)
    converged = False
    for iteration in range(1, int(max_iterations) + 1):
        similarities = x @ centers.T
        new_labels = np.argmax(similarities, axis=1)
        new_centers = centers.copy()
        assigned_similarity = similarities[np.arange(n), new_labels]
        for cluster in range(int(n_clusters)):
            members = x[new_labels == cluster]
            if len(members):
                resultant = members.sum(axis=0)
                norm = np.linalg.norm(resultant)
                if norm > 1e-14:
                    new_centers[cluster] = resultant / norm
                else:
                    worst = int(np.argmin(assigned_similarity))
                    new_centers[cluster] = x[worst]
            else:
                worst = int(np.argmin(assigned_similarity))
                new_centers[cluster] = x[worst]
        shift = float(np.max(angular_distance(centers, new_centers)))
        stable = np.array_equal(new_labels, labels)
        labels, centers = new_labels, new_centers
        if stable or shift <= tolerance:
            converged = True
            break
    similarities = x @ centers.T
    labels = np.argmax(similarities, axis=1)
    objective = float(np.sum(1.0 - similarities[np.arange(n), labels]))
    return {"labels": labels, "centers": centers, "objective": objective,
            "iterations": iteration, "converged": converged}


def _log_vmf_normalizer_3d(kappa: float) -> float:
    if kappa == 0:
        return -np.log(4.0 * np.pi)
    # log(sinh(kappa)) without overflow for large concentration.
    log_sinh = kappa - np.log(2.0) + np.log1p(-np.exp(-2.0*kappa))
    return float(np.log(kappa) - np.log(4.0*np.pi) - log_sinh)


def von_mises_fisher_density(
    vectors: ArrayLike, mean_direction: ArrayLike, concentration: float
) -> np.ndarray:
    """Evaluate the normalized 3-D von Mises-Fisher density on S2."""
    x = _unit_rows(vectors)
    mu = _unit_rows(np.asarray(mean_direction, dtype=float).reshape(1, 3))[0]
    kappa = float(concentration)
    if not np.isfinite(kappa) or kappa < 0:
        raise ValueError("concentration must be finite and nonnegative")
    log_density = _log_vmf_normalizer_3d(kappa) + kappa * (x @ mu)
    return np.exp(log_density)


def spherical_vmf_kde(
    query_vectors: ArrayLike, sample_vectors: ArrayLike, *, concentration: float,
    weights: ArrayLike | None = None
) -> np.ndarray:
    """Evaluate a normalized weighted vMF kernel density estimate on S2."""
    query = _unit_rows(query_vectors, name="query_vectors")
    samples = _unit_rows(sample_vectors, name="sample_vectors")
    kappa = float(concentration)
    if not np.isfinite(kappa) or kappa < 0:
        raise ValueError("concentration must be finite and nonnegative")
    if weights is None:
        w = np.ones(len(samples), dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != (len(samples),) or not np.isfinite(w).all() or np.any(w < 0) or w.sum() <= 0:
            raise ValueError("weights must be finite, nonnegative, match samples and have positive sum")
    log_c = _log_vmf_normalizer_3d(kappa)
    density = np.exp(log_c + kappa * (query @ samples.T)) @ w
    return density / w.sum()

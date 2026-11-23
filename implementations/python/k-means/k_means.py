"""Lloyd k-means with k-means++ seeding and deterministic empty-cluster repair."""
from __future__ import annotations
import numpy as np


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _initial_centers(x: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    n = len(x)
    chosen = [int(rng.integers(n))]
    closest = np.sum((x - x[chosen[0]]) ** 2, axis=1)
    while len(chosen) < k:
        total = float(closest.sum())
        if total <= 0:
            index = next(i for i in range(n) if i not in chosen)
        else:
            index = int(rng.choice(n, p=closest / total))
            if index in chosen:
                index = next(i for i in range(n) if i not in chosen)
        chosen.append(index)
        closest = np.minimum(closest, np.sum((x - x[index]) ** 2, axis=1))
    return x[chosen].copy()


def _assign(x: np.ndarray, centers: np.ndarray):
    squared = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2)
    labels = np.argmin(squared, axis=1)
    return labels, squared[np.arange(len(x)), labels]


def _repair_empty(labels: np.ndarray, residual: np.ndarray, k: int) -> np.ndarray:
    labels = labels.copy()
    counts = np.bincount(labels, minlength=k)
    for empty in np.flatnonzero(counts == 0):
        candidates = np.argsort(-residual, kind="stable")
        donor = next((int(i) for i in candidates if counts[labels[i]] > 1), None)
        if donor is None:
            raise RuntimeError("unable to repair an empty cluster")
        counts[labels[donor]] -= 1
        labels[donor] = int(empty)
        counts[empty] += 1
        residual[donor] = -np.inf
    return labels


def kmeans(observations: np.ndarray, k: int, *, max_iter: int = 300,
           tol: float = 1e-6, n_init: int = 10,
           random_state: int | None = 0) -> dict:
    """Cluster finite numeric rows by squared Euclidean distance."""
    x = np.asarray(observations, dtype=float)
    if x.ndim != 2 or x.shape[0] == 0 or x.shape[1] == 0:
        raise ValueError("observations must be a non-empty 2-D array")
    if not np.isfinite(x).all():
        raise ValueError("observations must contain only finite values")
    n = len(x)
    k = _positive_int(k, "k")
    if k > n:
        raise ValueError("k must not exceed the number of observations")
    max_iter = _positive_int(max_iter, "max_iter")
    n_init = _positive_int(n_init, "n_init")
    if isinstance(tol, (bool, np.bool_)):
        raise ValueError("tol must be finite and non-negative")
    try:
        tol = float(tol)
    except (TypeError, ValueError) as exc:
        raise ValueError("tol must be finite and non-negative") from exc
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("tol must be finite and non-negative")

    rng = np.random.default_rng(random_state)
    best, best_inertia = None, np.inf
    for _ in range(n_init):
        centers = _initial_centers(x, k, rng)
        previous_labels, converged = None, False
        for iteration in range(1, max_iter + 1):
            labels, residual = _assign(x, centers)
            labels = _repair_empty(labels, residual.copy(), k)
            updated = np.vstack([x[labels == j].mean(axis=0) for j in range(k)])
            shift = float(np.max(np.linalg.norm(updated - centers, axis=1)))
            stable = previous_labels is not None and np.array_equal(labels, previous_labels)
            centers = updated
            if stable and shift <= tol:
                converged = True
                break
            previous_labels = labels.copy()
        labels, residual = _assign(x, centers)
        labels = _repair_empty(labels, residual.copy(), k)
        centers = np.vstack([x[labels == j].mean(axis=0) for j in range(k)])
        inertia = float(np.sum((x - centers[labels]) ** 2))
        if inertia < best_inertia:
            best_inertia = inertia
            best = {"centers": centers.copy(), "labels": labels.copy(),
                    "inertia": inertia, "n_iter": iteration,
                    "converged": converged, "initialization": "k-means++"}
    return best

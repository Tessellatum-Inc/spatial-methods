"""PAM k-medoids and CLARA for precomputed dissimilarities."""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def euclidean_dissimilarity(points: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    """Return the dense Euclidean dissimilarity matrix for finite feature rows."""
    values = np.asarray(points, dtype=float)
    if values.ndim != 2 or values.shape[0] == 0 or values.shape[1] == 0:
        raise ValueError("points must have shape (n, d) with n, d >= 1")
    if not np.isfinite(values).all():
        raise ValueError("point coordinates must be finite")
    delta = values[:, None, :] - values[None, :, :]
    distances = np.sqrt(np.einsum("ijk,ijk->ij", delta, delta))
    np.fill_diagonal(distances, 0.0)
    return distances


def _validate_dissimilarity(dissimilarity: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    distances = np.asarray(dissimilarity, dtype=float)
    if distances.ndim != 2 or distances.shape[0] == 0 or distances.shape[0] != distances.shape[1]:
        raise ValueError("dissimilarity must be a non-empty square matrix")
    if not np.isfinite(distances).all():
        raise ValueError("dissimilarities must be finite")
    if (distances < 0).any():
        raise ValueError("dissimilarities must be non-negative")
    if not np.allclose(distances, distances.T, rtol=1e-10, atol=1e-12):
        raise ValueError("dissimilarity matrix must be symmetric")
    if not np.allclose(np.diag(distances), 0.0, rtol=0.0, atol=1e-12):
        raise ValueError("dissimilarity matrix diagonal must be zero")
    return distances


def _validate_controls(n: int, k: int, max_iter: int, tol: float) -> tuple[int, int, float]:
    if isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) or not 1 <= k <= n:
        raise ValueError("k must be an integer between 1 and the number of objects")
    if isinstance(max_iter, (bool, np.bool_)) or not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    try:
        tol = float(tol)
    except (TypeError, ValueError):
        raise ValueError("tol must be finite and non-negative") from None
    if not math.isfinite(tol) or tol < 0:
        raise ValueError("tol must be finite and non-negative")
    return int(k), int(max_iter), tol


def _assign(distances: np.ndarray, medoids: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    to_medoids = distances[:, np.asarray(medoids, dtype=int)]
    labels = np.argmin(to_medoids, axis=1)
    costs = to_medoids[np.arange(len(distances)), labels]
    return labels, costs


def pam(
    dissimilarity: Sequence[Sequence[float]] | np.ndarray,
    k: int,
    *,
    max_iter: int = 100,
    tol: float = 1e-12,
) -> dict:
    """Partition objects with deterministic BUILD and SWAP PAM steps.

    The input is a symmetric, non-negative, zero-diagonal dissimilarity
    matrix. Ties are resolved by input order. Returns medoid row indices,
    cluster labels, total dissimilarity, swap iterations and convergence.
    """
    distances = _validate_dissimilarity(dissimilarity)
    n = len(distances)
    k, max_iter, tol = _validate_controls(n, k, max_iter, tol)

    first = int(np.argmin(distances.sum(axis=0)))
    medoids = [first]
    nearest = distances[:, first].copy()

    # BUILD: greedily choose the object with the greatest reduction in cost.
    while len(medoids) < k:
        best_candidate = None
        best_cost = float("inf")
        selected = set(medoids)
        for candidate in range(n):
            if candidate in selected:
                continue
            cost = float(np.minimum(nearest, distances[:, candidate]).sum())
            if cost < best_cost - tol or (
                abs(cost - best_cost) <= tol
                and (best_candidate is None or candidate < best_candidate)
            ):
                best_cost = cost
                best_candidate = candidate
        medoids.append(best_candidate)
        nearest = np.minimum(nearest, distances[:, best_candidate])

    # SWAP: apply the best improving medoid/non-medoid exchange each round.
    converged = False
    iterations = 0
    for iteration in range(1, max_iter + 1):
        current_cost = float(np.min(distances[:, medoids], axis=1).sum())
        best_cost = current_cost
        best_move = None
        selected = set(medoids)
        for position in range(k):
            for candidate in range(n):
                if candidate in selected:
                    continue
                trial = medoids.copy()
                trial[position] = candidate
                cost = float(np.min(distances[:, trial], axis=1).sum())
                if cost < best_cost - tol:
                    best_cost = cost
                    best_move = (position, candidate)
        if best_move is None:
            converged = True
            break
        position, candidate = best_move
        medoids[position] = candidate
        iterations = iteration

    labels, assigned_costs = _assign(distances, medoids)
    return {
        "medoids": np.asarray(medoids, dtype=int),
        "labels": labels,
        "cost": float(assigned_costs.sum()),
        "iterations": iterations,
        "converged": converged,
    }


def clara(
    dissimilarity: Sequence[Sequence[float]] | np.ndarray,
    k: int,
    *,
    n_samples: int = 5,
    sample_size: int | None = None,
    random_state: int | None = 0,
    max_iter: int = 100,
    tol: float = 1e-12,
) -> dict:
    """CLARA: fit PAM to repeated samples and score medoids on all objects."""
    distances = _validate_dissimilarity(dissimilarity)
    n = len(distances)
    k, max_iter, tol = _validate_controls(n, k, max_iter, tol)
    if isinstance(n_samples, (bool, np.bool_)) or not isinstance(n_samples, (int, np.integer)) or n_samples < 1:
        raise ValueError("n_samples must be a positive integer")
    if sample_size is None:
        sample_size = min(n, max(40 + 2 * k, k))
    if isinstance(sample_size, (bool, np.bool_)) or not isinstance(sample_size, (int, np.integer)) or not k <= sample_size <= n:
        raise ValueError("sample_size must be an integer between k and n")

    rng = np.random.default_rng(random_state)
    best = None
    best_cost = float("inf")
    best_medoids = None
    for _ in range(int(n_samples)):
        sample = np.sort(rng.choice(n, size=int(sample_size), replace=False))
        fitted = pam(distances[np.ix_(sample, sample)], k, max_iter=max_iter, tol=tol)
        medoids = sample[fitted["medoids"]]
        labels, costs = _assign(distances, medoids)
        total_cost = float(costs.sum())
        medoid_key = tuple(int(value) for value in medoids)
        if (total_cost < best_cost - tol or
                (abs(total_cost - best_cost) <= tol and
                 (best_medoids is None or medoid_key < tuple(best_medoids)))):
            best_cost = total_cost
            best_medoids = medoid_key
            best = {
                "medoids": medoids.copy(),
                "labels": labels.copy(),
                "cost": total_cost,
                "sample": sample.copy(),
                "iterations": fitted["iterations"],
                "converged": fitted["converged"],
            }
    return {
        **best,
        "sample_size": int(sample_size),
        "samples_evaluated": int(n_samples),
    }


def clarans(
    dissimilarity: Sequence[Sequence[float]] | np.ndarray,
    k: int,
    *,
    max_neighbors: int = 250,
    num_local: int = 5,
    random_state: int | None = 0,
    tol: float = 1e-12,
) -> dict:
    """Randomized CLARANS medoid-neighbour search.

    Each local search samples medoid/non-medoid swaps. An improving swap is
    accepted and the unsuccessful-neighbour counter resets; after
    max_neighbors unsuccessful samples, that local minimum is recorded.
    """
    distances = _validate_dissimilarity(dissimilarity)
    n = len(distances)
    k, _, tol = _validate_controls(n, k, 1, tol)
    if isinstance(max_neighbors, (bool, np.bool_)) or not isinstance(max_neighbors, (int, np.integer)) or max_neighbors < 1:
        raise ValueError("max_neighbors must be a positive integer")
    if isinstance(num_local, (bool, np.bool_)) or not isinstance(num_local, (int, np.integer)) or num_local < 1:
        raise ValueError("num_local must be a positive integer")
    if k == n:
        medoids = np.arange(n, dtype=int)
        return {
            "medoids": medoids,
            "labels": np.arange(n, dtype=int),
            "cost": 0.0,
            "local_minima": 1,
            "neighbor_evaluations": 0,
            "converged": True,
        }

    rng = np.random.default_rng(random_state)
    best = None
    best_cost = float("inf")
    best_key = None
    total_evaluations = 0

    for _ in range(int(num_local)):
        medoids = sorted(int(v) for v in rng.choice(n, size=k, replace=False))
        current_cost = float(np.min(distances[:, medoids], axis=1).sum())
        unsuccessful = 0
        while unsuccessful < int(max_neighbors):
            position = int(rng.integers(k))
            available = np.setdiff1d(np.arange(n), np.asarray(medoids), assume_unique=True)
            candidate = int(rng.choice(available))
            trial = medoids.copy()
            trial[position] = candidate
            trial.sort()
            trial_cost = float(np.min(distances[:, trial], axis=1).sum())
            total_evaluations += 1
            if trial_cost < current_cost - tol:
                medoids = trial
                current_cost = trial_cost
                unsuccessful = 0
            else:
                unsuccessful += 1

        key = tuple(medoids)
        if (current_cost < best_cost - tol or
                (abs(current_cost - best_cost) <= tol and
                 (best_key is None or key < best_key))):
            best_cost = current_cost
            best_key = key
            labels, costs = _assign(distances, medoids)
            best = {
                "medoids": np.asarray(medoids, dtype=int),
                "labels": labels,
                "cost": float(costs.sum()),
            }

    return {
        **best,
        "local_minima": int(num_local),
        "neighbor_evaluations": total_evaluations,
        "converged": True,
    }

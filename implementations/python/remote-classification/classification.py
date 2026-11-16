"""Classical supervised and unsupervised multispectral classification."""
from __future__ import annotations

import numpy as np


def _features(values, name):
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or x.shape[0] < 1 or x.shape[1] < 1 or not np.all(np.isfinite(x)):
        raise ValueError(f"{name} must be a finite non-empty (samples, features) matrix")
    return x


def fit_gaussian_maximum_likelihood(samples, labels, *, ridge=1e-6, priors=None):
    """Fit a class-conditional multivariate Gaussian maximum-likelihood model.

    Covariances are estimated independently per class using the maximum-
    likelihood (1/n) normalization and stabilized by adding ridge times the
    global mean feature variance to the diagonal. Optional priors are supplied
    as a mapping from observed class labels to positive probabilities.
    """
    x = _features(samples, "samples")
    y = np.asarray(labels)
    if y.ndim != 1 or y.shape[0] != x.shape[0] or y.dtype.kind not in "biufUS":
        raise ValueError("labels must be a one-dimensional array matching samples")
    if y.dtype.kind in "fiu" and not np.all(np.isfinite(y)):
        raise ValueError("numeric class labels must be finite")
    classes, counts = np.unique(y, return_counts=True)
    if classes.size < 2 or np.any(counts < 2):
        raise ValueError("at least two classes with two or more samples each are required")
    if not np.isfinite(ridge) or ridge <= 0:
        raise ValueError("ridge must be positive and finite")
    scale = max(float(np.mean(np.var(x, axis=0))), np.finfo(float).eps)
    means, covariances, log_priors = [], [], []
    if priors is not None:
        if not hasattr(priors, "keys") or set(priors) != set(classes.tolist()):
            raise ValueError("priors must map every observed class and no other class")
        p = np.asarray([priors[c] for c in classes], dtype=float)
        if not np.all(np.isfinite(p)) or np.any(p <= 0):
            raise ValueError("class priors must be positive and finite")
        p /= p.sum()
    else:
        p = counts / counts.sum()
    for i, label in enumerate(classes):
        group = x[y == label]
        mean = group.mean(axis=0)
        centered = group - mean
        covariance = centered.T @ centered / group.shape[0]
        covariance += np.eye(x.shape[1]) * ridge * scale
        sign, logdet = np.linalg.slogdet(covariance)
        if sign <= 0:
            raise ValueError("regularized class covariance is not positive definite")
        means.append(mean)
        covariances.append(covariance)
        log_priors.append(np.log(p[i]))
    return {
        "classes": classes,
        "means": np.asarray(means),
        "covariances": np.asarray(covariances),
        "log_priors": np.asarray(log_priors),
        "ridge": float(ridge),
    }


def predict_gaussian_maximum_likelihood(model, samples, *, return_scores=False):
    """Predict class labels using multivariate Gaussian log posteriors."""
    x = _features(samples, "samples")
    classes = np.asarray(model["classes"])
    means = np.asarray(model["means"], dtype=float)
    covariances = np.asarray(model["covariances"], dtype=float)
    log_priors = np.asarray(model["log_priors"], dtype=float)
    if means.shape != (classes.size, x.shape[1]) or covariances.shape != (
        classes.size, x.shape[1], x.shape[1]
    ) or log_priors.shape != (classes.size,):
        raise ValueError("model dimensions do not match sample features")
    scores = np.empty((x.shape[0], classes.size), dtype=float)
    for i, covariance in enumerate(covariances):
        sign, logdet = np.linalg.slogdet(covariance)
        if sign <= 0:
            raise ValueError("model covariance must be positive definite")
        delta = x - means[i]
        solved = np.linalg.solve(covariance, delta.T).T
        scores[:, i] = (-0.5 * (x.shape[1] * np.log(2 * np.pi) + logdet
                                + np.einsum("ij,ij->i", delta, solved))
                        + log_priors[i])
    labels = classes[np.argmax(scores, axis=1)]
    return (labels, scores) if return_scores else labels


def kmeans(samples, n_clusters, *, n_init=10, max_iterations=300,
           tolerance=1e-5, random_state=None):
    """Lloyd k-means with k-means++ initialization and multiple restarts.

    Returns labels, centroids, inertia, iteration count and convergence flag.
    Empty clusters are reseeded to currently farthest observations.
    """
    x = _features(samples, "samples")
    n, dimensions = x.shape
    if not isinstance(n_clusters, (int, np.integer)) or not 1 <= n_clusters <= n:
        raise ValueError("n_clusters must be an integer between 1 and sample count")
    if not isinstance(n_init, (int, np.integer)) or n_init < 1:
        raise ValueError("n_init must be a positive integer")
    if not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    rng = np.random.default_rng(random_state)
    best = None
    for _ in range(n_init):
        centers = np.empty((n_clusters, dimensions), dtype=float)
        centers[0] = x[rng.integers(n)]
        closest = np.sum((x - centers[0]) ** 2, axis=1)
        for j in range(1, n_clusters):
            total = closest.sum()
            if total <= 0:
                candidate = rng.integers(n)
            else:
                candidate = rng.choice(n, p=closest / total)
            centers[j] = x[candidate]
            closest = np.minimum(closest, np.sum((x - centers[j]) ** 2, axis=1))
        converged = False
        for iteration in range(1, max_iterations + 1):
            distances = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2)
            labels = np.argmin(distances, axis=1)
            new_centers = centers.copy()
            assigned_distances = distances[np.arange(n), labels]
            for j in range(n_clusters):
                members = x[labels == j]
                if members.size:
                    new_centers[j] = members.mean(axis=0)
                else:
                    farthest = int(np.argmax(assigned_distances))
                    new_centers[j] = x[farthest]
                    assigned_distances[farthest] = -1
            shift = float(np.max(np.linalg.norm(new_centers - centers, axis=1)))
            centers = new_centers
            if shift <= tolerance:
                converged = True
                break
        distances = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2)
        labels = np.argmin(distances, axis=1)
        inertia = float(np.sum(distances[np.arange(n), labels]))
        if best is None or inertia < best["inertia"]:
            best = {"labels": labels.copy(), "centroids": centers.copy(),
                    "inertia": inertia, "iterations": iteration,
                    "converged": converged}
    return best

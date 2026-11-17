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


def isodata(samples, initial_clusters, *, min_clusters=1, max_clusters=None,
            min_cluster_size=2, max_iterations=100, split_std=1.0,
            merge_distance=0.5, tolerance=1e-4, random_state=None):
    """ISODATA clustering with adaptive cluster deletion, splitting and merging.

    Cluster spread is measured by per-feature standard deviation; clusters
    split along their highest-variance feature. The closest centroid pair is
    greedily merged whenever its Euclidean distance is below merge_distance.
    """
    x = _features(samples, "samples")
    n = x.shape[0]
    if not isinstance(initial_clusters, (int, np.integer)) or not 1 <= initial_clusters <= n:
        raise ValueError("initial_clusters must be between 1 and sample count")
    if max_clusters is None:
        max_clusters = max(initial_clusters, 2 * initial_clusters)
    if not isinstance(max_clusters, (int, np.integer)) or max_clusters < 1:
        raise ValueError("max_clusters must be a positive integer")
    if not isinstance(min_clusters, (int, np.integer)) or not 1 <= min_clusters <= max_clusters:
        raise ValueError("min_clusters must lie between 1 and max_clusters")
    if initial_clusters > max_clusters:
        raise ValueError("initial_clusters cannot exceed max_clusters")
    if not isinstance(min_cluster_size, (int, np.integer)) or min_cluster_size < 1:
        raise ValueError("min_cluster_size must be a positive integer")
    if not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not np.isfinite(split_std) or split_std < 0:
        raise ValueError("split_std must be finite and nonnegative")
    if not np.isfinite(merge_distance) or merge_distance < 0:
        raise ValueError("merge_distance must be finite and nonnegative")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    rng = np.random.default_rng(random_state)
    centers = kmeans(x, initial_clusters, n_init=5,
                     random_state=int(rng.integers(0, 2**32 - 1)))["centroids"]
    converged = False
    for iteration in range(1, max_iterations + 1):
        previous = centers.copy()
        distances = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2)
        labels = np.argmin(distances, axis=1)
        counts = np.bincount(labels, minlength=len(centers))
        keep = counts >= min_cluster_size
        if np.count_nonzero(keep) >= min_clusters and not np.all(keep):
            centers = centers[keep]
            distances = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2)
            labels = np.argmin(distances, axis=1)
        groups = [x[labels == j] for j in range(len(centers))]
        nonempty = [g for g in groups if len(g)]
        if len(nonempty) < len(centers):
            centers = np.asarray([g.mean(axis=0) for g in nonempty])
            groups = [x[np.argmin(np.sum((x[:, None, :] - centers[None, :, :]) ** 2,
                                         axis=2), axis=1) == j]
                      for j in range(len(centers))]
        else:
            centers = np.asarray([g.mean(axis=0) for g in groups])

        # Split the most dispersed clusters first, up to the configured cap.
        if len(centers) < max_clusters:
            candidates = []
            for j, group in enumerate(groups):
                if len(group) >= 2:
                    std = group.std(axis=0)
                    axis = int(np.argmax(std))
                    if std[axis] > split_std:
                        candidates.append((float(std[axis]), j, axis, std[axis]))
            candidates.sort(reverse=True)
            for _, j, axis, spread in candidates:
                if len(centers) >= max_clusters:
                    break
                center = centers[j].copy()
                offset = np.zeros(x.shape[1])
                offset[axis] = 0.5 * spread
                centers[j] = center - offset
                centers = np.vstack((centers, center + offset))

        # Greedily merge the closest pair while preserving min_clusters.
        while len(centers) > min_clusters:
            pairwise = np.linalg.norm(centers[:, None, :] - centers[None, :, :], axis=2)
            pairwise[np.triu_indices(len(centers))] = np.inf
            i, j = np.unravel_index(np.argmin(pairwise), pairwise.shape)
            if pairwise[i, j] >= merge_distance:
                break
            current_labels = np.argmin(
                np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2), axis=1)
            ni = max(1, int(np.count_nonzero(current_labels == i)))
            nj = max(1, int(np.count_nonzero(current_labels == j)))
            merged = (centers[i] * ni + centers[j] * nj) / (ni + nj)
            centers = np.delete(centers, [i, j], axis=0)
            centers = np.vstack((centers, merged))

        shift = (float(np.max(np.linalg.norm(centers[:min(len(centers), len(previous))]
                                              - previous[:min(len(centers), len(previous))],
                                              axis=1)))
                 if len(centers) == len(previous) else np.inf)
        if len(centers) == len(previous) and shift <= tolerance:
            converged = True
            break

    distances = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2)
    labels = np.argmin(distances, axis=1)
    used = np.unique(labels)
    centers = centers[used]
    remap = np.full(int(used.max()) + 1, -1, dtype=int)
    remap[used] = np.arange(len(used))
    labels = remap[labels]
    inertia = float(np.sum((x - centers[labels]) ** 2))
    return {"labels": labels, "centroids": centers, "inertia": inertia,
            "iterations": iteration, "converged": converged,
            "cluster_sizes": np.bincount(labels, minlength=len(centers))}



def _validated_labels(labels, sample_count):
    y = np.asarray(labels)
    if y.ndim != 1 or y.shape[0] != sample_count or y.dtype.kind not in "biufUS":
        raise ValueError("labels must be a one-dimensional numeric or string array matching samples")
    if y.dtype.kind in "fiu" and not np.all(np.isfinite(y)):
        raise ValueError("numeric class labels must be finite")
    classes, counts = np.unique(y, return_counts=True)
    if classes.size < 2 or np.any(counts < 2):
        raise ValueError("at least two classes with two or more samples each are required")
    return y, classes


def fit_svm_classifier(samples, labels, *, kernel="rbf", C=1.0, gamma="scale",
                       degree=3, class_weight=None, random_state=0):
    """Fit a support-vector classifier for pixel/object feature vectors.

    SVC decision scores are margins, not calibrated class probabilities.
    Scale continuous features using a training-only pipeline where appropriate.
    """
    from sklearn.svm import SVC

    x = _features(samples, "samples")
    y, classes = _validated_labels(labels, x.shape[0])
    if kernel not in {"linear", "poly", "rbf", "sigmoid"}:
        raise ValueError("kernel must be linear, poly, rbf or sigmoid")
    if isinstance(C, bool) or not np.isfinite(C) or C <= 0:
        raise ValueError("C must be finite and positive")
    if isinstance(gamma, str):
        if gamma not in {"scale", "auto"}:
            raise ValueError("string gamma must be scale or auto")
    elif isinstance(gamma, bool) or not np.isfinite(gamma) or gamma <= 0:
        raise ValueError("numeric gamma must be finite and positive")
    if isinstance(degree, bool) or not isinstance(degree, int) or degree < 1:
        raise ValueError("degree must be a positive integer")
    if class_weight not in (None, "balanced") and not isinstance(class_weight, dict):
        raise ValueError("class_weight must be None, balanced or a class-weight mapping")
    if random_state is not None and (isinstance(random_state, bool) or not isinstance(random_state, int)):
        raise ValueError("random_state must be an integer or None")
    estimator = SVC(kernel=kernel, C=float(C), gamma=gamma, degree=degree,
                    class_weight=class_weight, random_state=random_state)
    estimator.fit(x, y)
    return {"estimator": estimator, "classes": classes,
            "feature_count": int(x.shape[1]), "kernel": kernel}


def predict_svm_classifier(model, samples, *, return_scores=False):
    """Predict SVM classes; optionally return uncalibrated decision margins."""
    x = _features(samples, "samples")
    if not isinstance(model, dict) or "estimator" not in model or "feature_count" not in model:
        raise ValueError("model must be returned by fit_svm_classifier")
    if x.shape[1] != model["feature_count"]:
        raise ValueError("sample feature count does not match fitted SVM")
    labels = model["estimator"].predict(x)
    if return_scores:
        return {"labels": labels, "decision_scores": model["estimator"].decision_function(x)}
    return labels


def fit_random_forest_classifier(samples, labels, *, n_estimators=200,
                                 max_depth=None, min_samples_leaf=1,
                                 max_features="sqrt", class_weight=None,
                                 random_state=0, n_jobs=1):
    """Fit a random-forest classifier for multispectral feature vectors."""
    from sklearn.ensemble import RandomForestClassifier

    x = _features(samples, "samples")
    y, classes = _validated_labels(labels, x.shape[0])
    if isinstance(n_estimators, bool) or not isinstance(n_estimators, int) or n_estimators < 1:
        raise ValueError("n_estimators must be a positive integer")
    if max_depth is not None and (isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 1):
        raise ValueError("max_depth must be a positive integer or None")
    if isinstance(min_samples_leaf, bool) or not isinstance(min_samples_leaf, int) or min_samples_leaf < 1:
        raise ValueError("min_samples_leaf must be a positive integer")
    if class_weight not in (None, "balanced", "balanced_subsample") and not isinstance(class_weight, dict):
        raise ValueError("invalid random-forest class_weight")
    if random_state is not None and (isinstance(random_state, bool) or not isinstance(random_state, int)):
        raise ValueError("random_state must be an integer or None")
    if isinstance(n_jobs, bool) or not isinstance(n_jobs, int) or n_jobs == 0:
        raise ValueError("n_jobs must be a non-zero integer")
    estimator = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth,
        min_samples_leaf=min_samples_leaf, max_features=max_features,
        class_weight=class_weight, random_state=random_state, n_jobs=n_jobs,
    )
    estimator.fit(x, y)
    return {"estimator": estimator, "classes": classes,
            "feature_count": int(x.shape[1]),
            "feature_importances": estimator.feature_importances_.copy()}


def predict_random_forest_classifier(model, samples, *, return_probabilities=False):
    """Predict forest classes; optionally return vote-fraction probabilities."""
    x = _features(samples, "samples")
    if not isinstance(model, dict) or "estimator" not in model or "feature_count" not in model:
        raise ValueError("model must be returned by fit_random_forest_classifier")
    if x.shape[1] != model["feature_count"]:
        raise ValueError("sample feature count does not match fitted forest")
    labels = model["estimator"].predict(x)
    if return_probabilities:
        return {"labels": labels, "classes": model["classes"],
                "probabilities": model["estimator"].predict_proba(x),
                "feature_importances": model["feature_importances"].copy()}
    return labels

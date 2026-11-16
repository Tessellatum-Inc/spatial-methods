"""Nearest-neighbour predictor-space applicability envelope.

This is a transparent teaching baseline, not a reference-equivalent port of
Meyer & Pebesma's Area of Applicability dissimilarity-index workflow.
"""
from __future__ import annotations
import numpy as np


def fit_applicability_envelope(training_features, *, feature_weights=None,
                               quantile=0.95, distance="manhattan"):
    """Fit a leave-one-out nearest-neighbour threshold on training predictors.

    Features are scaled by their training ranges. Feature weights are
    non-negative and normalised to sum to one. The threshold is the requested
    quantile of each training row's nearest *other* training row distance.
    """
    x = np.asarray(training_features, dtype=float)
    if x.ndim != 2 or x.shape[0] < 3 or x.shape[1] < 1 or not np.all(np.isfinite(x)):
        raise ValueError("training_features must be a finite 2D matrix with >=3 rows")
    q = float(quantile)
    if not np.isfinite(q) or not 0 < q < 1:
        raise ValueError("quantile must lie strictly between 0 and 1")
    if distance not in ("manhattan", "euclidean"):
        raise ValueError("distance must be 'manhattan' or 'euclidean'")
    ranges = np.ptp(x, axis=0)
    scales = np.where(ranges > 0, ranges, 1.0)
    if feature_weights is None:
        weights = np.full(x.shape[1], 1.0 / x.shape[1])
    else:
        weights = np.asarray(feature_weights, dtype=float)
        if weights.shape != (x.shape[1],) or not np.all(np.isfinite(weights)) or np.any(weights < 0):
            raise ValueError("feature_weights must be finite, non-negative and match feature count")
        total = float(weights.sum())
        if total <= 0:
            raise ValueError("feature_weights must have positive sum")
        weights = weights / total
    z = (x - np.min(x, axis=0)) / scales
    delta = np.abs(z[:, None, :] - z[None, :, :])
    if distance == "manhattan":
        pairwise = np.sum(delta * weights[None, None, :], axis=2)
    else:
        pairwise = np.sqrt(np.sum(delta**2 * weights[None, None, :], axis=2))
    np.fill_diagonal(pairwise, np.inf)
    loo = np.min(pairwise, axis=1)
    threshold = float(np.quantile(loo, q))
    return {
        "training_features": x.copy(),
        "feature_min": np.min(x, axis=0),
        "feature_scale": scales,
        "feature_weights": weights,
        "quantile": q,
        "threshold": threshold,
        "training_loo_distance": loo,
        "distance": distance,
    }


def predict_applicability(model, target_features):
    """Return nearest-neighbour dissimilarity and an in-envelope boolean mask."""
    x = np.asarray(target_features, dtype=float)
    if x.ndim != 2 or x.shape[1] != model["training_features"].shape[1] or not np.all(np.isfinite(x)):
        raise ValueError("target_features must be finite with the fitted feature count")
    z_train = (model["training_features"] - model["feature_min"]) / model["feature_scale"]
    z_target = (x - model["feature_min"]) / model["feature_scale"]
    delta = np.abs(z_target[:, None, :] - z_train[None, :, :])
    if model["distance"] == "manhattan":
        distances = np.sum(delta * model["feature_weights"][None, None, :], axis=2)
    else:
        distances = np.sqrt(np.sum(delta**2 * model["feature_weights"][None, None, :], axis=2))
    dissimilarity = np.min(distances, axis=1)
    return {
        "dissimilarity": dissimilarity,
        "applicable": dissimilarity <= model["threshold"],
        "threshold": model["threshold"],
    }

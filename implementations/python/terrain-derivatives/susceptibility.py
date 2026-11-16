"""Groundwater vulnerability and categorical landslide-susceptibility baselines."""
from __future__ import annotations
import numpy as np


DRASTIC_WEIGHTS = np.array([5, 4, 3, 2, 1, 5, 3], dtype=float)


def drastic_index(ratings, *, weights=DRASTIC_WEIGHTS):
    """Calculate the weighted DRASTIC index from seven 1–10 rating layers.

    Axis 0 must contain, in order: depth to water, net recharge, aquifer
    media, soil media, topography, impact of vadose zone and hydraulic
    conductivity. This function consumes ratings, not raw environmental
    measurements or locally calibrated rating tables.
    """
    values = np.asarray(ratings, dtype=float)
    w = np.asarray(weights, dtype=float)
    if values.ndim < 1 or values.shape[0] != 7:
        raise ValueError("ratings axis 0 must contain exactly seven DRASTIC layers")
    if w.shape != (7,) or np.any(~np.isfinite(w)) or np.any(w <= 0):
        raise ValueError("weights must be seven finite positive values")
    if np.any(~np.isfinite(values)) or np.any((values < 1) | (values > 10)):
        raise ValueError("DRASTIC ratings must be finite values in [1, 10]")
    return np.tensordot(w, values, axes=(0, 0))


def frequency_ratio(predictor, event, *, valid_mask=None):
    """Compute categorical frequency ratios for a binary event inventory.

    FR(category) = P(category | event) / P(category). Predictor categories
    are finite numeric values. Returns the category-to-FR mapping and a
    raster of FR values; unknown/invalid cells are NaN.
    """
    x = np.asarray(predictor)
    y = np.asarray(event)
    if x.shape != y.shape or x.size == 0:
        raise ValueError("predictor and event must have the same non-empty shape")
    if y.dtype.kind not in "biuf" or np.any(~np.isfinite(y)) or np.any((y != 0) & (y != 1)):
        raise ValueError("event must contain only finite binary 0/1 labels")
    valid = np.isfinite(x) if x.dtype.kind in "iuf" else np.ones(x.shape, dtype=bool)
    if valid_mask is not None:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != x.shape:
            raise ValueError("valid_mask must match predictor shape")
        valid &= mask
    if not np.any(valid) or not np.any(y[valid] == 1):
        raise ValueError("valid cells must include at least one event")
    categories = np.unique(x[valid])
    total = np.count_nonzero(valid)
    events = np.count_nonzero(y[valid] == 1)
    mapping = {}
    result = np.full(x.shape, np.nan, dtype=float)
    for category in categories:
        cells = valid & (x == category)
        count = np.count_nonzero(cells)
        event_count = np.count_nonzero(cells & (y == 1))
        fr = (event_count / events) / (count / total)
        mapping[category.item() if hasattr(category, "item") else category] = float(fr)
        result[cells] = fr
    return {"frequency_ratio": mapping, "raster": result}


def fit_logistic_susceptibility(predictors, event, *, ridge=1e-6, max_iter=100, tolerance=1e-8):
    """Fit binary logistic regression by damped Newton/IRLS.

    Predictors have shape (observations, features); an intercept is added.
    Returns coefficients and convergence diagnostics. Ridge penalizes slopes
    but not the intercept. This is a compact baseline, not spatially blocked
    validation or a substitute for careful inventory design.
    """
    x = np.asarray(predictors, dtype=float)
    y = np.asarray(event, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 1 or y.shape != (x.shape[0],):
        raise ValueError("predictors must be 2D and event must match observation rows")
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(y)) or np.any((y != 0) & (y != 1)):
        raise ValueError("predictors must be finite and event must be binary")
    if np.unique(y).size != 2:
        raise ValueError("event must contain both classes")
    try:
        penalty = float(ridge)
        tol = float(tolerance)
    except (TypeError, ValueError):
        raise ValueError("ridge and tolerance must be finite and non-negative") from None
    if not np.isfinite(penalty) or penalty < 0 or not np.isfinite(tol) or tol <= 0:
        raise ValueError("ridge must be non-negative and tolerance positive")
    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    design = np.column_stack((np.ones(x.shape[0]), x))
    beta = np.zeros(design.shape[1])
    regularizer = np.eye(design.shape[1]) * penalty
    regularizer[0, 0] = 0.0
    converged = False
    for iteration in range(1, max_iter + 1):
        eta = np.clip(design @ beta, -35, 35)
        probability = 1.0 / (1.0 + np.exp(-eta))
        weights = np.maximum(probability * (1.0 - probability), 1e-10)
        gradient = design.T @ (y - probability) - regularizer @ beta
        hessian = (design.T * weights) @ design + regularizer
        try:
            step = np.linalg.solve(hessian, gradient)
        except np.linalg.LinAlgError:
            step = np.linalg.pinv(hessian) @ gradient
        beta += step
        if np.max(np.abs(step)) < tol:
            converged = True
            break
    return {"coefficients": beta, "converged": converged, "iterations": iteration,
            "ridge": penalty}


def predict_logistic_susceptibility(predictors, coefficients):
    """Predict event probabilities from fitted logistic coefficients."""
    x = np.asarray(predictors, dtype=float)
    beta = np.asarray(coefficients, dtype=float)
    if x.ndim < 1 or beta.ndim != 1 or x.shape[-1] + 1 != beta.size:
        raise ValueError("predictor feature axis must match coefficient count minus intercept")
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(beta)):
        raise ValueError("predictors and coefficients must be finite")
    eta = np.clip(np.concatenate((np.ones(x.shape[:-1] + (1,)), x), axis=-1) @ beta, -35, 35)
    return 1.0 / (1.0 + np.exp(-eta))

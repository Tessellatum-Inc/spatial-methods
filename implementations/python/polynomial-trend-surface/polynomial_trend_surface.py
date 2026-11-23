"""Polynomial trend-surface regression for planar spatial observations."""
from __future__ import annotations

import math
import numpy as np


def _array(values, *, name, ndim):
    try:
        result = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric values") from exc
    if result.ndim != ndim or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite {ndim}-dimensional array")
    return result


def _degree(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value not in (0, 1, 2, 3):
        raise ValueError("degree must be an integer from 0 through 3")
    return int(value)


def _basis(points, degree):
    columns = []
    terms = []
    for total in range(degree + 1):
        for x_power in range(total, -1, -1):
            y_power = total - x_power
            columns.append((points[:, 0] ** x_power) * (points[:, 1] ** y_power))
            terms.append((x_power, y_power))
    return np.column_stack(columns), tuple(terms)


class PolynomialTrendSurface:
    """Fit a total-degree 0–3 polynomial by ordinary or weighted least squares.

    Coordinates are centered and scaled before basis construction. The model
    is a global deterministic trend estimator, not a local interpolator.
    """

    def __init__(self, points, values, *, degree=1, weights=None):
        samples = _array(points, name="points", ndim=2)
        observations = _array(values, name="values", ndim=1)
        self.degree_ = _degree(degree)
        if samples.shape[1] != 2:
            raise ValueError("points must have shape (n, 2)")
        if len(samples) == 0 or len(observations) != len(samples):
            raise ValueError("points and values must have equal non-zero length")
        self.center_ = samples.mean(axis=0)
        self.scale_ = samples.std(axis=0)
        if np.any(self.scale_ == 0):
            raise ValueError("sample coordinates must vary along both axes")
        normalized = (samples - self.center_) / self.scale_
        design, self.terms_ = _basis(normalized, self.degree_)
        if weights is None:
            root_weights = np.ones(len(samples))
        else:
            supplied = _array(weights, name="weights", ndim=1)
            if len(supplied) != len(samples) or np.any(supplied <= 0):
                raise ValueError("weights must be positive and match the sample count")
            root_weights = np.sqrt(supplied)
        weighted_design = design * root_weights[:, None]
        weighted_values = observations * root_weights
        coefficients, _, rank, _ = np.linalg.lstsq(
            weighted_design, weighted_values, rcond=None
        )
        if rank != design.shape[1]:
            raise ValueError("sample geometry does not identify all polynomial terms")
        self.coefficients_ = coefficients
        self.rank_ = int(rank)
        self.observed_ = observations.copy()
        self.fitted_ = design @ coefficients
        self.residuals_ = observations - self.fitted_
        self.rmse_ = float(np.sqrt(np.mean(self.residuals_ ** 2)))
        total = float(np.sum((observations - observations.mean()) ** 2))
        residual = float(np.sum(self.residuals_ ** 2))
        self.r_squared_ = 1.0 if total == 0 and residual == 0 else (
            1.0 - residual / total if total > 0 else float("nan")
        )

    def predict(self, queries):
        targets = _array(queries, name="queries", ndim=2)
        if targets.shape[1] != 2:
            raise ValueError("queries must have shape (m, 2)")
        if len(targets) == 0:
            return np.empty(0, dtype=float)
        normalized = (targets - self.center_) / self.scale_
        design, _ = _basis(normalized, self.degree_)
        predictions = design @ self.coefficients_
        if not np.all(np.isfinite(predictions)):
            raise ValueError("trend prediction produced non-finite values")
        return predictions


def fit_trend_surface(points, values, *, degree=1, weights=None):
    """Convenience constructor returning a fitted PolynomialTrendSurface."""
    return PolynomialTrendSurface(points, values, degree=degree, weights=weights)

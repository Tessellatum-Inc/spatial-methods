"""Local quadratic modified Shepard interpolation for planar samples."""
from __future__ import annotations

import math
import numpy as np


def _finite_array(values, *, name, ndim):
    try:
        result = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric values") from exc
    if result.ndim != ndim or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite {ndim}-dimensional array")
    return result


def _integer_control(value, *, name, minimum, maximum):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be an integer")
    result = int(value)
    if not minimum <= result <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return result


def _local_basis(offsets, radius, quadratic=True):
    dx = offsets[:, 0] / radius
    dy = offsets[:, 1] / radius
    columns = [dx, dy]
    if quadratic:
        columns.extend((dx * dx, dx * dy, dy * dy))
    return np.column_stack(columns)


class ModifiedShepard2D:
    """Blend exact-at-node local polynomial fits with compact radial weights.

    For each data node, a local quadratic (or rank-deficient linear fallback)
    is fitted to its nearest nq neighbours. Local models are blended using
    Franke–Nielson-style compact weights with support radii set by nw nearest
    neighbours. This is a transparent teaching variant, not a byte-for-byte
    reproduction of Renka's QSHEP2D implementation.
    """

    def __init__(self, points, values, *, nw=None, nq=None):
        samples = _finite_array(points, name="points", ndim=2)
        observations = _finite_array(values, name="values", ndim=1)
        if samples.shape[1] != 2 or len(samples) < 6:
            raise ValueError("points must have shape (n, 2), with n >= 6")
        if len(observations) != len(samples):
            raise ValueError("one value is required for each sample point")
        if len(np.unique(samples, axis=0)) != len(samples):
            raise ValueError("duplicate sample coordinates are not supported")
        centered = samples - samples.mean(axis=0)
        if np.linalg.matrix_rank(np.column_stack((np.ones(len(samples)), centered))) < 3:
            raise ValueError("sample coordinates must not all be collinear")

        n = len(samples)
        self.nw_ = _integer_control(nw if nw is not None else min(19, n - 1),
                                    name="nw", minimum=2, maximum=n - 1)
        self.nq_ = _integer_control(nq if nq is not None else min(13, n - 1),
                                    name="nq", minimum=5, maximum=n - 1)
        self.points_ = samples.copy()
        self.values_ = observations.copy()
        delta = samples[:, None, :] - samples[None, :, :]
        distances = np.sqrt(np.sum(delta * delta, axis=2))
        if not np.all(np.isfinite(distances)):
            raise ValueError("coordinate range produces non-finite distances")
        np.fill_diagonal(distances, np.inf)
        order = np.argsort(distances, axis=1, kind="stable")
        sorted_distances = np.take_along_axis(distances, order, axis=1)
        self.weight_radii_ = sorted_distances[:, self.nw_ - 1].copy()
        self.fit_radii_ = sorted_distances[:, self.nq_ - 1].copy()
        if np.any(self.weight_radii_ <= 0) or np.any(self.fit_radii_ <= 0):
            raise ValueError("local neighbourhood radii must be positive")

        self._coefficients = []
        self._quadratic_flags = []
        for i in range(n):
            radius = self.fit_radii_[i]
            cutoff = sorted_distances[i, self.nq_ - 1]
            tolerance = 1e-12 * max(1.0, float(cutoff))
            neighbours = np.flatnonzero(
                (np.arange(n) != i) & (distances[i] <= cutoff + tolerance)
            )
            offsets = samples[neighbours] - samples[i]
            design = _local_basis(offsets, radius, quadratic=True)
            response = observations[neighbours] - observations[i]
            scaled_distance = distances[i, neighbours] / radius
            root_weights = 1.0 / scaled_distance
            weighted_design = design * root_weights[:, None]
            weighted_response = response * root_weights
            coefficients, _, rank, _ = np.linalg.lstsq(
                weighted_design, weighted_response, rcond=None
            )
            quadratic = rank == 5
            if not quadratic:
                linear_design = _local_basis(offsets, radius, quadratic=False)
                weighted_linear = linear_design * root_weights[:, None]
                coefficients, _, linear_rank, _ = np.linalg.lstsq(
                    weighted_linear, weighted_response, rcond=None
                )
                if linear_rank < 2:
                    coefficients = np.zeros(5, dtype=float)
                    quadratic = False
                else:
                    coefficients = np.concatenate((coefficients, np.zeros(3)))
                    quadratic = False
            self._coefficients.append(coefficients)
            self._quadratic_flags.append(quadratic)

    def predict(self, queries):
        """Predict a batch; exact nodes return their observations, unsupported points None."""
        targets = _finite_array(queries, name="queries", ndim=2)
        if targets.shape[1] != 2:
            raise ValueError("queries must have shape (m, 2)")
        predictions = []
        for query in targets:
            distances = np.sqrt(np.sum((self.points_ - query) ** 2, axis=1))
            if not np.all(np.isfinite(distances)):
                raise ValueError("query coordinate range produces non-finite distances")
            exact = np.flatnonzero(distances == 0)
            if len(exact):
                predictions.append(float(self.values_[exact[0]]))
                continue
            radii = self.weight_radii_
            active = distances < radii
            if not np.any(active):
                predictions.append(None)
                continue
            log_weights = np.full(len(distances), -np.inf)
            log_weights[active] = 2.0 * (
                np.log(radii[active] - distances[active])
                - np.log(radii[active])
                - np.log(distances[active])
            )
            maximum = float(np.max(log_weights[active]))
            weights = np.exp(log_weights[active] - maximum)
            node_predictions = []
            for index in np.flatnonzero(active):
                offset = query - self.points_[index]
                basis = _local_basis(offset.reshape(1, 2), self.fit_radii_[index],
                                     quadratic=self._quadratic_flags[index])
                value = self.values_[index] + float((basis @ self._coefficients[index][:basis.shape[1]])[0])
                node_predictions.append(value)
            denominator = float(weights.sum())
            estimate = float(np.dot(weights, np.asarray(node_predictions)) / denominator)
            if not math.isfinite(estimate):
                raise ValueError("modified Shepard prediction is non-finite")
            predictions.append(estimate)
        return predictions


def modified_shepard_interpolate(points, values, queries, *, nw=None, nq=None):
    """Fit a local-quadratic modified Shepard surface and predict queries."""
    return ModifiedShepard2D(points, values, nw=nw, nq=nq).predict(queries)

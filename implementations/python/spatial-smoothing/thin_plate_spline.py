"""Exact-knot 2-D thin-plate smoothing spline for scalar spatial responses."""
from __future__ import annotations
import numpy as np


def _coordinates(value, name):
    a = np.asarray(value, dtype=float)
    if a.ndim != 2 or a.shape[1] != 2 or a.shape[0] == 0 or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a nonempty finite N-by-2 coordinate array")
    return a


def _kernel(a, b):
    delta = a[:, None, :] - b[None, :, :]
    radius = np.sqrt(np.sum(delta * delta, axis=2))
    out = np.zeros_like(radius)
    positive = radius > 0
    out[positive] = radius[positive] ** 2 * np.log(radius[positive])
    return out


def _polynomial(coords):
    return np.column_stack((np.ones(coords.shape[0]), coords[:, 0], coords[:, 1]))


class ThinPlateSpline2D:
    """2-D thin-plate smoothing spline with a user-selected penalty.

    Coordinates must be in a suitable projected Cartesian coordinate system.
    The full knot set is used, so fitting requires a dense (n+3)-square solve.
    """
    def __init__(self, smoothing=1.0):
        if not np.isfinite(smoothing) or smoothing < 0:
            raise ValueError("smoothing must be finite and nonnegative")
        self.smoothing = float(smoothing)
        self._centres = None
        self._radial = None
        self._linear = None

    def fit(self, coordinates, values):
        x = _coordinates(coordinates, "coordinates")
        y = np.asarray(values, dtype=float)
        if y.ndim != 1 or y.size != x.shape[0] or not np.all(np.isfinite(y)):
            raise ValueError("values must be a finite vector matching coordinates")
        if x.shape[0] < 3 or np.linalg.matrix_rank(_polynomial(x)) < 3:
            raise ValueError("at least three non-collinear coordinate locations are required")
        K = _kernel(x, x)
        P = _polynomial(x)
        n = x.shape[0]
        system = np.block([[K + self.smoothing * np.eye(n), P],
                           [P.T, np.zeros((3, 3))]])
        rhs = np.concatenate((y, np.zeros(3)))
        try:
            coefficients = np.linalg.solve(system, rhs)
        except np.linalg.LinAlgError as exc:
            raise ValueError("thin-plate system is singular; check duplicate locations and smoothing") from exc
        self._centres = x.copy()
        self._radial = coefficients[:n]
        self._linear = coefficients[n:]
        self.n_observations_ = n
        return self

    def predict(self, coordinates):
        if self._centres is None:
            raise RuntimeError("fit must be called before predict")
        x = _coordinates(coordinates, "coordinates")
        return _kernel(x, self._centres) @ self._radial + _polynomial(x) @ self._linear

    def fit_predict(self, coordinates, values):
        return self.fit(coordinates, values).predict(coordinates)

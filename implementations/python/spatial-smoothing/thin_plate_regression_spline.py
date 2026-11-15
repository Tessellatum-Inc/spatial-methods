"""Low-rank 2-D thin-plate regression spline basis (Wood-style TPRS)."""
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


def _polynomial(coords, centre):
    shifted = coords - centre
    return np.column_stack((np.ones(coords.shape[0]), shifted[:, 0], shifted[:, 1]))


class ThinPlateRegressionSpline2D:
    """Rank-truncated 2-D thin-plate spline with an affine null space.

    k is the number of penalized radial basis functions; the full model
    therefore has k + 3 coefficients. The basis is obtained by projecting the
    full-knot thin-plate kernel into the orthogonal complement of {1, x, y},
    eigendecomposing that projected kernel, and retaining its k largest
    eigen-directions. The transformed basis has an identity wiggliness penalty.

    This is a transparent dense eigendecomposition, not mgcv's Lanczos/
    subsampled large-data constructor. Coordinates must be projected planar
    coordinates in a consistent linear unit.
    """
    def __init__(self, k=10, smoothing=1.0):
        if isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) or k < 1:
            raise ValueError("k must be a positive integer radial basis rank")
        if not np.isfinite(smoothing) or smoothing < 0:
            raise ValueError("smoothing must be finite and nonnegative")
        self.k = int(k)
        self.smoothing = float(smoothing)
        self._centres = None
        self._centre = None
        self._radial_coefficients = None
        self._linear = None

    def fit(self, coordinates, values):
        x = _coordinates(coordinates, "coordinates")
        y = np.asarray(values, dtype=float)
        if y.ndim != 1 or y.size != x.shape[0] or not np.all(np.isfinite(y)):
            raise ValueError("values must be a finite vector matching coordinates")
        n = x.shape[0]
        if n < 4 or np.linalg.matrix_rank(np.column_stack((np.ones(n), x))) < 3:
            raise ValueError("at least four locations spanning a non-collinear 2-D design are required")
        if np.unique(x, axis=0).shape[0] != n:
            raise ValueError("duplicate coordinate locations are not supported")
        if self.k > n - 3:
            raise ValueError("k cannot exceed n_observations - 3")

        centre = np.mean(x, axis=0)
        p = _polynomial(x, centre)
        q, _ = np.linalg.qr(p, mode="complete")
        q2 = q[:, 3:]
        kernel = _kernel(x, x)
        projected = q2.T @ kernel @ q2
        eigenvalues, eigenvectors = np.linalg.eigh(projected)
        tolerance = (np.finfo(float).eps
                     * max(1.0, float(np.max(np.abs(eigenvalues))))
                     * n * 100.0)
        if np.any(eigenvalues <= tolerance):
            raise ValueError("projected thin-plate kernel is numerically rank deficient")

        order = np.argsort(eigenvalues)[::-1][:self.k]
        selected_values = eigenvalues[order]
        selected_vectors = eigenvectors[:, order]
        radial_map = (q2 @ selected_vectors) / np.sqrt(selected_values)[None, :]
        basis = kernel @ radial_map
        design = np.column_stack((basis, p))

        if self.smoothing > 0:
            penalty = np.zeros((self.k, self.k + 3))
            penalty[:, :self.k] = np.sqrt(self.smoothing) * np.eye(self.k)
            augmented_design = np.vstack((design, penalty))
            augmented_values = np.concatenate((y, np.zeros(self.k)))
        else:
            augmented_design = design
            augmented_values = y

        coefficients, _, rank, _ = np.linalg.lstsq(
            augmented_design, augmented_values, rcond=None
        )
        if rank < self.k + 3:
            raise ValueError("reduced spline design is rank deficient")

        self._centres = x.copy()
        self._centre = centre
        self._radial_coefficients = radial_map @ coefficients[:self.k]
        self._linear = coefficients[self.k:]
        self.n_observations_ = n
        self.basis_rank_ = self.k
        self.basis_dimension_ = self.k + 3
        self.penalty_rank_ = self.k
        return self

    def predict(self, coordinates):
        if self._centres is None:
            raise RuntimeError("fit must be called before predict")
        x = _coordinates(coordinates, "coordinates")
        return (_kernel(x, self._centres) @ self._radial_coefficients
                + _polynomial(x, self._centre) @ self._linear)

    def fit_predict(self, coordinates, values):
        return self.fit(coordinates, values).predict(coordinates)

"""Small 2D radial-basis-function interpolation reference implementation."""
from __future__ import annotations

import math
import numpy as np


_SUPPORTED = {"thin_plate", "cubic", "gaussian"}


def _finite_scalar(value, *, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (int, float, np.integer, np.floating)
    ):
        raise ValueError(f"{name} must be a finite numeric scalar")
    try:
        result = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite numeric scalar") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite numeric scalar")
    return result


def _finite_array(values, *, name, ndim):
    try:
        array = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric values") from exc
    if array.ndim != ndim or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be a finite {ndim}-dimensional array")
    return array


def _kernel(distance, name, epsilon):
    if name == "thin_plate":
        squared = distance * distance
        result = np.zeros_like(distance)
        positive = distance > 0
        result[positive] = squared[positive] * np.log(distance[positive])
        return result
    if name == "cubic":
        return distance ** 3
    return np.exp(-((epsilon * distance) ** 2))


def _polynomial(points):
    return np.column_stack((np.ones(len(points)), points[:, 0], points[:, 1]))


def _distances(left, right):
    delta = left[:, None, :] - right[None, :, :]
    return np.sqrt(np.sum(delta * delta, axis=2))


class RBFInterpolator2D:
    """Fit a global 2D RBF interpolant with an affine polynomial tail.

    Coordinates are centered and scaled internally. The model supports
    thin-plate, cubic and Gaussian kernels, non-negative diagonal smoothing,
    and multiple output columns. It is a dense O(n^3) fitting baseline.
    """

    def __init__(self, points, values, *, kernel="thin_plate",
                 epsilon=1.0, smoothing=0.0):
        samples = _finite_array(points, name="points", ndim=2)
        observations = _finite_array(values, name="values", ndim=1)
        if samples.shape[1] != 2:
            raise ValueError("points must have shape (n, 2)")
        if len(samples) < 3 or len(observations) != len(samples):
            raise ValueError("at least three points and one value per point are required")
        if not isinstance(kernel, str) or kernel not in _SUPPORTED:
            raise ValueError(f"kernel must be one of {sorted(_SUPPORTED)}")
        epsilon = _finite_scalar(epsilon, name="epsilon")
        smoothing = _finite_scalar(smoothing, name="smoothing")
        if epsilon <= 0:
            raise ValueError("epsilon must be finite and positive")
        if smoothing < 0:
            raise ValueError("smoothing must be finite and non-negative")

        self.center_ = samples.mean(axis=0)
        self.scale_ = samples.std(axis=0)
        if np.any(self.scale_ == 0):
            raise ValueError("sample coordinates must vary along both axes")
        self.points_ = (samples - self.center_) / self.scale_
        if len(np.unique(self.points_, axis=0)) != len(self.points_):
            raise ValueError("duplicate sample coordinates are not supported")
        self.values_ = observations.copy()
        self.kernel_ = kernel
        self.epsilon_ = float(epsilon)
        self.smoothing_ = float(smoothing)

        polynomial = _polynomial(self.points_)
        if np.linalg.matrix_rank(polynomial) < polynomial.shape[1]:
            raise ValueError("sample points must support a full-rank affine polynomial tail")
        distances = _distances(self.points_, self.points_)
        radial = _kernel(distances, kernel, self.epsilon_)
        radial.flat[::len(radial) + 1] += self.smoothing_
        system = np.block([
            [radial, polynomial],
            [polynomial.T, np.zeros((polynomial.shape[1], polynomial.shape[1]))],
        ])
        rhs = np.concatenate((self.values_, np.zeros(polynomial.shape[1])))
        try:
            solution = np.linalg.solve(system, rhs)
        except np.linalg.LinAlgError as exc:
            raise ValueError("RBF system is singular; check sample geometry and smoothing") from exc
        if not np.all(np.isfinite(solution)):
            raise ValueError("RBF solve produced non-finite coefficients")
        self.weights_ = solution[:len(samples)]
        self.polynomial_coefficients_ = solution[len(samples):]

    def predict(self, queries):
        """Predict at query coordinates shaped (m, 2); returns a 1D array."""
        targets = _finite_array(queries, name="queries", ndim=2)
        if targets.shape[1] != 2:
            raise ValueError("queries must have shape (m, 2)")
        if len(targets) == 0:
            return np.empty(0, dtype=float)
        normalized = (targets - self.center_) / self.scale_
        radial = _kernel(_distances(normalized, self.points_), self.kernel_, self.epsilon_)
        result = radial @ self.weights_ + _polynomial(normalized) @ self.polynomial_coefficients_
        if not np.all(np.isfinite(result)):
            raise ValueError("RBF prediction produced non-finite values")
        return result


def rbf_interpolate(points, values, queries, *, kernel="thin_plate",
                    epsilon=1.0, smoothing=0.0):
    """Fit an RBF interpolant and return predictions for query points."""
    model = RBFInterpolator2D(
        points, values, kernel=kernel, epsilon=epsilon, smoothing=smoothing
    )
    return model.predict(queries)


def select_rbf_smoothing(
    points, values, candidates, *, kernel="thin_plate", epsilon=1.0
):
    """Select positive diagonal smoothing by exact leave-one-out PRESS.

    The diagonal of the augmented RBF linear smoother is obtained by solving
    against the identity matrix. PRESS residuals are e_i/(1-H_ii), avoiding
    n separate refits. Candidates are evaluated in the same normalized
    coordinate system used by RBFInterpolator2D.
    """
    samples = _finite_array(points, name="points", ndim=2)
    observations = _finite_array(values, name="values", ndim=1)
    choices = _finite_array(candidates, name="candidates", ndim=1)
    if choices.size == 0 or np.any(choices <= 0):
        raise ValueError("candidates must be a non-empty array of positive smoothing values")
    if len(np.unique(choices)) != len(choices):
        raise ValueError("smoothing candidates must be unique")
    epsilon = _finite_scalar(epsilon, name="epsilon")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    scores = {}
    for smoothing in choices:
        model = RBFInterpolator2D(
            samples, observations, kernel=kernel, epsilon=epsilon,
            smoothing=float(smoothing)
        )
        n = len(samples)
        polynomial = _polynomial(model.points_)
        kernel_matrix = _kernel(
            _distances(model.points_, model.points_), model.kernel_, model.epsilon_
        )
        system_radial = kernel_matrix.copy()
        system_radial.flat[::n + 1] += model.smoothing_
        system = np.block([
            [system_radial, polynomial],
            [polynomial.T, np.zeros((polynomial.shape[1], polynomial.shape[1]))],
        ])
        rhs = np.vstack([np.eye(n), np.zeros((polynomial.shape[1], n))])
        try:
            influence_solution = np.linalg.solve(system, rhs)
        except np.linalg.LinAlgError as exc:
            raise ValueError("RBF smoother system is singular during PRESS evaluation") from exc
        smoother = kernel_matrix @ influence_solution[:n] + polynomial @ influence_solution[n:]
        denominator = 1.0 - np.diag(smoother)
        if np.any(np.abs(denominator) < 1e-10):
            score = float("inf")
        else:
            residual = observations - smoother @ observations
            loo_residual = residual / denominator
            score = float(np.mean(loo_residual ** 2))
        scores[float(smoothing)] = score
    finite = [(score, smoothing) for smoothing, score in scores.items()
              if math.isfinite(score)]
    if not finite:
        raise ValueError("all smoothing candidates produced undefined PRESS scores")
    best_score, best_smoothing = min(finite)
    return {
        "smoothing": best_smoothing,
        "press_score": best_score,
        "scores": scores,
        "kernel": kernel,
        "epsilon": epsilon,
        "method": "exact leave-one-out PRESS",
    }

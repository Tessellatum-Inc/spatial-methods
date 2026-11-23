"""Principal-axis exploratory factor analysis with optional varimax rotation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import numpy as np
from numpy.typing import ArrayLike, NDArray

@dataclass(frozen=True)
class FactorAnalysisResult:
    means: NDArray[np.float64]
    scales: NDArray[np.float64]
    correlation: NDArray[np.float64]
    loadings: NDArray[np.float64]
    communalities: NDArray[np.float64]
    uniquenesses: NDArray[np.float64]
    initial_eigenvalues: NDArray[np.float64]
    rotation_matrix: NDArray[np.float64]
    iterations: int
    converged: bool
    rotation_iterations: int
    rotation_converged: bool
    heywood_clipped: bool

def _varimax(loadings: NDArray[np.float64], *, max_iter: int, tolerance: float):
    p, k = loadings.shape
    rotation = np.eye(k, dtype=float)
    previous = 0.0
    for iteration in range(1, max_iter + 1):
        rotated = loadings @ rotation
        target = loadings.T @ (rotated**3 - (1.0/p)*rotated @ np.diag(np.diag(rotated.T @ rotated)))
        left, singular_values, right_t = np.linalg.svd(target, full_matrices=False)
        rotation = left @ right_t
        objective = float(np.sum(singular_values))
        if iteration > 1 and objective-previous <= tolerance*max(1.0, previous):
            return loadings @ rotation, rotation, iteration, True
        previous = objective
    return loadings @ rotation, rotation, max_iter, False

def principal_axis_factor_analysis(data: ArrayLike, n_factors: int, *,
        rotation: Literal["none", "varimax"] = "varimax",
        max_iter: int = 500, tolerance: float = 1e-6) -> FactorAnalysisResult:
    """Fit principal-axis factors to the sample correlation matrix.

    Variables are standardized. Initial communalities are squared multiple
    correlations from the Moore-Penrose inverse. Communalities are iteratively
    replaced by sums of squared retained loadings and clipped to [0, 1].
    This is exploratory principal-axis factoring, not maximum-likelihood FA.
    """
    values = np.asarray(data, dtype=float)
    if values.ndim != 2 or values.shape[0] < 3 or values.shape[1] < 2:
        raise ValueError("data must be 2D with at least 3 rows and 2 columns")
    if not np.all(np.isfinite(values)):
        raise ValueError("data must contain only finite values")
    if not isinstance(n_factors, (int, np.integer)) or isinstance(n_factors, (bool, np.bool_)):
        raise ValueError("n_factors must be an integer")
    if not 1 <= int(n_factors) < values.shape[1]:
        raise ValueError("n_factors must be between 1 and number of variables - 1")
    if not isinstance(max_iter, (int, np.integer)) or isinstance(max_iter, (bool, np.bool_)) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if rotation not in ("none", "varimax"):
        raise ValueError("rotation must be 'none' or 'varimax'")
    means = np.mean(values, axis=0)
    scales = np.std(values, axis=0, ddof=1)
    if not np.all(np.isfinite(means)) or not np.all(np.isfinite(scales)):
        raise ValueError("data magnitude is too large for stable standardization")
    if np.any(scales <= 0):
        raise ValueError("every variable must have positive sample variance")
    z = (values-means)/scales
    correlation = z.T @ z / (values.shape[0]-1)
    correlation = (correlation+correlation.T)/2
    if not np.all(np.isfinite(correlation)):
        raise ValueError("correlation matrix is not finite")
    inv_diag = np.diag(np.linalg.pinv(correlation))
    if np.any(inv_diag <= 0) or not np.all(np.isfinite(inv_diag)):
        raise ValueError("could not initialise communalities")
    raw = 1-1/inv_diag
    communalities = np.clip(raw, 0, 1)
    clipped = bool(np.any(np.abs(raw-communalities)>1e-12))
    converged = False
    extracted = np.zeros((values.shape[1], int(n_factors)))
    eigenvalues = np.zeros(int(n_factors))
    for iteration in range(1, int(max_iter)+1):
        reduced = correlation.copy()
        np.fill_diagonal(reduced, communalities)
        vals, vecs = np.linalg.eigh(reduced)
        order = np.argsort(vals)[::-1][:int(n_factors)]
        eigenvalues = vals[order]
        extracted = vecs[:, order]*np.sqrt(np.maximum(eigenvalues, 0))
        raw = np.sum(extracted**2, axis=1)
        updated = np.clip(raw, 0, 1)
        clipped = clipped or bool(np.any(np.abs(raw-updated)>1e-12))
        difference = float(np.max(np.abs(updated-communalities)))
        communalities = updated
        if difference <= tolerance:
            converged = True
            break
    if rotation == "varimax":
        loadings, transform, rot_iter, rot_converged = _varimax(
            extracted, max_iter=int(max_iter), tolerance=float(tolerance))
    else:
        loadings, transform, rot_iter, rot_converged = extracted.copy(), np.eye(int(n_factors)), 0, True
    final_h2 = np.clip(np.sum(loadings**2, axis=1), 0, 1)
    return FactorAnalysisResult(means, scales, correlation, loadings, final_h2,
        1-final_h2, eigenvalues.copy(), transform, iteration, converged,
        rot_iter, rot_converged, clipped)

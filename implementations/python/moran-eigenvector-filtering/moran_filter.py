"""Moran eigenvectors and fixed-size OLS spatial filtering."""
from __future__ import annotations
import numpy as np


def _weights_matrix(weights, *, tolerance=1e-10):
    w = np.asarray(weights, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1] or w.shape[0] < 2:
        raise ValueError("weights must be a square matrix with at least two rows")
    if not np.all(np.isfinite(w)) or np.any(w < 0):
        raise ValueError("weights must be finite and nonnegative")
    if not np.allclose(w, w.T, atol=tolerance, rtol=0):
        raise ValueError("weights must be symmetric; row-standardized asymmetric matrices are not accepted")
    if np.any(np.abs(np.diag(w)) > tolerance):
        raise ValueError("weights diagonal must be zero")
    if not np.any(w > 0):
        raise ValueError("weights must contain at least one positive link")
    return w


def moran_eigenvectors(weights, n_components=None, *, positive_only=True,
                       eigenvalue_tolerance=1e-10):
    """Return eigenvectors of H W H sorted by descending eigenvalue.

    H = I - 11'/n removes the intercept. By default only positive eigenvalues
    above the tolerance are eligible for a positive-autocorrelation filter.
    """
    w = _weights_matrix(weights)
    if not isinstance(positive_only, bool):
        raise ValueError("positive_only must be boolean")
    if isinstance(eigenvalue_tolerance, bool):
        raise ValueError("eigenvalue_tolerance must be finite and nonnegative")
    try:
        tol = float(eigenvalue_tolerance)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid eigenvalue_tolerance") from exc
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("eigenvalue_tolerance must be finite and nonnegative")

    n = w.shape[0]
    h = np.eye(n) - np.ones((n, n)) / n
    centered = h @ w @ h
    eigenvalues, eigenvectors = np.linalg.eigh(centered)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    mask = eigenvalues > tol if positive_only else np.abs(eigenvalues) > tol
    eigenvalues, eigenvectors = eigenvalues[mask], eigenvectors[:, mask]

    if n_components is not None:
        if isinstance(n_components, bool) or not isinstance(n_components, (int, np.integer)) or n_components < 0:
            raise ValueError("n_components must be a nonnegative integer or None")
        if n_components > len(eigenvalues):
            raise ValueError("n_components exceeds the available eligible eigenvectors")
        eigenvalues = eigenvalues[:n_components]
        eigenvectors = eigenvectors[:, :n_components]
    return {
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "centered_weights": centered,
    }


def moran_eigenvector_filter(y, X, weights, *, n_components, add_intercept=True):
    """Fit OLS with a caller-selected number of leading Moran eigenvectors.

    This is a transparent fixed-size filtering baseline, not an automatic
    eigenvector-selection procedure. X may be None, a vector or a matrix.
    """
    y = np.asarray(y, dtype=float)
    if y.ndim != 1 or y.size < 2 or not np.all(np.isfinite(y)):
        raise ValueError("y must be a finite vector with at least two observations")
    w = _weights_matrix(weights)
    if len(y) != w.shape[0]:
        raise ValueError("y length must match weights matrix")
    if X is None:
        x = np.empty((len(y), 0), dtype=float)
    else:
        x = np.asarray(X, dtype=float)
        if x.ndim == 1:
            x = x[:, None]
        if x.ndim != 2 or x.shape[0] != len(y) or not np.all(np.isfinite(x)):
            raise ValueError("X must be a finite vector or matrix with matching rows")
    if not isinstance(add_intercept, bool):
        raise ValueError("add_intercept must be boolean")

    basis = moran_eigenvectors(w, n_components=n_components, positive_only=True)
    e = basis["eigenvectors"]
    parts = []
    if add_intercept:
        parts.append(np.ones((len(y), 1)))
    if x.shape[1]:
        parts.append(x)
    if e.shape[1]:
        parts.append(e)
    design = np.column_stack(parts) if parts else np.empty((len(y), 0))
    if design.shape[1] == 0:
        raise ValueError("model requires an intercept, covariates or eigenvectors")

    coefficients, _, rank, singular_values = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ coefficients
    residuals = y - fitted
    offset = 1 if add_intercept else 0
    beta = coefficients[offset:offset + x.shape[1]]
    gamma = coefficients[offset + x.shape[1]:]
    return {
        "intercept": float(coefficients[0]) if add_intercept else None,
        "coefficients": beta,
        "eigenvector_coefficients": gamma,
        "eigenvalues": basis["eigenvalues"],
        "eigenvectors": e,
        "fitted": fitted,
        "residuals": residuals,
        "design_rank": int(rank),
        "singular_values": singular_values,
        "residual_sum_squares": float(residuals @ residuals),
    }

"""Aitchison compositional geometry and log-ratio transforms."""
from __future__ import annotations

import numpy as np


def _as_matrix(values, name="composition"):
    x = np.asarray(values, dtype=float)
    if x.ndim not in (1, 2) or x.shape[-1] < 2 or x.size == 0:
        raise ValueError(
            f"{name} must be a vector or a non-empty matrix with at least two parts"
        )
    single = x.ndim == 1
    matrix = x[None, :] if single else x
    if not np.all(np.isfinite(matrix)) or np.any(matrix < 0):
        raise ValueError(f"{name} must contain finite nonnegative parts")
    totals = matrix.sum(axis=1, keepdims=True)
    if np.any(~np.isfinite(totals)) or np.any(totals <= 0):
        raise ValueError(f"each {name} must have positive finite total")
    return matrix, single


def closure(values):
    """Close one or more nonnegative compositions to unit sum."""
    matrix, single = _as_matrix(values)
    result = matrix / matrix.sum(axis=1, keepdims=True)
    return result[0] if single else result


def _positive_compositions(values, name="composition"):
    matrix, single = _as_matrix(values, name)
    matrix = matrix / matrix.sum(axis=1, keepdims=True)
    if np.any(matrix <= 0):
        raise ValueError(
            f"{name} must be strictly positive for log-ratio transforms; "
            "apply a justified zero-replacement model first"
        )
    return matrix, single


def clr(values):
    """Centered log-ratio transform; output parts sum to zero."""
    matrix, single = _positive_compositions(values)
    logs = np.log(matrix)
    result = logs - logs.mean(axis=1, keepdims=True)
    return result[0] if single else result


def helmert_basis(n_parts):
    """Return a D-by-(D-1) orthonormal Helmert contrast basis."""
    if (
        isinstance(n_parts, (bool, np.bool_))
        or not isinstance(n_parts, (int, np.integer))
        or n_parts < 2
    ):
        raise ValueError("n_parts must be an integer >= 2")
    basis = np.zeros((n_parts, n_parts - 1), dtype=float)
    for j in range(1, n_parts):
        scale = np.sqrt(j * (j + 1.0))
        basis[:j, j - 1] = 1.0 / scale
        basis[j, j - 1] = -j / scale
    return basis


def ilr(values):
    """Isometric log-ratio coordinates in a fixed Helmert basis."""
    matrix, single = _positive_compositions(values)
    basis = helmert_basis(matrix.shape[1])
    result = np.log(matrix) @ basis
    return result[0] if single else result


def ilr_inverse(coordinates):
    """Map ILR coordinates back to unit-sum positive compositions."""
    z = np.asarray(coordinates, dtype=float)
    if (
        z.ndim not in (1, 2) or z.shape[-1] < 1 or z.size == 0
        or not np.all(np.isfinite(z))
    ):
        raise ValueError("ILR coordinates must be a finite vector or non-empty matrix")
    single = z.ndim == 1
    matrix = z[None, :] if single else z
    basis = helmert_basis(matrix.shape[1] + 1)
    logs = matrix @ basis.T
    logs = logs - np.max(logs, axis=1, keepdims=True)
    exp = np.exp(logs)
    result = exp / exp.sum(axis=1, keepdims=True)
    return result[0] if single else result


def alr(values, denominator=-1):
    """Additive log-ratio transform relative to one selected part."""
    matrix, single = _positive_compositions(values)
    n_parts = matrix.shape[1]
    if (
        isinstance(denominator, (bool, np.bool_))
        or not isinstance(denominator, (int, np.integer))
        or not -n_parts <= denominator < n_parts
    ):
        raise ValueError("denominator must be an in-range integer part index")
    denominator %= n_parts
    numerators = [i for i in range(n_parts) if i != denominator]
    result = np.log(matrix[:, numerators] / matrix[:, [denominator]])
    return result[0] if single else result


def alr_inverse(coordinates, denominator=-1):
    """Invert ALR coordinates using the same denominator-part convention."""
    z = np.asarray(coordinates, dtype=float)
    if (
        z.ndim not in (1, 2) or z.shape[-1] < 1 or z.size == 0
        or not np.all(np.isfinite(z))
    ):
        raise ValueError("ALR coordinates must be a finite vector or non-empty matrix")
    single = z.ndim == 1
    matrix = z[None, :] if single else z
    n_parts = matrix.shape[1] + 1
    if (
        isinstance(denominator, (bool, np.bool_))
        or not isinstance(denominator, (int, np.integer))
        or not -n_parts <= denominator < n_parts
    ):
        raise ValueError("denominator index is out of range")
    denominator %= n_parts
    logs = np.zeros((matrix.shape[0], n_parts), dtype=float)
    numerators = [i for i in range(n_parts) if i != denominator]
    logs[:, numerators] = matrix
    logs -= np.max(logs, axis=1, keepdims=True)
    exp = np.exp(logs)
    result = exp / exp.sum(axis=1, keepdims=True)
    return result[0] if single else result


def aitchison_distance(first, second):
    """Euclidean distance between compositions in ILR coordinates."""
    a, _ = _positive_compositions(first, "first composition")
    b, _ = _positive_compositions(second, "second composition")
    if a.shape != b.shape:
        raise ValueError("compositions must have matching shapes")
    result = np.linalg.norm(ilr(a) - ilr(b), axis=1)
    return float(result[0]) if result.size == 1 else result

"""Iteratively reweighted multivariate alteration detection (IR-MAD)."""
from __future__ import annotations

import numpy as np
from scipy.special import gammaincc


def _as_image(image, name):
    x = np.asarray(image, dtype=float)
    if x.ndim not in (2, 3) or min(x.shape) < 1 or not np.all(np.isfinite(x)):
        raise ValueError(f"{name} must be finite non-empty (rows, cols[, bands]) data")
    was_2d = x.ndim == 2
    return (x[..., None] if was_2d else x), was_2d


def _mask(mask, shape):
    if mask is None:
        return np.ones(shape, dtype=bool)
    result = np.asarray(mask)
    if result.shape != shape or result.dtype.kind != "b":
        raise ValueError("valid_mask must be boolean and match the spatial image shape")
    if not np.any(result):
        raise ValueError("valid_mask must select at least one pixel")
    return result.copy()


def _weighted_mean_cov(x, weights, ridge):
    total = float(weights.sum())
    mean = np.sum(x * weights[:, None], axis=0) / total
    centered = x - mean
    covariance = (centered * weights[:, None]).T @ centered / total
    scale = max(float(np.trace(covariance)) / max(1, covariance.shape[0]), 1.0)
    covariance = covariance + np.eye(covariance.shape[0]) * ridge * scale
    return mean, covariance


def _inverse_sqrt(matrix):
    values, vectors = np.linalg.eigh(matrix)
    floor = max(float(values.max()), 1.0) * np.finfo(float).eps * matrix.shape[0]
    return (vectors * (1.0 / np.sqrt(np.maximum(values, floor)))) @ vectors.T


def ir_mad(reference, target, *, valid_mask=None, max_iterations=50,
           tolerance=1e-6, ridge=1e-8, min_weight=1e-8):
    """Compare two co-registered images using iteratively reweighted MAD.

    Each date may have a different number of bands. Weighted canonical
    correlation analysis produces paired canonical variates; their differences
    are MAD variates. A chi-square tail probability becomes the next pixel
    weight, progressively emphasizing observations consistent with no change.

    Returns a dictionary containing MAD variates, chi-square scores, weights,
    canonical correlations, and convergence diagnostics. The spatial arrays
    retain the input row/column shape. Inputs must be finite; use valid_mask to
    exclude clouds, shadows, borders or other unusable pixels.
    """
    ref, ref_2d = _as_image(reference, "reference")
    tgt, tgt_2d = _as_image(target, "target")
    if ref.shape[:2] != tgt.shape[:2]:
        raise ValueError("reference and target must share spatial dimensions")
    if ref_2d != tgt_2d:
        raise ValueError("reference and target must both be 2D or both be 3D")
    if not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be positive and finite")
    if not np.isfinite(ridge) or ridge <= 0:
        raise ValueError("ridge must be positive and finite")
    if not np.isfinite(min_weight) or not 0 < min_weight <= 1:
        raise ValueError("min_weight must lie in (0, 1]")
    valid = _mask(valid_mask, ref.shape[:2])
    x = ref.reshape(-1, ref.shape[-1])[valid.ravel()]
    y = tgt.reshape(-1, tgt.shape[-1])[valid.ravel()]
    components = min(x.shape[1], y.shape[1])
    if x.shape[0] <= max(x.shape[1], y.shape[1], 2):
        raise ValueError("too few valid pixels for the requested band dimensions")

    weights = np.ones(x.shape[0], dtype=float)
    converged = False
    correlations = np.empty(components)
    for iteration in range(1, max_iterations + 1):
        mean_x, cov_x = _weighted_mean_cov(x, weights, ridge)
        mean_y, cov_y = _weighted_mean_cov(y, weights, ridge)
        centered_x, centered_y = x - mean_x, y - mean_y
        total = weights.sum()
        cross = (centered_x * weights[:, None]).T @ centered_y / total
        white_x, white_y = _inverse_sqrt(cov_x), _inverse_sqrt(cov_y)
        left, singular, right_t = np.linalg.svd(white_x @ cross @ white_y, full_matrices=False)
        correlations = np.clip(singular[:components], 0.0, 1.0)
        coeff_x = white_x @ left[:, :components]
        coeff_y = white_y @ right_t.T[:, :components]
        mad = centered_x @ coeff_x - centered_y @ coeff_y
        variance = np.maximum(2.0 * (1.0 - correlations), ridge)
        chi_square = np.sum((mad * mad) / variance[None, :], axis=1)
        updated = np.clip(gammaincc(components / 2.0, chi_square / 2.0),
                          min_weight, 1.0)
        change = float(np.max(np.abs(updated - weights)))
        weights = updated
        if change <= tolerance:
            converged = True
            break

    # Refit once using the final posterior-like no-change weights.
    mean_x, cov_x = _weighted_mean_cov(x, weights, ridge)
    mean_y, cov_y = _weighted_mean_cov(y, weights, ridge)
    centered_x, centered_y = x - mean_x, y - mean_y
    cross = (centered_x * weights[:, None]).T @ centered_y / weights.sum()
    white_x, white_y = _inverse_sqrt(cov_x), _inverse_sqrt(cov_y)
    left, singular, right_t = np.linalg.svd(white_x @ cross @ white_y, full_matrices=False)
    correlations = np.clip(singular[:components], 0.0, 1.0)
    coeff_x = white_x @ left[:, :components]
    coeff_y = white_y @ right_t.T[:, :components]
    mad = centered_x @ coeff_x - centered_y @ coeff_y
    variance = np.maximum(2.0 * (1.0 - correlations), ridge)
    chi_square = np.sum((mad * mad) / variance[None, :], axis=1)

    spatial_shape = ref.shape[:2]
    mad_image = np.full((ref.shape[0] * ref.shape[1], components), np.nan)
    chi_image = np.full(ref.shape[:2], np.nan)
    weight_image = np.full(ref.shape[:2], np.nan)
    mad_image[valid.ravel()] = mad
    chi_image.ravel()[valid.ravel()] = chi_square
    weight_image.ravel()[valid.ravel()] = weights
    return {
        "mad_variates": mad_image.reshape(*spatial_shape, components),
        "chi_square": chi_image,
        "weights": weight_image,
        "canonical_correlations": correlations,
        "reference_coefficients": coeff_x,
        "target_coefficients": coeff_y,
        "reference_mean": mean_x,
        "target_mean": mean_y,
        "iterations": iteration,
        "converged": converged,
    }

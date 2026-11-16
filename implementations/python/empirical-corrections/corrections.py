"""Empirical dark-object and terrain-illumination corrections."""
from __future__ import annotations
import numpy as np


def _image(image):
    x = np.asarray(image, dtype=float)
    if x.ndim not in (2, 3) or min(x.shape) < 1 or not np.all(np.isfinite(x)):
        raise ValueError("image must be finite non-empty (rows, cols[, bands]) data")
    return x[..., None] if x.ndim == 2 else x, x.ndim == 2


def _valid_mask(mask, shape):
    if mask is None:
        return np.ones(shape, dtype=bool)
    m = np.asarray(mask)
    if m.shape != shape or m.dtype.kind != "b":
        raise ValueError("valid_mask must be boolean and match the spatial image shape")
    return m.copy()


def dark_object_subtraction(image, *, valid_mask=None, dark_percentile=1.0, clip_negative=True):
    """Subtract a per-band low-percentile path-radiance estimate.

    This is a simple empirical haze-reduction baseline, not a physical
    atmospheric radiative-transfer model. The percentile is estimated only
    from valid pixels and subtracted from every pixel in that band.
    """
    x, was_2d = _image(image)
    if not np.isfinite(dark_percentile) or not 0 <= dark_percentile <= 50:
        raise ValueError("dark_percentile must be between 0 and 50")
    if not isinstance(clip_negative, (bool, np.bool_)):
        raise ValueError("clip_negative must be boolean")
    valid = _valid_mask(valid_mask, x.shape[:2])
    if not np.any(valid):
        raise ValueError("valid_mask must select at least one pixel")
    path = np.percentile(x[valid], dark_percentile, axis=0)
    corrected = x - path.reshape(1, 1, -1)
    if clip_negative:
        corrected = np.maximum(corrected, 0.0)
    return {
        "corrected": corrected[..., 0] if was_2d else corrected,
        "path_radiance": path[0] if was_2d else path,
        "dark_percentile": float(dark_percentile),
    }


def c_correction(reflectance, cos_incidence, cos_zenith, *, valid_mask=None, epsilon=1e-8):
    """Apply per-band C-correction using OLS reflectance~cos(i).

    C is intercept/slope. The input reflectance and illumination cosines must
    be co-registered; pixels with invalid or near-zero illumination are
    excluded from coefficient fitting and returned as NaN.
    """
    x, was_2d = _image(reflectance)
    shape = x.shape[:2]
    ci, cz = np.asarray(cos_incidence, float), np.asarray(cos_zenith, float)
    if ci.shape != shape or cz.shape != shape or not np.all(np.isfinite(ci)) or not np.all(np.isfinite(cz)):
        raise ValueError("cos_incidence and cos_zenith must be finite spatial arrays")
    if np.any((ci < 0) | (ci > 1) | (cz < 0) | (cz > 1)):
        raise ValueError("illumination cosines must lie in [0, 1]")
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be positive and finite")
    valid = _valid_mask(valid_mask, shape) & (ci > epsilon)
    if valid.sum() < 2:
        raise ValueError("at least two valid illuminated pixels are required")
    corrected = np.full_like(x, np.nan)
    constants = np.empty(x.shape[-1], dtype=float)
    for band in range(x.shape[-1]):
        y = x[..., band][valid]
        slope, intercept = np.polyfit(ci[valid], y, 1)
        if not np.isfinite(slope) or abs(slope) <= epsilon:
            raise ValueError("C-correction regression slope is zero or unstable")
        c = intercept / slope
        if not np.isfinite(c) or c < 0:
            raise ValueError("estimated C must be finite and non-negative")
        constants[band] = c
        denominator = ci + c
        usable = valid & (denominator > epsilon)
        corrected[..., band][usable] = x[..., band][usable] * (cz + c)[usable] / denominator[usable]
    return {"corrected": corrected[..., 0] if was_2d else corrected,
            "c_parameters": constants[0] if was_2d else constants}


def minnaert_correction(reflectance, cos_incidence, cos_zenith, k, *, valid_mask=None, epsilon=1e-8):
    """Apply Minnaert terrain correction with caller-supplied exponent k.

    k may be scalar or one value per spectral band. Non-positive illumination
    and invalid-mask cells are returned as NaN.
    """
    x, was_2d = _image(reflectance)
    shape = x.shape[:2]
    ci, cz = np.asarray(cos_incidence, float), np.asarray(cos_zenith, float)
    if ci.shape != shape or cz.shape != shape or not np.all(np.isfinite(ci)) or not np.all(np.isfinite(cz)):
        raise ValueError("cos_incidence and cos_zenith must be finite spatial arrays")
    if np.any((ci < 0) | (ci > 1) | (cz < 0) | (cz > 1)):
        raise ValueError("illumination cosines must lie in [0, 1]")
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be positive and finite")
    exponents = np.asarray(k, dtype=float)
    if exponents.ndim == 0:
        exponents = np.full(x.shape[-1], float(exponents))
    if exponents.shape != (x.shape[-1],) or not np.all(np.isfinite(exponents)):
        raise ValueError("k must be finite scalar or one value per band")
    valid = _valid_mask(valid_mask, shape) & (ci > epsilon)
    ratio = np.divide(cz, ci, out=np.full_like(ci, np.nan), where=ci > epsilon)
    corrected = np.full_like(x, np.nan)
    for band, exponent in enumerate(exponents):
        corrected[..., band][valid] = x[..., band][valid] * ratio[valid] ** exponent
    return {"corrected": corrected[..., 0] if was_2d else corrected,
            "k": exponents[0] if was_2d else exponents.copy()}

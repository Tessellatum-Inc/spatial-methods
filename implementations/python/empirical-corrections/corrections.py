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


def histogram_match(source, reference, *, valid_mask=None, quantiles=1024):
    """Match each source band to a reference band's empirical distribution.

    Both inputs are matching (rows, cols[, bands]) arrays. The piecewise
    linear map is built from corresponding empirical quantiles. This is a
    univariate distribution match, not physical calibration; it can erase
    genuine distributional change and does not correct spatially varying
    illumination or sensor response.
    """
    src, was_2d = _image(source)
    ref, ref_2d = _image(reference)
    if src.shape != ref.shape or was_2d != ref_2d:
        raise ValueError("source and reference must have matching shapes and dimensionality")
    if not isinstance(quantiles, (int, np.integer)) or quantiles < 2:
        raise ValueError("quantiles must be an integer of at least 2")
    valid = _valid_mask(valid_mask, src.shape[:2])
    if valid.sum() < 2:
        raise ValueError("valid_mask must select at least two pixels")
    probabilities = np.linspace(0.0, 1.0, quantiles)
    matched = np.empty_like(src)
    for band in range(src.shape[-1]):
        source_values = src[..., band][valid]
        reference_values = ref[..., band][valid]
        source_q = np.quantile(source_values, probabilities)
        reference_q = np.quantile(reference_values, probabilities)
        # Collapse repeated source quantiles before interpolation; this also
        # handles constant-valued source bands without divide-by-zero.
        unique_source, first = np.unique(source_q, return_index=True)
        mapped_reference = reference_q[first]
        if unique_source.size == 1:
            matched[..., band] = reference_q[0]
        else:
            matched[..., band] = np.interp(src[..., band], unique_source, mapped_reference)
    return {"matched": matched[..., 0] if was_2d else matched,
            "quantile_probabilities": probabilities}


def pseudo_invariant_feature_normalization(reference, target, *, valid_mask=None,
                                           stable_fraction=0.5, ridge=1e-10):
    """Linearly normalize target bands to reference using automatically selected PIFs.

    A conservative baseline selects the lowest-change fraction of valid
    pixels using a robustly scaled multiband difference score, then fits
    reference_band = gain * target_band + offset on those pseudo-invariant
    candidates. This is not IR-MAD: it does not estimate canonical variates,
    iteratively reweight change probabilities, or model sensor noise.
    """
    ref, was_2d = _image(reference)
    tgt, tgt_2d = _image(target)
    if ref.shape != tgt.shape or was_2d != tgt_2d:
        raise ValueError("reference and target must have matching shapes and dimensionality")
    if not np.isfinite(stable_fraction) or not 0 < stable_fraction <= 1:
        raise ValueError("stable_fraction must be in (0, 1]")
    if not np.isfinite(ridge) or ridge <= 0:
        raise ValueError("ridge must be finite and positive")
    valid = _valid_mask(valid_mask, ref.shape[:2])
    indices = np.flatnonzero(valid)
    minimum = max(3, ref.shape[-1] + 1)
    count = max(minimum, int(np.ceil(stable_fraction * indices.size)))
    if count > indices.size:
        raise ValueError("at least max(3, bands + 1) valid pixels are required")
    difference = ref - tgt
    samples = difference.reshape(-1, ref.shape[-1])[indices]
    median = np.median(samples, axis=0)
    mad = 1.4826 * np.median(np.abs(samples - median), axis=0)
    scale = np.where(mad > ridge, mad, 1.0)
    scores = np.linalg.norm((samples - median) / scale, axis=1)
    chosen_local = np.argsort(scores, kind="stable")[:count]
    stable_flat = indices[chosen_local]
    stable = np.zeros(ref.shape[:2], dtype=bool)
    stable.flat[stable_flat] = True

    ref_samples = ref.reshape(-1, ref.shape[-1])[stable_flat]
    tgt_samples = tgt.reshape(-1, tgt.shape[-1])[stable_flat]
    gains = np.empty(ref.shape[-1])
    offsets = np.empty(ref.shape[-1])
    corrected = np.empty_like(tgt)
    for band in range(ref.shape[-1]):
        x = tgt_samples[:, band]
        y = ref_samples[:, band]
        centered = x - x.mean()
        denominator = float(centered @ centered)
        if denominator <= ridge:
            raise ValueError("selected PIF target values have insufficient variance")
        gain = float(centered @ (y - y.mean()) / denominator)
        offset = float(y.mean() - gain * x.mean())
        if not np.isfinite(gain) or not np.isfinite(offset):
            raise ValueError("PIF regression produced non-finite coefficients")
        gains[band], offsets[band] = gain, offset
        corrected[..., band] = gain * tgt[..., band] + offset
    return {"normalized": corrected[..., 0] if was_2d else corrected,
            "stable_mask": stable, "gain": gains[0] if was_2d else gains,
            "offset": offsets[0] if was_2d else offsets}



def fit_empirical_line(digital_numbers, reference_reflectance):
    """Fit per-band empirical-line DN-to-reflectance calibration.

    Inputs are paired ROI/sample means shaped (samples, bands), or 1D
    single-band vectors. Ordinary least squares fits reflectance = gain*DN
    + offset independently per band. At least two distinct DN values are
    required in every band. The caller is responsible for panel/target
    selection, co-registration, and reference reflectance provenance.
    """
    dn = np.asarray(digital_numbers, dtype=float)
    rho = np.asarray(reference_reflectance, dtype=float)
    if dn.ndim == 1:
        dn = dn[:, None]
    if rho.ndim == 1:
        rho = rho[:, None]
    if dn.ndim != 2 or rho.shape != dn.shape or dn.shape[0] < 2 or dn.shape[1] < 1:
        raise ValueError("inputs must be matching (samples, bands) arrays with at least two samples")
    if not np.all(np.isfinite(dn)) or not np.all(np.isfinite(rho)):
        raise ValueError("calibration samples must be finite")
    gains = np.empty(dn.shape[1])
    offsets = np.empty(dn.shape[1])
    r_squared = np.empty(dn.shape[1])
    rmse = np.empty(dn.shape[1])
    for band in range(dn.shape[1]):
        x, y = dn[:, band], rho[:, band]
        centered = x - x.mean()
        denominator = float(centered @ centered)
        if denominator <= np.finfo(float).eps * max(1.0, float(x @ x)):
            raise ValueError("each band requires at least two distinct DN values")
        gain = float(centered @ (y - y.mean()) / denominator)
        offset = float(y.mean() - gain * x.mean())
        residual = y - (gain * x + offset)
        total = float(np.sum((y - y.mean()) ** 2))
        gains[band], offsets[band] = gain, offset
        rmse[band] = float(np.sqrt(np.mean(residual ** 2)))
        r_squared[band] = 1.0 if total <= np.finfo(float).eps else 1.0 - float(residual @ residual) / total
    return {"gain": gains, "offset": offsets, "r_squared": r_squared, "rmse": rmse}


def apply_empirical_line(image, calibration, *, clip=None):
    """Apply a fitted empirical-line calibration to a 2D or multiband image.

    A 2D image uses a one-band calibration; a (rows, cols, bands) image
    requires matching coefficient vectors. Reflectance is not clipped unless
    an explicit (minimum, maximum) pair is supplied.
    """
    x, was_2d = _image(image)
    gain = np.asarray(calibration.get("gain"), dtype=float)
    offset = np.asarray(calibration.get("offset"), dtype=float)
    if gain.ndim != 1 or offset.shape != gain.shape or gain.size != x.shape[-1]:
        raise ValueError("calibration gain and offset must match the image band count")
    if not np.all(np.isfinite(gain)) or not np.all(np.isfinite(offset)):
        raise ValueError("calibration coefficients must be finite")
    result = x * gain.reshape(1, 1, -1) + offset.reshape(1, 1, -1)
    if clip is not None:
        bounds = np.asarray(clip, dtype=float)
        if bounds.shape != (2,) or not np.all(np.isfinite(bounds)) or bounds[0] > bounds[1]:
            raise ValueError("clip must be a finite (minimum, maximum) pair")
        result = np.clip(result, bounds[0], bounds[1])
    return result[..., 0] if was_2d else result

"""Reference methods for spectral analysis of gridded and multivariate fields."""
from __future__ import annotations

import math
import numpy as np


def _finite_matrix(values, name, *, min_rows=1, min_cols=1):
    try:
        result = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric values") from exc
    if result.ndim != 2 or result.shape[0] < min_rows or result.shape[1] < min_cols:
        raise ValueError(f"{name} must be a 2D array with at least {min_rows} rows and {min_cols} columns")
    if not np.isfinite(result).all():
        raise ValueError(f"{name} must contain only finite values")
    return result


def _mode_count(value, maximum, name="n_modes"):
    if value is None:
        return maximum
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be an integer or None")
    if not 1 <= value <= maximum:
        raise ValueError(f"{name} must be between 1 and {maximum}")
    return int(value)


def _positive_scalar(value, name, *, allow_zero=False):
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be finite and {'non-negative' if allow_zero else 'positive'}")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be finite and numeric") from exc
    if not math.isfinite(result) or result < 0 or (result == 0 and not allow_zero):
        raise ValueError(f"{name} must be finite and {'non-negative' if allow_zero else 'positive'}")
    return result


def periodogram_2d(field, *, spacing=(1.0, 1.0), window="hann"):
    """Return shifted 2-D Fourier frequencies and a normalised power periodogram.

    The input is a regularly sampled, finite planar grid. The field mean is
    removed. Window may be 'hann' (separable taper) or 'none'. Power is
    |FFT|² divided by the sum of squared window weights.
    """
    data = _finite_matrix(field, "field", min_rows=2, min_cols=2)
    try:
        step = np.asarray(spacing, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("spacing must contain two positive finite values") from exc
    if step.shape != (2,) or not np.isfinite(step).all() or np.any(step <= 0):
        raise ValueError("spacing must contain two positive finite values")
    if window == "hann":
        wy = np.hanning(data.shape[0])
        wx = np.hanning(data.shape[1])
        weights = wy[:, None] * wx[None, :]
        if not np.any(weights):
            weights = np.ones_like(data)
    elif window == "none":
        weights = np.ones_like(data)
    else:
        raise ValueError("window must be 'hann' or 'none'")
    anomalies = data - data.mean()
    norm = float(np.sum(weights * weights))
    spectrum = np.fft.fftshift(np.fft.fft2(anomalies * weights))
    power = np.abs(spectrum) ** 2 / norm
    fy = np.fft.fftshift(np.fft.fftfreq(data.shape[0], d=step[0]))
    fx = np.fft.fftshift(np.fft.fftfreq(data.shape[1], d=step[1]))
    return {"frequency_y": fy, "frequency_x": fx, "power": power}


def eof_analysis(field, *, n_modes=None, standardize=False):
    """Compute empirical orthogonal functions (EOFs) from time-by-space data.

    Columns are spatial cells/features and rows are time samples. Each column
    is centred over time. EOF signs are mathematically arbitrary.
    """
    data = _finite_matrix(field, "field", min_rows=2, min_cols=1)
    if not isinstance(standardize, (bool, np.bool_)):
        raise ValueError("standardize must be boolean")
    mean = data.mean(axis=0)
    anomalies = data - mean
    scale = np.ones(data.shape[1])
    if standardize:
        scale = anomalies.std(axis=0, ddof=1)
        if np.any(scale <= 0):
            raise ValueError("standardization requires non-constant spatial features")
        anomalies = anomalies / scale
    u, singular, vt = np.linalg.svd(anomalies, full_matrices=False)
    if not singular.size or singular[0] <= 0:
        raise ValueError("field has zero temporal variance")
    count = _mode_count(n_modes, len(singular))
    total = float(np.sum(singular * singular))
    return {
        "mean": mean,
        "scale": scale,
        "eofs": vt[:count].T,
        "pcs": u[:, :count] * singular[:count],
        "eigenvalues": singular[:count] ** 2 / (data.shape[0] - 1),
        "variance_fraction": singular[:count] ** 2 / total,
        "singular_values": singular[:count],
    }


def _diagonal_average(matrix):
    rows, cols = matrix.shape
    result = np.zeros(rows + cols - 1, dtype=float)
    counts = np.zeros(rows + cols - 1, dtype=float)
    for i in range(rows):
        for j in range(cols):
            result[i + j] += matrix[i, j]
            counts[i + j] += 1
    return result / counts


def ssa_decompose(series, *, window_length, n_components=None):
    """Perform univariate singular-spectrum analysis (SSA).

    Returns rank-one reconstructed components obtained by diagonal averaging
    of the trajectory matrix. Summing all returned components reconstructs
    the input up to floating-point precision.
    """
    try:
        values = np.asarray(series, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("series must contain finite numeric values") from exc
    if values.ndim != 1 or len(values) < 3 or not np.isfinite(values).all():
        raise ValueError("series must be a finite 1D array of length at least 3")
    if isinstance(window_length, (bool, np.bool_)) or not isinstance(window_length, (int, np.integer)):
        raise ValueError("window_length must be an integer")
    if not 2 <= window_length < len(values):
        raise ValueError("window_length must be between 2 and series length minus one")
    trajectory = np.column_stack([
        values[index:index + window_length]
        for index in range(len(values) - window_length + 1)
    ])
    u, singular, vt = np.linalg.svd(trajectory, full_matrices=False)
    count = _mode_count(n_components, len(singular), name="n_components")
    components = np.vstack([
        _diagonal_average(singular[index] * np.outer(u[:, index], vt[index]))
        for index in range(count)
    ])
    return {
        "components": components,
        "reconstruction": components.sum(axis=0),
        "singular_values": singular[:count],
        "trajectory_matrix": trajectory,
    }


def maximum_covariance_analysis(left, right, *, n_modes=None):
    """SVD of the cross-covariance between two time-aligned multivariate fields."""
    x = _finite_matrix(left, "left", min_rows=2)
    y = _finite_matrix(right, "right", min_rows=2)
    if x.shape[0] != y.shape[0]:
        raise ValueError("left and right fields must have the same time dimension")
    xc = x - x.mean(axis=0)
    yc = y - y.mean(axis=0)
    cross = xc.T @ yc / (len(x) - 1)
    u, singular, vt = np.linalg.svd(cross, full_matrices=False)
    count = _mode_count(n_modes, len(singular))
    total = float(np.sum(singular * singular))
    fractions = singular[:count] ** 2 / total if total > 0 else np.zeros(count)
    return {
        "left_patterns": u[:, :count],
        "right_patterns": vt[:count].T,
        "left_coefficients": xc @ u[:, :count],
        "right_coefficients": yc @ vt[:count].T,
        "singular_values": singular[:count],
        "covariance_fraction": fractions,
        "cross_covariance": cross,
    }


def _inverse_sqrt(matrix, name):
    values, vectors = np.linalg.eigh((matrix + matrix.T) * 0.5)
    if np.any(values <= 0):
        raise ValueError(f"{name} is not positive definite; use positive ridge regularisation")
    return (vectors / np.sqrt(values)) @ vectors.T


def canonical_correlation_analysis(left, right, *, n_modes=None, ridge=1e-8):
    """Regularised linear canonical correlation analysis for aligned samples."""
    x = _finite_matrix(left, "left", min_rows=3)
    y = _finite_matrix(right, "right", min_rows=3)
    if x.shape[0] != y.shape[0]:
        raise ValueError("left and right fields must have the same sample count")
    penalty = _positive_scalar(ridge, "ridge", allow_zero=True)
    xc = x - x.mean(axis=0)
    yc = y - y.mean(axis=0)
    denominator = len(x) - 1
    sxx = xc.T @ xc / denominator + penalty * np.eye(x.shape[1])
    syy = yc.T @ yc / denominator + penalty * np.eye(y.shape[1])
    sxy = xc.T @ yc / denominator
    wx = _inverse_sqrt(sxx, "left covariance")
    wy = _inverse_sqrt(syy, "right covariance")
    u, correlations, vt = np.linalg.svd(wx @ sxy @ wy, full_matrices=False)
    count = _mode_count(n_modes, len(correlations))
    left_weights = wx @ u[:, :count]
    right_weights = wy @ vt[:count].T
    return {
        "canonical_correlations": correlations[:count],
        "left_weights": left_weights,
        "right_weights": right_weights,
        "left_variates": xc @ left_weights,
        "right_variates": yc @ right_weights,
    }


def welch_coherence(left, right, *, sampling_frequency=1.0,
                    segment_length=None, overlap=None):
    """Estimate magnitude-squared cross-spectral coherence by Welch averaging."""
    try:
        x = np.asarray(left, dtype=float)
        y = np.asarray(right, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("signals must be finite numeric vectors") from exc
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) < 4:
        raise ValueError("signals must be equal-length 1D arrays of length at least 4")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("signals must be finite")
    fs = _positive_scalar(sampling_frequency, "sampling_frequency")
    length = min(256, len(x)) if segment_length is None else segment_length
    if isinstance(length, (bool, np.bool_)) or not isinstance(length, (int, np.integer)):
        raise ValueError("segment_length must be an integer")
    if not 2 <= length <= len(x):
        raise ValueError("segment_length must be between 2 and signal length")
    step_overlap = length // 2 if overlap is None else overlap
    if isinstance(step_overlap, (bool, np.bool_)) or not isinstance(step_overlap, (int, np.integer)):
        raise ValueError("overlap must be an integer")
    if not 0 <= step_overlap < length:
        raise ValueError("overlap must be in [0, segment_length)")
    window = np.hanning(length)
    if not np.any(window):
        window = np.ones(length)
    spectra_x, spectra_y, spectra_xy = [], [], []
    step = length - step_overlap
    for start in range(0, len(x) - length + 1, step):
        sx = (x[start:start + length] - np.mean(x[start:start + length])) * window
        sy = (y[start:start + length] - np.mean(y[start:start + length])) * window
        fx = np.fft.rfft(sx)
        fy = np.fft.rfft(sy)
        spectra_x.append(np.abs(fx) ** 2)
        spectra_y.append(np.abs(fy) ** 2)
        spectra_xy.append(fx * np.conjugate(fy))
    pxx = np.mean(spectra_x, axis=0)
    pyy = np.mean(spectra_y, axis=0)
    pxy = np.mean(spectra_xy, axis=0)
    denominator = pxx * pyy
    coherence = np.divide(
        np.abs(pxy) ** 2, denominator,
        out=np.zeros_like(denominator, dtype=float),
        where=denominator > 0,
    )
    coherence = np.clip(coherence, 0.0, 1.0)
    frequency = np.fft.rfftfreq(length, d=1.0 / fs)
    return {"frequency": frequency, "coherence": coherence}

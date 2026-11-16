"""Radial amplitude spectra and bounded single-layer depth fitting."""
from __future__ import annotations

import numpy as np


def radial_average_amplitude(grid, dx, dy, *, n_bins=40, min_count=3):
    """Return annular mean Fourier amplitude for a finite regular 2D grid.

    Wavenumbers are angular (radians per coordinate unit). The DC term is
    excluded. Bins are equal-width in radial wavenumber; empty/sparsely
    populated bins are omitted. This is a descriptive spectrum, not a
    statistically independent sample of Fourier coefficients.
    """
    data = np.asarray(grid, dtype=float)
    if data.ndim != 2 or min(data.shape) < 4 or not np.all(np.isfinite(data)):
        raise ValueError("grid must be a finite 2D array with each dimension >= 4")
    dx, dy = float(dx), float(dy)
    if not np.isfinite(dx) or not np.isfinite(dy) or dx <= 0 or dy <= 0:
        raise ValueError("dx and dy must be finite and positive")
    if isinstance(n_bins, bool) or not isinstance(n_bins, (int, np.integer)) or n_bins < 4:
        raise ValueError("n_bins must be an integer >= 4")
    if isinstance(min_count, bool) or not isinstance(min_count, (int, np.integer)) or min_count < 1:
        raise ValueError("min_count must be a positive integer")

    ky = 2 * np.pi * np.fft.fftfreq(data.shape[0], d=dy)
    kx = 2 * np.pi * np.fft.fftfreq(data.shape[1], d=dx)
    radial_k = np.sqrt(ky[:, None] ** 2 + kx[None, :] ** 2)
    amplitude = np.abs(np.fft.fft2(data))
    positive = radial_k > 0
    k = radial_k[positive]
    a = amplitude[positive]
    edges = np.linspace(0.0, float(k.max()) * (1.0 + 1e-12), int(n_bins) + 1)
    index = np.digitize(k, edges) - 1
    centers, means, counts = [], [], []
    for j in range(n_bins):
        selected = index == j
        count = int(np.count_nonzero(selected))
        if count >= min_count:
            centers.append(float(np.mean(k[selected])))
            means.append(float(np.mean(a[selected])))
            counts.append(count)
    return {
        "wavenumber": np.asarray(centers),
        "amplitude": np.asarray(means),
        "count": np.asarray(counts, dtype=int),
        "bin_edges": edges,
    }


def fit_single_layer_spectrum(wavenumber, amplitude, *, exponents=(-1, 0, 1),
                              min_bins=6, min_wavenumber=None,
                              max_wavenumber=None):
    """Fit log(A)=log(B)+n*log(k)-z*k for one equivalent source layer.

    The exponent n is selected from the caller's discrete candidate set and
    depth z is constrained to be non-negative. This is a single-segment,
    single-layer diagnostic fit; it does not estimate multiple spectral
    segments or solve the nonlinear multi-layer Phillips model.
    """
    k = np.asarray(wavenumber, dtype=float)
    a = np.asarray(amplitude, dtype=float)
    if k.ndim != 1 or a.ndim != 1 or k.size != a.size:
        raise ValueError("wavenumber and amplitude must be equal-length 1D arrays")
    if not np.all(np.isfinite(k)) or not np.all(np.isfinite(a)):
        raise ValueError("spectrum values must be finite")
    if np.any(k <= 0) or np.any(a <= 0):
        raise ValueError("wavenumbers and amplitudes must be positive")
    if isinstance(min_bins, bool) or not isinstance(min_bins, (int, np.integer)) or min_bins < 3:
        raise ValueError("min_bins must be an integer >= 3")
    candidates = tuple(exponents)
    if not candidates or any(isinstance(n, bool) or n not in (-1, 0, 1) for n in candidates):
        raise ValueError("exponents must be a non-empty subset of {-1, 0, 1}")
    use = np.ones(k.size, dtype=bool)
    if min_wavenumber is not None:
        if not np.isfinite(min_wavenumber) or min_wavenumber <= 0:
            raise ValueError("min_wavenumber must be finite and positive")
        use &= k >= min_wavenumber
    if max_wavenumber is not None:
        if not np.isfinite(max_wavenumber) or max_wavenumber <= 0:
            raise ValueError("max_wavenumber must be finite and positive")
        use &= k <= max_wavenumber
    k, a = k[use], a[use]
    if k.size < min_bins:
        raise ValueError("not enough positive spectrum bins in the selected range")

    log_a = np.log(a)
    fits = []
    for n in candidates:
        adjusted = log_a - int(n) * np.log(k)
        design = np.column_stack([np.ones(k.size), -k])
        intercept, depth = np.linalg.lstsq(design, adjusted, rcond=None)[0]
        if depth < 0:
            depth = 0.0
            intercept = float(np.mean(adjusted))
        predicted = intercept - depth * k
        residual = adjusted - predicted
        sse = float(np.dot(residual, residual))
        fits.append((sse, int(n), float(intercept), float(depth), residual))
    sse, n, intercept, depth, residual = min(fits, key=lambda item: item[0])
    centered = log_a - np.mean(log_a)
    total = float(np.dot(centered, centered))
    r_squared = 1.0 - sse / total if total > 0 else (1.0 if sse == 0 else 0.0)
    return {
        "B": float(np.exp(intercept)),
        "z": depth,
        "n": n,
        "rmse_log": float(np.sqrt(sse / k.size)),
        "r_squared_log": float(r_squared),
        "n_bins": int(k.size),
        "wavenumber": k,
        "observed_amplitude": a,
        "fitted_amplitude": np.exp(intercept + n * np.log(k) - depth * k),
    }

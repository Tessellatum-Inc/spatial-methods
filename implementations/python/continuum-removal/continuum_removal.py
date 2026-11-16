"""Convex-hull continuum removal for reflectance spectra."""
from __future__ import annotations
import numpy as np


def _upper_hull(x, y):
    hull = []
    for i in range(len(x)):
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            cross = (x[b] - x[a]) * (y[i] - y[b]) - (y[b] - y[a]) * (x[i] - x[b])
            if cross >= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    if len(hull) < 2:
        raise ValueError("at least two distinct wavelengths are required")
    return np.asarray(hull, dtype=int)


def continuum_removal(reflectance, wavelengths):
    """Divide each spectrum by its piecewise-linear upper convex-hull continuum.

    The last axis of reflectance is spectral band; all preceding dimensions
    are treated as independent spectra. Wavelengths must be strictly
    increasing. Returns continuum, continuum-removed reflectance, absorption
    depth (1 - ratio), and wavelength-integrated absorption area.
    """
    spectra = np.asarray(reflectance, dtype=float)
    wave = np.asarray(wavelengths, dtype=float)
    if spectra.ndim < 1 or spectra.shape[-1] < 2 or not np.all(np.isfinite(spectra)):
        raise ValueError("reflectance must be finite with at least two spectral bands")
    if np.any(spectra < 0):
        raise ValueError("reflectance must be non-negative")
    if wave.ndim != 1 or wave.size != spectra.shape[-1] or not np.all(np.isfinite(wave)):
        raise ValueError("wavelengths must be a finite 1-D array matching the spectral axis")
    if np.any(np.diff(wave) <= 0):
        raise ValueError("wavelengths must be strictly increasing")
    flat = spectra.reshape(-1, spectra.shape[-1])
    continuum = np.empty_like(flat)
    for row, spectrum in enumerate(flat):
        hull = _upper_hull(wave, spectrum)
        continuum[row] = np.interp(wave, wave[hull], spectrum[hull])
    if np.any(continuum <= 0):
        raise ValueError("upper-hull continuum must be positive at every wavelength")
    ratio = flat / continuum
    depth = 1.0 - ratio
    area = np.trapz(depth, wave, axis=1)
    output_shape = spectra.shape
    return {
        "continuum": continuum.reshape(output_shape),
        "continuum_removed": ratio.reshape(output_shape),
        "absorption_depth": depth.reshape(output_shape),
        "absorption_area": area.reshape(spectra.shape[:-1]),
    }

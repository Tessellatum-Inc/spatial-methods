"""Robust Gaussian sensor-noise estimation from Haar HH coefficients.

This is a scoped first-order estimator for approximately i.i.d. additive
Gaussian noise, not a general sensor noise model.
"""
from __future__ import annotations

import numpy as np

_GAUSSIAN_MAD = 0.6744897501960817


def haar_diagonal_detail(image: np.ndarray) -> np.ndarray:
    """Return orthonormal 2x2 Haar diagonal-detail coefficients.

    Odd final rows/columns are dropped (not padded) so every coefficient uses
    four observed pixels with equal weights and no synthetic edge samples.
    """
    a = np.asarray(image, dtype=float)
    if a.ndim != 2 or min(a.shape) < 2 or not np.all(np.isfinite(a)):
        raise ValueError("image must be a finite 2-D array at least 2x2")
    a = a[: a.shape[0] // 2 * 2, : a.shape[1] // 2 * 2]
    p00 = a[0::2, 0::2]
    p01 = a[0::2, 1::2]
    p10 = a[1::2, 0::2]
    p11 = a[1::2, 1::2]
    return (p00 - p01 - p10 + p11) / 2.0


def estimate_gaussian_noise(image: np.ndarray) -> float:
    """Estimate additive white Gaussian noise sigma using HH-detail MAD.

    sigma_hat = median(abs(HH - median(HH))) / 0.67448975.
    The estimate assumes locally smooth signal is sparse in the finest-scale
    diagonal-detail band and noise is approximately independent Gaussian.
    Strong texture, fine edges, correlated noise, striping, quantisation and
    signal-dependent noise can bias the estimate.
    """
    hh = haar_diagonal_detail(image)
    centre = np.median(hh)
    return float(np.median(np.abs(hh - centre)) / _GAUSSIAN_MAD)


def estimate_band_noise(image: np.ndarray) -> np.ndarray:
    """Estimate sigma independently for each band of an HxWxB array."""
    a = np.asarray(image, dtype=float)
    if a.ndim != 3 or min(a.shape[:2]) < 2 or a.shape[2] < 1 or not np.all(np.isfinite(a)):
        raise ValueError("image must be a finite HxWxB array with H,W >= 2 and B >= 1")
    return np.asarray([estimate_gaussian_noise(a[:, :, band]) for band in range(a.shape[2])])

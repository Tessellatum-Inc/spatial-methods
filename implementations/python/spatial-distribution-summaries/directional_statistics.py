"""Circular and directional statistics for planar bearings (radians)."""
from __future__ import annotations

from math import exp, isfinite, pi, sqrt
from typing import Sequence

import numpy as np


def _angles(values: Sequence[float]) -> np.ndarray:
    angles = np.asarray(values, dtype=float)
    if angles.ndim != 1 or angles.size == 0 or not np.isfinite(angles).all():
        raise ValueError("angles must be a non-empty finite one-dimensional sequence")
    return np.mod(angles, 2.0 * pi)


def circular_summary(angles: Sequence[float]) -> dict:
    """Return circular mean direction, mean resultant length and resultant.

    Angles are radians counterclockwise from the positive x-axis. When the
    resultant is numerically zero, mean_direction is NaN because no unique
    direction is defined.
    """
    values = _angles(angles)
    c = float(np.mean(np.cos(values)))
    s = float(np.mean(np.sin(values)))
    r = min(1.0, sqrt(c * c + s * s))
    mean = float(np.mod(np.arctan2(s, c), 2.0 * pi)) if r > 1e-14 else float("nan")
    return {
        "mean_direction": mean,
        "mean_resultant_length": r,
        "mean_cosine": c,
        "mean_sine": s,
        "resultant_length": r * len(values),
        "n": int(len(values)),
    }


def rayleigh_test(angles: Sequence[float]) -> dict:
    """Rayleigh test of circular uniformity against unimodal concentration.

    Uses the common finite-sample approximation to the null tail probability.
    The test is most sensitive to unimodal departures; it can have low power
    against symmetric multimodal alternatives.
    """
    values = _angles(angles)
    n = len(values)
    summary = circular_summary(values)
    r = summary["resultant_length"]
    z = r * r / n
    if n < 3:
        raise ValueError("Rayleigh approximation requires at least three angles")
    p = exp(sqrt(max(0.0, 1.0 + 4.0*n + 4.0*(n*n-r*r))) - (1.0 + 2.0*n))
    if n < 50:
        p *= 1.0 + (2.0*z-z*z)/(4.0*n) - (
            24.0*z - 132.0*z*z + 76.0*z**3 - 9.0*z**4
        )/(288.0*n*n)
    return {
        "statistic_z": float(z),
        "pvalue": float(min(1.0, max(0.0, p))),
        "mean_direction": summary["mean_direction"],
        "mean_resultant_length": summary["mean_resultant_length"],
        "n": n,
        "alternative": "non-uniform unimodal concentration",
    }


def kuiper_uniformity_test(angles: Sequence[float]) -> dict:
    """Kuiper's rotation-invariant one-sample test against circular uniformity.

    Reports V = D+ + D- and a Stephens-corrected asymptotic p-value. The
    approximation is intended for continuous angular observations; ties
    should be interpreted cautiously. Angles are normalized to [0, 2*pi).
    """
    values = np.sort(_angles(angles) / (2.0 * pi))
    n = len(values)
    if n < 2:
        raise ValueError("Kuiper test requires at least two angles")
    i = np.arange(1, n + 1, dtype=float)
    d_plus = float(np.max(i / n - values))
    d_minus = float(np.max(values - (i - 1.0) / n))
    v = d_plus + d_minus
    lam = (sqrt(n) + 0.155 + 0.24 / sqrt(n)) * v
    # Q_K(lambda) = 2 sum (4j^2 lambda^2 - 1) exp(-2j^2 lambda^2).
    p = 0.0
    for j in range(1, 1000):
        term = 2.0 * (4.0*j*j*lam*lam - 1.0) * exp(-2.0*j*j*lam*lam)
        p += term
        if abs(term) < 1e-14:
            break
    return {
        "statistic_v": v,
        "d_plus": d_plus,
        "d_minus": d_minus,
        "pvalue": float(min(1.0, max(0.0, p))),
        "n": n,
        "alternative": "any departure from circular uniformity",
    }


def von_mises_density(angles: Sequence[float], *, mean_direction: float = 0.0,
                      concentration: float = 1.0) -> np.ndarray:
    """Evaluate the von Mises circular density at angles (radians).

    Uses the normalized density exp(kappa*cos(theta-mu))/(2*pi*I0(kappa)).
    """
    values = _angles(angles)
    try:
        mu, kappa = float(mean_direction), float(concentration)
    except (TypeError, ValueError):
        raise ValueError("mean_direction and concentration must be finite; concentration >= 0") from None
    if not isfinite(mu) or not isfinite(kappa) or kappa < 0:
        raise ValueError("mean_direction must be finite and concentration nonnegative")
    # numpy.i0 is stable for the moderate concentrations this direct density
    # evaluator is intended to teach; very large kappa may overflow.
    normalizer = 2.0 * pi * float(np.i0(kappa))
    if not isfinite(normalizer):
        raise ValueError("concentration is too large for direct normalization")
    return np.exp(kappa * np.cos(values - mu)) / normalizer


def rose_histogram(angles: Sequence[float], *, bins: int = 16,
                   weights: Sequence[float] | None = None) -> dict:
    """Return weighted circular histogram counts and equally spaced edges."""
    values = _angles(angles)
    if isinstance(bins, (bool, np.bool_)) or not isinstance(bins, (int, np.integer)) or bins < 1:
        raise ValueError("bins must be a positive integer")
    if weights is None:
        w = np.ones(len(values), dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != values.shape or not np.isfinite(w).all() or (w < 0).any():
            raise ValueError("weights must be finite, nonnegative and match angles")
    counts, edges = np.histogram(values, bins=int(bins), range=(0.0, 2.0*pi), weights=w)
    return {"counts": counts, "edges": edges, "total_weight": float(w.sum())}

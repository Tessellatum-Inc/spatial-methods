"""Annual-maximum flood frequency analysis using L-moments."""
from __future__ import annotations
import math
import numpy as np


def weibull_return_periods(annual_maxima):
    """Return sorted annual maxima and Weibull plotting-position return periods."""
    x = np.asarray(annual_maxima, dtype=float)
    if x.ndim != 1 or x.size < 2 or np.any(~np.isfinite(x)):
        raise ValueError("annual_maxima must contain at least two finite values")
    ordered = np.sort(x)[::-1]
    ranks = np.arange(1, x.size + 1, dtype=float)
    return {"magnitude": ordered, "rank": ranks, "exceedance_probability": ranks / (x.size + 1.0),
            "return_period": (x.size + 1.0) / ranks}


def _sample_l_moments(values):
    x = np.sort(np.asarray(values, dtype=float))
    n = x.size
    b = []
    for r in range(3):
        weights = np.array([
            math.comb(i, r) / math.comb(n - 1, r) if i >= r else 0.0
            for i in range(n)
        ])
        b.append(float(np.dot(weights, x) / n))
    l1 = b[0]
    l2 = 2.0 * b[1] - b[0]
    l3 = 6.0 * b[2] - 6.0 * b[1] + b[0]
    return l1, l2, l3


def fit_gumbel_lmoments(annual_maxima):
    """Fit Gumbel location/scale by sample L-moments."""
    x = np.asarray(annual_maxima, dtype=float)
    if x.ndim != 1 or x.size < 3 or np.any(~np.isfinite(x)):
        raise ValueError("annual_maxima must contain at least three finite values")
    l1, l2, _ = _sample_l_moments(x)
    if l2 <= 0:
        raise ValueError("annual_maxima must have positive sample L-scale")
    scale = l2 / math.log(2.0)
    location = l1 - 0.5772156649015329 * scale
    return {"location": location, "scale": scale, "distribution": "gumbel"}


def gumbel_return_level(return_period, *, location, scale):
    """Return Gumbel non-exceedance quantile for T-year return period."""
    t = np.asarray(return_period, dtype=float)
    mu, beta = float(location), float(scale)
    if np.any(~np.isfinite(t)) or np.any(t <= 1):
        raise ValueError("return_period must be finite and greater than one year")
    if not math.isfinite(mu) or not math.isfinite(beta) or beta <= 0:
        raise ValueError("location must be finite and scale finite and positive")
    p = 1.0 - 1.0 / t
    return mu - beta * np.log(-np.log(p))


def fit_gev_lmoments(annual_maxima):
    """Fit GEV parameters (location, scale, shape) by sample L-moments.

    Shape follows the common GEV convention F(x)=exp(-(1-k*(x-mu)/sigma)**(1/k));
    k=0 is the Gumbel limit. The polynomial shape approximation is intended
    for ordinary hydrologic samples, not extreme-tail extrapolation audits.
    """
    x = np.asarray(annual_maxima, dtype=float)
    if x.ndim != 1 or x.size < 4 or np.any(~np.isfinite(x)):
        raise ValueError("annual_maxima must contain at least four finite values")
    l1, l2, l3 = _sample_l_moments(x)
    if l2 <= 0:
        raise ValueError("annual_maxima must have positive sample L-scale")
    tau3 = l3 / l2
    if not -0.99 < tau3 < 0.99:
        raise ValueError("sample L-skewness is outside the supported range")
    k = (0.28377530 + tau3 * (-1.21096399 + tau3 * (-2.50728214 - 1.13455566 * tau3)))
    if abs(k) < 1e-6:
        scale = l2 / math.log(2.0)
        location = l1 - 0.5772156649015329 * scale
        k = 0.0
    else:
        gamma = math.gamma(1.0 + k)
        scale = l2 * k / ((1.0 - 2.0 ** (-k)) * gamma)
        location = l1 - scale * (1.0 - gamma) / k
    if not math.isfinite(scale) or scale <= 0 or not math.isfinite(location):
        raise ValueError("sample does not yield valid GEV parameters")
    return {"location": location, "scale": scale, "shape": k, "distribution": "gev"}


def gev_return_level(return_period, *, location, scale, shape):
    """Return GEV non-exceedance quantile for T-year return period."""
    t = np.asarray(return_period, dtype=float)
    mu, sigma, k = float(location), float(scale), float(shape)
    if np.any(~np.isfinite(t)) or np.any(t <= 1):
        raise ValueError("return_period must be finite and greater than one year")
    if not math.isfinite(mu) or not math.isfinite(sigma) or sigma <= 0 or not math.isfinite(k):
        raise ValueError("location/shape must be finite and scale positive")
    p = 1.0 - 1.0 / t
    y = -np.log(p)
    if abs(k) < 1e-8:
        return mu - sigma * np.log(y)
    return mu + (sigma / k) * (1.0 - y ** k)


def flood_frequency_table(annual_maxima, return_periods=(2, 5, 10, 25, 50, 100), *, distribution="gev"):
    """Fit selected frequency model and return requested design-flood quantiles."""
    periods = np.asarray(return_periods, dtype=float)
    if periods.ndim != 1 or periods.size == 0 or np.any(~np.isfinite(periods)) or np.any(periods <= 1):
        raise ValueError("return_periods must be a non-empty 1D array greater than one")
    if distribution == "gev":
        params = fit_gev_lmoments(annual_maxima)
        levels = gev_return_level(periods, **{k: params[k] for k in ("location", "scale", "shape")})
    elif distribution == "gumbel":
        params = fit_gumbel_lmoments(annual_maxima)
        levels = gumbel_return_level(periods, **{k: params[k] for k in ("location", "scale")})
    else:
        raise ValueError("distribution must be 'gev' or 'gumbel'")
    return {"return_period": periods, "quantile": np.asarray(levels), "parameters": params}

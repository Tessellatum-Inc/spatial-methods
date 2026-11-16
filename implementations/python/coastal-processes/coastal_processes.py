"""Empirical coastal-process reference calculations with explicit assumptions."""
from __future__ import annotations
import numpy as np

_G = 9.80665


def _finite_positive(name, value):
    try:
        out = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be finite and positive") from None
    if not np.isfinite(out) or out <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return out


def stockdon_runup(h0, period, beach_slope, *, percentile=2, gravity=_G):
    """Stockdon et al. (2006) empirical vertical runup statistic (metres).

    Inputs are deep-water significant wave height H0 (m), peak period T (s),
    and dimensionless foreshore slope beta_f. Returns R2, R1, Rmean or Rlow
    for percentile=2, 1, 50 or 0 respectively. This parameterization is not
    a site-calibrated inundation model and excludes tide/surge setup.
    """
    h = np.asarray(h0, dtype=float)
    t = np.asarray(period, dtype=float)
    b = np.asarray(beach_slope, dtype=float)
    try:
        h, t, b = np.broadcast_arrays(h, t, b)
    except ValueError:
        raise ValueError("h0, period and beach_slope must be broadcast-compatible") from None
    if not np.isfinite([gravity]).all() or gravity <= 0:
        raise ValueError("gravity must be finite and positive")
    if np.any(~np.isfinite(h) | (h <= 0) | ~np.isfinite(t) | (t <= 0)
              | ~np.isfinite(b) | (b < 0)):
        raise ValueError("wave height and period must be positive; slope must be finite and non-negative")
    l0 = gravity * t**2 / (2 * np.pi)
    setup = 0.35 * b * np.sqrt(h * l0)
    swash = 0.5 * np.sqrt(h * l0 * (0.563 * b**2 + 0.004))
    r2 = 1.1 * (setup + swash)
    if percentile == 2:
        return r2
    if percentile == 1:
        return 0.75 * r2
    if percentile == 50:
        return 0.5 * r2
    if percentile == 0:
        return 0.0 * r2
    raise ValueError("percentile must be one of 0, 1, 2 or 50")


def cerc_longshore_transport(h_break, wave_angle_deg, *, coefficient=0.39,
                             rho_water=1025.0, rho_sediment=2650.0,
                             porosity=0.4, gravity=_G):
    """CERC-style signed bulk longshore transport rate (m3/s).

    Uses breaking wave height, wave angle measured from shore-normal, shallow
    water group speed sqrt(g*Hb), and the immersed-weight energy-flux form:
    Q = K P_ls / ((rho_s-rho_w) g (1-p)). It is an empirical bulk estimate;
    calibration, grain-size effects and detailed surf-zone transformation
    are not represented. Positive sign follows positive input angle.
    """
    h, a = np.broadcast_arrays(np.asarray(h_break, float),
                               np.asarray(wave_angle_deg, float))
    k = _finite_positive("coefficient", coefficient)
    rw = _finite_positive("rho_water", rho_water)
    rs = _finite_positive("rho_sediment", rho_sediment)
    g = _finite_positive("gravity", gravity)
    try:
        p = float(porosity)
    except (TypeError, ValueError):
        raise ValueError("porosity must be in [0, 1)") from None
    if not np.isfinite(p) or not 0 <= p < 1 or rs <= rw:
        raise ValueError("porosity must be in [0, 1) and sediment density exceed water density")
    if np.any(~np.isfinite(h) | (h < 0) | ~np.isfinite(a)):
        raise ValueError("breaking height must be finite and non-negative; angle finite")
    cg = np.sqrt(g * h)
    alpha = np.deg2rad(a)
    p_ls = rw * g * h**2 * cg / 8.0 * np.sin(alpha) * np.cos(alpha)
    return k * p_ls / ((rs - rw) * g * (1.0 - p))


def shoreline_change_rates(years, positions, *, uncertainties=None):
    """Compute EPR, OLS linear rate and optional inverse-variance WLR.

    Positions are signed distances in a projected linear unit at each survey
    time. Rates use that unit per year. Uncertainties are 1-sigma positional
    errors in the same unit; WLR uses weights 1/sigma**2. This is a transect-
    level time regression, not a full DSAS transect-generation workflow.
    """
    x = np.asarray(years, dtype=float)
    y = np.asarray(positions, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < 2:
        raise ValueError("years and positions must be equal-length 1D arrays with at least two observations")
    if np.any(~np.isfinite(x) | ~np.isfinite(y)) or np.unique(x).size != x.size:
        raise ValueError("years and positions must be finite and survey years unique")
    order = np.argsort(x)
    x, y = x[order], y[order]
    epr = (y[-1] - y[0]) / (x[-1] - x[0])
    xc = x - x.mean()
    slope = float(np.dot(xc, y - y.mean()) / np.dot(xc, xc))
    intercept = float(y.mean() - slope * x.mean())
    result = {"epr": float(epr), "ols_rate": slope, "ols_intercept": intercept,
              "ols_r_squared": float(1 - np.sum((y - (intercept + slope*x))**2) /
                                     np.sum((y-y.mean())**2)) if np.ptp(y) > 0 else 1.0}
    if uncertainties is not None:
        s = np.asarray(uncertainties, dtype=float)
        if s.shape != y.shape or np.any(~np.isfinite(s) | (s <= 0)):
            raise ValueError("uncertainties must be positive finite 1D errors matching positions")
        s = s[order]
        w = 1.0 / s**2
        xbar, ybar = np.sum(w*x)/np.sum(w), np.sum(w*y)/np.sum(w)
        denom = np.sum(w*(x-xbar)**2)
        if denom <= 0:
            raise ValueError("weighted survey years have zero variance")
        wslope = np.sum(w*(x-xbar)*(y-ybar))/denom
        wintercept = ybar - wslope*xbar
        result.update({"wlr_rate": float(wslope), "wlr_intercept": float(wintercept)})
    return result

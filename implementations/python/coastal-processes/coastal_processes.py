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
        return 0.5 * (setup - swash)
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


def bruun_rule_recession(sea_level_rise, active_profile_width, berm_height, closure_depth):
    """Idealized Bruun-rule recession R = S*W/(B+h*); consistent length units.
    This equilibrium cross-shore sediment-conservation relation omits
    alongshore transport, geology, barriers and profile disequilibrium.
    It is not a site-specific shoreline forecast.
    """
    s, width, berm, depth = np.broadcast_arrays(
        np.asarray(sea_level_rise, float), np.asarray(active_profile_width, float),
        np.asarray(berm_height, float), np.asarray(closure_depth, float))
    if np.any(~np.isfinite(s) | (s < 0) | ~np.isfinite(width) | (width <= 0)
              | ~np.isfinite(berm) | (berm < 0) | ~np.isfinite(depth) | (depth <= 0)):
        raise ValueError("rise and berm must be non-negative; width and closure depth positive")
    return s * width / (berm + depth)


def dean_equilibrium_profile(distance, scale_parameter):
    """Dean equilibrium profile h(x)=A*x**(2/3); x>=0, A>0.
    A has units length**(1/3) when x and h use the same length unit.
    """
    x = np.asarray(distance, dtype=float)
    a = _finite_positive("scale_parameter", scale_parameter)
    if np.any(~np.isfinite(x) | (x < 0)): raise ValueError("distance must be finite and non-negative")
    return a * np.power(x, 2.0 / 3.0)


def dean_profile_volume(scale_parameter, x_start, x_end):
    """Analytically integrate Dean profile depth from x_start to x_end.
    Returns (3/5)*A*(x_end**(5/3)-x_start**(5/3)); units are length**2.
    """
    a = _finite_positive("scale_parameter", scale_parameter)
    try: x0, x1 = float(x_start), float(x_end)
    except (TypeError, ValueError): raise ValueError("profile bounds must be finite") from None
    if not np.isfinite([x0, x1]).all() or x0 < 0 or x1 < x0:
        raise ValueError("profile bounds must be finite, non-negative and ordered")
    return 3.0 * a / 5.0 * (x1 ** (5.0 / 3.0) - x0 ** (5.0 / 3.0))

def fit_satellite_bathymetry_ratio(log_band_ratio, known_depths):
    """Fit a simple linear calibration depth = intercept + slope*log_ratio.
    Inputs must be paired finite 1D calibration samples with at least two
    distinct ratios. This is a transparent empirical baseline, not a
    physics-based radiative-transfer inversion.
    """
    x, y = np.asarray(log_band_ratio, float), np.asarray(known_depths, float)
    if x.ndim != 1 or y.ndim != 1 or x.shape != y.shape or x.size < 2:
        raise ValueError("calibration arrays must be equal-length 1D arrays with at least two samples")
    if np.any(~np.isfinite(x) | ~np.isfinite(y)) or np.ptp(x) == 0:
        raise ValueError("calibration samples must be finite with varying log ratios")
    slope, intercept = np.polyfit(x, y, 1)
    return {"intercept": float(intercept), "slope": float(slope),
            "r_squared": float(1 - np.sum((y-(intercept+slope*x))**2)/np.sum((y-y.mean())**2)) if np.ptp(y)>0 else 1.0}


def satellite_bathymetry_ratio(log_band_ratio, calibration, *, min_depth=None, max_depth=None):
    """Apply a fitted linear log-band-ratio calibration to depth estimates.
    NaNs are preserved. Optional depth limits mask predictions outside the
    calibrated operating interval; they do not extrapolate or clip values.
    """
    x = np.asarray(log_band_ratio, dtype=float)
    if np.any(np.isinf(x)): raise ValueError("log band ratio cannot contain infinity")
    try: intercept, slope = float(calibration["intercept"]), float(calibration["slope"])
    except (KeyError, TypeError, ValueError): raise ValueError("calibration needs finite intercept and slope") from None
    if not np.isfinite([intercept, slope]).all(): raise ValueError("calibration coefficients must be finite")
    out = intercept + slope*x
    if min_depth is not None:
        if not np.isfinite(min_depth): raise ValueError("min_depth must be finite")
        out = np.where(out >= min_depth, out, np.nan)
    if max_depth is not None:
        if not np.isfinite(max_depth): raise ValueError("max_depth must be finite")
        out = np.where(out <= max_depth, out, np.nan)
    if min_depth is not None and max_depth is not None and min_depth > max_depth:
        raise ValueError("min_depth cannot exceed max_depth")
    return out


def grid_multibeam_soundings(x, y, depth, *, cell_size, origin=(0.0, 0.0), statistic='mean'):
    """Bin soundings to a north-up regular grid using mean or median depth.
    Returns (depth_grid, count_grid, x_centres, y_centres). Grid indices
    increase eastward and southward; empty cells are NaN with count zero.
    The grid is an aggregation, not a hydrographic uncertainty or CUBE solver.
    """
    x, y, z = np.broadcast_arrays(np.asarray(x,float), np.asarray(y,float), np.asarray(depth,float))
    if x.ndim != 1: raise ValueError("soundings must be 1D arrays")
    if not np.isfinite(cell_size) or cell_size <= 0: raise ValueError("cell_size must be positive and finite")
    ox, oy = map(float, origin)
    if not np.isfinite([ox, oy]).all(): raise ValueError("origin must be finite")
    valid = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    if not np.any(valid): raise ValueError("at least one finite sounding is required")
    if statistic not in {"mean", "median"}: raise ValueError("statistic must be mean or median")
    col = np.floor((x[valid]-ox)/cell_size).astype(int)
    row = np.floor((oy-y[valid])/cell_size).astype(int)
    minc, maxc, minr, maxr = col.min(), col.max(), row.min(), row.max()
    ncol, nrow = maxc-minc+1, maxr-minr+1
    bins = [[] for _ in range(nrow*ncol)]
    for rr, cc, zz in zip(row-minr, col-minc, z[valid]): bins[rr*ncol+cc].append(float(zz))
    grid = np.full((nrow,ncol), np.nan); counts = np.zeros((nrow,ncol), dtype=int)
    for i, values in enumerate(bins):
        if values:
            rr, cc = divmod(i,ncol)
            grid[rr,cc] = np.mean(values) if statistic == "mean" else np.median(values)
            counts[rr,cc] = len(values)
    xc = ox + (np.arange(ncol)+minc+0.5)*cell_size
    yc = oy - (np.arange(nrow)+minr+0.5)*cell_size
    return grid, counts, xc, yc

def coastal_vulnerability_index(variable_ranks, *, axis=-1):
    """Compute the conventional six-variable CVI as sqrt(product of ranks).
    Ranks must be finite integers from 1 through 5. The selected axis must
    contain exactly six variables (commonly geomorphology, shoreline-change
    rate, coastal slope, relative sea-level change, significant wave height
    and tidal range). This combines ordinal ranks; it is not a probability.
    """
    r = np.asarray(variable_ranks, dtype=float)
    if r.ndim == 0: raise ValueError('ranks must include a six-variable axis')
    if not isinstance(axis, (int, np.integer)) or not -r.ndim <= axis < r.ndim:
        raise ValueError('axis is outside the rank array dimensions')
    if r.shape[axis] != 6: raise ValueError('CVI requires exactly six variable ranks')
    if np.any(~np.isfinite(r) | (r < 1) | (r > 5) | (r != np.floor(r))):
        raise ValueError('each variable rank must be an integer from 1 through 5')
    return np.sqrt(np.prod(r, axis=axis))

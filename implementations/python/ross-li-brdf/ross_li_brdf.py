"""RossThick-LiSparse reciprocal BRDF kernel fitting and normalization."""
from __future__ import annotations
import numpy as np


def ross_li_kernels(solar_zenith, view_zenith, relative_azimuth, *, height_to_width=2.0, width_to_radius=1.0):
    """Return Ross-Thick volumetric and Li-Sparse-Reciprocal geometric kernels; angles are radians."""
    ts, tv, phi = np.broadcast_arrays(np.asarray(solar_zenith, float), np.asarray(view_zenith, float), np.asarray(relative_azimuth, float))
    if not all(np.all(np.isfinite(a)) for a in (ts, tv, phi)):
        raise ValueError("geometry angles must be finite")
    if np.any((ts < 0) | (ts >= np.pi/2) | (tv < 0) | (tv >= np.pi/2)):
        raise ValueError("zenith angles must lie in [0, pi/2)")
    if not np.isfinite(height_to_width) or height_to_width <= 0 or not np.isfinite(width_to_radius) or width_to_radius <= 0:
        raise ValueError("shape ratios must be finite and positive")
    cos_xi = np.clip(np.cos(ts)*np.cos(tv) + np.sin(ts)*np.sin(tv)*np.cos(phi), -1, 1)
    xi = np.arccos(cos_xi)
    k_vol = (((np.pi/2-xi)*cos_xi + np.sin(xi))/(np.cos(ts)+np.cos(tv))) - np.pi/4
    scale = width_to_radius
    tan_s, tan_v = scale*np.tan(ts), scale*np.tan(tv)
    sec_s, sec_v = np.sqrt(1+tan_s**2), np.sqrt(1+tan_v**2)
    cos_xi_p = np.clip(1/(sec_s*sec_v) + (tan_s/sec_s)*(tan_v/sec_v)*np.cos(phi), -1, 1)
    d2 = np.maximum(tan_s**2+tan_v**2-2*tan_s*tan_v*np.cos(phi), 0)
    cross = tan_s*tan_v*np.sin(phi)
    cos_t = height_to_width*np.sqrt(d2+cross**2)/(sec_s+sec_v)
    t = np.arccos(np.clip(cos_t, -1, 1))
    overlap = (t-np.sin(t)*np.cos(t))*(sec_s+sec_v)/np.pi
    k_geo = overlap-sec_s-sec_v+0.5*(1+cos_xi_p)*sec_s*sec_v
    return k_vol, k_geo


def fit_ross_li_brdf(reflectance, solar_zenith, view_zenith, relative_azimuth, *,
                     reference_solar_zenith, reference_view_zenith=0.0,
                     reference_relative_azimuth=0.0, height_to_width=2.0,
                     width_to_radius=1.0, epsilon=1e-8):
    """Fit per-band isotropic/volumetric/geometric coefficients and normalize to reference geometry."""
    rho = np.asarray(reflectance, float)
    was_1d = rho.ndim == 1
    if was_1d:
        rho = rho[:, None]
    if rho.ndim != 2 or rho.shape[0] < 3 or rho.shape[1] < 1 or not np.all(np.isfinite(rho)):
        raise ValueError("reflectance must be finite (observations,) or (observations, bands), with >=3 observations")
    ts, tv, phi = (np.asarray(v, float) for v in (solar_zenith, view_zenith, relative_azimuth))
    if any(v.shape != (rho.shape[0],) for v in (ts, tv, phi)):
        raise ValueError("each geometry array must have one value per observation")
    kv, kg = ross_li_kernels(ts, tv, phi, height_to_width=height_to_width, width_to_radius=width_to_radius)
    design = np.column_stack((np.ones(rho.shape[0]), kv, kg))
    if np.linalg.matrix_rank(design) < 3:
        raise ValueError("observation geometries do not identify all three kernel coefficients")
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be finite and positive")
    coefficients, _, _, _ = np.linalg.lstsq(design, rho, rcond=None)
    fitted = design @ coefficients
    residual = rho-fitted
    total = np.sum((rho-rho.mean(axis=0))**2, axis=0)
    r2 = np.where(total > epsilon, 1-np.sum(residual**2, axis=0)/np.maximum(total, epsilon), 1.0)
    rmse = np.sqrt(np.mean(residual**2, axis=0))
    rkv, rkg = ross_li_kernels(reference_solar_zenith, reference_view_zenith, reference_relative_azimuth,
                               height_to_width=height_to_width, width_to_radius=width_to_radius)
    reference_model = np.array([1.0, float(rkv), float(rkg)]) @ coefficients
    if np.any(np.abs(fitted) <= epsilon) or np.any(np.abs(reference_model) <= epsilon):
        raise ValueError("fitted BRDF is too close to zero for stable normalization")
    normalized = rho*(reference_model[None, :]/fitted)
    return {"normalized": normalized[:, 0] if was_1d else normalized,
            "coefficients": coefficients[:, 0] if was_1d else coefficients,
            "r_squared": float(r2[0]) if was_1d else r2,
            "rmse": float(rmse[0]) if was_1d else rmse,
            "reference_reflectance": float(reference_model[0]) if was_1d else reference_model}

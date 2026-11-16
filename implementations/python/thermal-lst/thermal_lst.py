"""Thermal-infrared land-surface temperature retrieval baselines."""
from __future__ import annotations

import numpy as np


def _broadcast_finite(**values):
    arrays = {name: np.asarray(value, dtype=float) for name, value in values.items()}
    try:
        arrays = np.broadcast_arrays(*arrays.values())
    except ValueError as exc:
        raise ValueError("inputs must be broadcast-compatible") from exc
    if any(not np.all(np.isfinite(a)) for a in arrays):
        raise ValueError("inputs must contain only finite values")
    return dict(zip(values, arrays))


def brightness_temperature(radiance, k1, k2):
    """Convert at-sensor spectral radiance to brightness temperature (K).

    K1 and K2 are sensor/band-specific Planck calibration constants and
    radiance must use the units associated with those constants.
    """
    a = _broadcast_finite(radiance=radiance)
    l = a["radiance"]
    if np.any(l <= 0) or not np.isfinite(k1) or not np.isfinite(k2) or k1 <= 0 or k2 <= 0:
        raise ValueError("radiance, K1 and K2 must be positive and finite")
    return k2 / np.log1p(k1 / l)


def single_channel_lst(radiance, emissivity, transmittance, upwelling_radiance,
                       downwelling_radiance, k1, k2):
    """Invert a single-band thermal radiative-transfer equation.

    Uses L_sensor = tau * (eps * B(Ts) + (1-eps) * L_down) + L_up,
    followed by the inverse Planck function. Radiance units and K1/K2 must
    correspond to the same sensor band. Atmospheric terms are supplied by
    the caller; this function does not retrieve them.
    """
    a = _broadcast_finite(radiance=radiance, emissivity=emissivity,
                          transmittance=transmittance,
                          upwelling_radiance=upwelling_radiance,
                          downwelling_radiance=downwelling_radiance)
    l, eps, tau, lup, ldown = (a[k] for k in (
        "radiance", "emissivity", "transmittance",
        "upwelling_radiance", "downwelling_radiance"))
    if np.any(l <= 0) or np.any((eps <= 0) | (eps > 1)):
        raise ValueError("radiance must be positive and emissivity in (0, 1]")
    if np.any((tau <= 0) | (tau > 1)) or np.any(lup < 0) or np.any(ldown < 0):
        raise ValueError("transmittance must be in (0, 1] and atmospheric radiances nonnegative")
    if not np.isfinite(k1) or not np.isfinite(k2) or k1 <= 0 or k2 <= 0:
        raise ValueError("K1 and K2 must be positive and finite")
    surface_radiance = (l - lup - tau * (1.0 - eps) * ldown) / (tau * eps)
    if np.any(surface_radiance <= 0):
        raise ValueError("atmosphere-corrected surface radiance must be positive")
    return k2 / np.log1p(k1 / surface_radiance)


def split_window_lst(brightness_temperature_10, brightness_temperature_11,
                     emissivity_10, emissivity_11, water_vapour,
                     coefficients):
    """Apply a caller-calibrated two-channel generalized split-window model.

    coefficients are (c0,...,c6) for:
      T10 + c1*dT + c2*dT**2 + c0
      + (c3+c4*w)*(1-eps_mean) + (c5+c6*w)*(eps10-eps11)

    Temperatures are kelvin; water vapour uses the units for which the
    coefficients were calibrated. Coefficients are sensor/atmosphere specific.
    """
    a = _broadcast_finite(t10=brightness_temperature_10,
                          t11=brightness_temperature_11,
                          eps10=emissivity_10, eps11=emissivity_11,
                          water_vapour=water_vapour)
    t10, t11, e10, e11, w = (a[k] for k in ("t10", "t11", "eps10", "eps11", "water_vapour"))
    coeff = np.asarray(coefficients, dtype=float)
    if coeff.shape != (7,) or not np.all(np.isfinite(coeff)):
        raise ValueError("coefficients must be seven finite values (c0 through c6)")
    if np.any(t10 <= 0) or np.any(t11 <= 0):
        raise ValueError("brightness temperatures must be positive kelvin values")
    if np.any((e10 <= 0) | (e10 > 1) | (e11 <= 0) | (e11 > 1)):
        raise ValueError("both emissivities must lie in (0, 1]")
    if np.any(w < 0):
        raise ValueError("water vapour must be nonnegative")
    c0, c1, c2, c3, c4, c5, c6 = coeff
    dt = t10 - t11
    mean_emissivity = 0.5 * (e10 + e11)
    return (t10 + c1 * dt + c2 * dt**2 + c0
            + (c3 + c4 * w) * (1.0 - mean_emissivity)
            + (c5 + c6 * w) * (e10 - e11))

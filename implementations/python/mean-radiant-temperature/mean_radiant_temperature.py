"""Globe-thermometer mean radiant temperature estimates (ISO 7726 form)."""
from __future__ import annotations
import numpy as np

STEFAN_BOLTZMANN = 5.670374419e-8

def mean_radiant_temperature(globe_temperature_c, air_temperature_c, air_velocity_m_s, *, globe_diameter_m=0.15, emissivity=0.95):
    """Estimate MRT from a steady-state spherical globe observation.

    Inputs: Celsius, m/s, metres, and dimensionless emissivity.
    Natural/forced convection coefficients follow ISO 7726 empirical forms.
    """
    try:
        tg, ta, velocity = np.broadcast_arrays(
            np.asarray(globe_temperature_c, dtype=float),
            np.asarray(air_temperature_c, dtype=float),
            np.asarray(air_velocity_m_s, dtype=float))
        diameter, eps = float(globe_diameter_m), float(emissivity)
    except (TypeError, ValueError) as exc:
        raise ValueError("inputs must be numeric") from exc
    if not all(np.all(np.isfinite(a)) for a in (tg, ta, velocity)):
        raise ValueError("temperatures and velocity must be finite")
    if np.any(tg <= -273.15) or np.any(ta <= -273.15):
        raise ValueError("temperatures must be above absolute zero")
    if np.any(velocity < 0):
        raise ValueError("air velocity must be nonnegative")
    if not np.isfinite(diameter) or diameter <= 0:
        raise ValueError("globe diameter must be finite and positive")
    if not np.isfinite(eps) or not 0 < eps <= 1:
        raise ValueError("emissivity must be in (0, 1]")
    delta = tg - ta
    h_natural = 1.4 * (np.abs(delta) / diameter) ** 0.25
    h_forced = 6.3 * velocity ** 0.6 / diameter ** 0.4
    use_forced = h_forced >= h_natural
    h_conv = np.maximum(h_natural, h_forced)
    globe_k = tg + 273.15
    radiant_k4 = globe_k**4 + h_conv * delta / (eps * STEFAN_BOLTZMANN)
    if np.any(~np.isfinite(radiant_k4)) or np.any(radiant_k4 <= 0):
        raise ValueError("inputs produce nonphysical radiant temperature")
    radiant_c = radiant_k4**0.25 - 273.15
    if radiant_c.ndim == 0:
        return {"mean_radiant_temperature_c": float(radiant_c),
                "convective_heat_transfer_w_m2_k": float(h_conv),
                "convection_regime": "forced" if bool(use_forced) else "natural"}
    return {"mean_radiant_temperature_c": radiant_c,
            "convective_heat_transfer_w_m2_k": h_conv,
            "convection_regime": np.where(use_forced, "forced", "natural")}

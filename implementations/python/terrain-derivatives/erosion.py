"""USLE/RUSLE empirical soil-loss factors and slope-length calculations."""
from __future__ import annotations
import numpy as np


def rusle_ls_factor(slope_degrees, slope_length, *, m=None):
    """Calculate a conventional RUSLE L*S factor from slope and slope length.

    Slope is in degrees and slope_length is horizontal slope length in metres.
    If m is omitted, the slope-dependent exponent is calculated from the
    conventional beta relationship. The S-factor uses the common two-branch
    percent-slope approximation. This is not a flow-accumulation-aware LS
    formulation for complex terrain.
    """
    slope, length = np.broadcast_arrays(np.asarray(slope_degrees, float), np.asarray(slope_length, float))
    if np.any(~np.isfinite(slope)) or np.any(~np.isfinite(length)):
        raise ValueError("slope and slope_length must be finite")
    if np.any((slope < 0) | (slope >= 90)) or np.any(length <= 0):
        raise ValueError("slope must be in [0, 90) and slope_length positive")
    sin_slope = np.sin(np.radians(slope))
    if m is None:
        beta = sin_slope / (0.0896 * (3.0 * sin_slope ** 0.8 + 0.56))
        exponent = beta / (1.0 + beta)
    else:
        try:
            exponent = np.broadcast_to(np.asarray(m, float), slope.shape)
        except ValueError:
            raise ValueError("m must be broadcastable to slope") from None
        if np.any(~np.isfinite(exponent)) or np.any((exponent < 0) | (exponent > 1)):
            raise ValueError("m must be finite and in [0, 1]")
    l_factor = (length / 22.13) ** exponent
    percent_slope = np.tan(np.radians(slope)) * 100.0
    s_factor = np.where(percent_slope < 9.0, 10.8 * sin_slope + 0.03, 16.8 * sin_slope - 0.50)
    s_factor = np.where(slope == 0.0, 0.0, np.maximum(s_factor, 0.0))
    return l_factor * s_factor


def rusle_soil_loss(rainfall_erosivity, soil_erodibility, ls_factor, cover_management, support_practice):
    """Calculate long-term mean sheet/rill soil loss A=R*K*LS*C*P.

    All five factors must be finite and non-negative and follow a mutually
    consistent unit convention. Inputs broadcast using NumPy rules. The
    output unit is determined by the supplied R and K units.
    """
    factors = np.broadcast_arrays(*[np.asarray(v, float) for v in (
        rainfall_erosivity, soil_erodibility, ls_factor,
        cover_management, support_practice,
    )])
    if any(np.any(~np.isfinite(v)) or np.any(v < 0) for v in factors):
        raise ValueError("R, K, LS, C and P factors must be finite and non-negative")
    result = np.ones(factors[0].shape, dtype=float)
    for factor in factors:
        result *= factor
    return result


def usle_soil_loss(rainfall_erosivity, soil_erodibility, ls_factor, cover_management, support_practice):
    """USLE factor-product baseline; see rusle_soil_loss for the contract."""
    return rusle_soil_loss(
        rainfall_erosivity, soil_erodibility, ls_factor,
        cover_management, support_practice,
    )

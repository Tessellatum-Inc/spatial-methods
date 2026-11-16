"""SAR radiometric backscatter calibration and block multilooking."""
from __future__ import annotations
import numpy as np


def radiometric_calibrate(digital_number, calibration_factor, *,
                          output="sigma0", incidence_angle=None,
                          noise_power=0.0):
    """Calibrate complex/detected DN to sigma0, beta0 or gamma0.

    calibration_factor maps input intensity |DN|^2 to sigma0. Incidence
    angle is radians from vertical and is required for beta0/gamma0.
    Noise power is subtracted from intensity before calibration and floored
    at zero. Calibration LUT interpolation and sensor metadata are caller-owned.
    """
    dn = np.asarray(digital_number)
    if dn.ndim < 1 or not np.all(np.isfinite(dn)):
        raise ValueError("digital_number must be a finite non-scalar array")
    try:
        factor = np.asarray(calibration_factor, dtype=float)
        noise = np.asarray(noise_power, dtype=float)
        intensity, factor, noise = np.broadcast_arrays(np.abs(dn)**2, factor, noise)
    except (TypeError, ValueError):
        raise ValueError("calibration_factor and noise_power must broadcast to the input") from None
    if not np.all(np.isfinite(factor)) or np.any(factor <= 0):
        raise ValueError("calibration_factor must be finite and positive")
    if not np.all(np.isfinite(noise)) or np.any(noise < 0):
        raise ValueError("noise_power must be finite and non-negative")
    sigma0 = np.maximum(intensity-noise, 0.0)*factor
    kind = str(output).lower()
    if kind == "sigma0":
        return sigma0
    if kind not in {"beta0", "gamma0"}:
        raise ValueError("output must be sigma0, beta0 or gamma0")
    if incidence_angle is None:
        raise ValueError("incidence_angle is required for beta0 and gamma0")
    angle = np.asarray(incidence_angle, dtype=float)
    try:
        angle = np.broadcast_to(angle, sigma0.shape)
    except ValueError:
        raise ValueError("incidence_angle must broadcast to the calibrated image") from None
    if not np.all(np.isfinite(angle)) or np.any((angle <= 0) | (angle >= np.pi/2)):
        raise ValueError("incidence_angle must be finite and between zero and pi/2 radians")
    denominator = np.sin(angle) if kind == "beta0" else np.cos(angle)
    return sigma0/denominator


def multilook_intensity(image, *, looks=(2, 2), nodata_policy="omit"):
    """Average non-overlapping azimuth/range blocks; trailing edges are cropped."""
    z = np.asarray(image, dtype=float)
    if z.ndim != 2 or min(z.shape) < 1:
        raise ValueError("image must be a non-empty 2D array")
    if len(looks) != 2 or any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer)) or v < 1 for v in looks):
        raise ValueError("looks must be two positive integers")
    az, rg = map(int, looks)
    policy = str(nodata_policy).lower()
    if policy not in {"omit", "propagate"}:
        raise ValueError("nodata_policy must be omit or propagate")
    rows, cols = z.shape[0]//az, z.shape[1]//rg
    if rows == 0 or cols == 0:
        raise ValueError("look factors exceed the image dimensions")
    crop = z[:rows*az, :cols*rg]
    blocks = crop.reshape(rows, az, cols, rg).transpose(0,2,1,3).reshape(rows,cols,az*rg)
    valid = np.isfinite(blocks)
    count = valid.sum(axis=2)
    total = np.where(valid, blocks, 0.0).sum(axis=2)
    mean = np.divide(total, count, out=np.full((rows,cols), np.nan), where=count>0)
    if policy == "propagate":
        mean[count < az*rg] = np.nan
    return {"intensity": mean, "valid_looks": count,
            "looks": (az, rg), "cropped_shape": (rows*az, cols*rg)}

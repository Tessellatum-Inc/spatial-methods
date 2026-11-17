"""Finite-difference Tissot indicatrix diagnostics for map projections."""
from __future__ import annotations

from math import asin, cos, degrees, isfinite, pi, sin, sqrt
from typing import Callable


def tissot_indicatrix(
    projection: Callable[[float, float], tuple[float, float]],
    longitude: float,
    latitude: float,
    *,
    earth_radius: float = 6_371_008.8,
    step_degrees: float = 1e-5,
) -> dict:
    """Estimate local principal scales, area scale and angular distortion.

    projection receives longitude and latitude in degrees and returns projected
    x/y in the same linear units as earth_radius.
    """
    if not callable(projection):
        raise ValueError("projection must be callable")
    if not isfinite(longitude) or not isfinite(latitude) or not -90 < latitude < 90:
        raise ValueError("longitude must be finite and latitude must be finite and strictly between the poles")
    if not isfinite(earth_radius) or earth_radius <= 0:
        raise ValueError("earth_radius must be finite and positive")
    if not isfinite(step_degrees) or step_degrees <= 0 or step_degrees >= 0.1:
        raise ValueError("step_degrees must be finite and in (0, 0.1)")

    step = step_degrees * pi / 180.0

    def project(lon_rad: float, lat_rad: float) -> tuple[float, float]:
        try:
            x, y = projection(degrees(lon_rad), degrees(lat_rad))
            x, y = float(x), float(y)
        except (TypeError, ValueError, OverflowError, ArithmeticError) as exc:
            raise ValueError("projection must return finite numeric x/y coordinates") from exc
        if not isfinite(x) or not isfinite(y):
            raise ValueError("projection must return finite numeric x/y coordinates")
        return x, y

    lon = longitude * pi / 180.0
    lat = latitude * pi / 180.0
    xp = project(lon + step, lat)
    xm = project(lon - step, lat)
    yp = project(lon, lat + step)
    ym = project(lon, lat - step)
    dx_dlon = (xp[0] - xm[0]) / (2 * step)
    dy_dlon = (xp[1] - xm[1]) / (2 * step)
    dx_dlat = (yp[0] - ym[0]) / (2 * step)
    dy_dlat = (yp[1] - ym[1]) / (2 * step)

    east_ground = earth_radius * cos(lat)
    north_ground = earth_radius
    j11, j21 = dx_dlon / east_ground, dy_dlon / east_ground
    j12, j22 = dx_dlat / north_ground, dy_dlat / north_ground
    # Eigenvalues of J.T @ J give squared principal local scale factors.
    a = j11 * j11 + j21 * j21
    b = j11 * j12 + j21 * j22
    c = j12 * j12 + j22 * j22
    discriminant = sqrt(max(0.0, (a - c) ** 2 + 4 * b * b))
    largest = max(0.0, (a + c + discriminant) / 2)
    smallest = max(0.0, (a + c - discriminant) / 2)
    major = sqrt(largest)
    minor = sqrt(smallest)
    area = abs(j11 * j22 - j12 * j21)
    if major + minor == 0:
        angular = None
    else:
        ratio = max(-1.0, min(1.0, (major - minor) / (major + minor)))
        angular = degrees(2 * asin(ratio))
    return {
        "major_scale": major,
        "minor_scale": minor,
        "area_scale": area,
        "angular_distortion_degrees": angular,
        "jacobian": ((j11, j12), (j21, j22)),
        "longitude": float(longitude),
        "latitude": float(latitude),
        "earth_radius": float(earth_radius),
        "step_degrees": float(step_degrees),
    }

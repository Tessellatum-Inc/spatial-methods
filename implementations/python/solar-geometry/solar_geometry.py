"""Solar position and extraterrestrial irradiance reference calculations."""
from datetime import datetime, timezone
import math
SOLAR_CONSTANT = 1361.0

def _validate(latitude, longitude, timestamp):
    if isinstance(latitude, bool) or not isinstance(latitude, (int, float)) or not math.isfinite(latitude) or not -90 <= latitude <= 90:
        raise ValueError("latitude must be finite and in [-90, 90]")
    if isinstance(longitude, bool) or not isinstance(longitude, (int, float)) or not math.isfinite(longitude) or not -180 <= longitude <= 180:
        raise ValueError("longitude must be finite and in [-180, 180]")
    if not isinstance(timestamp, datetime) or timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return float(latitude), float(longitude), timestamp.astimezone(timezone.utc)

def solar_position(latitude, longitude, timestamp):
    """Return geometric solar elevation, zenith and azimuth (clockwise from north)."""
    lat, lon, dt = _validate(latitude, longitude, timestamp)
    day = dt.timetuple().tm_yday
    hour = dt.hour + dt.minute / 60 + dt.second / 3600 + dt.microsecond / 3.6e9
    gamma = 2 * math.pi / 365 * (day - 1 + (hour - 12) / 24)
    eq_time = 229.18 * (0.000075 + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma))
    decl = (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma))
    minutes = dt.hour * 60 + dt.minute + dt.second / 60 + dt.microsecond / 60e6
    true_solar_minutes = (minutes + eq_time + 4 * lon) % 1440
    hour_angle = math.radians(true_solar_minutes / 4 - 180)
    phi = math.radians(lat)
    cos_zenith = math.sin(phi) * math.sin(decl) + math.cos(phi) * math.cos(decl) * math.cos(hour_angle)
    zenith = math.degrees(math.acos(max(-1.0, min(1.0, cos_zenith))))
    elevation = 90.0 - zenith
    azimuth = (math.degrees(math.atan2(math.sin(hour_angle),
        math.cos(hour_angle) * math.sin(phi) - math.tan(decl) * math.cos(phi))) + 180.0) % 360.0
    return {"solar_elevation_deg": elevation, "solar_zenith_deg": zenith,
            "solar_azimuth_deg": azimuth, "equation_of_time_minutes": eq_time,
            "declination_deg": math.degrees(decl)}

def extraterrestrial_irradiance(latitude, longitude, timestamp, solar_constant=SOLAR_CONSTANT):
    """Return top-of-atmosphere normal and horizontal irradiance in W m-2."""
    position = solar_position(latitude, longitude, timestamp)
    if isinstance(solar_constant, bool) or not isinstance(solar_constant, (int, float)) or not math.isfinite(solar_constant) or solar_constant <= 0:
        raise ValueError("solar_constant must be finite and positive")
    day = timestamp.astimezone(timezone.utc).timetuple().tm_yday
    normal = float(solar_constant) * (1.0 + 0.033 * math.cos(2 * math.pi * day / 365))
    horizontal = normal * max(0.0, math.sin(math.radians(position["solar_elevation_deg"])))
    return {"normal_irradiance_w_m2": normal, "horizontal_irradiance_w_m2": horizontal}

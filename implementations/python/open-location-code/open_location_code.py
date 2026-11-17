"""Minimal full-code Open Location Code (Plus Code) reference implementation.

Implements encoding and decoding of full codes. Short-code recovery requires
local context and is intentionally outside this module's contract.
"""
import math
from decimal import Decimal

ALPHABET = "23456789CFGHJMPQRVWX"
SEPARATOR = "+"
SEPARATOR_POSITION = 8
MAX_CODE_LENGTH = 15


def _validate_coordinate(latitude, longitude):
    if not math.isfinite(latitude) or not math.isfinite(longitude):
        raise ValueError("latitude and longitude must be finite")
    if not -90.0 <= latitude <= 90.0:
        raise ValueError("latitude must be in [-90, 90]")


def encode(latitude, longitude, code_length=10):
    """Encode WGS84 coordinates as a full code of 10 to 15 characters."""
    latitude, longitude = float(latitude), float(longitude)
    _validate_coordinate(latitude, longitude)
    if not isinstance(code_length, int) or isinstance(code_length, bool) or not 10 <= code_length <= MAX_CODE_LENGTH:
        raise ValueError("code_length must be an integer from 10 to 15")
    latitude = min(Decimal(str(latitude)), Decimal("90") - Decimal("1e-12"))
    longitude = (Decimal(str(longitude)) + Decimal(180)) % Decimal(360)
    if longitude < 0:
        longitude += Decimal(360)
    longitude -= Decimal(180)
    resolutions = tuple(map(Decimal, ("20", "1", "0.05", "0.0025", "0.000125")))
    lat_value, lon_value = latitude + Decimal(90), longitude + Decimal(180)
    digits = []
    for resolution in resolutions:
        lat_digit = min(int(lat_value / resolution), 19)
        lon_digit = min(int(lon_value / resolution), 19)
        digits.extend((ALPHABET[lat_digit], ALPHABET[lon_digit]))
        lat_value -= lat_digit * resolution
        lon_value -= lon_digit * resolution
    if code_length > 10:
        lat_resolution = lon_resolution = resolutions[-1]
        for _ in range(code_length - 10):
            lat_resolution /= 5
            lon_resolution /= 4
            row = min(int(lat_value / lat_resolution), 4)
            col = min(int(lon_value / lon_resolution), 3)
            digits.append(ALPHABET[row * 4 + col])
            lat_value -= row * lat_resolution
            lon_value -= col * lon_resolution
    raw = "".join(digits[:code_length])
    return raw[:SEPARATOR_POSITION] + SEPARATOR + raw[SEPARATOR_POSITION:]


def decode(code):
    """Decode a full code to (south, west, north, east) cell bounds."""
    if not isinstance(code, str):
        raise ValueError("code must be a string")
    code = code.strip().upper()
    if code.count(SEPARATOR) != 1 or code.index(SEPARATOR) != SEPARATOR_POSITION:
        raise ValueError("a full code with separator at position 8 is required")
    raw = code.replace(SEPARATOR, "")
    if not 10 <= len(raw) <= MAX_CODE_LENGTH or any(ch not in ALPHABET for ch in raw):
        raise ValueError("code must contain 10 to 15 valid alphabet characters")
    resolutions = tuple(map(Decimal, ("20", "1", "0.05", "0.0025", "0.000125")))
    south, west = Decimal(-90), Decimal(-180)
    lat_resolution = lon_resolution = resolutions[0]
    for pair_index in range(5):
        south += ALPHABET.index(raw[2 * pair_index]) * lat_resolution
        west += ALPHABET.index(raw[2 * pair_index + 1]) * lon_resolution
        lat_resolution = lon_resolution = resolutions[min(pair_index + 1, 4)]
    north, east = south + lat_resolution, west + lon_resolution
    for ch in raw[10:]:
        lat_resolution /= 5
        lon_resolution /= 4
        row, col = divmod(ALPHABET.index(ch), 4)
        south += row * lat_resolution
        west += col * lon_resolution
        north, east = south + lat_resolution, west + lon_resolution
    return tuple(map(float, (south, west, north, east)))

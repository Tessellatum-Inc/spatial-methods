"""Geohash encode/decode reference implementation."""
from math import isfinite

_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"
_DECODE = {char: i for i, char in enumerate(_ALPHABET)}


def _coordinate(value, lower, upper, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a finite number") from None
    if not isfinite(number) or not lower <= number <= upper:
        raise ValueError(f"{name} must lie in [{lower}, {upper}]")
    return number


def encode(latitude, longitude, precision=12):
    """Encode WGS84 latitude/longitude into a base-32 geohash."""
    lat = _coordinate(latitude, -90, 90, "latitude")
    lon = _coordinate(longitude, -180, 180, "longitude")
    if isinstance(precision, bool) or not isinstance(precision, int) or not 1 <= precision <= 12:
        raise ValueError("precision must be an integer from 1 through 12")
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    bits, value, chars = 0, 0, []
    even = True
    while len(chars) < precision:
        interval = lon_range if even else lat_range
        coordinate = lon if even else lat
        midpoint = (interval[0] + interval[1]) / 2
        value <<= 1
        if coordinate >= midpoint:
            value |= 1
            interval[0] = midpoint
        else:
            interval[1] = midpoint
        even = not even
        bits += 1
        if bits == 5:
            chars.append(_ALPHABET[value])
            bits, value = 0, 0
    return "".join(chars)


def decode_bounds(geohash):
    """Return (south, north, west, east) bounds of a geohash cell."""
    if not isinstance(geohash, str) or not 1 <= len(geohash) <= 12:
        raise ValueError("geohash must be a string of 1 through 12 characters")
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    even = True
    for char in geohash.lower():
        if char not in _DECODE:
            raise ValueError(f"invalid geohash character: {char!r}")
        value = _DECODE[char]
        for mask in (16, 8, 4, 2, 1):
            interval = lon_range if even else lat_range
            midpoint = (interval[0] + interval[1]) / 2
            if value & mask:
                interval[0] = midpoint
            else:
                interval[1] = midpoint
            even = not even
    return lat_range[0], lat_range[1], lon_range[0], lon_range[1]


def decode(geohash):
    """Return the geohash cell centre as (latitude, longitude)."""
    south, north, west, east = decode_bounds(geohash)
    return (south+north)/2, (west+east)/2

"""Small, dependency-free spatial key encoders for integer grids and geographic coordinates.

The module deliberately separates three encodings:
- Morton/Z-order interleaves integer coordinate bits.
- Hilbert maps integer grid cells to a locality-preserving one-dimensional index.
- Geohash recursively bisects longitude/latitude intervals into base-32 strings.
"""
from __future__ import annotations

import math

_GEOHASH_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"
_GEOHASH_DECODE = {char: index for index, char in enumerate(_GEOHASH_ALPHABET)}


def _validate_grid(x: int, y: int, bits: int) -> int:
    if isinstance(bits, bool) or not isinstance(bits, int) or not 1 <= bits <= 32:
        raise ValueError("bits must be an integer from 1 through 32")
    limit = 1 << bits
    for name, value in (("x", x), ("y", y)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
        if not 0 <= value < limit:
            raise ValueError(f"{name} must be in [0, {limit})")
    return limit


def morton_encode(x: int, y: int, bits: int = 16) -> int:
    """Interleave x/y bits, placing x in even bit positions and y in odd ones."""
    _validate_grid(x, y, bits)
    code = 0
    for bit in range(bits):
        code |= ((x >> bit) & 1) << (2 * bit)
        code |= ((y >> bit) & 1) << (2 * bit + 1)
    return code


def morton_decode(code: int, bits: int = 16) -> tuple[int, int]:
    """Invert :func:`morton_encode` for a fixed coordinate bit width."""
    if isinstance(bits, bool) or not isinstance(bits, int) or not 1 <= bits <= 32:
        raise ValueError("bits must be an integer from 1 through 32")
    if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code < (1 << (2 * bits)):
        raise ValueError("code does not fit the requested bit width")
    x = y = 0
    for bit in range(bits):
        x |= ((code >> (2 * bit)) & 1) << bit
        y |= ((code >> (2 * bit + 1)) & 1) << bit
    return x, y


def _hilbert_rotate(scale: int, x: int, y: int, rx: int, ry: int) -> tuple[int, int]:
    if ry == 0:
        if rx == 1:
            x = scale - 1 - x
            y = scale - 1 - y
        x, y = y, x
    return x, y


def hilbert_encode(x: int, y: int, bits: int = 16) -> int:
    """Map a cell in a 2**bits square grid to its Hilbert distance."""
    side = _validate_grid(x, y, bits)
    distance = 0
    scale = side // 2
    while scale:
        rx = 1 if (x & scale) else 0
        ry = 1 if (y & scale) else 0
        distance += scale * scale * ((3 * rx) ^ ry)
        x, y = _hilbert_rotate(scale, x, y, rx, ry)
        scale //= 2
    return distance


def hilbert_decode(distance: int, bits: int = 16) -> tuple[int, int]:
    """Invert :func:`hilbert_encode` for a fixed grid bit width."""
    if isinstance(bits, bool) or not isinstance(bits, int) or not 1 <= bits <= 32:
        raise ValueError("bits must be an integer from 1 through 32")
    side = 1 << bits
    if isinstance(distance, bool) or not isinstance(distance, int) or not 0 <= distance < side * side:
        raise ValueError("distance does not fit the requested grid")
    x = y = 0
    remaining = distance
    scale = 1
    while scale < side:
        rx = 1 & (remaining // 2)
        ry = 1 & (remaining ^ rx)
        x, y = _hilbert_rotate(scale, x, y, rx, ry)
        x += scale * rx
        y += scale * ry
        remaining //= 4
        scale *= 2
    return x, y


def geohash_encode(latitude: float, longitude: float, precision: int = 8) -> str:
    """Encode WGS84 latitude/longitude as a base-32 geohash."""
    if isinstance(precision, bool) or not isinstance(precision, int) or not 1 <= precision <= 12:
        raise ValueError("precision must be an integer from 1 through 12")
    latitude = float(latitude)
    longitude = float(longitude)
    if not math.isfinite(latitude) or not -90.0 <= latitude <= 90.0:
        raise ValueError("latitude must be finite and in [-90, 90]")
    if not math.isfinite(longitude) or not -180.0 <= longitude <= 180.0:
        raise ValueError("longitude must be finite and in [-180, 180]")
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    even = True
    bits = 0
    value = 0
    result: list[str] = []
    while len(result) < precision:
        interval = lon_range if even else lat_range
        coordinate = longitude if even else latitude
        midpoint = (interval[0] + interval[1]) / 2.0
        value <<= 1
        if coordinate >= midpoint:
            value |= 1
            interval[0] = midpoint
        else:
            interval[1] = midpoint
        even = not even
        bits += 1
        if bits == 5:
            result.append(_GEOHASH_ALPHABET[value])
            bits = value = 0
    return "".join(result)


def geohash_decode(code: str) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return ((south, north), (west, east)) bounds for a geohash."""
    if not isinstance(code, str) or not 1 <= len(code) <= 12:
        raise ValueError("geohash must be a string of 1 through 12 characters")
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    even = True
    for char in code.lower():
        if char not in _GEOHASH_DECODE:
            raise ValueError(f"invalid geohash character: {char!r}")
        value = _GEOHASH_DECODE[char]
        for mask in (16, 8, 4, 2, 1):
            interval = lon_range if even else lat_range
            midpoint = (interval[0] + interval[1]) / 2.0
            if value & mask:
                interval[0] = midpoint
            else:
                interval[1] = midpoint
            even = not even
    return (lat_range[0], lat_range[1]), (lon_range[0], lon_range[1])

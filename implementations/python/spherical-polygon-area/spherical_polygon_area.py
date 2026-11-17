"""Spherical polygon area on a sphere using signed triangle excesses."""
from __future__ import annotations

import math
import numpy as np


def _ring_vectors(ring, name):
    try:
        coordinates = np.asarray(ring, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a numeric array of latitude/longitude pairs") from exc
    if coordinates.ndim != 2 or coordinates.shape[1] != 2 or len(coordinates) < 3:
        raise ValueError(f"{name} must contain at least three latitude/longitude pairs")
    if not np.isfinite(coordinates).all():
        raise ValueError(f"{name} must contain finite coordinates")
    if np.any((coordinates[:, 0] < -90) | (coordinates[:, 0] > 90)):
        raise ValueError("latitudes must lie in [-90, 90] degrees")
    if np.any((coordinates[:, 1] < -180) | (coordinates[:, 1] > 180)):
        raise ValueError("longitudes must lie in [-180, 180] degrees")
    if np.allclose(coordinates[0], coordinates[-1], rtol=0, atol=1e-12):
        coordinates = coordinates[:-1]
    if len(coordinates) < 3:
        raise ValueError(f"{name} must contain at least three distinct ring vertices")
    lat = np.deg2rad(coordinates[:, 0])
    lon = np.deg2rad(coordinates[:, 1])
    vectors = np.column_stack((np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)))
    if any(np.linalg.norm(vectors[i] - vectors[(i+1) % len(vectors)]) < 1e-12 for i in range(len(vectors))):
        raise ValueError(f"{name} contains consecutive duplicate vertices")
    if any(np.linalg.norm(vectors[i] + vectors[(i+1) % len(vectors)]) < 1e-10 for i in range(len(vectors))):
        raise ValueError(f"{name} contains an antipodal edge with ambiguous minor arc")
    return vectors


def _signed_unit_sphere_area(vectors):
    anchor = vectors[0]
    total = 0.0
    for i in range(1, len(vectors)-1):
        b, c = vectors[i], vectors[i+1]
        determinant = float(np.dot(anchor, np.cross(b, c)))
        denominator = 1.0 + float(np.dot(anchor, b) + np.dot(b, c) + np.dot(c, anchor))
        total += 2.0 * math.atan2(determinant, denominator)
    return total


def spherical_polygon_area(exterior, *, holes=None, radius=6371008.8):
    """Compute spherical polygon area in square units of ``radius``.

    Rings are arrays of (latitude, longitude) degrees. The exterior is
    measured by absolute signed spherical excess; hole areas are subtracted.
    This fan-triangulation formulation assumes a simple polygon whose
    intended region is the smaller region represented without hemisphere-scale
    ambiguity. It does not implement ellipsoidal geodesic polygon area.
    """
    if isinstance(radius, (bool, np.bool_)):
        raise ValueError("radius must be finite and positive")
    try:
        r = float(radius)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("radius must be finite and positive") from exc
    if not math.isfinite(r) or r <= 0:
        raise ValueError("radius must be finite and positive")
    outer = abs(_signed_unit_sphere_area(_ring_vectors(exterior, "exterior")))
    outer = min(outer, 4.0 * math.pi - outer)
    hole_area = 0.0
    if holes is not None:
        for index, ring in enumerate(holes):
            hole_area += abs(_signed_unit_sphere_area(_ring_vectors(ring, f"hole {index}")))
    if hole_area > outer + 1e-10:
        raise ValueError("total hole area cannot exceed exterior area")
    return max(0.0, outer - hole_area) * r * r

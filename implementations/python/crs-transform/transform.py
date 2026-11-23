"""Explicit-axis-order coordinate transformation using pyproj."""
from __future__ import annotations
from typing import Sequence
import numpy as np
from pyproj import CRS, Geod, Transformer
from pyproj.exceptions import ProjError

def transform_points(points: Sequence[Sequence[float]]|np.ndarray, source_crs, target_crs) -> np.ndarray:
    """Transform an N×2 coordinate array, enforcing traditional x/y order.

    For geographic coordinates x is longitude and y is latitude. For projected
    coordinates x is easting and y is northing. CRS units and datum operations
    are delegated to PROJ through pyproj.
    """
    coordinates=np.asarray(points,dtype=float)
    if coordinates.ndim!=2 or coordinates.shape[1]!=2 or coordinates.shape[0]==0:
        raise ValueError("points must be a non-empty N×2 coordinate array")
    if not np.isfinite(coordinates).all():
        raise ValueError("coordinates must be finite")
    try:
        source=CRS.from_user_input(source_crs)
        target=CRS.from_user_input(target_crs)
        transformer=Transformer.from_crs(source,target,always_xy=True)
        x,y=transformer.transform(coordinates[:,0],coordinates[:,1],errcheck=True)
    except (ProjError,ValueError,TypeError) as error:
        raise ValueError(f"coordinate transformation failed: {error}") from error
    result=np.column_stack([x,y]).astype(float)
    if not np.isfinite(result).all():
        raise ValueError("coordinate transformation produced non-finite output")
    return result


def _geod_from_ellipsoid(ellipsoid="WGS84"):
    """Build a PROJ geodesic calculator from a CRS or ellipsoid definition."""
    try:
        crs = CRS.from_user_input(ellipsoid)
        geod = crs.get_geod() if crs.is_geographic else crs.geodetic_crs.get_geod()
        if geod is not None:
            return geod
    except (ProjError, ValueError, TypeError, AttributeError):
        pass
    try:
        return Geod(ellps=str(ellipsoid))
    except (ProjError, ValueError, TypeError, KeyError) as error:
        raise ValueError(f"invalid ellipsoid or CRS: {error}") from error


def geodesic_inverse(points_a, points_b, *, ellipsoid="WGS84") -> dict:
    """Solve ellipsoidal inverse geodesics for matching lon/lat degree arrays.

    Returns forward azimuth at the first point, back azimuth at the second
    point (degrees clockwise from north) and ellipsoidal distance in metres.
    Karney's robust geodesic solver is supplied by PROJ.
    """
    a = np.asarray(points_a, dtype=float)
    b = np.asarray(points_b, dtype=float)
    if a.shape != b.shape or a.ndim != 2 or a.shape[1] != 2 or len(a) == 0:
        raise ValueError("points_a and points_b must be matching non-empty N×2 arrays")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("geographic coordinates must be finite")
    if np.any(np.abs(a[:, 1]) > 90) or np.any(np.abs(b[:, 1]) > 90):
        raise ValueError("latitude must lie within [-90, 90] degrees")
    geod = _geod_from_ellipsoid(ellipsoid)
    try:
        az12, az21, distance = geod.inv(a[:, 0], a[:, 1], b[:, 0], b[:, 1])
    except (ProjError, ValueError, TypeError) as error:
        raise ValueError(f"inverse geodesic failed: {error}") from error
    return {"forward_azimuth_degrees": np.asarray(az12),
            "back_azimuth_degrees": np.asarray(az21),
            "distance_metres": np.asarray(distance)}


def geodesic_direct(points, azimuth_degrees, distance_metres, *, ellipsoid="WGS84") -> np.ndarray:
    """Solve direct ellipsoidal geodesics for lon/lat, azimuth and distance arrays."""
    coordinates = np.asarray(points, dtype=float)
    azimuth = np.asarray(azimuth_degrees, dtype=float)
    distance = np.asarray(distance_metres, dtype=float)
    if coordinates.ndim != 2 or coordinates.shape[1] != 2 or len(coordinates) == 0:
        raise ValueError("points must be a non-empty N×2 lon/lat array")
    try:
        azimuth = np.broadcast_to(azimuth, (len(coordinates),))
        distance = np.broadcast_to(distance, (len(coordinates),))
    except ValueError:
        raise ValueError("azimuth and distance must be scalar or match point count") from None
    if not np.isfinite(coordinates).all() or not np.isfinite(azimuth).all() or not np.isfinite(distance).all():
        raise ValueError("coordinates, azimuths and distances must be finite")
    if np.any(np.abs(coordinates[:, 1]) > 90) or np.any(distance < 0):
        raise ValueError("latitude must be within [-90, 90] and distance nonnegative")
    geod = _geod_from_ellipsoid(ellipsoid)
    try:
        lon, lat, _ = geod.fwd(coordinates[:, 0], coordinates[:, 1], azimuth, distance)
    except (ProjError, ValueError, TypeError) as error:
        raise ValueError(f"direct geodesic failed: {error}") from error
    return np.column_stack((lon, lat))


def geodesic_polygon_area(ring, *, ellipsoid="WGS84", signed=False) -> dict:
    """Compute ellipsoidal polygon area and perimeter from a lon/lat ring.

    The ring may be open or closed. The returned area is square metres and
    perimeter metres. By default area is the smaller unsigned region; signed
    mode preserves orientation according to the geodesic library convention.
    """
    coordinates = np.asarray(ring, dtype=float)
    if coordinates.ndim != 2 or coordinates.shape[1] != 2 or len(coordinates) < 3:
        raise ValueError("ring must contain at least three lon/lat coordinate pairs")
    if not np.isfinite(coordinates).all() or np.any(np.abs(coordinates[:, 1]) > 90):
        raise ValueError("ring coordinates must be finite with latitude in [-90, 90]")
    if len(coordinates) > 1 and np.allclose(coordinates[0], coordinates[-1]):
        coordinates = coordinates[:-1]
    if len(coordinates) < 3:
        raise ValueError("ring must contain at least three distinct vertices")
    geod = _geod_from_ellipsoid(ellipsoid)
    try:
        area, perimeter = geod.polygon_area_perimeter(coordinates[:, 0], coordinates[:, 1])
    except (ProjError, ValueError, TypeError) as error:
        raise ValueError(f"geodesic polygon calculation failed: {error}") from error
    return {"area_square_metres": float(area if signed else abs(area)),
            "signed_area_square_metres": float(area),
            "perimeter_metres": float(perimeter)}


def geodesic_point_buffer(center, radius_metres, *, vertices=72, ellipsoid="WGS84") -> np.ndarray:
    """Approximate an ellipsoidal geodesic-radius buffer as a lon/lat ring.

    Vertices are placed at equal azimuth increments using the ellipsoidal
    direct solution. Longitudes are returned in PROJ's normalized range,
    supporting buffers that cross the antimeridian. This is a sampled boundary,
    not an exact analytic polygon or a topology-aware geometry buffer.
    """
    point = np.asarray(center, dtype=float)
    if point.shape != (2,) or not np.isfinite(point).all() or abs(point[1]) > 90:
        raise ValueError("center must be a finite (longitude, latitude) pair")
    radius = float(radius_metres)
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("radius_metres must be finite and positive")
    if isinstance(vertices, (bool, np.bool_)) or not isinstance(vertices, (int, np.integer)) or vertices < 8:
        raise ValueError("vertices must be an integer of at least eight")
    azimuths = np.linspace(0.0, 360.0, int(vertices), endpoint=False)
    points = np.repeat(point[None, :], int(vertices), axis=0)
    return geodesic_direct(points, azimuths, np.full(int(vertices), radius), ellipsoid=ellipsoid)

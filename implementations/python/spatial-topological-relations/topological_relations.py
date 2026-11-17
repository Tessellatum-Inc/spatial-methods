"""DE-9IM and RCC-8 topological relations for planar polygonal regions."""
from __future__ import annotations

from typing import Literal
from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry

RCC8 = Literal["DC", "EC", "PO", "EQ", "TPP", "NTPP", "TPPi", "NTPPi"]
_ALLOWED = {"DC", "EC", "PO", "EQ", "TPP", "NTPP", "TPPi", "NTPPi"}


def _validate(geometry: BaseGeometry, name: str, *, regions_only: bool) -> None:
    if not isinstance(geometry, BaseGeometry):
        raise TypeError(f"{name} must be a Shapely geometry")
    if geometry.is_empty:
        raise ValueError(f"{name} must not be empty")
    if not geometry.is_valid:
        raise ValueError(f"{name} must be valid")
    if regions_only and not isinstance(geometry, (Polygon, MultiPolygon)):
        raise TypeError(f"{name} must be a Polygon or MultiPolygon region")


def de9im(a: BaseGeometry, b: BaseGeometry) -> str:
    """Return the nine-intersection matrix string for valid non-empty inputs."""
    _validate(a, "a", regions_only=False)
    _validate(b, "b", regions_only=False)
    return a.relate(b)


def rcc8(a: BaseGeometry, b: BaseGeometry) -> RCC8:
    """Classify the RCC-8 relation from region a to region b.

    Only valid planar Polygon and MultiPolygon inputs are accepted. A and B
    must use the same coordinate space and geometry-engine precision model.
    """
    _validate(a, "a", regions_only=True)
    _validate(b, "b", regions_only=True)
    if a.equals(b):
        return "EQ"
    if a.disjoint(b):
        return "DC"
    if a.touches(b):
        return "EC"
    if a.within(b):
        return "TPP" if a.boundary.intersects(b.boundary) else "NTPP"
    if a.contains(b):
        return "TPPi" if a.boundary.intersects(b.boundary) else "NTPPi"
    if a.overlaps(b):
        return "PO"
    raise ValueError("relation is outside the supported RCC-8 region cases")


CARDINAL_DIRECTIONS = {
    ("W", "S"): "SW", ("O", "S"): "S", ("E", "S"): "SE",
    ("W", "O"): "W",  ("O", "O"): "OVERLAPPING", ("E", "O"): "E",
    ("W", "N"): "NW", ("O", "N"): "N", ("E", "N"): "NE",
}


def cardinal_direction(a: BaseGeometry, b: BaseGeometry) -> str:
    """Return B's 9-region MBR direction relative to A.

    The relation compares axis-aligned minimum bounding rectangles. Touching
    interval endpoints count as directional separation. This is a qualitative
    bounding-box model, not a centroid bearing or a full directional calculus.
    """
    _validate(a, "a", regions_only=False)
    _validate(b, "b", regions_only=False)
    ax0, ay0, ax1, ay1 = a.bounds
    bx0, by0, bx1, by1 = b.bounds
    if bx0 >= ax1:
        x_relation = "E"
    elif bx1 <= ax0:
        x_relation = "W"
    else:
        x_relation = "O"
    if by0 >= ay1:
        y_relation = "N"
    elif by1 <= ay0:
        y_relation = "S"
    else:
        y_relation = "O"
    return CARDINAL_DIRECTIONS[(x_relation, y_relation)]

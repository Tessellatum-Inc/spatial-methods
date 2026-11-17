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

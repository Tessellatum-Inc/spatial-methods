"""Möller–Trumbore ray/triangle intersection reference implementation."""
from __future__ import annotations
from dataclasses import dataclass
from math import inf, isfinite
from typing import Sequence

Vec3 = tuple[float, float, float]

@dataclass(frozen=True)
class RayTriangleHit:
    """Intersection result; t is the parameter in origin + t * direction."""
    t: float
    u: float
    v: float
    w: float
    point: Vec3

def _vec3(value: Sequence[float], label: str) -> Vec3:
    if len(value) != 3:
        raise ValueError(f"{label} must contain exactly three coordinates")
    result = tuple(float(component) for component in value)
    if not all(isfinite(component) for component in result):
        raise ValueError(f"{label} must contain only finite coordinates")
    return result  # type: ignore[return-value]

def _sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def _add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def _scale(a: Vec3, k: float) -> Vec3:
    return (a[0]*k, a[1]*k, a[2]*k)

def _dot(a: Vec3, b: Vec3) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def intersect_ray_triangle(
    origin: Sequence[float],
    direction: Sequence[float],
    triangle: Sequence[Sequence[float]],
    *,
    t_min: float = 1e-9,
    t_max: float = inf,
    cull_backface: bool = False,
    epsilon: float = 1e-12,
) -> RayTriangleHit | None:
    """Intersect ray origin + t * direction with a triangle.

    t is a physical distance only when direction is unit length. Edges and
    vertices are included within epsilon. Degenerate and near-parallel cases
    return None. Back-face culling is opt-in.
    """
    o, d = _vec3(origin, "origin"), _vec3(direction, "direction")
    if len(triangle) != 3:
        raise ValueError("triangle must contain exactly three vertices")
    a, b, c = (_vec3(vertex, "triangle vertex") for vertex in triangle)
    if not (isfinite(t_min) and t_min >= 0):
        raise ValueError("t_min must be finite and non-negative")
    if not (t_max >= t_min):
        raise ValueError("t_max must be greater than or equal to t_min")
    if not (isfinite(epsilon) and epsilon >= 0):
        raise ValueError("epsilon must be finite and non-negative")
    e1, e2 = _sub(b, a), _sub(c, a)
    pvec = _cross(d, e2)
    determinant = _dot(e1, pvec)
    if cull_backface:
        if determinant <= epsilon:
            return None
    elif abs(determinant) <= epsilon:
        return None
    inverse = 1.0 / determinant
    offset = _sub(o, a)
    u = _dot(offset, pvec) * inverse
    if u < -epsilon or u > 1.0 + epsilon:
        return None
    qvec = _cross(offset, e1)
    v = _dot(d, qvec) * inverse
    if v < -epsilon or u + v > 1.0 + epsilon:
        return None
    t = _dot(e2, qvec) * inverse
    if t < t_min or t > t_max:
        return None
    return RayTriangleHit(t, u, v, 1.0-u-v, _add(o, _scale(d, t)))

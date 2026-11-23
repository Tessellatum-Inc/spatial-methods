"""Boundary-representation Boolean operations using a binary space partition tree.

This is a compact CSG teaching implementation. Inputs are closed collections
of convex, planar polygons with consistent outward winding. Floating-point
classification uses an explicit tolerance; this is not an exact-predicate
or production mesh Boolean kernel.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable

Vec3 = tuple[float, float, float]
COPLANAR, FRONT, BACK, SPANNING = 0, 1, 2, 3


def _add(a: Vec3, b: Vec3) -> Vec3:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def _sub(a: Vec3, b: Vec3) -> Vec3:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def _scale(a: Vec3, s: float) -> Vec3:
    return a[0] * s, a[1] * s, a[2] * s


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def _length(a: Vec3) -> float:
    return sqrt(_dot(a, a))


def _unit(a: Vec3) -> Vec3:
    length = _length(a)
    if length == 0:
        raise ValueError("A polygon plane needs three non-collinear vertices.")
    return _scale(a, 1.0 / length)


@dataclass(frozen=True)
class Vertex:
    pos: Vec3

    def interpolate(self, other: "Vertex", t: float) -> "Vertex":
        return Vertex(_add(self.pos, _scale(_sub(other.pos, self.pos), t)))


@dataclass(frozen=True)
class Plane:
    normal: Vec3
    w: float

    @classmethod
    def from_vertices(cls, vertices: tuple[Vertex, ...], tolerance: float) -> "Plane":
        if len(vertices) < 3:
            raise ValueError("A polygon needs at least three vertices.")
        origin = vertices[0].pos
        normal = None
        for i in range(1, len(vertices) - 1):
            candidate = _cross(_sub(vertices[i].pos, origin),
                               _sub(vertices[i + 1].pos, origin))
            if _length(candidate) > tolerance:
                normal = _unit(candidate)
                break
        if normal is None:
            raise ValueError("Polygon vertices are collinear or degenerate.")
        w = _dot(normal, origin)
        if any(abs(_dot(normal, v.pos) - w) > tolerance for v in vertices):
            raise ValueError("Polygon vertices are not coplanar.")
        return cls(normal, w)


@dataclass(frozen=True)
class Polygon:
    vertices: tuple[Vertex, ...]
    plane: Plane

    @classmethod
    def from_points(cls, points: Iterable[Iterable[float]],
                    tolerance: float = 1e-8) -> "Polygon":
        vertices = tuple(Vertex(tuple(float(c) for c in p)) for p in points)
        if any(len(v.pos) != 3 for v in vertices):
            raise ValueError("Every vertex must have three coordinates.")
        if len(vertices) > 1 and _length(_sub(vertices[0].pos, vertices[-1].pos)) <= tolerance:
            vertices = vertices[:-1]
        if len(vertices) < 3:
            raise ValueError("A polygon needs at least three vertices.")
        if any(not all(abs(c) < float("inf") for c in v.pos) for v in vertices):
            raise ValueError("Coordinates must be finite.")
        plane = Plane.from_vertices(vertices, tolerance)
        turns = []
        for i in range(len(vertices)):
            a, b, c = (vertices[i - 1].pos, vertices[i].pos,
                       vertices[(i + 1) % len(vertices)].pos)
            turn = _dot(_cross(_sub(b, a), _sub(c, b)), plane.normal)
            if abs(turn) > tolerance:
                turns.append(turn)
        if not turns or (min(turns) < -tolerance and max(turns) > tolerance):
            raise ValueError("BSP input polygons must be convex and consistently wound.")
        return cls(vertices, plane)


class _Node:
    def __init__(self, polygons: Iterable[Polygon] = (), tolerance: float = 1e-8):
        self.tolerance = tolerance
        self.plane: Plane | None = None
        self.front: _Node | None = None
        self.back: _Node | None = None
        self.polygons: list[Polygon] = []
        values = list(polygons)
        if values:
            self.build(values)

    def clone(self) -> "_Node":
        node = _Node(tolerance=self.tolerance)
        node.plane = self.plane
        node.front = self.front.clone() if self.front else None
        node.back = self.back.clone() if self.back else None
        node.polygons = self.polygons.copy()
        return node

    def invert(self) -> None:
        self.polygons = [Polygon(tuple(reversed(p.vertices)),
                                 Plane(_scale(p.plane.normal, -1), -p.plane.w))
                         for p in self.polygons]
        if self.plane:
            self.plane = Plane(_scale(self.plane.normal, -1), -self.plane.w)
        if self.front:
            self.front.invert()
        if self.back:
            self.back.invert()
        self.front, self.back = self.back, self.front

    def _split(self, splitter: Plane, polygon: Polygon,
               coplanar_front: list[Polygon], coplanar_back: list[Polygon],
               front: list[Polygon], back: list[Polygon]) -> None:
        types = []
        polygon_type = 0
        for vertex in polygon.vertices:
            t = _dot(splitter.normal, vertex.pos) - splitter.w
            kind = BACK if t < -self.tolerance else FRONT if t > self.tolerance else COPLANAR
            polygon_type |= kind
            types.append(kind)
        if polygon_type == COPLANAR:
            target = coplanar_front if _dot(splitter.normal, polygon.plane.normal) > 0 else coplanar_back
            target.append(polygon)
        elif polygon_type == FRONT:
            front.append(polygon)
        elif polygon_type == BACK:
            back.append(polygon)
        elif polygon_type == SPANNING:
            f: list[Vertex] = []
            b: list[Vertex] = []
            count = len(polygon.vertices)
            for i, vi in enumerate(polygon.vertices):
                j = (i + 1) % count
                vj = polygon.vertices[j]
                ti, tj = types[i], types[j]
                if ti != BACK:
                    f.append(vi)
                if ti != FRONT:
                    b.append(vi)
                if (ti | tj) == SPANNING:
                    direction = _sub(vj.pos, vi.pos)
                    denominator = _dot(splitter.normal, direction)
                    if abs(denominator) <= self.tolerance:
                        raise ArithmeticError("Unstable BSP edge-plane intersection.")
                    t = (splitter.w - _dot(splitter.normal, vi.pos)) / denominator
                    v = vi.interpolate(vj, t)
                    f.append(v)
                    b.append(v)
            if len(f) >= 3:
                front.append(Polygon(tuple(f), Plane.from_vertices(tuple(f), self.tolerance)))
            if len(b) >= 3:
                back.append(Polygon(tuple(b), Plane.from_vertices(tuple(b), self.tolerance)))

    def clip_polygons(self, polygons: list[Polygon]) -> list[Polygon]:
        if self.plane is None:
            return polygons.copy()
        front: list[Polygon] = []
        back: list[Polygon] = []
        for polygon in polygons:
            self._split(self.plane, polygon, front, back, front, back)
        if self.front:
            front = self.front.clip_polygons(front)
        if self.back:
            back = self.back.clip_polygons(back)
        else:
            back = []
        return front + back

    def clip_to(self, other: "_Node") -> None:
        self.polygons = other.clip_polygons(self.polygons)
        if self.front:
            self.front.clip_to(other)
        if self.back:
            self.back.clip_to(other)

    def all_polygons(self) -> list[Polygon]:
        result = self.polygons.copy()
        if self.front:
            result.extend(self.front.all_polygons())
        if self.back:
            result.extend(self.back.all_polygons())
        return result

    def build(self, polygons: list[Polygon]) -> None:
        if not polygons:
            return
        if self.plane is None:
            self.plane = polygons[0].plane
        front: list[Polygon] = []
        back: list[Polygon] = []
        for polygon in polygons:
            self._split(self.plane, polygon, self.polygons, self.polygons, front, back)
        if front:
            if self.front is None:
                self.front = _Node(tolerance=self.tolerance)
            self.front.build(front)
        if back:
            if self.back is None:
                self.back = _Node(tolerance=self.tolerance)
            self.back.build(back)


def _prepare(polygons: Iterable[Polygon], tolerance: float) -> list[Polygon]:
    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")
    values = list(polygons)
    if not values:
        raise ValueError("Each solid must contain at least one polygon.")
    return values


def union(a: Iterable[Polygon], b: Iterable[Polygon],
          tolerance: float = 1e-8) -> list[Polygon]:
    """Return the boundary polygons of A ∪ B (convex polygon soup inputs)."""
    an, bn = _Node(_prepare(a, tolerance), tolerance), _Node(_prepare(b, tolerance), tolerance)
    an.clip_to(bn)
    bn.clip_to(an)
    bn.invert()
    bn.clip_to(an)
    bn.invert()
    an.build(bn.all_polygons())
    return an.all_polygons()


def intersection(a: Iterable[Polygon], b: Iterable[Polygon],
                 tolerance: float = 1e-8) -> list[Polygon]:
    """Return the boundary polygons of A ∩ B (convex polygon soup inputs)."""
    an, bn = _Node(_prepare(a, tolerance), tolerance), _Node(_prepare(b, tolerance), tolerance)
    an.invert()
    bn.clip_to(an)
    bn.invert()
    an.clip_to(bn)
    bn.clip_to(an)
    an.build(bn.all_polygons())
    an.invert()
    return an.all_polygons()


def difference(a: Iterable[Polygon], b: Iterable[Polygon],
               tolerance: float = 1e-8) -> list[Polygon]:
    """Return the boundary polygons of A \\ B (convex polygon soup inputs)."""
    an, bn = _Node(_prepare(a, tolerance), tolerance), _Node(_prepare(b, tolerance), tolerance)
    an.invert()
    an.clip_to(bn)
    bn.clip_to(an)
    bn.invert()
    bn.clip_to(an)
    bn.invert()
    an.build(bn.all_polygons())
    an.invert()
    return an.all_polygons()


def box(minimum: Vec3, maximum: Vec3) -> list[Polygon]:
    """Create an outward-wound axis-aligned box from strict min/max corners."""
    x0, y0, z0 = minimum
    x1, y1, z1 = maximum
    if not (x0 < x1 and y0 < y1 and z0 < z1):
        raise ValueError("Box maximum coordinates must exceed minimum coordinates.")
    faces = [
        [(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)],
        [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],
        [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],
        [(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)],
        [(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)],
        [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
    ]
    return [Polygon.from_points(face) for face in faces]

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


@dataclass(frozen=True)
class AABB:
    """Axis-aligned bounds in the same Cartesian frame as the mesh."""
    minimum: Vec3
    maximum: Vec3

    @classmethod
    def from_triangle(cls, triangle: tuple[Vec3, Vec3, Vec3]) -> "AABB":
        return cls(
            tuple(min(v[a] for v in triangle) for a in range(3)),  # type: ignore[arg-type]
            tuple(max(v[a] for v in triangle) for a in range(3)),  # type: ignore[arg-type]
        )

    @classmethod
    def union(cls, boxes: Sequence["AABB"]) -> "AABB":
        if not boxes:
            raise ValueError("at least one box is required")
        return cls(
            tuple(min(b.minimum[a] for b in boxes) for a in range(3)),  # type: ignore[arg-type]
            tuple(max(b.maximum[a] for b in boxes) for a in range(3)),  # type: ignore[arg-type]
        )

    @property
    def centroid(self) -> Vec3:
        return tuple((self.minimum[a] + self.maximum[a]) / 2 for a in range(3))  # type: ignore[return-value]

    @property
    def surface_area(self) -> float:
        x, y, z = (max(0.0, self.maximum[a] - self.minimum[a]) for a in range(3))
        return 2.0 * (x*y + y*z + z*x)

    def intersect_ray(
        self, origin: Vec3, direction: Vec3,
        t_min: float = 0.0, t_max: float = inf,
    ) -> tuple[float, float] | None:
        """Return the ray-parameter interval clipped to this box."""
        near, far = t_min, t_max
        for axis in range(3):
            o, d = origin[axis], direction[axis]
            low, high = self.minimum[axis], self.maximum[axis]
            if d == 0.0:
                if o < low or o > high:
                    return None
                continue
            t0, t1 = (low-o)/d, (high-o)/d
            if t0 > t1:
                t0, t1 = t1, t0
            near, far = max(near, t0), min(far, t1)
            if near > far:
                return None
        return near, far


@dataclass(frozen=True)
class BVHNode:
    bounds: AABB
    left: "BVHNode | None" = None
    right: "BVHNode | None" = None
    triangle_indices: tuple[int, ...] = ()

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def _as_triangle(value: Sequence[Sequence[float]]) -> tuple[Vec3, Vec3, Vec3]:
    if len(value) != 3:
        raise ValueError("each triangle must contain exactly three vertices")
    return tuple(_vec3(vertex, "triangle vertex") for vertex in value)  # type: ignore[return-value]


def build_bvh(
    triangles: Sequence[Sequence[Sequence[float]]], *, leaf_size: int = 4,
) -> BVHNode | None:
    """Build a deterministic binary BVH with exact-centroid SAH split scans.

    Every centroid split on each axis is evaluated. This transparent builder
    favours reproducibility and inspectability over production build speed;
    binned SAH is preferable for large meshes.
    """
    if leaf_size < 1:
        raise ValueError("leaf_size must be at least one")
    tris = tuple(_as_triangle(t) for t in triangles)
    if not tris:
        return None
    boxes = tuple(AABB.from_triangle(t) for t in tris)
    centres = tuple(box.centroid for box in boxes)

    def build(indices: tuple[int, ...]) -> BVHNode:
        bounds = AABB.union([boxes[i] for i in indices])
        if len(indices) <= leaf_size:
            return BVHNode(bounds=bounds, triangle_indices=indices)
        leaf_cost = bounds.surface_area * len(indices)
        best_cost = inf
        best_split: tuple[tuple[int, ...], tuple[int, ...]] | None = None
        for axis in range(3):
            ordered = tuple(sorted(indices, key=lambda i: (centres[i][axis], i)))
            prefix: list[AABB] = []
            running: list[AABB] = []
            for index in ordered:
                running.append(boxes[index])
                prefix.append(AABB.union(running))
            suffix: list[AABB | None] = [None] * len(ordered)
            running = []
            for pos in range(len(ordered)-1, -1, -1):
                running.append(boxes[ordered[pos]])
                suffix[pos] = AABB.union(running)
            for split in range(1, len(ordered)):
                left, right = ordered[:split], ordered[split:]
                right_bounds = suffix[split]
                assert right_bounds is not None
                cost = prefix[split-1].surface_area*len(left) + right_bounds.surface_area*len(right)
                if cost < best_cost:
                    best_cost, best_split = cost, (left, right)
        if best_split is None or best_cost >= leaf_cost:
            return BVHNode(bounds=bounds, triangle_indices=indices)
        return BVHNode(bounds=bounds, left=build(best_split[0]), right=build(best_split[1]))

    return build(tuple(range(len(tris))))


def intersect_bvh(
    root: BVHNode | None,
    triangles: Sequence[Sequence[Sequence[float]]],
    origin: Sequence[float],
    direction: Sequence[float],
    *,
    t_min: float = 1e-9,
    t_max: float = inf,
    cull_backface: bool = False,
) -> tuple[int, RayTriangleHit] | None:
    """Return (input triangle index, nearest hit) using near-first traversal."""
    if root is None:
        return None
    o, d = _vec3(origin, "origin"), _vec3(direction, "direction")
    tris = tuple(_as_triangle(t) for t in triangles)
    if not tris:
        return None
    if any(i < 0 or i >= len(tris) for i in _leaf_triangle_indices(root)):
        raise ValueError("BVH contains an index outside the supplied triangle sequence")
    interval = root.bounds.intersect_ray(o, d, t_min, t_max)
    if interval is None:
        return None
    best_t = t_max
    best: tuple[int, RayTriangleHit] | None = None
    stack: list[tuple[float, BVHNode]] = [(interval[0], root)]
    while stack:
        entry, node = stack.pop()
        if entry > best_t:
            continue
        if node.is_leaf:
            for index in node.triangle_indices:
                hit = intersect_ray_triangle(
                    o, d, tris[index], t_min=t_min, t_max=best_t,
                    cull_backface=cull_backface,
                )
                if hit is not None and hit.t < best_t:
                    best_t, best = hit.t, (index, hit)
            continue
        children: list[tuple[float, BVHNode]] = []
        for child in (node.left, node.right):
            if child is not None:
                child_interval = child.bounds.intersect_ray(o, d, t_min, best_t)
                if child_interval is not None:
                    children.append((child_interval[0], child))
        children.sort(key=lambda item: item[0], reverse=True)
        stack.extend(children)
    return best


def _leaf_triangle_indices(node: BVHNode) -> tuple[int, ...]:
    if node.is_leaf:
        return node.triangle_indices
    indices: list[int] = []
    if node.left is not None:
        indices.extend(_leaf_triangle_indices(node.left))
    if node.right is not None:
        indices.extend(_leaf_triangle_indices(node.right))
    return tuple(indices)

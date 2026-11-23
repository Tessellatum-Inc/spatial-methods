"""Winged-edge topology for consistently oriented polygon meshes."""
from dataclasses import dataclass
from collections import defaultdict
from collections.abc import Sequence


@dataclass(frozen=True)
class WingedEdge:
    vertices: tuple[int, int]       # canonical endpoint order (low, high)
    left_face: int | None
    right_face: int | None
    left_prev: tuple[int, int] | None
    left_next: tuple[int, int] | None
    right_prev: tuple[int, int] | None
    right_next: tuple[int, int] | None


@dataclass(frozen=True)
class WingedEdgeMesh:
    vertex_count: int
    faces: tuple[tuple[int, ...], ...]
    edges: tuple[WingedEdge, ...]

    @classmethod
    def from_faces(cls, vertex_count: int,
                   faces: Sequence[Sequence[int]]) -> "WingedEdgeMesh":
        if not isinstance(vertex_count, int) or vertex_count < 0:
            raise ValueError("vertex_count must be a non-negative integer")
        normalized, seen = [], set()
        incidence = defaultdict(list)
        for fi, face in enumerate(faces):
            face = tuple(face)
            if len(face) < 3:
                raise ValueError(f"face {fi} must have at least three vertices")
            if any(not isinstance(v, int) or v < 0 or v >= vertex_count for v in face):
                raise ValueError(f"face {fi} has an out-of-range vertex")
            if len(set(face)) != len(face):
                raise ValueError(f"face {fi} repeats a vertex")
            key = tuple(sorted(face))
            if key in seen:
                raise ValueError("duplicate faces are not allowed")
            seen.add(key)
            normalized.append(face)
            for i, u in enumerate(face):
                v = face[(i + 1) % len(face)]
                edge = tuple(sorted((u, v)))
                incidence[edge].append((fi, u, v))
        edges = []
        for (lo, hi), uses in sorted(incidence.items()):
            if len(uses) > 2:
                raise ValueError(f"edge {(lo, hi)} is non-manifold")
            if len(uses) == 2 and uses[0][1:] != uses[1][1:][::-1]:
                raise ValueError(f"edge {(lo, hi)} has inconsistent face winding")
            left = right = None
            left_prev = left_next = right_prev = right_next = None
            for fi, u, v in uses:
                face = normalized[fi]
                i = next(i for i in range(len(face))
                         if face[i] == u and face[(i+1) % len(face)] == v)
                prev_edge = tuple(sorted((face[i-1], u)))
                next_edge = tuple(sorted((v, face[(i+2) % len(face)])))
                if (u, v) == (lo, hi):
                    left, left_prev, left_next = fi, prev_edge, next_edge
                else:
                    right, right_prev, right_next = fi, prev_edge, next_edge
            edges.append(WingedEdge((lo, hi), left, right,
                                    left_prev, left_next,
                                    right_prev, right_next))
        return cls(vertex_count, tuple(normalized), tuple(edges))

    def edge(self, u: int, v: int) -> WingedEdge:
        key = tuple(sorted((u, v)))
        for edge in self.edges:
            if edge.vertices == key:
                return edge
        raise KeyError(key)

    def incident_edges(self, vertex: int) -> tuple[WingedEdge, ...]:
        if not 0 <= vertex < self.vertex_count:
            raise IndexError(vertex)
        return tuple(e for e in self.edges if vertex in e.vertices)

    def boundary_edges(self) -> tuple[WingedEdge, ...]:
        return tuple(e for e in self.edges
                     if (e.left_face is None) != (e.right_face is None))

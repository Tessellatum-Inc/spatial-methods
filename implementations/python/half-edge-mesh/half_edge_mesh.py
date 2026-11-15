"""Indexed half-edge topology for oriented triangular surface meshes.

This module builds a manifold-with-boundary half-edge structure from a
triangle soup. It does not repair non-manifold input or infer missing faces.
"""
from dataclasses import dataclass
from collections import defaultdict
from collections.abc import Sequence


@dataclass(frozen=True)
class HalfEdge:
    origin: int
    face: int
    next: int
    prev: int
    twin: int | None


@dataclass(frozen=True)
class HalfEdgeMesh:
    vertex_count: int
    faces: tuple[tuple[int, int, int], ...]
    halfedges: tuple[HalfEdge, ...]
    face_edge: tuple[int, ...]
    vertex_edge: tuple[int | None, ...]

    @classmethod
    def from_triangles(cls, vertex_count: int,
                       faces: Sequence[Sequence[int]]) -> "HalfEdgeMesh":
        """Build topology; boundary edges have twin=None.

        Every undirected edge may occur once (boundary) or twice (interior).
        Two incident faces must traverse a shared edge in opposite directions.
        """
        if not isinstance(vertex_count, int) or vertex_count < 0:
            raise ValueError("vertex_count must be a non-negative integer")
        normalized = []
        seen_faces = set()
        for fi, face in enumerate(faces):
            if len(face) != 3:
                raise ValueError(f"face {fi} is not triangular")
            tri = tuple(face)
            if any(not isinstance(v, int) or v < 0 or v >= vertex_count for v in tri):
                raise ValueError(f"face {fi} has an out-of-range vertex")
            if len(set(tri)) != 3:
                raise ValueError(f"face {fi} repeats a vertex")
            canonical = tuple(sorted(tri))
            if canonical in seen_faces:
                raise ValueError("duplicate geometric faces are not allowed")
            seen_faces.add(canonical)
            normalized.append(tri)

        # First create each face's directed cycle.
        origins, face_ids, nxt, prv = [], [], [], []
        undirected = defaultdict(list)
        face_edge = []
        vertex_edge = [None] * vertex_count
        for fi, tri in enumerate(normalized):
            base = len(origins)
            face_edge.append(base)
            for k, u in enumerate(tri):
                v = tri[(k + 1) % 3]
                undirected[tuple(sorted((u, v)))].append((u, v, base + k))
                origins.append(u)
                face_ids.append(fi)
                nxt.append(base + (k + 1) % 3)
                prv.append(base + (k - 1) % 3)
                if vertex_edge[u] is None:
                    vertex_edge[u] = base + k

        twins = [None] * len(origins)
        for edge, incidents in undirected.items():
            if len(incidents) > 2:
                raise ValueError(f"non-manifold edge {edge} has more than two incident faces")
            if len(incidents) == 2:
                u1, v1, h1 = incidents[0]
                u2, v2, h2 = incidents[1]
                if (u1, v1) != (v2, u2):
                    raise ValueError(f"faces have inconsistent winding at edge {edge}")
                twins[h1], twins[h2] = h2, h1

        halfedges = tuple(HalfEdge(origins[i], face_ids[i], nxt[i], prv[i], twins[i])
                          for i in range(len(origins)))
        mesh = cls(vertex_count, tuple(normalized), halfedges,
                   tuple(face_edge), tuple(vertex_edge))
        mesh.validate()
        return mesh

    def destination(self, halfedge_index: int) -> int:
        """Return the destination vertex of a directed half-edge."""
        self._check_halfedge(halfedge_index)
        return self.halfedges[self.halfedges[halfedge_index].next].origin

    def face_cycle(self, face_index: int) -> tuple[int, ...]:
        """Return half-edge indices around a face in its input orientation."""
        if not 0 <= face_index < len(self.faces):
            raise IndexError("face index out of range")
        start = self.face_edge[face_index]
        cycle, current = [], start
        while True:
            cycle.append(current)
            current = self.halfedges[current].next
            if current == start:
                return tuple(cycle)
            if len(cycle) > 3:
                raise ValueError("corrupt face cycle")

    def boundary_edges(self) -> tuple[int, ...]:
        return tuple(i for i, edge in enumerate(self.halfedges) if edge.twin is None)

    def adjacent_faces(self, face_index: int) -> tuple[int, ...]:
        neighbours = set()
        for h in self.face_cycle(face_index):
            twin = self.halfedges[h].twin
            if twin is not None:
                neighbours.add(self.halfedges[twin].face)
        return tuple(sorted(neighbours))

    def incident_faces(self, vertex_index: int) -> tuple[int, ...]:
        if not 0 <= vertex_index < self.vertex_count:
            raise IndexError("vertex index out of range")
        return tuple(i for i, face in enumerate(self.faces) if vertex_index in face)

    def _check_halfedge(self, index: int) -> None:
        if not isinstance(index, int) or not 0 <= index < len(self.halfedges):
            raise IndexError("half-edge index out of range")

    def validate(self) -> None:
        """Check local pointer, twin symmetry, face cycles and vertex references."""
        n = len(self.halfedges)
        if len(self.face_edge) != len(self.faces) or len(self.vertex_edge) != self.vertex_count:
            raise ValueError("index arrays have inconsistent lengths")
        for i, h in enumerate(self.halfedges):
            if not (0 <= h.origin < self.vertex_count and 0 <= h.face < len(self.faces)):
                raise ValueError(f"half-edge {i} has invalid origin or face")
            if not (0 <= h.next < n and 0 <= h.prev < n):
                raise ValueError(f"half-edge {i} has invalid next/prev")
            if self.halfedges[h.next].prev != i or self.halfedges[h.prev].next != i:
                raise ValueError(f"half-edge {i} violates next/prev reciprocity")
            if self.halfedges[h.next].face != h.face or self.halfedges[h.prev].face != h.face:
                raise ValueError(f"half-edge {i} crosses a face cycle")
            if h.twin is not None:
                self._check_halfedge(h.twin)
                t = self.halfedges[h.twin]
                if t.twin != i or t.origin != self.destination(i) or self.destination(h.twin) != h.origin:
                    raise ValueError(f"half-edge {i} has an invalid twin")
        for fi in range(len(self.faces)):
            cycle = self.face_cycle(fi)
            if len(cycle) != 3 or any(self.halfedges[h].face != fi for h in cycle):
                raise ValueError(f"face {fi} does not have a triangular cycle")
        for vi, h in enumerate(self.vertex_edge):
            if h is not None and self.halfedges[h].origin != vi:
                raise ValueError(f"vertex {vi} outgoing-edge reference is invalid")

        # Build each vertex link in one pass over the faces. The link of a
        # manifold vertex is one connected path (boundary) or cycle (interior).
        links = [{} for _ in range(self.vertex_count)]
        for tri in self.faces:
            for i, vi in enumerate(tri):
                a, b = tri[(i + 1) % 3], tri[(i + 2) % 3]
                links[vi].setdefault(a, set()).add(b)
                links[vi].setdefault(b, set()).add(a)
        for vi, link in enumerate(links):
            if not link:  # isolated vertex
                continue
            degrees = [len(neighbours) for neighbours in link.values()]
            endpoints = sum(degree == 1 for degree in degrees)
            if any(degree not in (1, 2) for degree in degrees) or endpoints not in (0, 2):
                raise ValueError(f"vertex {vi} has a non-manifold link")
            start = next(iter(link))
            seen, stack = set(), [start]
            while stack:
                node = stack.pop()
                if node not in seen:
                    seen.add(node)
                    stack.extend(link[node] - seen)
            if len(seen) != len(link):
                raise ValueError(f"vertex {vi} has a disconnected (non-manifold) link")

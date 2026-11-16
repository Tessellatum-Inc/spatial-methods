"""DCEL builder for already-noded polygonal planar subdivisions.

This module constructs topology; it is deliberately not a noder or Boolean
overlay engine. Input rings must be closed, simple and non-zero-area. Shared
edges must occur once per incident face in opposite directions.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
from math import isfinite
from typing import Hashable, Mapping, Sequence


def _q(p):
    return (Fraction(str(p[0])), Fraction(str(p[1])))


def _orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def _on_segment(a, b, p):
    return (_orient(a, b, p) == 0 and
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _segments_intersect(a, b, c, d):
    o1, o2, o3, o4 = _orient(a,b,c), _orient(a,b,d), _orient(c,d,a), _orient(c,d,b)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True
    return ((o1 == 0 and _on_segment(a,b,c)) or
            (o2 == 0 and _on_segment(a,b,d)) or
            (o3 == 0 and _on_segment(c,d,a)) or
            (o4 == 0 and _on_segment(c,d,b)))


def _angle_compare(origin, first, second, vertices, halfedges):
    """Exact CCW ordering of two outgoing half-edges around one vertex."""
    ox, oy = _q(origin)
    p1 = _q(vertices[halfedges[first].target].point)
    p2 = _q(vertices[halfedges[second].target].point)
    ax, ay = p1[0]-ox, p1[1]-oy
    bx, by = p2[0]-ox, p2[1]-oy
    ha = 0 if (ay > 0 or (ay == 0 and ax >= 0)) else 1
    hb = 0 if (by > 0 or (by == 0 and bx >= 0)) else 1
    if ha != hb:
        return -1 if ha < hb else 1
    cross = ax*by - ay*bx
    if cross:
        return -1 if cross > 0 else 1
    da, db = ax*ax + ay*ay, bx*bx + by*by
    return (da > db) - (da < db)


def _validate_noded_segments(segments):
    """Reject crossings, T-junctions and partial collinear overlaps.

    A DCEL constructor may accept already-noded shared vertices and shared
    edges, but it must not silently treat an un-noded segment arrangement as
    a valid planar subdivision. This O(E^2) validation is a correctness-first
    guard; large arrangements should be noded with a sweep-line algorithm.
    """
    unique = {}
    for a, b in segments:
        key = tuple(sorted((a, b)))
        unique[key] = (a, b)
    edges = list(unique.values())
    # Detect positive-length collinear overlaps before generic T-junction
    # checks, so the reported failure is stable regardless of edge order.
    for i, (a, b) in enumerate(edges):
        for c, d in edges[i + 1:]:
            if _orient(a, b, c) != 0 or _orient(a, b, d) != 0:
                continue
            axis = 0 if abs(b[0]-a[0]) >= abs(b[1]-a[1]) else 1
            overlap = min(max(a[axis], b[axis]), max(c[axis], d[axis])) - max(
                min(a[axis], b[axis]), min(c[axis], d[axis])
            )
            if overlap > 0:
                raise ValueError("Input boundaries must not contain partial collinear overlaps")
    for i, (a, b) in enumerate(edges):
        for c, d in edges[i + 1:]:
            if not _segments_intersect(a, b, c, d):
                continue
            shared = set((a, b)) & set((c, d))
            if _orient(a, b, c) == 0 and _orient(a, b, d) == 0:
                non_shared = (set((a, b)) | set((c, d))) - shared
                if not shared or any(
                    (p in (a, b) and _on_segment(c, d, p)) or
                    (p in (c, d) and _on_segment(a, b, p))
                    for p in non_shared
                ):
                    raise ValueError("Input boundaries must not contain partial collinear overlaps")
                continue
            if not shared:
                raise ValueError("Input boundaries must be noded: segments cross or form a T-junction")


def _validate_simple_ring(points):
    qpoints = [_q(p) for p in points[:-1]]
    area2 = sum(qpoints[i][0]*qpoints[(i+1)%len(qpoints)][1] -
                qpoints[(i+1)%len(qpoints)][0]*qpoints[i][1]
                for i in range(len(qpoints)))
    if area2 == 0:
        raise ValueError("Rings must have non-zero signed area")
    n = len(qpoints)
    for i in range(n):
        a, b = qpoints[i], qpoints[(i+1)%n]
        for j in range(i+1, n):
            # Consecutive edges (including first/last) meet at their shared endpoint.
            if j == i+1 or (i == 0 and j == n-1):
                continue
            c, d = qpoints[j], qpoints[(j+1)%n]
            if _segments_intersect(a,b,c,d):
                raise ValueError("Rings must be simple: non-adjacent edges intersect")


@dataclass
class Vertex:
    id: int
    point: tuple[float, float]
    outgoing: list[int]


@dataclass
class HalfEdge:
    id: int
    origin: int
    target: int
    twin: int
    next: int | None = None
    prev: int | None = None
    face: Hashable | None = None


@dataclass
class Face:
    id: Hashable
    boundary_cycles: list[int]


class DCEL:
    def __init__(self):
        self.vertices: list[Vertex] = []
        self.halfedges: list[HalfEdge] = []
        self.faces: dict[Hashable, Face] = {}
        self.unbounded_cycles: list[int] = []
        self.unbounded_face = Face(None, self.unbounded_cycles)
        self._vertex_by_point = {}

    def _vertex(self, p):
        if p not in self._vertex_by_point:
            i = len(self.vertices)
            self._vertex_by_point[p] = i
            self.vertices.append(Vertex(i, p, []))
        return self._vertex_by_point[p]

    @classmethod
    def from_faces(cls, faces: Mapping[Hashable, Sequence[Sequence[Sequence[float]]]]):
        d = cls()
        directed = {}
        input_segments = []
        for fid, rings in faces.items():
            if fid in d.faces:
                raise ValueError("Face identifiers must be unique")
            if not rings:
                raise ValueError("Each face needs at least one boundary ring")
            d.faces[fid] = Face(fid, [])
            for ring in rings:
                pts = []
                for p in ring:
                    if len(p) != 2:
                        raise ValueError("Coordinates must be x,y pairs")
                    x, y = float(p[0]), float(p[1])
                    if not isfinite(x) or not isfinite(y):
                        raise ValueError("Coordinates must be finite")
                    pts.append((x, y))
                if len(pts) < 4 or pts[0] != pts[-1]:
                    raise ValueError("Rings must be closed and contain at least three edges")
                core = pts[:-1]
                if len(set(core)) != len(core):
                    raise ValueError("Rings must not repeat vertices")
                _validate_simple_ring(pts)
                input_segments.extend(zip(core, core[1:] + core[:1]))
                ids = [d._vertex(p) for p in core]
                cycle = []
                for u, v in zip(ids, ids[1:] + ids[:1]):
                    key = (u, v)
                    if key in directed:
                        raise ValueError("Duplicate directed edge; shared boundaries must have opposite directions")
                    eid = len(d.halfedges)
                    directed[key] = eid
                    d.halfedges.append(HalfEdge(eid, u, v, -1, face=fid))
                    d.vertices[u].outgoing.append(eid)
                    cycle.append(eid)
                for j, eid in enumerate(cycle):
                    d.halfedges[eid].next = cycle[(j+1) % len(cycle)]
                    d.halfedges[eid].prev = cycle[j-1]
                d.faces[fid].boundary_cycles.append(cycle[0])

        _validate_noded_segments(input_segments)

        # Pair shared boundaries; unmatched edges receive exterior twins.
        for (u, v), eid in list(directed.items()):
            rev = directed.get((v, u))
            if rev is not None:
                d.halfedges[eid].twin = rev
            else:
                tid = len(d.halfedges)
                d.halfedges.append(HalfEdge(tid, v, u, eid))
                d.halfedges[eid].twin = tid
                d.vertices[v].outgoing.append(tid)

        # At each target, take the clockwise predecessor of the incoming edge's twin.
        # This keeps the unbounded face on the right and skips shared interior edges.
        for vertex in d.vertices:
            vertex.outgoing.sort(key=cmp_to_key(
                lambda first, second: _angle_compare(
                    vertex.point, first, second, d.vertices, d.halfedges
                )
            ))
        for edge in d.halfedges:
            if edge.face is None:
                outgoing = d.vertices[edge.target].outgoing
                twin_pos = outgoing.index(edge.twin)
                # Skip bounded-face half-edges in the angular fan: the
                # exterior boundary may pass a vertex where several bounded
                # faces meet, but it must remain on exterior half-edges.
                for offset in range(1, len(outgoing) + 1):
                    candidate = outgoing[(twin_pos-offset) % len(outgoing)]
                    if d.halfedges[candidate].face is None:
                        edge.next = candidate
                        break
                if edge.next is None:
                    raise ValueError("Exterior boundary has no successor at a vertex")
        for edge in d.halfedges:
            if edge.face is None:
                d.halfedges[edge.next].prev = edge.id

        seen = set()
        for edge in d.halfedges:
            if edge.face is not None or edge.id in seen:
                continue
            start, cur = edge.id, edge.id
            while cur not in seen:
                seen.add(cur)
                nxt = d.halfedges[cur].next
                if nxt is None:
                    raise ValueError("Incomplete exterior linkage")
                cur = nxt
            if cur != start:
                raise ValueError("Non-manifold or inconsistent ring junction")
            d.unbounded_cycles.append(start)
        d.validate()
        return d

    def validate(self):
        for edge in self.halfedges:
            if not (0 <= edge.twin < len(self.halfedges)):
                raise AssertionError("Missing twin")
            twin = self.halfedges[edge.twin]
            if twin.twin != edge.id or (edge.origin, edge.target) != (twin.target, twin.origin):
                raise AssertionError("Twin invariant failed")
            if edge.next is None or edge.prev is None:
                raise AssertionError("Incomplete next/prev")
            if self.halfedges[edge.next].prev != edge.id or self.halfedges[edge.prev].next != edge.id:
                raise AssertionError("Next/prev invariant failed")
        return True

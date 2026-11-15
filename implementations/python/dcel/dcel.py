"""Exact-coordinate DCEL builder for polygonal planar subdivisions.

Input faces are supplied as one or more closed boundary rings. Rings must be
simple, consistently non-overlapping, and shared boundaries must be encoded
once in each incident face with opposite direction. Coordinates are preserved
as supplied (converted to finite floats); this is a topology structure, not a
robust noding/arrangement constructor.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import atan2, isfinite, pi
from typing import Hashable, Mapping, Sequence

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
        self._vertex_by_point = {}

    def _vertex(self, p):
        if p not in self._vertex_by_point:
            i=len(self.vertices); self._vertex_by_point[p]=i
            self.vertices.append(Vertex(i,p,[]))
        return self._vertex_by_point[p]

    @classmethod
    def from_faces(cls, faces: Mapping[Hashable, Sequence[Sequence[Sequence[float]]]]):
        d=cls()
        directed={}
        pending=[]
        for fid,rings in faces.items():
            if fid in d.faces: raise ValueError("Face identifiers must be unique")
            if not rings: raise ValueError("Each face needs at least one boundary ring")
            d.faces[fid]=Face(fid,[])
            for ring in rings:
                pts=[]
                for p in ring:
                    if len(p)!=2: raise ValueError("Coordinates must be x,y pairs")
                    x,y=float(p[0]),float(p[1])
                    if not isfinite(x) or not isfinite(y): raise ValueError("Coordinates must be finite")
                    pts.append((x,y))
                if len(pts)<4 or pts[0]!=pts[-1]: raise ValueError("Rings must be closed and contain at least three edges")
                core=pts[:-1]
                if len(set(core))<3 or len(set(zip(core,core[1:]+core[:1])))!=len(core):
                    raise ValueError("Rings must not repeat vertices or zero-length edges")
                if any(core[i]==core[(i+1)%len(core)] for i in range(len(core))):
                    raise ValueError("Zero-length edges are not allowed")
                start=len(d.halfedges)
                ids=[d._vertex(p) for p in core]
                for i,(u,v) in enumerate(zip(ids,ids[1:]+ids[:1])):
                    key=(u,v)
                    if key in directed: raise ValueError("Duplicate directed edge; shared boundaries must have opposite directions")
                    eid=len(d.halfedges); directed[key]=eid
                    d.halfedges.append(HalfEdge(eid,u,v,-1,face=fid))
                    d.vertices[u].outgoing.append(eid)
                cycle=list(range(start,len(d.halfedges)))
                for j,eid in enumerate(cycle):
                    d.halfedges[eid].next=cycle[(j+1)%len(cycle)]
                    d.halfedges[eid].prev=cycle[j-1]
                d.faces[fid].boundary_cycles.append(start)
                pending.append((fid,cycle))
        # Pair opposite directed edges; create exterior twins for unpaired edges.
        for (u,v),eid in list(directed.items()):
            rev=directed.get((v,u))
            if rev is not None:
                d.halfedges[eid].twin=rev
            else:
                tid=len(d.halfedges)
                d.halfedges.append(HalfEdge(tid,v,u,eid))
                d.halfedges[eid].twin=tid
                d.vertices[v].outgoing.append(tid)
        # The predecessor of the twin in CCW order keeps the incident face left.
        for vertex in d.vertices:
            vertex.outgoing.sort(key=lambda e: atan2(
                d.vertices[d.halfedges[e].target].point[1]-vertex.point[1],
                d.vertices[d.halfedges[e].target].point[0]-vertex.point[0]))
        for e in d.halfedges:
            if e.face is not None: continue
            at=d.vertices[e.target].outgoing
            twin_pos=at.index(e.twin)
            e.next=at[(twin_pos-1)%len(at)]
        for e in d.halfedges:
            if e.face is None:
                d.halfedges[e.next].prev=e.id
        # Trace all unassigned twin cycles and label them as unbounded/exterior.
        seen=set()
        for e in d.halfedges:
            if e.face is not None or e.id in seen: continue
            start=e.id; cur=start; cycle=[]
            while cur not in seen:
                seen.add(cur); cycle.append(cur)
                nxt=d.halfedges[cur].next
                if nxt is None: raise ValueError("Incomplete exterior linkage")
                cur=nxt
            if cur!=start: raise ValueError("Non-manifold or inconsistent ring junction")
            d.unbounded_cycles.append(start)
        return d

    def validate(self):
        for e in self.halfedges:
            if not (0<=e.twin<len(self.halfedges)): raise AssertionError("Missing twin")
            t=self.halfedges[e.twin]
            if t.twin!=e.id or (e.origin,e.target)!=(t.target,t.origin): raise AssertionError("Twin invariant failed")
            if e.next is None or e.prev is None: raise AssertionError("Incomplete next/prev")
            if self.halfedges[e.next].prev!=e.id or self.halfedges[e.prev].next!=e.id:
                raise AssertionError("Next/prev invariant failed")
        return True

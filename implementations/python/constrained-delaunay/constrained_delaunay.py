"""Polygon-boundary constrained Delaunay triangulation by Lawson flips."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from typing import Iterable, Sequence
from ear_clipping import Triangle, orient, triangulate as ear_triangulate
Point = tuple[Fraction, Fraction]
Edge = tuple[Point, Point]

def _point(value: Sequence[float | int]) -> Point:
    if len(value) != 2: raise ValueError("each vertex must contain exactly x and y")
    return Fraction(str(value[0])), Fraction(str(value[1]))

def _edge(a: Point, b: Point) -> Edge:
    return (a, b) if a < b else (b, a)

def _incircle(a: Point, b: Point, c: Point, d: Point) -> Fraction:
    """Positive iff d lies inside circumcircle abc, for CCW abc."""
    ax, ay = a[0]-d[0], a[1]-d[1]
    bx, by = b[0]-d[0], b[1]-d[1]
    cx, cy = c[0]-d[0], c[1]-d[1]
    return ((ax*ax+ay*ay)*(bx*cy-by*cx)
            -(bx*bx+by*by)*(ax*cy-ay*cx)
            +(cx*cx+cy*cy)*(ax*by-ay*bx))

def _opposite(triangle: Triangle, a: Point, b: Point) -> Point:
    return next(p for p in triangle if p != a and p != b)

def _ccw_triangle(a: Point, b: Point, c: Point) -> Triangle:
    turn=orient(a,b,c)
    if turn == 0: raise ValueError("edge flip would create a degenerate triangle")
    return (a,b,c) if turn > 0 else (a,c,b)

def constrained_delaunay_triangulate(vertices: Iterable[Sequence[float | int]], *,
                                     max_flips: int | None = None) -> list[Triangle]:
    """Triangulate one simple polygon; boundary edges remain constrained.

    Exact rational orientation/incircle predicates are used. Holes, interior
    constraints, Steiner points and quality refinement are not supported.
    Cocircular edges are left unchanged (weakly-Delaunay output).
    """
    ring=[_point(p) for p in vertices]
    if len(ring)>1 and ring[0]==ring[-1]: ring.pop()
    compact=[]
    for p in ring:
        if not compact or p!=compact[-1]: compact.append(p)
    if len(compact)>1 and compact[0]==compact[-1]: compact.pop()
    if len(compact)<3: raise ValueError("a polygon needs at least three distinct vertices")
    if len(set(compact))!=len(compact): raise ValueError("repeated non-consecutive vertices are unsupported")
    triangles=ear_triangulate(compact)
    constraints={_edge(a,b) for a,b in zip(compact,compact[1:]+compact[:1])}
    limit=max_flips if max_flips is not None else max(100,20*len(triangles)**2)
    if not isinstance(limit,int) or isinstance(limit,bool) or limit<0:
        raise ValueError("max_flips must be a non-negative integer")
    flips=0
    while True:
        incidence: dict[Edge,list[int]]=defaultdict(list)
        for index,tri in enumerate(triangles):
            for a,b in ((tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])):
                incidence[_edge(a,b)].append(index)
        changed=False
        for edge,owners in incidence.items():
            if edge in constraints or len(owners)!=2: continue
            u,v=edge
            first,second=triangles[owners[0]],triangles[owners[1]]
            a,b=_opposite(first,u,v),_opposite(second,u,v)
            if orient(u,v,a)*orient(u,v,b)>=0: continue
            if orient(a,b,u)*orient(a,b,v)>=0: continue
            if orient(u,v,a)<0: u,v=v,u
            if _incircle(u,v,a,b)<=0 or _edge(a,b) in incidence: continue
            replacements=(_ccw_triangle(a,b,v),_ccw_triangle(b,a,u))
            for index in sorted(owners,reverse=True): triangles.pop(index)
            triangles.extend(replacements)
            flips+=1
            if flips>limit: raise RuntimeError("edge-flip limit reached; input may be degenerate")
            changed=True
            break
        if not changed: break
    return triangles

def triangle_area(triangle: Triangle) -> Fraction:
    return abs(orient(*triangle))/2

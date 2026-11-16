"""Polygon-boundary constrained Delaunay triangulation by Lawson flips."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from math import isfinite
from typing import Iterable, Sequence
from ear_clipping import (Triangle, _clean_ring, _on_segment,
                          _segments_intersect, _signed_area2, _validate_simple,
                          orient, triangulate as ear_triangulate)
Point = tuple[Fraction, Fraction]
Edge = tuple[Point, Point]

def _point(value: Sequence[float | int]) -> Point:
    if len(value) != 2: raise ValueError("each vertex must contain exactly x and y")
    if any(isinstance(v, float) and not isfinite(v) for v in value):
        raise ValueError("coordinates must be finite")
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
    # Match ear clipping's normalization exactly: consecutive duplicates and
    # redundant collinear boundary vertices are removed before constraints form.
    compact = _clean_ring(_point(p) for p in vertices)
    if len(set(compact)) != len(compact):
        raise ValueError("repeated non-consecutive vertices are unsupported")
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


def _inside_ring(point: Point, ring: Sequence[Point]) -> bool:
    """Return True only for strict interior; points on the boundary return False."""
    x, y = point
    inside = False
    for a, b in zip(ring, list(ring[1:]) + [ring[0]]):
        if _on_segment(a, b, point):
            return False
        if (a[1] > y) != (b[1] > y):
            crossing_x = a[0] + (y-a[1]) * (b[0]-a[0]) / (b[1]-a[1])
            if crossing_x > x:
                inside = not inside
    return inside


def constrained_delaunay_with_diagonals(
    vertices: Iterable[Sequence[float | int]],
    constraints: Iterable[tuple[Sequence[float | int], Sequence[float | int]]],
    *,
    max_flips: int | None = None,
) -> list[Triangle]:
    """Constrained-Delaunay triangulate a simple polygon with non-crossing diagonals.

    Each constraint must join two existing, normalized polygon vertices and
    lie strictly inside the polygon except at its endpoints. Constraints are
    inserted as partition diagonals: the polygon is split into simple pieces,
    and each piece is Lawson-flipped while all of its boundary edges (including
    the supplied diagonals) remain constrained. Holes, Steiner points, crossing
    constraints and segments whose endpoints are not polygon vertices are not
    supported.
    """
    ring = _clean_ring(_point(p) for p in vertices)
    _validate_simple(ring)
    if _signed_area2(ring) < 0:
        ring.reverse()
    if len(set(ring)) != len(ring):
        raise ValueError("repeated non-consecutive vertices are unsupported")
    index = {point: i for i, point in enumerate(ring)}

    parsed: list[tuple[Point, Point]] = []
    seen: set[Edge] = set()
    for raw_a, raw_b in constraints:
        a, b = _point(raw_a), _point(raw_b)
        if a not in index or b not in index:
            raise ValueError("constraint endpoints must be existing normalized polygon vertices")
        if a == b:
            raise ValueError("constraint endpoints must be distinct")
        edge = _edge(a, b)
        if edge in seen:
            raise ValueError("duplicate constraints are not supported")
        seen.add(edge)
        parsed.append((a, b))

    # Reject chords that leave the polygon or touch/cross a non-incident boundary.
    boundary = list(zip(ring, ring[1:] + ring[:1]))
    boundary_edges = {_edge(c, d) for c, d in boundary}
    for a, b in parsed:
        if _edge(a, b) in boundary_edges:
            continue
        for c, d in boundary:
            if c in (a, b) or d in (a, b):
                continue
            if _segments_intersect(a, b, c, d):
                raise ValueError("constraint crosses or touches a non-incident polygon edge")
        midpoint = ((a[0]+b[0])/2, (a[1]+b[1])/2)
        if not _inside_ring(midpoint, ring):
            raise ValueError("constraint must lie in the polygon interior")

    # Distinct constraints may share an endpoint, but may not cross or overlap.
    for i, (a, b) in enumerate(parsed):
        for c, d in parsed[i+1:]:
            shared = set((a, b)) & set((c, d))
            if not _segments_intersect(a, b, c, d):
                continue
            if len(shared) != 1:
                raise ValueError("constraints cross or overlap")
            common = next(iter(shared))
            other_a = b if a == common else a
            other_b = d if c == common else c
            if orient(common, other_a, other_b) == 0:
                raise ValueError("collinear constraints overlap or reverse")

    pieces: list[list[Point]] = [ring]
    for a, b in parsed:
        split_done = False
        for piece_index, piece in enumerate(pieces):
            if a not in piece or b not in piece:
                continue
            ia, ib = piece.index(a), piece.index(b)
            if (ia-ib) % len(piece) in (1, len(piece)-1):
                split_done = True  # already a boundary edge of this piece
                break
            first = piece[ia:ib+1] if ia < ib else piece[ia:] + piece[:ib+1]
            second = piece[ib:ia+1] if ib < ia else piece[ib:] + piece[:ia+1]
            if len(first) < 3 or len(second) < 3:
                raise ValueError("constraint creates a degenerate polygon piece")
            _validate_simple(first)
            _validate_simple(second)
            pieces[piece_index:piece_index+1] = [first, second]
            split_done = True
            break
        if not split_done:
            raise ValueError("constraints are incompatible or do not form an interior partition")

    result: list[Triangle] = []
    for piece in pieces:
        result.extend(constrained_delaunay_triangulate(piece, max_flips=max_flips))
    if len(result) != len(ring)-2:
        raise RuntimeError("constrained partition triangulation did not produce n-2 triangles")
    if sum((triangle_area(t) for t in result), Fraction(0)) != abs(_signed_area2(ring))/2:
        raise RuntimeError("constrained partition triangulation failed exact area conservation")
    return result

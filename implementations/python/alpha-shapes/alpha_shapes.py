"""Planar alpha-shape boundaries from a Delaunay triangulation.

The parameter is a circumradius threshold (not its reciprocal).
"""
from __future__ import annotations
from collections import defaultdict
from math import isfinite
from numbers import Real
from typing import Sequence
import numpy as np
from scipy.spatial import Delaunay, QhullError

Point = tuple[float, float]
Ring = list[Point]

def _normalise(points: Sequence[Sequence[float]]) -> list[Point]:
    result = []
    for point in points:
        if len(point) != 2:
            raise ValueError("each point must have two coordinates")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError("coordinates must be finite")
        result.append((x, y))
    return sorted(set(result))

def _signed_area(ring: Ring) -> float:
    return 0.5 * sum(
        ring[i][0] * ring[(i + 1) % len(ring)][1]
        - ring[(i + 1) % len(ring)][0] * ring[i][1]
        for i in range(len(ring))
    )

def alpha_shape(points: Sequence[Sequence[float]], alpha: Real) -> list[Ring]:
    """Return unclosed boundary rings for triangles with circumradius <= alpha.

    Alpha is a positive distance threshold in the input coordinate units.
    Outer rings are counter-clockwise; hole rings are clockwise. Inputs with
    fewer than three unique or collinear points return no polygon rings.
    """
    if isinstance(alpha, bool) or not isinstance(alpha, Real):
        raise ValueError("alpha must be a positive finite circumradius threshold")
    alpha = float(alpha)
    if not isfinite(alpha) or alpha <= 0:
        raise ValueError("alpha must be a positive finite circumradius threshold")
    pts = _normalise(points)
    if len(pts) < 3:
        return []
    coordinates = np.asarray(pts, dtype=float)
    try:
        triangulation = Delaunay(coordinates)
    except QhullError:
        return []

    # Each undirected edge stores its first CCW orientation and incidence.
    edge_incidence: dict[tuple[int, int], list[int]] = {}
    for simplex in triangulation.simplices:
        a, b, c = map(int, simplex)
        pa, pb, pc = coordinates[[a, b, c]]
        cross = ((pb[0] - pa[0]) * (pc[1] - pa[1])
                 - (pb[1] - pa[1]) * (pc[0] - pa[0]))
        twice_area = abs(float(cross))
        if twice_area == 0:
            continue
        side_a = float(np.linalg.norm(pb - pc))
        side_b = float(np.linalg.norm(pa - pc))
        side_c = float(np.linalg.norm(pa - pb))
        circumradius = side_a * side_b * side_c / (2.0 * twice_area)
        if circumradius > alpha * (1.0 + 1e-12):
            continue
        if cross < 0:
            b, c = c, b
        for u, v in ((a, b), (b, c), (c, a)):
            key = (min(u, v), max(u, v))
            if key in edge_incidence:
                edge_incidence[key][2] += 1
            else:
                edge_incidence[key] = [u, v, 1]

    boundary_edges = [(u, v) for u, v, n in edge_incidence.values() if n == 1]
    if not boundary_edges:
        return []
    outgoing: dict[int, list[int]] = defaultdict(list)
    for u, v in boundary_edges:
        outgoing[u].append(v)
    if any(len(neighbours) != 1 for neighbours in outgoing.values()):
        raise ValueError("alpha complex has a non-manifold boundary")

    unused = set(boundary_edges)
    rings: list[Ring] = []
    while unused:
        start, current = min(unused)
        ring = [pts[start]]
        previous = start
        while current != start:
            edge = (previous, current)
            if edge not in unused:
                raise ValueError("alpha boundary does not form disjoint simple rings")
            unused.remove(edge)
            ring.append(pts[current])
            neighbours = outgoing.get(current, [])
            if len(neighbours) != 1:
                raise ValueError("alpha complex has an open boundary")
            previous, current = current, neighbours[0]
            if len(ring) > len(boundary_edges):
                raise ValueError("alpha boundary failed to close")
        closing_edge = (previous, start)
        if closing_edge not in unused:
            raise ValueError("alpha boundary does not form disjoint simple rings")
        unused.remove(closing_edge)
        if len(ring) >= 3 and _signed_area(ring) != 0:
            rings.append(ring)
    rings.sort(key=lambda ring: (-abs(_signed_area(ring)), -_signed_area(ring), ring[0]))
    return rings


def alpha_shape_3d(points: Sequence[Sequence[float]], alpha: Real) -> dict:
    """Return the boundary triangle mesh of retained 3D Delaunay tetrahedra.

    Alpha is a positive circumradius threshold in coordinate units. This
    returns the boundary of the retained tetrahedron union, not isolated
    lower-dimensional simplices of the full 3D alpha complex.
    """
    if isinstance(alpha, bool) or not isinstance(alpha, Real):
        raise ValueError("alpha must be a positive finite circumradius threshold")
    alpha=float(alpha)
    if not isfinite(alpha) or alpha<=0:
        raise ValueError("alpha must be a positive finite circumradius threshold")
    pts=[]
    for point in points:
        if len(point)!=3:
            raise ValueError("each point must have three coordinates")
        p=tuple(float(v) for v in point)
        if not all(isfinite(v) for v in p):
            raise ValueError("coordinates must be finite")
        pts.append(p)
    pts=sorted(set(pts))
    if len(pts)<4:
        return {"vertices":[],"faces":[]}
    coordinates=np.asarray(pts,dtype=float)
    try:
        triangulation=Delaunay(coordinates)
    except QhullError:
        return {"vertices":[],"faces":[]}
    face_incidence={}
    face_templates=((1,2,3),(0,3,2),(0,1,3),(0,2,1))
    for simplex in triangulation.simplices:
        tet=list(map(int,simplex))
        p=coordinates[tet]
        matrix=2.0*(p[1:]-p[0])
        rhs=np.sum(p[1:]*p[1:],axis=1)-float(p[0]@p[0])
        try:
            centre=np.linalg.solve(matrix,rhs)
        except np.linalg.LinAlgError:
            continue
        radius=float(np.linalg.norm(centre-p[0]))
        if not isfinite(radius):
            raise ValueError("tetrahedron circumradius overflowed")
        if radius>alpha*(1.0+1e-12):
            continue
        orientation=float(np.linalg.det(p[1:]-p[0]))
        if orientation==0:
            continue
        if orientation<0:
            tet[2],tet[3]=tet[3],tet[2]
        for template in face_templates:
            face=tuple(tet[i] for i in template)
            key=tuple(sorted(face))
            if key in face_incidence:
                face_incidence[key][1]+=1
            else:
                face_incidence[key]=[face,1]
    if any(count>2 for _face,count in face_incidence.values()):
        raise ValueError("retained tetrahedra have a non-manifold face incidence")
    boundary=[face for face,count in face_incidence.values() if count==1]
    if not boundary:
        return {"vertices":[],"faces":[]}
    used=sorted({vertex for face in boundary for vertex in face})
    remap={old:new for new,old in enumerate(used)}
    vertices=[pts[i] for i in used]
    faces=[tuple(remap[i] for i in face) for face in boundary]
    return {"vertices":vertices,"faces":faces}

"""Exact-predicate y-monotone partitioning and triangulation for simple polygons.

The module provides a stack triangulator for already-monotone rings and a
start/end/split/merge/regular sweep that partitions general strict-y simple
polygons before triangulation. Horizontal event ties and holes are unsupported.
"""
from __future__ import annotations

from fractions import Fraction
from math import isfinite
from typing import Iterable, Sequence

Point = tuple[Fraction, Fraction]
Triangle = tuple[Point, Point, Point]


def _point(value: Sequence[float | int]) -> Point:
    if len(value) != 2:
        raise ValueError("Each vertex must contain exactly x and y.")
    result = []
    for coordinate in value:
        if isinstance(coordinate, float) and not isfinite(coordinate):
            raise ValueError("Coordinates must be finite.")
        result.append(Fraction(str(coordinate)))
    return result[0], result[1]


def orient(a: Point, b: Point, c: Point) -> Fraction:
    return ((b[0] - a[0]) * (c[1] - a[1]) -
            (b[1] - a[1]) * (c[0] - a[0]))


def _area2(ring: Sequence[Point]) -> Fraction:
    return sum((ring[i][0] * ring[(i + 1) % len(ring)][1] -
                ring[(i + 1) % len(ring)][0] * ring[i][1])
               for i in range(len(ring)))


def _on_segment(a: Point, b: Point, p: Point) -> bool:
    return (orient(a, b, p) == 0 and
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _intersects(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if ((o1 > 0 > o2 or o2 > 0 > o1) and
            (o3 > 0 > o4 or o4 > 0 > o3)):
        return True
    return ((o1 == 0 and _on_segment(a, b, c)) or
            (o2 == 0 and _on_segment(a, b, d)) or
            (o3 == 0 and _on_segment(c, d, a)) or
            (o4 == 0 and _on_segment(c, d, b)))


def _clean(vertices: Iterable[Sequence[float | int]]) -> list[Point]:
    ring = [_point(v) for v in vertices]
    if len(ring) > 1 and ring[0] == ring[-1]:
        ring.pop()
    compact = []
    for p in ring:
        if not compact or compact[-1] != p:
            compact.append(p)
    if len(compact) > 1 and compact[0] == compact[-1]:
        compact.pop()
    if len(compact) < 3 or len(set(compact)) != len(compact):
        raise ValueError("A simple polygon needs at least three distinct vertices.")
    if _area2(compact) == 0:
        raise ValueError("Polygon area must be non-zero.")
    n = len(compact)
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if _intersects(compact[i], compact[(i + 1) % n],
                           compact[j], compact[(j + 1) % n]):
                raise ValueError("Input ring is not a simple polygon.")
    if _area2(compact) < 0:
        compact.reverse()
    return compact


def _monotone_chains(ring: Sequence[Point]) -> tuple[set[int], set[int], int, int]:
    ys = [p[1] for p in ring]
    if len(set(ys)) != len(ys):
        raise ValueError("Polygon is not y-monotone: distinct vertex y-coordinates are required.")
    top = max(range(len(ring)), key=lambda i: ring[i][1])
    bottom = min(range(len(ring)), key=lambda i: ring[i][1])
    n = len(ring)

    forward = []
    i = top
    while True:
        forward.append(i)
        if i == bottom:
            break
        i = (i + 1) % n
    backward = []
    i = top
    while True:
        backward.append(i)
        if i == bottom:
            break
        i = (i - 1) % n

    for chain in (forward, backward):
        if any(ring[chain[k]][1] <= ring[chain[k + 1]][1]
               for k in range(len(chain) - 1)):
            raise ValueError("Polygon is not y-monotone.")
    # For a CCW ring, the forward top-to-bottom chain is the left boundary.
    return set(forward), set(backward), top, bottom


def _ccw(a: Point, b: Point, c: Point) -> Triangle | None:
    turn = orient(a, b, c)
    if turn == 0:
        return None
    return (a, b, c) if turn > 0 else (a, c, b)


def triangulate(vertices: Iterable[Sequence[float | int]]) -> list[Triangle]:
    """Triangulate a strictly y-monotone simple polygon with exact ear clipping.

    The monotone-chain validation is retained, while exact-predicate ear
    clipping is used as a robust reference triangulator. Its worst-case time
    is O(n^2); it avoids fragile floating-point stack-side decisions and
    supports exact area-conservation checks.
    """
    ring = _clean(vertices)
    _monotone_chains(ring)
    active = list(range(len(ring)))
    triangles: list[Triangle] = []

    def point_in_or_on_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
        return (orient(a, b, p) >= 0 and orient(b, c, p) >= 0
                and orient(c, a, p) >= 0)

    def valid_diagonal(previous: int, following: int) -> bool:
        a, b = ring[previous], ring[following]
        for k, u in enumerate(active):
            v = active[(k + 1) % len(active)]
            if u in (previous, following) or v in (previous, following):
                continue
            if _intersects(a, b, ring[u], ring[v]):
                return False
        midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        polygon = [ring[i] for i in active]
        return _inside_ring(polygon, midpoint)

    while len(active) > 3:
        clipped = False
        for position, current in enumerate(active):
            previous = active[position - 1]
            following = active[(position + 1) % len(active)]
            a, b, c = ring[previous], ring[current], ring[following]
            if orient(a, b, c) <= 0:
                continue
            if not valid_diagonal(previous, following):
                continue
            if any(
                point_in_or_on_triangle(ring[other], a, b, c)
                for other in active
                if other not in (previous, current, following)
            ):
                continue
            triangles.append((a, b, c))
            active.pop(position)
            clipped = True
            break
        if not clipped:
            raise RuntimeError(
                "Exact ear clipping found no valid ear; check degeneracies or polygon validity."
            )

    final = _ccw(*(ring[i] for i in active))
    if final is None:
        raise RuntimeError("Final triangulation cell is degenerate.")
    triangles.append(final)
    if len(triangles) != len(ring) - 2:
        raise RuntimeError("Triangulation did not produce exactly n-2 triangles.")
    if sum((abs(orient(*t)) for t in triangles), Fraction(0)) != abs(_area2(ring)):
        raise RuntimeError("Triangulation failed exact area conservation.")
    return triangles

def triangle_area(triangle: Triangle) -> Fraction:
    return abs(orient(*triangle)) / 2


def polygon_area(vertices: Iterable[Sequence[float | int]]) -> Fraction:
    return abs(_area2(_clean(vertices))) / 2


def _edge_x(ring: Sequence[Point], edge: tuple[int, int], y: Fraction) -> Fraction:
    a, b = ring[edge[0]], ring[edge[1]]
    if a[1] == b[1]:
        raise ValueError("Horizontal edges are unsupported by the strict-y sweep.")
    return a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])


def _diagonal_is_valid(ring: Sequence[Point], i: int, j: int) -> bool:
    n = len(ring)
    if i == j or (i - j) % n in (1, n - 1):
        return False
    a, b = ring[i], ring[j]
    for k in range(n):
        l = (k + 1) % n
        if k in (i, j) or l in (i, j):
            continue
        if _intersects(a, b, ring[k], ring[l]):
            return False
    midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return _inside_ring(ring, midpoint)


def _inside_ring(ring: Sequence[Point], point: Point) -> bool:
    x, y = point
    inside = False
    for i, a in enumerate(ring):
        b = ring[(i + 1) % len(ring)]
        if _on_segment(a, b, point):
            return True
        if (a[1] > y) != (b[1] > y):
            crossing_x = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if crossing_x > x:
                inside = not inside
    return inside


def partition_y_monotone(vertices: Iterable[Sequence[float | int]]) -> list[list[Point]]:
    """Partition a simple polygon into strictly y-monotone pieces.

    Uses the standard start/end/split/merge/regular vertex sweep. Input vertices
    must have distinct y-coordinates (so horizontal edges and event ties are
    excluded). The sweep status is a simple Python list: this transparent
    reference implementation is O(n^2) in the worst case, not the O(n log n)
    bound of a balanced-tree implementation. Predicates are exact Fractions.
    """
    ring = _clean(vertices)
    n = len(ring)
    ys = [p[1] for p in ring]
    if len(set(ys)) != n:
        raise ValueError("The partition sweep requires distinct vertex y-coordinates.")
    if any(orient(ring[i - 1], ring[i], ring[(i + 1) % n]) == 0 for i in range(n)):
        raise ValueError("The partition sweep requires no three consecutive collinear vertices.")
    previous = [(i - 1) % n for i in range(n)]
    following = [(i + 1) % n for i in range(n)]
    events = sorted(range(n), key=lambda i: (-ring[i][1], ring[i][0]))
    status: list[tuple[int, int]] = []
    helper: dict[tuple[int, int], int] = {}
    diagonals: list[tuple[int, int]] = []

    def is_convex(v: int) -> bool:
        return orient(ring[previous[v]], ring[v], ring[following[v]]) > 0

    def add_diagonal(a: int, b: int) -> None:
        if a == b or (a - b) % n in (1, n - 1):
            return
        pair = (min(a, b), max(a, b))
        if pair not in diagonals:
            if not _diagonal_is_valid(ring, a, b):
                raise RuntimeError(f"Sweep proposed an invalid diagonal: {a}-{b}.")
            diagonals.append(pair)

    def left_edge(v: int) -> tuple[int, int]:
        vx, vy = ring[v]
        candidates = [( _edge_x(ring, edge, vy), edge) for edge in status
                      if _edge_x(ring, edge, vy) < vx]
        if not candidates:
            raise RuntimeError(f"No status edge lies left of sweep vertex {v}.")
        return max(candidates, key=lambda item: item[0])[1]

    for v in events:
        p, q = previous[v], following[v]
        p_above, q_above = ring[p][1] > ring[v][1], ring[q][1] > ring[v][1]
        p_below, q_below = ring[p][1] < ring[v][1], ring[q][1] < ring[v][1]
        convex = is_convex(v)

        if p_below and q_below:  # start or split
            if convex:
                edge = (v, q)
                status.append(edge)
                helper[edge] = v
            else:
                edge = left_edge(v)
                add_diagonal(v, helper[edge])
                helper[edge] = v
                new_edge = (v, q)
                status.append(new_edge)
                helper[new_edge] = v

        elif p_above and q_above:  # end or merge
            upper_edge = (p, v)
            if upper_edge not in status:
                raise RuntimeError("Sweep status lost an incoming polygon edge.")
            if helper.get(upper_edge) is not None and not is_convex(helper[upper_edge]):
                add_diagonal(v, helper[upper_edge])
            status.remove(upper_edge)
            helper.pop(upper_edge, None)
            if not convex:
                edge = left_edge(v)
                if not is_convex(helper[edge]):
                    add_diagonal(v, helper[edge])
                helper[edge] = v

        else:  # regular vertex
            if p_above and q_below:  # polygon interior lies to the right
                upper_edge = (p, v)
                if upper_edge not in status:
                    raise RuntimeError("Sweep status lost an incoming regular edge.")
                if not is_convex(helper[upper_edge]):
                    add_diagonal(v, helper[upper_edge])
                status.remove(upper_edge)
                helper.pop(upper_edge, None)
                lower_edge = (v, q)
                status.append(lower_edge)
                helper[lower_edge] = v
            else:
                edge = left_edge(v)
                if not is_convex(helper[edge]):
                    add_diagonal(v, helper[edge])
                helper[edge] = v

    pieces: list[list[int]] = [list(range(n))]
    for i, j in diagonals:
        for piece_index, piece in enumerate(pieces):
            if i in piece and j in piece:
                a, b = piece.index(i), piece.index(j)
                if a > b:
                    a, b = b, a
                first = piece[a:b + 1]
                second = piece[b:] + piece[:a + 1]
                if len(first) < 3 or len(second) < 3:
                    raise RuntimeError("A partition diagonal produced a degenerate piece.")
                pieces[piece_index:piece_index + 1] = [first, second]
                break
        else:
            raise RuntimeError("Partition diagonals do not form a valid non-crossing split.")

    result = [[ring[i] for i in piece] for piece in pieces]
    for piece in result:
        _monotone_chains(piece)
    if len(result) != len(diagonals) + 1:
        raise RuntimeError("Partition did not produce one additional piece per diagonal.")
    return result


def triangulate_general(vertices: Iterable[Sequence[float | int]]) -> list[Triangle]:
    """Triangulate a simple strict-y polygon by monotone partition + stack scan."""
    values = list(vertices)
    pieces = partition_y_monotone(values)
    triangles = [triangle for piece in pieces for triangle in triangulate(piece)]
    ring = _clean(values)
    if len(triangles) != len(ring) - 2:
        raise RuntimeError("Partition triangulation did not produce n-2 triangles.")
    if sum((abs(orient(*t)) for t in triangles), Fraction(0)) != abs(_area2(ring)):
        raise RuntimeError("Partition triangulation failed exact area conservation.")
    return triangles

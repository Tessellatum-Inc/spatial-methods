"""Greedy triangle merging for convex decomposition of a simple polygon.

This is a transparent teaching baseline inspired by triangulate-and-merge
approaches. It is not presented as an optimized Hertel-Mehlhorn implementation.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Iterable, Sequence

from ear_clipping import polygon_area, triangulate

Point = tuple[Fraction, Fraction]
RawPoint = Sequence[int | float | str | Fraction]


def _cross(a: Point, b: Point, c: Point) -> Fraction:
    return ((b[0] - a[0]) * (c[1] - b[1])
            - (b[1] - a[1]) * (c[0] - b[0]))


def _dot(a: Point, b: Point) -> Fraction:
    return a[0] * b[0] + a[1] * b[1]


def _sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def _area2(ring: Sequence[Point]) -> Fraction:
    return sum(ring[i][0] * ring[(i + 1) % len(ring)][1]
               - ring[(i + 1) % len(ring)][0] * ring[i][1]
               for i in range(len(ring)))


def _clean(ring: list[Point]) -> list[Point]:
    result: list[Point] = []
    for p in ring:
        if not result or result[-1] != p:
            result.append(p)
    if len(result) > 1 and result[0] == result[-1]:
        result.pop()
    changed = True
    while changed and len(result) >= 3:
        changed = False
        for i, p in enumerate(result):
            prev, nxt = result[i - 1], result[(i + 1) % len(result)]
            incoming, outgoing = _sub(p, prev), _sub(nxt, p)
            if _cross(prev, p, nxt) == 0 and _dot(incoming, outgoing) > 0:
                result.pop(i)
                changed = True
                break
    return result


def _merge_if_convex(a: Sequence[Point], b: Sequence[Point]) -> list[Point] | None:
    """Remove one oppositely directed shared edge if the union stays convex."""
    shared: list[tuple[int, int]] = []
    for i, u in enumerate(a):
        v = a[(i + 1) % len(a)]
        for j, x in enumerate(b):
            y = b[(j + 1) % len(b)]
            if u == y and v == x:
                shared.append((i, j))
    if len(shared) != 1:
        return None

    i, j = shared[0]
    # Walk around A from the shared edge's end back to its start, then around
    # B along its non-shared boundary. The common edge disappears.
    path_a = [a[(i + 1 + k) % len(a)] for k in range(len(a))]
    path_b = [b[(j + 1 + k) % len(b)] for k in range(len(b))]
    candidate = _clean(list(path_a) + list(path_b[1:-1]))
    if len(candidate) < 3 or _area2(candidate) <= 0:
        return None
    if any(_cross(candidate[k - 1], candidate[k],
                  candidate[(k + 1) % len(candidate)]) < 0
           for k in range(len(candidate))):
        return None
    start = min(range(len(candidate)), key=lambda k: (candidate[k][1], candidate[k][0]))
    return candidate[start:] + candidate[:start]


def convex_decompose(vertices: Iterable[RawPoint]) -> list[list[Point]]:
    """Partition one simple polygon ring into convex pieces.

    Ear clipping creates an initial triangulation. Adjacent pieces are then
    greedily merged whenever their shared edge can be removed without creating
    a reflex corner. Coordinates and predicates use exact rational arithmetic.
    The result is a valid convex partition, not necessarily a minimum-cardinality
    partition. Holes and self-intersecting inputs are unsupported.
    """
    ring = list(vertices)
    triangles = triangulate(ring)
    # Maintain piece adjacency by undirected edge. The former implementation
    # rescanned every pair after every successful merge. This worklist only
    # revisits pairs that share an edge with a newly-created piece.
    from collections import deque

    pieces: dict[int, list[Point]] = {i: list(t) for i, t in enumerate(triangles)}
    next_id = len(pieces)
    edge_owners: dict[tuple[Point, Point], set[int]] = {}
    queue: deque[tuple[int, int]] = deque()
    queued: set[tuple[int, int]] = set()

    def edge_key(a: Point, b: Point) -> tuple[Point, Point]:
        return (a, b) if a < b else (b, a)

    def enqueue_pair(a: int, b: int) -> None:
        pair = (a, b) if a < b else (b, a)
        if pair not in queued:
            queued.add(pair)
            queue.append(pair)

    for pid, piece in pieces.items():
        for a, b in zip(piece, piece[1:] + piece[:1]):
            key = edge_key(a, b)
            owners = edge_owners.setdefault(key, set())
            for other in owners:
                enqueue_pair(pid, other)
            owners.add(pid)

    while queue:
        a_id, b_id = queue.popleft()
        if a_id not in pieces or b_id not in pieces:
            continue
        merged = _merge_if_convex(pieces[a_id], pieces[b_id])
        if merged is None:
            continue

        # Remove both old pieces from the edge index before inserting their
        # replacement. Empty owner sets are discarded to keep the index small.
        for pid in (a_id, b_id):
            piece = pieces[pid]
            for a, b in zip(piece, piece[1:] + piece[:1]):
                key = edge_key(a, b)
                owners = edge_owners.get(key)
                if owners is not None:
                    owners.discard(pid)
                    if not owners:
                        del edge_owners[key]
            del pieces[pid]

        merged_id = next_id
        next_id += 1
        pieces[merged_id] = merged
        for a, b in zip(merged, merged[1:] + merged[:1]):
            key = edge_key(a, b)
            owners = edge_owners.setdefault(key, set())
            for other in owners:
                enqueue_pair(merged_id, other)
            owners.add(merged_id)

    result = list(pieces.values())
    expected_area = polygon_area(ring)
    actual_area = sum((abs(_area2(piece)) / 2 for piece in result), Fraction(0))
    if actual_area != expected_area:
        raise RuntimeError("convex partition failed area conservation")
    return result


def hertel_mehlhorn_decompose(
    vertices: Iterable[RawPoint],
) -> list[list[Point]]:
    """Apply a Hertel–Mehlhorn-style diagonal-removal pass to an ear triangulation.

    Each internal diagonal of the *initial* triangulation is considered once.
    It is removed when its two current incident pieces have a convex union.
    Newly-created diagonals are not added to the pass. This is intentionally
    separate from :func:`convex_decompose`, whose repeated worklist can revisit
    newly exposed adjacencies and is a more aggressive greedy variant.

    The triangulation is the dominant cost in this repository's current
    baseline (ear clipping is O(n^3)); this routine does not claim the
    specialized linear-time post-processing bound or a minimum partition.
    """
    from collections import defaultdict

    ring = list(vertices)
    triangles = triangulate(ring)
    pieces: dict[int, list[Point]] = {
        i: list(triangle) for i, triangle in enumerate(triangles)
    }
    if len(pieces) <= 1:
        return list(pieces.values())

    def edge_key(a: Point, b: Point) -> tuple[Point, Point]:
        return (a, b) if a < b else (b, a)

    edge_owners: dict[tuple[Point, Point], set[int]] = defaultdict(set)

    def add_piece(pid: int, piece: Sequence[Point]) -> None:
        for a, b in zip(piece, list(piece[1:]) + [piece[0]]):
            edge_owners[edge_key(a, b)].add(pid)

    for pid, piece in pieces.items():
        add_piece(pid, piece)

    # Freeze the original triangulation's internal diagonals. A diagonal is
    # considered once even if an earlier merge changes its incident pieces.
    original_diagonals = sorted(
        edge for edge, owners in edge_owners.items() if len(owners) == 2
    )
    next_id = len(pieces)
    for diagonal in original_diagonals:
        owners = edge_owners.get(diagonal, set())
        if len(owners) != 2:
            continue
        a_id, b_id = sorted(owners)
        merged = _merge_if_convex(pieces[a_id], pieces[b_id])
        if merged is None:
            continue

        for pid in (a_id, b_id):
            old_piece = pieces.pop(pid)
            for a, b in zip(old_piece, old_piece[1:] + old_piece[:1]):
                key = edge_key(a, b)
                edge_owners[key].discard(pid)
                if not edge_owners[key]:
                    del edge_owners[key]

        merged_id = next_id
        next_id += 1
        pieces[merged_id] = merged
        add_piece(merged_id, merged)

    result = list(pieces.values())
    expected_area = polygon_area(ring)
    actual_area = sum(
        (abs(_area2(piece)) / 2 for piece in result), Fraction(0)
    )
    if actual_area != expected_area:
        raise RuntimeError("Hertel-Mehlhorn pass failed area conservation")
    if any(
        any(_cross(piece[i - 1], piece[i], piece[(i + 1) % len(piece)]) < 0
            for i in range(len(piece)))
        for piece in result
    ):
        raise RuntimeError("Hertel-Mehlhorn pass produced a non-convex piece")
    return result

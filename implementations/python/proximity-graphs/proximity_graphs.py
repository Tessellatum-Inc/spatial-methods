"""Small-input Euclidean proximity graph baselines."""
from __future__ import annotations

from math import hypot, isfinite
from typing import Sequence


def _normalise(points: Sequence[Sequence[float]]) -> list[tuple[float, float]]:
    result = []
    for point in points:
        if len(point) != 2:
            raise ValueError("Each point must have two coordinates")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError("Coordinates must be finite")
        result.append((x, y))
    if len(set(result)) != len(result):
        raise ValueError("Points must be distinct")
    return result


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])


def gabriel_graph(points: Sequence[Sequence[float]]) -> list[tuple[int, int]]:
    """Return edges whose open diameter disk contains no other input point."""
    pts = _normalise(points)
    edges = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            u, v = pts[i], pts[j]
            blocked = False
            for k, w in enumerate(pts):
                if k in (i, j):
                    continue
                # Strictly negative means w is strictly inside the diameter disk.
                dot = (w[0] - u[0]) * (w[0] - v[0]) + (w[1] - u[1]) * (w[1] - v[1])
                if dot < 0:
                    blocked = True
                    break
            if not blocked:
                edges.append((i, j))
    return edges


def relative_neighborhood_graph(points: Sequence[Sequence[float]]) -> list[tuple[int, int]]:
    """Return edges whose open lune contains no third point."""
    pts = _normalise(points)
    edges = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            uv = _distance(pts[i], pts[j])
            blocked = any(
                k not in (i, j)
                and max(_distance(pts[i], w), _distance(pts[j], w)) < uv
                for k, w in enumerate(pts)
            )
            if not blocked:
                edges.append((i, j))
    return edges


def euclidean_mst(points: Sequence[Sequence[float]]) -> list[tuple[int, int, float]]:
    """Kruskal MST over the complete Euclidean graph; O(n^2 log n)."""
    pts = _normalise(points)
    n = len(pts)
    if n <= 1:
        return []
    candidates = sorted(
        (_distance(pts[i], pts[j]), i, j)
        for i in range(n) for j in range(i + 1, n)
    )
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    result = []
    for weight, i, j in candidates:
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        if rank[ri] < rank[rj]:
            ri, rj = rj, ri
        parent[rj] = ri
        if rank[ri] == rank[rj]:
            rank[ri] += 1
        result.append((i, j, weight))
        if len(result) == n - 1:
            break
    return result


def _delaunay_candidate_edges(points: Sequence[Sequence[float]]) -> tuple[list[tuple[float, float]], list[tuple[int, int]]]:
    """Return Delaunay edges for a non-collinear planar point set.

    SciPy/Qhull chooses one valid triangulation when the input is degenerate.
    Consequently this candidate set is not guaranteed to retain every
    boundary-tie edge of a Gabriel graph for cocircular sites.
    """
    pts = _normalise(points)
    if len(pts) < 3:
        raise ValueError("at least three points are required")
    import numpy as np
    from scipy.spatial import Delaunay

    coordinates = np.asarray(pts, dtype=float)
    if np.linalg.matrix_rank(coordinates - coordinates[0]) < 2:
        raise ValueError("sites must not all be collinear")
    triangulation = Delaunay(coordinates)
    candidates = set()
    for a, b, c in triangulation.simplices:
        for u, v in ((a, b), (b, c), (c, a)):
            candidates.add((min(int(u), int(v)), max(int(u), int(v))))
    return pts, sorted(candidates)


def delaunay_filtered_gabriel_graph(points: Sequence[Sequence[float]]) -> list[tuple[int, int]]:
    """Filter Delaunay edges using the open-diameter-disk Gabriel predicate.

    Under general-position Euclidean assumptions, every Gabriel edge is a
    Delaunay edge. The blocker scan is still O(n) per candidate, so this
    transparent filter is O(n^2), not the linear-time specialised algorithm.
    Cocircular boundary ties follow Qhull's chosen triangulation.
    """
    pts, candidates = _delaunay_candidate_edges(points)
    result = []
    for i, j in candidates:
        u, v = pts[i], pts[j]
        blocked = any(
            (w[0] - u[0]) * (w[0] - v[0]) + (w[1] - u[1]) * (w[1] - v[1]) < 0
            for k, w in enumerate(pts) if k not in (i, j)
        )
        if not blocked:
            result.append((i, j))
    return result


def delaunay_filtered_rng(points: Sequence[Sequence[float]]) -> list[tuple[int, int]]:
    """Filter Delaunay edges using the open-lune RNG predicate.

    Under general-position Euclidean assumptions the RNG is contained in the
    Delaunay triangulation. This direct blocker scan is O(n^2) overall; it is
    not Lingas's specialised linear-time post-processing algorithm.
    """
    pts, candidates = _delaunay_candidate_edges(points)
    result = []
    for i, j in candidates:
        uv = _distance(pts[i], pts[j])
        blocked = any(
            max(_distance(pts[i], w), _distance(pts[j], w)) < uv
            for k, w in enumerate(pts) if k not in (i, j)
        )
        if not blocked:
            result.append((i, j))
    return result


def beta_skeleton(points: Sequence[Sequence[float]], beta: float = 2.0
                  ) -> list[tuple[int, int]]:
    """Lune-based beta-skeleton for 1 <= beta <= 2.

    beta=1 is the open-disk Gabriel definition; beta=2 is the open-lune
    relative-neighbourhood definition. Points strictly inside both defining
    disks block an edge; boundary ties do not.
    """
    if not isfinite(beta) or not 1.0 <= beta <= 2.0:
        raise ValueError("this lune-based implementation requires beta in [1, 2]")
    pts = _normalise(points)
    if beta == 1.0:
        return gabriel_graph(pts)
    if beta == 2.0:
        return relative_neighborhood_graph(pts)
    edges = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            u, v = pts[i], pts[j]
            dx, dy = v[0] - u[0], v[1] - u[1]
            distance = hypot(dx, dy)
            radius = beta * distance / 2.0
            c1 = (u[0] + beta * dx / 2.0, u[1] + beta * dy / 2.0)
            c2 = (v[0] - beta * dx / 2.0, v[1] - beta * dy / 2.0)
            radius2 = radius * radius
            boundary_epsilon = 1e-12 * max(1.0, radius2)
            blocked = False
            for k, w in enumerate(pts):
                if k in (i, j):
                    continue
                d1 = (w[0] - c1[0]) ** 2 + (w[1] - c1[1]) ** 2
                d2 = (w[0] - c2[0]) ** 2 + (w[1] - c2[1]) ** 2
                if d1 < radius2 - boundary_epsilon and d2 < radius2 - boundary_epsilon:
                    blocked = True
                    break
            if not blocked:
                edges.append((i, j))
    return edges


def yao_graph(points: Sequence[Sequence[float]], cones: int = 8,
              orientation: float = 0.0) -> list[tuple[int, int]]:
    """Return the undirected union of each point's nearest-neighbour cone choices.

    Each vertex selects at most one nearest point in each equal-angle cone.
    Ties are broken by input index. The output is the undirected union of
    directed selections, not the mutual-choice intersection.
    """
    from math import atan2, pi

    if not isinstance(cones, int) or cones < 3:
        raise ValueError("cones must be an integer of at least 3")
    if not isfinite(orientation):
        raise ValueError("orientation must be finite")
    pts = _normalise(points)
    width = 2.0 * pi / cones
    selected = set()
    for i, origin in enumerate(pts):
        best: dict[int, tuple[float, int]] = {}
        for j, target in enumerate(pts):
            if i == j:
                continue
            dx, dy = target[0] - origin[0], target[1] - origin[1]
            angle = (atan2(dy, dx) - orientation) % (2.0 * pi)
            cone = min(cones - 1, int(angle / width))
            distance2 = dx * dx + dy * dy
            candidate = (distance2, j)
            if cone not in best or candidate < best[cone]:
                best[cone] = candidate
        for _distance2, j in best.values():
            selected.add((min(i, j), max(i, j)))
    return sorted(selected)



def delaunay_euclidean_mst(
    points: Sequence[Sequence[float]],
) -> list[tuple[int, int, float]]:
    """Build an exact Euclidean MST from a sparse Delaunay candidate graph.

    For non-collinear sites, the Euclidean MST is contained in every
    Delaunay triangulation, so Kruskal only needs the O(n) triangulation
    edges. Collinear sites are handled by connecting adjacent points in
    lexicographic order. Complexity is O(n log n) for non-collinear sites.
    """
    pts = _normalise(points)
    n = len(pts)
    if n <= 1:
        return []
    if n == 2:
        return [(0, 1, _distance(pts[0], pts[1]))]

    import numpy as np
    coordinates = np.asarray(pts, dtype=float)
    if np.linalg.matrix_rank(coordinates - coordinates[0]) < 2:
        ordered = sorted(range(n), key=lambda i: (pts[i][0], pts[i][1], i))
        return [
            (min(a, b), max(a, b), _distance(pts[a], pts[b]))
            for a, b in zip(ordered, ordered[1:])
        ]

    _normalised_points, candidate_pairs = _delaunay_candidate_edges(pts)
    candidates = sorted(
        (_distance(pts[i], pts[j]), i, j) for i, j in candidate_pairs
    )
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    result = []
    for weight, i, j in candidates:
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        if rank[ri] < rank[rj]:
            ri, rj = rj, ri
        parent[rj] = ri
        if rank[ri] == rank[rj]:
            rank[ri] += 1
        result.append((i, j, weight))
        if len(result) == n - 1:
            break
    if len(result) != n - 1:
        raise RuntimeError("Delaunay candidate graph did not connect all sites")
    return result


def yao_graph_kdtree(
    points: Sequence[Sequence[float]], cones: int = 8,
    orientation: float = 0.0,
) -> list[tuple[int, int]]:
    """Exact Yao graph using adaptive k-nearest queries in a cKDTree.

    For each source and cone, increase the global-neighbour query size until
    at least one returned point lies in that cone. The nearest such point is
    then the nearest cone point: every unqueried site is at least as far as
    the returned global k-th neighbour. A radius query collects all distance
    ties before input-index tie-breaking. The undirected union is returned.

    Typical sparse queries avoid scanning every site, but adversarial cone
    occupancy can force quadratic work. This is an exact indexed search, not
    the optimal O(n log n) Yao construction.
    """
    from math import atan2, pi
    import numpy as np
    from scipy.spatial import cKDTree

    if not isinstance(cones, int) or isinstance(cones, bool) or cones < 3:
        raise ValueError("cones must be an integer of at least 3")
    if not isfinite(orientation):
        raise ValueError("orientation must be finite")
    pts = _normalise(points)
    n = len(pts)
    if n <= 1:
        return []
    coordinates = np.asarray(pts, dtype=float)
    tree = cKDTree(coordinates)
    width = 2.0 * pi / cones
    selected: set[tuple[int, int]] = set()

    for i, origin in enumerate(pts):
        for cone in range(cones):
            k = 1
            best_index = None
            best_distance = None
            while k < n:
                distances, indices = tree.query(coordinates[i], k=min(k + 1, n))
                distances = np.atleast_1d(distances)
                indices = np.atleast_1d(indices)
                candidates = []
                for distance, j_raw in zip(distances, indices):
                    j = int(j_raw)
                    if j == i or j >= n:
                        continue
                    dx, dy = pts[j][0] - origin[0], pts[j][1] - origin[1]
                    angle = (atan2(dy, dx) - orientation) % (2.0 * pi)
                    if min(cones - 1, int(angle / width)) == cone:
                        candidates.append((float(distance), j))
                if candidates:
                    best_distance = min(item[0] for item in candidates)
                    # Include every exact-distance tie, even if cKDTree's
                    # k-neighbour result cut through a tied set.
                    radius = np.nextafter(best_distance, np.inf)
                    tied = tree.query_ball_point(coordinates[i], radius)
                    eligible = []
                    for j_raw in tied:
                        j = int(j_raw)
                        if j == i:
                            continue
                        dx, dy = pts[j][0] - origin[0], pts[j][1] - origin[1]
                        angle = (atan2(dy, dx) - orientation) % (2.0 * pi)
                        if min(cones - 1, int(angle / width)) == cone:
                            eligible.append((dx * dx + dy * dy, j))
                    if eligible:
                        best_index = min(eligible)[1]
                    break
                if k + 1 >= n:
                    break
                k = min(n - 1, k * 2)
            if best_index is not None:
                selected.add((min(i, best_index), max(i, best_index)))
    return sorted(selected)


def euclidean_mst_prim(
    points: Sequence[Sequence[float]],
) -> list[tuple[int, int, float]]:
    """Build an exact Euclidean MST with dense Prim in O(n²) time, O(n) space.

    Unlike complete-graph Kruskal, this never materialises or sorts all
    O(n²) edges. It is a useful memory-bounded baseline for moderate point
    sets and an independent cross-check for the Delaunay-candidate MST.
    Equal candidate weights are resolved by vertex index, then parent index.
    """
    pts = _normalise(points)
    n = len(pts)
    if n <= 1:
        return []

    in_tree = [False] * n
    best = [float("inf")] * n
    parent = [-1] * n
    best[0] = 0.0
    result: list[tuple[int, int, float]] = []

    for _ in range(n):
        vertex = min(
            (i for i in range(n) if not in_tree[i]),
            key=lambda i: (best[i], i),
        )
        if best[vertex] == float("inf"):
            raise RuntimeError("complete Euclidean graph unexpectedly disconnected")
        in_tree[vertex] = True
        if parent[vertex] != -1:
            a, b = parent[vertex], vertex
            result.append((min(a, b), max(a, b), best[vertex]))

        for other in range(n):
            if in_tree[other] or other == vertex:
                continue
            weight = _distance(pts[vertex], pts[other])
            if (weight < best[other]
                    or (weight == best[other]
                        and (parent[other] == -1 or vertex < parent[other]))):
                best[other] = weight
                parent[other] = vertex

    return result


def delaunay_filtered_beta_skeleton(
    points: Sequence[Sequence[float]], beta: float = 2.0,
) -> list[tuple[int, int]]:
    """Build a lune-based beta-skeleton from Delaunay edges with indexed blockers.

    For 1 <= beta <= 2, beta-skeleton edges are Delaunay candidates in
    general position. A cKDTree radius query restricts blocker checks to the
    first defining disk; every candidate is still tested against both disks.
    Expected work is sparse on well-distributed inputs, but worst-case work
    remains quadratic. Cocircular tie limitations follow Qhull's triangulation.
    """
    import numpy as np
    from scipy.spatial import cKDTree

    if isinstance(beta, bool) or not isinstance(beta, (int, float)) or not isfinite(beta) or not 1.0 <= beta <= 2.0:
        raise ValueError("beta must be a finite number in [1, 2]")
    pts, edges = _delaunay_candidate_edges(points)
    coordinates = np.asarray(pts, dtype=float)
    tree = cKDTree(coordinates)
    result = []
    for i, j in edges:
        u, v = pts[i], pts[j]
        dx, dy = v[0] - u[0], v[1] - u[1]
        distance = hypot(dx, dy)
        radius = beta * distance / 2.0
        c1 = (u[0] + beta * dx / 2.0, u[1] + beta * dy / 2.0)
        c2 = (v[0] - beta * dx / 2.0, v[1] - beta * dy / 2.0)
        radius2 = radius * radius
        epsilon = 1e-12 * max(1.0, radius2)
        blocked = False
        # The first disk is a necessary condition for a point to block the
        # lune. query_ball_point is inclusive; the exact strict test follows.
        for k_raw in tree.query_ball_point(c1, np.nextafter(radius, np.inf)):
            k = int(k_raw)
            if k == i or k == j:
                continue
            w = pts[k]
            d1 = (w[0] - c1[0]) ** 2 + (w[1] - c1[1]) ** 2
            d2 = (w[0] - c2[0]) ** 2 + (w[1] - c2[1]) ** 2
            if d1 < radius2 - epsilon and d2 < radius2 - epsilon:
                blocked = True
                break
        if not blocked:
            result.append((i, j))
    return result

"""Conservative triangle-mesh cleanup and orientation repair.

This is a combinatorial/coordinate cleanup utility, not a general hole filler,
self-intersection resolver, or geometric remesher.
"""
from collections import defaultdict, deque
from math import floor, isfinite, sqrt
from collections.abc import Sequence


def repair_triangle_mesh(vertices: Sequence[Sequence[float]],
                         faces: Sequence[Sequence[int]], *,
                         weld_tolerance: float = 0.0):
    """Return (vertices, faces, report) after conservative mesh cleanup.

    Steps: validate inputs; optionally weld vertices within Euclidean tolerance
    using neighbouring spatial-hash cells; drop collapsed/zero-area and
    duplicate triangles; reject edges with >2 incident faces; orient each
    connected face component consistently; compact unused vertices.

    The returned vertex coordinates are tuples of floats. Face indices refer
    to the compacted vertex array. Welding is greedy in input vertex order:
    each point maps to the first previously accepted point within tolerance.
    """
    if weld_tolerance < 0 or not isfinite(weld_tolerance):
        raise ValueError("weld_tolerance must be finite and non-negative")
    coords = []
    for i, point in enumerate(vertices):
        if len(point) != 3:
            raise ValueError(f"vertex {i} must have three coordinates")
        p = tuple(float(v) for v in point)
        if not all(isfinite(v) for v in p):
            raise ValueError(f"vertex {i} has non-finite coordinates")
        coords.append(p)

    mapped = []
    kept = []
    cells = defaultdict(list)
    tol2 = weld_tolerance * weld_tolerance
    for i, p in enumerate(coords):
        target = None
        if weld_tolerance > 0:
            cell = tuple(floor(v / weld_tolerance) for v in p)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        for candidate in cells[(cell[0]+dx, cell[1]+dy, cell[2]+dz)]:
                            q = kept[candidate]
                            if sum((p[k]-q[k])**2 for k in range(3)) <= tol2:
                                target = candidate
                                break
                        if target is not None:
                            break
                    if target is not None:
                        break
                if target is not None:
                    break
        if target is None:
            target = len(kept)
            kept.append(p)
            if weld_tolerance > 0:
                cells[tuple(floor(v / weld_tolerance) for v in p)].append(target)
        mapped.append(target)

    cleaned, seen = [], set()
    removed_collapsed = removed_duplicate = 0
    for fi, face in enumerate(faces):
        if len(face) != 3:
            raise ValueError(f"face {fi} must be triangular")
        tri = tuple(face)
        if any(not isinstance(v, int) or v < 0 or v >= len(coords) for v in tri):
            raise ValueError(f"face {fi} has an out-of-range vertex")
        tri = tuple(mapped[v] for v in tri)
        if len(set(tri)) != 3 or _area2(kept, tri) == 0.0:
            removed_collapsed += 1
            continue
        key = tuple(sorted(tri))
        if key in seen:
            removed_duplicate += 1
            continue
        seen.add(key)
        cleaned.append(tri)

    # Edge incidence also supplies the parity constraint for orientation:
    # adjacent faces must traverse their common edge in opposite directions.
    incidence = defaultdict(list)
    for fi, tri in enumerate(cleaned):
        for k, u in enumerate(tri):
            v = tri[(k+1) % 3]
            incidence[tuple(sorted((u, v)))].append((fi, u, v))
    for edge, uses in incidence.items():
        if len(uses) > 2:
            raise ValueError(f"non-manifold edge {edge} has more than two incident faces")

    adjacency = [[] for _ in cleaned]
    for edge, uses in incidence.items():
        if len(uses) == 2:
            (a, u1, v1), (b, u2, v2) = uses
            same_direction = (u1, v1) == (u2, v2)
            adjacency[a].append((b, same_direction))
            adjacency[b].append((a, same_direction))

    flips = [None] * len(cleaned)
    components = 0
    for root in range(len(cleaned)):
        if flips[root] is not None:
            continue
        components += 1
        flips[root] = False
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b, must_differ in adjacency[a]:
                expected = flips[a] ^ must_differ
                if flips[b] is None:
                    flips[b] = expected
                    queue.append(b)
                elif flips[b] != expected:
                    raise ValueError("surface component is non-orientable or inconsistently constrained")

    oriented = [tuple(reversed(tri)) if flips[i] else tri
                for i, tri in enumerate(cleaned)]
    used = sorted({v for tri in oriented for v in tri})
    compact = {old: new for new, old in enumerate(used)}
    out_vertices = tuple(kept[v] for v in used)
    out_faces = tuple(tuple(compact[v] for v in tri) for tri in oriented)
    report = {
        "input_vertices": len(vertices),
        "input_faces": len(faces),
        "welded_vertices": len(vertices) - len(kept),
        "removed_collapsed_faces": removed_collapsed,
        "removed_duplicate_faces": removed_duplicate,
        "removed_unreferenced_vertices": len(kept) - len(used),
        "flipped_faces": sum(bool(v) for v in flips),
        "face_components": components,
    }
    return out_vertices, out_faces, report


def _area2(vertices, tri):
    a, b, c = (vertices[i] for i in tri)
    ab = tuple(b[k]-a[k] for k in range(3))
    ac = tuple(c[k]-a[k] for k in range(3))
    cross = (ab[1]*ac[2]-ab[2]*ac[1],
             ab[2]*ac[0]-ab[0]*ac[2],
             ab[0]*ac[1]-ab[1]*ac[0])
    return sqrt(sum(v*v for v in cross))

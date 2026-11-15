"""Conservative isotropic-style triangular surface remeshing.

Operations are local and topology-checked after each edit. This educational
baseline is intentionally slower than production remeshers.
"""
from collections import defaultdict
from math import acos, sqrt, isfinite


def _edge_faces(faces):
    out = defaultdict(list)
    for fi, tri in enumerate(faces):
        for k, u in enumerate(tri):
            v = tri[(k + 1) % 3]
            out[tuple(sorted((u, v)))].append(fi)
    return out


def _dist(a, b):
    return sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def _mid(a, b):
    return tuple((a[i] + b[i]) * 0.5 for i in range(3))


def _valid(vertices, faces):
    """Dependency-free combinatorial manifold/orientation check."""
    incidence = defaultdict(list)
    for fi, tri in enumerate(faces):
        if len(tri) != 3 or len(set(tri)) != 3:
            return False
        if any(not isinstance(v, int) or v < 0 or v >= len(vertices) for v in tri):
            return False
        for k, u in enumerate(tri):
            v = tri[(k + 1) % 3]
            incidence[tuple(sorted((u, v)))].append((fi, u, v))
    if any(len(uses) > 2 for uses in incidence.values()):
        return False
    for uses in incidence.values():
        if len(uses) == 2 and uses[0][1:] != uses[1][1:][::-1]:
            return False
    links = [defaultdict(set) for _ in vertices]
    for tri in faces:
        for i, v in enumerate(tri):
            a, b = tri[(i + 1) % 3], tri[(i + 2) % 3]
            links[v][a].add(b)
            links[v][b].add(a)
    for link in links:
        if not link:
            continue
        degrees = [len(x) for x in link.values()]
        if any(d not in (1, 2) for d in degrees) or sum(d == 1 for d in degrees) not in (0, 2):
            return False
        seen, stack = set(), [next(iter(link))]
        while stack:
            v = stack.pop()
            if v not in seen:
                seen.add(v)
                stack.extend(link[v] - seen)
        if len(seen) != len(link):
            return False
    return True


def split_edge(vertices, faces, edge):
    """Bisect one edge and all incident faces; return new mesh or unchanged."""
    u, v = edge
    incidence = _edge_faces(faces)
    if edge not in incidence:
        return vertices, faces, False
    midpoint = len(vertices)
    out = []
    for tri in faces:
        if u in tri and v in tri:
            k = next(i for i in range(3)
                     if {tri[i], tri[(i + 1) % 3]} == {u, v})
            a, b, c = tri[k], tri[(k + 1) % 3], tri[(k + 2) % 3]
            out.extend(((a, midpoint, c), (midpoint, b, c)))
        else:
            out.append(tri)
    new_vertices = tuple(vertices) + (_mid(vertices[u], vertices[v]),)
    new_faces = tuple(out)
    return (new_vertices, new_faces, True) if _valid(new_vertices, new_faces) else (vertices, faces, False)


def collapse_edge(vertices, faces, edge, *, boundary_edges=None):
    """Collapse edge to its midpoint, rejecting invalid manifold results.

    A boundary edge may collapse only when both endpoints are boundary
    vertices. Interior-to-boundary collapses are prohibited.
    """
    u, v = edge
    incidence = _edge_faces(faces)
    if edge not in incidence:
        return vertices, faces, False
    boundary_edges = boundary_edges if boundary_edges is not None else {
        e for e, fs in incidence.items() if len(fs) == 1
    }
    boundary_vertices = {x for e in boundary_edges for x in e}
    if (u in boundary_vertices) != (v in boundary_vertices):
        return vertices, faces, False
    # Collapsing an interior chord between boundary vertices can erase or
    # pinch the boundary even though both endpoints are boundary vertices.
    if u in boundary_vertices and edge not in boundary_edges:
        return vertices, faces, False
    replacement = _mid(vertices[u], vertices[v])
    out, seen = [], set()
    for tri in faces:
        mapped = tuple(u if x == v else x for x in tri)
        if len(set(mapped)) < 3:
            continue
        key = tuple(sorted(mapped))
        if key in seen:
            return vertices, faces, False
        seen.add(key)
        out.append(mapped)
    new_vertices = list(vertices)
    new_vertices[u] = replacement
    # Keep indices stable during the pass; compact only after all operations.
    new_faces = tuple(out)
    if not _valid(new_vertices, new_faces):
        return vertices, faces, False
    return tuple(new_vertices), new_faces, True


def flip_edge(vertices, faces, edge):
    """Flip an interior edge when the minimum local angle strictly improves."""
    incidence = _edge_faces(faces)
    incident = incidence.get(edge, [])
    if len(incident) != 2:
        return vertices, faces, False
    f0, f1 = incident
    t0, t1 = faces[f0], faces[f1]
    u, v = edge
    a = next(x for x in t0 if x not in edge)
    b = next(x for x in t1 if x not in edge)
    if a == b or tuple(sorted((a, b))) in incidence:
        return vertices, faces, False
    # Orient replacement triangles consistently with the original pair.
    # Extract cyclic order so the shared edge is u->v in the first face.
    if not any(t0[i] == u and t0[(i + 1) % 3] == v for i in range(3)):
        u, v = v, u
    replacements = ((a, b, v), (b, a, u))
    if not _valid(vertices, tuple(t for i, t in enumerate(faces)
                                  if i not in (f0, f1)) + replacements):
        return vertices, faces, False
    before = min(_min_angle(vertices, t0), _min_angle(vertices, t1))
    after = min(_min_angle(vertices, replacements[0]),
                _min_angle(vertices, replacements[1]))
    if after <= before + 1e-12:
        return vertices, faces, False
    out = list(faces)
    out[f0], out[f1] = replacements
    return vertices, tuple(out), True


def _min_angle(vertices, tri):
    p = [vertices[i] for i in tri]
    angles = []
    for i in range(3):
        a = _dist(p[(i + 1) % 3], p[i])
        b = _dist(p[(i + 2) % 3], p[i])
        c = _dist(p[(i + 1) % 3], p[(i + 2) % 3])
        if a == 0 or b == 0:
            return 0.0
        cosv = max(-1.0, min(1.0, (a*a + b*b - c*c) / (2*a*b)))
        angles.append(acos(cosv))
    return min(angles)


def _vertex_normals(vertices, faces):
    normals = [[0.0, 0.0, 0.0] for _ in vertices]
    for tri in faces:
        p, q, r = (vertices[i] for i in tri)
        a = tuple(q[k]-p[k] for k in range(3))
        b = tuple(r[k]-p[k] for k in range(3))
        n = (a[1]*b[2]-a[2]*b[1],
             a[2]*b[0]-a[0]*b[2],
             a[0]*b[1]-a[1]*b[0])
        for vi in tri:
            for k in range(3):
                normals[vi][k] += n[k]
    return normals


def tangential_relax(vertices, faces, *, iterations=1, factor=0.2,
                     pin_boundary=True):
    """Move vertices toward neighbour averages projected to tangent planes."""
    if iterations < 0 or not 0 <= factor <= 1:
        raise ValueError("iterations must be >=0 and factor in [0, 1]")
    incidence = _edge_faces(faces)
    boundary = {v for e, fs in incidence.items() if len(fs) == 1 for v in e}
    neighbours = [set() for _ in vertices]
    for u, v in incidence:
        neighbours[u].add(v)
        neighbours[v].add(u)
    current = tuple(tuple(p) for p in vertices)
    for _ in range(iterations):
        normals = _vertex_normals(current, faces)
        updated = list(current)
        for vi, ns in enumerate(neighbours):
            if not ns or (pin_boundary and vi in boundary):
                continue
            avg = tuple(sum(current[j][k] for j in ns)/len(ns) for k in range(3))
            delta = tuple(avg[k]-current[vi][k] for k in range(3))
            n = normals[vi]
            nn = sum(x*x for x in n)
            if nn > 1e-24:
                dot = sum(delta[k]*n[k] for k in range(3))/nn
                delta = tuple(delta[k]-dot*n[k] for k in range(3))
            updated[vi] = tuple(current[vi][k]+factor*delta[k] for k in range(3))
        current = tuple(updated)
    return current


def isotropic_remesh(vertices, faces, target_length, *, iterations=3,
                     split_ratio=4/3, collapse_ratio=4/5,
                     relax_factor=0.2, relax_iterations=1,
                     preserve_boundary=True):
    """Run split/collapse/flip and tangential relaxation passes.

    The operation order is long-edge splitting, short-edge collapsing,
    quality-improving flips, then tangential relaxation. Boundary edges are
    protected from collapse when preserve_boundary is true.
    """
    if not isfinite(target_length) or target_length <= 0:
        raise ValueError("target_length must be finite and positive")
    if iterations < 0 or split_ratio <= 1 or not 0 < collapse_ratio < 1:
        raise ValueError("invalid iteration or edge-ratio parameters")
    if not _valid(vertices, faces):
        raise ValueError("input must be a consistently oriented manifold triangle mesh")
    vertices, faces = tuple(tuple(map(float, p)) for p in vertices), tuple(tuple(t) for t in faces)
    if any(len(p) != 3 or not all(isfinite(x) for x in p) for p in vertices):
        raise ValueError("vertices must be finite 3D coordinates")
    counts = {"splits": 0, "collapses": 0, "flips": 0}
    for _ in range(iterations):
        # Snapshot candidates; edits re-evaluate topology before committing.
        edges = list(_edge_faces(faces))
        for edge in edges:
            if _dist(vertices[edge[0]], vertices[edge[1]]) > split_ratio*target_length:
                vertices, faces, changed = split_edge(vertices, faces, edge)
                counts["splits"] += int(changed)
        incidence = _edge_faces(faces)
        boundary = {e for e, fs in incidence.items() if len(fs) == 1}
        for edge in list(incidence):
            if _dist(vertices[edge[0]], vertices[edge[1]]) < collapse_ratio*target_length:
                if preserve_boundary and (edge in boundary or
                                          edge[0] in {v for e in boundary for v in e} or
                                          edge[1] in {v for e in boundary for v in e}):
                    continue
                vertices, faces, changed = collapse_edge(
                    vertices, faces, edge, boundary_edges=boundary)
                counts["collapses"] += int(changed)
        for edge in list(_edge_faces(faces)):
            vertices, faces, changed = flip_edge(vertices, faces, edge)
            counts["flips"] += int(changed)
        vertices = tangential_relax(vertices, faces, iterations=relax_iterations,
                                    factor=relax_factor,
                                    pin_boundary=preserve_boundary)
    # Compact unused vertices and remap connectivity.
    used = sorted({v for tri in faces for v in tri})
    remap = {old: new for new, old in enumerate(used)}
    vertices = tuple(vertices[i] for i in used)
    faces = tuple(tuple(remap[v] for v in tri) for tri in faces)
    if not _valid(vertices, faces):
        raise RuntimeError("remesher produced invalid topology")
    return vertices, faces, counts
